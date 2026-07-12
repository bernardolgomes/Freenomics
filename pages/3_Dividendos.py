import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Calendário de Dividendos",
        "subtitulo": "Consulta o histórico de dividendos e o dividend yield dos ativos da tua carteira.",
        "sec_config": "⚙️ Configura a carteira",
        "ticker_label": "Ticker", "btn_add": "➕ Adicionar ticker",
        "anos_label": "Anos de histórico",
        "btn_ver": "📅 Ver dividendos",
        "a_carregar": "A carregar dados de dividendos...",
        "aviso_sem": "Nenhum dos tickers tem histórico de dividendos (ex: SOFI não paga dividendos).",
        "sugestao": "Experimenta: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "resumo": "Resumo de dividendos por ativo",
        "historico": "Histórico de dividendos",
        "ultimos": "Últimos pagamentos",
        "pagamentos": "pagamentos",
        "yield_label": "yield anual",
        "por_acao": "por ação/ano",
        "nota_titulo": "O que é o Dividend Yield?",
        "nota": "É a percentagem do preço da ação que recebes em dividendos por ano. Ex: um yield de 3% num ativo de €100 significa que recebes €3/ano por ação. Atenção: um yield muito alto pode ser sinal de que o preço da ação caiu significativamente.",
        "aviso": "⚠️ Dados históricos — não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Dados via Yahoo Finance",
    },
    "🇬🇧 English": {
        "titulo": "Dividend Calendar",
        "subtitulo": "Check the dividend history and yield of your portfolio assets.",
        "sec_config": "⚙️ Configure portfolio",
        "ticker_label": "Ticker", "btn_add": "➕ Add ticker",
        "anos_label": "Years of history",
        "btn_ver": "📅 View dividends",
        "a_carregar": "Loading dividend data...",
        "aviso_sem": "None of the tickers have dividend history (e.g. SOFI doesn't pay dividends).",
        "sugestao": "Try: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "resumo": "Dividend summary per asset",
        "historico": "Dividend history",
        "ultimos": "Latest payments",
        "pagamentos": "payments",
        "yield_label": "annual yield",
        "por_acao": "per share/year",
        "nota_titulo": "What is Dividend Yield?",
        "nota": "It's the percentage of the share price you receive in dividends per year. E.g. a 3% yield on a €100 asset means €3/year per share. Note: a very high yield may signal the share price has fallen significantly.",
        "aviso": "⚠️ Historical data — does not constitute financial advice.",
        "rodape": "Freenomics · Data via Yahoo Finance",
    },
    "🇫🇷 Français": {
        "titulo": "Calendrier des Dividendes",
        "subtitulo": "Consultez l'historique des dividendes et le rendement de vos actifs.",
        "sec_config": "⚙️ Configurer le portefeuille",
        "ticker_label": "Ticker", "btn_add": "➕ Ajouter un ticker",
        "anos_label": "Années d'historique",
        "btn_ver": "📅 Voir les dividendes",
        "a_carregar": "Chargement des données de dividendes...",
        "aviso_sem": "Aucun ticker n'a d'historique de dividendes.",
        "sugestao": "Essayez: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "resumo": "Résumé des dividendes par actif",
        "historico": "Historique des dividendes",
        "ultimos": "Derniers paiements",
        "pagamentos": "paiements",
        "yield_label": "rendement annuel",
        "por_acao": "par action/an",
        "nota_titulo": "Qu'est-ce que le Dividend Yield?",
        "nota": "C'est le pourcentage du prix de l'action que vous recevez en dividendes par an.",
        "aviso": "⚠️ Données historiques — ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Données via Yahoo Finance",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Dividendenkalender",
        "subtitulo": "Sehen Sie die Dividendenhistorie und -rendite Ihrer Portfolio-Anlagen.",
        "sec_config": "⚙️ Portfolio konfigurieren",
        "ticker_label": "Ticker", "btn_add": "➕ Ticker hinzufügen",
        "anos_label": "Jahre Historik",
        "btn_ver": "📅 Dividenden anzeigen",
        "a_carregar": "Dividendendaten werden geladen...",
        "aviso_sem": "Keiner der Ticker hat eine Dividendenhistorie.",
        "sugestao": "Versuchen Sie: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "resumo": "Dividendenzusammenfassung je Anlage",
        "historico": "Dividendenhistorie",
        "ultimos": "Letzte Zahlungen",
        "pagamentos": "Zahlungen",
        "yield_label": "Jahresrendite",
        "por_acao": "je Aktie/Jahr",
        "nota_titulo": "Was ist die Dividendenrendite?",
        "nota": "Es ist der Prozentsatz des Aktienkurses, den Sie jährlich als Dividende erhalten.",
        "aviso": "⚠️ Historische Daten — stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Daten via Yahoo Finance",
    },
    "🇪🇸 Español": {
        "titulo": "Calendario de Dividendos",
        "subtitulo": "Consulta el historial de dividendos y el yield de los activos de tu cartera.",
        "sec_config": "⚙️ Configura la cartera",
        "ticker_label": "Ticker", "btn_add": "➕ Añadir ticker",
        "anos_label": "Años de historial",
        "btn_ver": "📅 Ver dividendos",
        "a_carregar": "Cargando datos de dividendos...",
        "aviso_sem": "Ninguno de los tickers tiene historial de dividendos.",
        "sugestao": "Prueba: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "resumo": "Resumen de dividendos por activo",
        "historico": "Historial de dividendos",
        "ultimos": "Últimos pagos",
        "pagamentos": "pagos",
        "yield_label": "yield anual",
        "por_acao": "por acción/año",
        "nota_titulo": "¿Qué es el Dividend Yield?",
        "nota": "Es el porcentaje del precio de la acción que recibes en dividendos al año.",
        "aviso": "⚠️ Datos históricos — no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Datos via Yahoo Finance",
    },
}.get(lang, {})

