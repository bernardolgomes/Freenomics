"""
Análise de Ação · Freenomics
Framework de "future earnings": projeta receitas, margem e nº de ações, calcula o EPS,
aplica um P/E alvo e estima o preço futuro, o retorno anual e a margem de segurança.
No fim dá um veredicto em checklist. Histórico preenchido automaticamente via yfinance.
"""

import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
import yfinance as yf
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo, demo_bar
from translations import CSS, FIX_DROPDOWNS_JS, style_fig
import auth

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

N_ANOS = 5

L = {
    "🇵🇹 Português": {
        "titulo": "Análise de Ação",
        "subtitulo": "Projeta os resultados de uma empresa, estima o preço futuro e percebe se faz sentido investir.",
        "ticker": "Ticker (ex.: AAPL, MSFT, ASML.AS)", "btn_carregar": "📥 Carregar dados",
        "erro_dados": "Não foi possível obter dados para este ticker. Confirma o símbolo ou preenche manualmente.",
        "sec_hist": "📚 Histórico (financial statements)",
        "ano": "Ano", "receitas": "Receitas", "cresc_rec": "Crescimento de receitas (%)",
        "lucro": "Lucro líquido", "margem": "Margem líquida (%)", "acoes": "Nº de ações (milhões)",
        "eps": "EPS", "pe": "P/E alvo", "dividendos": "Dividendo por ação",
        "sec_proj": "🔮 Projeções (edita as células)",
        "dica_proj": "Preenchido com base no histórico. Ajusta o crescimento, a margem, as ações, o P/E e os dividendos de cada ano.",
        "sec_param": "⚙️ Parâmetros",
        "preco_atual": "Preço atual", "retorno_desejado": "Retorno anual desejado (%)",
        "margem_seg": "Margem de segurança (%)", "benchmark": "Média anual S&P 500 (%)",
        "btn_calcular": "🧮 Calcular análise",
        "sec_res": "📊 Resultados",
        "preco_est": "Preço estimado", "mudanca": "Mudança face ao preço atual",
        "retorno_anual": "Retorno anual esperado", "preco_alvo": "Preço para obter o retorno desejado",
        "preco_seg": "Preço com margem de segurança", "falta": "Variação até ao preço com margem",
        "sec_veredicto": "✅ Veredicto",
        "c_retorno": "Retorno esperado ≥ retorno desejado",
        "c_bench": "Retorno esperado acima do S&P 500",
        "c_margem": "Preço atual ≤ preço com margem de segurança",
        "c_cresc": "Receitas projetadas crescem em média ≥ 5%/ano",
        "c_margem_liq": "Margem líquida projetada não diminui",
        "c_diluicao": "Número de ações não aumenta (sem diluição)",
        "c_pe": "P/E projetado ≤ P/E atual (cenário prudente)",
        "v_bom": "Faz sentido investir: a maioria dos critérios é cumprida.",
        "v_neutro": "Neutro: há pontos a favor e contra. Revê as projeções ou espera por um preço melhor.",
        "v_mau": "Não faz sentido neste preço e com estes pressupostos.",
        "pontuacao": "Pontuação",
        "grafico": "Preço estimado vs preço atual",
        "aviso": "⚠️ Modelo baseado em pressupostos teus, não numa previsão. Não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Análise de ações individuais",
        "unidades": "Valores em milhões (moeda da empresa).",
    },
    "🇬🇧 English": {
        "titulo": "Stock Analysis",
        "subtitulo": "Project a company's results, estimate its future price and see whether investing makes sense.",
        "ticker": "Ticker (e.g. AAPL, MSFT, ASML.AS)", "btn_carregar": "📥 Load data",
        "erro_dados": "Could not get data for this ticker. Check the symbol or fill in manually.",
        "sec_hist": "📚 History (financial statements)",
        "ano": "Year", "receitas": "Revenue", "cresc_rec": "Revenue growth (%)",
        "lucro": "Net income", "margem": "Net margin (%)", "acoes": "Shares (millions)",
        "eps": "EPS", "pe": "Target P/E", "dividendos": "Dividend per share",
        "sec_proj": "🔮 Projections (edit the cells)",
        "dica_proj": "Pre-filled from history. Adjust growth, margin, shares, P/E and dividends for each year.",
        "sec_param": "⚙️ Parameters",
        "preco_atual": "Current price", "retorno_desejado": "Desired annual return (%)",
        "margem_seg": "Margin of safety (%)", "benchmark": "S&P 500 annual average (%)",
        "btn_calcular": "🧮 Run analysis",
        "sec_res": "📊 Results",
        "preco_est": "Estimated price", "mudanca": "Change vs current price",
        "retorno_anual": "Expected annual return", "preco_alvo": "Price to get the desired return",
        "preco_seg": "Price with margin of safety", "falta": "Change to margin-of-safety price",
        "sec_veredicto": "✅ Verdict",
        "c_retorno": "Expected return ≥ desired return",
        "c_bench": "Expected return above the S&P 500",
        "c_margem": "Current price ≤ price with margin of safety",
        "c_cresc": "Projected revenue grows on average ≥ 5%/year",
        "c_margem_liq": "Projected net margin does not decrease",
        "c_diluicao": "Share count does not increase (no dilution)",
        "c_pe": "Projected P/E ≤ current P/E (prudent scenario)",
        "v_bom": "Investing makes sense: most criteria are met.",
        "v_neutro": "Neutral: mixed signals. Review the projections or wait for a better price.",
        "v_mau": "Does not make sense at this price and with these assumptions.",
        "pontuacao": "Score",
        "grafico": "Estimated price vs current price",
        "aviso": "⚠️ Model based on your own assumptions, not a forecast. Not financial advice.",
        "rodape": "Freenomics · Individual stock analysis",
        "unidades": "Values in millions (company currency).",
    },
    "🇫🇷 Français": {
        "titulo": "Analyse d'Action",
        "subtitulo": "Projetez les résultats d'une entreprise, estimez son prix futur et voyez si investir a du sens.",
        "ticker": "Ticker (ex. AAPL, MSFT, ASML.AS)", "btn_carregar": "📥 Charger les données",
        "erro_dados": "Impossible d'obtenir les données pour ce ticker. Vérifiez le symbole ou saisissez manuellement.",
        "sec_hist": "📚 Historique (états financiers)",
        "ano": "Année", "receitas": "Chiffre d'affaires", "cresc_rec": "Croissance du CA (%)",
        "lucro": "Résultat net", "margem": "Marge nette (%)", "acoes": "Nb d'actions (millions)",
        "eps": "BPA", "pe": "P/E cible", "dividendos": "Dividende par action",
        "sec_proj": "🔮 Projections (modifiez les cellules)",
        "dica_proj": "Pré-rempli à partir de l'historique. Ajustez croissance, marge, actions, P/E et dividendes.",
        "sec_param": "⚙️ Paramètres",
        "preco_atual": "Prix actuel", "retorno_desejado": "Rendement annuel souhaité (%)",
        "margem_seg": "Marge de sécurité (%)", "benchmark": "Moyenne annuelle S&P 500 (%)",
        "btn_calcular": "🧮 Calculer l'analyse",
        "sec_res": "📊 Résultats",
        "preco_est": "Prix estimé", "mudanca": "Variation vs prix actuel",
        "retorno_anual": "Rendement annuel attendu", "preco_alvo": "Prix pour le rendement souhaité",
        "preco_seg": "Prix avec marge de sécurité", "falta": "Variation jusqu'au prix avec marge",
        "sec_veredicto": "✅ Verdict",
        "c_retorno": "Rendement attendu ≥ rendement souhaité",
        "c_bench": "Rendement attendu supérieur au S&P 500",
        "c_margem": "Prix actuel ≤ prix avec marge de sécurité",
        "c_cresc": "CA projeté en croissance moyenne ≥ 5%/an",
        "c_margem_liq": "La marge nette projetée ne diminue pas",
        "c_diluicao": "Le nombre d'actions n'augmente pas (pas de dilution)",
        "c_pe": "P/E projeté ≤ P/E actuel (scénario prudent)",
        "v_bom": "Investir a du sens : la plupart des critères sont remplis.",
        "v_neutro": "Neutre : signaux mitigés. Révisez les projections ou attendez un meilleur prix.",
        "v_mau": "N'a pas de sens à ce prix et avec ces hypothèses.",
        "pontuacao": "Score",
        "grafico": "Prix estimé vs prix actuel",
        "aviso": "⚠️ Modèle basé sur vos hypothèses, pas une prévision. Ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Analyse d'actions individuelles",
        "unidades": "Valeurs en millions (devise de l'entreprise).",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Aktienanalyse",
        "subtitulo": "Projiziere die Ergebnisse eines Unternehmens, schätze den Kurs und prüfe, ob ein Investment sinnvoll ist.",
        "ticker": "Ticker (z. B. AAPL, MSFT, ASML.AS)", "btn_carregar": "📥 Daten laden",
        "erro_dados": "Keine Daten für diesen Ticker. Symbol prüfen oder manuell ausfüllen.",
        "sec_hist": "📚 Historie (Finanzberichte)",
        "ano": "Jahr", "receitas": "Umsatz", "cresc_rec": "Umsatzwachstum (%)",
        "lucro": "Nettogewinn", "margem": "Nettomarge (%)", "acoes": "Aktien (Mio.)",
        "eps": "EPS", "pe": "Ziel-KGV", "dividendos": "Dividende je Aktie",
        "sec_proj": "🔮 Projektionen (Zellen bearbeiten)",
        "dica_proj": "Aus der Historie vorbefüllt. Wachstum, Marge, Aktien, KGV und Dividenden je Jahr anpassen.",
        "sec_param": "⚙️ Parameter",
        "preco_atual": "Aktueller Kurs", "retorno_desejado": "Gewünschte Jahresrendite (%)",
        "margem_seg": "Sicherheitsmarge (%)", "benchmark": "S&P-500-Jahresdurchschnitt (%)",
        "btn_calcular": "🧮 Analyse berechnen",
        "sec_res": "📊 Ergebnisse",
        "preco_est": "Geschätzter Kurs", "mudanca": "Änderung zum aktuellen Kurs",
        "retorno_anual": "Erwartete Jahresrendite", "preco_alvo": "Kurs für die gewünschte Rendite",
        "preco_seg": "Kurs mit Sicherheitsmarge", "falta": "Änderung bis zum Kurs mit Marge",
        "sec_veredicto": "✅ Fazit",
        "c_retorno": "Erwartete Rendite ≥ gewünschte Rendite",
        "c_bench": "Erwartete Rendite über dem S&P 500",
        "c_margem": "Aktueller Kurs ≤ Kurs mit Sicherheitsmarge",
        "c_cresc": "Projizierter Umsatz wächst im Schnitt ≥ 5 %/Jahr",
        "c_margem_liq": "Projizierte Nettomarge sinkt nicht",
        "c_diluicao": "Aktienzahl steigt nicht (keine Verwässerung)",
        "c_pe": "Projiziertes KGV ≤ aktuelles KGV (vorsichtiges Szenario)",
        "v_bom": "Investment sinnvoll: Die meisten Kriterien sind erfüllt.",
        "v_neutro": "Neutral: gemischte Signale. Projektionen prüfen oder auf besseren Kurs warten.",
        "v_mau": "Bei diesem Kurs und diesen Annahmen nicht sinnvoll.",
        "pontuacao": "Punktzahl",
        "grafico": "Geschätzter Kurs vs aktueller Kurs",
        "aviso": "⚠️ Modell basiert auf deinen Annahmen, keine Prognose. Keine Anlageberatung.",
        "rodape": "Freenomics · Einzelaktienanalyse",
        "unidades": "Werte in Millionen (Währung des Unternehmens).",
    },
    "🇪🇸 Español": {
        "titulo": "Análisis de Acción",
        "subtitulo": "Proyecta los resultados de una empresa, estima su precio futuro y comprueba si tiene sentido invertir.",
        "ticker": "Ticker (p. ej. AAPL, MSFT, ASML.AS)", "btn_carregar": "📥 Cargar datos",
        "erro_dados": "No se pudieron obtener datos de este ticker. Revisa el símbolo o rellena manualmente.",
        "sec_hist": "📚 Histórico (estados financieros)",
        "ano": "Año", "receitas": "Ingresos", "cresc_rec": "Crecimiento de ingresos (%)",
        "lucro": "Beneficio neto", "margem": "Margen neto (%)", "acoes": "Nº de acciones (millones)",
        "eps": "BPA", "pe": "P/E objetivo", "dividendos": "Dividendo por acción",
        "sec_proj": "🔮 Proyecciones (edita las celdas)",
        "dica_proj": "Rellenado con el histórico. Ajusta crecimiento, margen, acciones, P/E y dividendos de cada año.",
        "sec_param": "⚙️ Parámetros",
        "preco_atual": "Precio actual", "retorno_desejado": "Rentabilidad anual deseada (%)",
        "margem_seg": "Margen de seguridad (%)", "benchmark": "Media anual S&P 500 (%)",
        "btn_calcular": "🧮 Calcular análisis",
        "sec_res": "📊 Resultados",
        "preco_est": "Precio estimado", "mudanca": "Cambio frente al precio actual",
        "retorno_anual": "Rentabilidad anual esperada", "preco_alvo": "Precio para la rentabilidad deseada",
        "preco_seg": "Precio con margen de seguridad", "falta": "Variación hasta el precio con margen",
        "sec_veredicto": "✅ Veredicto",
        "c_retorno": "Rentabilidad esperada ≥ rentabilidad deseada",
        "c_bench": "Rentabilidad esperada superior al S&P 500",
        "c_margem": "Precio actual ≤ precio con margen de seguridad",
        "c_cresc": "Ingresos proyectados crecen de media ≥ 5%/año",
        "c_margem_liq": "El margen neto proyectado no disminuye",
        "c_diluicao": "El nº de acciones no aumenta (sin dilución)",
        "c_pe": "P/E proyectado ≤ P/E actual (escenario prudente)",
        "v_bom": "Tiene sentido invertir: se cumplen la mayoría de los criterios.",
        "v_neutro": "Neutral: señales mixtas. Revisa las proyecciones o espera un mejor precio.",
        "v_mau": "No tiene sentido a este precio y con estos supuestos.",
        "pontuacao": "Puntuación",
        "grafico": "Precio estimado vs precio actual",
        "aviso": "⚠️ Modelo basado en tus supuestos, no una predicción. No es asesoramiento financiero.",
        "rodape": "Freenomics · Análisis de acciones individuales",
        "unidades": "Valores en millones (moneda de la empresa).",
    },
}[lang]


