import os, json

target_dir = r"E:\Programa ing inversa\Proyecto Sigep"
data_dir = os.path.join(target_dir, "data")
os.makedirs(data_dir, exist_ok=True)

momentos = [
    {
        "codigo": "15",
        "sigla": "IDP",
        "nombre": "Ingreso Devengado - Percibido",
        "tipo": "RECURSO",
        "descripcion": "Ingreso simultáneo donde se reconoce el derecho a percibir y se realiza el cobro efectivo en ventanilla bancaria o caja.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Venta de servicios, valores, patentes municipales, timbres, formularios"
    },
    {
        "codigo": "09",
        "sigla": "GCT",
        "nombre": "Compromiso-Devengado-Pagado (GCT)",
        "tipo": "GASTO",
        "descripcion": "Gasto Corriente Total simultáneo. Se ejecuta la partida presupuestaria y se realiza el pago contable inmediato con cheque o banco.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Compra directa con cheque/transferencia (Librería Pompeya, limpieza, útiles)"
    },
    {
        "codigo": "08",
        "sigla": "CD",
        "nombre": "Compromiso-Devengado (CD)",
        "tipo": "GASTO",
        "descripcion": "Compromiso y Devengado simultáneo al recibir bienes o servicios a crédito / pendiente de pago a proveedores.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Recepción de activos o materiales con factura por pagar"
    },
    {
        "codigo": "01",
        "sigla": "PREV",
        "nombre": "Preventivo de Gasto",
        "tipo": "GASTO",
        "descripcion": "Reserva previa de asignación presupuestaria antes de iniciar el proceso de contratación. No genera asiento patrimonial contable.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": False,
        "ejemplo": "Inicio de licitación pública o cotización para obras o consultorías"
    },
    {
        "codigo": "02",
        "sigla": "COMP",
        "nombre": "Compromiso de Gasto",
        "tipo": "GASTO",
        "descripcion": "Suscripción del contrato o emisión de Orden de Compra formal con el proveedor.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": False,
        "ejemplo": "Firma de contrato de provisión o adjudicación"
    },
    {
        "codigo": "03",
        "sigla": "DEV",
        "nombre": "Devengado de Gasto",
        "tipo": "GASTO",
        "descripcion": "Recepción definitiva del bien o servicio prestado (conformidad de almacén o supervisión). Nace la obligación contable por pagar.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Recepción de mercadería o activos según acta de entrega"
    },
    {
        "codigo": "04",
        "sigla": "PAG",
        "nombre": "Pagado de Gasto",
        "tipo": "GASTO",
        "descripcion": "Desembolso efectivo mediante cheque o transferencia SIGEP al beneficiario para cancelar un devengado previo.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Emisión de cheque de pago al contratista con retenciones"
    },
    {
        "codigo": "12",
        "sigla": "DEVR",
        "nombre": "Devengado de Recursos",
        "tipo": "RECURSO",
        "descripcion": "Reconocimiento del derecho exigible de cobro por venta de servicios, impuestos, tasas o transferencias pendientes.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Liquidación de venta de servicios o patentes por cobrar"
    },
    {
        "codigo": "13",
        "sigla": "PERC",
        "nombre": "Percibido de Recursos",
        "tipo": "RECURSO",
        "descripcion": "Ingreso efectivo de fondos en las cuentas corrientes fiscales o caja proveniente de un recurso devengado.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Cobro de liquidación impositiva o venta de servicios devengada"
    },
    {
        "codigo": "07",
        "sigla": "PCD",
        "nombre": "Preventivo-Compromiso-Devengado (PCD)",
        "tipo": "GASTO",
        "descripcion": "Integración de los 3 momentos para contrataciones directas.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Servicios de imprenta urgente o pasajes"
    },
    {
        "codigo": "10",
        "sigla": "DP",
        "nombre": "Devengado-Pagado (DP)",
        "tipo": "GASTO",
        "descripcion": "Devengado y cancelación simultánea sin compromiso previo.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": True,
        "ejemplo": "Pago de viáticos o gastos de representación de emergencia"
    },
    {
        "codigo": "21",
        "sigla": "EST",
        "nombre": "Estimación de Recursos",
        "tipo": "RECURSO",
        "descripcion": "Cálculo o presupuestación anual proyectada de los ingresos en el POA.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": False,
        "ejemplo": "Aprobación del Presupuesto Operativo Anual de Recursos"
    },
    {
        "codigo": "32",
        "sigla": "MOD",
        "nombre": "Modificación Presupuestaria / Traspaso",
        "tipo": "PRESUPUESTO",
        "descripcion": "Traspaso intrainstitucional de crédito presupuestario entre partidas de gasto o proyectos.",
        "afecta_presupuesto": True,
        "afecta_contabilidad": False,
        "ejemplo": "Traspaso de partida 22110 a 39500 para compra de útiles"
    },
    {
        "codigo": "40",
        "sigla": "AJUSTE",
        "nombre": "Asiento de Ajuste / Contabilidad Pura",
        "tipo": "CONTABLE",
        "descripcion": "Registro de operaciones contables financieras sin afectación presupuestaria.",
        "afecta_presupuesto": False,
        "afecta_contabilidad": True,
        "ejemplo": "Depreciación de activos fijos, regularización de fondos en avance"
    }
]

