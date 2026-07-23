# app.py
import streamlit as st

# Importamos nuestros módulos locales
from formularios import (
    modulo_hematologia, modulo_bioquimica, modulo_serologia, 
    modulo_endocrino, modulo_citologia, modulo_urianalisis, modulo_copro
)
from generador_pdf import generar_pdf_cedivet

# ==========================================
# BLOQUE 1: CONFIGURACIÓN
# ==========================================
st.set_page_config(page_title="CEDIVET - Generador de Reportes", layout="wide")
st.title("🧪 CENTRO DIAGNÓSTICO VETERINARIO - CEDIVET")
st.caption("Sistema automatizado de captura y generación de reportes clínicos.")

st.markdown("""
<style>
    .card-qs { background-color: #EBF5FB; border-left: 6px solid #1B4F72; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-hem { background-color: #FDEDEC; border-left: 6px solid #900C3F; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-uri { background-color: #FEF9E7; border-left: 6px solid #B7950B; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-cop { background-color: #F5EEF8; border-left: 6px solid #6C3483; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-obs { background-color: #EAEDED; border-left: 6px solid #2E4053; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-sero { background-color: #F9E79F; border-left: 6px solid #D4AC0D; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-endo { background-color: #D6EAF8; border-left: 6px solid #2874A6; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
    .card-cito { background-color: #FADBD8; border-left: 6px solid #C0392B; padding: 12px; border-radius: 6px; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# ==========================================
# BLOQUE 2: PACIENTE
# ==========================================
st.subheader("1. Datos Generales del Paciente")
c1, c2, c3 = st.columns(3)
with c1:
    estudio_id = st.text_input("📝 No. Estudio", "JL-27-26")
    especie = st.selectbox("🐾 Especie", ["CANIDEO", "FELINO"])
    sexo = st.selectbox("♀️♂️ Sexo", ["HEMBRA", "MACHO"])
with c2:
    fecha = st.text_input("📅 Fecha", "22 DE JULIO DEL 2026")
    raza = st.text_input("🐕/🐈 Raza", "MESTIZO")
    edad = st.text_input("🎂 Edad", "7 AÑOS")
with c3:
    medico = st.text_input("🩺 Médico Solicitante", "MVZ. JASMIN RIVERA")
    paciente = st.text_input("🏷️ Nombre / Identificación", "PIZZA PEREZ")

es_felino = (especie == "FELINO")
st.markdown("---")

# ==========================================
# BLOQUE 3: ENRUTADOR
# ==========================================
col_cat, col_est = st.columns(2)
with col_cat:
    categoria = st.selectbox(
        "📂 Categoría de Análisis",
        ["Hematología", "Bioquímica Clínica (QS)", "Urianálisis y Copro", 
         "Serología y Pruebas Rápidas", "Endocrinología", "Citología / Dermatología", "Paquetes y Perfiles"]
    )
with col_est:
    if categoria == "Hematología":
        tipo_estudio = st.selectbox("🔬 Estudio:", ["Hemograma Completo", "Fórmula Roja", "Fórmula Blanca", "Tiempos de Coagulación (TP, TTP)"])
    elif categoria == "Bioquímica Clínica (QS)":
        tipo_estudio = st.selectbox("🔬 Perfil:", ["QS 1 (Básica / Renal)", "QS 2 (Hepático I)", "QS 3 (Hepático II)", "QS 4 (Pancreático I)", "QS 5 (General / Completa)", "QS 6 (Pancreático II)", "QS 7 (Páncreas Endocrino / Lípidos)", "Electrolitos Sanguíneos (Na, K, Cl)"])
    elif categoria == "Urianálisis y Copro":
        tipo_estudio = st.selectbox("🔬 Estudio:", ["Urianálisis Completo", "Coproparasitoscópico por Flotación", "Coproparasitoscópico Serie (3 muestras)", "Perfil Coprológico Físico-Químico"])
    elif categoria == "Serología y Pruebas Rápidas":
        tipo_estudio = st.selectbox("🔬 Prueba:", ["Prueba Snap 4Dx (Canino)", "Prueba SIDA/Leucemia VIF/ViLeF (Felino)", "Prueba Rápida Parvovirus", "Prueba Rápida Giardia", "Prueba Rápida Moquillo"])
    elif categoria == "Endocrinología":
        tipo_estudio = st.selectbox("🔬 Estudio:", ["Perfil Tiroideo (T4 Tot, TSH)", "T4 Total", "Cortisol Basal"])
    elif categoria == "Citología / Dermatología":
        tipo_estudio = st.selectbox("🔬 Estudio:", ["Raspado Cutáneo (Ectoparásitos)", "Citología Ótica", "Citología de Masa/Piel"])
    elif categoria == "Paquetes y Perfiles":
        tipo_estudio = st.selectbox("🔬 Paquete:", ["Perfil General (Hemograma + QS 5)", "Perfil General Completo (Hemograma + QS 5 + Urianálisis)", "Paquete Renal (Hemograma + QS 1 + Urianálisis)", "Perfil Hepático-Renal (Hemograma + QS 1 + QS 2)", "Perfil Geriatra (Hemograma + QS 5 + Urianálisis + Copro)", "Perfil Gastrointestinal (Hemograma + QS 4 + Copro)", "Prequirúrgico 1 (Hemograma + Gluc, Urea, Creat, ALT, TP, TTP)", "Prequirúrgico 2 (Hemograma + Urea, Creat, Prot. Totales)", "Prequirúrgico 3 (Hemograma + QS 1 + TP, TTP)", "Paquete Adopción Responsable (Hemograma + Copro + Snap Serológico)"])

necesita_roja = any(x in tipo_estudio for x in ["Hemograma", "Fórmula Roja", "Perfil", "Paquete", "Prequirúrgico"])
necesita_blanca = any(x in tipo_estudio for x in ["Hemograma", "Fórmula Blanca", "Perfil", "Paquete", "Prequirúrgico"])
necesita_qs = any(x in tipo_estudio for x in ["QS", "Perfil", "Paquete Renal", "Prequirúrgico", "Electrolitos"])
necesita_uri = any(x in tipo_estudio for x in ["Urianálisis", "Paquete Renal", "Perfil Geriatra", "Perfil General Completo"])
necesita_copro = any(x in tipo_estudio for x in ["Copro", "Gastrointestinal", "Geriatra", "Adopción"])
necesita_sero = any(x in tipo_estudio for x in ["Snap", "SIDA/Leucemia", "Rápida", "Adopción"])
necesita_endo = categoria == "Endocrinología"
necesita_cito = categoria == "Citología / Dermatología"

st.markdown("---")
st.subheader(f"📋 Formulario de Entrada: {tipo_estudio}")

# ==========================================
# BLOQUE 4: RENDERIZADO DE FORMULARIOS
# ==========================================
datos_estudio = {}

if necesita_roja or necesita_blanca:
    datos_estudio.update(modulo_hematologia(es_felino, necesita_roja, necesita_blanca))
if necesita_qs:
    datos_estudio.update(modulo_bioquimica(es_felino, tipo_estudio))
if necesita_sero:
    datos_estudio.update(modulo_serologia(tipo_estudio))
if necesita_endo:
    datos_estudio.update(modulo_endocrino(es_felino))
if necesita_cito:
    datos_estudio.update(modulo_citologia())
if necesita_uri:
    datos_estudio.update(modulo_urianalisis(es_felino))
if necesita_copro:
    datos_estudio.update(modulo_copro())

st.markdown("---")
st.markdown('<div class="card-obs"><b>💬 OBSERVACIONES / NOTAS CLÍNICAS</b></div>', unsafe_allow_html=True)
observaciones_txt = st.text_area("Notas para el reporte:", "Muestra procesada bajo protocolos estándares. Correlacionar con cuadro clínico.")

# ==========================================
# BLOQUE 5: GENERADOR PDF
# ==========================================
st.markdown("---")
if st.button("📄 Generar PDF Oficial CEDIVET", type="primary"):
    pdf_bytes, nombre_archivo = generar_pdf_cedivet(
        estudio_id, paciente, especie, raza, fecha, medico, sexo, edad, 
        tipo_estudio, datos_estudio, observaciones_txt
    )
    st.success("¡Reporte generado exitosamente!")
    st.download_button(label="⬇️ Descargar PDF", data=pdf_bytes, file_name=nombre_archivo, mime="application/pdf")