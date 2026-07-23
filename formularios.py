# formularios.py
import streamlit as st

def modulo_hematologia(es_felino, necesita_roja, necesita_blanca):
    datos_locales = {}
    st.markdown('<div class="card-hem"><b>🔴 HEMATOLOGÍA Y HEMOGRAMA COMPLETO</b></div>', unsafe_allow_html=True)
    h_col1, h_col2 = st.columns(2)
    
    if necesita_roja:
        with h_col1:
            st.caption("🔴 **Fórmula Roja (Índices Automatizados)**")
            hto = st.number_input("Hematocrito (%)", value=38.0 if es_felino else 45.0, step=0.5)
            hb = st.number_input("Hemoglobina (g/dL)", value=12.0 if es_felino else 15.0, step=0.1)
            eritrocitos = st.number_input("Eritrocitos (x10^6/µL)", value=7.5 if es_felino else 6.8, step=0.1)
            
            vgm = (hto * 10) / eritrocitos if eritrocitos > 0 else 0.0
            hgm = (hb * 10) / eritrocitos if eritrocitos > 0 else 0.0
            chgm = (hb * 100) / hto if hto > 0 else 0.0
            
            st.info(f"📊 **ÍNDICES:** VGM: {vgm:.1f} fL | HGM: {hgm:.1f} pg | CHGM: {chgm:.1f} g/dL")
            
            ref_roja = {
                "hto": "24.0 - 45.0" if es_felino else "37.0 - 55.0",
                "hb": "8.0 - 15.0" if es_felino else "12.0 - 18.0",
                "eri": "5.00 - 10.00" if es_felino else "5.50 - 8.50",
                "vgm": "39.0 - 55.0" if es_felino else "60.0 - 77.0",
                "hgm": "12.5 - 17.5" if es_felino else "19.5 - 24.5",
                "chgm": "30.0 - 36.0" if es_felino else "32.0 - 36.0"
            }

            datos_locales['hem_roja'] = [
                ("HEMATOCRITO", f"{hto:.1f}", "%", ref_roja["hto"]),
                ("HEMOGLOBINA", f"{hb:.1f}", "g/dL", ref_roja["hb"]),
                ("ERITROCITOS", f"{eritrocitos:.2f}", "x10^6/µL", ref_roja["eri"]),
                ("VGM", f"{vgm:.1f}", "fL", ref_roja["vgm"]),
                ("HGM", f"{hgm:.1f}", "pg", ref_roja["hgm"]),
                ("CHGM", f"{chgm:.1f}", "g/dL", ref_roja["chgm"])
            ]

    if necesita_blanca:
        with h_col2:
            st.caption("⚪ **Fórmula Blanca & Diferencial Automatizado**")
            leucocitos = st.number_input("Leucocitos Totales (x10^3/µL)", value=12.5 if es_felino else 10.5, step=0.1)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                pct_bandas = st.number_input("% Bandas", value=0.0, step=0.5)
                pct_seg = st.number_input("% Segmentados", value=55.0 if es_felino else 70.0, step=0.5)
                pct_linf = st.number_input("% Linfocitos", value=30.0 if es_felino else 20.0, step=0.5)
            with col_p2:
                pct_mono = st.number_input("% Monocitos", value=5.0, step=0.5)
                pct_eos = st.number_input("% Eosinófilos", value=8.0 if es_felino else 4.0, step=0.5)
                pct_baso = st.number_input("% Basófilos", value=2.0 if es_felino else 1.0, step=0.5)

            leu_abs_total = leucocitos * 1000.0
            plaquetas = st.number_input("Plaquetas (x10^3/µL)", value=350.0, step=10.0)

            ref_blanca = {
                "leu": "5.5 - 19.5" if es_felino else "6.0 - 17.0",
                "bandas": "0 - 300" if es_felino else "0 - 300",
                "seg": "2500 - 12500" if es_felino else "3000 - 11500",
                "linf": "1500 - 7000" if es_felino else "1000 - 4800",
                "mono": "0 - 850" if es_felino else "100 - 1400",
                "eos": "100 - 1500" if es_felino else "100 - 1250",
                "baso": "Raros" if es_felino else "Raros",
                "plaq": "300 - 800" if es_felino else "200 - 500"
            }

            datos_locales['hem_blanca'] = [
                ("LEUCOCITOS TOTALES", f"{leucocitos:.1f}", "x10^3/µL", ref_blanca["leu"]),
                ("BANDAS", f"{int((pct_bandas/100)*leu_abs_total)} ({pct_bandas}%)", "/µL", ref_blanca["bandas"]),
                ("SEGMENTADOS", f"{int((pct_seg/100)*leu_abs_total)} ({pct_seg}%)", "/µL", ref_blanca["seg"]),
                ("LINFOCITOS", f"{int((pct_linf/100)*leu_abs_total)} ({pct_linf}%)", "/µL", ref_blanca["linf"]),
                ("MONOCITOS", f"{int((pct_mono/100)*leu_abs_total)} ({pct_mono}%)", "/µL", ref_blanca["mono"]),
                ("EOSINÓFILOS", f"{int((pct_eos/100)*leu_abs_total)} ({pct_eos}%)", "/µL", ref_blanca["eos"]),
                ("BASÓFILOS", f"{int((pct_baso/100)*leu_abs_total)} ({pct_baso}%)", "/µL", ref_blanca["baso"]),
                ("PLAQUETAS", f"{plaquetas:.0f}", "x10^3/µL", ref_blanca["plaq"])
            ]
    return datos_locales