@st.cache_data(ttl=3600, show_spinner=False)
def carregar_dados(ticker):
    """Devolve (historico DataFrame, preco, dividendo_anual) ou None."""
    try:
        t = yf.Ticker(ticker)
        inc = t.income_stmt
        if inc is None or inc.empty:
            return None

        def linha(*nomes):
            for nome in nomes:
                if nome in inc.index:
                    return inc.loc[nome]
            return None

        rec = linha("Total Revenue", "Operating Revenue")
        luc = linha("Net Income", "Net Income Common Stockholders")
        acc = linha("Diluted Average Shares", "Basic Average Shares", "Ordinary Shares Number")
        if rec is None or luc is None:
            return None
        df = pd.DataFrame({"rec": rec, "luc": luc, "acc": acc if acc is not None else float("nan")})
        df.index = pd.to_datetime(df.index).year
        df = df.sort_index().dropna(subset=["rec", "luc"]).tail(4)

        hist = t.history(period="5d")
        preco = float(hist["Close"].dropna().iloc[-1]) if not hist.empty else None
        div = 0.0
        try:
            div = float(t.info.get("dividendRate") or 0.0)
        except Exception:
            pass
        return df, preco, div
    except Exception:
        return None


show_logo()
st.title(L["titulo"])
st.markdown(f"<p style='color:#C8D3DA;'>{L['subtitulo']}</p>", unsafe_allow_html=True)
demo_bar("analise")

