import os
import json
import sqlite3
import urllib.request
import re
from datetime import datetime
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel
import uvicorn
from export_pdf import generar_pdf_oficial
import eeff_engine

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
DB_PATH = os.path.join(BASE_DIR, "sigep.db")

app = FastAPI(title="SIGEP Bolivia - Sistema Presupuestario y Contable")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS comprobantes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero_cbte TEXT,
        fecha TEXT,
        entidad TEXT,
        momento_codigo TEXT,
        momento_desc TEXT,
        beneficiario TEXT,
        monto_total REAL,
        datos_json TEXT,
        created_at TEXT,
        updated_at TEXT
    )
    """)
    conn.commit()
    conn.close()

init_db()

class ComprobanteSaveRequest(BaseModel):
    id: int | None = None
    numero_cbte: str
    fecha: str
    entidad: str
    momento_codigo: str
    momento_desc: str
    beneficiario: str
    monto_total: float
    datos: dict

def read_json_file(filename: str):
    file_path = os.path.join(DATA_DIR, filename)
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Live BCB indicators fetcher
@app.get("/api/indicadores-bcb")
def get_indicadores_bcb():
    url = "https://www.bcb.gob.bo"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=6) as r:
            html = r.read().decode("utf-8", errors="ignore")
        
        ufv = None
        m_ufv = re.search(r'bcb-quote-name">UFV</div>\s*<div class="bcb-quote-unit">Bs/UFV</div>\s*</div>\s*<div class="bcb-quote-value">([0-9.,]+)</div>', html)
        if m_ufv:
            ufv = m_ufv.group(1).replace(",", ".")
        else:
            m_alt = re.search(r'UFV.*?([23]\.\d{5})', html.replace(",", "."))
            if m_alt:
                ufv = m_alt.group(1)

        return {
            "status": "ok",
            "fuente": "Banco Central de Bolivia (BCB Oficial en Línea)",
            "ufv": ufv if ufv else "3.36081",
            "tipo_cambio": "6.86",
            "tc_compra": "6.86",
            "tc_venta": "6.96",
            "fecha_consulta": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
    except Exception as e:
        return {
            "status": "offline_fallback",
            "fuente": "Banco Central de Bolivia (Oficial)",
            "ufv": "3.36081",
            "tipo_cambio": "6.86",
            "tc_compra": "6.86",
            "tc_venta": "6.96",
            "error": str(e),
            "fecha_consulta": datetime.now().strftime("%d/%m/%Y %H:%M")
        }

@app.get("/api/catalogo")
def get_catalogo():
    return {
        "partidas_gasto": read_json_file("clasificador_gastos.json"),
        "rubros_recurso": read_json_file("clasificador_recursos.json"),
        "plan_cuentas": read_json_file("plan_cuentas.json"),
        "momentos": read_json_file("momentos.json"),
        "fuentes_organismos": read_json_file("fuentes_organismos.json"),
        "plantillas": read_json_file("plantillas_academicas.json")
    }

@app.get("/api/comprobantes")
def list_comprobantes():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, numero_cbte, fecha, entidad, momento_codigo, momento_desc, beneficiario, monto_total, datos_json, created_at, updated_at 
        FROM comprobantes ORDER BY id ASC
    """)
    rows = cursor.fetchall()
    comprobantes = []
    for row in rows:
        item = dict(row)
        try:
            item["datos"] = json.loads(item["datos_json"]) if item.get("datos_json") else {}
        except Exception:
            item["datos"] = {}
        comprobantes.append(item)
    conn.close()
    return comprobantes

@app.get("/api/comprobantes/{cbte_id}")
def get_comprobante(cbte_id: int):
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comprobantes WHERE id = ?", (cbte_id,))
    row = cursor.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Comprobante no encontrado")
    item = dict(row)
    item["datos"] = json.loads(item["datos_json"])
    return item