def modulo_bioquimica(es_felino, tipo_estudio):
    datos_locales = {}
    st.markdown('<div class="card-qs"><b>🧪 PARÁMETROS BIOQUÍMICOS (CÁLCULOS AUTOMÁTICOS)</b></div>', unsafe_allow_html=True)
    q_col1, q_col2, q_col3 = st.columns(3)
    
    with q_col1:
        glucosa = st.text_input("Glucosa (mmol/L)", "5.5")
        urea = st.text_input("Urea (mmol/L)", "7.6")
        creatinina = st.text_input("Creatinina (µmol/L)", "110.0" if es_felino else "94.0")
        colesterol = st.text_input("Colesterol (mmol/L)", "4.2")
        trigliceridos = st.text_input("Triglicéridos (mmol/L)", "0.8")

    with q_col2:
        alt = st.text_input("ALT [U/L]", "45.0" if es_felino else "58.7")
        ast = st.text_input("AST [U/L]", "30.0" if es_felino else "43.2")
        fa = st.text_input("Fosfatasa Alcalina (FA) [U/L]", "80.0" if es_felino else "196.0")
        bt = st.number_input("Bilirrubina Total (µmol/L)", value=5.0)
        bd = st.number_input("Bilirrubina Directa/Conjugada (µmol/L)", value=1.5)
        bi = bt - bd
        st.caption(f"🧬 Bilirrubina Indirecta Calculada: **{bi:.1f}** µmol/L")

    with q_col3:
        pt = st.number_input("Proteínas Totales (g/L)", value=68.0 if es_felino else 64.0)
        alb = st.number_input("Albúmina (g/L)", value=32.0 if es_felino else 34.0)
        glob = pt - alb
        rel_ag = alb / glob if glob > 0 else 0.0
        st.caption(f"🧬 Globulinas Calc: **{glob:.1f}** g/L | Rel A/G: **{rel_ag:.2f}**")
        amilasa = st.text_input("Amilasa [U/L]", "750.0")
        lipasa = st.text_input("Lipasa [U/L]", "120.0")

    ref_qs = {
        "gluc": "3.8 - 7.9" if es_felino else "3.8 - 6.8", "urea": "4.9 - 11.9" if es_felino else "3.5 - 9.0",
        "creat": "70 - 160" if es_felino else "44 - 130", "alt": "12 - 130" if es_felino else "10 - 100",
        "ast": "0 - 48" if es_felino else "0 - 50", "fa": "14 - 111" if es_felino else "20 - 150",
        "pt": "60 - 80" if es_felino else "54 - 75", "alb": "28 - 39" if es_felino else "26 - 40",
        "glob": "26 - 51" if es_felino else "27 - 44", "ag": "0.6 - 1.2" if es_felino else "0.7 - 1.5",
        "bili": "0 - 15.0" if es_felino else "0 - 15.0", "ami": "500 - 1500" if es_felino else "300 - 1500",
        "lip": "0 - 250" if es_felino else "0 - 500",
    }

    if "QS 1" in tipo_estudio or "Paquete Renal" in tipo_estudio or "Prequirúrgico 2" in tipo_estudio:
        datos_locales['qs_items'] = [
            ("GLUCOSA", glucosa, "mmol/L", ref_qs["gluc"]), ("UREA", urea, "mmol/L", ref_qs["urea"]),
            ("CREATININA", creatinina, "µmol/L", ref_qs["creat"]), ("PROTEINAS TOTALES", f"{pt:.1f}", "g/L", ref_qs["pt"])
        ]
    elif "Hepático" in tipo_estudio or "QS 2" in tipo_estudio or "QS 3" in tipo_estudio:
        datos_locales['qs_items'] = [
            ("ALT", alt, "U/L", ref_qs["alt"]), ("AST", ast, "U/L", ref_qs["ast"]),
            ("FOSFATASA ALCALINA", fa, "U/L", ref_qs["fa"]), ("BILIRRUBINA TOTAL", f"{bt:.1f}", "µmol/L", ref_qs["bili"]),
            ("BILIRRUBINA DIRECTA", f"{bd:.1f}", "µmol/L", "-"), ("BILIRRUBINA INDIRECTA", f"{bi:.1f}", "µmol/L", "-"),
            ("PROTEINAS TOTALES", f"{pt:.1f}", "g/L", ref_qs["pt"]), ("ALBUMINA", f"{alb:.1f}", "g/L", ref_qs["alb"]),
            ("GLOBULINAS", f"{glob:.1f}", "g/L", ref_qs["glob"]), ("RELACION A/G", f"{rel_ag:.2f}", "-", ref_qs["ag"])
        ]
    else: 
        datos_locales['qs_items'] = [
            ("GLUCOSA", glucosa, "mmol/L", ref_qs["gluc"]), ("UREA", urea, "mmol/L", ref_qs["urea"]),
            ("CREATININA", creatinina, "µmol/L", ref_qs["creat"]), ("ALT", alt, "U/L", ref_qs["alt"]),
            ("FOSFATASA ALCALINA", fa, "U/L", ref_qs["fa"]), ("BILIRRUBINA TOTAL", f"{bt:.1f}", "µmol/L", ref_qs["bili"]),
            ("PROTEINAS TOTALES", f"{pt:.1f}", "g/L", ref_qs["pt"]), ("ALBUMINA", f"{alb:.1f}", "g/L", ref_qs["alb"]),
            ("GLOBULINAS", f"{glob:.1f}", "g/L", ref_qs["glob"])
        ]
    return datos_locales