# O modo demonstração pede para carregar o ticker de exemplo automaticamente
_auto_carregar = st.session_state.pop("aa_auto_load", False)

col_t, col_b = st.columns([3, 1])
with col_t:
    ticker = st.text_input(L["ticker"], value=st.session_state.get("aa_ticker", "AAPL")).strip().upper()
with col_b:
    st.write("")
    st.write("")
    if st.button(L["btn_carregar"], use_container_width=True, key="aa_carregar") or _auto_carregar:
        st.session_state["aa_ticker"] = ticker
        res = carregar_dados(ticker)
        if res is None:
            st.session_state.pop("aa_dados", None)
            st.error(L["erro_dados"])
        else:
            st.session_state["aa_dados"] = res
            st.session_state.pop("aa_proj", None)

if "aa_dados" not in st.session_state:
    st.stop()

df, preco_api, div_api = st.session_state["aa_dados"]
anos_hist = list(df.index)
rec_h = df["rec"].astype(float)
luc_h = df["luc"].astype(float)
acc_h = df["acc"].astype(float)
ultimo_acc = acc_h.dropna().iloc[-1] if acc_h.notna().any() else 1e9
margem_h = luc_h / rec_h * 100
eps_h = luc_h / acc_h
cresc_h = rec_h.pct_change() * 100

