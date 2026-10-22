import sqlite3
import json
import os
import html
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

def safe_float(val):
    if val is None or val == "":
        return 0.0
    if isinstance(val, (int, float)):
        return float(val)
    val_str = str(val).strip().replace("Bs.", "").replace("Bs", "").replace("bs.", "").replace("bs", "").replace("$", "").strip()
    if not val_str:
        return 0.0
    if "," in val_str and "." in val_str:
        if val_str.rfind(",") > val_str.rfind("."):
            val_str = val_str.replace(".", "").replace(",", ".")
        else:
            val_str = val_str.replace(",", "")
    elif "," in val_str:
        parts = val_str.split(",")
        if len(parts) == 2 and len(parts[1]) in (1, 2):
            val_str = val_str.replace(",", ".")
        else:
            val_str = val_str.replace(",", "")
    try:
        return float(val_str)
    except Exception:
        return 0.0

def esc(s):
    if s is None:
        return ""
    return html.escape(str(s))

def numero_a_letras(numero):
    try:
        numero = float(numero)
    except Exception:
        numero = 0.0
    if numero < 0:
        numero = abs(numero)
    entero = int(numero)
    centavos = int(round((numero - entero) * 100))
    centavos_str = f"{centavos:02d}/100 BS."

    unidades = ["", "UN", "DOS", "TRES", "CUATRO", "CINCO", "SEIS", "SIETE", "OCHO", "NUEVE"]
    decenas = ["", "DIEZ", "VEINTE", "TREINTA", "CUARENTA", "CINCUENTA", "SESENTA", "SETENTA", "OCHENTA", "NOVENTA"]
    diez_y = ["DIEZ", "ONCE", "DOCE", "TRECE", "CATORCE", "QUINCE", "DIECISEIS", "DIECISIETE", "DIECIOCHO", "DIECINUEVE"]

    if entero == 0:
        return f"SON: CERO {centavos_str}"

    def dec(n):
        if n == 0: return ""
        if n < 10: return unidades[n]
        if n < 20: return diez_y[n - 10]
        if n == 20: return "VEINTE"
        if n < 30: return "VEINTI" + unidades[n - 20]
        u = n % 10
        d = n // 10
        return (decenas[d] + (" Y " + unidades[u] if u > 0 else "")).strip()

    def cen(n):
        c = n // 100
        resto = n % 100
        if c == 1:
            return ("CIENTO " + dec(resto) if resto > 0 else "CIEN").strip()
        centenas_str = ["", "CIEN", "DOSCIENTOS", "TRESCIENTOS", "CUATROCIENTOS", "QUINIENTOS", "SEISCIENTOS", "SETECIENTOS", "OCHOCIENTOS", "NOVECIENTOS"]
        return (centenas_str[c] + (" " + dec(resto) if resto > 0 else "")).strip()

    def miles(n):
        m = n // 1000
        resto = n % 1000
        str_m = ("UN MIL" if m == 1 else (cen(m) + " MIL")) if m > 0 else ""
        str_r = cen(resto) if resto > 0 else ""
        return f"{str_m} {str_r}".strip()

    def millones(n):
        mill = n // 1000000
        resto = n % 1000000
        str_mill = ("UN MILLON" if mill == 1 else (cen(mill) + " MILLONES")) if mill > 0 else ""
        str_r = miles(resto) if resto > 0 else ""
        return f"{str_mill} {str_r}".strip()

    return f"SON: {millones(entero)} {centavos_str}".upper()

