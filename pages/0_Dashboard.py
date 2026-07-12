import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import T_DASHBOARD, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_DASHBOARD[lang]

# ── CABEÇALHO ─────────────────────────────────────────────────
st.markdown("### 📊 Freenomics")
st.title(T["titulo"])
st.caption(T["subtitulo"])

# ── TEXTOS ADICIONAIS POR LÍNGUA ─────────────────────────────
TEXTOS = {
    "🇵🇹 Português": {
        "sec_carteira":    "⚙️ Configura a tua carteira",
        "tickers_label":   "Tickers (separados por vírgula)",
        "periodo_label":   "Período de análise",
        "preco_compra":    "Preço médio de compra ($)",
        "n_acoes":         "Nº de ações",
        "btn_analisar":    "📊 Analisar carteira",
        "a_carregar":      "A carregar dados de mercado...",
        "erro_tickers":    "Não foi possível carregar dados para alguns tickers.",
        "carteira_real":   "💼 A tua carteira real",
        "preco_arrow":     "Preço compra → atual",
        "ganho_label":     "Ganho / Perda",
        "valor_label":     "Valor atual",
        "investido":       "investido",
        "resumo":          "RESUMO DA CARTEIRA",
        "tot_investido":   "Total investido",
        "tot_atual":       "Valor atual",
        "tot_ganho":       "Ganho / Perda total",
        "fx_nota":         "Taxa de câmbio",
        "mostrar_usd":     "Mostrar em USD ($)",
        "grafico_titulo":  "Evolução comparada (base 100)",
        "insights_titulo": "📝 Leitura automática dos resultados",
        "api_label":       "🤖 Anthropic API Key (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info":        "Com API key, os insights são gerados por IA.",
        "aviso":           "⚠️ Análise gerada automaticamente — não constitui aconselhamento financeiro.",
        "rodape":          "Freenomics · Dados via Yahoo Finance",
        "periodos":        {"6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825},
        "queda_maxima":    "de queda máxima",
        "caption_base100": "💡 **Base 100:** todos os ativos começam no mesmo ponto para comparar performance relativa. Ex: 180 = subiu 80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** a linha tracejada representa o S&P 500. Serve para perceber se a tua carteira está a superar o mercado.",
    },
    "🇬🇧 English": {
        "sec_carteira":    "⚙️ Configure your portfolio",
        "tickers_label":   "Tickers (comma-separated)",
        "periodo_label":   "Analysis period",
        "preco_compra":    "Average purchase price ($)",
        "n_acoes":         "Number of shares",
        "btn_analisar":    "📊 Analyse portfolio",
        "a_carregar":      "Loading market data...",
        "erro_tickers":    "Could not load data for some tickers.",
        "carteira_real":   "💼 Your real portfolio",
        "preco_arrow":     "Purchase → current price",
        "ganho_label":     "Gain / Loss",
        "valor_label":     "Current value",
        "investido":       "invested",
        "resumo":          "PORTFOLIO SUMMARY",
        "tot_investido":   "Total invested",
        "tot_atual":       "Current value",
        "tot_ganho":       "Total gain / loss",
        "fx_nota":         "Exchange rate",
        "mostrar_usd":     "Show in USD ($)",
        "grafico_titulo":  "Comparative evolution (base 100)",
        "insights_titulo": "📝 Automatic reading of results",
        "api_label":       "🤖 Anthropic API Key (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info":        "With an API key, insights are AI-generated.",
        "aviso":           "⚠️ Automatically generated analysis — does not constitute financial advice.",
        "rodape":          "Freenomics · Data via Yahoo Finance",
        "periodos":        {"6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825},
        "queda_maxima":    "max drawdown reached",
        "caption_base100": "💡 **Base 100:** all assets start at the same point to compare relative performance. E.g. 180 = rose 80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** the dashed line represents the S&P 500. It shows whether your portfolio is outperforming the market.",
    },
    "🇫🇷 Français": {
        "sec_carteira":    "⚙️ Configurez votre portefeuille",
        "tickers_label":   "Tickers (séparés par virgule)",
        "periodo_label":   "Période d'analyse",
        "preco_compra":    "Prix d'achat moyen ($)",
        "n_acoes":         "Nombre d'actions",
        "btn_analisar":    "📊 Analyser le portefeuille",
        "a_carregar":      "Chargement des données...",
        "erro_tickers":    "Impossible de charger les données pour certains tickers.",
        "carteira_real":   "💼 Votre portefeuille réel",
        "preco_arrow":     "Prix achat → actuel",
        "ganho_label":     "Gain / Perte",
        "valor_label":     "Valeur actuelle",
        "investido":       "investi",
        "resumo":          "RÉSUMÉ DU PORTEFEUILLE",
        "tot_investido":   "Total investi",
        "tot_atual":       "Valeur actuelle",
        "tot_ganho":       "Gain / Perte total",
        "fx_nota":         "Taux de change",
        "mostrar_usd":     "Afficher en USD ($)",
        "grafico_titulo":  "Évolution comparée (base 100)",
        "insights_titulo": "📝 Lecture automatique des résultats",
        "api_label":       "🤖 Clé API Anthropic (optionnel)",
        "api_placeholder": "sk-ant-...",
        "api_info":        "Avec une clé API, les insights sont générés par IA.",
        "aviso":           "⚠️ Analyse générée automatiquement — ne constitue pas un conseil financier.",
        "rodape":          "Freenomics · Données via Yahoo Finance",
        "periodos":        {"6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825},
        "queda_maxima":    "de baisse maximale",
        "caption_base100": "💡 **Base 100 :** tous les actifs partent du même point. Ex : 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark) :** la ligne en pointillés représente le S&P 500.",
    },
    "🇩🇪 Deutsch": {
        "sec_carteira":    "⚙️ Portfolio konfigurieren",
        "tickers_label":   "Ticker (kommagetrennt)",
        "periodo_label":   "Analysezeitraum",
        "preco_compra":    "Durchschn. Kaufpreis ($)",
        "n_acoes":         "Anzahl Aktien",
        "btn_analisar":    "📊 Portfolio analysieren",
        "a_carregar":      "Marktdaten werden geladen...",
        "erro_tickers":    "Daten für einige Ticker konnten nicht geladen werden.",
        "carteira_real":   "💼 Ihr reales Portfolio",
        "preco_arrow":     "Kaufpreis → aktuell",
        "ganho_label":     "Gewinn / Verlust",
        "valor_label":     "Aktueller Wert",
        "investido":       "investiert",
        "resumo":          "PORTFOLIO-ZUSAMMENFASSUNG",
        "tot_investido":   "Gesamt investiert",
        "tot_atual":       "Aktueller Wert",
        "tot_ganho":       "Gesamtgewinn / -verlust",
        "fx_nota":         "Wechselkurs",
        "mostrar_usd":     "In USD anzeigen ($)",
        "grafico_titulo":  "Vergleichende Entwicklung (Basis 100)",
        "insights_titulo": "📝 Automatische Auswertung",
        "api_label":       "🤖 Anthropic API-Schlüssel (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info":        "Mit API-Schlüssel werden Insights KI-generiert.",
        "aviso":           "⚠️ Automatisch generierte Analyse — stellt keine Finanzberatung dar.",
        "rodape":          "Freenomics · Daten via Yahoo Finance",
        "periodos":        {"6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
        "queda_maxima":    "maximaler Rückgang",
        "caption_base100": "💡 **Basis 100:** Alle Anlagen starten am selben Punkt. Bsp.: 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (Benchmark):** Die gestrichelte Linie zeigt den S&P 500.",
    },
    "🇪🇸 Español": {
        "sec_carteira":    "⚙️ Configura tu cartera",
        "tickers_label":   "Tickers (separados por coma)",
        "periodo_label":   "Período de análisis",
        "preco_compra":    "Precio medio de compra ($)",
        "n_acoes":         "Nº de acciones",
        "btn_analisar":    "📊 Analizar cartera",
        "a_carregar":      "Cargando datos de mercado...",
        "erro_tickers":    "No se pudieron cargar datos para algunos tickers.",
        "carteira_real":   "💼 Tu cartera real",
        "preco_arrow":     "Precio compra → actual",
        "ganho_label":     "Ganancia / Pérdida",
        "valor_label":     "Valor actual",
        "investido":       "invertido",
        "resumo":          "RESUMEN DE CARTERA",
        "tot_investido":   "Total invertido",
        "tot_atual":       "Valor actual",
        "tot_ganho":       "Ganancia / Pérdida total",
        "fx_nota":         "Tipo de cambio",
        "mostrar_usd":     "Mostrar en USD ($)",
        "grafico_titulo":  "Evolución comparada (base 100)",
        "insights_titulo": "📝 Lectura automática de resultados",
        "api_label":       "🤖 Clave API Anthropic (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info":        "Con clave API, los insights son generados por IA.",
        "aviso":           "⚠️ Análisis generado automáticamente — no constituye asesoramiento financiero.",
        "rodape":          "Freenomics · Datos via Yahoo Finance",
        "periodos":        {"6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825},
        "queda_maxima":    "de caída máxima",
        "caption_base100": "💡 **Base 100:** todos los activos parten del mismo punto. Ej: 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** la línea discontinua representa el S&P 500.",
    },
}
L = TEXTOS.get(lang, TEXTOS["🇬🇧 English"])

# ── FORMULÁRIO PRINCIPAL ──────────────────────────────────────
st.header(L["sec_carteira"])

col_t, col_p = st.columns([2, 1])
with col_t:
    tickers_input = st.text_input(L["tickers_label"], value="SPY, SOFI",
                                   placeholder="Ex: AAPL, TSLA, NVDA")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
with col_p:
    periodo_opcoes = L["periodos"]
    periodo_label = st.selectbox(L["periodo_label"], list(periodo_opcoes.keys()), index=2)
    dias = periodo_opcoes[periodo_label]

# Inputs de compra por ticker
st.markdown("**Detalhe por ativo:**" if lang == "🇵🇹 Português" else "**Asset detail:**")
compras = {}
if tickers:
    cols_form = st.columns(len(tickers))
    for col, t in zip(cols_form, tickers):
        with col:
            st.markdown(f"**{t}**")
            pc = st.number_input(L["preco_compra"], min_value=0.0, value=0.0,
                                  step=0.01, format="%.2f", key=f"pc_{t}")
            na = st.number_input(L["n_acoes"], min_value=0.0, value=0.0,
                                  step=1.0, format="%.0f", key=f"na_{t}")
            if pc > 0 and na > 0:
                compras[t] = {"preco_compra": pc, "n_acoes": na}

col_api, col_usd = st.columns([3, 1])
with col_api:
    api_key = st.text_input(L["api_label"], type="password",
                             placeholder=L["api_placeholder"],
                             help=L["api_info"])
with col_usd:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    mostrar_usd = st.toggle(L["mostrar_usd"], value=False)

analisar = st.button(L["btn_analisar"], type="primary", use_container_width=True)

if not analisar and "freenomics_dados" not in st.session_state:
    st.stop()

# ── DADOS ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar_dados(ticker, dias):
    end = datetime.today()
    start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

@st.cache_data(ttl=3600)
def get_eurusd():
    try:
        fx = yf.download("EURUSD=X", period="1d", progress=False)
        close = fx["Close"]
        if isinstance(close, pd.DataFrame):
            close = close.iloc[:, 0]
        return float(close.iloc[-1])
    except Exception:
        return 1.08

if analisar:
    st.session_state["freenomics_dados"] = {
        "tickers": tickers, "dias": dias,
        "periodo_label": periodo_label, "compras": compras
    }

cfg = st.session_state.get("freenomics_dados", {})
tickers      = cfg.get("tickers", tickers)
dias         = cfg.get("dias", dias)
periodo_label = cfg.get("periodo_label", periodo_label)
compras      = cfg.get("compras", compras)

dados = {}
with st.spinner(L["a_carregar"]):
    for t in tickers:
        try:
            df = carregar_dados(t, dias)
            if not df.empty:
                dados[t] = df
        except Exception:
            pass

if not dados:
    st.error(L["erro_tickers"])
    st.stop()

eurusd  = get_eurusd()
usdeur  = 1 / eurusd
simbolo = "$" if mostrar_usd else "€"
fator   = 1.0 if mostrar_usd else usdeur

# ── MÉTRICAS E PREÇOS ATUAIS ──────────────────────────────────
def calcular_metricas(df):
    precos = df["Close"]
    if isinstance(precos, pd.DataFrame):
        precos = precos.iloc[:, 0]
    precos = precos.squeeze()
    ret  = float((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
    rd   = precos.pct_change().dropna()
    vol  = float(rd.std() * np.sqrt(252) * 100)
    pico = precos.cummax()
    dd   = float(((precos - pico) / pico).min() * 100)
    sh   = float((rd.mean() / rd.std()) * np.sqrt(252)) if rd.std().item() != 0 else 0.0
    preco_atual = float(precos.iloc[-1])
    return {"retorno_total": round(ret,2), "volatilidade": round(vol,2),
            "max_drawdown": round(dd,2), "sharpe": round(sh,2),
            "preco_atual": round(preco_atual, 2)}

metricas = {t: calcular_metricas(df) for t, df in dados.items()}

# ── FUNÇÕES DE CARTÃO ─────────────────────────────────────────
def cor(valor):
    return "#4CAF50" if valor >= 0 else "#F44336"

def cartao(label, valor_str, euros_str=None, euros_cor="#4CAF50"):
    html  = '<div style="background:#0E2A3D;border-radius:10px;padding:16px 18px;'
    html += 'border-left:4px solid #C29A4B;margin-bottom:12px;">'
    html += '<p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 4px 0;">' + label + '</p>'
    html += '<p style="color:#FAF8F3;font-size:1.8rem;font-weight:700;margin:0;">' + valor_str + '</p>'
    if euros_str:
        html += '<p style="color:' + euros_cor + ';font-size:0.95rem;margin:4px 0 0 0;">' + euros_str + '</p>'
    html += '</div>'
    return html

st.markdown("---")

# ── CARTEIRA REAL (se preços introduzidos) ────────────────────
if compras:
    st.subheader(L["carteira_real"])
    total_inv = 0
    total_atu = 0
    rows = []

    for t, c in compras.items():
        if t not in metricas:
            continue
        pa  = metricas[t]["preco_atual"]
        pc  = c["preco_compra"]
        na  = c["n_acoes"]
        inv_usd = pc * na
        atu_usd = pa * na
        gan_usd = atu_usd - inv_usd
        pct     = ((pa / pc) - 1) * 100 if pc > 0 else 0
        rows.append({"ticker": t, "pc": pc, "pa": pa,
                     "inv": inv_usd * fator, "atu": atu_usd * fator,
                     "gan": gan_usd * fator, "pct": pct})
        total_inv += inv_usd * fator
        total_atu += atu_usd * fator

    cols_r = st.columns(len(rows))
    for col, r in zip(cols_r, rows):
        with col:
            st.markdown(f"**{r['ticker']}**")
            st.markdown(cartao(L["preco_arrow"],
                f"${r['pc']:.2f} → ${r['pa']:.2f}"), unsafe_allow_html=True)
            st.markdown(cartao(f"{L['ganho_label']} ({simbolo})",
                f"{simbolo}{r['gan']:+,.0f}",
                euros_str=f"{r['pct']:+.1f}%",
                euros_cor=cor(r['gan'])), unsafe_allow_html=True)
            st.markdown(cartao(f"{L['valor_label']} ({simbolo})",
                f"{simbolo}{r['atu']:,.0f}",
                euros_str=f"{L['investido']}: {simbolo}{r['inv']:,.0f}",
                euros_cor="#C8D3DA"), unsafe_allow_html=True)

    gan_total = total_atu - total_inv
    gan_pct   = (gan_total / total_inv * 100) if total_inv > 0 else 0
    fx_str    = f"1 USD = {simbolo}{fator:.4f}" if not mostrar_usd else "USD"

    st.markdown(f"""
    <div style="background:#0E2A3D;border-radius:10px;padding:20px 24px;
                border:2px solid #C29A4B;margin:12px 0;">
        <p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 12px 0;">{L['resumo']}</p>
        <div style="display:flex;gap:40px;flex-wrap:wrap;">
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_investido']}</p>
                 <p style="color:#FAF8F3;font-size:1.4rem;font-weight:700;margin:0;">{simbolo}{total_inv:,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_atual']}</p>
                 <p style="color:#FAF8F3;font-size:1.4rem;font-weight:700;margin:0;">{simbolo}{total_atu:,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_ganho']}</p>
                 <p style="color:{cor(gan_total)};font-size:1.4rem;font-weight:700;margin:0;">{simbolo}{gan_total:+,.0f} ({gan_pct:+.1f}%)</p></div>
        </div>
        <p style="color:#6B7280;font-size:0.75rem;margin:10px 0 0 0;">{L['fx_nota']}: {fx_str} · Yahoo Finance</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# ── GRÁFICO ───────────────────────────────────────────────────
st.subheader(L["grafico_titulo"])
fig = go.Figure()
for i, (t, df) in enumerate(dados.items()):
    close = df["Close"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
    close = close.squeeze()
    norm = (close / close.iloc[0]) * 100
    fig.add_trace(go.Scatter(x=df.index, y=norm.values.flatten(),
        name=t, line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)], width=2.5)))

if "SPY" not in tickers:
    try:
        df_spy = carregar_dados("SPY", dias)
        if not df_spy.empty:
            c = df_spy["Close"]
            if isinstance(c, pd.DataFrame): c = c.iloc[:, 0]
            c = c.squeeze()
            norm_spy = (c / c.iloc[0]) * 100
            fig.add_trace(go.Scatter(x=df_spy.index, y=norm_spy.values.flatten(),
                name="S&P 500 (benchmark)",
                line=dict(color="#888888", width=1.5, dash="dash"), opacity=0.7))
    except Exception:
        pass

fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Value (base 100)", xaxis_title="Date",
    hovermode="x unified", height=440,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)
st.caption(L["caption_base100"])
st.caption(L["caption_benchmark"])

# ── INSIGHTS ──────────────────────────────────────────────────
st.subheader(L["insights_titulo"])

LINGUA_NOME = {
    "🇵🇹 Português": "português europeu", "🇬🇧 English": "English",
    "🇫🇷 Français": "français", "🇩🇪 Deutsch": "Deutsch", "🇪🇸 Español": "español",
}

def gerar_insights_api(metricas, periodo_label, lang, api_key, compras, fator, simbolo):
    lingua = LINGUA_NOME.get(lang, "português")
    linhas = []
    for t, m in metricas.items():
        linha = f"- {t}: retorno {m['retorno_total']}%, volatilidade {m['volatilidade']}%, drawdown {m['max_drawdown']}%, Sharpe {m['sharpe']}"
        if t in compras:
            pc = compras[t]["preco_compra"]
            na = compras[t]["n_acoes"]
            gan = (m["preco_atual"] - pc) * na * fator
            pct = ((m["preco_atual"] / pc) - 1) * 100 if pc > 0 else 0
            linha += f", ganho real: {simbolo}{gan:+,.0f} ({pct:+.1f}%)"
        linhas.append(linha)

    prompt = f"""És um consultor financeiro a analisar uma carteira de investimentos para um investidor individual.

Período: {periodo_label}
Dados:
{chr(10).join(linhas)}

Escreve uma análise em {lingua} com 3-4 parágrafos curtos que:
1. Contextualiza a performance dos ativos de forma clara
2. Comenta o risco (volatilidade e drawdown) em linguagem acessível
3. Se houver dados reais de compra, comenta o ganho/perda em termos concretos
4. Termina com uma reflexão prática para o investidor

Tom direto, como um amigo que percebe de finanças. Sem bullet points. Sem títulos."""

    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": "claude-haiku-4-5-20251001", "max_tokens": 600,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=30)
        if r.status_code == 200:
            return r.json()["content"][0]["text"], True
    except Exception:
        pass
    return None, False

def fallback_insights(metricas, periodo_label, T):
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
        mv = sorted(metricas.items(), key=lambda x: x[1]["volatilidade"], reverse=True)[0]
        frases.append(T["insight_volatil"](mv[0], mv[1]["volatilidade"]))
    for t, m in metricas.items():
        if m["max_drawdown"] < -20:
            frases.append(T["insight_drawdown"](t, m["max_drawdown"]))
    ms = sorted(metricas.items(), key=lambda x: x[1]["sharpe"], reverse=True)[0]
    if ms[1]["sharpe"] > 0:
        frases.append(T["insight_sharpe"](ms[0]))
    return frases

def renderizar(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)

if api_key:
    with st.spinner("🤖 A gerar análise com IA..."):
        texto_ai, sucesso = gerar_insights_api(
            metricas, periodo_label, lang, api_key, compras, fator, simbolo)
    if sucesso and texto_ai:
        html = renderizar(texto_ai).replace("\n\n", "<br><br>")
        st.markdown(f"<div class='insight-box'>{html}</div>", unsafe_allow_html=True)
        st.caption("✨ " + L["aviso"])
    else:
        st.warning("API indisponível. A usar análise automática.")
        for f in fallback_insights(metricas, periodo_label, T):
            st.markdown(f"<div class='insight-box'>{renderizar(f)}</div>", unsafe_allow_html=True)
else:
    for f in fallback_insights(metricas, periodo_label, T):
        st.markdown(f"<div class='insight-box'>{renderizar(f)}</div>", unsafe_allow_html=True)
    st.info(f"💡 {L['api_info']}")

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
