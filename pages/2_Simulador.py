import streamlit as st
import numpy as np
import plotly.graph_objects as go
import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, PLOT_COLORS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Simulador de Investimento Regular",
        "subtitulo": "Descobre quanto acumulas ao investir uma quantia fixa todos os meses — o poder do juro composto.",
        "sec_config": "⚙️ Configura a simulação",
        "inv_inicial": "Investimento inicial (€)", "contrib": "Contribuição mensal (€)",
        "anos": "Horizonte temporal (anos)", "retorno": "Retorno anual esperado (%)",
        "inflacao": "Inflação estimada (%)", "dica": "💡 O S&P 500 teve um retorno histórico médio de ~10%/ano. Ajustando à inflação (~7% real).",
        "btn_simular": "📊 Simular",
        "grafico": "Evolução do capital ao longo do tempo",
        "capital_nominal": "Capital acumulado (nominal)", "total_investido": "Total investido",
        "capital_real": "Capital real (adj. inflação)",
        "marcos": "Marcos ao longo do tempo", "anos_label": "anos", "investido_label": "investido",
        "valor_final": "Valor final (nominal)", "valor_real": "Valor final (real)", "adj": "ajustado à inflação",
        "total_inv": "Total investido", "multiplicador": "Multiplicador",
        "aviso": "⚠️ Simulação baseada em retorno constante. Retornos reais variam — não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Calculadora de juro composto",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Ao investires **€{cm:.0f}/mês** durante **{anos} anos** com um retorno de **{r}%/ano**, transformas um total investido de **€{ti:,.0f}** em **€{vf:,.0f}** — os juros compostos geram **€{g:,.0f}** adicionais. Ajustando à inflação de {inf}%, o poder de compra real seria de **€{vr:,.0f}**.",
    },
    "🇬🇧 English": {
        "titulo": "Regular Investment Simulator",
        "subtitulo": "Find out how much you accumulate by investing a fixed amount every month.",
        "sec_config": "⚙️ Configure the simulation",
        "inv_inicial": "Initial investment (€)", "contrib": "Monthly contribution (€)",
        "anos": "Time horizon (years)", "retorno": "Expected annual return (%)",
        "inflacao": "Estimated inflation (%)", "dica": "💡 The S&P 500 had a historical average return of ~10%/year. Inflation-adjusted (~7% real).",
        "btn_simular": "📊 Simulate",
        "grafico": "Capital growth over time",
        "capital_nominal": "Accumulated capital (nominal)", "total_investido": "Total invested",
        "capital_real": "Real capital (inflation-adj.)",
        "marcos": "Milestones over time", "anos_label": "years", "investido_label": "invested",
        "valor_final": "Final value (nominal)", "valor_real": "Final value (real)", "adj": "inflation-adjusted",
        "total_inv": "Total invested", "multiplicador": "Multiplier",
        "aviso": "⚠️ Simulation based on constant return. Real returns vary — does not constitute financial advice.",
        "rodape": "Freenomics · Compound interest calculator",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"By investing **€{cm:.0f}/month** for **{anos} years** at **{r}%/year**, you turn **€{ti:,.0f}** invested into **€{vf:,.0f}** — compound interest generates an extra **€{g:,.0f}**. Adjusted for {inf}% inflation, real purchasing power would be **€{vr:,.0f}**.",
    },
    "🇫🇷 Français": {
        "titulo": "Simulateur d'Investissement Régulier",
        "subtitulo": "Découvrez combien vous accumulez en investissant chaque mois.",
        "sec_config": "⚙️ Configurez la simulation",
        "inv_inicial": "Investissement initial (€)", "contrib": "Contribution mensuelle (€)",
        "anos": "Horizon temporel (années)", "retorno": "Rendement annuel attendu (%)",
        "inflacao": "Inflation estimée (%)", "dica": "💡 Le S&P 500 a eu un rendement moyen historique de ~10%/an.",
        "btn_simular": "📊 Simuler",
        "grafico": "Évolution du capital dans le temps",
        "capital_nominal": "Capital accumulé (nominal)", "total_investido": "Total investi",
        "capital_real": "Capital réel (adj. inflation)",
        "marcos": "Jalons dans le temps", "anos_label": "ans", "investido_label": "investi",
        "valor_final": "Valeur finale (nominale)", "valor_real": "Valeur finale (réelle)", "adj": "ajusté à l'inflation",
        "total_inv": "Total investi", "multiplicador": "Multiplicateur",
        "aviso": "⚠️ Simulation basée sur un rendement constant — ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Calculateur d'intérêts composés",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"En investissant **€{cm:.0f}/mois** pendant **{anos} ans** à **{r}%/an**, vous transformez **€{ti:,.0f}** investis en **€{vf:,.0f}** — les intérêts composés génèrent **€{g:,.0f}** supplémentaires. Ajusté à {inf}% d'inflation : **€{vr:,.0f}**.",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Regelmäßiger Investitionssimulator",
        "subtitulo": "Berechnen Sie, wie viel Sie durch monatliche Einzahlungen ansparen.",
        "sec_config": "⚙️ Simulation konfigurieren",
        "inv_inicial": "Anfangsinvestition (€)", "contrib": "Monatlicher Beitrag (€)",
        "anos": "Anlagehorizont (Jahre)", "retorno": "Erwartete Jahresrendite (%)",
        "inflacao": "Geschätzte Inflation (%)", "dica": "💡 Der S&P 500 erzielte historisch ~10%/Jahr.",
        "btn_simular": "📊 Simulieren",
        "grafico": "Kapitalentwicklung über die Zeit",
        "capital_nominal": "Angespartes Kapital (nominal)", "total_investido": "Gesamt investiert",
        "capital_real": "Reales Kapital (inflationsbereinigt)",
        "marcos": "Meilensteine", "anos_label": "Jahre", "investido_label": "investiert",
        "valor_final": "Endwert (nominal)", "valor_real": "Endwert (real)", "adj": "inflationsbereinigt",
        "total_inv": "Gesamt investiert", "multiplicador": "Multiplikator",
        "aviso": "⚠️ Simulation auf Basis konstanter Rendite — stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Zinseszinsrechner",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Durch monatliche Einzahlungen von **€{cm:.0f}** über **{anos} Jahre** bei **{r}%/Jahr** werden aus **€{ti:,.0f}** investiertem Kapital **€{vf:,.0f}** — der Zinseszins generiert **€{g:,.0f}**. Inflationsbereinigt ({inf}%): **€{vr:,.0f}**.",
    },
    "🇪🇸 Español": {
        "titulo": "Simulador de Inversión Regular",
        "subtitulo": "Descubre cuánto acumulas invirtiendo una cantidad fija cada mes.",
        "sec_config": "⚙️ Configura la simulación",
        "inv_inicial": "Inversión inicial (€)", "contrib": "Contribución mensual (€)",
        "anos": "Horizonte temporal (años)", "retorno": "Rentabilidad anual esperada (%)",
        "inflacao": "Inflación estimada (%)", "dica": "💡 El S&P 500 tuvo una rentabilidad histórica media de ~10%/año.",
        "btn_simular": "📊 Simular",
        "grafico": "Evolución del capital a lo largo del tiempo",
        "capital_nominal": "Capital acumulado (nominal)", "total_investido": "Total invertido",
        "capital_real": "Capital real (adj. inflación)",
        "marcos": "Hitos a lo largo del tiempo", "anos_label": "años", "investido_label": "invertido",
        "valor_final": "Valor final (nominal)", "valor_real": "Valor final (real)", "adj": "ajustado a inflación",
        "total_inv": "Total invertido", "multiplicador": "Multiplicador",
        "aviso": "⚠️ Simulación basada en rentabilidad constante — no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Calculadora de interés compuesto",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Al invertir **€{cm:.0f}/mes** durante **{anos} años** con **{r}%/año**, conviertes **€{ti:,.0f}** invertidos en **€{vf:,.0f}** — el interés compuesto genera **€{g:,.0f}** adicionales. Ajustando a {inf}% de inflación: **€{vr:,.0f}**.",
    },
}.get(lang, {})

