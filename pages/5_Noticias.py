import streamlit as st, yfinance as yf
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_GERAL, CSS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_GERAL[lang]

st.markdown("### 📊 Freenomics"); st.title(T["noticias_titulo"]); st.caption(T["noticias_sub"])
st.sidebar.header(T["noticias_carteira"])
tickers_input = st.sidebar.text_input(T["noticias_tickers"], value="SPY, SOFI, AAPL")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
max_n = st.sidebar.slider(T["noticias_max"], 3, 10, 5)

todas = []
with st.spinner(T["noticias_a_carregar"]):
    for t in tickers:
        try:
            noticias = yf.Ticker(t).news
            if noticias:
                for n in noticias[:max_n]:
                    todas.append({"ticker": t, "titulo": n.get("content",{}).get("title",""), "resumo": n.get("content",{}).get("summary",""), "url": n.get("content",{}).get("canonicalUrl",{}).get("url","#"), "fonte": n.get("content",{}).get("provider",{}).get("displayName",""), "data": n.get("content",{}).get("pubDate","")})
        except: st.warning(f"{T['noticias_aviso']} {t}.")

if not todas: st.warning(T["noticias_sem"]); st.stop()

filtro = st.selectbox(T["noticias_filtro"], [T["noticias_todos"]] + tickers)
filtradas = todas if filtro == T["noticias_todos"] else [n for n in todas if n["ticker"]==filtro]
st.caption(f"{len(filtradas)} {T['noticias_encontradas']}")

for n in filtradas:
    data_str = ""
    if n["data"]:
        try:
            from dateutil import parser as dp; data_str = dp.parse(n["data"]).strftime("%d/%m/%Y %H:%M")
        except: data_str = n["data"][:10]
    resumo = n["resumo"][:280]+"..." if len(n["resumo"])>280 else n["resumo"]
    st.markdown(f"<div class='noticia-card'><div class='noticia-meta'><span class='ticker-badge'>{n['ticker']}</span>{n['fonte']} · {data_str}</div><div class='noticia-titulo'>{n['titulo']}</div><div class='noticia-resumo'>{resumo}</div></div>", unsafe_allow_html=True)
    if n["url"] and n["url"]!="#": st.markdown(f"[{T['noticias_ler']}]({n['url']})")

st.markdown("---"); st.caption(T["noticias_rodape"])