with open(os.path.join(data_dir, "momentos.json"), "w", encoding="utf-8") as f:
    json.dump(momentos, f, ensure_ascii=False, indent=2)

fuentes = [
    {"codigo": "20/210", "ff": "20", "of": "210", "nombre": "Recursos Específicos / Gobiernos Autónomos Municipales"},
    {"codigo": "10/111", "ff": "10", "of": "111", "nombre": "Tesoro General de la Nación (TGN)"},
    {"codigo": "41/119", "ff": "41", "of": "119", "nombre": "Transferencias TGN - Coparticipación Tributaria"},
    {"codigo": "41/113", "ff": "41", "of": "113", "nombre": "Transferencias TGN - Impuesto Directo a los Hidrocarburos (IDH)"},
    {"codigo": "20/220", "ff": "20", "of": "220", "nombre": "Regalías y Participaciones"},
    {"codigo": "42/230", "ff": "42", "of": "230", "nombre": "Transferencias de Recursos Específicos"}
]

with open(os.path.join(data_dir, "fuentes_organismos.json"), "w", encoding="utf-8") as f:
    json.dump(fuentes, f, ensure_ascii=False, indent=2)

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
            "ufv": "2.40000",
            "doc_respaldo": "INFORME DEL CAJERO, ARQUEO DE CAJA",
            "depositante": "DISTINTOS BENEFICIARIOS",
            "beneficiario": "DISTINTOS BENEFICIARIOS",
            "elaborado_por": "Alejandro Cazas Tarqui",
            "glosa": "REGISTRO POR LA VENTA DE SERVICIOS, FORMULARIOS (BS. 200), CARATULAS MUNICIPALES (BS. 2000) Y TIMBRES (BS. 700) A DISTINTOS BENEFICIARIOS SEGUN ARQUEO DE CAJA E INFORME DEL CAJERO.",
            "grid_rows": [
                {
                    "ap": "0000000000",
                    "gasto": "",
                    "recurso": "12200",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11310",
                    "aux": "CAJERO",
                    "oec": "001",
                    "debe": "2900.00",
                    "haber": "0.00",
                    "descripcion": "Cuentas a Cobrar a Corto Plazo / Venta de Servicios de las Adm. Públicas"
                },
                {
                    "ap": "0000000000",
                    "gasto": "",
                    "recurso": "12200",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "41100",
                    "aux": "SERV-PUB",
                    "oec": "001",
                    "debe": "0.00",
                    "haber": "2900.00",
                    "descripcion": "Venta de Servicios de las Administraciones Públicas (Presupuesto Recursos)"
                }
            ],
            "filas_presupuesto": [
                {
                    "codigo_presup": "20/210 0000",
                    "partida": "12200",
                    "partida_tipo": "R",
                    "codigo_contable": "11310",
                    "cheque": "",
                    "linea": "1",
                    "descripcion": "Venta de Servicios de las Administraciones Públicas (Formularios, Carátulas y Timbres)",
                    "dh": "H",
                    "parcial": "2900.00",
                    "es_encabezado": False
                }
            ],
            "filas_contabilidad": [
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11310",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Cuentas a Cobrar a Corto Plazo",
                    "dh": "D",
                    "parcial": "",
                    "debe": "2900.00",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "41100",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Venta de Bienes y Servicios de las Administraciones Públicas",
                    "dh": "H",
                    "parcial": "",
                    "debe": "",
                    "haber": "2900.00",
                    "es_encabezado": False
                }
            ]
        }
    },
    {
        "id": "caso_manuscrito_percibido_servicios",
        "titulo": "Ejercicio 2: Ingreso Devengado - Percibido (Código 15 - IDP)",
        "descripcion": "El caso directo mostrado en 'quiero que sea así': Cobro inmediato en efectivo/banco por venta de servicios y valores municipales.",
        "comprobante": {
            "entidad": "1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN",
            "direccion": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "unidad_ejecutora": "001",
            "unidad_ejecutora_desc": "DIRECCION ADMINISTRATIVA Y FINANCIERA",
            "numero_cbte": "0000002",
            "fecha": "31/12/2021",
            "hora": "12:00:00",
            "momento_codigo": "15",
            "momento_desc": "Ingreso Devengado - Percibido",
            "moneda": "BBS",
            "tipo_cambio": "6.86",
            "ufv": "2.40000",
            "doc_respaldo": "BOLETA DE RECAUDACION FISCAL Nº 8492, LIBRO DE CAJA",
            "depositante": "CONTRIBUYENTES VARIOS",
            "beneficiario": "CONTRIBUYENTES VARIOS",
            "elaborado_por": "Alejandro Cazas Tarqui",
            "glosa": "RECAUDACION DIRECTA POR INGRESO DEVENGADO Y PERCIBIDO POR VENTA DE SERVICIOS Y VALORES MUNICIPALES INGRESADOS A CAJA CENTRAL.",
            "grid_rows": [
                {
                    "ap": "0000000000",
                    "gasto": "",
                    "recurso": "12200",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11111",
                    "aux": "CAJA-MN",
                    "oec": "001",
                    "debe": "2900.00",
                    "haber": "0.00",
                    "descripcion": "Caja Moneda Nacional - Recaudación en Ventanilla"
                },
                {
                    "ap": "0000000000",
                    "gasto": "",
                    "recurso": "12200",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "41100",
                    "aux": "ING-SERV",
                    "oec": "001",
                    "debe": "0.00",
                    "haber": "2900.00",
                    "descripcion": "Venta de Bienes y Servicios Municipales"
                }
            ],
            "filas_presupuesto": [
                {
                    "codigo_presup": "20/210 0000",
                    "partida": "12200",
                    "partida_tipo": "R",
                    "codigo_contable": "11111",
                    "cheque": "",
                    "linea": "1",
                    "descripcion": "Venta de Servicios de las Administraciones Públicas",
                    "dh": "H",
                    "parcial": "2900.00",
                    "es_encabezado": False
                }
            ],
            "filas_contabilidad": [
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11111",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Caja Moneda Nacional",
                    "dh": "D",
                    "parcial": "",
                    "debe": "2900.00",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "41100",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Venta de Bienes y Servicios de las Administraciones Públicas",
                    "dh": "H",
                    "parcial": "",
                    "debe": "",
                    "haber": "2900.00",
                    "es_encabezado": False
                }
            ]
        }
    },
    {
        "id": "caso_foto_san_joaquin",
        "titulo": "Ejercicio 3: Compra al Contado (Código 09 - GCT / C-D-P)",
        "descripcion": "El comprobante oficial completo de la primera fotografía: Compra de Papelería, Limpieza y Útiles para el GAM San Joaquín con cheque del Banco Unión por Bs. 18,000.",
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
            "moneda": "BBS Bolivianos",
            "tipo_cambio": "6.86",
            "ufv": "2.35000",
            "doc_respaldo": "COTIZACIONES, ORDEN DE COMPRA...",
            "depositante": 'Libreria y Papeleria "POMPEYA"',
            "beneficiario": 'Libreria y Papeleria "POMPEYA"',
            "elaborado_por": "Alejandro Cazas Tarqui",
            "glosa": "REGISTRO PARA CONTABILIZAR LA COMPRA DE: LIBRERIA Y PAPELERIA POMPEYA DE: PAPEL DE ESCRITORIO, MATERIAL DE LIMPIEZA Y UTILES DE ESCRITORIO Y OFICINA, PARA EL FUNCIONAMIENTO DEL EJECUTIVO MUNICIPAL DEL GOBIERNO AUTONOMO MUNICIPAL DE SAN JOAQUIN, SEGUN FACTURA Nº 005240 QUE SE ADJUNTA.",
            "grid_rows": [
                {
                    "ap": "20/210 0000",
                    "gasto": "32100",
                    "recurso": "",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11510",
                    "aux": "PAPEL",
                    "oec": "001",
                    "debe": "3000.00",
                    "haber": "0.00",
                    "descripcion": "Papel de Escritorio"
                },
                {
                    "ap": "20/210 0000",
                    "gasto": "39100",
                    "recurso": "",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11510",
                    "aux": "MAT-LIM",
                    "oec": "001",
                    "debe": "5000.00",
                    "haber": "0.00",
                    "descripcion": "Material de Limpieza"
                },
                {
                    "ap": "20/210 0000",
                    "gasto": "39500",
                    "recurso": "",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11510",
                    "aux": "UTIL-ESC",
                    "oec": "001",
                    "debe": "10000.00",
                    "haber": "0.00",
                    "descripcion": "Útiles de Escritorio y Oficina"
                },
                {
                    "ap": "20/210 0000",
                    "gasto": "",
                    "recurso": "",
                    "ff": "20",
                    "of": "210",
                    "et": "0000",
                    "cta": "11124",
                    "aux": "B-UNION",
                    "oec": "001",
                    "debe": "0.00",
                    "haber": "18000.00",
                    "descripcion": "Cuentas Fiscales Banco Unión - Cheque Nº 2001"
                }
            ],
            "filas_presupuesto": [
                {
                    "codigo_presup": "0000000000",
                    "partida": "32000",
                    "partida_tipo": "",
                    "codigo_contable": "",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "EJECUTIVO MUNICIPAL\nProductos de Papel, Cartón e Impresos",
                    "dh": "",
                    "parcial": "",
                    "es_encabezado": True
                },
                {
                    "codigo_presup": "20/210 0000",
                    "partida": "32100",
                    "partida_tipo": "G",
                    "codigo_contable": "11510",
                    "cheque": "",
                    "linea": "1",
                    "descripcion": "Papel",
                    "dh": "D",
                    "parcial": "3000.00",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "39000",
                    "partida_tipo": "",
                    "codigo_contable": "",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Productos Varios",
                    "dh": "",
                    "parcial": "",
                    "es_encabezado": True
                },
                {
                    "codigo_presup": "20/210 0000",
                    "partida": "39100",
                    "partida_tipo": "G",
                    "codigo_contable": "11510",
                    "cheque": "",
                    "linea": "2",
                    "descripcion": "Material de Limpieza",
                    "dh": "D",
                    "parcial": "5000.00",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "20/210 0000",
                    "partida": "39500",
                    "partida_tipo": "G",
                    "codigo_contable": "11510",
                    "cheque": "",
                    "linea": "3",
                    "descripcion": "Utiles de Escritorio y Oficina",
                    "dh": "D",
                    "parcial": "10000.00",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "Referencias\n20/210\n\n0000",
                    "partida": "",
                    "partida_tipo": "",
                    "codigo_contable": "",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "...Fuentes Utilizadas...\nRecursos Específicos/Rec.Específ. de...\n...Entidades Utilizadas...",
                    "dh": "",
                    "parcial": "",
                    "es_encabezado": True
                }
            ],
            "filas_contabilidad": [
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11500",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Bienes de Consumo",
                    "dh": "",
                    "parcial": "",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": True
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11510",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Inventarios de Materias Primas, Materiales...",
                    "dh": "D",
                    "parcial": "",
                    "debe": "18000.00",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "MAT-LIMPIE",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "MATERIAL DE LIMPIEZA",
                    "dh": "D",
                    "parcial": "5000.00",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "PAPEL-...",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "PAPEL DE ESCRITORIO",
                    "dh": "D",
                    "parcial": "3000.00",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "UTIL-ESCRI",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "UTILES DE ESCRITORIO Y OFICINA",
                    "dh": "D",
                    "parcial": "10000.00",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11100",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Disponible",
                    "dh": "",
                    "parcial": "",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": True
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11120",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Bancos",
                    "dh": "",
                    "parcial": "",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": True
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "11124",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "Cuentas Fiscales y Otras en la Banca...",
                    "dh": "H",
                    "parcial": "",
                    "debe": "",
                    "haber": "18000.00",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "REC-...",
                    "cheque": "",
                    "linea": "",
                    "descripcion": "BANCO UNION",
                    "dh": "H",
                    "parcial": "18000.00",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": False
                },
                {
                    "codigo_presup": "",
                    "partida": "",
                    "codigo_contable": "",
                    "cheque": "2001",
                    "linea": "",
                    "descripcion": 'Libreria y Papeleria "POMPEYA"',
                    "dh": "H",
                    "parcial": "18000.00",
                    "debe": "",
                    "haber": "",
                    "es_encabezado": False
                }
            ]
        }
    }
]

with open(os.path.join(data_dir, "plantillas_academicas.json"), "w", encoding="utf-8") as f:
    json.dump(plantillas, f, ensure_ascii=False, indent=2)

print("Plantillas y momentos configurados con exito!")