show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── FORMULÁRIO ────────────────────────────────────────────────
st.header(L["sec_config"])

col1, col2 = st.columns(2)
with col1:
    inv_inicial = st.number_input(L["inv_inicial"], value=1000, step=100, min_value=0)
    contrib     = st.number_input(L["contrib"],     value=200,  step=50,  min_value=0)
    anos        = st.slider(L["anos"], 1, 40, 10)
with col2:
    retorno  = st.slider(L["retorno"],  1.0, 20.0, 8.0, step=0.5)
    inflacao = st.slider(L["inflacao"], 0.0, 6.0,  2.5, step=0.5)
    st.caption(L["dica"])

simular = st.button(L["btn_simular"], type="primary", use_container_width=True)

if not simular and "sim_resultado" not in st.session_state:
    st.stop()

if simular:
    st.session_state["sim_resultado"] = {
        "inv_inicial": inv_inicial, "contrib": contrib,
        "anos": anos, "retorno": retorno, "inflacao": inflacao,
    }

cfg      = st.session_state.get("sim_resultado", {})
inv_ini  = cfg.get("inv_inicial", inv_inicial)
contrib  = cfg.get("contrib", contrib)
anos     = cfg.get("anos", anos)
retorno  = cfg.get("retorno", retorno)
inflacao = cfg.get("inflacao", inflacao)

