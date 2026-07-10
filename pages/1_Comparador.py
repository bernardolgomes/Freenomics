import streamlit as st
import yfinance as yf
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_COMPARADOR, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_COMPARADOR[lang]

st.markdown("### 📊 Freenomics")
st.title(T["titulo"])
st.caption(T["subtitulo"])

# ── SIDEBAR ──────────────────────────────────────────────────
st.sidebar.header(T["sidebar_a"])
tickers_a = st.sidebar.text_input(T["tickers_a"], value="SPY")
st.sidebar.header(T["sidebar_b"])
tickers_b = st.sidebar.text_input(T["tickers_b"], value="SOFI")
periodo_opcoes = T["periodos"]
periodo_label = st.sidebar.selectbox(T["periodo"], list(periodo_opcoes.keys()), index=2)
dias = periodo_opcoes[periodo_label]
investimento = st.sidebar.number_input(T["investimento"], value=10000, step=500)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🤖 Anthropic API")
api_key = st.sidebar.text_input("API Key", type="password", placeholder="sk-ant-...", help="Obtém a tua key em console.anthropic.com")

# ── DADOS ────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar(ticker, dias):
    end = datetime.today(); start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

def retorno_carteira(tickers_str, dias):
    tickers = [t.strip().upper() for t in tickers_str.split(",") if t.strip()]
    series = []
    for t in tickers:
        df = carregar(t, dias)
        if not df.empty:
            close = df["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            close = close.squeeze()
            series.append(close / close.iloc[0])
    if not series:
        return None, []
    return pd.concat(series, axis=1).mean(axis=1), tickers

with st.spinner(T["a_carregar"]):
    retorno_a, lista_a = retorno_carteira(tickers_a, dias)
    retorno_b, lista_b = retorno_carteira(tickers_b, dias)

if retorno_a is None or retorno_b is None:
    st.error(T["a_carregar"]); st.stop()

def metricas_serie(serie):
    d = serie.pct_change().dropna()
    return {
        "retorno": round(float((serie.iloc[-1]-1)*100), 2),
        "vol": round(float(d.std()*np.sqrt(252)*100), 2),
        "dd": round(float(((serie-serie.cummax())/serie.cummax()).min()*100), 2),
        "sharpe": round(float((d.mean()/d.std())*np.sqrt(252)) if d.std().item() != 0 else 0, 2),
    }

ma = metricas_serie(retorno_a)
mb = metricas_serie(retorno_b)
nome_a = " + ".join(lista_a)
nome_b = " + ".join(lista_b)
vencedor = nome_a if ma["retorno"] > mb["retorno"] else nome_b

st.markdown(f"<div class='winner-box'>{T['vencedor']}: {vencedor}</div>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
for col, nome, m in [(col1, f"{T['carteira_a']} — {nome_a}", ma), (col2, f"{T['carteira_b']} — {nome_b}", mb)]:
    with col:
        st.subheader(nome)
        st.metric(T["retorno"], f"{m['retorno']}%",
                  delta="+▲" if m['retorno'] >= 0 else "-▼",
                  delta_color="normal")
        st.metric(T["vol"], f"{m['vol']}%")
        st.metric(T["drawdown"], f"{m['dd']}%",
                  delta="-▼", delta_color="normal")
        st.metric(T["sharpe"], f"{m['sharpe']}",
                  delta="+▲" if m['sharpe'] >= 0 else "-▼",
                  delta_color="normal")
        ganho = investimento*(1+m['retorno']/100) - investimento
        st.metric(T["valor_final"], f"€{investimento*(1+m['retorno']/100):,.0f}",
                  delta=f"+€{ganho:,.0f}" if ganho >= 0 else f"-€{abs(ganho):,.0f}",
                  delta_color="normal")

# ── GRÁFICO ──────────────────────────────────────────────────
st.subheader(T["grafico"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=retorno_a.index, y=(retorno_a*100).values.flatten(), name=f"A: {nome_a}", line=dict(color=PLOT_COLORS[0], width=2.5)))
fig.add_trace(go.Scatter(x=retorno_b.index, y=(retorno_b*100).values.flatten(), name=f"B: {nome_b}", line=dict(color=PLOT_COLORS[1], width=2.5)))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3", yaxis_title=T["grafico_y"], xaxis_title=T["grafico_x"], hovermode="x unified", height=420, legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

# ── INSIGHTS VIA API ─────────────────────────────────────────
LINGUA_NOME = {
    "🇵🇹 Português": "português europeu",
    "🇬🇧 English": "English",
    "🇫🇷 Français": "français",
    "🇩🇪 Deutsch": "Deutsch",
    "🇪🇸 Español": "español",
}

def gerar_insights_comparador(ma, mb, nome_a, nome_b, periodo_label, investimento, lang, api_key):
    lingua = LINGUA_NOME.get(lang, "português")
    val_a = investimento * (1 + ma["retorno"]/100)
    val_b = investimento * (1 + mb["retorno"]/100)
    perda_a = investimento * abs(ma["dd"]) / 100
    perda_b = investimento * abs(mb["dd"]) / 100

    prompt = f"""És um consultor financeiro experiente a comparar duas estratégias de investimento para um investidor individual.

Período de análise: {periodo_label}
Investimento inicial: €{investimento:,.0f}

Carteira A — {nome_a}:
- Retorno: {ma['retorno']}% → valor final €{val_a:,.0f}
- Volatilidade anual: {ma['vol']}%
- Pior queda desde o pico (drawdown): {ma['dd']}% (perda temporária de €{perda_a:,.0f})
- Sharpe ratio: {ma['sharpe']}

Carteira B — {nome_b}:
- Retorno: {mb['retorno']}% → valor final €{val_b:,.0f}
- Volatilidade anual: {mb['vol']}%
- Pior queda desde o pico (drawdown): {mb['dd']}% (perda temporária de €{perda_b:,.0f})
- Sharpe ratio: {mb['sharpe']}

Escreve uma análise comparativa em {lingua} com 3-4 parágrafos curtos que:
1. Compare os retornos em termos concretos (euros ganhos, não só percentagens)
2. Analise qual carteira exigiu mais "estômago" para aguentar — fala do drawdown em euros e o que isso significa psicologicamente
3. Dê uma perspetiva sobre qual foi a escolha mais inteligente considerando o risco tomado (Sharpe ratio), não só o retorno bruto
4. Termine com uma reflexão prática: o retorno extra de uma justificou o risco adicional? Que tipo de investidor escolheria cada uma?

Tom: honesto, direto, como um amigo que percebe de finanças e te diz a verdade.
Não uses bullet points. Não repitas todos os números — escolhe os que mais importam para a narrativa.
Não incluas títulos. Apenas parágrafos seguidos."""

    try:
        response = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            },
            json={
                "model": "claude-haiku-4-5-20251001",
                "max_tokens": 600,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        if response.status_code == 200:
            return response.json()["content"][0]["text"], True
        return None, False
    except Exception:
        return None, False

def fallback_comparador(ma, mb, nome_a, nome_b, periodo_label, investimento, T):
    val_a = investimento * (1 + ma["retorno"]/100)
    val_b = investimento * (1 + mb["retorno"]/100)
    vencedor_ret = nome_a if ma["retorno"] > mb["retorno"] else nome_b
    vencedor_sharpe = nome_a if ma["sharpe"] > mb["sharpe"] else nome_b
    perda_a = investimento * abs(ma["dd"]) / 100
    perda_b = investimento * abs(mb["dd"]) / 100
    return [
        f"Em {periodo_label}, **{nome_a}** gerou um retorno de {ma['retorno']}% (€{val_a:,.0f}) e **{nome_b}** de {mb['retorno']}% (€{val_b:,.0f}). O melhor retorno bruto foi de **{vencedor_ret}**.",
        f"Em termos de risco, **{nome_a}** chegou a cair €{perda_a:,.0f} desde o seu pico, enquanto **{nome_b}** chegou a cair €{perda_b:,.0f}. Quanto maior a queda, mais difícil é manter a calma e não vender.",
        f"Ajustando ao risco (Sharpe ratio), **{vencedor_sharpe}** foi a escolha mais eficiente — ofereceu mais retorno por unidade de risco assumida.",
    ]

st.subheader("📝 Análise comparativa")

import re
def renderizar(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)

if api_key:
    with st.spinner("🤖 A gerar análise comparativa com IA..."):
        texto_ai, sucesso = gerar_insights_comparador(ma, mb, nome_a, nome_b, periodo_label, investimento, lang, api_key)
    if sucesso and texto_ai:
        texto_html = renderizar(texto_ai).replace("\n\n", "<br><br>")
        st.markdown(f"<div class='insight-box'>{texto_html}</div>", unsafe_allow_html=True)
        st.caption("✨ Análise gerada por IA · Não constitui aconselhamento financeiro.")
    else:
        st.warning("Não foi possível contactar a API. A usar análise automática.")
        for frase in fallback_comparador(ma, mb, nome_a, nome_b, periodo_label, investimento, T):
            st.markdown(f"<div class='insight-box'>{renderizar(frase)}</div>", unsafe_allow_html=True)
else:
    for frase in fallback_comparador(ma, mb, nome_a, nome_b, periodo_label, investimento, T):
        st.markdown(f"<div class='insight-box'>{renderizar(frase)}</div>", unsafe_allow_html=True)
    st.info("💡 Adiciona a tua Anthropic API key na sidebar para análises geradas por IA.")

st.markdown("---")
st.caption(T["rodape"])