# ── Histórico ─────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["sec_hist"])
hist_tab = pd.DataFrame({
    L["receitas"]: (rec_h / 1e6).round(0),
    L["cresc_rec"]: cresc_h.round(1),
    L["lucro"]: (luc_h / 1e6).round(0),
    L["margem"]: margem_h.round(1),
    L["acoes"]: (acc_h / 1e6).round(1),
    L["eps"]: eps_h.round(2),
}).T
hist_tab.columns = [str(a) for a in anos_hist]
st.dataframe(hist_tab, use_container_width=True)
st.caption(L["unidades"])

# ── Parâmetros ────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["sec_param"])
c1, c2, c3, c4 = st.columns(4)
preco_atual = c1.number_input(L["preco_atual"], min_value=0.0, value=float(preco_api or 0.0), step=1.0, key="aa_preco")
retorno_desejado = c2.number_input(L["retorno_desejado"], value=15.0, step=1.0, key="aa_ret")
margem_seg = c3.number_input(L["margem_seg"], value=10.0, step=1.0, key="aa_mos")
benchmark = c4.number_input(L["benchmark"], value=10.7, step=0.1, key="aa_bench")

# ── Projeções ─────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["sec_proj"])
st.caption(L["dica_proj"])

ano_base = int(anos_hist[-1])
cagr = cresc_h.dropna().mean() if cresc_h.notna().sum() else 5.0
cagr = float(max(min(cagr, 30.0), -10.0))
margem_base = float(margem_h.iloc[-1])
pe_atual = float(preco_atual / eps_h.iloc[-1]) if preco_atual and eps_h.iloc[-1] > 0 else 20.0

