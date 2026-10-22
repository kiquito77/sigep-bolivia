"""Generador del Comprobante de Contabilidad con la geometría del SIGEP oficial.

Coordenadas tomadas de `jcbte.frx` (unidad FRU: 1/10000 in) y verificadas contra una
impresión real del sistema (`C:\\sgp2021\\rep\\Ultimo.txt`).

Uso:
    python oficial_pdf.py --sample            # Cbte 0000006 (el de la muestra oficial)
    python oficial_pdf.py --db 12             # un comprobante de sigep.db
    python oficial_pdf.py --db 12 --out x.pdf
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas

IN = 72.0
BASE = Path(__file__).resolve().parent
DB = BASE.parent / "sigep.db"

# --- geometría del reporte (pulgadas, origen arriba-izquierda) -----------------
ANCHO = 11.167
ALTO_CONTENIDO = 4.80
ESCALA = 11.0 / ANCHO          # encaja en Carta horizontal (11 in)

COL = {
    "ap": 0.167, "part": 1.281, "cta": 1.917, "cheque": 2.823,
    "l": 3.93, "dh": 4.16, "desc": 4.40,
    "parcial": 8.657, "debe": 9.854, "haber": 10.948,
}
FILA_Y = 1.500
FILA_ALTO = 0.115


class Hoja:
    """Dibuja en pulgadas con origen arriba-izquierda."""

    def __init__(self, c: canvas.Canvas, ancho_in: float, alto_in: float):
        self.c = c
        self.ancho_px = ancho_in * IN
        self.alto_px = alto_in * IN

    def x(self, v: float) -> float:
        return v * IN * ESCALA

    def y(self, v: float) -> float:
        return self.alto_px - v * IN * ESCALA

    def texto(self, x, y, s, size=6, fuente="Helvetica", alineacion="left", gris=0):
        if not s:
            return
        c = self.c
        c.setFont(fuente, size * ESCALA)
        c.setFillGray(gris)
        px, py = self.x(x), self.y(y)
        if alineacion == "right":
            c.drawRightString(px, py, str(s))
        elif alineacion == "center":
            c.drawCentredString(px, py, str(s))
        else:
            c.drawString(px, py, str(s))
        c.setFillGray(0)

    def linea(self, x1, y1, x2, y2, grosor=0.6):
        self.c.setLineWidth(grosor)
        self.c.line(self.x(x1), self.y(y1), self.x(x2), self.y(y2))

    def caja(self, x, y, ancho, alto, grosor=0.6):
        self.c.setLineWidth(grosor)
        self.c.rect(self.x(x), self.y(y + alto), ancho * IN * ESCALA, alto * IN * ESCALA)


def dibujar(h: Hoja, d: dict) -> None:
    # ---------------- encabezado izquierdo: institución / sigla / unidad
    h.texto(0.05, 0.12, d.get("entidad", ""), 7.5, "Helvetica-Bold")
    h.texto(0.05, 0.26, d.get("unidad_desc", ""), 8)
    direccion = d.get("direccion", "")
    if direccion and direccion != d.get("unidad_desc"):
        h.texto(0.05, 0.40, direccion, 8)

    # ---------------- encabezado derecho: fecha / hora / página
    h.texto(8.79, 0.12, "Fecha de Imp.:", 8)
    h.texto(9.77, 0.12, d.get("fecha_imp", ""), 8)
    h.texto(8.79, 0.26, "Hora de Imp.:", 8)
    h.texto(9.77, 0.26, d.get("hora", ""), 8)
    h.texto(8.79, 0.40, "Pagina Numero:", 8)
    h.texto(9.77, 0.40, d.get("pagina", "1"), 8)

    # ---------------- título y número
    h.texto(4.667 + 3.281 / 2, 0.50, "C O M P R O B A N T E   D E   C O N T A B I L I D A D",
            8, "Helvetica-Bold", "center")
    h.texto(9.10, 0.60, "Validado", 6, alineacion="right")
    h.texto(9.25, 0.60, "Cbte No.", 6)
    h.texto(9.85, 0.74, d.get("numero", ""), 8, "Helvetica-Bold", "center")

    # ---------------- datos del comprobante
    h.texto(0.333, 0.74, "Unidad Ejecutora :", 8)
    h.texto(1.72, 0.74, d.get("unidad", ""), 8)
    h.texto(2.10, 0.74, d.get("unidad_desc", ""), 8)

    h.texto(0.333, 0.875, "Cod. Transac. :", 8)
    h.texto(1.44, 0.875, d.get("codtr", ""), 8)
    h.texto(1.75, 0.875, d.get("codtr_desc", ""), 8)
    h.texto(4.75, 0.875, "Cod.Trans.Resp.:", 8)
    h.texto(5.85, 0.875, d.get("codtr1", ""), 8)
    if d.get("codtr1"):
        h.texto(6.05, 0.875, "Reversion de " + d.get("codtr1_desc", ""), 8)
    h.texto(9.00, 0.875, "Fecha Cbte.:", 6, alineacion="right")
    h.texto(9.05, 0.875, d.get("fecha", ""), 8)

    h.texto(0.333, 1.00, "Moneda :", 8)
    h.texto(1.083, 1.00, d.get("moneda", ""), 8)
    h.texto(1.417, 1.00, d.get("moneda_desc", ""), 8)
    h.texto(4.75, 1.00, "T/C :", 8)
    h.texto(5.55, 1.00, d.get("cambio", ""), 8)
    h.texto(6.40, 1.00, "UFV :", 6)
    h.texto(6.75, 1.00, d.get("ufv", ""), 6)
    h.texto(8.677, 1.00, "Documento Respaldo:", 6)
    h.texto(9.677, 1.00, (d.get("docres") or "")[:52], 6)

    # ---------------- cabecera de la grilla
    h.linea(0.10, 1.14, 11.10, 1.14)
    h.texto(0.667, 1.20, "CODIGO", 6, alineacion="center")
    h.texto(1.490, 1.20, "PART.", 6, alineacion="center")
    h.texto(2.330, 1.20, "CODIGO", 6, alineacion="center")
    h.texto(3.400, 1.20, "CHEQUE", 6, alineacion="center")
    h.texto(4.160, 1.20, "D", 6, alineacion="center")
    h.texto(4.400, 1.20, "DESCRIPCION DE LAS CUENTAS", 6, "Helvetica-Bold")
    h.texto(8.657, 1.20, "PARCIALES", 6, alineacion="right")
    h.texto(9.854, 1.20, "DEBE", 6, alineacion="right")
    h.texto(10.948, 1.20, "HABER", 6, alineacion="right")
    h.texto(0.667, 1.33, "PRESUP.", 6, alineacion="center")
    h.texto(1.490, 1.33, "PRESUP.", 6, alineacion="center")
    h.texto(2.330, 1.33, "CONTABLE", 6, alineacion="center")
    h.texto(3.400, 1.33, "NUMERO (A)", 6, alineacion="center")
    h.texto(4.400, 1.33, ".................PRESUPUESTO..................", 6)
    h.linea(0.10, 1.42, 11.10, 1.42)
    h.linea(0.10, 1.14, 0.10, 1.42)

    # ---------------- filas
    y = FILA_Y
    for fila in d.get("filas", [])[:7]:
        h.texto(COL["ap"], y, fila.get("ap", ""), 6)
        h.texto(COL["part"], y, fila.get("part", ""), 6)
        h.texto(COL["cta"], y, fila.get("cta", ""), 6)
        h.texto(COL["cheque"], y, fila.get("cheque", ""), 6)
        h.texto(COL["l"], y, fila.get("l", ""), 6, alineacion="right")
        h.texto(COL["dh"], y, fila.get("dh", ""), 6, alineacion="center")
        h.texto(COL["desc"], y, (fila.get("desc", "") or "")[:78], 6)
        h.texto(COL["parcial"], y, fila.get("parcial", ""), 6, alineacion="right")
        h.texto(COL["debe"], y, fila.get("debe", ""), 6, alineacion="right")
        h.texto(COL["haber"], y, fila.get("haber", ""), 6, alineacion="right")
        y += FILA_ALTO

    # ---------------- totales
    h.linea(0.10, 2.260, 11.10, 2.260)
    h.texto(6.30, 2.345, "T O T A L E S", 8, "Helvetica-Bold")
    h.texto(COL["parcial"], 2.345, d.get("total_parcial", ""), 6, alineacion="right")
    h.texto(COL["debe"], 2.345, d.get("total_debe", ""), 6, alineacion="right")
    h.texto(COL["haber"], 2.345, d.get("total_haber", ""), 6, alineacion="right")
    h.linea(0.10, 2.400, 11.10, 2.400)

    # ---------------- importe en letras
    h.texto(0.20, 2.475, d.get("literal", ""), 6, "Helvetica-Bold")

    # ---------------- beneficiario / transacción
    h.caja(0.10, 2.62, 5.75, 1.20)
    h.caja(5.92, 2.62, 5.18, 1.20)
    h.texto(0.18, 2.75, "Beneficiario :", 6, "Helvetica-Bold")
    h.texto(6.00, 2.75, "Descripcion de la Transaccion :", 6, "Helvetica-Bold")
    for i, ln in enumerate(d.get("bene_lineas", [])[:4]):
        h.texto(0.20, 2.92 + i * 0.14, ln, 6)
    for i, ln in enumerate(d.get("glosa_lineas", [])[:7]):
        h.texto(6.00, 2.92 + i * 0.14, ln, 6)

    # ---------------- firmas
    h.caja(0.10, 3.95, 6.50, 0.50)
    etiquetas = ["ELABORADO POR", "REVISADO", "APROBADO", "APROBADO", "APROBADO"]
    for i, et in enumerate(etiquetas):
        h.texto(0.10 + 0.30 + i * 1.30, 4.31, et, 6)
    for x in (1.55, 2.81, 3.99, 5.22):
        h.linea(x, 3.95, x, 4.45)
    h.texto(0.20, 3.88, d.get("elaborado_por", ""), 6)

    # ---------------- pie
    h.texto(0.10, 4.66, "(R)(R) SigepMV, V.9.0.0 (R)(R)", 6)
    h.texto(7.20, 4.66, d.get("pie_datos", ""), 6)


def hoja_nueva(c, d, ancho_in=11.0, alto_in=8.5):
    h = Hoja(c, ancho_in, alto_in)
    dibujar(h, d)
    c.showPage()


def generar_salida(pdf: Path, comprobantes: list[dict]) -> Path:
    pdf.parent.mkdir(parents=True, exist_ok=True)
    c = canvas.Canvas(str(pdf), pagesize=landscape(letter))
    for d in comprobantes:
        hoja_nueva(c, d, 11.0, 8.5)
    c.save()
    return pdf


# ------------------------------------------------------------------ datos
def muestra() -> dict:
    """Cbte 0000006 tal como aparece en rep\\Ultimo.txt."""
    return {
        "entidad": "1814 - GM - GOBIERNO AUTONOMO MUNICIPAL DE SAN JOAQUIN",
        "unidad_desc": "ALEJANDRO CAZAS TARQUI",
        "direccion": "",
        "numero": "0000006",
        "unidad": "001",
        "codtr": "02",
        "codtr_desc": "Compromiso (PPT)",
        "codtr1": "",
        "fecha": "15 Enero 2021",
        "moneda": "BBS",
        "moneda_desc": "Bolivianos",
        "cambio": "6.86",
        "ufv": "2.35801",
        "docres": "CONTRATO",
        "fecha_imp": "21/10/2026",
        "hora": "17:03:00",
        "pagina": "1",
        "filas": [
            {"ap": "170000000287", "part": "", "cta": "", "cheque": "", "l": "",
             "dh": "", "desc": "CONST. ENLOSETADO DE CALLES CIUDAD DE SAN JOAQUIN  (SAN JOAQUIN)"},
            {"ap": "", "part": "42000", "cta": "", "cheque": "", "l": "", "dh": "",
             "desc": "Construcciones"},
            {"ap": "", "part": "42300", "cta": "", "cheque": "", "l": "", "dh": "",
             "desc": "Construcciones y Mejoras de Bienes Nacionales de Dominio Publico"},
            {"ap": "", "part": "42310", "cta": "43/413 0000", "cheque": "G", "l": "1", "dh": "D",
             "desc": "Construcciones y Mejoras de Bienes de Dominio Publico",
             "parcial": "2,903,560.00"},
            {"ap": "", "part": "", "cta": "Referencias", "cheque": "", "l": "1", "dh": "",
             "desc": ". . . . . . . Fuentes Utilizadas. . . . . . ."},
            {"ap": "", "part": "43/413", "cta": "", "cheque": "", "l": "", "dh": "",
             "desc": "Transferencias de Credito Externo/Fondo Financiero para el"},
            {"ap": "", "part": "0000", "cta": "", "cheque": "", "l": "", "dh": "",
             "desc": ". . . . . . .Entidades Utilizadas. . . . . . ."},
        ],
        "total_parcial": "2,903,560.00",
        "total_debe": "2,903,560.00",
        "total_haber": "",
        "literal": "Son: DOS MILLONES NOVECIENTOS TRES MIL QUINIENTOS SESENTA 00/100 Bs.",
        "bene_lineas": ['Empresa Constructora "GRIMALDI y Cia."'],
        "glosa_lineas": [
            'REGISTRO PARA CONTABILIZAR LA FIRMA DE CONTRATO CON LA EMPRESA CONSTRUCTORA',
            '"GRIMALDI y Cia." PARA LA CONSTRUCCION ENLOSETADO DE CALLES CIUDAD DE SAN',
            "JOAQUIN, DEL GOBIERNO AUTONOMO MUNICIPAL DE SAN JOAQUIN, SEGUN CONTRATO QUE SE",
            "ADJUNTA..",
        ],
        "elaborado_por": "Alejandro Cazas Tarqui",
        "pie_datos": "C:\\SGP2021\\DATA\\",
    }


def desde_db(cbte_id: int) -> dict:
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    row = conn.execute("SELECT * FROM comprobantes WHERE id = ?", (cbte_id,)).fetchone()
    conn.close()
    if not row:
        raise SystemExit(f"no existe el comprobante id={cbte_id}")
    d = json.loads(row["datos_json"]) if row["datos_json"] else {}
    filas = []
    for r in d.get("grid_rows", []):
        debe = float(r.get("debe") or 0)
        haber = float(r.get("haber") or 0)
        filas.append({
            "ap": "", "part": r.get("rubro", ""), "cta": r.get("cta", ""), "cheque": "",
            "l": "", "dh": "D" if debe else ("H" if haber else ""),
            "desc": r.get("descripcion", ""),
            "debe": f"{debe:,.2f}" if debe else "",
            "haber": f"{haber:,.2f}" if haber else "",
        })
    total_d = sum(float(r.get("debe") or 0) for r in d.get("grid_rows", []))
    total_h = sum(float(r.get("haber") or 0) for r in d.get("grid_rows", []))
    return {
        "entidad": d.get("entidad", ""),
        "unidad_desc": d.get("unidad_ejecutora_desc", ""),
        "direccion": d.get("direccion", ""),
        "numero": row["numero_cbte"],
        "unidad": d.get("unidad_ejecutora", "001"),
        "codtr": d.get("momento_codigo", ""),
        "codtr_desc": d.get("momento_desc", ""),
        "codtr1": "",
        "fecha": d.get("fecha", ""),
        "moneda": d.get("moneda", "BBS"),
        "moneda_desc": "Bolivianos",
        "cambio": d.get("tipo_cambio", d.get("dolar", "")),
        "ufv": d.get("ufv", ""),
        "docres": d.get("doc_respaldo", ""),
        "fecha_imp": d.get("fecha", ""),
        "hora": d.get("hora", ""),
        "filas": filas,
        "total_debe": f"{total_d:,.2f}" if total_d else "",
        "total_haber": f"{total_h:,.2f}" if total_h else "",
        "literal": "",
        "bene_lineas": [d.get("beneficiario") or d.get("depositante", "")],
        "glosa_lineas": [d.get("glosa", "")],
        "elaborado_por": d.get("elaborado_por", ""),
        "pie_datos": "C:\\SGP2021\\DATA\\",
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--db", type=int)
    ap.add_argument("--all", action="store_true", help="todos los comprobantes de sigep.db")
    ap.add_argument("--out", type=Path)
    args = ap.parse_args()

    if args.all:
        conn = sqlite3.connect(DB)
        ids = [r[0] for r in conn.execute("SELECT id FROM comprobantes ORDER BY id")]
        conn.close()
        datos = [desde_db(i) for i in ids]
        salida = args.out or (BASE / "oficial" / "comprobantes_replica.pdf")
        print(f"comprobantes: {len(datos)}")
    elif args.sample or args.db is None:
        datos = [muestra()]
        salida = args.out or (BASE / "oficial" / "muestra_oficial.pdf")
    else:
        datos = [desde_db(args.db)]
        salida = args.out or (BASE / "oficial" / f"cbte_{args.db}.pdf")

    generar_salida(salida, datos)
    print("PDF:", salida)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
