import os
import sys
import streamlit as st

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from utils import page_chrome, run_page, demo_bar
from translations import NOMES_PAGINAS

lang = st.session_state.get("lang", "🇵🇹 Português")
n = NOMES_PAGINAS.get(lang, NOMES_PAGINAS["🇬🇧 English"])

TITULO = {
    "🇵🇹 Português": "📈 Carteira",
    "🇬🇧 English":   "📈 Portfolio",
    "🇫🇷 Français":  "📈 Portefeuille",
    "🇩🇪 Deutsch":   "📈 Portfolio",
    "🇪🇸 Español":   "📈 Cartera",
}

# Logo, CSS e título uma só vez; os separadores reutilizam as páginas antigas
page_chrome(TITULO.get(lang, TITULO["🇬🇧 English"]))
demo_bar("carteira")

_PAGES = os.path.join(_ROOT, "pages")
tab_analise, tab_risco, tab_div = st.tabs([n["dashboard"], n["risco"], n["dividendos"]])

with tab_analise:
    run_page(os.path.join(_PAGES, "0_Dashboard.py"))
with tab_risco:
    run_page(os.path.join(_PAGES, "4_Risco.py"))
with tab_div:
    run_page(os.path.join(_PAGES, "3_Dividendos.py"))
