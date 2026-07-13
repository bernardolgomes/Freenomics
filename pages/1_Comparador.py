import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Comparador de Carteiras",
        "subtitulo": "Compara múltiplas estratégias de investimento e descobre qual teria performado melhor.",
        "sec_config": "⚙️ Configura as carteiras",
        "periodo_label": "Período de análise",
        "carteira": "📁 Carteira",
        "ticker_label": "Ticker", "moeda_label": "Moeda",
        "preco_label": "Preço médio de compra", "acoes_label": "Nº de ações",
        "btn_add_ativo": "➕ Adicionar ativo",
        "btn_add_carteira": "➕ Adicionar carteira",
        "btn_remover_carteira": "🗑️ Remover carteira",
        "btn_comparar": "📊 Comparar carteiras",
        "min_carteiras": "Precisas de pelo menos 2 carteiras para comparar.",
        "a_carregar": "A carregar dados...",
        "erro": "Não foi possível carregar dados.",
        "vencedor": "🏆 Melhor performance no período",
        "retorno": "Retorno total", "vol": "Volatilidade anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final",
        "ganho_label": "Ganho / Perda", "valor_label": "Valor atual",
        "investido": "investido",
        "tot_inv": "Total investido", "tot_atu": "Valor atual",
        "tot_gan": "Ganho / Perda total", "fx_nota": "Taxa de câmbio",
        "mostrar_usd": "Mostrar em USD ($)",
        "grafico": "Evolução comparada (base 100)",
        "analise": "📝 Análise comparativa",
        "api_label": "🤖 Anthropic API Key (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Com API key, a análise é gerada por IA.",
        "aviso": "⚠️ Análise gerada automaticamente — não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Dados via Yahoo Finance",
        "caption_base100": "💡 **Base 100:** todos os ativos começam no mesmo ponto para comparar performance relativa.",
        "periodos": {"1 mês": 30, "3 meses": 90, "6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825, "10 anos": 3650, "20 anos": 7300},
        "letras": ["A", "B", "C", "D", "E", "F"],
    },
    "🇬🇧 English": {
        "titulo": "Portfolio Comparator",
        "subtitulo": "Compare multiple investment strategies and find out which would have performed better.",
        "sec_config": "⚙️ Configure portfolios",
        "periodo_label": "Analysis period",
        "carteira": "📁 Portfolio",
        "ticker_label": "Ticker", "moeda_label": "Currency",
        "preco_label": "Average purchase price", "acoes_label": "Number of shares",
        "btn_add_ativo": "➕ Add asset",
        "btn_add_carteira": "➕ Add portfolio",
        "btn_remover_carteira": "🗑️ Remove portfolio",
        "btn_comparar": "📊 Compare portfolios",
        "min_carteiras": "You need at least 2 portfolios to compare.",
        "a_carregar": "Loading data...",
        "erro": "Could not load data.",
        "vencedor": "🏆 Best performance in the period",
        "retorno": "Total return", "vol": "Ann. volatility",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (approx.)",
        "valor_final": "Final value",
        "ganho_label": "Gain / Loss", "valor_label": "Current value",
        "investido": "invested",
        "tot_inv": "Total invested", "tot_atu": "Current value",
        "tot_gan": "Total gain / loss", "fx_nota": "Exchange rate",
        "mostrar_usd": "Show in USD ($)",
        "grafico": "Comparative evolution (base 100)",
        "analise": "📝 Comparative analysis",
        "api_label": "🤖 Anthropic API Key (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "With an API key, analysis is AI-generated.",
        "aviso": "⚠️ Automatically generated — does not constitute financial advice.",
        "rodape": "Freenomics · Data via Yahoo Finance",
        "caption_base100": "💡 **Base 100:** all assets start at the same point to compare relative performance.",
        "periodos": {"1 month": 30, "3 months": 90, "6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825, "10 years": 3650, "20 years": 7300},
        "letras": ["A", "B", "C", "D", "E", "F"],
    },
    "🇫🇷 Français": {
        "titulo": "Comparateur de Portefeuilles",
        "subtitulo": "Comparez plusieurs stratégies d'investissement.",
        "sec_config": "⚙️ Configurez les portefeuilles",
        "periodo_label": "Période d'analyse",
        "carteira": "📁 Portefeuille",
        "ticker_label": "Ticker", "moeda_label": "Devise",
        "preco_label": "Prix d'achat moyen", "acoes_label": "Nombre d'actions",
        "btn_add_ativo": "➕ Ajouter un actif",
        "btn_add_carteira": "➕ Ajouter un portefeuille",
        "btn_remover_carteira": "🗑️ Supprimer le portefeuille",
        "btn_comparar": "📊 Comparer les portefeuilles",
        "min_carteiras": "Vous avez besoin d'au moins 2 portefeuilles pour comparer.",
        "a_carregar": "Chargement...",
        "erro": "Impossible de charger les données.",
        "vencedor": "🏆 Meilleure performance sur la période",
        "retorno": "Rendement total", "vol": "Volatilité ann.",
        "drawdown": "Drawdown max", "sharpe": "Sharpe (approx.)",
        "valor_final": "Valeur finale",
        "ganho_label": "Gain / Perte", "valor_label": "Valeur actuelle",
        "investido": "investi",
        "tot_inv": "Total investi", "tot_atu": "Valeur actuelle",
        "tot_gan": "Gain / Perte total", "fx_nota": "Taux de change",
        "mostrar_usd": "Afficher en USD ($)",
        "grafico": "Évolution comparée (base 100)",
        "analise": "📝 Analyse comparative",
        "api_label": "🤖 Clé API Anthropic (optionnel)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Avec une clé API, l'analyse est générée par IA.",
        "aviso": "⚠️ Analyse automatique — ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Données via Yahoo Finance",
        "caption_base100": "💡 **Base 100 :** tous les actifs partent du même point.",
        "periodos": {"1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825, "10 ans": 3650, "20 ans": 7300},
        "letras": ["A", "B", "C", "D", "E", "F"],
    },
    "🇩🇪 Deutsch": {
        "titulo": "Portfolio-Vergleich",
        "subtitulo": "Vergleichen Sie mehrere Anlagestrategien.",
        "sec_config": "⚙️ Portfolios konfigurieren",
        "periodo_label": "Analysezeitraum",
        "carteira": "📁 Portfolio",
        "ticker_label": "Ticker", "moeda_label": "Währung",
        "preco_label": "Durchschn. Kaufpreis", "acoes_label": "Anzahl Aktien",
        "btn_add_ativo": "➕ Anlage hinzufügen",
        "btn_add_carteira": "➕ Portfolio hinzufügen",
        "btn_remover_carteira": "🗑️ Portfolio entfernen",
        "btn_comparar": "📊 Portfolios vergleichen",
        "min_carteiras": "Sie benötigen mindestens 2 Portfolios zum Vergleich.",
        "a_carregar": "Daten werden geladen...",
        "erro": "Daten konnten nicht geladen werden.",
        "vencedor": "🏆 Beste Performance im Zeitraum",
        "retorno": "Gesamtrendite", "vol": "Jährl. Volatilität",
        "drawdown": "Max. Drawdown", "sharpe": "Sharpe (ca.)",
        "valor_final": "Endwert",
        "ganho_label": "Gewinn / Verlust", "valor_label": "Aktueller Wert",
        "investido": "investiert",
        "tot_inv": "Gesamt investiert", "tot_atu": "Aktueller Wert",
        "tot_gan": "Gesamtgewinn / -verlust", "fx_nota": "Wechselkurs",
        "mostrar_usd": "In USD anzeigen ($)",
        "grafico": "Vergleichende Entwicklung (Basis 100)",
        "analise": "📝 Vergleichende Analyse",
        "api_label": "🤖 Anthropic API-Schlüssel (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Mit API-Schlüssel wird die Analyse KI-generiert.",
        "aviso": "⚠️ Automatisch generiert — stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Daten via Yahoo Finance",
        "caption_base100": "💡 **Basis 100:** Alle Anlagen starten am selben Punkt.",
        "periodos": {"1 Monat": 30, "3 Monate": 90, "6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825, "10 Jahre": 3650, "20 Jahre": 7300},
        "letras": ["A", "B", "C", "D", "E", "F"],
    },
    "🇪🇸 Español": {
        "titulo": "Comparador de Carteras",
        "subtitulo": "Compara múltiples estrategias de inversión.",
        "sec_config": "⚙️ Configura las carteras",
        "periodo_label": "Período de análisis",
        "carteira": "📁 Cartera",
        "ticker_label": "Ticker", "moeda_label": "Divisa",
        "preco_label": "Precio medio de compra", "acoes_label": "Nº de acciones",
        "btn_add_ativo": "➕ Añadir activo",
        "btn_add_carteira": "➕ Añadir cartera",
        "btn_remover_carteira": "🗑️ Eliminar cartera",
        "btn_comparar": "📊 Comparar carteras",
        "min_carteiras": "Necesitas al menos 2 carteras para comparar.",
        "a_carregar": "Cargando datos...",
        "erro": "No se pudieron cargar datos.",
        "vencedor": "🏆 Mejor rendimiento en el período",
        "retorno": "Rendimiento total", "vol": "Volatilidad anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final",
        "ganho_label": "Ganancia / Pérdida", "valor_label": "Valor actual",
        "investido": "invertido",
        "tot_inv": "Total invertido", "tot_atu": "Valor actual",
        "tot_gan": "Ganancia / Pérdida total", "fx_nota": "Tipo de cambio",
        "mostrar_usd": "Mostrar en USD ($)",
        "grafico": "Evolución comparada (base 100)",
        "analise": "📝 Análisis comparativo",
        "api_label": "🤖 Clave API Anthropic (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Con clave API, el análisis es generado por IA.",
        "aviso": "⚠️ Análisis automático — no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Datos via Yahoo Finance",
        "caption_base100": "💡 **Base 100:** todos los activos parten del mismo punto.",
        "periodos": {"1 mes": 30, "3 meses": 90, "6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825, "10 años": 3650, "20 años": 7300},
        "letras": ["A", "B", "C", "D", "E", "F"],
    },
}.get(lang, {})

# ── CABEÇALHO ─────────────────────────────────────────────────
show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── INICIALIZAR LISTA DE CARTEIRAS ────────────────────────────
if "comp_portfolios" not in st.session_state:
    st.session_state.comp_portfolios = [
        [{"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0}],
        [{"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0}],
    ]

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_config"])

periodo_opcoes = L["periodos"]
periodo_label  = st.radio(L["periodo_label"], list(periodo_opcoes.keys()), index=4, horizontal=True)
dias = periodo_opcoes[periodo_label]

st.markdown("---")

letras       = L["letras"]
remover_port = None
remover_ativ = None

# Mostrar carteiras em colunas (max 3 por linha)
n_ports = len(st.session_state.comp_portfolios)
cols_per_row = min(n_ports, 3)
port_cols = st.columns(cols_per_row)

for pi, ativos in enumerate(st.session_state.comp_portfolios):
    letra = letras[pi] if pi < len(letras) else str(pi+1)
    with port_cols[pi % cols_per_row]:
        # Cabeçalho da carteira
        c_title, c_del = st.columns([4, 1])
        with c_title:
            st.markdown(f"**{L['carteira']} {letra}**")
        with c_del:
            if n_ports > 2 and st.button("🗑️", key=f"del_port_{pi}", help=L["btn_remover_carteira"]):
                remover_port = pi

        # Ativos da carteira
        rem_ativ_local = None
        for ai, ativo in enumerate(ativos):
            c1, c2 = st.columns([3, 1])
            with c1:
                st.session_state.comp_portfolios[pi][ai]["ticker"] = st.text_input(
                    L["ticker_label"], value=ativo["ticker"],
                    key=f"p{pi}_t{ai}", placeholder="ex: AAPL",
                    label_visibility="collapsed" if ai > 0 else "visible"
                ).upper().strip()
            with c2:
                st.session_state.comp_portfolios[pi][ai]["moeda"] = st.selectbox(
                    L["moeda_label"], ["USD", "EUR"],
                    index=0 if ativo["moeda"] == "USD" else 1,
                    key=f"p{pi}_m{ai}",
                    label_visibility="collapsed" if ai > 0 else "visible"
                )
            c3, c4, c5 = st.columns([2, 2, 0.5])
            with c3:
                sim = "$" if ativo["moeda"] == "USD" else "€"
                st.session_state.comp_portfolios[pi][ai]["preco"] = st.number_input(
                    f"{L['preco_label']} ({sim})", value=float(ativo["preco"]),
                    min_value=0.0, step=0.01, format="%.2f",
                    key=f"p{pi}_pc{ai}", label_visibility="collapsed")
            with c4:
                st.session_state.comp_portfolios[pi][ai]["acoes"] = st.number_input(
                    L["acoes_label"], value=float(ativo["acoes"]),
                    min_value=0.0, step=1.0, format="%.0f",
                    key=f"p{pi}_na{ai}", label_visibility="collapsed")
            with c5:
                if len(ativos) > 1 and st.button("✕", key=f"p{pi}_ra{ai}"):
                    rem_ativ_local = ai

        if rem_ativ_local is not None:
            st.session_state.comp_portfolios[pi].pop(rem_ativ_local)
            st.rerun()

        if st.button(L["btn_add_ativo"], key=f"add_ativ_{pi}"):
            st.session_state.comp_portfolios[pi].append(
                {"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0})
            st.rerun()

if remover_port is not None:
    st.session_state.comp_portfolios.pop(remover_port)
    st.rerun()

st.markdown("---")

# Botão adicionar carteira
col_add, col_empty = st.columns([2, 3])
with col_add:
    if len(st.session_state.comp_portfolios) < 6:
        if st.button(L["btn_add_carteira"], use_container_width=True):
            st.session_state.comp_portfolios.append(
                [{"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0}])
            st.rerun()

col_api, col_usd = st.columns([3, 1])
with col_api:
    api_key = st.text_input(L["api_label"], type="password",
                             placeholder=L["api_placeholder"], help=L["api_info"])
with col_usd:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    mostrar_usd = st.toggle(L["mostrar_usd"], value=False)

comparar = st.button(L["btn_comparar"], type="primary", use_container_width=True)

if not comparar and "comp_resultado" not in st.session_state:
    st.stop()

if comparar:
    if len(st.session_state.comp_portfolios) < 2:
        st.warning(L["min_carteiras"])
        st.stop()
    st.session_state["comp_resultado"] = {
        "portfolios": [[a.copy() for a in p] for p in st.session_state.comp_portfolios],
        "dias": dias, "periodo_label": periodo_label,
    }

cfg       = st.session_state.get("comp_resultado", {})
portfolios = cfg.get("portfolios", st.session_state.comp_portfolios)
dias      = cfg.get("dias", dias)
periodo_label = cfg.get("periodo_label", periodo_label)

# ── DADOS ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar(ticker, dias):
    end = datetime.today(); start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

@st.cache_data(ttl=3600)
def get_eurusd():
    try:
        fx = yf.download("EURUSD=X", period="1d", progress=False)
        close = fx["Close"]
        if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
        return float(close.squeeze().iloc[-1])
    except Exception:
        return 1.08

todos_tickers = list({a["ticker"] for p in portfolios for a in p if a["ticker"]})
dados = {}
with st.spinner(L["a_carregar"]):
    for t in todos_tickers:
        try:
            df = carregar(t, dias)
            if not df.empty: dados[t] = df
        except Exception:
            pass

if not dados:
    st.error(L["erro"]); st.stop()

eurusd = get_eurusd()
usdeur = 1 / eurusd
sim_d  = "$" if mostrar_usd else "€"
def to_eur(usd): return usd * usdeur
def to_disp(eur): return eur * eurusd if mostrar_usd else eur

def retorno_medio(ativos):
    series = []
    for a in ativos:
        t = a["ticker"]
        if t not in dados: continue
        c = dados[t]["Close"]
        if isinstance(c, pd.DataFrame): c = c.iloc[:, 0]
        c = c.squeeze()
        series.append(c / c.iloc[0])
    if not series: return None
    return pd.concat(series, axis=1).mean(axis=1)

def metricas_serie(serie):
    d = serie.pct_change().dropna()
    return {
        "retorno": round(float((serie.iloc[-1]-1)*100), 2),
        "vol":     round(float(d.std()*np.sqrt(252)*100), 2),
        "dd":      round(float(((serie-serie.cummax())/serie.cummax()).min()*100), 2),
        "sharpe":  round(float((d.mean()/d.std())*np.sqrt(252)) if d.std().item()!=0 else 0, 2),
    }

resultados = []
for pi, ativos in enumerate(portfolios):
    letra = letras[pi] if pi < len(letras) else str(pi+1)
    ret   = retorno_medio(ativos)
    if ret is None: continue
    nomes = [a["ticker"] for a in ativos if a["ticker"]]
    resultados.append({
        "letra": letra,
        "nome": f"{L['carteira']} {letra} — {' + '.join(nomes)}",
        "nome_curto": f"{L['carteira']} {letra}",
        "ativos": ativos,
        "retorno": ret,
        "metricas": metricas_serie(ret),
    })

if len(resultados) < 2:
    st.error(L["erro"]); st.stop()

def cor(v): return "#4CAF50" if v >= 0 else "#F44336"

def cartao(label, valor_str, euros_str=None, euros_cor="#4CAF50"):
    html  = '<div style="background:#0E2A3D;border-radius:10px;padding:14px 16px;'
    html += 'border-left:4px solid #C29A4B;margin-bottom:10px;">'
    html += '<p style="color:#C8D3DA;font-size:0.8rem;margin:0 0 3px 0;">' + label + '</p>'
    html += '<p style="color:#FAF8F3;font-size:1.5rem;font-weight:700;margin:0;">' + valor_str + '</p>'
    if euros_str:
        html += '<p style="color:' + euros_cor + ';font-size:0.85rem;margin:3px 0 0 0;">' + euros_str + '</p>'
    html += '</div>'
    return html

st.markdown("---")

# ── VENCEDOR ──────────────────────────────────────────────────
melhor = max(resultados, key=lambda x: x["metricas"]["retorno"])
st.markdown(f"<div class='winner-box'>{L['vencedor']}: {melhor['nome']}</div>",
            unsafe_allow_html=True)

# ── MÉTRICAS COMPARATIVAS ─────────────────────────────────────
cols_m = st.columns(len(resultados))
for col, r in zip(cols_m, resultados):
    m = r["metricas"]
    with col:
        st.markdown(f"**{r['nome']}**")
        st.markdown(cartao(L["retorno"], f"{m['retorno']}%",
            euros_str="+▲" if m['retorno']>=0 else "-▼",
            euros_cor=cor(m['retorno'])), unsafe_allow_html=True)
        st.markdown(cartao(L["vol"], f"{m['vol']}%"), unsafe_allow_html=True)
        st.markdown(cartao(L["drawdown"], f"{m['dd']}%",
            euros_str="-▼", euros_cor="#F44336"), unsafe_allow_html=True)
        st.markdown(cartao(L["sharpe"], f"{m['sharpe']}"), unsafe_allow_html=True)

# ── GRÁFICO ───────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["grafico"])
fig = go.Figure()
for i, r in enumerate(resultados):
    fig.add_trace(go.Scatter(
        x=r["retorno"].index,
        y=(r["retorno"]*100).values.flatten(),
        name=r["nome_curto"],
        line=dict(color=PLOT_COLORS[i % len(PLOT_COLORS)], width=2.5)
    ))
fig.update_layout(
    plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Value (base 100)", xaxis_title="Date",
    hovermode="x unified", height=440,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)
st.caption(L["caption_base100"])

# ── ANÁLISE ───────────────────────────────────────────────────
st.subheader(L["analise"])

LINGUA_NOME = {
    "🇵🇹 Português": "português europeu", "🇬🇧 English": "English",
    "🇫🇷 Français": "français", "🇩🇪 Deutsch": "Deutsch", "🇪🇸 Español": "español",
}

def gerar_ai(resultados, periodo_label, lang, api_key):
    lingua = LINGUA_NOME.get(lang, "português")
    linhas = [f"- {r['nome_curto']}: retorno {r['metricas']['retorno']}%, vol {r['metricas']['vol']}%, drawdown {r['metricas']['dd']}%, Sharpe {r['metricas']['sharpe']}"
              for r in resultados]
    prompt = f"""Compara estas {len(resultados)} carteiras em {lingua} em 3-4 parágrafos para um investidor individual.
Período: {periodo_label}
{chr(10).join(linhas)}
Foca: qual performou melhor, risco relativo, qual foi mais eficiente (Sharpe). Tom direto. Sem bullet points."""
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

def render(t): return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", t)

melhor_sharpe = max(resultados, key=lambda x: x["metricas"]["sharpe"])

if api_key:
    with st.spinner("🤖 A gerar análise com IA..."):
        txt, ok = gerar_ai(resultados, periodo_label, lang, api_key)
    if ok and txt:
        st.markdown(f"<div class='insight-box'>{render(txt).replace(chr(10)+chr(10),'<br><br>')}</div>",
                    unsafe_allow_html=True)
    else:
        st.warning("API indisponível.")
        fb = [
            f"Em {periodo_label}, **{melhor['nome_curto']}** liderou com {melhor['metricas']['retorno']}%.",
            f"Ajustando ao risco (Sharpe), **{melhor_sharpe['nome_curto']}** foi a escolha mais eficiente.",
        ]
        for f in fb:
            st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
else:
    fb = [
        f"Em {periodo_label}, **{melhor['nome_curto']}** liderou com {melhor['metricas']['retorno']}%.",
        f"Ajustando ao risco (Sharpe), **{melhor_sharpe['nome_curto']}** foi a escolha mais eficiente.",
    ]
    for f in fb:
        st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
    st.info(f"💡 {L['api_info']}")

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
