import os, json

base_dir = r"E:\Programa ing inversa\Proyecto Sigep"
data_dir = os.path.join(base_dir, "data")

def load_j(name):
    p = os.path.join(data_dir, name)
    if os.path.exists(p):
        with open(p, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

plantillas = [
    {
        "id": "caso_manuscrito_devengado_servicios",
        "titulo": "Ejercicio 1: Venta de Servicios, Carátulas y Timbres (Devengado de Recursos)",
        "descripcion": "Del apunte manuscrito de clase: Venta de servicios por Bs. 2,900 (Formularios Bs. 200, Carátula municipal Bs. 2000, Timbres Bs. 700) según arqueo de caja e informe del cajero.",
        "comprobante": {
            "entidad": "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN",
            "direccion": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "unidad_ejecutora": "001",
            "unidad_ejecutora_desc": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "numero_cbte": "0000001",
            "fecha": "10/09/2026",
            "hora": "10:30:00",
            "momento_codigo": "12",
            "momento_desc": "Devengado de Recursos",
            "moneda": "BBS",
            "tipo_cambio": "6.86",
            "dolar": "6.86",
            "ufv": "3.36081",
            "doc_respaldo": "INFORME DEL CAJERO, ARQUEO DE CAJA",
            "depositante": "DISTINTOS BENEFICIARIOS",
            "beneficiario": "DISTINTOS BENEFICIARIOS",
            "elaborado_por": "Alejandro Cazas Tarqui",
            "glosa": "REGISTRO POR LA VENTA DE SERVICIOS, FORMULARIOS (BS. 200), CARATULAS MUNICIPALES (BS. 2000) Y TIMBRES (BS. 700) A DISTINTOS BENEFICIARIOS SEGUN ARQUEO DE CAJA E INFORME DEL CAJERO.",
            "grid_rows": [
                {
                    "rubro": "",
                    "cta": "11310",
                    "descripcion": "CUENTAS A COBRAR A CORTO PLAZO",
                    "presupuesto": "0.00",
                    "debe": "2900.00",
                    "haber": "0.00"
                },
                {
                    "rubro": "",
                    "cta": "52200",
                    "descripcion": "VENTA DE SERVICIOS",
                    "presupuesto": "0.00",
                    "debe": "0.00",
                    "haber": "2900.00"
                },
                {
                    "rubro": "12200",
                    "cta": "",
                    "descripcion": "VENTA DE SERVICIOS DE LAS ADMINISTRACIONES PUBLICAS",
                    "presupuesto": "2900.00",
                    "debe": "0.00",
                    "haber": "0.00"
                }
            ]
        }
    },
    {
        "id": "caso_foto_san_joaquin",
        "titulo": "Ejercicio 2: Compra de Papel, Limpieza y Útiles al Contado (C-D-P / GCT)",
        "descripcion": "El comprobante oficial de la primera foto: GAM San Joaquín compra de papel, limpieza y útiles con cheque de Banco Unión por Bs. 18,000.",
        "comprobante": {
            "entidad": "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN",
            "direccion": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "unidad_ejecutora": "001",
            "unidad_ejecutora_desc": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "numero_cbte": "0000004",
            "fecha": "10 Enero 2021",
            "hora": "21:25:45",
            "momento_codigo": "09",
            "momento_desc": "Compromiso-Devengado-Pagado (GCT)",
            "moneda": "BBS",
            "tipo_cambio": "6.86",
            "dolar": "6.86",
            "ufv": "3.36081",
            "doc_respaldo": "COTIZACIONES, ORDEN DE COMPRA...",
            "depositante": 'Libreria y Papeleria "POMPEYA"',
            "beneficiario": 'Libreria y Papeleria "POMPEYA"',
            "elaborado_por": "Alejandro Cazas Tarqui",
            "glosa": "REGISTRO PARA CONTABILIZAR LA COMPRA DE: LIBRERIA Y PAPELERIA POMPEYA DE: PAPEL DE ESCRITORIO, MATERIAL DE LIMPIEZA Y UTILES DE ESCRITORIO Y OFICINA, PARA EL FUNCIONAMIENTO DEL EJECUTIVO MUNICIPAL DEL GOBIERNO AUTONOMO MUNICIPAL DE SAN JOAQUIN, SEGUN FACTURA Nº 005240 QUE SE ADJUNTA.",
            "grid_rows": [
                {
                    "rubro": "32100",
                    "cta": "11510",
                    "descripcion": "Papel de Escritorio",
                    "presupuesto": "3000.00",
                    "debe": "3000.00",
                    "haber": "0.00"
                },
                {
                    "rubro": "39100",
                    "cta": "11510",
                    "descripcion": "Material de Limpieza",
                    "presupuesto": "5000.00",
                    "debe": "5000.00",
                    "haber": "0.00"
                },
                {
                    "rubro": "39500",
                    "cta": "11510",
                    "descripcion": "Útiles de Escritorio y Oficina",
                    "presupuesto": "10000.00",
                    "debe": "10000.00",
                    "haber": "0.00"
                },
                {
                    "rubro": "",
                    "cta": "11124",
                    "descripcion": "Cuentas Fiscales Banco Unión - Chq. 2001",
                    "presupuesto": "0.00",
                    "debe": "0.00",
                    "haber": "18000.00"
                }
            ]
        }
    }
]

with open(os.path.join(data_dir, "plantillas_academicas.json"), "w", encoding="utf-8") as f:
    json.dump(plantillas, f, ensure_ascii=False, indent=2)

payload = {
    "partidas_gasto": load_j("clasificador_gastos.json"),
    "rubros_recurso": load_j("clasificador_recursos.json"),
    "plan_cuentas": load_j("plan_cuentas.json"),
    "momentos": load_j("momentos.json"),
    "fuentes_organismos": load_j("fuentes_organismos.json"),
    "plantillas": plantillas
}

with open(os.path.join(base_dir, "static", "data_embedded.js"), "w", encoding="utf-8") as f:
    f.write("window.SIGEP_EMBEDDED_DATA = " + json.dumps(payload, ensure_ascii=False) + ";\n")

print("Plantillas y data_embedded.js actualizados correctamente!")
