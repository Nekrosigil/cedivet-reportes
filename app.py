import os
import io
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors

st.set_page_config(page_title="CEDIVET - Generador de Reportes", layout="wide")

st.title("🧪 CENTRO DIAGNÓSTICO VETERINARIO - CEDIVET")
st.caption("Sistema automatizado de captura y generación de reportes clínicos en PDF.")

# CSS personalizado para diferenciar campos manuales
st.markdown("""
<style>
    .manual-header {
        background-color: #f0f2f6;
        padding: 8px;
        border-radius: 5px;
        border-left: 5px solid #ff4b4b;
        font-weight: bold;
        margin-bottom: 10px;
    }
    .auto-header {
        background-color: #e8f4f8;
        padding: 8px;
        border-radius: 5px;
        border-left: 5px solid #1c83e1;
        font-weight: bold;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- 1. DATOS DEL PACIENTE ---
st.subheader("1. Datos Generales del Paciente (Entrada Manual)")
c1, c2, c3 = st.columns(3)

with c1:
    estudio_id = st.text_input("📝 No. Estudio", "JL-27-26")
    especie = st.text_input("🐶 Especie", "CANIDEO")
    sexo = st.selectbox("♀️♂️ Sexo", ["HEMBRA", "MACHO"])

with c2:
    fecha = st.text_input("📅 Fecha", "12 DE JULIO DEL 2026")
    raza = st.text_input("🐕 Raza", "MESTIZO")
    edad = st.text_input("🎂 Edad", "7 AÑOS")

with c3:
    medico = st.text_input("🩺 Médico Solicitante", "MVZ. JASMIN RIVERA")
    paciente = st.text_input("🏷️ Nombre / Identificación", "PIZZA PEREZ")

st.markdown("---")

# --- 2. CAPTURA DE ESTUDIO ---
tipo_estudio = st.selectbox("🔬 Selecciona el Estudio a Procesar:", ["Biometría Hemática", "Química Sanguínea", "Urianálisis"])

datos_estudio = {}

if tipo_estudio == "Biometría Hemática":
    col_izq, col_der = st.columns(2)
    
    with col_izq:
        st.markdown('<div class="manual-header">🔴 FÓRMULA ROJA - Captura Manual de Valores</div>', unsafe_allow_html=True)
        
        eritrocitos = st.number_input("Eritrocitos (millones por mm³)", value=5.60, step=0.01, format="%.2f")
        hemoglobina = st.number_input("Hemoglobina (g/dl)", value=13.00, step=0.1, format="%.1f")
        hematocrito = st.number_input("Hematocrito (%)", value=38.00, step=0.1, format="%.1f")
        vsg = st.text_input("V.S.G. (mm/h)", "4")
        plaquetas = st.text_input("Plaquetas (por mm³)", "208,000")
        reticulocitos = st.text_input("Reticulocitos (%)", "0.1%")

        # --- CÁLCULOS AUTOMÁTICOS FÓRMULA ROJA ---
        vgm_calc = (hematocrito * 10) / eritrocitos if eritrocitos > 0 else 0.0
        hgm_calc = (hemoglobina * 10) / eritrocitos if eritrocitos > 0 else 0.0
        chgm_calc = (hemoglobina * 100) / hematocrito if hematocrito > 0 else 0.0

        st.markdown('<div class="auto-header">⚡ ÍNDICES ERITROCITARIOS (Calculados Automáticamente)</div>', unsafe_allow_html=True)
        st.info(f"**V.G.M.:** {vgm_calc:.1f} micras³\n\n"
                f"**H.G.M.:** {hgm_calc:.1f} Uug\n\n"
                f"**C.H.G.M.:** {chgm_calc:.1f} %")

        datos_estudio['eritrocitos'] = f"{eritrocitos:.2f}"
        datos_estudio['hemoglobina'] = f"{hemoglobina:.1f}"
        datos_estudio['hematocrito'] = f"{hematocrito:.1f}"
        datos_estudio['vgm'] = f"{vgm_calc:.1f}"
        datos_estudio['hgm'] = f"{hgm_calc:.1f}"
        datos_estudio['chgm'] = f"{chgm_calc:.1f}"
        datos_estudio['vsg'] = vsg
        datos_estudio['plaquetas'] = plaquetas
        datos_estudio['reticulocitos'] = reticulocitos

    with col_der:
        st.markdown('<div class="manual-header">⚪ FÓRMULA BLANCA - Conteo y Diferencial Leucocitario</div>', unsafe_allow_html=True)
        
        leucocitos_totales = st.number_input("Leucocitos Totales (Cels/µl)", value=10200, step=100)
        
        st.write("**Porcentajes Relativos (%)**")
        pct_linfocitos = st.number_input("% Linfocitos", value=22.0, step=0.5)
        pct_monocitos = st.number_input("% Monocitos", value=1.0, step=0.5)
        pct_eosinofilos = st.number_input("% Eosinófilos", value=2.0, step=0.5)
        pct_basofilos = st.number_input("% Basófilos", value=0.0, step=0.5)
        pct_mielocitos = st.number_input("% Mielocitos", value=0.0, step=0.5)
        pct_juveniles = st.number_input("% Juveniles", value=0.0, step=0.5)
        
        st.markdown("---")
        st.write("**Desglose de Neutrófilos**")
        pct_banda = st.number_input("% Neutrófilos en Banda", value=2.0, step=0.5)
        pct_segmentados = st.number_input("% Neutrófilos Segmentados", value=73.0, step=0.5)
        
        pct_neutrofilos_total = pct_banda + pct_segmentados

        # --- CÁLCULOS AUTOMÁTICOS FÓRMULA BLANCA ---
        st.markdown('<div class="auto-header">⚡ VALORES ABSOLUTOS (Calculados Automáticamente)</div>', unsafe_allow_html=True)
        
        poblaciones_pct = {
            "Linfocitos": pct_linfocitos,
            "Monocitos": pct_monocitos,
            "Eosinófilos": pct_eosinofilos,
            "Basófilos": pct_basofilos,
            "Mielocitos": pct_mielocitos,
            "Juveniles": pct_juveniles,
            "Banda": pct_banda,
            "Segmentados": pct_segmentados
        }
        
        diferencial_completo = {}
        abs_summary = ""
        for nombre, pct_val in poblaciones_pct.items():
            abs_val = int((leucocitos_totales * pct_val) / 100)
            diferencial_completo[nombre] = (pct_val, abs_val)
            abs_summary += f"• **{nombre}:** {abs_val:,} Cels/µl ({pct_val}%)\n"
            
        st.info(f"**Neutrófilos Totales:** {pct_neutrofilos_total}%\n\n" + abs_summary)

        datos_estudio['leucocitos_totales'] = f"{leucocitos_totales:,}"
        datos_estudio['pct_neutrofilos_total'] = pct_neutrofilos_total
        datos_estudio['diferencial'] = diferencial_completo

    st.markdown("---")
    st.markdown('<div class="manual-header">✍️ OBSERVACIONES E INTERPRETACIÓN</div>', unsafe_allow_html=True)
    datos_estudio['formula_roja_obs'] = st.text_area("Fórmula Roja (Observaciones)", "ANISOCITOSIS LEVE, EQUINOCITOS ++, EQUINOCITOS +++")
    datos_estudio['interpretacion'] = st.text_area("Interpretación", "LEUCOCITOSIS CON NEUTROFILIA HIPERSEGMENTADA.")

# --- 3. GENERACIÓN DE PDF ---
st.markdown("---")
if st.button("📄 Generar PDF del Reporte Oficial", type="primary"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    
    # A) FONDO Y MEMBRETE (TAMAÑO CARTA COMPLETO)
    if os.path.exists("marca_agua.png"):
        c.drawImage("marca_agua.png", 0, 0, width=612, height=792)

    # B) DATOS DEL PACIENTE (ALINEADOS DEBAJO DE LA LÍNEA DEL ENCABEZADO)
    y_paciente = 660
    c.setFont("Helvetica-Bold", 8)
    c.drawString(45, y_paciente, "ESTUDIO:")
    c.drawString(400, y_paciente, "FECHA:")
    c.drawString(45, y_paciente - 14, "ESPECIE:")
    c.drawString(45, y_paciente - 28, "RAZA:")
    c.drawString(45, y_paciente - 42, "SEXO:")
    c.drawString(45, y_paciente - 56, "IDENTIFICACION:")
    c.drawString(45, y_paciente - 70, "EDAD:")

    c.setFont("Helvetica", 8)
    c.drawString(130, y_paciente, estudio_id)
    c.drawString(445, y_paciente, fecha)
    c.drawString(130, y_paciente - 14, especie)
    c.drawString(130, y_paciente - 28, raza)
    c.drawString(130, y_paciente - 42, sexo)
    c.drawString(130, y_paciente - 56, paciente)
    c.drawString(130, y_paciente - 70, edad)

    # C) TITULO DEL ESTUDIO
    y = y_paciente - 95
    c.setFont("Helvetica-Bold", 10)
    c.drawString(45, y, "BIOMETRÍA HEMATICA")
    c.drawString(380, y, "VALORES DE REFERENCIA")
    
    y -= 14
    c.setFont("Helvetica", 7.5)
    
    # Tabla Serie Roja
    items_roja = [
        ("ERITROCITOS:", datos_estudio['eritrocitos'], "millones por mm³", "5.5 - 8.5"),
        ("HEMOGLOBINA:", datos_estudio['hemoglobina'], "g/dl", "12 - 19.5"),
        ("HEMATOCRITO:", datos_estudio['hematocrito'], "%", "33 - 55"),
        ("V.G.M.:", datos_estudio['vgm'], "micras 3", "60 - 77"),
        ("C.H.G.M.:", datos_estudio['chgm'], "%", "32 - 36"),
        ("H.G.M.:", datos_estudio['hgm'], "Uug", "19.5 - 24"),
        ("V.S.G.:", datos_estudio['vsg'], "mm/h", "0 - 13")
    ]
    
    for param, res, unidad, ref in items_roja:
        c.drawString(45, y, param)
        c.drawString(180, y, str(res))
        c.drawString(240, y, unidad)
        c.drawString(380, y, ref)
        y -= 12

    # Encabezado Leucocitos
    y -= 5
    c.setFont("Helvetica-Bold", 8)
    c.drawString(380, y, "VALORES DE REFERENCIA")
    
    y -= 12
    c.setFont("Helvetica", 7.5)
    c.drawString(45, y, "LEUCOCITOS:")
    c.drawString(180, y, "RANGO %")
    c.drawString(270, y, "VALORES ABSOLUTOS")
    c.drawString(410, y, "Cels/µl")

    y -= 12
    c.setFont("Helvetica-Bold", 8)
    c.drawString(45, y, "TOTAL:")
    c.drawString(180, y, str(datos_estudio['leucocitos_totales']))
    c.drawString(410, y, "6,000 - 15,000")

    ref_poblaciones = {
        "Linfocitos": ("12 - 30%", "1,000 - 4,800"),
        "Monocitos": ("2 - 10%", "150 - 1,350"),
        "Neutrófilos": (f"{datos_estudio['pct_neutrofilos_total']}%", "3,000 - 11,000"),
        "Eosinófilos": ("2 - 10%", "100 - 1,250"),
        "Basófilos": ("0%", "0"),
        "Mielocitos": ("0%", "0"),
        "Juveniles": ("0%", "0"),
        "Banda": ("0 - 3%", "0 - 500"),
        "Segmentados": ("60 - 77%", "3,000 - 11,000")
    }

    y -= 12
    c.setFont("Helvetica", 7.5)
    for celula, (pct_val, abs_val) in datos_estudio['diferencial'].items():
        if celula == "Eosinófilos":
            # Línea de Neutrófilos Totales
            c.setFont("Helvetica-Bold", 7.5)
            c.drawString(45, y, "NEUTROFILOS:")
            pct_n, abs_n = ref_poblaciones["Neutrófilos"]
            c.drawString(180, y, pct_n)
            c.drawString(410, y, abs_n)
            y -= 11
            c.setFont("Helvetica", 7.5)

        pct_ref, abs_ref = ref_poblaciones.get(celula, ("-", "-"))
        
        # Sangría para los tipos de neutrófilos
        indent = 65 if celula in ["Mielocitos", "Juveniles", "Banda", "Segmentados"] else 45
        c.drawString(indent, y, celula.upper() + ":")
        c.drawString(180, y, str(pct_val))
        c.drawString(270, y, f"{abs_val:,}")
        c.drawString(410, y, abs_ref)
        y -= 11

    # Plaquetas y Reticulocitos
    y -= 5
    c.drawString(45, y, f"PLAQUETAS:  {datos_estudio['plaquetas']}")
    c.drawString(380, y, "200 - 400 mil por mm³")
    y -= 12
    c.drawString(45, y, f"RETICULOCITOS:  {datos_estudio['reticulocitos']}")
    c.drawString(380, y, "0 - .15%")

    # Observaciones e Interpretación
    y -= 20
    c.setFont("Helvetica-Bold", 8)
    c.drawString(45, y, "FORMULA ROJA:")
    c.setFont("Helvetica", 8)
    c.drawString(130, y, datos_estudio['formula_roja_obs'])
    
    y -= 14
    c.setFont("Helvetica-Bold", 8)
    c.drawString(45, y, "INTERPRETACION:")
    c.setFont("Helvetica", 8)
    c.drawString(130, y, datos_estudio['interpretacion'])

    # D) PIE DE PÁGINA Y FIRMAS (ALINEADOS A LA PARTE INFERIOR)
    c.setFont("Helvetica", 8)
    c.drawString(45, 95, "Sin más por el momento le enviamos un cordial saludo.")
    
    c.setFont("Helvetica-Bold", 8)
    c.drawString(45, 75, "Patóloga Clínica Responsable")
    c.drawString(45, 62, "M.V.Z Norabel Pérez Conde")
    c.drawString(45, 50, "CED. PROF 2345183")

    c.drawString(320, 62, "M.M.V.Z Rosario Arvizu Venegas")
    c.drawString(320, 50, "CED. PROF 3971744")

    c.save()
    
    st.success("¡PDF generado con membrete exacto y cálculos automáticos!")
    st.download_button(
        label="⬇️ Descargar Reporte PDF",
        data=buffer.getvalue(),
        file_name=f"Reporte_BH_{paciente}.pdf",
        mime="application/pdf"
    )