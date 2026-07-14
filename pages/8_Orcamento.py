"""
Orçamento & Capacidade de Investir — Freenomics
Calcula a taxa de esforço/poupança a partir do rendimento e despesas mensais,
e guarda a capacidade de investir para a página de Objetivos reutilizar.
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, FIX_DROPDOWNS_JS

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

CATEGORIAS = ["habitacao", "alimentacao", "transportes", "subscricoes", "lazer", "saude", "outros"]
CORES = ["#0E2A3D", "#C29A4B", "#6B8E7F", "#A8453E", "#5C6B73", "#8E6BA8", "#B0B0B0"]

L = {
    "🇵🇹 Português": {
        "titulo": "Orçamento & Capacidade de Investir",
        "subtitulo": "Regista o teu rendimento e despesas mensais para descobrires a tua taxa de esforço e quanto podes investir todos os meses.",
        "sec_rendimento": "💶 Rendimento mensal",
        "salario": "Salário líquido", "outras_receitas": "Outras receitas (freelance, rendas, etc.)",
        "sec_despesas": "🧾 Despesas mensais",
        "habitacao": "🏠 Habitação (renda/prestação, condomínio)", "alimentacao": "🛒 Alimentação",
        "transportes": "🚗 Transportes", "subscricoes": "📺 Subscrições",
        "lazer": "🎉 Lazer & Restaurantes", "saude": "💊 Saúde", "outros": "📦 Outros",
        "btn_calcular": "📊 Calcular taxa de esforço",
        "resumo_titulo": "💡 Resumo",
        "tot_rendimento": "Rendimento total", "tot_despesas": "Despesas totais",
        "saldo": "Capacidade de investir/mês", "taxa_esforco": "Taxa de esforço",
        "taxa_poupanca": "Taxa de poupança",
        "dist_titulo": "Distribuição das despesas",
        "sem_saldo": "As tuas despesas são iguais ou superiores ao rendimento — não sobra capacidade para investir este mês.",
        "insight_boa": lambda p: f"Estás a poupar **{p:.0f}%** do teu rendimento — acima da regra geral de 20%. Excelente base para investir de forma consistente.",
        "insight_ok": lambda p: f"Estás a poupar **{p:.0f}%** do teu rendimento. A regra geral (50/30/20) sugere pelo menos 20% — estás perto, mas há margem para otimizar despesas.",
        "insight_baixa": lambda p: f"Estás a poupar apenas **{p:.0f}%** do teu rendimento — abaixo do recomendado (20%). Vale a pena rever as maiores categorias de despesa antes de aumentar o investimento.",
        "aviso": "⚠️ Estimativa baseada nos valores introduzidos — ajusta sempre que a tua situação mudar.",
        "rodape": "Freenomics · Planeamento de orçamento pessoal",
    },
    "🇬🇧 English": {
        "titulo": "Budget & Investing Capacity",
        "subtitulo": "Record your monthly income and expenses to find your savings rate and how much you can invest every month.",
        "sec_rendimento": "💶 Monthly income",
        "salario": "Net salary", "outras_receitas": "Other income (freelance, rent, etc.)",
        "sec_despesas": "🧾 Monthly expenses",
        "habitacao": "🏠 Housing (rent/mortgage, condo fees)", "alimentacao": "🛒 Groceries",
        "transportes": "🚗 Transport", "subscricoes": "📺 Subscriptions",
        "lazer": "🎉 Leisure & Dining", "saude": "💊 Health", "outros": "📦 Other",
        "btn_calcular": "📊 Calculate savings rate",
        "resumo_titulo": "💡 Summary",
        "tot_rendimento": "Total income", "tot_despesas": "Total expenses",
        "saldo": "Investing capacity/month", "taxa_esforco": "Expense ratio",
        "taxa_poupanca": "Savings rate",
        "dist_titulo": "Expense distribution",
        "sem_saldo": "Your expenses equal or exceed your income — there's no capacity left to invest this month.",
        "insight_boa": lambda p: f"You're saving **{p:.0f}%** of your income — above the general 20% rule. Great base to invest consistently.",
        "insight_ok": lambda p: f"You're saving **{p:.0f}%** of your income. The general rule (50/30/20) suggests at least 20% — you're close, but there's room to optimise expenses.",
        "insight_baixa": lambda p: f"You're only saving **{p:.0f}%** of your income — below the recommended 20%. Worth reviewing your biggest expense categories before increasing investment.",
        "aviso": "⚠️ Estimate based on the values entered — update whenever your situation changes.",
        "rodape": "Freenomics · Personal budget planning",
    },
    "🇫🇷 Français": {
        "titulo": "Budget & Capacité d'Investissement",
        "subtitulo": "Enregistrez vos revenus et dépenses mensuels pour découvrir votre taux d'épargne et combien vous pouvez investir chaque mois.",
        "sec_rendimento": "💶 Revenu mensuel",
        "salario": "Salaire net", "outras_receitas": "Autres revenus (freelance, loyers, etc.)",
        "sec_despesas": "🧾 Dépenses mensuelles",
        "habitacao": "🏠 Logement (loyer/prêt, charges)", "alimentacao": "🛒 Alimentation",
        "transportes": "🚗 Transport", "subscricoes": "📺 Abonnements",
        "lazer": "🎉 Loisirs & Restaurants", "saude": "💊 Santé", "outros": "📦 Autres",
        "btn_calcular": "📊 Calculer le taux d'épargne",
        "resumo_titulo": "💡 Résumé",
        "tot_rendimento": "Revenu total", "tot_despesas": "Dépenses totales",
        "saldo": "Capacité d'investir/mois", "taxa_esforco": "Taux d'effort",
        "taxa_poupanca": "Taux d'épargne",
        "dist_titulo": "Répartition des dépenses",
        "sem_saldo": "Vos dépenses égalent ou dépassent votre revenu — aucune capacité d'investir ce mois-ci.",
        "insight_boa": lambda p: f"Vous épargnez **{p:.0f}%** de votre revenu — au-dessus de la règle des 20%. Excellente base pour investir.",
        "insight_ok": lambda p: f"Vous épargnez **{p:.0f}%** de votre revenu. La règle générale (50/30/20) suggère au moins 20% — vous êtes proche, mais il y a de la marge.",
        "insight_baixa": lambda p: f"Vous n'épargnez que **{p:.0f}%** de votre revenu — en dessous des 20% recommandés. Il vaut la peine de revoir vos plus grosses dépenses.",
        "aviso": "⚠️ Estimation basée sur les valeurs saisies — mettez à jour si votre situation change.",
        "rodape": "Freenomics · Planification budgétaire personnelle",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Budget & Investitionsfähigkeit",
        "subtitulo": "Erfassen Sie Ihr monatliches Einkommen und Ihre Ausgaben, um Ihre Sparquote zu ermitteln.",
        "sec_rendimento": "💶 Monatliches Einkommen",
        "salario": "Nettogehalt", "outras_receitas": "Sonstige Einnahmen (Freelance, Miete usw.)",
        "sec_despesas": "🧾 Monatliche Ausgaben",
        "habitacao": "🏠 Wohnen (Miete/Kredit, Nebenkosten)", "alimentacao": "🛒 Lebensmittel",
        "transportes": "🚗 Transport", "subscricoes": "📺 Abonnements",
        "lazer": "🎉 Freizeit & Restaurants", "saude": "💊 Gesundheit", "outros": "📦 Sonstiges",
        "btn_calcular": "📊 Sparquote berechnen",
        "resumo_titulo": "💡 Zusammenfassung",
        "tot_rendimento": "Gesamteinkommen", "tot_despesas": "Gesamtausgaben",
        "saldo": "Investitionsfähigkeit/Monat", "taxa_esforco": "Ausgabenquote",
        "taxa_poupanca": "Sparquote",
        "dist_titulo": "Ausgabenverteilung",
        "sem_saldo": "Ihre Ausgaben entsprechen oder übersteigen Ihr Einkommen — diesen Monat bleibt keine Investitionskapazität.",
        "insight_boa": lambda p: f"Sie sparen **{p:.0f}%** Ihres Einkommens — über der allgemeinen 20%-Regel. Sehr gute Basis.",
        "insight_ok": lambda p: f"Sie sparen **{p:.0f}%** Ihres Einkommens. Die 50/30/20-Regel empfiehlt mindestens 20% — Sie sind nah dran.",
        "insight_baixa": lambda p: f"Sie sparen nur **{p:.0f}%** Ihres Einkommens — unter den empfohlenen 20%. Prüfen Sie Ihre größten Ausgabenkategorien.",
        "aviso": "⚠️ Schätzung basierend auf den eingegebenen Werten — aktualisieren Sie bei Änderungen.",
        "rodape": "Freenomics · Persönliche Budgetplanung",
    },
    "🇪🇸 Español": {
        "titulo": "Presupuesto & Capacidad de Inversión",
        "subtitulo": "Registra tus ingresos y gastos mensuales para descubrir tu tasa de ahorro y cuánto puedes invertir cada mes.",
        "sec_rendimento": "💶 Ingresos mensuales",
        "salario": "Salario neto", "outras_receitas": "Otros ingresos (freelance, alquileres, etc.)",
        "sec_despesas": "🧾 Gastos mensuales",
        "habitacao": "🏠 Vivienda (alquiler/hipoteca, comunidad)", "alimentacao": "🛒 Alimentación",
        "transportes": "🚗 Transporte", "subscricoes": "📺 Suscripciones",
        "lazer": "🎉 Ocio & Restaurantes", "saude": "💊 Salud", "outros": "📦 Otros",
        "btn_calcular": "📊 Calcular tasa de ahorro",
        "resumo_titulo": "💡 Resumen",
        "tot_rendimento": "Ingresos totales", "tot_despesas": "Gastos totales",
        "saldo": "Capacidad de invertir/mes", "taxa_esforco": "Tasa de esfuerzo",
        "taxa_poupanca": "Tasa de ahorro",
        "dist_titulo": "Distribución de gastos",
        "sem_saldo": "Tus gastos igualan o superan tus ingresos — no queda capacidad para invertir este mes.",
        "insight_boa": lambda p: f"Estás ahorrando **{p:.0f}%** de tu ingreso — por encima de la regla del 20%. Excelente base para invertir.",
        "insight_ok": lambda p: f"Estás ahorrando **{p:.0f}%** de tu ingreso. La regla general (50/30/20) sugiere al menos 20% — estás cerca.",
        "insight_baixa": lambda p: f"Solo estás ahorrando **{p:.0f}%** de tu ingreso — por debajo del 20% recomendado. Vale la pena revisar tus mayores gastos.",
        "aviso": "⚠️ Estimación basada en los valores introducidos — actualiza cuando cambie tu situación.",
        "rodape": "Freenomics · Planificación de presupuesto personal",
    },
}[lang]

show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

st.markdown("---")

# ── RENDIMENTO ────────────────────────────────────────────────
st.header(L["sec_rendimento"])
col_r1, col_r2 = st.columns(2)
with col_r1:
    salario = st.number_input(L["salario"], min_value=0.0, value=1500.0, step=50.0)
with col_r2:
    outras_receitas = st.number_input(L["outras_receitas"], min_value=0.0, value=0.0, step=50.0)

st.markdown("---")

# ── DESPESAS ──────────────────────────────────────────────────
st.header(L["sec_despesas"])
despesas = {}
defaults = {"habitacao": 500.0, "alimentacao": 300.0, "transportes": 100.0,
            "subscricoes": 30.0, "lazer": 150.0, "saude": 50.0, "outros": 100.0}
cols_d = st.columns(4)
for i, cat in enumerate(CATEGORIAS):
    with cols_d[i % 4]:
        despesas[cat] = st.number_input(L[cat], min_value=0.0, value=defaults[cat], step=10.0, key=f"desp_{cat}")

st.markdown("---")

calcular = st.button(L["btn_calcular"], type="primary", use_container_width=True)

if not calcular and "orcamento_resultado" not in st.session_state:
    st.stop()

if calcular:
    st.session_state["orcamento_resultado"] = {
        "salario": salario, "outras_receitas": outras_receitas,
        "despesas": dict(despesas),
    }

cfg = st.session_state.get("orcamento_resultado", {})
salario = cfg.get("salario", salario)
outras_receitas = cfg.get("outras_receitas", outras_receitas)
despesas = cfg.get("despesas", despesas)

total_rendimento = salario + outras_receitas
total_despesas = sum(despesas.values())
saldo = total_rendimento - total_despesas
taxa_esforco = (total_despesas / total_rendimento * 100) if total_rendimento > 0 else 0
taxa_poupanca = (saldo / total_rendimento * 100) if total_rendimento > 0 else 0

st.markdown("---")
st.subheader(L["resumo_titulo"])

def cor(v): return "#4CAF50" if v >= 0 else "#F44336"

def cartao(label, valor_str, cor_hex="#C29A4B"):
    return f"""<div style="background:#0E2A3D;border-radius:10px;padding:16px 18px;
        border-left:4px solid {cor_hex};margin-bottom:12px;">
        <p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 4px 0;">{label}</p>
        <p style="color:{cor_hex if cor_hex!='#C29A4B' else '#FAF8F3'};font-size:1.6rem;font-weight:700;margin:0;">{valor_str}</p>
    </div>"""

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(cartao(L["tot_rendimento"], f"€{total_rendimento:,.0f}"), unsafe_allow_html=True)
with c2: st.markdown(cartao(L["tot_despesas"], f"€{total_despesas:,.0f}"), unsafe_allow_html=True)
with c3: st.markdown(cartao(L["saldo"], f"€{saldo:,.0f}", cor(saldo)), unsafe_allow_html=True)
with c4: st.markdown(cartao(L["taxa_poupanca"], f"{taxa_poupanca:.0f}%", cor(taxa_poupanca)), unsafe_allow_html=True)

st.caption(f"{L['taxa_esforco']}: {taxa_esforco:.0f}%")

# ── GRÁFICO ───────────────────────────────────────────────────
st.subheader(L["dist_titulo"])
labels_pie = [L[k] for k, v in despesas.items() if v > 0]
values_pie = [v for v in despesas.values() if v > 0]
if values_pie:
    fig = go.Figure(go.Pie(labels=labels_pie, values=values_pie,
        marker=dict(colors=CORES[:len(values_pie)]), textinfo="label+percent", hole=0.4))
    fig.update_layout(paper_bgcolor="#FAF8F3", showlegend=False, height=340,
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig, use_container_width=True)

# ── INSIGHT ───────────────────────────────────────────────────
if saldo <= 0:
    st.warning(L["sem_saldo"])
elif taxa_poupanca >= 20:
    st.markdown(f"<div class='insight-box'>{L['insight_boa'](taxa_poupanca).replace('**','')}</div>", unsafe_allow_html=True)
elif taxa_poupanca >= 10:
    st.markdown(f"<div class='insight-box'>{L['insight_ok'](taxa_poupanca).replace('**','')}</div>", unsafe_allow_html=True)
else:
    st.markdown(f"<div class='insight-box'>{L['insight_baixa'](taxa_poupanca).replace('**','')}</div>", unsafe_allow_html=True)

# Guarda a capacidade de investir e o estado desta página para outras páginas reutilizarem
st.session_state["capacidade_mensal"] = max(saldo, 0)
st.session_state["export_orcamento"] = {
    "total_rendimento": total_rendimento, "total_despesas": total_despesas,
    "saldo_mensal": saldo, "taxa_esforco": round(taxa_esforco, 1),
    "taxa_poupanca": round(taxa_poupanca, 1),
    "categorias": [(L[k], v) for k, v in despesas.items()],
}

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