def modulo_serologia(tipo_estudio):
    st.markdown('<div class="card-sero"><b>🩸 PRUEBAS RÁPIDAS Y SEROLOGÍA</b></div>', unsafe_allow_html=True)
    prueba_nom = st.text_input("Nombre de la Prueba", tipo_estudio)
    resultado = st.selectbox("Resultado", ["NEGATIVO", "POSITIVO", "DUDOSO / REPETIR"])
    return {'sero_items': [(prueba_nom, resultado)]}

def modulo_endocrino(es_felino):
    st.markdown('<div class="card-endo"><b>⚕️ ENDOCRINOLOGÍA</b></div>', unsafe_allow_html=True)
    t4 = st.text_input("T4 Total (nmol/L)", "20.5")
    tsh = st.text_input("TSH (ng/mL)", "0.15")
    return {'endo_items': [
        ("T4 TOTAL", t4, "nmol/L", "10.0 - 60.0" if es_felino else "15.0 - 50.0"),
        ("TSH", tsh, "ng/mL", "< 0.3" if es_felino else "< 0.6")
    ]}

def modulo_citologia():
    st.markdown('<div class="card-cito"><b>🔬 CITOLOGÍA Y MICROSCOPÍA</b></div>', unsafe_allow_html=True)
    sitio = st.text_input("Sitio Anatómico / Origen de Muestra", "Piel (Dorso)")
    hallazgo = st.text_area("Descripción Microscópica", "Abundantes queratinocitos. Ausencia de ácaros.")
    return {'cito_items': [("ORIGEN", sitio), ("DESCRIPCIÓN", hallazgo)]}

def modulo_urianalisis(es_felino):
    st.markdown('<div class="card-uri"><b>📋 URIANÁLISIS COMPLETO</b></div>', unsafe_allow_html=True)
    u1, u2 = st.columns(2)
    with u1:
        ph = st.text_input("pH Urinario", "6.5" if es_felino else "6.0")
        ge = st.text_input("Gravedad Específica", "1.040" if es_felino else "1.030")
        aspecto = st.text_input("Aspecto / Color", "CLARO / AMARILLO PALIDO")
    with u2:
        hb_u = st.text_input("Sangre Oculta", "NEGATIVO")
        prot_u = st.text_input("Proteína Urinaria", "NEGATIVO")
        sed = st.text_input("Sedimento Urinario", "SIN HALLAZGOS PATOLÓGICOS")
    return {'uri_items': [
        ("pH URINARIO", ph, "-", "6.0 - 7.5"), ("GRAVEDAD ESPECÍFICA", ge, "-", "> 1.035" if es_felino else "> 1.030"),
        ("ASPECTO Y COLOR", aspecto, "-", "Claro / Amarillo pálido"), ("SANGRE OCULTA", hb_u, "-", "Negativo"),
        ("PROTEÍNA", prot_u, "-", "Negativo / Trazas"), ("SEDIMENTO", sed, "-", "Normal")
    ]}

def modulo_copro():
    st.markdown('<div class="card-cop"><b>💩 EXAMEN COPROLÓGICO</b></div>', unsafe_allow_html=True)
    cp1, cp2 = st.columns(2)
    with cp1:
        consistencia = st.selectbox("Consistencia", ["FORMADA", "BLANDA", "PASTOSA", "LÍQUIDA/DIARREICA"])
        moco = st.selectbox("Moco o Sangre", ["AUSENTE", "MOCO PRESENTE", "SANGRE FRESCA PRESENTE"])
    with cp2:
        hallazgos = st.text_area("Examen Microscópico Directo", "NO SE OBSERVARON FORMAS PARASITARIAS.")
        flotacion = st.text_input("Técnica de Flotación", "NEGATIVO A PROTOZOARIOS Y HELMINTOS")
    return {'copro_items': [("CONSISTENCIA", consistencia), ("MOCO / SANGRE", moco), ("MICROSCOPÍA", hallazgos), ("FLOTACIÓN", flotacion)]}
