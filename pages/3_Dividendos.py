import streamlit as st, yfinance as yf, pandas as pd
import plotly.graph_objects as go
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_GERAL, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_GERAL[lang]

st.markdown("### 📊 Freenomics"); st.title(T["div_titulo"]); st.caption(T["div_sub"])
st.sidebar.header(T["div_carteira"])
tickers_input = st.sidebar.text_input(T["div_tickers"], value="SPY, AAPL, JNJ, KO")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
anos_hist = st.sidebar.slider(T["div_anos"], 1, 10, 5)

@st.cache_data(ttl=3600)
def carregar_div(ticker):
    t = yf.Ticker(ticker); return t.dividends, t.info

resultados = {}
with st.spinner(T["div_a_carregar"]):
    for t in tickers:
        try:
            divs, info = carregar_div(t)
            if divs is not None and not divs.empty: resultados[t] = {"divs": divs, "info": info}
        except: pass

if not resultados:
    st.warning(T["div_aviso_sem"]); st.info(T["div_info"]); st.stop()

st.subheader(T["div_resumo"])
cols = st.columns(min(len(resultados),4))
for col, (t, dados) in zip(cols, resultados.items()):
    info = dados["info"]
    yield_a = info.get("dividendYield",0) or 0
    rate = info.get("dividendRate",0) or 0
    col.metric(t, f"{yield_a*100:.2f}% {T['div_yield']}", f"€{rate:.2f} {T['div_ano_acao']}")

st.subheader(f"{T['div_historico']} {anos_hist} {T['div_anos_label']}")
fig = go.Figure()
ano_inicio = datetime.today().year - anos_hist
for i, (t, dados) in enumerate(resultados.items()):
    df = dados["divs"][dados["divs"].index.year >= ano_inicio]
    if not df.empty:
        fig.add_trace(go.Bar(x=df.index, y=df.values.flatten(), name=t, marker_color=PLOT_COLORS[i % len(PLOT_COLORS)], opacity=0.85))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3", yaxis_title=T["div_y"], xaxis_title=T["div_x"], barmode="group", height=420, legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

st.subheader(T["div_ultimos"])
for t, dados in resultados.items():
    df = dados["divs"][dados["divs"].index.year >= ano_inicio]
    if df.empty: continue
    d = pd.DataFrame({T["div_ticker"]: t, T["div_data"]: df.index.strftime("%d/%m/%Y"), T["div_div"]: df.values.flatten().round(4)})
    d = d.sort_values(T["div_data"], ascending=False).head(12)
    with st.expander(f"📋 {t} — {T['div_ultimos_label']} {len(d)} {T['div_pagamentos']}"):
        st.dataframe(d.set_index(T["div_ticker"]), use_container_width=True)

st.markdown(f"<div class='info-box'>💡 <strong>{T['div_nota_titulo']}</strong><br>{T['div_nota']}</div>", unsafe_allow_html=True)
st.markdown("---"); st.caption(T["div_rodape"])