# Colunas com chaves internas (independentes da língua); os rótulos vêm do column_config
if "aa_proj" not in st.session_state:
    st.session_state["aa_proj"] = pd.DataFrame({
        "cresc": [round(cagr, 1)] * N_ANOS,
        "margem": [round(margem_base, 1)] * N_ANOS,
        "acoes": [round(ultimo_acc / 1e6, 1)] * N_ANOS,
        "pe": [round(pe_atual, 1)] * N_ANOS,
        "div": [round(div_api, 2)] * N_ANOS,
    }, index=[str(ano_base + i + 1) for i in range(N_ANOS)])

proj_in = st.data_editor(
    st.session_state["aa_proj"], use_container_width=True, key="aa_editor",
    column_config={
        "cresc": st.column_config.NumberColumn(L["cresc_rec"]),
        "margem": st.column_config.NumberColumn(L["margem"]),
        "acoes": st.column_config.NumberColumn(L["acoes"]),
        "pe": st.column_config.NumberColumn(L["pe"]),
        "div": st.column_config.NumberColumn(L["dividendos"]),
    },
)

calcular = st.button(L["btn_calcular"], type="primary", use_container_width=True, key="aa_calcular")
if calcular:
    st.session_state["aa_calc"] = True
if not st.session_state.get("aa_calc"):
    st.stop()

# ── Cálculos ──────────────────────────────────────────────────
rec_p, luc_p, eps_p, preco_p = [], [], [], []
rec_prev = float(rec_h.iloc[-1]) / 1e6
for _, r in proj_in.iterrows():
    rec_prev = rec_prev * (1 + r["cresc"] / 100)
    luc = rec_prev * r["margem"] / 100
    acoes = max(r["acoes"], 1e-9)
    eps = luc / acoes
    rec_p.append(rec_prev); luc_p.append(luc); eps_p.append(eps)
    preco_p.append(eps * r["pe"])

