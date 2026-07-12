import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from translations import CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Comparador de Carteiras",
        "subtitulo": "Compara duas estratégias de investimento e descobre qual teria performado melhor.",
        "sec_config": "⚙️ Configura as carteiras",
        "periodo_label": "Período de análise",
        "carteira_a": "📁 Carteira A", "carteira_b": "📁 Carteira B",
        "ticker_label": "Ticker", "moeda_label": "Moeda",
        "preco_label": "Preço médio de compra", "acoes_label": "Nº de ações",
        "btn_add": "➕ Adicionar ativo",
        "btn_comparar": "📊 Comparar carteiras",
        "a_carregar": "A carregar dados...",
        "erro": "Não foi possível carregar dados.",
        "vencedor": "🏆 Melhor performance no período",
        "retorno": "Retorno total", "vol": "Volatilidade anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final",
        "ganho_label": "Ganho / Perda", "valor_label": "Valor atual",
        "investido": "investido", "resumo_a": "RESUMO CARTEIRA A",
        "resumo_b": "RESUMO CARTEIRA B",
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
        "periodos": {"6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825},
        "de_ganho": "de ganho", "queda_maxima": "de queda máxima",
    },
    "🇬🇧 English": {
        "titulo": "Portfolio Comparator",
        "subtitulo": "Compare two investment strategies and find out which would have performed better.",
        "sec_config": "⚙️ Configure portfolios",
        "periodo_label": "Analysis period",
        "carteira_a": "📁 Portfolio A", "carteira_b": "📁 Portfolio B",
        "ticker_label": "Ticker", "moeda_label": "Currency",
        "preco_label": "Average purchase price", "acoes_label": "Number of shares",
        "btn_add": "➕ Add asset",
        "btn_comparar": "📊 Compare portfolios",
        "a_carregar": "Loading data...",
        "erro": "Could not load data.",
        "vencedor": "🏆 Best performance in the period",
        "retorno": "Total return", "vol": "Ann. volatility",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (approx.)",
        "valor_final": "Final value",
        "ganho_label": "Gain / Loss", "valor_label": "Current value",
        "investido": "invested", "resumo_a": "PORTFOLIO A SUMMARY",
        "resumo_b": "PORTFOLIO B SUMMARY",
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
        "periodos": {"6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825},
        "de_ganho": "gain", "queda_maxima": "max drawdown reached",
    },
    "🇫🇷 Français": {
        "titulo": "Comparateur de Portefeuilles",
        "subtitulo": "Comparez deux stratégies d'investissement.",
        "sec_config": "⚙️ Configurez les portefeuilles",
        "periodo_label": "Période d'analyse",
        "carteira_a": "📁 Portefeuille A", "carteira_b": "📁 Portefeuille B",
        "ticker_label": "Ticker", "moeda_label": "Devise",
        "preco_label": "Prix d'achat moyen", "acoes_label": "Nombre d'actions",
        "btn_add": "➕ Ajouter un actif",
        "btn_comparar": "📊 Comparer les portefeuilles",
        "a_carregar": "Chargement...",
        "erro": "Impossible de charger les données.",
        "vencedor": "🏆 Meilleure performance sur la période",
        "retorno": "Rendement total", "vol": "Volatilité ann.",
        "drawdown": "Drawdown max", "sharpe": "Sharpe (approx.)",
        "valor_final": "Valeur finale",
        "ganho_label": "Gain / Perte", "valor_label": "Valeur actuelle",
        "investido": "investi", "resumo_a": "RÉSUMÉ PORTEFEUILLE A",
        "resumo_b": "RÉSUMÉ PORTEFEUILLE B",
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
        "periodos": {"6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825},
        "de_ganho": "de gain", "queda_maxima": "de baisse maximale",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Portfolio-Vergleich",
        "subtitulo": "Vergleichen Sie zwei Anlagestrategien.",
        "sec_config": "⚙️ Portfolios konfigurieren",
        "periodo_label": "Analysezeitraum",
        "carteira_a": "📁 Portfolio A", "carteira_b": "📁 Portfolio B",
        "ticker_label": "Ticker", "moeda_label": "Währung",
        "preco_label": "Durchschn. Kaufpreis", "acoes_label": "Anzahl Aktien",
        "btn_add": "➕ Anlage hinzufügen",
        "btn_comparar": "📊 Portfolios vergleichen",
        "a_carregar": "Daten werden geladen...",
        "erro": "Daten konnten nicht geladen werden.",
        "vencedor": "🏆 Beste Performance im Zeitraum",
        "retorno": "Gesamtrendite", "vol": "Jährl. Volatilität",
        "drawdown": "Max. Drawdown", "sharpe": "Sharpe (ca.)",
        "valor_final": "Endwert",
        "ganho_label": "Gewinn / Verlust", "valor_label": "Aktueller Wert",
        "investido": "investiert", "resumo_a": "ZUSAMMENFASSUNG PORTFOLIO A",
        "resumo_b": "ZUSAMMENFASSUNG PORTFOLIO B",
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
        "periodos": {"6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
        "de_ganho": "Gewinn", "queda_maxima": "maximaler Rückgang",
    },
    "🇪🇸 Español": {
        "titulo": "Comparador de Carteras",
        "subtitulo": "Compara dos estrategias de inversión.",
        "sec_config": "⚙️ Configura las carteras",
        "periodo_label": "Período de análisis",
        "carteira_a": "📁 Cartera A", "carteira_b": "📁 Cartera B",
        "ticker_label": "Ticker", "moeda_label": "Divisa",
        "preco_label": "Precio medio de compra", "acoes_label": "Nº de acciones",
        "btn_add": "➕ Añadir activo",
        "btn_comparar": "📊 Comparar carteras",
        "a_carregar": "Cargando datos...",
        "erro": "No se pudieron cargar datos.",
        "vencedor": "🏆 Mejor rendimiento en el período",
        "retorno": "Rendimiento total", "vol": "Volatilidad anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final",
        "ganho_label": "Ganancia / Pérdida", "valor_label": "Valor actual",
        "investido": "invertido", "resumo_a": "RESUMEN CARTERA A",
        "resumo_b": "RESUMEN CARTERA B",
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
        "periodos": {"6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825},
        "de_ganho": "de ganancia", "queda_maxima": "de caída máxima",
    },
}.get(lang, {})

# ── CABEÇALHO ─────────────────────────────────────────────────
st.markdown("### 📊 Freenomics")
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── INICIALIZAR LISTAS ────────────────────────────────────────
if "comp_a" not in st.session_state:
    st.session_state.comp_a = [{"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0}]
if "comp_b" not in st.session_state:
    st.session_state.comp_b = [{"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0}]

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_config"])

periodo_opcoes = L["periodos"]
periodo_label = st.selectbox(L["periodo_label"], list(periodo_opcoes.keys()), index=2)
dias = periodo_opcoes[periodo_label]

st.markdown("---")

def render_lista(lista_key, titulo):
    st.subheader(titulo)
    lista = st.session_state[lista_key]
    remover = None
    for i, ativo in enumerate(lista):
        c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 2, 0.4])
        with c1:
            lista[i]["ticker"] = st.text_input(
                L["ticker_label"], value=ativo["ticker"],
                key=f"{lista_key}_tk_{i}", placeholder="ex: AAPL").upper().strip()
        with c2:
            lista[i]["moeda"] = st.selectbox(
                L["moeda_label"], ["USD", "EUR"],
                index=0 if ativo["moeda"] == "USD" else 1,
                key=f"{lista_key}_mo_{i}")
        with c3:
            sim = "$" if ativo["moeda"] == "USD" else "€"
            lista[i]["preco"] = st.number_input(
                f"{L['preco_label']} ({sim})", min_value=0.0,
                value=float(ativo["preco"]), step=0.01, format="%.2f",
                key=f"{lista_key}_pc_{i}")
        with c4:
            lista[i]["acoes"] = st.number_input(
                L["acoes_label"], min_value=0.0,
                value=float(ativo["acoes"]), step=1.0, format="%.0f",
                key=f"{lista_key}_na_{i}")
        with c5:
            st.markdown("<br>", unsafe_allow_html=True)
            if len(lista) > 1 and st.button("🗑️", key=f"{lista_key}_rm_{i}"):
                remover = i
    if remover is not None:
        lista.pop(remover)
        st.rerun()
    if st.button(L["btn_add"], key=f"{lista_key}_add"):
        lista.append({"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0})
        st.rerun()

col_a, col_b = st.columns(2)
with col_a:
    render_lista("comp_a", L["carteira_a"])
with col_b:
    render_lista("comp_b", L["carteira_b"])

st.markdown("---")

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
        return float(close.iloc[-1])
    except Exception:
        return 1.08

if comparar:
    st.session_state["comp_resultado"] = {
        "lista_a": [a.copy() for a in st.session_state.comp_a],
        "lista_b": [a.copy() for a in st.session_state.comp_b],
        "dias": dias, "periodo_label": periodo_label,
    }

cfg = st.session_state.get("comp_resultado", {})
lista_a = cfg.get("lista_a", st.session_state.comp_a)
lista_b = cfg.get("lista_b", st.session_state.comp_b)
dias = cfg.get("dias", dias)
periodo_label = cfg.get("periodo_label", periodo_label)

eurusd = get_eurusd()
usdeur = 1 / eurusd
sim_d  = "$" if mostrar_usd else "€"

def to_eur(val_usd): return val_usd * usdeur
def to_disp(val_eur): return val_eur * eurusd if mostrar_usd else val_eur

# Carregar todos os tickers únicos
todos_tickers = list({a["ticker"] for a in lista_a + lista_b if a["ticker"]})
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

def preco_atual(t):
    if t not in dados: return 0.0
    c = dados[t]["Close"]
    if isinstance(c, pd.DataFrame): c = c.iloc[:, 0]
    return float(c.squeeze().iloc[-1])

def retorno_medio(lista):
    series = []
    for a in lista:
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
        "retorno": round(float((serie.iloc[-1]-1)*100),2),
        "vol":     round(float(d.std()*np.sqrt(252)*100),2),
        "dd":      round(float(((serie-serie.cummax())/serie.cummax()).min()*100),2),
        "sharpe":  round(float((d.mean()/d.std())*np.sqrt(252)) if d.std().item()!=0 else 0,2),
    }

ret_a = retorno_medio(lista_a)
ret_b = retorno_medio(lista_b)

if ret_a is None or ret_b is None:
    st.error(L["erro"]); st.stop()

ma = metricas_serie(ret_a)
mb = metricas_serie(ret_b)

nome_a = " + ".join([a["ticker"] for a in lista_a if a["ticker"]])
nome_b = " + ".join([a["ticker"] for a in lista_b if a["ticker"]])

def cor(v): return "#4CAF50" if v >= 0 else "#F44336"

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

# ── VENCEDOR ──────────────────────────────────────────────────
venc = nome_a if ma["retorno"] > mb["retorno"] else nome_b
st.markdown(f"<div class='winner-box'>{L['vencedor']}: {venc}</div>", unsafe_allow_html=True)

# ── MÉTRICAS COMPARATIVAS ─────────────────────────────────────
col1, col2 = st.columns(2)
for col, nome, m in [(col1, f"{L['carteira_a']} — {nome_a}", ma),
                      (col2, f"{L['carteira_b']} — {nome_b}", mb)]:
    with col:
        st.subheader(nome)
        st.markdown(cartao(L["retorno"], f"{m['retorno']}%",
            euros_str="+▲" if m['retorno']>=0 else "-▼",
            euros_cor=cor(m['retorno'])), unsafe_allow_html=True)
        st.markdown(cartao(L["vol"], f"{m['vol']}%"), unsafe_allow_html=True)
        st.markdown(cartao(L["drawdown"], f"{m['dd']}%",
            euros_str="-▼", euros_cor="#F44336"), unsafe_allow_html=True)
        st.markdown(cartao(L["sharpe"], f"{m['sharpe']}"), unsafe_allow_html=True)

# ── CARTEIRA REAL (se preços introduzidos) ────────────────────
def resumo_real(lista, titulo, cor_titulo):
    ativos_com_dados = [a for a in lista if a["ticker"] in dados and a["preco"] > 0 and a["acoes"] > 0]
    if not ativos_com_dados: return
    st.markdown(f"**{titulo}**")
    total_inv_eur = total_atu_eur = 0
    rows = []
    for a in ativos_com_dados:
        t, mo, pc, na = a["ticker"], a["moeda"], a["preco"], a["acoes"]
        pa = preco_atual(t)
        inv_eur = (pc * na * usdeur) if mo == "USD" else (pc * na)
        atu_eur = pa * na * usdeur
        gan_eur = atu_eur - inv_eur
        pct = ((atu_eur / inv_eur) - 1) * 100 if inv_eur > 0 else 0
        total_inv_eur += inv_eur; total_atu_eur += atu_eur
        rows.append({"ticker": t, "moeda": mo, "pc": pc, "pa": pa,
                     "inv": to_disp(inv_eur), "atu": to_disp(atu_eur),
                     "gan": to_disp(gan_eur), "pct": pct})
    cols_r = st.columns(len(rows))
    for col, r in zip(cols_r, rows):
        with col:
            sim_c = "$" if r["moeda"] == "USD" else "€"
            st.markdown(f"*{r['ticker']} ({r['moeda']})*")
            st.markdown(cartao(f"{L['ganho_label']} ({sim_d})",
                f"{sim_d}{r['gan']:+,.0f}",
                euros_str=f"{r['pct']:+.1f}%",
                euros_cor=cor(r['gan'])), unsafe_allow_html=True)
            st.markdown(cartao(f"{L['valor_label']} ({sim_d})",
                f"{sim_d}{r['atu']:,.0f}",
                euros_str=f"{L['investido']}: {sim_d}{r['inv']:,.0f}",
                euros_cor="#C8D3DA"), unsafe_allow_html=True)
    gan_t = total_atu_eur - total_inv_eur
    gan_p = (gan_t / total_inv_eur * 100) if total_inv_eur > 0 else 0
    st.markdown(f"""<div style="background:#0E2A3D;border-radius:10px;padding:16px 20px;
        border:2px solid {cor_titulo};margin:8px 0;">
        <div style="display:flex;gap:30px;flex-wrap:wrap;">
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_inv']}</p>
                 <p style="color:#FAF8F3;font-size:1.2rem;font-weight:700;margin:0;">{sim_d}{to_disp(total_inv_eur):,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_atu']}</p>
                 <p style="color:#FAF8F3;font-size:1.2rem;font-weight:700;margin:0;">{sim_d}{to_disp(total_atu_eur):,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_gan']}</p>
                 <p style="color:{cor(gan_t)};font-size:1.2rem;font-weight:700;margin:0;">{sim_d}{to_disp(gan_t):+,.0f} ({gan_p:+.1f}%)</p></div>
        </div></div>""", unsafe_allow_html=True)

tem_real_a = any(a["preco"] > 0 and a["acoes"] > 0 for a in lista_a)
tem_real_b = any(a["preco"] > 0 and a["acoes"] > 0 for a in lista_b)

if tem_real_a or tem_real_b:
    st.markdown("---")
    col_ra, col_rb = st.columns(2)
    with col_ra: resumo_real(lista_a, L["resumo_a"], "#0E2A3D")
    with col_rb: resumo_real(lista_b, L["resumo_b"], "#C29A4B")

# ── GRÁFICO ───────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["grafico"])
fig = go.Figure()
fig.add_trace(go.Scatter(x=ret_a.index, y=(ret_a*100).values.flatten(),
    name=f"A: {nome_a}", line=dict(color=PLOT_COLORS[0], width=2.5)))
fig.add_trace(go.Scatter(x=ret_b.index, y=(ret_b*100).values.flatten(),
    name=f"B: {nome_b}", line=dict(color=PLOT_COLORS[1], width=2.5)))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title="Value (base 100)", xaxis_title="Date",
    hovermode="x unified", height=420,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)
st.caption(L["caption_base100"])

# ── ANÁLISE ───────────────────────────────────────────────────
st.subheader(L["analise"])

LINGUA_NOME = {
    "🇵🇹 Português": "português europeu", "🇬🇧 English": "English",
    "🇫🇷 Français": "français", "🇩🇪 Deutsch": "Deutsch", "🇪🇸 Español": "español",
}

def gerar_ai(ma, mb, nome_a, nome_b, periodo_label, lang, api_key):
    lingua = LINGUA_NOME.get(lang, "português")
    prompt = f"""Compara estas duas carteiras em {lingua} em 3 parágrafos curtos para um investidor.
Período: {periodo_label}
Carteira A ({nome_a}): retorno {ma['retorno']}%, vol {ma['vol']}%, drawdown {ma['dd']}%, Sharpe {ma['sharpe']}
Carteira B ({nome_b}): retorno {mb['retorno']}%, vol {mb['vol']}%, drawdown {mb['dd']}%, Sharpe {mb['sharpe']}
Foca: retorno relativo, risco real, qual foi mais eficiente. Tom direto. Sem bullet points."""
    try:
        r = requests.post("https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01",
                     "content-type": "application/json"},
            json={"model": "claude-haiku-4-5-20251001", "max_tokens": 500,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=30)
        if r.status_code == 200:
            return r.json()["content"][0]["text"], True
    except Exception:
        pass
    return None, False

def render(t): return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", t)

if api_key:
    with st.spinner("🤖 A gerar análise com IA..."):
        txt, ok = gerar_ai(ma, mb, nome_a, nome_b, periodo_label, lang, api_key)
    if ok and txt:
        st.markdown(f"<div class='insight-box'>{render(txt).replace(chr(10)+chr(10),'<br><br>')}</div>", unsafe_allow_html=True)
    else:
        st.warning("API indisponível.")
        venc_sharpe = nome_a if ma["sharpe"] > mb["sharpe"] else nome_b
        for f in [
            f"Em {periodo_label}, **{nome_a}** gerou {ma['retorno']}% e **{nome_b}** gerou {mb['retorno']}%. O melhor retorno foi de **{venc}**.",
            f"Em termos de risco ajustado (Sharpe), **{venc_sharpe}** foi a escolha mais eficiente.",
        ]:
            st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
else:
    venc_sharpe = nome_a if ma["sharpe"] > mb["sharpe"] else nome_b
    for f in [
        f"Em {periodo_label}, **{nome_a}** gerou {ma['retorno']}% e **{nome_b}** gerou {mb['retorno']}%. O melhor retorno foi de **{venc}**.",
        f"Em termos de risco ajustado (Sharpe), **{venc_sharpe}** foi a escolha mais eficiente.",
    ]:
        st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
    st.info(f"💡 {L['api_info']}")

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
