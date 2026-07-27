import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors

# ==========================================
# CANVAS EN DOS PASADAS PARA PAGINACIÓN
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
            # Pie de página dinámico en cada hoja
            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#5D6D7E"))
            self.drawRightString(567, 25, f"Página {self._pageNumber} de {page_count if 'page_count' in locals() else num_pages}")
            super().showPage()
        super().save()


def generar_pdf_cedivet(estudio_id, paciente, especie, raza, fecha, medico, sexo, edad, tipo_estudio, datos_estudio, observaciones_txt):
    buffer = io.BytesIO()
    c = NumberedCanvas(buffer, pagesize=letter)
    
    # Límite inferior para no pisar la firma (margen de seguridad)
    LIMITE_INFERIOR = 110
    Y_INICIAL = 665

    def aplicar_fondo(canvas_obj):
        if os.path.exists("marca_agua.jpg"):
            canvas_obj.drawImage("marca_agua.jpg", 0, 0, width=612, height=792)
        elif os.path.exists("marca_agua.png"):
            canvas_obj.drawImage("marca_agua.png", 0, 0, width=612, height=792)

    def dibujar_encabezado_paciente(canvas_obj, pos_y):
        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.setFillColor(colors.HexColor("#1A252C"))

        canvas_obj.drawString(45, pos_y, "NO. ESTUDIO:")
        canvas_obj.drawString(45, pos_y - 12, "PACIENTE / IDENT.:")
        canvas_obj.drawString(45, pos_y - 24, "ESPECIE:")
        canvas_obj.drawString(45, pos_y - 36, "RAZA:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(135, pos_y, str(estudio_id or ''))
        canvas_obj.drawString(135, pos_y - 12, str(paciente or ''))
        canvas_obj.drawString(135, pos_y - 24, str(especie or ''))
        canvas_obj.drawString(135, pos_y - 36, str(raza or ''))

        canvas_obj.setFont("Helvetica-Bold", 8)
        canvas_obj.drawString(340, pos_y, "FECHA:")
        canvas_obj.drawString(340, pos_y - 12, "MEDICO SOLICITANTE:")
        canvas_obj.drawString(340, pos_y - 24, "SEXO:")
        canvas_obj.drawString(340, pos_y - 36, "EDAD:")

        canvas_obj.setFont("Helvetica", 8)
        canvas_obj.drawString(445, pos_y, str(fecha or ''))
        canvas_obj.drawString(445, pos_y - 12, str(medico or ''))
        canvas_obj.drawString(445, pos_y - 24, str(sexo or ''))
        canvas_obj.drawString(445, pos_y - 36, str(edad or ''))

    # Inicializar Primera Página
    aplicar_fondo(c)
    dibujar_encabezado_paciente(c, Y_INICIAL)
    y = Y_INICIAL - 55

    # Función para verificar salto de página
    def verificar_salto_pagina(pos_y, alto_requerido):
        if (pos_y - alto_requerido) < LIMITE_INFERIOR:
            c.showPage()  # Cambia a nueva página
            aplicar_fondo(c)
            dibujar_encabezado_paciente(c, Y_INICIAL)
            return Y_INICIAL - 55
        return pos_y

    def dibujar_encabezado_bloque(canvas_obj, titulo, pos_y, color_hex):
        canvas_obj.setFillColor(colors.HexColor(color_hex))
        canvas_obj.rect(45, pos_y - 2, 520, 14, fill=1, stroke=0)
        canvas_obj.setFillColor(colors.white)
        canvas_obj.setFont("Helvetica-Bold", 8.5)
        canvas_obj.drawString(50, pos_y + 2, titulo)
        canvas_obj.setFillColor(colors.HexColor("#1A252C"))

    def dibujar_tabla_estudio(canvas_obj, lista_datos, pos_y):
        tabla_data = [["PARÁMETRO", "RESULTADO", "UNIDAD", "RANGOS REFERENCIA"]]
        for fila in lista_datos:
            p = str(fila[0]) if len(fila) > 0 else ""
            r = str(fila[1]) if len(fila) > 1 else ""
            u = str(fila[2]) if len(fila) > 2 else ""
            ref = str(fila[3]) if len(fila) > 3 else ""
            tabla_data.append([p, r, u, ref])

        t = Table(tabla_data, colWidths=[180, 110, 90, 140])
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EAEDED")),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#2C3E50")),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 7.5),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('ALIGN', (1, 0), (1, -1), 'CENTER'),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
            ('TOPPADDING', (0, 0), (-1, -1), 3),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#BDC3C7")),
        ]))
        
        w, h = t.wrap(520, 400)
        t.drawOn(canvas_obj, 45, pos_y - h)
        return pos_y - h - 10

    # -------------------------------------------------------------
    # IMPRESIÓN DE BLOQUES CON CONTROL AUTOMÁTICO DE SALTO DE PÁGINA
    # -------------------------------------------------------------

    # Hemograma / QS / Endocrinología
    if 'hem_roja' in datos_estudio and datos_estudio['hem_roja']:
        alto_est = len(datos_estudio['hem_roja']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "🔴 FÓRMULA ROJA (ERITROGRAMA)", y, "#900C3F")
        y = dibujar_tabla_estudio(c, datos_estudio['hem_roja'], y - 14)

    if 'hem_blanca' in datos_estudio and datos_estudio['hem_blanca']:
        alto_est = len(datos_estudio['hem_blanca']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "⚪ FÓRMULA BLANCA Y PLAQUETAS (LEUCOGRAMA)", y, "#2C3E50")
        y = dibujar_tabla_estudio(c, datos_estudio['hem_blanca'], y - 14)

    if 'qs_items' in datos_estudio and datos_estudio['qs_items']:
        alto_est = len(datos_estudio['qs_items']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "🧪 BIOQUÍMICA CLÍNICA", y, "#1B4F72")
        y = dibujar_tabla_estudio(c, datos_estudio['qs_items'], y - 14)

    if 'endo_items' in datos_estudio and datos_estudio['endo_items']:
        alto_est = len(datos_estudio['endo_items']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "⚕️ ENDOCRINOLOGÍA", y, "#2874A6")
        y = dibujar_tabla_estudio(c, datos_estudio['endo_items'], y - 14)

    # Urianálisis
    if 'uri_fisico' in datos_estudio and datos_estudio['uri_fisico']:
        alto_est = len(datos_estudio['uri_fisico']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "🧪 URIANÁLISIS - EXAMEN FÍSICO", y, "#117A65")
        y = dibujar_tabla_estudio(c, datos_estudio['uri_fisico'], y - 14)

    if 'uri_quimico' in datos_estudio and datos_estudio['uri_quimico']:
        alto_est = len(datos_estudio['uri_quimico']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "🔬 URIANÁLISIS - EXAMEN QUÍMICO", y, "#117A65")
        y = dibujar_tabla_estudio(c, datos_estudio['uri_quimico'], y - 14)

    if 'uri_micro' in datos_estudio and datos_estudio['uri_micro']:
        alto_est = len(datos_estudio['uri_micro']) * 15 + 30
        y = verificar_salto_pagina(y, alto_est)
        dibujar_encabezado_bloque(c, "🔬 URIANÁLISIS - SEDIMENTO Y MICROSCOPÍA", y, "#117A65")
        y = dibujar_tabla_estudio(c, datos_estudio['uri_micro'], y - 14)

    if datos_estudio.get('obs_urianalisis'):
        y = verificar_salto_pagina(y, 25)
        c.setFont("Helvetica-Bold", 8)
        c.drawString(45, y, "Observaciones Urinarias:")
        c.setFont("Helvetica", 8)
        c.drawString(155, y, str(datos_estudio['obs_urianalisis']))
        y -= 15

    # Copro / Sero / Cito
    if 'copro_items' in datos_estudio and datos_estudio['copro_items']:
        y = verificar_salto_pagina(y, len(datos_estudio['copro_items']) * 12 + 20)
        dibujar_encabezado_bloque(c, "💩 COPROPARASITOSCÓPICO Y COPROLÓGICO", y, "#6C3483")
        y -= 14
        c.setFont("Helvetica", 8)
        for param, val in datos_estudio['copro_items']:
            c.drawString(55, y, f"• {param}: {val}")
            y -= 10
        y -= 6

    if 'sero_items' in datos_estudio and datos_estudio['sero_items']:
        y = verificar_salto_pagina(y, len(datos_estudio['sero_items']) * 14 + 20)
        dibujar_encabezado_bloque(c, "🩸 PRUEBAS RÁPIDAS Y SEROLOGÍA", y, "#D4AC0D")
        y -= 14
        c.setFont("Helvetica", 9)
        for prueba, resultado in datos_estudio['sero_items']:
            c.drawString(55, y, f"Prueba: {prueba}  |  Resultado: {resultado}")
            y -= 12
        y -= 6

    if 'cito_items' in datos_estudio and datos_estudio['cito_items']:
        y = verificar_salto_pagina(y, len(datos_estudio['cito_items']) * 12 + 20)
        dibujar_encabezado_bloque(c, "🔬 CITOLOGÍA Y DERMATOLOGÍA", y, "#C0392B")
        y -= 14
        c.setFont("Helvetica", 8)
        for param, val in datos_estudio['cito_items']:
            c.drawString(55, y, f"{param}: {val}")
            y -= 10
        y -= 6

    # Observaciones Generales
    if observaciones_txt:
        lineas_obs = str(observaciones_txt).split('\n')
        y = verificar_salto_pagina(y, len(lineas_obs) * 12 + 25)
        dibujar_encabezado_bloque(c, "💬 OBSERVACIONES Y NOTAS CLÍNICAS", y, "#2E4053")
        y -= 14
        c.setFont("Helvetica-Oblique", 7.5)
        c.setFillColor(colors.HexColor("#2C3E50"))
        for line in lineas_obs:
            c.drawString(55, y, line)
            y -= 10

    c.save()

    # Nomenclatura del archivo
    estudio_clean = str(estudio_id or '').strip().replace(' ', '_')
    tipo_clean = str(tipo_estudio or '').strip().replace(' ', '_').replace('(', '').replace(')', '').replace('+', 'Y')
    especie_clean = str(especie or '').strip().replace(' ', '_')
    paciente_clean = str(paciente or '').strip().replace(' ', '_')

    nombre_archivo_pdf = f"{estudio_clean}_{tipo_clean}_{especie_clean}_{paciente_clean}.pdf"

    return buffer.getvalue(), nombre_archivo_pdf
