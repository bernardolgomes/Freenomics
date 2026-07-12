import streamlit as st
from translations import LINGUAS, NOMES_PAGINAS

st.set_page_config(page_title="Freenomics", layout="wide", page_icon="📊")

# Injectar tagline no topo da sidebar via CSS
st.markdown("""
<style>
[data-testid="stSidebarContent"]::before {
    content: "MONEY · MINDSET · FREEDOM";
    display: block;
    text-align: center;
    color: #C29A4B;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 2.5px;
    padding: 14px 0 12px 0;
    border-bottom: 1px solid #C29A4B;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
}
</style>
""", unsafe_allow_html=True)

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

PATRIMONIO = {
    "🇵🇹 Português": "💎 Património",
    "🇬🇧 English":   "💎 Net Worth",
    "🇫🇷 Français":  "💎 Patrimoine",
    "🇩🇪 Deutsch":   "💎 Vermögen",
    "🇪🇸 Español":   "💎 Patrimonio",
}

pg = st.navigation([
    st.Page("pages/0_Dashboard.py",    title=n["dashboard"]),
    st.Page("pages/1_Comparador.py",   title=n["comparador"]),
    st.Page("pages/2_Simulador.py",    title=n["simulador"]),
    st.Page("pages/3_Dividendos.py",   title=n["dividendos"]),
    st.Page("pages/4_Risco.py",        title=n["risco"]),
    st.Page("pages/5_Noticias.py",     title=n["noticias"]),
    st.Page("pages/7_patrimonio.py",   title=PATRIMONIO[lang]),
    st.Page("pages/6_Exportar.py",     title=EXPORTAR[lang]),
])
pg.run()