@app.post("/api/comprobantes")
def save_comprobante(req: ComprobanteSaveRequest):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    datos_str = json.dumps(req.datos, ensure_ascii=False)

    target_id = None
    if req.id:
        cursor.execute("SELECT id FROM comprobantes WHERE id = ?", (req.id,))
        row = cursor.fetchone()
        if row:
            target_id = row[0]

    # Si no encontró por ID, verificar si ya existe por número de comprobante para actualizar
    if not target_id and req.numero_cbte:
        cursor.execute("SELECT id FROM comprobantes WHERE numero_cbte = ?", (req.numero_cbte,))
        row = cursor.fetchone()
        if row:
            target_id = row[0]

    if target_id:
        cursor.execute("""
            UPDATE comprobantes 
            SET numero_cbte = ?, fecha = ?, entidad = ?, momento_codigo = ?, momento_desc = ?, beneficiario = ?, monto_total = ?, datos_json = ?, updated_at = ?
            WHERE id = ?
        """, (req.numero_cbte, req.fecha, req.entidad, req.momento_codigo, req.momento_desc, req.beneficiario, req.monto_total, datos_str, now_str, target_id))
        cbte_id = target_id
    else:
        cursor.execute("""
            INSERT INTO comprobantes (numero_cbte, fecha, entidad, momento_codigo, momento_desc, beneficiario, monto_total, datos_json, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (req.numero_cbte, req.fecha, req.entidad, req.momento_codigo, req.momento_desc, req.beneficiario, req.monto_total, datos_str, now_str, now_str))
        cbte_id = cursor.lastrowid
    
    conn.commit()
    conn.close()

    # Invalidar caché de Estados Financieros para que se recalculen automáticamente con los nuevos comprobantes
    try:
        eeff_engine.invalidate_eeff_cache()
    except Exception:
        pass

    return {"status": "ok", "id": cbte_id, "numero_cbte": req.numero_cbte, "message": "Comprobante guardado con éxito"}

@app.delete("/api/comprobantes/{cbte_id}")
def delete_comprobante(cbte_id: int):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comprobantes WHERE id = ?", (cbte_id,))
    conn.commit()
    conn.close()

    # Invalidar caché de Estados Financieros para que se recalculen automáticamente
    try:
        eeff_engine.invalidate_eeff_cache()
    except Exception:
        pass

    return {"status": "ok", "message": "Comprobante eliminado"}

@app.get("/api/descargar-respaldo-db")
def descargar_respaldo_db():
    if os.path.exists(DB_PATH):
        return FileResponse(DB_PATH, filename="sigep_respaldo_comprobantes.db", media_type="application/octet-stream")
    raise HTTPException(status_code=404, detail="Base de datos no encontrada")

@app.get("/api/descargar-pdf-oficial")
def descargar_pdf_oficial():
    pdf_path = os.path.join(BASE_DIR, "COMPROBANTES_SIGEP_OFICIALES.pdf")
    try:
        generar_pdf_oficial(pdf_path)
    except Exception as e:
        print(f"Error generando PDF: {e}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Error al generar el PDF: {str(e)}")

    if os.path.exists(pdf_path):
        return FileResponse(
            pdf_path, 
            filename="COMPROBANTES_SIGEP_OFICIALES.pdf", 
            media_type="application/pdf"
        )
    raise HTTPException(status_code=500, detail="Error al generar el PDF")

# ========================================================
# ENDPOINTS: LIBRO MAYOR Y ESTADOS FINANCIEROS (EEFF)
# ========================================================
@app.get("/api/mayores")
def api_get_mayores():
    try:
        return eeff_engine.get_mayores(DB_PATH)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eeff")
def api_get_all_eeff(recalculate: bool = False):
    try:
        return eeff_engine.load_all_eeff(DB_PATH, force_recompute=recalculate)
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eeff/{report_id}")
def api_get_eeff_report(report_id: str):
    try:
        all_rep = eeff_engine.load_all_eeff(DB_PATH)
        if report_id not in all_rep:
            raise HTTPException(status_code=404, detail="Estado financiero no encontrado")
        return all_rep[report_id]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/eeff/{report_id}")
async def api_save_eeff_report(report_id: str, payload: dict):
    try:
        res = eeff_engine.save_eeff_custom(report_id, payload)
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/eeff/{report_id}/reset")
def api_reset_eeff_report(report_id: str):
    try:
        fresh_data = eeff_engine.reset_eeff_report(report_id)
        if not fresh_data:
            raise HTTPException(status_code=404, detail="Reporte no encontrado")
        return fresh_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/eeff/{report_id}/download-docx")
def api_download_eeff_docx(report_id: str):
    try:
        out_path = eeff_engine.generate_eeff_docx(report_id)
        if out_path and os.path.exists(out_path):
            filename_map = {
                "balance_general": "01_Balance_General.docx",
                "recursos_gastos_corrientes": "02_Estado_de_Recursos_y_Gastos_Corrientes.docx",
                "flujo_efectivo": "03_Flujo_de_Caja.docx",
                "ejecucion_presupuesto_recursos": "04_Ejecucion_Presupuesto_de_Recursos.docx",
                "ejecucion_presupuesto_gastos": "05_Ejecucion_Presupuesto_de_Gastos.docx",
                "cuenta_ahorro_inversion_financiamiento": "06_Cuenta_Ahorro_Inversion_Financiamiento.docx",
                "cambios_patrimonio_neto": "07_Estado_de_Cambios_en_el_Patrimonio_Neto.docx",
                "estado_cuentas_complementaria": "08_Estado_de_Cuenta_Informacion_Complementaria.docx"
            }
            fname = filename_map.get(report_id, f"{report_id}.docx")
            return FileResponse(
                out_path,
                filename=fname,
                media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )
        raise HTTPException(status_code=500, detail="No se pudo generar el documento Word")
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

static_dir = os.path.join(BASE_DIR, "static")
os.makedirs(static_dir, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def read_root():
    index_file = os.path.join(BASE_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return HTMLResponse("<h1>SIGEP Iniciado</h1>")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print("Iniciando Sistema SIGEP...")
    print(f"Puerto activo: {port}")
    print("Acceso Local: http://127.0.0.1:" + str(port))
    print("Acceso Móvil / Red WiFi: http://0.0.0.0:" + str(port))
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
