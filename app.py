import streamlit as st
import json
from supabase import create_client, Client

# Importamos nuestros módulos locales
from formularios import (
    modulo_hematologia, modulo_bioquimica, modulo_serologia,  
    modulo_endocrino, modulo_citologia, modulo_urianalisis, modulo_copro
)
from generador_pdf import generar_pdf_cedivet

# ==========================================
# CONFIGURACIÓN INICIAL Y SUPABASE
# ==========================================
st.set_page_config(page_title="CEDIVET - Generador de Reportes", layout="wide")

@st.cache_resource
def init_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["key"]
    return create_client(url, key)

supabase: Client = init_supabase()

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
# BARRA LATERAL: ARCHIVERO CLÍNICO AVANZADO
# ==========================================
st.sidebar.header("📁 Archivero Clínico")
busqueda_input = st.sidebar.text_input("Buscar por ID o Paciente (ej. JL-27-26 o Pizza)")

if "datos_cargados" not in st.session_state:
    st.session_state["datos_cargados"] = None

if busqueda_input:
    try:
        response = supabase.table("estudios").select("*").or_(f"estudio_id.ilike.%{busqueda_input}%,paciente.ilike.%{busqueda_input}%").execute()
        if response.data:
            st.sidebar.success(f"Se encontraron {len(response.data)} registro(s).")
            opciones_estudios = {
                f"{row['estudio_id']} - {row['paciente']} ({row['tipo_estudio']} - {row['fecha']})": row 
                for row in response.data
            }
            estudio_seleccionado_key = st.sidebar.selectbox("Selecciona el estudio exacto:", list(opciones_estudios.keys()))
            
            if st.sidebar.button("📥 Cargar estudio al formulario"):
                st.session_state["datos_cargados"] = opciones_estudios[estudio_seleccionado_key]
                st.sidebar.success("¡Estudio cargado con éxito!")
        else:
            st.sidebar.warning("No se encontraron registros.")
    except Exception as e:
        st.sidebar.error(f"Error en búsqueda: {e}")

datos_recuperados = st.session_state["datos_cargados"]

if datos_recuperados:
    st.sidebar.info(f"Editando expediente: **{datos_recuperados['estudio_id']}**")
    if st.sidebar.button("❌ Limpiar / Nuevo Estudio"):
        st.session_state["datos_cargados"] = None
        st.success("Formulario limpiado. Listo para un nuevo estudio.")

# Extraemos el diccionario interno de resultados guardados si existe
resultados_previos = datos_recuperados.get("datos_estudio", {}) if datos_recuperados else {}

# ==========================================
# BLOQUE 2: PACIENTE Y VARIABLES INICIALES
# ==========================================
st.subheader("1. Datos Generales del Paciente")
c1, c2, c3 = st.columns(3)

def_id = datos_recuperados["estudio_id"] if datos_recuperados else "JL-27-26"
def_esp_idx = 0 if not datos_recuperados or datos_recuperados.get("especie") == "CANIDEO" else 1
def_fec = datos_recuperados["fecha"] if datos_recuperados else "22 DE JULIO DEL 2026"
def_raz = datos_recuperados["raza"] if datos_recuperados else "MESTIZO"
def_eda = datos_recuperados["edad"] if datos_recuperados else "7 AÑOS"
def_med = datos_recuperados["medico"] if datos_recuperados else "MVZ. JASMIN RIVERA"
def_pac = datos_recuperados["paciente"] if datos_recuperados else "PIZZA PEREZ"

with c1:
    estudio_id = st.text_input("📝 No. Estudio (Recomendación: usa un sufijo único si repites clave, ej. JL-27-26-02)", def_id)
    especie = st.selectbox("🐾 Especie", ["CANIDEO", "FELINO"], index=def_esp_idx)
    sexo = st.selectbox("♀️♂️ Sexo", ["HEMBRA", "MACHO"])
with c2:
    fecha = st.text_input("📅 Fecha", def_fec)
    raza = st.text_input("🐕/🐈 Raza", def_raz)
    edad = st.text_input("🎂 Edad", def_eda)
with c3:
    medico = st.text_input("🩺 Médico Solicitante", def_med)
    paciente = st.text_input("🏷️ Nombre / Identificación", def_pac)

es_felino = (especie == "FELINO")
st.markdown("---")

# ==========================================
# BLOQUE 3: ENRUTADOR DE CATEGORÍAS
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
# BLOQUE 4: RENDERIZADO DE FORMULARIOS CON DATOS PRECARGADOS
# ==========================================
datos_estudio = {}

# Nota: Tus módulos actuales generan los inputs de Streamlit. Si tus funciones de formularios 
# aceptan un diccionario de valores previos (ej. 'datos_previos=resultados_previos'), 
# asegúrate de pasárselo. Aquí ejecutamos la recolección estándar:
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
def_obs = datos_recuperados.get("observaciones", "Muestra procesada bajo protocolos estándares. Correlacionar con cuadro clínico.") if datos_recuperados else "Muestra procesada bajo protocolos estándares. Correlacionar con cuadro clínico."
observaciones_txt = st.text_area("Notas para el reporte:", def_obs)

# ==========================================
# BLOQUE 5: GENERADOR PDF Y BASE DE DATOS
# ==========================================
st.markdown("---")
if st.button("📄 Generar PDF Oficial CEDIVET", type="primary"):
    
    # 1. Generar el PDF
    pdf_bytes, nombre_archivo = generar_pdf_cedivet(
        estudio_id, paciente, especie, raza, fecha, medico, sexo, edad, 
        tipo_estudio, datos_estudio, observaciones_txt
    )
    
    # 2. Empaquetar para Supabase
    paquete_datos = {
        "estudio_id": estudio_id,
        "paciente": paciente,
        "especie": especie,
        "raza": raza,
        "fecha": fecha,
        "medico": medico,
        "sexo": sexo,
        "edad": edad,
        "tipo_estudio": tipo_estudio,
        "datos_estudio": datos_estudio,  
        "observaciones": observaciones_txt
    }

    # 3. Guardar / Actualizar en la nube asegurando unicidad por estudio_id
    try:
        supabase.table("estudios").upsert(paquete_datos, on_conflict="estudio_id").execute()
        st.success("¡Estudio guardado y sincronizado de forma independiente en la nube!")
    except Exception as e:
        st.error(f"Error al guardar en la base de datos: {e}")

    st.success("¡Reporte generado exitosamente!")
    st.download_button(label="⬇️ Descargar PDF", data=pdf_bytes, file_name=nombre_archivo, mime="application/pdf")
