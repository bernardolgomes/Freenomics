import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys, os, requests
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_DASHBOARD, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_DASHBOARD[lang]

st.markdown("### 📊 Freenomics")
st.title(T["titulo"])
st.caption(T["subtitulo"])

# ── SIDEBAR ──────────────────────────────────────────────────
st.sidebar.header(T["sidebar_carteira"])
tickers_input = st.sidebar.text_input(T["sidebar_tickers"], value="SPY, SOFI")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
periodo_opcoes = T["periodos"]
periodo_label = st.sidebar.selectbox(T["sidebar_periodo"], list(periodo_opcoes.keys()), index=2)
dias = periodo_opcoes[periodo_label]
investimento_inicial = st.sidebar.number_input(T["sidebar_investimento"], value=1000, step=100)

st.sidebar.markdown("---")
st.sidebar.markdown("#### 🤖 Anthropic API")
api_key = st.sidebar.text_input("API Key", type="password", placeholder="sk-ant-...", help="Obtém a tua key em console.anthropic.com")

# ── DADOS ────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar_dados(ticker, dias):
    end = datetime.today()
    start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

dados = {}
with st.spinner(T["a_carregar"]):
    for t in tickers:
        try:
            df = carregar_dados(t, dias)
            if not df.empty:
                dados[t] = df
        except Exception:
            st.warning(f"{T['erro_ticker']} {t}.")

if not dados:
    st.error(T["erro_nenhum"])
    st.stop()

# ── MÉTRICAS ─────────────────────────────────────────────────
def calcular_metricas(df):
    precos = df["Close"]
    if isinstance(precos, pd.DataFrame):
        precos = precos.iloc[:, 0]
    precos = precos.squeeze()
    retorno_total = float((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
    retornos_diarios = precos.pct_change().dropna()
    volatilidade = float(retornos_diarios.std() * np.sqrt(252) * 100)
    pico = precos.cummax()
    max_drawdown = float(((precos - pico) / pico).min() * 100)
    sharpe = float((retornos_diarios.mean() / retornos_diarios.std()) * np.sqrt(252)) if retornos_diarios.std().item() != 0 else 0.0
    preco_atual = float(precos.iloc[-1])
    preco_inicial = float(precos.iloc[0])
    return {
        "retorno_total": round(retorno_total, 2),
        "volatilidade": round(volatilidade, 2),
        "max_drawdown": round(max_drawdown, 2),
        "sharpe": round(sharpe, 2),
        "preco_atual": round(preco_atual, 2),
        "preco_inicial": round(preco_inicial, 2),
    }

metricas = {t: calcular_metricas(df) for t, df in dados.items()}

# ── CARTÕES ──────────────────────────────────────────────────
def cartao(label, pct_str, euros_str=None, euros_cor="#4CAF50"):
    euros_html = ""
    if euros_str:
        euros_html = f'<p style="color:{euros_cor};font-size:0.95rem;margin:4px 0 0 0;">'+ euros_str + '</p>'
    partes = [
        '<div style="background:#0E2A3D;border-radius:10px;padding:16px 18px;border-left:4px solid #C29A4B;margin-bottom:12px;">',
        f'<p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 4px 0;">' + label + '</p>',
        f'<p style="color:#FAF8F3;font-size:1.8rem;font-weight:700;margin:0;">' + pct_str + '</p>',
        euros_html,
        '</div>'
    ]
    return "".join(partes)

def cor(valor):
    return "#4CAF50" if valor >= 0 else "#F44336"

cols = st.columns(len(dados))
for col, (t, m) in zip(cols, metricas.items()):
    with col:
        st.subheader(t)
        ganho = investimento_inicial * m['retorno_total'] / 100
        perda_dd = investimento_inicial * m['max_drawdown'] / 100
        st.markdown(cartao(
            T["metrica_retorno"], f"{m['retorno_total']}%",
            euros_str=f"{'+' if ganho >= 0 else ''}€{ganho:,.0f}",
            euros_cor=cor(m['retorno_total'])
        ), unsafe_allow_html=True)
        st.markdown(cartao(
            T["metrica_vol"], f"{m['volatilidade']}%"
        ), unsafe_allow_html=True)
        st.markdown(cartao(
            T["metrica_drawdown"], f"{m['max_drawdown']}%",
            euros_str=f"€{perda_dd:,.0f} de queda máxima",
            euros_cor="#F44336"
        ), unsafe_allow_html=True)
        st.markdown(cartao(
            T["metrica_sharpe"], f"{m['sharpe']}",
            euros_str=None
        ), unsafe_allow_html=True)

# ── GRÁFICO ──────────────────────────────────────────────────
st.subheader(T["grafico_titulo"])
fig = go.Figure()
for i, (t, df) in enumerate(dados.items()):
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.squeeze()
    norm = (close / close.iloc[0]) * 100
    fig.add_trace(go.Scatter(
        x=df.index, y=norm.values.flatten(), name=t,
        line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)], width=2.5)
    ))

# Benchmark SP500 (SPY) — só adiciona se SPY não estiver já na carteira
if "SPY" not in [t.upper() for t in tickers]:
    try:
        df_spy = carregar_dados("SPY", dias)
        if not df_spy.empty:
            close_spy = df_spy["Close"]
            if isinstance(close_spy, pd.DataFrame):
                close_spy = close_spy.iloc[:, 0]
            close_spy = close_spy.squeeze()
            norm_spy = (close_spy / close_spy.iloc[0]) * 100
            fig.add_trace(go.Scatter(
                x=df_spy.index,
                y=norm_spy.values.flatten(),
                name="S&P 500 (benchmark)",
                line=dict(color="#888888", width=1.5, dash="dash"),
                opacity=0.7,
            ))
    except Exception:
        pass

