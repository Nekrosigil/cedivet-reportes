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
            vsg = st.number_input("V.S.G. (mm/h)", value=0.0, step=1.0)
            
            vgm = (hto * 10) / eritrocitos if eritrocitos > 0 else 0.0
            hgm = (hb * 10) / eritrocitos if eritrocitos > 0 else 0.0
            chgm = (hb * 100) / hto if hto > 0 else 0.0
            
            st.info(f"📊 **ÍNDICES:** VGM: {vgm:.1f} fL | HGM: {hgm:.1f} pg | CHGM: {chgm:.1f} g/dL")
            
            obs_roja = st.text_input("Observaciones Fórmula Roja (ej. Anisocitosis, Acantocitos)", "SIN ALTERACIONES MORFOLÓGICAS")
            
            ref_roja = {
                "hto": "24.0 - 45.0" if es_felino else "33.0 - 55.0",
                "hb": "8.0 - 15.0" if es_felino else "12.0 - 19.5",
                "eri": "5.00 - 10.00" if es_felino else "5.50 - 8.50",
                "vgm": "39.0 - 55.0" if es_felino else "60.0 - 77.0",
                "hgm": "12.5 - 17.5" if es_felino else "19.5 - 24.0",
                "chgm": "30.0 - 36.0" if es_felino else "32.0 - 36.0",
                "vsg": "0 - 10" if es_felino else "0 - 13"
            }

            datos_locales['hem_roja'] = [
                ("HEMATOCRITO", f"{hto:.1f}", "%", ref_roja["hto"]),
                ("HEMOGLOBINA", f"{hb:.1f}", "g/dL", ref_roja["hb"]),
                ("ERITROCITOS", f"{eritrocitos:.2f}", "x10^6/µL", ref_roja["eri"]),
                ("VGM", f"{vgm:.1f}", "fL", ref_roja["vgm"]),
                ("HGM", f"{hgm:.1f}", "pg", ref_roja["hgm"]),
                ("CHGM", f"{chgm:.1f}", "g/dL", ref_roja["chgm"]),
                ("V.S.G.", f"{vsg:.0f}", "mm/h", ref_roja["vsg"])
            ]
            datos_locales['obs_formula_roja'] = obs_roja

    if necesita_blanca:
        with h_col2:
            st.caption("⚪ **Fórmula Blanca & Diferencial Automatizado**")
            leucocitos = st.number_input("Leucocitos Totales (x10^3/µL)", value=12.5 if es_felino else 10.5, step=0.1)
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                pct_mielocitos = st.number_input("% Mielocitos", value=0.0, step=0.5)
                pct_juveniles = st.number_input("% Juveniles", value=0.0, step=0.5)
                pct_bandas = st.number_input("% Bandas", value=0.0, step=0.5)
                pct_seg = st.number_input("% Segmentados", value=55.0 if es_felino else 70.0, step=0.5)
            with col_p2:
                pct_linf = st.number_input("% Linfocitos", value=30.0 if es_felino else 20.0, step=0.5)
                pct_mono = st.number_input("% Monocitos", value=5.0, step=0.5)
                pct_eos = st.number_input("% Eosinófilos", value=8.0 if es_felino else 4.0, step=0.5)
                pct_baso = st.number_input("% Basófilos", value=2.0 if es_felino else 1.0, step=0.5)

            leu_abs_total = leucocitos * 1000.0
            plaquetas = st.number_input("Plaquetas (x10^3/µL)", value=350.0, step=10.0)
            reticulocitos = st.number_input("Reticulocitos (%)", value=0.1, step=0.05)
            
            obs_blanca = st.text_input("Interpretación / Diagnóstico Hematológico", "DENTRO DE PARÁMETROS NORMALES")

            ref_blanca = {
                "leu": "5.5 - 19.5" if es_felino else "6.0 - 15.0",
                "mielo": "0",
                "juv": "0",
                "bandas": "0 - 300" if es_felino else "0 - 500",
                "seg": "2500 - 12500" if es_felino else "3000 - 11000",
                "linf": "1500 - 7000" if es_felino else "1000 - 4800",
                "mono": "0 - 850" if es_felino else "150 - 1350",
                "eos": "100 - 1500" if es_felino else "100 - 1250",
                "baso": "0",
                "plaq": "300 - 800" if es_felino else "200 - 400",
                "reti": "0 - 0.15"
            }

            datos_locales['hem_blanca'] = [
                ("LEUCOCITOS TOTALES", f"{leucocitos:.1f}", "x10^3/µL", ref_blanca["leu"]),
                ("MIELOCITOS", f"{int((pct_mielocitos/100)*leu_abs_total)} ({pct_mielocitos}%)", "/µL", ref_blanca["mielo"]),
                ("JUVENILES", f"{int((pct_juveniles/100)*leu_abs_total)} ({pct_juveniles}%)", "/µL", ref_blanca["juv"]),
                ("BANDAS", f"{int((pct_bandas/100)*leu_abs_total)} ({pct_bandas}%)", "/µL", ref_blanca["bandas"]),
                ("SEGMENTADOS", f"{int((pct_seg/100)*leu_abs_total)} ({pct_seg}%)", "/µL", ref_blanca["seg"]),
                ("LINFOCITOS", f"{int((pct_linf/100)*leu_abs_total)} ({pct_linf}%)", "/µL", ref_blanca["linf"]),
                ("MONOCITOS", f"{int((pct_mono/100)*leu_abs_total)} ({pct_mono}%)", "/µL", ref_blanca["mono"]),
                ("EOSINÓFILOS", f"{int((pct_eos/100)*leu_abs_total)} ({pct_eos}%)", "/µL", ref_blanca["eos"]),
                ("BASÓFILOS", f"{int((pct_baso/100)*leu_abs_total)} ({pct_baso}%)", "/µL", ref_blanca["baso"]),
                ("PLAQUETAS", f"{plaquetas:.0f}", "x10^3/µL", ref_blanca["plaq"]),
                ("RETICULOCITOS", f"{reticulocitos:.2f}", "%", ref_blanca["reti"])
            ]
            datos_locales['obs_formula_blanca'] = obs_blanca

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
        ck = st.text_input("Creatina Cinasa (CK) [U/L]", "213.0")
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
        "gluc": "3.8 - 7.9" if es_felino else "3.3 - 6.8", "urea": "4.9 - 11.9" if es_felino else "2.1 - 7.91",
        "creat": "70 - 160" if es_felino else "60 - 126", "alt": "12 - 130" if es_felino else "4.0 - 70.0",
        "ast": "0 - 48" if es_felino else "12.0 - 55.0", "fa": "14 - 111" if es_felino else "6.0 - 189.0",
        "ck": "17 - 213", "pt": "60 - 80" if es_felino else "56 - 75", "alb": "28 - 39" if es_felino else "29 - 40",
        "glob": "26 - 51" if es_felino else "24 - 39", "ag": "0.6 - 1.2" if es_felino else "0.7 - 1.0",
        "bili": "0 - 15.0" if es_felino else "0.2 - 0.5", "ami": "500 - 1500" if es_felino else "300 - 1500",
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
            ("FOSFATASA ALCALINA", fa, "U/L", ref_qs["fa"]), ("CK", ck, "U/L", ref_qs["ck"]),
            ("BILIRRUBINA TOTAL", f"{bt:.1f}", "µmol/L", ref_qs["bili"]),
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
    datos_locales = {}
    
    st.markdown('<div class="card-uri"><b>📋 URIANÁLISIS COMPLETO (EVALUACIÓN INTEGRAL)</b></div>', unsafe_allow_html=True)
    
    # Referencias dinámicas según especie
    ref_uri = {
        "ge": "> 1.035" if es_felino else "> 1.030",
        "ph": "6.0 - 7.0" if es_felino else "6.0 - 7.5",
        "prot": "Negativo" if es_felino else "Negativo / Trazas",
        "bili": "Negativo (Siempre patológico)" if es_felino else "Negativo / Trazas (+ en machos)",
        "hb": "Negativo",
        "glu": "Negativo",
        "cetonas": "Negativo"
    }

    u_col1, u_col2, u_col3 = st.columns(3)
    
    with u_col1:
        st.caption("🧪 **EXAMEN FÍSICO**")
        volumen = st.text_input("Volumen (mL)", "3.0")
        color = st.text_input("Color", "AMARILLO PALIDO" if es_felino else "OCRE")
        aspecto = st.text_input("Aspecto", "CLARO" if es_felino else "TURBIO")
        sedimento = st.text_input("Sedimento", "ESCASO" if es_felino else "ABUNDANTE")
        ph = st.text_input("pH Urinario", "6.0" if es_felino else "6.5")
        ge = st.text_input("Gravedad Específica", "1.040" if es_felino else "1.015")

    with u_col2:
        st.caption("🔬 **EXAMEN QUÍMICO**")
        hb_u = st.selectbox("Sangre Oculta / Hemoglobina", ["NEGATIVO", "POSITIVO +", "POSITIVO ++", "POSITIVO +++"])
        prot_u = st.text_input("Proteína Urinaria (g/L)", "NEGATIVO" if es_felino else "2 g/L")
        glu_u = st.selectbox("Glucosa Urinaria", ["NEGATIVO", "POSITIVO +", "POSITIVO ++", "POSITIVO +++"])
        cetonas = st.selectbox("Cuerpos Cetónicos", ["NEGATIVO", "POSITIVO +", "POSITIVO ++", "POSITIVO +++"])
        urobilinogeno = st.selectbox("Urobilinógeno", ["NEGATIVO", "POSITIVO +", "POSITIVO ++"])
        bilirrubina_u = st.selectbox("Bilirrubina Urinaria", ["NEGATIVO", "POSITIVO +", "POSITIVO ++", "POSITIVO +++"])

    with u_col3:
        st.caption("🔬 **EXAMEN MICROSCÓPICO (SEDIMENTO)**")
        c_vesicales = st.text_input("Células Vesicales", "1-2 POR CAMPO")
        c_transicionales = st.text_input("Células Transicionales", "NO SE OBSERVAN")
        c_renales = st.text_input("Células Renales", "NO SE OBSERVAN")
        eritrocitos_u = st.text_input("Glóbulos Rojos", "0-2 POR CAMPO")
        leucocitos_u = st.text_input("Leucocitos", "10-15 POR CAMPO")
        
        crist_oxalato = st.text_input("Oxalato de Calcio", "NO SE OBSERVAN")
        crist_fosfatos_t = st.text_input("Fosfatos Triples", "NO SE OBSERVAN")
        uratos_amorfos = st.text_input("Uratos Amorfos", "NO SE OBSERVAN")
        bacterias_u = st.text_input("Bacterias", "NO SE OBSERVAN")
        piocitos = st.text_input("Piocitos", "NO SE OBSERVAN")
        cilindros = st.text_input("Cilindros (Hialinos/Granulosos)", "NO SE OBSERVAN")
        mucina_u = st.text_input("Mucina", "ESCASA")

    st.markdown("---")
    diag_uri = st.text_input("Diagnóstico Urinario / Observaciones", "SIN HALLAZGOS PATOLÓGICOS" if es_felino else "CISTITIS SEVERA, CRISTALURIA, PROTEINURIA SEVERA")

    # 1. EXAMEN FÍSICO
    datos_locales['uri_fisico'] = [
        ("VOLUMEN", volumen, "mL", "-"),
        ("COLOR", color, "-", "Amarillo pálido / Claro"),
        ("ASPECTO", aspecto, "-", "Claro / Transparente"),
        ("SEDIMENTO", sedimento, "-", "Escaso"),
        ("pH URINARIO", ph, "-", ref_uri["ph"]),
        ("GRAVEDAD ESPECÍFICA", ge, "-", ref_uri["ge"])
    ]
    
    # 2. EXAMEN QUÍMICO
    datos_locales['uri_quimico'] = [
        ("HEMOGLOBINA / SANGRE", hb_u, "-", ref_uri["hb"]),
        ("PROTEÍNA URINARIA", prot_u, "-", ref_uri["prot"]),
        ("GLUCOSA", glu_u, "-", ref_uri["glu"]),
        ("CUERPOS CETÓNICOS", cetonas, "-", ref_uri["cetonas"]),
        ("UROBILINÓGENO", urobilinogeno, "-", "Negativo"),
        ("BILIRRUBINA", bilirrubina_u, "-", ref_uri["bili"])
    ]
    
    # 3. EXAMEN MICROSCÓPICO (SEDIMENTO)
    datos_locales['uri_micro'] = [
        ("CÉLULAS VESICALES", c_vesicales, "por campo", "Escasas (0 - 2)"),
        ("CÉLULAS TRANSICIONALES", c_transicionales, "por campo", "Ausentes / Escasas"),
        ("CÉLULAS RENALES", c_renales, "por campo", "Ausentes"),
        ("GLÓBULOS ROJOS", eritrocitos_u, "por campo", "0 - 2 por campo"),
        ("LEUCOCITOS", leucocitos_u, "por campo", "0 - 5 por campo"),
        ("OXALATO DE CALCIO", crist_oxalato, "-", "Ausentes"),
        ("FOSFATOS TRIPLES", crist_fosfatos_t, "-", "Ausentes"),
        ("URATOS AMORFOS", uratos_amorfos, "-", "Ausentes"),
        ("BACTERIAS", bacterias_u, "-", "Ausentes"),
        ("PIOCITOS", piocitos, "-", "Ausentes"),
        ("CILINDROS", cilindros, "-", "Ausentes"),
        ("MUCINA", mucina_u, "-", "Escasa")
    ]
    
    datos_locales['obs_urianalisis'] = diag_uri

    return datos_locales

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
