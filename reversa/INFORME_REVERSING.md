# Ingeniería inversa de `C:\sgp2021` — SIGEP MV 2021 (Visual FoxPro 9)

Fecha: 2026-10-21 · Objetivo: `C:\sgp2021` · Proyecto destino: `Proyecto Sigep` (web)

---

## 1. Resumen ejecutivo

`C:\sgp2021` es el **SIGEP MV 2021** oficial, una aplicación de escritorio **Visual FoxPro 9**
(runtime `VFP9r.dll`, `VFP9ENU.DLL`) compuesta por un lanzador (`sigepmv2021.exe`) y ~20 módulos
`.APP` compilados, con datos en tablas `.dbf` y reportes en `.frx`.

Lo que se logró extraer sin ejecutar el programa:

| Área | Resultado |
|---|---|
| Modelo de datos | **188 archivos DBF** leídos (93 en `Data\` + copia preventiva), 147 con datos, con esquema y contenido |
| Reporte oficial del comprobante | **7 reportes FRX** decodificados a objetos, posiciones y expresiones |
| Formularios | **2 formularios SCX** (diálogo de impresión) con todas sus opciones |
| Lógica | Sin código fuente (VFP compila a p-code); se recuperaron nombres, SQL y mensajes |
| Geometría del reporte | Unidades resueltas: **1 pulgada = 10 000 FRU** (constante `$FRUs` del propio VFP) |

**Hallazgo central:** el comprobante oficial **no** es el formato vertical que genera hoy el proyecto
web. Es un reporte de **10.767 in de ancho por ~4.8 in de alto**, con fuente **Arial 6 pt** para la
grilla y **MS Sans Serif 8 pt** para las etiquetas, y tiene **6 variantes** según el tipo de papel
(sin preimpreso, Carta preimpreso, Ancho preimpreso y preimpresos 04/05/06).

---

## 2. Inventario del objetivo

### 2.1 Módulos (`.APP` / `.exe`)

| Archivo | Tamaño | Rol inferido |
|---|---|---|
| `sigepmv2021.exe` | 10.6 MB | Lanzador / menú principal |
| `mant.APP` | 58.9 MB | Mantenimiento (catálogos, altas/bajas) |
| `cge.APP` | 4.0 MB | Contabilidad general del Estado |
| `eje_pres.APP` | 4.2 MB | Ejecución presupuestaria |
| `repteso.APP` | 1.9 MB | Reportes de tesorería |
| `pr_cbte.APP` | 1.1 MB | **Impresión de comprobantes** |
| `jconta.APP` | 1.5 MB | Asientos / libros contables |
| `caif.APP`, `det_pres.APP`, `apr_pres.APP`, `rep_pres.APP` | 1.5–2.2 MB | Presupuesto, CAIF, detalles |
| `ctas.APP`, `aux_ctas.APP`, `bante_*.APP` | 0.08–2.2 MB | Cuentas, auxiliares, bancos |
| `params.APP`, `varios.APP`, `otras_op.APP`, `liscom.APP`, `gerencia.APP` | 0.2–3.5 MB | Parámetros y utilitarios |
| `impsfpm.app`, `impmodif.app` | 2.7 / 2.0 MB | Importación (SFPM / modificaciones) |
| `ReportBuilder.app`, `ReportOutput.app`, `ReportPreview.app` | 0.1–0.9 MB | Motor de reportes VFP |
| `vfpencryption.fll` | 173 KB | Librería de cifrado |

### 2.2 Datos

- `Data\*.dbf` + índices `.cdx/.idx` + memos `.fpt`: **93 tablas** (catálogo completo en
  `spec/TABLAS.md` y diccionario de campos en `spec/DICCIONARIO_TABLAS.md`).
- `DATA_COPIA_PREVENTIVA_20261020\`: copia de seguridad completa (mismo esquema, 93 tablas más).
- `Formatos_Comprobantes\`: los 7 reportes del comprobante y 2 formularios de opciones.
- `rep\`: salidas exportadas, incluida **una impresión real del comprobante** (`Ultimo.txt`).
- `themes\`: 9 imágenes de fondo de la interfaz.
- `bkp\`, `log\`, `cge\`: respaldos, bitácora y contabilidad.

### 2.3 Configuración

`config.fpw` (entorno VFP):

```
CODEPAGE = 1250      <- página de códigos Windows-1250 (¡no 1252!)
RESOURCE = OFF
MVCOUNT  = 8092
SCREEN   = OFF
ALLOWEXTERNAL = ON
```

`config.s3` (rutas relativas al ejecutable):

```
Directorio [DBF] = .\DATA\      Directorio [REP] = .\rep\
Directorio [TMP] = .\TMP\       Directorio [BKP] = .\bkp\
Directorio [LOG] = .\log\       Directorio [CGE] = .\cge\
```

> Detalle relevante para el port: la base está en **cp1250**, no en cp1252. Por eso algunos textos
> (`Reversi�n`, `Aut�nomo`) aparecen con caracteres raros al leerlos como latin-1.

---

## 3. Método y herramientas

1. **REA 6.7.0** instalado localmente en `_rea\` (npm). Se comprobó que **no puede abrir `.APP`**
   (`unsupported binary format`) y que **no hay motor nativo** (Ghidra/IDA/Hopper) en la máquina.
   Se usó REA para inventario de artefactos y descarte razonado, no para el análisis final.
2. **Parser propio de tablas VFP** (`reversa/vfp.py`): lee DBF (cabecera, campos, registros) y los
   memo FPT/FRT/SCT con sus bloques.
3. **Decodificador de reportes** (`reversa/dump_frx.py`, `frx_spec.py`): convierte los 75 campos del
   FRX en objetos con posición, tamaño, fuente y expresión.
4. **Reconstructor visual** (`reversa/render_frx.py`): dibuja el reporte a partir de sus objetos →
   `reversa/oficial/jcbte_layout.png`.
5. **Extractor de cadenas** (`reversa/scan_all.py`): 32 binarios, SQL, nombres de tablas y mensajes.
6. **Lector de formularios** (`reversa/dump_scx.py`): clases, propiedades, controles y métodos.

Evidencia cruda en `reversa/spec/`: `tablas.json`, `reportes.json`, `formularios.json`, `cadenas.json`.

> **Unidades del reporte.** El XSLT interno de VFP (presente en los `.APP`) define
> `<xsl:variable name="FRUs" select="10000"/>` y calcula `hpos div $FRUs` para obtener pulgadas.
> Es decir: **10 000 FRU = 1 pulgada**. Con eso todas las coordenadas del `.frx` cuadran.

---

## 4. Modelo de datos (núcleo del comprobante)

### 4.1 `s3cbte` — cabecera del comprobante (25 campos, 13 registros)

| Campo | Tipo | Significado |
|---|---|---|
| `UNIDAD` | C3 | Unidad ejecutora (`001`) |
| `CBTE` | C7 | Número validado (`0000001`…) |
| `BORRADOR` | C7 | Número de borrador (`1000001`…, prefijo `1`) |
| `FECHA` / `FECHAIN` | D8 | Fecha del comprobante / fecha de ingreso |
| `CODTR` / `CODTR1` | C2 | Momento contable / momento de reversión |
| `DOCRES` | C50 | Documento de respaldo |
| `MONEDA` | C3 | Moneda (`BBS`) |
| `CAMBIO` | N10.2 | Tipo de cambio |
| `UFV` | N8.5 | UFV del día |
| `BENE` | C140 | Beneficiario / depositante |
| `GLOSA` | M | Glosa (se imprime en 7 líneas de 67 caracteres) |
| `TDBB` / `THBB` | C16 | **Totales Debe/Haber ya formateados** (`14,968,764.00`) |
| `GAS` / `REC` / `CON` | L | Marca si el comprobante afecta gasto, recurso, contabilidad |
| `ESTADO` | N1 | Estado (todos los registros reales están en `3`) |
| `IMP`, `TP`, `CASO`, `CBTER`, `USUARIO` | — | Impreso, tipo de comprobante, caso, débito/extranjera, usuario |

### 4.2 `s3movga` — líneas del comprobante (18 campos, 375 registros)

`UNIDAD, CBTE, LINEA, FECHA, CODTR, CODTR1, AP, GASTO, FF, OF, ET, OEC, DBB, HBB, DBE, HBE, CLASEG, ESTADO`

- `AP`: apertura programática (25 caracteres, p. ej. `1700000002878102400000000`).
- `GASTO`: partida presupuestaria de 5 dígitos (`13110`, `39990`…).
- `FF`, `OF`, `ET`, `OEC`: fuente de financiamiento, organismo, entidad, objeto del gasto.
- `DBB`/`HBB`: debe/haber en bolivianos; `DBE`/`HBE`: en moneda extranjera.
- `CLASEG`: clasificador económico del gasto.

### 4.3 Resto del núcleo

| Tabla | Registros | Contenido |
|---|---|---|
| `s3relga` | 1 022 | Relación cuenta contable ↔ partida de gasto ↔ CAIF |
| `s3ctas` | 372 | Saldos y movimientos por cuenta (`SALDOD/SALDOH/DBB/HBB`) |
| `s3plan_c` | 372 | Plan de cuentas (`CTA, DES, TIPO, AUX, NIVEL, AUX_BASE`) |
| `s3codigo` | 17 | **Momentos contables** (código, descripción, tipo, bits) |
| `s3unidad` | 1 | Configuración de la entidad y **contadores de numeración** |
| `s3moneda` | 2 | Monedas |
| `s6cbte_bene` | 11 | Beneficiarios |

### 4.4 Numeración y estados (reconstruido de `s3unidad` + `s3cbte`)

```
s3unidad:  CBTE_VALI = 13          ← último comprobante validado
           CBTE_BORR = 1000012     ← último borrador (prefijo 1 + correlativo)

s3cbte:    BORRADOR 1000001 … 1000012   (borrador en curso)
           CBTE     0000001 … 0000013   (7 dígitos, ya validado)
           ESTADO = 3                    (en los 13 comprobantes reales)
```

Al validar, el borrador `1NNNNNN` se convierte en el comprobante `0NNNNNN` y los contadores de
`s3unidad` avanzan. *Hipótesis a confirmar:* `ESTADO=3` = validado/impreso; `CBTER` `D`/`E` distinguen
comprobantes en bolivianos de los que tienen componente en moneda extranjera.

### 4.5 Momentos contables (`s3codigo`, 17 códigos)

| Código | Descripción | Tipo | Bits |
|---|---|---|---|
| 01 | Traspasos Presupuestarios | PPT | 000000 |
| 02 | Compromiso | PPT | 100000 |
| 05 | Pago | COT | 000100 |
| 07 | Compromiso-Devengado | GCO | 111000 |
| 09 | Compromiso-Devengado-Pagado | GCT | 111100 |
| 10 | Devengado | GCO | 011000 |
| 11 | Devengado - Pagado | GCT | 011100 |
| 13 | Ingreso Devengado | RCO | 000010 |
| 14 | Ingreso de Caja | COT | 000001 |
| 15 | Ingreso Devengado - Percibido | RCT | 000011 |
| 18 | Gasto Comprometido Devengado - Pagado - Ingreso Devengado - Percibido | PCO | 111010 |
| 23 | Asientos de Cierre de Ejercicio | CON | 000000 |
| 24 | Asientos de Ajuste de la Contabilidad | CON | 000000 |
| 25 | Distribución de Presupuesto | PPT | 000000 |
| 26 | Reversión de Comprobantes | REV | 000000 |
| 29 | Traspaso de Presupuesto entre UEs | PPT | 000000 |
| 30 | Distribución de Reformulado/Modificación (SIGMA) | PPT | 000000 |

Los `BITS` (6 posiciones) codifican qué etapas toca el asiento: compromiso, devengado, pagado,
ingreso devengado, ingreso percibido y una sexta posición sin identificar.

### 4.6 `s3link` y la nota `(A)` del comprobante

La única sentencia SQL del módulo `pr_cbte.APP` revela la tabla de enlace entre líneas:

```sql
SELECT DISTINCT a.cbte_a, a.linea_a
  FROM (_dirdbf+[s3link]) a
  LEFT OUTER JOIN (xcur) b ON a.unidad = b.unidad AND a.cbte_a = b.cbte AND a.linea_a = b.linea
 WHERE a.unidad = xUni AND a.cbte_b = xCbteB AND &xwhr AND a.linea_b = xLin
```

`s3link` guarda pares `(cbte_a, linea_a) ↔ (cbte_b, linea_b)`: la línea destino del comprobante
actual apunta a la línea de origen de otro comprobante. Eso alimenta la columna **`(A)`** y la nota
al pie *«el número y línea del Comprobante Origen cuando es una transacción relacionada»*.
Es el mecanismo de trazabilidad entre cadenas de comprobantes (compromiso → devengado → pago).

El resto del acceso a datos de `pr_cbte.APP` es xBase procedimental (`SELECT`, `SCATTER`, `GATHER`)
que arma el cursor `s3impri` que consume el reporte; no hay más SQL de negocio en ese módulo.

---

## 5. El reporte oficial del comprobante (`jcbte.frx`)

- **107 objetos** en el primer bloque (el archivo contiene un segundo bloque duplicado y reescalado).
- Ancho de diseño: **10.767 in**; alto ocupado: **~4.80 in**.
- Fuentes: **Arial 6 pt** (grilla y datos), **MS Sans Serif 8 pt** (etiquetas).
- Propiedades: `PAPERSIZE=1` (Carta), `ORIENTATION=1` (*hipótesis: horizontal*), `COLOR=2`.

### 5.1 Bandas

| Banda | Alto |
|---|---|
| Título (encabezado con membrete) | 1.375 in |
| Encabezado de columnas | 0.141 in |
| Detalle (líneas del comprobante) | 2.307 in |
| Pie / totales | 0.141 in |

### 5.2 Contenido (posiciones en pulgadas desde el borde superior izquierdo)

| Objeto | x | y | Expresión |
|---|---|---|---|
| Título | 4.667 | 0.365 | `"C O M P R O B A N T E   D E   C O N T A B I L I D A D"` |
| Unidad Ejecutora | 0.333 | 0.552 | `"Unidad Ejecutora:"` → `s3unidad.desc` (x 1.750) |
| Cód. Trans. | 0.333 | 0.688 | `"Cod. Trans. :"` → `s3cbte.codtr` / `s3codigo.des` |
| Moneda | 0.333 | 0.812 | `"Moneda :"` → `s3cbte.moneda` / `s3moneda.des` |
| Nro. Comprobante | 8.677 | 0.583 | `"Numero de Comprobante:"` → `s3impri.cbte` (x 9.688) |
| Fecha Cbte | 8.677 | 0.719 | `"Fecha del Comprobante:"` → `s3cbte.fecha` |
| Doc. Respaldo | 8.677 | 0.844 | `"Documento Respaldo:"` → `s3cbte.docres` |
| Cod.Trans.Resp. | 4.750 | 0.688 | `s3cbte.codtr1` + `"Reversion de "+s3codigo.des` |
| Tipo de Cambio | 4.750 | 0.812 | `"Tipo de Cambio:"` → `s3cbte.cambio` |
| Encabezado columnas | — | 1.79–1.82 | `CODIGO PART. CODIGO CHEQUE D/H` y `PRESUP. PRESUP. CONTABLE NUMERO DESCRIPCION DE LAS CUENTAS` |
| Línea de detalle | 0.167 | 1.823 | `s3impri.api`, `parti`, `ctai`, `chequei`, `des`, `tipoi`, `parcial`, `debe`, `haber` |
| Totales | — | 2.271 | `"T O T A L E S"` + `iif(inlist(s3cbte.codtr,'01','02','25',[28]),nume(sdebe),cdebe)` |
| Beneficiario | 0.167 | 2.979 | `substr(s3cbte.bene,1,67)` / `68,134` / `135,201` |
| Glosa | 6.000 | 2.979 | `mline(s3cbte.glosa,1)` … `mline(s3cbte.glosa,7)` |
| Firmas | — | 4.0–4.4 | `ELABORADO POR / REVISADO / APROBADO ×3` |

### 5.3 Las 7 variantes del comprobante (medidas reales)

| Reporte | Ancho útil | Alto útil | Etiquetas impresas | Familia |
|---|---|---|---|---|
| `jcbte.frx` | **11.167 in** | 4.802 in | todas | Ancho, sin preimpreso |
| `jcbte_pr.frx` | 10.470 in | 4.792 in | solo fecha/hora/página | Ancho, preimpreso |
| `jcbte2.frx` | 8.000 in | 5.583 in | todas | Carta, sin preimpreso |
| `jcbte_p2.frx` | 8.000 in | 7.709 in | solo fecha/hora/página | Carta, preimpreso |
| `jcbte_p3.frx` | 8.000 in | 5.657 in | solo fecha/hora/página | Carta, preimpreso 04 |
| `jcbte_p4.frx` | 8.000 in | 5.323 in | solo fecha/hora/página | Carta, preimpreso 05 |
| `jcbte_p5.frx` | 8.000 in | 6.281 in | todas | Carta, preimpreso 06 |

El combo `cbo_tipocbte14` del formulario `opi_cbt2.scx` ofrece 6 opciones
(`1 Carta sin preimpreso`, `2 Carta preimpreso`, `3 Ancho preimpreso`, `4/5/6 Carta preimpreso 04/05/06`).
La correspondencia exacta opción→archivo está en p-code; por geometría y etiquetas la asignación
más probable es:

| Opción | Reporte |
|---|---|
| 1 · Carta sin preimpreso | `jcbte2.frx` |
| 2 · Carta preimpreso | `jcbte_p2.frx` |
| 3 · Ancho preimpreso | `jcbte_pr.frx` |
| 4/5/6 · Carta preimpreso 04/05/06 | `jcbte_p3` / `jcbte_p4` / `jcbte_p5` |
| (no listada) Ancho sin preimpreso | `jcbte.frx` — la usada en la impresión real |

### 5.4 Comprobante impreso real (verdad de referencia)

`C:\sgp2021\rep\Ultimo.txt` es una **impresión real** del Cbte `0000006` (Compromiso, contratista
GRIMALDI, Bs. 2 903 560). Confirma el formato y las etiquetas exactas:

```
1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN            Fecha :
ALEJANDRO CAZAS TARQUI                                            Hora : 21/10/2026
                                                                  Página : 1
      C O M P R O B A N T E   D E   C O N T A B I L I D A D       Validado Cbte No.
                                                                  0000006
Unidad Ejecutora :001  ALEJANDRO CAZAS TARQUI                     Fecha Cbte. 15 Enero 2021
Cod. Transac. :02  Compromiso (PPT)
Moneda :BBS  Bolivianos
Cod.Trans.Resp.:            T/C : 6.86        Documento Respaldo: CONTRATO
CODIGO PART. CODIGO CHEQUE        D  DESCRIPCION DE LAS CUENTAS        PARCIALES  DEBE  HABER
PRESUP. PRESUP. CONTABLE NUMERO (A) L
.................PRESUPUESTO..................
...
(A) :el número y línea del Comprobante Origen...      T O T A L E S   2,903,560.00
Son: DOS MILLONES NOVECIENTOS TRES MIL QUINIENTOS SESENTA 00/100 Bs.
Beneficiario :        Descripción de la Transaccion :
ELABORADO POR        REVISADO        APROBADO        APROBADO        APROBADO
®® SigepMV, V.9.0.0 ®®                      C:\SGP2021\DATA\
```

Aporta datos que el `.frx` no muestra explícitos:

- El membrete es `1814 - GM - <nombre de la entidad>` (código + sigla + nombre).
- La leyenda `Validado Cbte No.` y el número en 7 dígitos bajo ella.
- Fecha larga en español: `15 Enero 2021` (no `15/01/2021`).
- La columna `L` (línea) y los bloques `..........PRESUPUESTO..........`.
- La nota al pie `(A) :el número y línea del Comprobante Origen cuando es una transacción relacionada`.
- El bloque `Referencias` con `Fuentes Utilizadas` / `Entidades Utilizadas`.
- El pie `®® SigepMV, V.9.0.0 ®®` y la ruta de datos `C:\SGP2021\DATA\`.

### 5.5 Opciones del diálogo de impresión (`opi_cbte.scx`)

`Agregar Apertura Programática`, `Incluir Auxiliares de Agregación`,
`Imprimir Referencia de la Fuentes`, `Imprimir Referencia de la Entidades`,
`Anteponer "-->"/"--->" a los Números de Cheques`, `Indentar las Descripciones`,
`Se está usando Papel PreImpreso`, `Ordenar el Reporte como el Sicopre/Informix`,
y combos de **nivel de agregación** de partidas (1–4) y de contabilidad (1–5).

---

## 6. Discrepancias con el proyecto web actual

| Aspecto | SIGEP oficial | `Proyecto Sigep` hoy |
|---|---|---|
| Orientación / tamaño | Horizontal, 11.167 × 4.8 in (`jcbte`) | Vertical, Carta completa |
| Tipografía | Arial 6 / MS Sans Serif 8 | Helvetica 7.5 |
| Numeración | `CBTE_VALI`/`CBTE_BORR`; borrador `1NNNNNN` → validado `0NNNNNN` | `numero_cbte` libre |
| Totales | Guardados formateados en `TDBB`/`THBB` | Calculados al vuelo |
| Líneas | `s3movga` con AP/GASTO/FF/OF/ET/OEC y debe/haber en Bs y ME | JSON libre `grid_rows` |
| Glosa | 7 líneas × 67 caracteres (`mline`) | Texto libre |
| Variantes de papel | 6 | 1 |

---

## 7. Qué quedó fuera (y cómo seguirlo)

1. **Código de los `.APP`.** VFP compila a p-code: no hay PRG embebido (0 coincidencias de
   `PROCEDURE`/`FUNCTION`). Recuperar la lógica de validación exige un decompilador de VFP
   (ReFox/UnFoxAll) o ingeniería dinámica; las tablas y los strings ya revelan estructura y mensajes.
2. **Formularios de captura.** Los 2 `.scx` del comprobante son solo el diálogo de impresión.
   Las pantallas de carga están compiladas dentro de los `.APP` (no son `.scx` sueltos).
3. **Verificación contra impresión real.** ✅ Resuelto: `rep\Ultimo.txt` es una impresión real del
   Cbte 0000006 y confirma etiquetas, orden de bloques y membrete (ver §5.4).
4. **Catálogos completos.** ✅ Extraídos a `catalogos\*.json`: `s3plan_c` (372 cuentas),
   `s3codigo` (17 momentos), `s3relga` (1 022 relaciones), `s3ctas` (372 saldos), `s3gastos` (498),
   `s3recur` (350), `r_entidad` (587), `s3et` (592), `s3sector`, `s3funcion`, `s3ff`, `s3ff_of`,
   `s6bancos`, `s7benef`, `s3parametros`, entre otros.

---

## 8. Siguientes pasos propuestos

1. Portar `jcbte_spec.json` a `export_pdf.py` con geometría exacta en pulgadas (horizontal, 11.167 in).
2. Cargar los catálogos de `catalogos\` en la web (reemplazan los JSON actuales de `data\`).
3. Implementar la numeración borrador → validado con `CBTE_BORR`/`CBTE_VALI`.
4. Reproducir el diálogo de impresión (6 tipos de papel + opciones de agregación).
5. Comparar el PDF generado contra `rep\Ultimo.txt` (estructura y textos) y ajustar fuentes/márgenes.

---

## 9. Réplica del comprobante oficial

`reversa/oficial_pdf.py` reconstruye el comprobante con la geometría del `.frx` (pulgadas, origen
arriba-izquierda) y lo valida contra la impresión real. Página: Carta horizontal (11 × 8.5 in) con
escala 0.985 para encajar el ancho de diseño de 11.167 in.

Modos de uso:

```bash
python reversa/oficial_pdf.py --sample        # Cbte 0000006, el de rep\Ultimo.txt
python reversa/oficial_pdf.py --db 12         # un comprobante de sigep.db
python reversa/oficial_pdf.py --all           # los 34 comprobantes del proyecto
```

Resultados verificados:

| Archivo | Contenido |
|---|---|
| `oficial/muestra_oficial.pdf` + `.png` | réplica del Cbte 0000006 (contrastada con `Ultimo.txt`) |
| `oficial/comprobantes_replica.pdf` | **34 páginas**, una por comprobante de `sigep.db` |
| `oficial/cbte_12.pdf` + `.png` | comprobante real del proyecto (Devengado de Gasto) |

Elementos replicados: membrete `1814 - GM - …`, `Fecha/Hora de Imp.`, `Pagina Numero`,
título espaciado, bloque `Validado / Cbte No.` con el número en 7 dígitos, filas
`Unidad Ejecutora`, `Cod. Transac.`, `Moneda`, `Cod.Trans.Resp.`, `T/C`, `UFV`, `Documento Respaldo`,
cabecera de grilla en dos líneas con `.....PRESUPUESTO.....`, columnas
`CODIGO / PART. / CODIGO / CHEQUE / D-H / DESCRIPCION / PARCIALES / DEBE / HABER`,
`T O T A L E S`, importe en letras, cajas de `Beneficiario` y `Descripción de la Transacción`,
bloque de 5 firmas y pie `SigepMV, V.9.0.0`.

Diferencias conocidas (documentadas, no accidentales):

- La columna `D/H` se coloca según la impresión real (~4.16 in); en `jcbte.frx` ese objeto figura
  en una coordenada que no coincide con el encabezado impreso, señal de que el `.frx` fue editado
  (los archivos de `Formatos_Comprobantes` tienen fecha de hoy).
- No se dibujan las líneas verticales internas de la grilla (el `.frx` las define sueltas y la
  impresión de referencia no las muestra).
- La numeración, la conversión a letras y los totales se toman de los datos; el SIGEP los calcula
  en p-code.

Guía de integración con la web: `server.py` ya expone `/api/descargar-pdf-oficial`; basta sustituir
la llamada a `generar_pdf_oficial` por `oficial_pdf.generar_salida(...)` alimentándolo con
`desde_db(id)` para cada comprobante.

---

### Evidencia y artefactos

```
reversa/
├── vfp.py               lector DBF/FPT/FRT/SCT
├── dump_frx.py          volcado legible de reportes
├── frx_spec.py          especificación en pulgadas (md + json)
├── render_frx.py        reconstrucción visual del reporte
├── dump_scx.py          volcado de formularios
├── scan_all.py          escaneo completo (tablas/reportes/formularios/binarios)
├── export_docs.py       exporta specs, diccionario de tablas y catálogos
├── export_sql.py        SQL de negocio y mensajes por módulo
├── oficial_pdf.py       generador del comprobante con la geometría oficial
├── pdf2png.py           render de verificación (PyMuPDF)
├── oficial/Formatos/    copia de los .frx/.frt/.scx/.sct analizados
├── oficial/jcbte_layout.png   reconstrucción del reporte oficial
├── oficial/muestra_oficial.pdf|png   réplica del Cbte 0000006
├── oficial/comprobantes_replica.pdf  los 34 comprobantes en formato oficial
├── catalogos/           21 catálogos JSON listos para la web
└── spec/
    ├── tablas.json · reportes.json · formularios.json · cadenas.json   (crudo)
    ├── TABLAS.md                      catálogo de las 93 tablas
    ├── DICCIONARIO_TABLAS.md          campos de las 93 tablas
    ├── SQL_POR_MODULO.md              SQL de negocio y mensajes por .APP
    └── reportes/*_spec.md|json        las 7 variantes del comprobante
```
