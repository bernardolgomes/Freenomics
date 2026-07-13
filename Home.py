import streamlit as st
from translations import LINGUAS, NOMES_PAGINAS

st.set_page_config(page_title="Freenomics", layout="wide", page_icon="📊")

import streamlit.components.v1 as components
components.html("""
<script>
function fixDropdowns() {
    try {
        var doc = window.parent.document;
        // Opções da lista
        doc.querySelectorAll('li[role="option"]').forEach(function(el) {
            el.style.setProperty('color', '#FFFFFF', 'important');
            el.style.setProperty('background-color', '#1A2F4A', 'important');
        });
        // Container popup
        doc.querySelectorAll('[data-baseweb="popover"], [data-baseweb="menu"], ul[role="listbox"]').forEach(function(el) {
            el.style.setProperty('background-color', '#1A2F4A', 'important');
        });
        // Texto dentro de cada opção
        doc.querySelectorAll('[data-baseweb="option"]').forEach(function(el) {
            el.style.setProperty('color', '#FFFFFF', 'important');
            el.style.setProperty('background-color', '#1A2F4A', 'important');
            el.querySelectorAll('*').forEach(function(child) {
                child.style.setProperty('color', '#FFFFFF', 'important');
            });
        });
    } catch(e) {}
}
// Observer para apanhar dropdowns que abrem dinamicamente
try {
    var observer = new MutationObserver(fixDropdowns);
    observer.observe(window.parent.document.body, { childList: true, subtree: true });
} catch(e) {}
// Correr também periodicamente como fallback
setInterval(fixDropdowns, 200);
</script>
""", height=0)

st.markdown("""
<style>
[data-testid="stSidebarNav"]::before {
    content: "MONEY · MINDSET · FREEDOM";
    display: block;
    text-align: center;
    color: #FFFFFF;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    padding: 14px 0 12px 0;
    border-bottom: 1px solid #C29A4B;
    margin-bottom: 16px;
    font-family: 'Inter', sans-serif;
}
/* Linha dourada no separador da sidebar */
[data-testid="stSidebarContent"] hr {
    border-color: #C29A4B !important;
    opacity: 1 !important;
}
</style>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state["lang"] = "🇵🇹 Português"

st.sidebar.markdown("### 🌐 Language / Língua")
lang = st.sidebar.radio(
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
    st.Page("pages/8_Orcamento.py",    title=n["orcamento"]),
    st.Page("pages/9_Objetivos.py",    title=n["objetivos"]),
    st.Page("pages/6_Exportar.py",     title=EXPORTAR[lang]),
])
pg.run()