# ── CÁLCULO ───────────────────────────────────────────────────
meses = anos * 12
r_m      = retorno / 100 / 12
r_real_m = ((1 + retorno/100) / (1 + inflacao/100) - 1) / 12

vn, vr, ti = [], [], []
cn, cr, inv_acc = inv_ini, inv_ini, inv_ini
for _ in range(meses):
    cn = cn*(1+r_m)+contrib; cr = cr*(1+r_real_m)+contrib; inv_acc += contrib
    vn.append(cn); vr.append(cr); ti.append(inv_acc)

vf = vn[-1]; vreal = vr[-1]; tinv = ti[-1]; ganho = vf - tinv; mult = vf/tinv if tinv>0 else 1

st.markdown("---")

# ── MÉTRICAS ──────────────────────────────────────────────────
def cartao(label, valor_str, sub_str=None, sub_cor="#C29A4B"):
    html  = '<div style="background:#0E2A3D;border-radius:10px;padding:16px 18px;border-left:4px solid #C29A4B;margin-bottom:12px;">'
    html += '<p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 4px 0;">' + label + '</p>'
    html += '<p style="color:#FAF8F3;font-size:1.8rem;font-weight:700;margin:0;">' + valor_str + '</p>'
    if sub_str:
        html += '<p style="color:' + sub_cor + ';font-size:0.95rem;margin:4px 0 0 0;">' + sub_str + '</p>'
    html += '</div>'
    return html

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(cartao(L["valor_final"], f"€{vf:,.0f}", f"+€{ganho:,.0f}", "#4CAF50"), unsafe_allow_html=True)
with c2: st.markdown(cartao(L["valor_real"],  f"€{vreal:,.0f}", L["adj"]), unsafe_allow_html=True)
with c3: st.markdown(cartao(L["total_inv"],   f"€{tinv:,.0f}"), unsafe_allow_html=True)
with c4: st.markdown(cartao(L["multiplicador"], f"{mult:.1f}x", f"{retorno}%/{L['anos_label']}"), unsafe_allow_html=True)

# ── GRÁFICO ───────────────────────────────────────────────────
st.subheader(L["grafico"])
labels = [m/12 for m in range(1, meses+1)]
fig = go.Figure()
fig.add_trace(go.Scatter(x=labels, y=vn, name=L["capital_nominal"], line=dict(color=PLOT_COLORS[0], width=2.5)))
fig.add_trace(go.Scatter(x=labels, y=ti, name=L["total_investido"],  line=dict(color=PLOT_COLORS[1], width=2, dash="dash")))
fig.add_trace(go.Scatter(x=labels, y=vr, name=L["capital_real"],     line=dict(color=PLOT_COLORS[2], width=1.5, dash="dot")))
fig.update_layout(plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
    yaxis_title=f"€", xaxis_title=L["anos_label"],
    hovermode="x unified", height=430,
    legend=dict(orientation="h", yanchor="bottom", y=1.02))
st.plotly_chart(fig, use_container_width=True)

# ── MARCOS ────────────────────────────────────────────────────
st.subheader(L["marcos"])
marcos = [m for m in [5, 10, 15, 20, 25, 30] if m <= anos]
if marcos:
    cols = st.columns(len(marcos))
    for col, ano in zip(cols, marcos):
        idx = ano*12-1
        col.markdown(cartao(f"{ano} {L['anos_label']}", f"€{vn[idx]:,.0f}",
            f"{L['investido_label']}: €{ti[idx]:,.0f}"), unsafe_allow_html=True)

# ── INSIGHT ───────────────────────────────────────────────────
def render(t): return re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", t)
txt = L["insight"](contrib, anos, retorno, tinv, vf, ganho, inflacao, vreal)
st.markdown(f"<div class='insight-box'>{render(txt)}</div>", unsafe_allow_html=True)
st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