def generar_pdf_oficial(output_path=None):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(base_dir, "sigep.db")
    if not output_path:
        output_path = os.path.join(base_dir, "COMPROBANTES_SIGEP_OFICIALES.pdf")

    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("SELECT id, numero_cbte, fecha, monto_total, datos_json FROM comprobantes ORDER BY id ASC")
    rows = c.fetchall()
    conn.close()

    if not rows:
        return None

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=10 * mm,
        rightMargin=10 * mm,
        topMargin=8 * mm,
        bottomMargin=8 * mm
    )

    style_normal = ParagraphStyle('Norm', fontName='Helvetica', fontSize=7.5, leading=9.5)
    style_bold = ParagraphStyle('Bold', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5)
    style_small = ParagraphStyle('Small', fontName='Helvetica', fontSize=7, leading=8.5)
    style_title = ParagraphStyle('Title', fontName='Helvetica-Bold', fontSize=11, leading=13, alignment=1)
    style_cbte_num = ParagraphStyle('Num', fontName='Helvetica-Bold', fontSize=12, leading=14, alignment=2)
    style_cbte_lbl = ParagraphStyle('NumLbl', fontName='Helvetica', fontSize=7.5, leading=9, alignment=2)

    elements = []

    for idx, r in enumerate(rows):
        num_cbte = r[1]
        fecha = r[2]
        d = json.loads(r[4]) if r[4] else {}

        entidad = d.get('entidad', '1814 - GM - GOBIERNO AUTÓNOMO MUNICIPAL DE SAN JOAQUÍN')
        ue_codigo = d.get('unidad_ejecutora', '001')
        ue_desc = d.get('unidad_ejecutora_desc', d.get('direccion', 'DIRECCION ADMINISTRATIVA Y FINANCIERA'))
        momento_desc = f"{d.get('momento_codigo', '12')}    {d.get('momento_desc', 'Devengado de Recursos')}"
        depositante = d.get('depositante', d.get('beneficiario', 'DISTINTOS BENEFICIARIOS'))
        respaldo = d.get('doc_respaldo', '110 Resumen de Planillas')
        dolar = d.get('dolar', '6.86')
        ufv = d.get('ufv', '3.36131')
        glosa = d.get('glosa', 'REGISTRO DE LA TRANSACCIÓN SEGÚN DOCUMENTACIÓN DE RESPALDO ADJUNTA.')
        elaborado_por = d.get('elaborado_por', 'C.T.')
        if elaborado_por == 'Alejandro Cazas Tarqui':
            elaborado_por = 'C.T.'

        # 0. Manejo dinámico del Enunciado:
        # - Si tiene enunciado: baja a 7-8 cm e imprime en letra grande legible Nº 16.
        # - Si NO tiene enunciado: se mantiene arriba a exactamente 3 cm (30 mm) del borde superior.
        enunciado_text = (d.get('enunciado') or '').strip()
        has_enunciado = len(enunciado_text) > 0

        if has_enunciado:
            style_enun_title = ParagraphStyle('EnunT', fontName='Helvetica-Bold', fontSize=13, leading=16, textColor=colors.black)
            style_enun_body = ParagraphStyle('EnunB', fontName='Helvetica-Bold', fontSize=16, leading=20, textColor=colors.black)
            t_enun = Table([
                [Paragraph("<u>ENUNCIADO / TRANSACCIÓN:</u>", style_enun_title)],
                [Paragraph(esc(enunciado_text).replace('\n', '<br/>'), style_enun_body)]
            ], colWidths=[192.9 * mm], rowHeights=[6 * mm, 58 * mm])
            t_enun.setStyle(TableStyle([
                ('VALIGN', (0,0), (-1,-1), 'TOP'),
                ('LEFTPADDING', (0,0), (-1,-1), 0),
                ('RIGHTPADDING', (0,0), (-1,-1), 0),
                ('TOPPADDING', (0,0), (-1,-1), 0),
                ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ]))
            elements.append(t_enun)
            elements.append(Spacer(1, 4 * mm))
        else:
            # Sin enunciado: comprobante arriba a unos 3 cm (topMargin 10mm + Spacer 20mm = 30mm = 3cm)
            elements.append(Spacer(1, 20 * mm))

        # 1. Encabezado
        t_header = Table([
            [
                Paragraph(f"<b>{esc(entidad)}</b><br/>{esc(ue_desc)}", ParagraphStyle('HLeft', parent=style_normal, fontSize=8, leading=10)),
                Paragraph(f"Fecha : {esc(fecha)}<br/>Hora : 10:30:00<br/>Página : 1", ParagraphStyle('HRight', parent=style_normal, fontSize=7, leading=9, alignment=2))
            ]
        ], colWidths=[135 * mm, 60.9 * mm])
        t_header.setStyle(TableStyle([
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0),
            ('TOPPADDING', (0,0), (-1,-1), 0),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(t_header)
        elements.append(Spacer(1, 1 * mm))

        # 2. Título y Número de Comprobante (Centrado con caja gris y número a la derecha)
        t_title = Table([
            [
                "",
                Paragraph("COMPROBANTE DE CONTABILIDAD", style_title),
                Paragraph("ValidadoCbte No.<br/><b>" + esc(num_cbte) + "</b>", ParagraphStyle('CbteHeader', parent=style_normal, alignment=2, leading=11))
            ]
        ], colWidths=[42 * mm, 112 * mm, 41.9 * mm])
        t_title.setStyle(TableStyle([
            ('BOX', (1,0), (1,0), 0.5, colors.black),
            ('BACKGROUND', (1,0), (1,0), colors.HexColor('#E3E3E3')),
            ('ALIGN', (1,0), (1,0), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(t_title)
        elements.append(Spacer(1, 1.5 * mm))

        # 3. Metadatos (Limpio como en Word, sin caja exterior)
        p_ue = Paragraph(f"Unidad Ejecutora : <i>{esc(ue_codigo)}    {esc(ue_desc)}</i>", style_small)
        p_fcbte = Paragraph(f"Fecha Cbte.  <font size=\"9.5\"><b><i>{esc(fecha)}</i></b></font>", ParagraphStyle('FC', parent=style_small, alignment=2))
        p_trans = Paragraph(f"Cod. Transac. : <i>{esc(momento_desc)}</i>", style_small)
        p_mon = Paragraph("Moneda : <i>BBS Bolivianos</i>", style_small)
        p_tc = Paragraph(f"T/C (BCB) : <b><i>{esc(dolar)}</i></b>    UFV (BCB) : <b><i>{esc(ufv)}</i></b>    Documento Respaldo : <i>{esc(respaldo)}</i>", style_small)

        t_meta = Table([
            [p_ue, p_fcbte],
            [p_trans, ""],
            [p_mon, ""],
            [p_tc, ""]
        ], colWidths=[150 * mm, 45.9 * mm])
        t_meta.setStyle(TableStyle([
            ('SPAN', (0, 1), (1, 1)),
            ('SPAN', (0, 2), (1, 2)),
            ('SPAN', (0, 3), (1, 3)),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 0.8),
            ('BOTTOMPADDING', (0,0), (-1,-1), 0.8),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        elements.append(t_meta)
        elements.append(Spacer(1, 1.5 * mm))

        # 4. Grilla de Cuentas y Presupuesto
        grid_rows = d.get('grid_rows', [])
        table_rows = [
            [
                Paragraph("<b>RUBRO</b>", ParagraphStyle('THC', parent=style_bold, fontSize=7.5, alignment=1)),
                Paragraph("<b>CUENTA<br/>CONTABLE</b>", ParagraphStyle('THC', parent=style_bold, fontSize=7.5, alignment=1)),
                Paragraph("<b>DESCRIPCION DE LAS CUENTAS</b>", ParagraphStyle('THL', parent=style_bold, fontSize=7.5, alignment=1)),
                Paragraph("<b>PRESUPUESTOS<br/>(Bs.)</b>", ParagraphStyle('THR', parent=style_bold, fontSize=7, alignment=1)),
                Paragraph("<b>DEBE<br/>(Bs.)</b>", ParagraphStyle('THR', parent=style_bold, fontSize=7.5, alignment=1)),
                Paragraph("<b>HABER<br/>(Bs.)</b>", ParagraphStyle('THR', parent=style_bold, fontSize=7.5, alignment=1)),
            ]
        ]

        total_p = 0.0
        total_d = 0.0
        total_h = 0.0

        filled = [
            r_item for r_item in grid_rows 
            if r_item.get('rubro') or r_item.get('cta') or r_item.get('descripcion') or 
               safe_float(r_item.get('presupuesto', 0)) > 0 or safe_float(r_item.get('debe', 0)) > 0 or safe_float(r_item.get('haber', 0)) > 0
        ]

        for r_item in filled:
            rub = str(r_item.get('rubro', '') or '')
            cta = str(r_item.get('cta', '') or '')
            desc = str(r_item.get('descripcion', '') or '')
            p_val = safe_float(r_item.get('presupuesto', 0))
            d_val = safe_float(r_item.get('debe', 0))
            h_val = safe_float(r_item.get('haber', 0))
            total_p += p_val
            total_d += d_val
            total_h += h_val

            table_rows.append([
                Paragraph(esc(rub), ParagraphStyle('CR', parent=style_normal, fontSize=7, alignment=1, textColor=colors.HexColor('#8b0000'))),
                Paragraph(esc(cta), ParagraphStyle('CC', parent=style_normal, fontSize=7, alignment=1)),
                Paragraph(esc(desc), ParagraphStyle('CD', parent=style_normal, fontSize=7.5)),
                Paragraph(f"{p_val:,.2f}" if p_val > 0 else "", ParagraphStyle('RP', fontName='Courier', fontSize=8, alignment=2, textColor=colors.HexColor('#8b0000'))),
                Paragraph(f"{d_val:,.2f}" if d_val > 0 else "", ParagraphStyle('RD', fontName='Courier', fontSize=8, alignment=2)),
                Paragraph(f"{h_val:,.2f}" if h_val > 0 else "", ParagraphStyle('RH', fontName='Courier', fontSize=8, alignment=2)),
            ])

        # Filas del cuerpo: 5 filas si tiene enunciado para no desbordar, o 9 filas si no tiene enunciado para balancear la hoja
        target_rows = 5 if has_enunciado else 9
        needed = max(0, target_rows - len(filled))
        for _ in range(needed):
            table_rows.append(["", "", "", "", "", ""])

        # Fila de Totales
        table_rows.append([
            Paragraph("<b>TOTALES</b>", ParagraphStyle('TH_Tot', parent=style_bold, fontSize=8, alignment=1)),
            "",
            "",
            Paragraph(f"<b>{total_p:,.2f}</b>" if total_p > 0 else "", ParagraphStyle('THRP', fontName='Courier-Bold', fontSize=8.5, alignment=2, textColor=colors.HexColor('#8b0000'))),
            Paragraph(f"<b>{total_d:,.2f}</b>" if total_d > 0 else "", ParagraphStyle('THRD', fontName='Courier-Bold', fontSize=8.5, alignment=2)),
            Paragraph(f"<b>{total_h:,.2f}</b>" if total_h > 0 else "", ParagraphStyle('THRH', fontName='Courier-Bold', fontSize=8.5, alignment=2)),
        ])

        col_widths = [25.5 * mm, 26.8 * mm, 71.0 * mm, 23.1 * mm, 23.1 * mm, 23.4 * mm]
        t_grid = Table(table_rows, colWidths=col_widths)
        t_grid.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f2f2f2')),
            ('LINEBELOW', (0,0), (-1,0), 0.5, colors.black),
            ('LINEABOVE', (0,-1), (-1,-1), 0.5, colors.black),
            ('LINEBELOW', (0,-1), (-1,-1), 0.5, colors.black),
            ('LINEBEFORE', (1,0), (-1,-1), 0.5, colors.black),
            ('SPAN', (0,-1), (2,-1)),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('VALIGN', (0,0), (-1,0), 'MIDDLE'),
            ('VALIGN', (0,-1), (-1,-1), 'MIDDLE'),
            ('TOPPADDING', (0,0), (-1,-1), 1.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 1.5),
            ('LEFTPADDING', (0,0), (-1,-1), 2.5),
            ('RIGHTPADDING', (0,0), (-1,-1), 2.5),
        ]))
        elements.append(t_grid)

        # 5. Literal (Directamente pegado debajo con borde negro)
        disp_total = total_d if total_d > 0 else (total_p if total_p > 0 else total_h)
        literal_text = numero_a_letras(disp_total)
        t_lit = Table([[Paragraph(literal_text, ParagraphStyle('Lit', parent=style_small, alignment=1))]], colWidths=[192.9 * mm])
        t_lit.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('TOPPADDING', (0,0), (-1,-1), 2),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t_lit)

        # 6. Glosa y Beneficiario
        t_glosa = Table([
            [
                Paragraph(f"<u><b>Beneficiario / Depositante :</b></u><br/><font size=\"7\">{esc(depositante)}</font>", style_small),
                Paragraph(f"<u>Descripción de la Transacción :</u><br/><font size=\"6.5\">{esc(glosa)}</font><br/><br/><div align=\"right\"><b>{esc(elaborado_por)}</b></div>", style_small)
            ]
        ], colWidths=[78.7 * mm, 114.2 * mm], rowHeights=[20 * mm])
        t_glosa.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('LINEBEFORE', (1,0), (1,0), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
            ('TOPPADDING', (0,0), (-1,-1), 2.5),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
            ('LEFTPADDING', (0,0), (-1,-1), 3),
            ('RIGHTPADDING', (0,0), (-1,-1), 3),
        ]))
        elements.append(t_glosa)

        # 7. Cuadro de Firmas Oficiales (5 columnas como en Word)
        t_sig = Table([
            [
                Paragraph("<font size=\"6.5\">SIGEP</font><br/><br/><br/><b>ELABORADO POR</b>", ParagraphStyle('S1', parent=style_small, alignment=1)),
                Paragraph("<br/><br/><br/><b>REVISADO</b>", ParagraphStyle('S2', parent=style_small, alignment=1)),
                Paragraph("<br/><br/><br/><b>APROBADO</b>", ParagraphStyle('S3', parent=style_small, alignment=1)),
                Paragraph("<br/><br/><br/><b>APROBADO</b>", ParagraphStyle('S4', parent=style_small, alignment=1)),
                Paragraph("<br/><br/><br/><b>APROBADO</b>", ParagraphStyle('S5', parent=style_small, alignment=1)),
            ]
        ], colWidths=[38.58 * mm] * 5, rowHeights=[16 * mm])
        t_sig.setStyle(TableStyle([
            ('BOX', (0,0), (-1,-1), 0.5, colors.black),
            ('INNERGRID', (0,0), (-1,-1), 0.5, colors.black),
            ('VALIGN', (0,0), (-1,-1), 'BOTTOM'),
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('TOPPADDING', (0,0), (-1,-1), 1),
            ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ]))
        elements.append(t_sig)

        if idx < len(rows) - 1:
            elements.append(PageBreak())

    doc.build(elements)
    return output_path

if __name__ == '__main__':
    out = generar_pdf_oficial()
    print("PDF creado con éxito en:", out)
