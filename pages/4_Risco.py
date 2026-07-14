import streamlit as st
import streamlit.components.v1 as components
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, PLOT_COLORS, FIX_DROPDOWNS_JS

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Análise de Risco",
        "subtitulo": "Correlação entre ativos, volatilidade histórica e simulação de cenários adversos.",
        "sec_config": "⚙️ Configura a carteira",
        "ticker_label": "Ticker", "btn_add": "➕ Adicionar ticker",
        "periodo_label": "Período", "capital_label": "Capital total investido (€)",
        "btn_analisar": "⚠️ Analisar risco",
        "a_carregar": "A carregar dados...",
        "erro": "Precisas de pelo menos 2 tickers válidos.",
        "vol_titulo": "Volatilidade e risco por ativo",
        "var_label": "VaR 95%", "perda_txt": "Num dia mau (5% piores), podes perder até",
        "capital_txt": "num capital de",
        "risco_alto": "alto", "risco_medio": "medio", "risco_baixo": "baixo",
        "corr_titulo": "Correlação entre ativos",
        "corr_sub": "1 = movem juntos | -1 = direções opostas | 0 = sem relação",
        "dd_titulo": "Drawdown histórico (queda face ao pico)",
        "stress_titulo": "Simulação de cenários adversos",
        "stress_sub": "Impacto estimado no capital em diferentes cenários de mercado",
        "cenarios": {"Correção leve (-10%)": -0.10, "Correção moderada (-20%)": -0.20,
                     "Bear market (-35%)": -0.35, "Crash severo (-50%)": -0.50},
        "aviso": "⚠️ VaR = Value at Risk (percentil 5%) · Não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Dados via Yahoo Finance",
        "periodos": {"1 ano": 365, "2 anos": 730, "5 anos": 1825},
    },
    "🇬🇧 English": {
        "titulo": "Risk Analysis",
        "subtitulo": "Asset correlation, historical volatility and adverse scenario simulation.",
        "sec_config": "⚙️ Configure portfolio",
        "ticker_label": "Ticker", "btn_add": "➕ Add ticker",
        "periodo_label": "Period", "capital_label": "Total invested capital (€)",
        "btn_analisar": "⚠️ Analyse risk",
        "a_carregar": "Loading data...",
        "erro": "You need at least 2 valid tickers.",
        "vol_titulo": "Volatility and risk per asset",
        "var_label": "VaR 95%", "perda_txt": "On a bad day (worst 5%), you could lose up to",
        "capital_txt": "on a capital of",
        "risco_alto": "alto", "risco_medio": "medio", "risco_baixo": "baixo",
        "corr_titulo": "Asset correlation",
        "corr_sub": "1 = move together | -1 = opposite directions | 0 = no relation",
        "dd_titulo": "Historical drawdown (fall from peak)",
        "stress_titulo": "Stress scenario simulation",
        "stress_sub": "Estimated impact on capital in different market scenarios",
        "cenarios": {"Mild correction (-10%)": -0.10, "Moderate correction (-20%)": -0.20,
                     "Bear market (-35%)": -0.35, "Severe crash (-50%)": -0.50},
        "aviso": "⚠️ VaR = Value at Risk (5th percentile) · Does not constitute financial advice.",
        "rodape": "Freenomics · Data via Yahoo Finance",
        "periodos": {"1 year": 365, "2 years": 730, "5 years": 1825},
    },
    "🇫🇷 Français": {
        "titulo": "Analyse des Risques",
        "subtitulo": "Corrélation entre actifs, volatilité historique et simulation de scénarios adverses.",
        "sec_config": "⚙️ Configurer le portefeuille",
        "ticker_label": "Ticker", "btn_add": "➕ Ajouter un ticker",
        "periodo_label": "Période", "capital_label": "Capital total investi (€)",
        "btn_analisar": "⚠️ Analyser le risque",
        "a_carregar": "Chargement...",
        "erro": "Vous avez besoin d'au moins 2 tickers valides.",
        "vol_titulo": "Volatilité et risque par actif",
        "var_label": "VaR 95%", "perda_txt": "Un mauvais jour (5% pires), vous pourriez perdre jusqu'à",
        "capital_txt": "sur un capital de",
        "risco_alto": "alto", "risco_medio": "medio", "risco_baixo": "baixo",
        "corr_titulo": "Corrélation entre actifs",
        "corr_sub": "1 = évoluent ensemble | -1 = directions opposées | 0 = sans relation",
        "dd_titulo": "Drawdown historique (chute depuis le pic)",
        "stress_titulo": "Simulation de scénarios de stress",
        "stress_sub": "Impact estimé sur le capital dans différents scénarios de marché",
        "cenarios": {"Correction légère (-10%)": -0.10, "Correction modérée (-20%)": -0.20,
                     "Bear market (-35%)": -0.35, "Krach sévère (-50%)": -0.50},
        "aviso": "⚠️ VaR = Value at Risk (5e percentile) · Ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Données via Yahoo Finance",
        "periodos": {"1 an": 365, "2 ans": 730, "5 ans": 1825},
    },
    "🇩🇪 Deutsch": {
        "titulo": "Risikoanalyse",
        "subtitulo": "Korrelation zwischen Anlagen, historische Volatilität und Stressszenarien.",
        "sec_config": "⚙️ Portfolio konfigurieren",
        "ticker_label": "Ticker", "btn_add": "➕ Ticker hinzufügen",
        "periodo_label": "Zeitraum", "capital_label": "Gesamtinvestiertes Kapital (€)",
        "btn_analisar": "⚠️ Risiko analysieren",
        "a_carregar": "Daten werden geladen...",
        "erro": "Sie benötigen mindestens 2 gültige Ticker.",
        "vol_titulo": "Volatilität und Risiko je Anlage",
        "var_label": "VaR 95%", "perda_txt": "An einem schlechten Tag (schlechteste 5%) könnten Sie bis zu verlieren",
        "capital_txt": "bei einem Kapital von",
        "risco_alto": "alto", "risco_medio": "medio", "risco_baixo": "baixo",
        "corr_titulo": "Korrelation zwischen Anlagen",
        "corr_sub": "1 = bewegen sich zusammen | -1 = entgegengesetzt | 0 = kein Zusammenhang",
        "dd_titulo": "Historischer Drawdown (Rückgang vom Höchststand)",
        "stress_titulo": "Stressszenario-Simulation",
        "stress_sub": "Geschätzte Auswirkungen auf das Kapital in verschiedenen Marktszenarien",
        "cenarios": {"Leichte Korrektur (-10%)": -0.10, "Moderate Korrektur (-20%)": -0.20,
                     "Bärenmarkt (-35%)": -0.35, "Schwerer Crash (-50%)": -0.50},
        "aviso": "⚠️ VaR = Value at Risk (5. Perzentil) · Stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Daten via Yahoo Finance",
        "periodos": {"1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
    },
    "🇪🇸 Español": {
        "titulo": "Análisis de Riesgo",
        "subtitulo": "Correlación entre activos, volatilidad histórica y simulación de escenarios adversos.",
        "sec_config": "⚙️ Configura la cartera",
        "ticker_label": "Ticker", "btn_add": "➕ Añadir ticker",
        "periodo_label": "Período", "capital_label": "Capital total invertido (€)",
        "btn_analisar": "⚠️ Analizar riesgo",
        "a_carregar": "Cargando datos...",
        "erro": "Necesitas al menos 2 tickers válidos.",
        "vol_titulo": "Volatilidad y riesgo por activo",
        "var_label": "VaR 95%", "perda_txt": "En un mal día (peor 5%), podrías perder hasta",
        "capital_txt": "sobre un capital de",
        "risco_alto": "alto", "risco_medio": "medio", "risco_baixo": "baixo",
        "corr_titulo": "Correlación entre activos",
        "corr_sub": "1 = se mueven juntos | -1 = direcciones opuestas | 0 = sin relación",
        "dd_titulo": "Drawdown histórico (caída desde el pico)",
        "stress_titulo": "Simulación de escenarios adversos",
        "stress_sub": "Impacto estimado en el capital en diferentes escenarios de mercado",
        "cenarios": {"Corrección leve (-10%)": -0.10, "Corrección moderada (-20%)": -0.20,
                     "Bear market (-35%)": -0.35, "Crash severo (-50%)": -0.50},
        "aviso": "⚠️ VaR = Value at Risk (percentil 5%) · No constituye asesoramiento financiero.",
        "rodape": "Freenomics · Datos via Yahoo Finance",
        "periodos": {"1 año": 365, "2 años": 730, "5 años": 1825},
    },
}.get(lang, {})

