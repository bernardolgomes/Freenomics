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
    "🇵🇹 Português": "🧪 Simular e Comparar",
    "🇬🇧 English":   "🧪 Simulate & Compare",
    "🇫🇷 Français":  "🧪 Simuler et Comparer",
    "🇩🇪 Deutsch":   "🧪 Simulieren & Vergleichen",
    "🇪🇸 Español":   "🧪 Simular y Comparar",
}

# Logo, CSS e título uma só vez; os separadores reutilizam as páginas antigas
page_chrome(TITULO.get(lang, TITULO["🇬🇧 English"]))
demo_bar("simular")

_PAGES = os.path.join(_ROOT, "pages")
tab_sim, tab_comp = st.tabs([n["simulador"], n["comparador"]])

with tab_sim:
    run_page(os.path.join(_PAGES, "2_Simulador.py"))
with tab_comp:
    run_page(os.path.join(_PAGES, "1_Comparador.py"))