fig.update_layout(
    plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title=T["grafico_y"], xaxis_title=T["grafico_x"],
    hovermode="x unified", height=440,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
)
st.plotly_chart(fig, use_container_width=True)

# ── INSIGHTS VIA API ANTHROPIC ───────────────────────────────
st.subheader(T["insights_titulo"])

LINGUA_NOME = {
    "🇵🇹 Português": "português europeu",
    "🇬🇧 English": "English",
    "🇫🇷 Français": "français",
    "🇩🇪 Deutsch": "Deutsch",
    "🇪🇸 Español": "español",
}

def gerar_insights_api(metricas, periodo_label, investimento, lang, api_key):
    lingua = LINGUA_NOME.get(lang, "português")

    # Contexto rico para o modelo
    linhas = []
    for t, m in metricas.items():
        perda_max_euros = investimento * abs(m["max_drawdown"]) / 100
        ganho_euros = investimento * m["retorno_total"] / 100
        linhas.append(
            f"- {t}: retorno {m['retorno_total']}% (€{ganho_euros:,.0f} num investimento de €{investimento}), "
            f"volatilidade anual {m['volatilidade']}%, drawdown máximo {m['max_drawdown']}% "
            f"(significando uma perda temporária de €{perda_max_euros:,.0f}), Sharpe ratio {m['sharpe']}"
        )
    resumo = "\n".join(linhas)

    prompt = f"""És um consultor financeiro experiente a explicar dados de investimento a um investidor individual não profissional.

Analisa estes dados do período de {periodo_label}:
{resumo}

Escreve uma análise em {lingua} com 3-4 parágrafos curtos (2-3 frases cada) que:
1. Explique qual ativo performou melhor e contextualize esse retorno de forma humana (ex: o que significa na prática)
2. Compare o risco de cada ativo de forma clara — usa os valores em euros, não só percentagens
3. Dê uma perspetiva honesta sobre o binómio risco/retorno — o melhor retorno valeu o risco adicional?
4. Termine com uma nota prática para o investidor refletir (não uma recomendação direta de compra/venda)

Tom: claro, direto, como se explicasses a um amigo inteligente que não é especialista em finanças.
Não uses bullet points. Não repitas os números todos — escolhe os mais relevantes.
Não incluas títulos nem secções. Apenas os parágrafos seguidos."""

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
        else:
            return None, False
    except Exception:
        return None, False

def gerar_insights_fallback(metricas, periodo_label, T):
    """Versão de fallback com regras — usada se não houver API key."""
    frases = []
    ordenado = sorted(metricas.items(), key=lambda x: x[1]["retorno_total"], reverse=True)
    melhor, pior = ordenado[0], ordenado[-1]
    if len(metricas) > 1:
        frase = T["insight_melhor"](melhor[0], periodo_label, melhor[1]["retorno_total"]) + " "
        frase += T["insight_pior_subida"](pior[0], pior[1]["retorno_total"]) if pior[1]["retorno_total"] >= 0 else T["insight_pior_queda"](pior[0], pior[1]["retorno_total"])
        frases.append(frase)
    else:
        t, m = list(metricas.items())[0]
        frases.append(T["insight_unico"](t, periodo_label, m["retorno_total"]))
    if len(metricas) > 1:
        mais_volatil = sorted(metricas.items(), key=lambda x: x[1]["volatilidade"], reverse=True)[0]
        frases.append(T["insight_volatil"](mais_volatil[0], mais_volatil[1]["volatilidade"]))
    for t, m in metricas.items():
        if m["max_drawdown"] < -20:
            frases.append(T["insight_drawdown"](t, m["max_drawdown"]))
    melhor_sharpe = sorted(metricas.items(), key=lambda x: x[1]["sharpe"], reverse=True)[0]
    if melhor_sharpe[1]["sharpe"] > 0:
        frases.append(T["insight_sharpe"](melhor_sharpe[0]))
    return frases

import re

def renderizar_insight(texto):
    """Converte **bold** em <strong> para renderização correta no HTML."""
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)

if api_key:
    with st.spinner("🤖 A gerar análise com IA..."):
        texto_ai, sucesso = gerar_insights_api(metricas, periodo_label, investimento_inicial, lang, api_key)
    if sucesso and texto_ai:
        texto_html = renderizar_insight(texto_ai).replace("\n\n", "<br><br>")
        st.markdown(f"<div class='insight-box'>{texto_html}</div>", unsafe_allow_html=True)
        st.caption("✨ Análise gerada por IA · " + T["aviso"])
    else:
        st.warning("Não foi possível contactar a API. A usar análise automática.")
        for frase in gerar_insights_fallback(metricas, periodo_label, T):
            st.markdown(f"<div class='insight-box'>{renderizar_insight(frase)}</div>", unsafe_allow_html=True)
else:
    for frase in gerar_insights_fallback(metricas, periodo_label, T):
        st.markdown(f"<div class='insight-box'>{renderizar_insight(frase)}</div>", unsafe_allow_html=True)
    st.info("💡 Adiciona a tua Anthropic API key na sidebar para análises geradas por IA.")

st.caption(T["aviso"])
st.markdown("---")
st.caption(T["rodape"])