show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_config"])

if "risco_tickers" not in st.session_state:
    st.session_state.risco_tickers = ["", ""]

remover = None
cols_t = st.columns(min(len(st.session_state.risco_tickers), 4))
for i, t in enumerate(st.session_state.risco_tickers):
    with cols_t[i % 4]:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.session_state.risco_tickers[i] = st.text_input(
                L["ticker_label"], value=t, key=f"risco_t_{i}",
                placeholder="ex: AAPL",
                label_visibility="collapsed" if i > 0 else "visible").upper().strip()
        with c2:
            if len(st.session_state.risco_tickers) > 2:
                if st.button("🗑️", key=f"risco_rm_{i}"): remover = i

if remover is not None:
    st.session_state.risco_tickers.pop(remover); st.rerun()

col_add, col_per, col_cap = st.columns([1, 1, 1])
with col_add:
    if st.button(L["btn_add"]):
        st.session_state.risco_tickers.append(""); st.rerun()
with col_per:
    periodo_opcoes = L["periodos"]
    periodo_label = st.selectbox(L["periodo_label"], list(periodo_opcoes.keys()), index=1)
    dias = periodo_opcoes[periodo_label]
with col_cap:
    capital = st.number_input(L["capital_label"], value=10000, step=500)

analisar = st.button(L["btn_analisar"], type="primary", use_container_width=True)