divs_total = float(proj_in["div"].sum())
preco_final = preco_p[-1]
if preco_atual > 0 and (preco_final + divs_total) > 0:
    retorno_anual = ((preco_final + divs_total) / preco_atual) ** (1 / N_ANOS) - 1
else:
    retorno_anual = -1.0
preco_alvo = (preco_final + divs_total) / ((1 + retorno_desejado / 100) ** N_ANOS)
preco_com_margem = preco_alvo * (1 - margem_seg / 100)
var_ate_margem = (preco_com_margem / preco_atual - 1) if preco_atual else 0

anos_proj = list(proj_in.index)
mudanca = [(p / preco_atual - 1) * 100 if preco_atual else 0 for p in preco_p]

# Checklist
crescimento_medio = float(proj_in["cresc"].mean())
checks = [
    (L["c_retorno"], retorno_anual * 100 >= retorno_desejado),
    (L["c_bench"], retorno_anual * 100 > benchmark),
    (L["c_margem"], preco_atual <= preco_com_margem),
    (L["c_cresc"], crescimento_medio >= 5),
    (L["c_margem_liq"], proj_in["margem"].iloc[-1] >= margem_base - 0.05),
    (L["c_diluicao"], proj_in["acoes"].iloc[-1] <= ultimo_acc / 1e6 + 0.05),
    (L["c_pe"], proj_in["pe"].iloc[-1] <= pe_atual + 0.05),
]
pontos = sum(1 for _, ok in checks if ok)

st.markdown("---")
st.subheader(L["sec_res"])

st.session_state["export_analise_acao"] = {
    "ticker": st.session_state.get("aa_ticker", ticker),
    "retorno_anual": retorno_anual * 100, "preco_atual": preco_atual,
    "preco_alvo": preco_alvo, "preco_com_margem": preco_com_margem,
    "pontos": pontos, "total": len(checks),
}

if not auth.has_full_access():
    # Amostra gratuita: só o retorno anual esperado
    st.metric(L["retorno_anual"], f"{retorno_anual*100:.1f}%")
    auth.render_locked_section()
    st.stop()

tab_res = pd.DataFrame({
    L["receitas"]: [round(x, 0) for x in rec_p],
    L["lucro"]: [round(x, 0) for x in luc_p],
    L["eps"]: [round(x, 2) for x in eps_p],
    L["preco_est"]: [round(x, 2) for x in preco_p],
    L["mudanca"]: [f"{m:+.1f}%" for m in mudanca],
}, index=anos_proj).T
st.dataframe(tab_res, use_container_width=True)

m1, m2, m3, m4 = st.columns(4)
m1.metric(L["retorno_anual"], f"{retorno_anual*100:.1f}%", f"{retorno_anual*100 - benchmark:+.1f} pp vs S&P")
m2.metric(L["preco_atual"], f"{preco_atual:,.2f}")
m3.metric(L["preco_alvo"], f"{preco_alvo:,.2f}")
m4.metric(L["preco_seg"], f"{preco_com_margem:,.2f}", f"{var_ate_margem*100:+.1f}%")

fig = go.Figure()
fig.add_bar(x=anos_proj, y=preco_p, name=L["preco_est"], marker_color="#C29A4B")
fig.add_hline(y=preco_atual, line_dash="dash", line_color="#FAF8F3", annotation_text=L["preco_atual"])
fig.add_hline(y=preco_com_margem, line_dash="dot", line_color="#4FB8C4", annotation_text=L["preco_seg"])
style_fig(fig, titulo=L["grafico"], height=400, legenda=False)
st.plotly_chart(fig, use_container_width=True)

st.subheader(L["sec_veredicto"])
for texto, ok in checks:
    st.markdown(f"{'🟢' if ok else '🔴'} {texto}")
st.markdown(f"**{L['pontuacao']}: {pontos}/{len(checks)}**")
if pontos >= 6:
    st.success(L["v_bom"])
elif pontos >= 4:
    st.warning(L["v_neutro"])
else:
    st.error(L["v_mau"])

st.session_state["export_analise_acao"] = {
    "ticker": st.session_state.get("aa_ticker", ticker),
    "retorno_anual": retorno_anual * 100, "preco_atual": preco_atual,
    "preco_alvo": preco_alvo, "preco_com_margem": preco_com_margem,
    "pontos": pontos, "total": len(checks),
}

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
