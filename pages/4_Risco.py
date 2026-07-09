import streamlit as st, yfinance as yf, pandas as pd, numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_GERAL, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_GERAL[lang]

st.markdown("### 📊 Freenomics"); st.title(T["risco_titulo"]); st.caption(T["risco_sub"])
st.sidebar.header(T["risco_carteira"])
tickers_input = st.sidebar.text_input(T["risco_tickers"], value="SPY, SOFI, AAPL, BTC-USD")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
periodo_opcoes = T["risco_periodos"]
periodo_label = st.sidebar.selectbox(T["risco_periodo"], list(periodo_opcoes.keys()), index=1)
dias = periodo_opcoes[periodo_label]
capital = st.sidebar.number_input(T["risco_capital"], value=10000, step=500)

@st.cache_data(ttl=3600)
def carregar(ticker, dias):
    end = datetime.today(); start = end - timedelta(days=dias)
    df = yf.download(ticker, start=start, end=end, progress=False)
    if df.empty:
        return pd.Series(dtype=float)
    close = df["Close"]
    # yfinance pode devolver DataFrame ou Series dependendo da versão
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    return close.squeeze()

dados = {}
with st.spinner(T["risco_a_carregar"]):
    for t in tickers:
        try:
            s = carregar(t, dias)
            if s is not None and len(s) > 0:
                dados[t] = s
        except Exception:
            pass

if len(dados) < 2:
    st.error(T["risco_erro"]); st.stop()

# Construir DataFrame alinhando pelos índices comuns
precos = pd.DataFrame(dados).dropna()

if precos.empty or precos.shape[1] < 2:
    st.error(T["risco_erro"]); st.stop()

retornos = precos.pct_change().dropna()

st.subheader(T["risco_vol_titulo"])
cols = st.columns(len(dados))
for col, t in zip(cols, dados.keys()):
    if t not in retornos.columns:
        continue
    vol = float(retornos[t].std() * np.sqrt(252) * 100)
    var = float(np.percentile(retornos[t], 5) * 100)
    perda = capital * abs(var) / 100
    nivel = "alto" if vol > 40 else ("medio" if vol > 20 else "baixo")
    with col:
        st.metric(t, f"Vol: {vol:.1f}%", f"{T['risco_var']}: {var:.2f}%/dia")
        st.markdown(
            f"<div class='risco-box risco-{nivel}'>{T['risco_perda']} "
            f"<strong>€{perda:,.0f}</strong> {T['risco_capital_label']} €{capital:,.0f}.</div>",
            unsafe_allow_html=True
        )

st.subheader(T["risco_corr_titulo"]); st.caption(T["risco_corr_sub"])
corr = retornos.corr().round(2)
fig = go.Figure(data=go.Heatmap(
    z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
    colorscale=[[0, "#C29A4B"], [0.5, "#FAF8F3"], [1, "#0E2A3D"]],
    zmin=-1, zmax=1, text=corr.values.round(2), texttemplate="%{text}", showscale=True
))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
                  height=350, margin=dict(l=10, r=10, t=10, b=10))
st.plotly_chart(fig, use_container_width=True)

st.subheader(T["risco_dd_titulo"])
fig2 = go.Figure()
for i, t in enumerate(dados.keys()):
    if t not in precos.columns:
        continue
    pico = precos[t].cummax()
    dd = (precos[t] - pico) / pico * 100
    fig2.add_trace(go.Scatter(
        x=precos.index, y=dd.values, name=t,
        line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)], width=1.5)
    ))
fig2.update_layout(
    plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Drawdown (%)", xaxis_title=T["risco_periodo"],
    hovermode="x unified", height=380,
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
st.plotly_chart(fig2, use_container_width=True)

st.subheader(T["risco_stress_titulo"]); st.caption(T["risco_stress_sub"])
cenarios = T["risco_cenarios"]
cols2 = st.columns(len(cenarios))
for col, (nome, pct) in zip(cols2, cenarios.items()):
    perda = capital * pct
    col.metric(nome, f"€{capital + perda:,.0f}", f"€{perda:,.0f}", delta_color="inverse")

st.markdown("---"); st.caption(T["risco_rodape"])