if not analisar and "risco_resultado" not in st.session_state:
    st.stop()

if analisar:
    st.session_state["risco_resultado"] = {
        "tickers": [t for t in st.session_state.risco_tickers if t],
        "dias": dias, "capital": capital,
    }

cfg     = st.session_state.get("risco_resultado", {})
tickers = cfg.get("tickers", [t for t in st.session_state.risco_tickers if t])
dias    = cfg.get("dias", dias)
capital = cfg.get("capital", capital)

@st.cache_data(ttl=3600)
def carregar(ticker, dias):
    end = datetime.today(); start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

dados = {}
with st.spinner(L["a_carregar"]):
    for t in tickers:
        try:
            df = carregar(t, dias)
            if not df.empty:
                close = df["Close"]
                if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
                dados[t] = close.squeeze()
        except Exception:
            pass

st.markdown("---")

if len(dados) < 2:
    st.error(L["erro"]); st.stop()

precos  = pd.DataFrame(dados).dropna()
retornos = precos.pct_change().dropna()

# ── VOLATILIDADE E VAR ────────────────────────────────────────
st.subheader(L["vol_titulo"])
metricas_r = {}
cols = st.columns(len(dados))
for col, t in zip(cols, dados.keys()):
    if t not in retornos.columns: continue
    vol  = float(retornos[t].std() * np.sqrt(252) * 100)
    var  = float(np.percentile(retornos[t], 5) * 100)
    perda = capital * abs(var) / 100
    nivel = "alto" if vol > 40 else ("medio" if vol > 20 else "baixo")
    metricas_r[t] = {"vol": round(vol, 1), "var": round(var, 2)}
    with col:
        def cartao_r(label, val, sub=None, sub_cor="#FAF8F3"):
            h  = '<div style="background:#0E2A3D;border-radius:10px;padding:14px 16px;border-left:4px solid #C29A4B;margin-bottom:10px;">'
            h += f'<p style="color:#C8D3DA;font-size:0.8rem;margin:0 0 2px 0;">{label}</p>'
            h += f'<p style="color:#FAF8F3;font-size:1.4rem;font-weight:700;margin:0;">{val}</p>'
            if sub: h += f'<p style="color:{sub_cor};font-size:0.85rem;margin:2px 0 0 0;">{sub}</p>'
            h += '</div>'
            return h
        st.markdown(f"**{t}**")
        st.markdown(cartao_r("Vol. anual", f"{vol:.1f}%",
            f"{L['var_label']}: {var:.2f}%/dia"), unsafe_allow_html=True)
        st.markdown(f"""<div class='risco-box risco-{nivel}'>
            {L['perda_txt']} <strong>€{perda:,.0f}</strong> {L['capital_txt']} €{capital:,.0f}.
        </div>""", unsafe_allow_html=True)

# ── CORRELAÇÃO ────────────────────────────────────────────────
st.subheader(L["corr_titulo"])
st.caption(L["corr_sub"])
corr = retornos.corr().round(2)
fig = go.Figure(data=go.Heatmap(
    z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
    colorscale=[[0,"#C29A4B"],[0.5,"#FAF8F3"],[1,"#0E2A3D"]],
    zmin=-1, zmax=1, text=corr.values.round(2), texttemplate="%{text}", showscale=True))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    height=350, margin=dict(l=10,r=10,t=10,b=10))
st.plotly_chart(fig, use_container_width=True)

# ── DRAWDOWN ──────────────────────────────────────────────────
st.subheader(L["dd_titulo"])
fig2 = go.Figure()
for i, t in enumerate(dados.keys()):
    if t not in precos.columns: continue
    pico = precos[t].cummax()
    dd   = (precos[t] - pico) / pico * 100
    fig2.add_trace(go.Scatter(x=precos.index, y=dd.values,
        name=t, line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)], width=1.5)))
fig2.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Drawdown (%)", xaxis_title="Date",
    hovermode="x unified", height=380,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig2, use_container_width=True)

# ── STRESS ────────────────────────────────────────────────────
st.subheader(L["stress_titulo"])
st.caption(L["stress_sub"])
cenarios = L["cenarios"]
cols2 = st.columns(len(cenarios))
for col, (nome, pct) in zip(cols2, cenarios.items()):
    perda = capital * pct
    col.metric(nome, f"€{capital+perda:,.0f}", f"€{perda:,.0f}", delta_color="inverse")

if metricas_r:
    mais_vol = max(metricas_r.items(), key=lambda x: x[1]["vol"])
    insight_risco = (
        f"{mais_vol[0]} é o ativo com maior volatilidade ({mais_vol[1]['vol']}%). "
        f"Num cenário de crash severo (-50%), o capital de €{capital:,.0f} reduziria para €{capital*0.5:,.0f}."
    )
    # Guarda o estado atual desta página para a página de Exportar reutilizar
    st.session_state["export_risco"] = {
        "metricas": metricas_r, "capital": capital, "insight": insight_risco,
    }

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
