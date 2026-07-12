import streamlit as st
import yfinance as yf
import requests
import xml.etree.ElementTree as ET
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Notícias",
        "subtitulo": "Notícias de mercado actualizadas — ações, cripto e imobiliário.",
        "tipo_label": "Tipo de notícias",
        "tipo_acoes": "📈 Ações & ETFs",
        "tipo_cripto": "₿ Cripto",
        "tipo_imob": "🏠 Mercado Imobiliário",
        "tickers_label": "Tickers (separados por vírgula)",
        "max_label": "Notícias por ticker",
        "pais_label": "País / Região",
        "btn_ver": "📰 Ver notícias",
        "a_carregar": "A carregar notícias...",
        "sem_noticias": "Não foram encontradas notícias. Tenta outros tickers ou volta mais tarde.",
        "filtro_label": "Filtrar por",
        "todos": "Todos",
        "encontradas": "notícias encontradas",
        "ler": "Ler artigo completo ↗",
        "aviso_ticker": "Não foi possível carregar notícias para",
        "aviso": "⚠️ Conteúdo de terceiros — Freenomics não é responsável pelo conteúdo dos artigos.",
        "rodape": "Freenomics · Notícias via Yahoo Finance e Google News",
        "paises": {
            "🇵🇹 Portugal": "mercado imobiliário Portugal",
            "🇧🇷 Brasil": "mercado imobiliário Brasil",
            "🇬🇧 Reino Unido": "UK real estate market",
            "🇩🇪 Alemanha": "Immobilienmarkt Deutschland",
            "🇫🇷 França": "marché immobilier France",
            "🇺🇸 EUA": "US real estate market",
            "🇪🇸 Espanha": "mercado inmobiliario España",
        },
        "imob_reits": "ETFs Imobiliários (REIT)",
        "imob_reits_hint": "Adiciona também notícias de REITs como VNQ (EUA), IUKP.L (UK)",
    },
    "🇬🇧 English": {
        "titulo": "News",
        "subtitulo": "Up-to-date market news — stocks, crypto and real estate.",
        "tipo_label": "News type",
        "tipo_acoes": "📈 Stocks & ETFs",
        "tipo_cripto": "₿ Crypto",
        "tipo_imob": "🏠 Real Estate",
        "tickers_label": "Tickers (comma-separated)",
        "max_label": "News per ticker",
        "pais_label": "Country / Region",
        "btn_ver": "📰 View news",
        "a_carregar": "Loading news...",
        "sem_noticias": "No news found. Try other tickers or come back later.",
        "filtro_label": "Filter by",
        "todos": "All",
        "encontradas": "news found",
        "ler": "Read full article ↗",
        "aviso_ticker": "Could not load news for",
        "aviso": "⚠️ Third-party content — Freenomics is not responsible for article content.",
        "rodape": "Freenomics · News via Yahoo Finance and Google News",
        "paises": {
            "🇺🇸 USA": "US real estate market",
            "🇬🇧 UK": "UK real estate market",
            "🇵🇹 Portugal": "mercado imobiliário Portugal",
            "🇩🇪 Germany": "Immobilienmarkt Deutschland",
            "🇫🇷 France": "marché immobilier France",
            "🇧🇷 Brazil": "mercado imobiliário Brasil",
            "🇪🇸 Spain": "mercado inmobiliario España",
        },
        "imob_reits": "Real Estate ETFs (REITs)",
        "imob_reits_hint": "Also add REIT news: VNQ (USA), IUKP.L (UK), EGL.L (Europe)",
    },
    "🇫🇷 Français": {
        "titulo": "Actualités",
        "subtitulo": "Actualités de marché en temps réel — actions, crypto et immobilier.",
        "tipo_label": "Type d'actualités",
        "tipo_acoes": "📈 Actions & ETFs",
        "tipo_cripto": "₿ Crypto",
        "tipo_imob": "🏠 Marché Immobilier",
        "tickers_label": "Tickers (séparés par virgule)",
        "max_label": "Actualités par ticker",
        "pais_label": "Pays / Région",
        "btn_ver": "📰 Voir les actualités",
        "a_carregar": "Chargement des actualités...",
        "sem_noticias": "Aucune actualité trouvée.",
        "filtro_label": "Filtrer par",
        "todos": "Tous",
        "encontradas": "actualités trouvées",
        "ler": "Lire l'article complet ↗",
        "aviso_ticker": "Impossible de charger les actualités pour",
        "aviso": "⚠️ Contenu tiers — Freenomics n'est pas responsable du contenu des articles.",
        "rodape": "Freenomics · Actualités via Yahoo Finance et Google News",
        "paises": {
            "🇫🇷 France": "marché immobilier France",
            "🇩🇪 Allemagne": "Immobilienmarkt Deutschland",
            "🇵🇹 Portugal": "mercado imobiliário Portugal",
            "🇬🇧 Royaume-Uni": "UK real estate market",
            "🇺🇸 États-Unis": "US real estate market",
            "🇪🇸 Espagne": "mercado inmobiliario España",
        },
        "imob_reits": "ETFs Immobiliers (REITs)",
        "imob_reits_hint": "Ajoutez aussi: VNQ (USA), IUKP.L (UK)",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Nachrichten",
        "subtitulo": "Aktuelle Marktnachrichten — Aktien, Krypto und Immobilien.",
        "tipo_label": "Nachrichtentyp",
        "tipo_acoes": "📈 Aktien & ETFs",
        "tipo_cripto": "₿ Krypto",
        "tipo_imob": "🏠 Immobilienmarkt",
        "tickers_label": "Ticker (kommagetrennt)",
        "max_label": "Nachrichten pro Ticker",
        "pais_label": "Land / Region",
        "btn_ver": "📰 Nachrichten anzeigen",
        "a_carregar": "Nachrichten werden geladen...",
        "sem_noticias": "Keine Nachrichten gefunden.",
        "filtro_label": "Filtern nach",
        "todos": "Alle",
        "encontradas": "Nachrichten gefunden",
        "ler": "Vollständigen Artikel lesen ↗",
        "aviso_ticker": "Nachrichten konnten nicht geladen werden für",
        "aviso": "⚠️ Inhalte Dritter — Freenomics ist nicht für den Artikelinhalt verantwortlich.",
        "rodape": "Freenomics · Nachrichten via Yahoo Finance und Google News",
        "paises": {
            "🇩🇪 Deutschland": "Immobilienmarkt Deutschland",
            "🇦🇹 Österreich": "Immobilienmarkt Österreich",
            "🇵🇹 Portugal": "mercado imobiliário Portugal",
            "🇬🇧 UK": "UK real estate market",
            "🇺🇸 USA": "US real estate market",
            "🇫🇷 Frankreich": "marché immobilier France",
        },
        "imob_reits": "Immobilien-ETFs (REITs)",
        "imob_reits_hint": "Fügen Sie auch hinzu: VNQ (USA), IUKP.L (UK)",
    },
    "🇪🇸 Español": {
        "titulo": "Noticias",
        "subtitulo": "Noticias de mercado actualizadas — acciones, cripto e inmobiliario.",
        "tipo_label": "Tipo de noticias",
        "tipo_acoes": "📈 Acciones & ETFs",
        "tipo_cripto": "₿ Cripto",
        "tipo_imob": "🏠 Mercado Inmobiliario",
        "tickers_label": "Tickers (separados por coma)",
        "max_label": "Noticias por ticker",
        "pais_label": "País / Región",
        "btn_ver": "📰 Ver noticias",
        "a_carregar": "Cargando noticias...",
        "sem_noticias": "No se encontraron noticias.",
        "filtro_label": "Filtrar por",
        "todos": "Todos",
        "encontradas": "noticias encontradas",
        "ler": "Leer artículo completo ↗",
        "aviso_ticker": "No se pudieron cargar noticias para",
        "aviso": "⚠️ Contenido de terceros — Freenomics no es responsable del contenido.",
        "rodape": "Freenomics · Noticias via Yahoo Finance y Google News",
        "paises": {
            "🇪🇸 España": "mercado inmobiliario España",
            "🇵🇹 Portugal": "mercado imobiliário Portugal",
            "🇺🇸 EE.UU.": "US real estate market",
            "🇬🇧 Reino Unido": "UK real estate market",
            "🇩🇪 Alemania": "Immobilienmarkt Deutschland",
            "🇫🇷 Francia": "marché immobilier France",
        },
        "imob_reits": "ETFs Inmobiliarios (REITs)",
        "imob_reits_hint": "Añade también: VNQ (EE.UU.), IUKP.L (UK)",
    },
}.get(lang, {})

