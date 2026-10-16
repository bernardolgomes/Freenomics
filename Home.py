import streamlit as st
from translations import LINGUAS, NOMES_PAGINAS
import auth

st.set_page_config(page_title="Freenomics", layout="wide", page_icon="📊")

# O modo demonstração pré-preenche widgets via session_state: evita o aviso amarelo de "valor duplicado"
# (também definido em .streamlit/config.toml; isto cobre execuções sem esse ficheiro).
try:
    from streamlit import config as _st_config
    _st_config.set_option("global.disableWidgetStateDuplicationWarning", True)
except Exception:
    pass

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
/* Dropdown do idioma: garantir espaço suficiente para abrir sem cortar. */
[data-baseweb="popover"] {
    max-height: 70vh !important;
}
[data-baseweb="menu"],
ul[role="listbox"] {
    max-height: 65vh !important;
    overflow-y: auto !important;
    -webkit-overflow-scrolling: touch !important;
}
</style>
""", unsafe_allow_html=True)

if "lang" not in st.session_state:
    st.session_state["lang"] = "🇵🇹 Português"

st.sidebar.markdown("### 🌐 Language")
lang = st.sidebar.selectbox(
    "", LINGUAS,
    index=LINGUAS.index(st.session_state["lang"]),
    label_visibility="collapsed",
    key="lang_selector"
)
st.session_state["lang"] = lang

auth.refresh_plan()
auth.render_login_widget_top_right()

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

ANALISE_ACAO = {
    "🇵🇹 Português": "🔎 Análise de Ação",
    "🇬🇧 English":   "🔎 Stock Analysis",
    "🇫🇷 Français":  "🔎 Analyse d'Action",
    "🇩🇪 Deutsch":   "🔎 Aktienanalyse",
    "🇪🇸 Español":   "🔎 Análisis de Acción",
}

CARTEIRA = {
    "🇵🇹 Português": "📈 Carteira",
    "🇬🇧 English":   "📈 Portfolio",
    "🇫🇷 Français":  "📈 Portefeuille",
    "🇩🇪 Deutsch":   "📈 Portfolio",
    "🇪🇸 Español":   "📈 Cartera",
}

SIMULAR = {
    "🇵🇹 Português": "🧪 Simular e Comparar",
    "🇬🇧 English":   "🧪 Simulate & Compare",
    "🇫🇷 Français":  "🧪 Simuler et Comparer",
    "🇩🇪 Deutsch":   "🧪 Simulieren & Vergleichen",
    "🇪🇸 Español":   "🧪 Simular y Comparar",
}

LEGAL = {
    "🇵🇹 Português": "📜 Termos e Privacidade",
    "🇬🇧 English":   "📜 Terms & Privacy",
    "🇫🇷 Français":  "📜 Conditions et Confidentialité",
    "🇩🇪 Deutsch":   "📜 AGB & Datenschutz",
    "🇪🇸 Español":   "📜 Términos y Privacidad",
}

SECOES = {
    "🇵🇹 Português": ["Começar", "As minhas finanças", "Investir", "Mercado e Relatório"],
    "🇬🇧 English":   ["Start", "My finances", "Invest", "Market & Report"],
    "🇫🇷 Français":  ["Démarrer", "Mes finances", "Investir", "Marché et Rapport"],
    "🇩🇪 Deutsch":   ["Start", "Meine Finanzen", "Investieren", "Markt & Bericht"],
    "🇪🇸 Español":   ["Empezar", "Mis finanzas", "Invertir", "Mercado e Informe"],
}[lang]

PAGINAS = {
    "boasvindas": st.Page("pages/11_BoasVindas.py", title=n["boasvindas"], default=True),
    "precos":     st.Page("pages/10_Precos.py", title=n["precos"]),
    "orcamento":  st.Page("pages/8_Orcamento.py", title=n["orcamento"]),
    "objetivos":  st.Page("pages/9_Objetivos.py", title=n["objetivos"]),
    "patrimonio": st.Page("pages/7_patrimonio.py", title=PATRIMONIO[lang]),
    "analise":    st.Page("pages/12_Analise_Acao.py", title=ANALISE_ACAO[lang]),
    "carteira":   st.Page("pages/13_Carteira.py", title=CARTEIRA[lang]),
    "simular":    st.Page("pages/14_Simular_Comparar.py", title=SIMULAR[lang]),
    "noticias":   st.Page("pages/5_Noticias.py", title=n["noticias"]),
    "exportar":   st.Page("pages/6_Exportar.py", title=EXPORTAR[lang]),
    "legal":      st.Page("pages/15_Legal.py", title=LEGAL[lang]),
}
# Disponível para st.page_link nas outras páginas (ex.: botão "Próximo passo")
st.session_state["_paginas"] = PAGINAS

P = PAGINAS
pg = st.navigation({
    SECOES[0]: [P["boasvindas"], P["precos"]],
    SECOES[1]: [P["orcamento"], P["objetivos"], P["patrimonio"]],
    SECOES[2]: [P["analise"], P["carteira"], P["simular"]],
    SECOES[3]: [P["noticias"], P["exportar"], P["legal"]],
})
pg.run()
