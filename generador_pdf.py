import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

# ==========================================
# CANVAS EN DOS PASADAS PARA PAGINACIÓN REAL
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
            
            # 1. Dibujar Marca de Agua / Fondo
            if os.path.exists("marca_agua.jpg"):
                self.drawImage("marca_agua.jpg", 0, 0, width=612, height=792)
            elif os.path.exists("marca_agua.png"):
                self.drawImage("marca_agua.png", 0, 0, width=612, height=792)

            # 2. Dibujar Numeración de Página
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#5D6D7E"))
            self.drawRightString(567, 25, f"Página {self._pageNumber} de {num_pages}")
            
            super().showPage()
        super().save()


def generar_pdf_cedivet(estudio_id, paciente, especie, raza, fecha, medico, sexo, edad, tipo_estudio, datos_estudio, observaciones_txt):
    buffer = io.BytesIO()
    
    # Documento base
    doc = BaseDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=135,
        bottomMargin=110
    )

    # Frame principal donde fluye el contenido (entre encabezado y firma)
    frame_contenido = Frame(
        doc.leftMargin,
        doc.bottomMargin,
        doc.width,
        doc.height,
        id='normal',
        topPadding=0,
        bottomPadding=0,
        leftPadding=0,
        rightPadding=0
    )

    # Dibujado del encabezado estático del paciente
    def dibujar_encabezado_paciente(canvas_obj, doc_obj):
        y = 665
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(colors.HexColor("#1A252C"))

        canvas_obj.drawString(45, y, "NO. ESTUDIO:")
        canvas_obj.drawString(45, y - 12, "PACIENTE / IDENT.:")
        canvas_obj.drawString(45, y - 24, "ESPECIE:")
        canvas_obj.drawString(45, y - 36, "RAZA:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(135, y, str(estudio_id or ''))
        canvas_obj.drawString(135, y - 12, str(paciente or ''))
        canvas_obj.drawString(135, y - 24, str(especie or ''))
        canvas_obj.drawString(135, y - 36, str(raza or ''))

        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(340, y, "FECHA:")
        canvas_obj.drawString(340, y - 12, "MEDICO SOLICITANTE:")
        canvas_obj.drawString(340, y - 24, "SEXO:")
        canvas_obj.drawString(340, y - 36, "EDAD:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(445, y, str(fecha or ''))
        canvas_obj.drawString(445, y - 12, str(medico or ''))
        canvas_obj.drawString(445, y - 24, str(sexo or ''))
        canvas_obj.drawString(445, y - 36, str(edad or ''))

    template = PageTemplate(id='HojaEstudio', frames=frame_contenido, onPage=dibujar_encabezado_paciente)
    doc.addPageTemplates([template])

    styles = getSampleStyleSheet()
    estilo_celda = ParagraphStyle('Celda', parent=styles['Normal'], fontName='Helvetica', fontSize=7.5, leading=9)
    estilo_celda_hdr = ParagraphStyle('CeldaHdr', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=8, leading=9, textColor=colors.HexColor("#2C3E50"))
    estilo_obs = ParagraphStyle('Obs', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=8, leading=11, textColor=colors.HexColor("#2C3E50"))

    # Helper para armar tablas dinámicas
    def crear_bloque_tabla(titulo, lista_datos, color_hex="#117A65"):
        elementos = []
        
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
        elementos.append(hdr_table)

        tabla_data = [[
            Paragraph("PARÁMETRO", estilo_celda_hdr),
            Paragraph("RESULTADO", estilo_celda_hdr),
            Paragraph("UNIDAD", estilo_celda_hdr),
            Paragraph("RANGOS REFERENCIA", estilo_celda_hdr)
        ]]
        
        for fila in lista_datos:
            p = str(fila[0]) if len(fila) > 0 else ""
            r = str(fila[1]) if len(fila) > 1 else ""
            u = str(fila[2]) if len(fila) > 2 else ""
            ref = str(fila[3]) if len(fila) > 3 else ""
            
            tabla_data.append([
                Paragraph(p, estilo_celda),
                Paragraph(r, estilo_celda),
                Paragraph(u, estilo_celda),
                Paragraph(ref, estilo_celda)
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
        elementos.append(t)
        elementos.append(Spacer(1, 8))
        return elementos

    story = []

    # Bloques condicionales
    if datos_estudio.get('hem_roja'):
        story.extend(crear_bloque_tabla("🔴 FÓRMULA ROJA (ERITROGRAMA)", datos_estudio['hem_roja'], "#900C3F"))

    if datos_estudio.get('hem_blanca'):
        story.extend(crear_bloque_tabla("⚪ FÓRMULA BLANCA Y PLAQUETAS (LEUCOGRAMA)", datos_estudio['hem_blanca'], "#2C3E50"))

    if datos_estudio.get('qs_items'):
        story.extend(crear_bloque_tabla("🧪 BIOQUÍMICA CLÍNICA", datos_estudio['qs_items'], "#1B4F72"))

    if datos_estudio.get('endo_items'):
        story.extend(crear_bloque_tabla("⚕️ ENDOCRINOLOGÍA", datos_estudio['endo_items'], "#2874A6"))

    # Urianálisis
    if datos_estudio.get('uri_fisico'):
        story.extend(crear_bloque_tabla("🧪 URIANÁLISIS - EXAMEN FÍSICO", datos_estudio['uri_fisico'], "#117A65"))

    if datos_estudio.get('uri_quimico'):
        story.extend(crear_bloque_tabla("🔬 URIANÁLISIS - EXAMEN QUÍMICO", datos_estudio['uri_quimico'], "#117A65"))

    if datos_estudio.get('uri_micro'):
        story.extend(crear_bloque_tabla("🔬 URIANÁLISIS - SEDIMENTO Y MICROSCOPÍA", datos_estudio['uri_micro'], "#117A65"))

    if datos_estudio.get('obs_urianalisis'):
        story.append(Paragraph(f"<b>Observaciones Urinarias:</b> {datos_estudio['obs_urianalisis']}", estilo_obs))
        story.append(Spacer(1, 8))

    # Copro / Sero / Cito
    if datos_estudio.get('copro_items'):
        story.append(Paragraph("<b>💩 COPROPARASITOSCÓPICO Y COPROLÓGICO</b>", estilo_celda_hdr))
        for param, val in datos_estudio['copro_items']:
            story.append(Paragraph(f"• {param}: {val}", estilo_celda))
        story.append(Spacer(1, 6))

    if datos_estudio.get('sero_items'):
        story.append(Paragraph("<b>🩸 PRUEBAS RÁPIDAS Y SEROLOGÍA</b>", estilo_celda_hdr))
        for prueba, resultado in datos_estudio['sero_items']:
            story.append(Paragraph(f"Prueba: {prueba} | Resultado: {resultado}", estilo_celda))
        story.append(Spacer(1, 6))

    if datos_estudio.get('cito_items'):
        story.append(Paragraph("<b>🔬 CITOLOGÍA Y DERMATOLOGÍA</b>", estilo_celda_hdr))
        for param, val in datos_estudio['cito_items']:
            story.append(Paragraph(f"{param}: {val}", estilo_celda))
        story.append(Spacer(1, 6))

    # Observaciones Generales
    if observaciones_txt:
        hdr_obs = Table([["💬 OBSERVACIONES Y NOTAS CLÍNICAS"]], colWidths=[522], rowHeights=[16])
        hdr_obs.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#2E4053")),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 8.5),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))
        story.append(hdr_obs)
        story.append(Spacer(1, 4))
        for line in str(observaciones_txt).split('\n'):
            if line.strip():
                story.append(Paragraph(line.strip(), estilo_obs))

    # Generación con NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)

    # Nomenclatura del archivo
    estudio_clean = str(estudio_id or '').strip().replace(' ', '_')
    tipo_clean = str(tipo_estudio or '').strip().replace(' ', '_').replace('(', '').replace(')', '').replace('+', 'Y')
    especie_clean = str(especie or '').strip().replace(' ', '_')
    paciente_clean = str(paciente or '').strip().replace(' ', '_')

    nombre_archivo_pdf = f"{estudio_clean}_{tipo_clean}_{especie_clean}_{paciente_clean}.pdf"

    return buffer.getvalue(), nombre_archivo_pdf
