import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# CANVAS ESPECIAL: NUMERACIÓN Y MARCA DE AGUA
# ==========================================
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        # 1. Fondo / Marca de Agua
        if os.path.exists("marca_agua.jpg"):
            self.drawImage("marca_agua.jpg", 0, 0, width=612, height=792)
        elif os.path.exists("marca_agua.png"):
            self.drawImage("marca_agua.png", 0, 0, width=612, height=792)

        # 2. Pie de Página (Numeración dinamica "Página X de Y")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#5D6D7E"))
        self.drawRightString(567, 30, f"Página {self._pageNumber} de {page_count}")


# ==========================================
# FUNCIÓN PRINCIPAL DE GENERACIÓN
# ==========================================
def generar_pdf_cedivet(estudio_id, paciente, especie, raza, fecha, medico, sexo, edad, tipo_estudio, datos_estudio, observaciones_txt):
    buffer = io.BytesIO()
    
    # Configuración del documento con márgenes de seguridad para encabezado y pie
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=150,  # Espacio reservado para el encabezado del paciente
        bottomMargin=80   # Espacio reservado para pie/firma
    )

    styles = getSampleStyleSheet()
    
    # Estilos de texto
    estilo_celda = ParagraphStyle('Celda', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9)
    estilo_celda_hdr = ParagraphStyle('CeldaHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=9, textColor=colors.HexColor("#2C3E50"))
    estilo_obs = ParagraphStyle('Obs', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#2C3E50"))

    # 1. ENCABEZADO DEL PACIENTE (Se repite en la parte superior de cada hoja)
    def dibujar_encabezado_paciente(canvas_obj, doc_obj):
        y = 665
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(colors.HexColor("#1A252C"))

        canvas_obj.drawString(45, y, "NO. ESTUDIO:")
        canvas_obj.drawString(45, y - 12, "PACIENTE / IDENT.:")
        canvas_obj.drawString(45, y - 24, "ESPECIE:")
        canvas_obj.drawString(45, y - 36, "RAZA:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(135, y, str(estudio_id))
        canvas_obj.drawString(135, y - 12, str(paciente))
        canvas_obj.drawString(135, y - 24, str(especie))
        canvas_obj.drawString(135, y - 36, str(raza))

        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(340, y, "FECHA:")
        canvas_obj.drawString(340, y - 12, "MEDICO SOLICITANTE:")
        canvas_obj.drawString(340, y - 24, "SEXO:")
        canvas_obj.drawString(340, y - 36, "EDAD:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(445, y, str(fecha))
        canvas_obj.drawString(445, y - 12, str(medico))
        canvas_obj.drawString(445, y - 24, str(sexo))
        canvas_obj.drawString(445, y - 36, str(edad))

    # Helper para armar tablas estándar
    def crear_bloque_tabla(titulo, lista_datos, color_hex="#117A65"):
        elementos_bloque = []
        
        # Encabezado del bloque
        hdr_table = Table([[titulo]], colWidths=[522], rowHeights=[16])
        hdr_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor(color_hex)),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
            ('TOPPADDING', (0, 0), (-1, -1), 2),
        ]))
        elementos_bloque.append(hdr_table)

        # Contenido de la tabla
        tabla_data = [[
            Paragraph("PARÁMETRO", estilo_celda_hdr),
            Paragraph("RESULTADO", estilo_celda_hdr),
            Paragraph("UNIDAD", estilo_celda_hdr),
            Paragraph("RANGOS REFERENCIA", estilo_celda_hdr)
        ]]
        
        for p, r, u, ref in lista_datos:
            tabla_data.append([
                Paragraph(str(p), estilo_celda),
                Paragraph(str(r), estilo_celda),
                Paragraph(str(u), estilo_celda),
                Paragraph(str(ref), estilo_celda)
            ])

        t = Table(tabla_data, colWidths=[182, 110, 90, 140])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EAEDED")),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 2.5),
            ('TOPPADDING', (0, 0), (-1, -1), 2.5),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ]))
        elementos_bloque.append(t)
        elementos_bloque.append(Spacer(1, 10))
        
        return elementos_bloque

    # 2. CONSTRUCCIÓN DEL CONTENIDO FLUIDO
    story = []

    # Bloques de Hemograma / QS / Endo
    if 'hem_roja' in datos_estudio:
        story.extend(crear_bloque_tabla("🔴 FÓRMULA ROJA (ERITROGRAMA)", datos_estudio['hem_roja'], "#900C3F"))

    if 'hem_blanca' in datos_estudio:
        story.extend(crear_bloque_tabla("⚪ FÓRMULA BLANCA Y PLAQUETAS (LEUCOGRAMA)", datos_estudio['hem_blanca'], "#2C3E50"))

    if 'qs_items' in datos_estudio and len(datos_estudio['qs_items']) > 0:
        story.extend(crear_bloque_tabla("🧪 BIOQUÍMICA CLÍNICA", datos_estudio['qs_items'], "#1B4F72"))

    if 'endo_items' in datos_estudio:
        story.extend(crear_bloque_tabla("⚕️ ENDOCRINOLOGÍA", datos_estudio['endo_items'], "#2874A6"))

    # Bloques de Urianálisis
    if 'uri_fisico' in datos_estudio:
        story.extend(crear_bloque_tabla("🧪 URIANÁLISIS - EXAMEN FÍSICO", datos_estudio['uri_fisico'], "#117A65"))

    if 'uri_quimico' in datos_estudio:
        story.extend(crear_bloque_tabla("🔬 URIANÁLISIS - EXAMEN QUÍMICO", datos_estudio['uri_quimico'], "#117A65"))

    if 'uri_micro' in datos_estudio:
        story.extend(crear_bloque_tabla("🔬 URIANÁLISIS - SEDIMENTO Y MICROSCOPÍA", datos_estudio['uri_micro'], "#117A65"))

    # Observaciones Urinarias
    if datos_estudio.get('obs_urianalisis'):
        p_obs_uri = Paragraph(f"<b>Observaciones Urinarias:</b> {datos_estudio['obs_urianalisis']}", estilo_obs)
        story.append(p_obs_uri)
        story.append(Spacer(1, 10))

    # Otros estudios (Copro, Serología, Citología)
    if 'copro_items' in datos_estudio:
        bloque_copro = []
        bloque_copro.append(Paragraph("<b>💩 COPROPARASITOSCÓPICO Y COPROLÓGICO</b>", estilo_celda_hdr))
        for param, val in datos_estudio['copro_items']:
            bloque_copro.append(Paragraph(f"• {param}: {val}", estilo_celda))
        bloque_copro.append(Spacer(1, 8))
        story.append(KeepTogether(bloque_copro))

    if 'sero_items' in datos_estudio:
        bloque_sero = []
        bloque_sero.append(Paragraph("<b>🩸 PRUEBAS RÁPIDAS Y SEROLOGÍA</b>", estilo_celda_hdr))
        for prueba, resultado in datos_estudio['sero_items']:
            bloque_sero.append(Paragraph(f"Prueba: {prueba} | Resultado: {resultado}", estilo_celda))
        bloque_sero.append(Spacer(1, 8))
        story.append(KeepTogether(bloque_sero))

    if 'cito_items' in datos_estudio:
        bloque_cito = []
        bloque_cito.append(Paragraph("<b>🔬 CITOLOGÍA Y DERMATOLOGÍA</b>", estilo_celda_hdr))
        for param, val in datos_estudio['cito_items']:
            bloque_cito.append(Paragraph(f"{param}: {val}", estilo_celda))
        bloque_cito.append(Spacer(1, 8))
        story.append(KeepTogether(bloque_cito))

    # Observaciones Generales
    if observaciones_txt:
        bloque_obs = []
        hdr_obs = Table([["💬 OBSERVACIONES Y NOTAS CLÍNICAS"]], colWidths=[522], rowHeights=[16])
        hdr_obs.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2E4053")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        bloque_obs.append(hdr_obs)
        bloque_obs.append(Spacer(1, 4))
        for line in observaciones_txt.split('\n'):
            if line.strip():
                bloque_obs.append(Paragraph(line.strip(), estilo_obs))
        
        story.append(KeepTogether(bloque_obs))

    # CONSTRUIR EL PDF
    doc.build(
        story,
        canvasmaker=NumberedCanvas,
        onFirstPage=dibujar_encabezado_paciente,
        onLaterPages=dibujar_encabezado_paciente
    )

    # Nomenclatura del archivo
    estudio_clean = str(estudio_id).strip().replace(' ', '_')
    tipo_clean = str(tipo_estudio).strip().replace(' ', '_').replace('(', '').replace(')', '').replace('+', 'Y')
    especie_clean = str(especie).strip().replace(' ', '_')
    paciente_clean = str(paciente).strip().replace(' ', '_')

    nombre_archivo_pdf = f"{estudio_clean}_{tipo_clean}_{especie_clean}_{paciente_clean}.pdf"

    return buffer.getvalue(), nombre_archivo_pdf