st.markdown("### 📊 Freenomics")
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_config"])

if "div_tickers" not in st.session_state:
    st.session_state.div_tickers = [""]

remover = None
cols_t = st.columns(min(len(st.session_state.div_tickers), 4))
for i, t in enumerate(st.session_state.div_tickers):
    with cols_t[i % 4]:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.session_state.div_tickers[i] = st.text_input(
                L["ticker_label"], value=t, key=f"div_t_{i}",
                label_visibility="collapsed" if i > 0 else "visible").upper().strip()
        with c2:
            if len(st.session_state.div_tickers) > 1:
                st.markdown("<br>" if i == 0 else "", unsafe_allow_html=True)
                if st.button("🗑️", key=f"div_rm_{i}"): remover = i

if remover is not None:
    st.session_state.div_tickers.pop(remover); st.rerun()

col_add, col_anos = st.columns([1, 2])
with col_add:
    if st.button(L["btn_add"]):
        st.session_state.div_tickers.append(""); st.rerun()
with col_anos:
    anos_hist = st.slider(L["anos_label"], 1, 10, 5)

ver = st.button(L["btn_ver"], type="primary", use_container_width=True)

if not ver and "div_resultado" not in st.session_state:
    st.stop()

if ver:
    st.session_state["div_resultado"] = {
        "tickers": [t for t in st.session_state.div_tickers if t],
        "anos": anos_hist,
    }

cfg     = st.session_state.get("div_resultado", {})
tickers = cfg.get("tickers", [t for t in st.session_state.div_tickers if t])
anos_hist = cfg.get("anos", anos_hist)

@st.cache_data(ttl=3600)
def carregar_div(ticker):
    t = yf.Ticker(ticker)
    return t.dividends, t.info

resultados = {}
with st.spinner(L["a_carregar"]):
    for t in tickers:
        try:
            divs, info = carregar_div(t)
            if divs is not None and not divs.empty:
                resultados[t] = {"divs": divs, "info": info}
        except Exception:
            pass

st.markdown("---")

if not resultados:
    st.warning(L["aviso_sem"])
    st.info(L["sugestao"])
    st.stop()

# ── RESUMO ────────────────────────────────────────────────────
st.subheader(L["resumo"])
cols = st.columns(min(len(resultados), 4))
for col, (t, dados) in zip(cols, resultados.items()):
    info = dados["info"]
    y    = (info.get("dividendYield", 0) or 0) * 100
    rate = info.get("dividendRate", 0) or 0
    with col:
        def cartao_div(label, val, sub=None):
            h  = '<div style="background:#0E2A3D;border-radius:10px;padding:14px 16px;border-left:4px solid #C29A4B;margin-bottom:10px;">'
            h += f'<p style="color:#C8D3DA;font-size:0.8rem;margin:0 0 2px 0;">{label}</p>'
            h += f'<p style="color:#FAF8F3;font-size:1.5rem;font-weight:700;margin:0;">{val}</p>'
            if sub: h += f'<p style="color:#C29A4B;font-size:0.85rem;margin:2px 0 0 0;">{sub}</p>'
            h += '</div>'
            return h
        st.markdown(f"**{t}**")
        st.markdown(cartao_div(L["yield_label"], f"{y:.2f}%",
            f"${rate:.2f} {L['por_acao']}"), unsafe_allow_html=True)

# ── GRÁFICO ───────────────────────────────────────────────────
st.subheader(f"{L['historico']} — {anos_hist} {L.get('anos_label','anos')}")
fig = go.Figure()
ano_inicio = datetime.today().year - anos_hist
for i, (t, dados) in enumerate(resultados.items()):
    df = dados["divs"][dados["divs"].index.year >= ano_inicio]
    if not df.empty:
        fig.add_trace(go.Bar(x=df.index, y=df.values.flatten(),
            name=t, marker_color=PLOT_COLORS[i % len(PLOT_COLORS)], opacity=0.85))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Dividend per share ($/€)", xaxis_title="Date",
    barmode="group", height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

# ── TABELA ────────────────────────────────────────────────────
st.subheader(L["ultimos"])
for t, dados in resultados.items():
    df = dados["divs"][dados["divs"].index.year >= ano_inicio]
    if df.empty: continue
    d = pd.DataFrame({"Data": df.index.strftime("%d/%m/%Y"),
                      "Dividendo": df.values.flatten().round(4)}).sort_values("Data", ascending=False).head(12)
    with st.expander(f"📋 {t} — {len(d)} {L['pagamentos']}"):
        st.dataframe(d.set_index("Data"), use_container_width=True)

st.markdown(f"<div class='info-box'>💡 <strong>{L['nota_titulo']}</strong><br>{L['nota']}</div>",
    unsafe_allow_html=True)
st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