# ── CABEÇALHO ─────────────────────────────────────────────────
show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── FORMULÁRIO ────────────────────────────────────────────────
tipo = st.radio(L["tipo_label"],
    [L["tipo_acoes"], L["tipo_cripto"], L["tipo_imob"]],
    horizontal=True)

st.markdown("---")

if tipo in [L["tipo_acoes"], L["tipo_cripto"]]:
    # Defaults por tipo
    default_tickers = {
        L["tipo_acoes"]: "SPY, AAPL, NVDA",
        L["tipo_cripto"]: "BTC-USD, ETH-USD, SOL-USD",
    }
    tickers_input = st.text_input(L["tickers_label"],
        value=default_tickers.get(tipo, ""),
        placeholder="ex: AAPL")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
    max_n = st.slider(L["max_label"], 3, 10, 5)

elif tipo == L["tipo_imob"]:
    paises = L["paises"]
    pais = st.selectbox(L["pais_label"], list(paises.keys()))
    max_n = st.slider(L["max_label"], 3, 15, 8)
    st.caption(f"💡 {L['imob_reits_hint']}")

ver = st.button(L["btn_ver"], type="primary", use_container_width=True)

if not ver and "noticias_resultado" not in st.session_state:
    st.stop()

if ver:
    st.session_state["noticias_resultado"] = {
        "tipo": tipo, "lang": lang,
        "tickers": tickers if tipo != L["tipo_imob"] else [],
        "pais": pais if tipo == L["tipo_imob"] else "",
        "query": paises[pais] if tipo == L["tipo_imob"] else "",
        "max_n": max_n,
    }

