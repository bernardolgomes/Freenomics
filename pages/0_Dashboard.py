import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import requests, sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import T_DASHBOARD, CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")
T = T_DASHBOARD[lang]

TEXTOS = {
    "🇵🇹 Português": {
        "sec_carteira": "⚙️ Configura a tua carteira",
        "periodo_label": "Período de análise",
        "ticker_label": "Ticker", "moeda_label": "Moeda",
        "preco_label": "Preço médio de compra", "acoes_label": "Nº de ações",
        "btn_add": "➕ Adicionar ativo",
        "btn_analisar": "📊 Analisar carteira",
        "a_carregar": "A carregar dados de mercado...",
        "erro": "Não foi possível carregar dados para alguns tickers.",
        "carteira_real": "💼 A tua carteira real",
        "preco_arrow": "Preço compra → atual",
        "ganho_label": "Ganho / Perda", "valor_label": "Valor atual",
        "investido": "investido", "resumo": "RESUMO DA CARTEIRA",
        "tot_inv": "Total investido", "tot_atu": "Valor atual",
        "tot_gan": "Ganho / Perda total", "fx_nota": "Taxa de câmbio",
        "mostrar_usd": "Mostrar em USD ($)",
        "grafico_titulo": "Evolução comparada (base 100)",
        "insights_titulo": "📝 Leitura automática dos resultados",
        "api_label": "🤖 Anthropic API Key (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Com API key, os insights são gerados por IA.",
        "aviso": "⚠️ Análise gerada automaticamente — não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Dados via Yahoo Finance",
        "periodos": {"1 mês": 30, "3 meses": 90, "6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825, "10 anos": 3650, "20 anos": 7300},
        "caption_base100": "💡 **Base 100:** todos os ativos começam no mesmo ponto. Ex: 180 = subiu 80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** a linha tracejada representa o S&P 500. Serve para perceber se a tua carteira está a superar o mercado.",
        "insight_melhor": lambda m, p, r: f"Nos últimos **{p.lower()}**, **{m}** teve a melhor performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"enquanto **{p}** registou a menor subida ({r}%).",
        "insight_pior_queda": lambda p, r: f"enquanto **{p}** registou uma queda ({r}%).",
        "insight_unico": lambda t, p, r: f"Nos últimos {p.lower()}, **{t}** registou um retorno de {r}%.",
        "insight_volatil": lambda t, v: f"Em termos de risco, **{t}** foi o ativo mais instável, com volatilidade de {v}% ao ano.",
        "insight_drawdown": lambda t, d: f"**{t}** sofreu uma queda máxima de {d}% face ao seu pico — um valor considerável.",
        "insight_sharpe": lambda t: f"Ajustando ao risco (Sharpe), **{t}** foi quem ofereceu o melhor equilíbrio retorno/risco.",
    },
    "🇬🇧 English": {
        "sec_carteira": "⚙️ Configure your portfolio",
        "periodo_label": "Analysis period",
        "ticker_label": "Ticker", "moeda_label": "Currency",
        "preco_label": "Average purchase price", "acoes_label": "Number of shares",
        "btn_add": "➕ Add asset",
        "btn_analisar": "📊 Analyse portfolio",
        "a_carregar": "Loading market data...",
        "erro": "Could not load data for some tickers.",
        "carteira_real": "💼 Your real portfolio",
        "preco_arrow": "Purchase → current price",
        "ganho_label": "Gain / Loss", "valor_label": "Current value",
        "investido": "invested", "resumo": "PORTFOLIO SUMMARY",
        "tot_inv": "Total invested", "tot_atu": "Current value",
        "tot_gan": "Total gain / loss", "fx_nota": "Exchange rate",
        "mostrar_usd": "Show in USD ($)",
        "grafico_titulo": "Comparative evolution (base 100)",
        "insights_titulo": "📝 Automatic reading of results",
        "api_label": "🤖 Anthropic API Key (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "With an API key, insights are AI-generated.",
        "aviso": "⚠️ Automatically generated — does not constitute financial advice.",
        "rodape": "Freenomics · Data via Yahoo Finance",
        "periodos": {"1 month": 30, "3 months": 90, "6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825, "10 years": 3650, "20 years": 7300},
        "caption_base100": "💡 **Base 100:** all assets start at the same point. E.g. 180 = rose 80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** the dashed line represents the S&P 500 — shows if your portfolio beats the market.",
        "insight_melhor": lambda m, p, r: f"Over the last **{p.lower()}**, **{m}** had the best performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"while **{p}** recorded the smallest gain ({r}%).",
        "insight_pior_queda": lambda p, r: f"while **{p}** recorded a decline ({r}%).",
        "insight_unico": lambda t, p, r: f"Over the last {p.lower()}, **{t}** recorded a return of {r}%.",
        "insight_volatil": lambda t, v: f"In terms of risk, **{t}** was the most volatile asset, with {v}% annualised volatility.",
        "insight_drawdown": lambda t, d: f"**{t}** suffered a maximum drawdown of {d}% from its peak.",
        "insight_sharpe": lambda t: f"Risk-adjusted (Sharpe), **{t}** offered the best balance between return and volatility.",
    },
    "🇫🇷 Français": {
        "sec_carteira": "⚙️ Configurez votre portefeuille",
        "periodo_label": "Période d'analyse",
        "ticker_label": "Ticker", "moeda_label": "Devise",
        "preco_label": "Prix d'achat moyen", "acoes_label": "Nombre d'actions",
        "btn_add": "➕ Ajouter un actif",
        "btn_analisar": "📊 Analyser le portefeuille",
        "a_carregar": "Chargement des données...",
        "erro": "Impossible de charger les données pour certains tickers.",
        "carteira_real": "💼 Votre portefeuille réel",
        "preco_arrow": "Prix achat → actuel",
        "ganho_label": "Gain / Perte", "valor_label": "Valeur actuelle",
        "investido": "investi", "resumo": "RÉSUMÉ DU PORTEFEUILLE",
        "tot_inv": "Total investi", "tot_atu": "Valeur actuelle",
        "tot_gan": "Gain / Perte total", "fx_nota": "Taux de change",
        "mostrar_usd": "Afficher en USD ($)",
        "grafico_titulo": "Évolution comparée (base 100)",
        "insights_titulo": "📝 Lecture automatique des résultats",
        "api_label": "🤖 Clé API Anthropic (optionnel)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Avec une clé API, les insights sont générés par IA.",
        "aviso": "⚠️ Analyse automatique — ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Données via Yahoo Finance",
        "periodos": {"1 mois": 30, "3 mois": 90, "6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825, "10 ans": 3650, "20 ans": 7300},
        "caption_base100": "💡 **Base 100 :** tous les actifs partent du même point. Ex : 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark) :** la ligne en pointillés représente le S&P 500.",
        "insight_melhor": lambda m, p, r: f"Au cours des **{p.lower()}** derniers, **{m}** a eu la meilleure performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"tandis que **{p}** a enregistré la plus faible hausse ({r}%).",
        "insight_pior_queda": lambda p, r: f"tandis que **{p}** a enregistré une baisse ({r}%).",
        "insight_unico": lambda t, p, r: f"Au cours des {p.lower()} derniers, **{t}** a enregistré un rendement de {r}%.",
        "insight_volatil": lambda t, v: f"**{t}** a été l'actif le plus instable, avec une volatilité de {v}% par an.",
        "insight_drawdown": lambda t, d: f"**{t}** a subi une baisse maximale de {d}% par rapport à son pic.",
        "insight_sharpe": lambda t: f"Ajusté au risque (Sharpe), **{t}** a offert le meilleur équilibre rendement/risque.",
    },
    "🇩🇪 Deutsch": {
        "sec_carteira": "⚙️ Portfolio konfigurieren",
        "periodo_label": "Analysezeitraum",
        "ticker_label": "Ticker", "moeda_label": "Währung",
        "preco_label": "Durchschn. Kaufpreis", "acoes_label": "Anzahl Aktien",
        "btn_add": "➕ Anlage hinzufügen",
        "btn_analisar": "📊 Portfolio analysieren",
        "a_carregar": "Marktdaten werden geladen...",
        "erro": "Daten für einige Ticker konnten nicht geladen werden.",
        "carteira_real": "💼 Ihr reales Portfolio",
        "preco_arrow": "Kaufpreis → aktuell",
        "ganho_label": "Gewinn / Verlust", "valor_label": "Aktueller Wert",
        "investido": "investiert", "resumo": "PORTFOLIO-ZUSAMMENFASSUNG",
        "tot_inv": "Gesamt investiert", "tot_atu": "Aktueller Wert",
        "tot_gan": "Gesamtgewinn / -verlust", "fx_nota": "Wechselkurs",
        "mostrar_usd": "In USD anzeigen ($)",
        "grafico_titulo": "Vergleichende Entwicklung (Basis 100)",
        "insights_titulo": "📝 Automatische Auswertung",
        "api_label": "🤖 Anthropic API-Schlüssel (optional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Mit API-Schlüssel werden Insights KI-generiert.",
        "aviso": "⚠️ Automatisch generiert — stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Daten via Yahoo Finance",
        "periodos": {"1 Monat": 30, "3 Monate": 90, "6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825, "10 Jahre": 3650, "20 Jahre": 7300},
        "caption_base100": "💡 **Basis 100:** Alle Anlagen starten am selben Punkt. Bsp.: 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (Benchmark):** Die gestrichelte Linie zeigt den S&P 500.",
        "insight_melhor": lambda m, p, r: f"In den letzten **{p.lower()}** hatte **{m}** die beste Performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"während **{p}** den geringsten Anstieg verzeichnete ({r}%).",
        "insight_pior_queda": lambda p, r: f"während **{p}** einen Rückgang verzeichnete ({r}%).",
        "insight_unico": lambda t, p, r: f"In den letzten {p.lower()} verzeichnete **{t}** eine Rendite von {r}%.",
        "insight_volatil": lambda t, v: f"**{t}** war die volatilste Anlage mit {v}% jährlicher Volatilität.",
        "insight_drawdown": lambda t, d: f"**{t}** erlitt einen maximalen Drawdown von {d}% vom Höchststand.",
        "insight_sharpe": lambda t: f"Risikoadjustiert (Sharpe) bot **{t}** das beste Rendite-Risiko-Verhältnis.",
    },
    "🇪🇸 Español": {
        "sec_carteira": "⚙️ Configura tu cartera",
        "periodo_label": "Período de análisis",
        "ticker_label": "Ticker", "moeda_label": "Divisa",
        "preco_label": "Precio medio de compra", "acoes_label": "Nº de acciones",
        "btn_add": "➕ Añadir activo",
        "btn_analisar": "📊 Analizar cartera",
        "a_carregar": "Cargando datos de mercado...",
        "erro": "No se pudieron cargar datos para algunos tickers.",
        "carteira_real": "💼 Tu cartera real",
        "preco_arrow": "Precio compra → actual",
        "ganho_label": "Ganancia / Pérdida", "valor_label": "Valor actual",
        "investido": "invertido", "resumo": "RESUMEN DE CARTERA",
        "tot_inv": "Total invertido", "tot_atu": "Valor actual",
        "tot_gan": "Ganancia / Pérdida total", "fx_nota": "Tipo de cambio",
        "mostrar_usd": "Mostrar en USD ($)",
        "grafico_titulo": "Evolución comparada (base 100)",
        "insights_titulo": "📝 Lectura automática de resultados",
        "api_label": "🤖 Clave API Anthropic (opcional)",
        "api_placeholder": "sk-ant-...",
        "api_info": "Con clave API, los insights son generados por IA.",
        "aviso": "⚠️ Análisis automático — no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Datos via Yahoo Finance",
        "periodos": {"1 mes": 30, "3 meses": 90, "6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825, "10 años": 3650, "20 años": 7300},
        "caption_base100": "💡 **Base 100:** todos los activos parten del mismo punto. Ej: 180 = +80%.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** la línea discontinua representa el S&P 500.",
        "insight_melhor": lambda m, p, r: f"En los últimos **{p.lower()}**, **{m}** tuvo el mejor rendimiento ({r}%).",
        "insight_pior_subida": lambda p, r: f"mientras **{p}** registró la menor subida ({r}%).",
        "insight_pior_queda": lambda p, r: f"mientras **{p}** registró una caída ({r}%).",
        "insight_unico": lambda t, p, r: f"En los últimos {p.lower()}, **{t}** registró un rendimiento de {r}%.",
        "insight_volatil": lambda t, v: f"**{t}** fue el activo más volátil, con una volatilidad de {v}% anual.",
        "insight_drawdown": lambda t, d: f"**{t}** sufrió una caída máxima de {d}% desde su pico.",
        "insight_sharpe": lambda t: f"Ajustado al riesgo (Sharpe), **{t}** ofreció el mejor equilibrio rendimiento/riesgo.",
    },
}
L = TEXTOS.get(lang, TEXTOS["🇬🇧 English"])

# ── CABEÇALHO ─────────────────────────────────────────────────
show_logo()
st.title(T["titulo"])
st.caption(T["subtitulo"])

# ── INICIALIZAR LISTA DE ATIVOS ───────────────────────────────
if "ativos" not in st.session_state:
    st.session_state.ativos = [
        {"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0},
    ]

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_carteira"])

# Período
periodo_opcoes = L["periodos"]
periodo_label = st.selectbox(L["periodo_label"], list(periodo_opcoes.keys()), index=2)
dias = periodo_opcoes[periodo_label]

st.markdown("---")

# Lista dinâmica de ativos
ativos_para_remover = None
for i, ativo in enumerate(st.session_state.ativos):
    c1, c2, c3, c4, c5 = st.columns([2, 1, 2, 2, 0.4])
    with c1:
        st.session_state.ativos[i]["ticker"] = st.text_input(
            L["ticker_label"], value=ativo["ticker"],
            key=f"tk_{i}", placeholder="ex: AAPL").upper().strip()
    with c2:
        st.session_state.ativos[i]["moeda"] = st.selectbox(
            L["moeda_label"], ["USD", "EUR"],
            index=0 if ativo["moeda"] == "USD" else 1,
            key=f"mo_{i}")
    with c3:
        simbolo_input = "$" if ativo["moeda"] == "USD" else "€"
        st.session_state.ativos[i]["preco"] = st.number_input(
            f"{L['preco_label']} ({simbolo_input})",
            min_value=0.0, value=float(ativo["preco"]),
            step=0.01, format="%.2f", key=f"pc_{i}")
    with c4:
        st.session_state.ativos[i]["acoes"] = st.number_input(
            L["acoes_label"], min_value=0.0, value=float(ativo["acoes"]),
            step=1.0, format="%.0f", key=f"na_{i}")
    with c5:
        st.markdown("<br>", unsafe_allow_html=True)
        if len(st.session_state.ativos) > 1:
            if st.button("🗑️", key=f"rm_{i}", help="Remover"):
                ativos_para_remover = i

if ativos_para_remover is not None:
    st.session_state.ativos.pop(ativos_para_remover)
    st.rerun()

if st.button(L["btn_add"], use_container_width=False):
    st.session_state.ativos.append(
        {"ticker": "", "moeda": "USD", "preco": 0.0, "acoes": 0.0})
    st.rerun()

st.markdown("---")

# API e toggle
col_api, col_usd = st.columns([3, 1])
with col_api:
    api_key = st.text_input(L["api_label"], type="password",
                             placeholder=L["api_placeholder"],
                             help=L["api_info"])
with col_usd:
    st.markdown("&nbsp;", unsafe_allow_html=True)
    mostrar_usd = st.toggle(L["mostrar_usd"], value=False)

analisar = st.button(L["btn_analisar"], type="primary", use_container_width=True)

if not analisar and "freenomics_resultado" not in st.session_state:
    st.stop()

# ── DADOS ─────────────────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar_dados(ticker, dias):
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

if analisar:
    st.session_state["freenomics_resultado"] = {
        "ativos": [a.copy() for a in st.session_state.ativos],
        "dias": dias, "periodo_label": periodo_label,
    }

cfg      = st.session_state.get("freenomics_resultado", {})
ativos_r = cfg.get("ativos", st.session_state.ativos)
dias     = cfg.get("dias", dias)
periodo_label = cfg.get("periodo_label", periodo_label)

tickers = [a["ticker"] for a in ativos_r if a["ticker"]]
dados   = {}
with st.spinner(L["a_carregar"]):
    for t in tickers:
        try:
            df = carregar_dados(t, dias)
            if not df.empty: dados[t] = df
        except Exception:
            pass

if not dados:
    st.error(L["erro"]); st.stop()

eurusd = get_eurusd()
usdeur = 1 / eurusd
simbolo_display = "$" if mostrar_usd else "€"

def to_display(valor_eur):
    return valor_eur * eurusd if mostrar_usd else valor_eur

def calc_metricas(df):
    precos = df["Close"]
    if isinstance(precos, pd.DataFrame): precos = precos.iloc[:, 0]
    precos = precos.squeeze()
    ret  = float((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
    rd   = precos.pct_change().dropna()
    vol  = float(rd.std() * np.sqrt(252) * 100)
    pico = precos.cummax()
    dd   = float(((precos - pico) / pico).min() * 100)
    sh   = float((rd.mean() / rd.std()) * np.sqrt(252)) if rd.std().item() != 0 else 0.0
    pa   = float(precos.iloc[-1])
    return {"retorno_total": round(ret,2), "volatilidade": round(vol,2),
            "max_drawdown": round(dd,2), "sharpe": round(sh,2), "preco_atual": round(pa,2)}

metricas = {t: calc_metricas(df) for t, df in dados.items()}

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

# ── CARTEIRA REAL ─────────────────────────────────────────────
ativos_com_dados = [a for a in ativos_r if a["ticker"] in metricas and a["preco"] > 0 and a["acoes"] > 0]

if ativos_com_dados:
    st.subheader(L["carteira_real"])
    total_inv_eur = 0
    total_atu_eur = 0
    rows = []

    for a in ativos_com_dados:
        t   = a["ticker"]
        mo  = a["moeda"]
        pc  = a["preco"]
        na  = a["acoes"]
        pa  = metricas[t]["preco_atual"]

        # Converter tudo para EUR internamente
        if mo == "USD":
            inv_eur = pc * na * usdeur
            atu_eur = pa * na * usdeur
        else:  # EUR
            inv_eur = pc * na
            atu_eur = pa * na * usdeur  # preço atual de yfinance é sempre USD

        gan_eur = atu_eur - inv_eur
        pct     = ((atu_eur / inv_eur) - 1) * 100 if inv_eur > 0 else 0

        total_inv_eur += inv_eur
        total_atu_eur += atu_eur

        rows.append({"ticker": t, "moeda": mo, "pc": pc, "pa": pa,
                     "inv": to_display(inv_eur), "atu": to_display(atu_eur),
                     "gan": to_display(gan_eur), "pct": pct})

    cols_r = st.columns(max(len(rows), 1))
    for col, r in zip(cols_r, rows):
        with col:
            simbolo_compra = "$" if r["moeda"] == "USD" else "€"
            st.markdown(f"**{r['ticker']}** ({r['moeda']})")
            st.markdown(cartao(L["preco_arrow"],
                f"{simbolo_compra}{r['pc']:.2f} → ${r['pa']:.2f}"),
                unsafe_allow_html=True)
            st.markdown(cartao(f"{L['ganho_label']} ({simbolo_display})",
                f"{simbolo_display}{r['gan']:+,.0f}",
                euros_str=f"{r['pct']:+.1f}%",
                euros_cor=cor(r['gan'])), unsafe_allow_html=True)
            st.markdown(cartao(f"{L['valor_label']} ({simbolo_display})",
                f"{simbolo_display}{r['atu']:,.0f}",
                euros_str=f"{L['investido']}: {simbolo_display}{r['inv']:,.0f}",
                euros_cor="#C8D3DA"), unsafe_allow_html=True)

    gan_total = total_atu_eur - total_inv_eur
    gan_pct   = (gan_total / total_inv_eur * 100) if total_inv_eur > 0 else 0
    fx_str    = f"1 USD = €{usdeur:.4f}" if not mostrar_usd else f"1 EUR = ${eurusd:.4f}"

    st.markdown(f"""
    <div style="background:#0E2A3D;border-radius:10px;padding:20px 24px;
                border:2px solid #C29A4B;margin:12px 0;">
        <p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 12px 0;">{L['resumo']}</p>
        <div style="display:flex;gap:40px;flex-wrap:wrap;">
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_inv']}</p>
                 <p style="color:#FAF8F3;font-size:1.4rem;font-weight:700;margin:0;">{simbolo_display}{to_display(total_inv_eur):,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_atu']}</p>
                 <p style="color:#FAF8F3;font-size:1.4rem;font-weight:700;margin:0;">{simbolo_display}{to_display(total_atu_eur):,.0f}</p></div>
            <div><p style="color:#C8D3DA;font-size:0.8rem;margin:0;">{L['tot_gan']}</p>
                 <p style="color:{cor(gan_total)};font-size:1.4rem;font-weight:700;margin:0;">{simbolo_display}{to_display(gan_total):+,.0f} ({gan_pct:+.1f}%)</p></div>
        </div>
        <p style="color:#6B7280;font-size:0.75rem;margin:10px 0 0 0;">{L['fx_nota']}: {fx_str} · Yahoo Finance</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("---")

# ── GRÁFICO ───────────────────────────────────────────────────
st.subheader(L["grafico_titulo"])
fig = go.Figure()
for i, t in enumerate(tickers):
    if t not in dados: continue
    df = dados[t]
    close = df["Close"]
    if isinstance(close, pd.DataFrame): close = close.iloc[:, 0]
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
            fig.add_trace(go.Scatter(x=df_spy.index, y=((c/c.iloc[0])*100).values.flatten(),
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

def gerar_ai(metricas, periodo_label, lang, api_key):
    lingua = LINGUA_NOME.get(lang, "português")
    linhas = [f"- {t}: retorno {m['retorno_total']}%, volatilidade {m['volatilidade']}%, drawdown {m['max_drawdown']}%, Sharpe {m['sharpe']}"
              for t, m in metricas.items()]
    prompt = f"""Analisa esta carteira em {lingua} em 3-4 parágrafos curtos para um investidor individual.
Período: {periodo_label}
{chr(10).join(linhas)}
Foca: melhor/pior performance, risco em linguagem acessível, conclusão prática.
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

def fallback(metricas, periodo_label, L):
    frases = []
    ordenado = sorted(metricas.items(), key=lambda x: x[1]["retorno_total"], reverse=True)
    melhor, pior = ordenado[0], ordenado[-1]
    if len(metricas) > 1:
        f = L["insight_melhor"](melhor[0], periodo_label, melhor[1]["retorno_total"]) + " "
        f += L["insight_pior_subida"](pior[0], pior[1]["retorno_total"]) if pior[1]["retorno_total"] >= 0 else L["insight_pior_queda"](pior[0], pior[1]["retorno_total"])
        frases.append(f)
    else:
        t, m = list(metricas.items())[0]
        frases.append(L["insight_unico"](t, periodo_label, m["retorno_total"]))
    if len(metricas) > 1:
        mv = sorted(metricas.items(), key=lambda x: x[1]["volatilidade"], reverse=True)[0]
        frases.append(L["insight_volatil"](mv[0], mv[1]["volatilidade"]))
    for t, m in metricas.items():
        if m["max_drawdown"] < -20:
            frases.append(L["insight_drawdown"](t, m["max_drawdown"]))
    ms = sorted(metricas.items(), key=lambda x: x[1]["sharpe"], reverse=True)[0]
    if ms[1]["sharpe"] > 0:
        frases.append(L["insight_sharpe"](ms[0]))
    return frases

def render(texto):
    return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", texto)

if api_key:
    with st.spinner("🤖 A gerar análise com IA..."):
        texto_ai, ok = gerar_ai(metricas, periodo_label, lang, api_key)
    if ok and texto_ai:
        st.markdown(f"<div class='insight-box'>{render(texto_ai).replace(chr(10)+chr(10), '<br><br>')}</div>", unsafe_allow_html=True)
        st.caption("✨ " + L["aviso"])
    else:
        st.warning("API indisponível. A usar análise automática.")
        for f in fallback(metricas, periodo_label, L):
            st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
else:
    for f in fallback(metricas, periodo_label, L):
        st.markdown(f"<div class='insight-box'>{render(f)}</div>", unsafe_allow_html=True)
    st.info(f"💡 {L['api_info']}")

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
