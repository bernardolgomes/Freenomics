import streamlit as st
from translations import LINGUAS, NOMES_PAGINAS

st.set_page_config(page_title="Freenomics", layout="wide", page_icon="📊")

if "lang" not in st.session_state:
    st.session_state["lang"] = "🇵🇹 Português"

st.sidebar.markdown("### 🌐 Language / Língua")
lang = st.sidebar.selectbox(
    "", LINGUAS,
    index=LINGUAS.index(st.session_state["lang"]),
    label_visibility="collapsed",
    key="lang_selector"
)
st.session_state["lang"] = lang

n = NOMES_PAGINAS[lang]

EXPORTAR = {
    "🇵🇹 Português": "📄 Exportar Relatório",
    "🇬🇧 English":   "📄 Export Report",
    "🇫🇷 Français":  "📄 Exporter Rapport",
    "🇩🇪 Deutsch":   "📄 Bericht exportieren",
    "🇪🇸 Español":   "📄 Exportar Informe",
}

pg = st.navigation([
    st.Page("pages/0_Dashboard.py",  title=n["dashboard"]),
    st.Page("pages/1_Comparador.py", title=n["comparador"]),
    st.Page("pages/2_Simulador.py",  title=n["simulador"]),
    st.Page("pages/3_Dividendos.py", title=n["dividendos"]),
    st.Page("pages/4_Risco.py",      title=n["risco"]),
    st.Page("pages/5_Noticias.py",   title=n["noticias"]),
    st.Page("pages/6_Exportar.py", title=EXPORTAR[lang]),
])
pg.run()