cfg    = st.session_state.get("noticias_resultado", {})
tipo   = cfg.get("tipo", tipo)
max_n  = cfg.get("max_n", 5)

# ── FUNÇÕES ───────────────────────────────────────────────────
def card_noticia(badge, fonte, data_str, titulo, resumo, url, badge_cor="#4A9FD4"):
    resumo_curto = resumo[:280] + "..." if len(resumo) > 280 else resumo
    st.markdown(f"""
    <div class='noticia-card'>
        <div class='noticia-meta'>
            <span style='display:inline-block;background:{badge_cor};color:#0A1628;
                border-radius:4px;padding:2px 8px;font-size:0.75rem;
                font-weight:700;margin-right:6px;'>{badge}</span>
            {fonte} · {data_str}
        </div>
        <div class='noticia-titulo'>{titulo}</div>
        <div class='noticia-resumo'>{resumo_curto}</div>
    </div>""", unsafe_allow_html=True)
    if url and url != "#":
        st.markdown(f"[{L['ler']}]({url})")

def formatar_data(data_str):
    if not data_str: return ""
    try:
        from dateutil import parser as dp
        return dp.parse(data_str).strftime("%d/%m/%Y %H:%M")
    except Exception:
        return data_str[:10] if len(data_str) >= 10 else data_str

st.markdown("---")

# ── AÇÕES / CRIPTO ────────────────────────────────────────────
if tipo in [L.get("tipo_acoes",""), L.get("tipo_cripto","")]:
    tickers = cfg.get("tickers", [])
    todas = []
    badge_cor = "#4A9FD4" if tipo == L.get("tipo_acoes","") else "#F7931A"

    with st.spinner(L["a_carregar"]):
        for t in tickers:
            try:
                noticias = yf.Ticker(t).news
                if noticias:
                    for n in noticias[:max_n]:
                        c = n.get("content", {})
                        todas.append({
                            "ticker": t,
                            "titulo": c.get("title", ""),
                            "resumo": c.get("summary", ""),
                            "url":    c.get("canonicalUrl", {}).get("url", "#"),
                            "fonte":  c.get("provider", {}).get("displayName", ""),
                            "data":   c.get("pubDate", ""),
                        })
            except Exception:
                st.warning(f"{L['aviso_ticker']} {t}.")

    if not todas:
        st.warning(L["sem_noticias"]); st.stop()

    # Filtro
    opcoes_filtro = [L["todos"]] + tickers
    filtro = st.selectbox(L["filtro_label"], opcoes_filtro)
    filtradas = todas if filtro == L["todos"] else [n for n in todas if n["ticker"] == filtro]
    st.caption(f"{len(filtradas)} {L['encontradas']}")

    for n in filtradas:
        card_noticia(n["ticker"], n["fonte"], formatar_data(n["data"]),
                     n["titulo"], n["resumo"], n["url"], badge_cor)

# ── IMOBILIÁRIO ───────────────────────────────────────────────
elif tipo == L.get("tipo_imob",""):
    query = cfg.get("query", "")
    pais  = cfg.get("pais", "")

    def google_news_rss(query, max_n=10):
        """Busca notícias via Google News RSS — sem API key."""
        import urllib.parse
        q = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={q}&hl=pt&gl=PT&ceid=PT:pt"
        try:
            resp = requests.get(url, timeout=10,
                headers={"User-Agent": "Mozilla/5.0"})
            if resp.status_code != 200:
                return []
            root = ET.fromstring(resp.content)
            items = root.findall(".//item")
            noticias = []
            for item in items[:max_n]:
                titulo = item.findtext("title", "")
                link   = item.findtext("link", "#")
                fonte  = item.findtext("source", "Google News")
                data   = item.findtext("pubDate", "")
                if titulo:
                    noticias.append({
                        "titulo": titulo, "url": link,
                        "fonte": fonte, "data": data,
                        "resumo": "",
                    })
            return noticias
        except Exception:
            return []

    with st.spinner(L["a_carregar"]):
        noticias_imob = google_news_rss(query, max_n)

    if not noticias_imob:
        st.warning(L["sem_noticias"]); st.stop()

    st.caption(f"{len(noticias_imob)} {L['encontradas']} — {pais}")

    for n in noticias_imob:
        # Formatar data do RSS (formato diferente)
        data_str = ""
        if n["data"]:
            try:
                from dateutil import parser as dp
                data_str = dp.parse(n["data"]).strftime("%d/%m/%Y")
            except Exception:
                data_str = ""

        card_noticia("🏠", n["fonte"], data_str,
                     n["titulo"], n["resumo"], n["url"],
                     badge_cor="#6B8E7F")

st.markdown("---")
st.caption(L["aviso"])
st.caption(L["rodape"])
