"""
Objetivos Financeiros · Freenomics
Define vários objetivos (casa, fundo de emergência, etc.) e compara cenários de
retorno para perceber quanto tempo demoras a atingir cada um.
"""

import streamlit as st
import streamlit.components.v1 as components
import plotly.graph_objects as go
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo, demo_bar, next_step, capacidade_mensal, patrimonio_total
import auth
from translations import CSS, PLOT_COLORS, FIX_DROPDOWNS_JS, style_fig

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

CENARIOS_ALL = {
    "🇵🇹 Português": {"Poupança (2%/ano)": 0.02, "Conservador (4%/ano)": 0.04,
                       "Moderado (6%/ano)": 0.06, "Ações (8%/ano)": 0.08},
    "🇬🇧 English": {"Savings (2%/yr)": 0.02, "Conservative (4%/yr)": 0.04,
                    "Moderate (6%/yr)": 0.06, "Equities (8%/yr)": 0.08},
    "🇫🇷 Français": {"Épargne (2%/an)": 0.02, "Conservateur (4%/an)": 0.04,
                     "Modéré (6%/an)": 0.06, "Actions (8%/an)": 0.08},
    "🇩🇪 Deutsch": {"Sparkonto (2%/Jahr)": 0.02, "Konservativ (4%/Jahr)": 0.04,
                    "Moderat (6%/Jahr)": 0.06, "Aktien (8%/Jahr)": 0.08},
    "🇪🇸 Español": {"Ahorro (2%/año)": 0.02, "Conservador (4%/año)": 0.04,
                    "Moderado (6%/año)": 0.06, "Acciones (8%/año)": 0.08},
}
CENARIOS = CENARIOS_ALL[lang]
# Chave interna do cenário = taxa anual (independente da língua); o nome traduz-se só na apresentação
NOME_CENARIO = {taxa: nome for nome, taxa in CENARIOS.items()}
TAXAS = list(NOME_CENARIO.keys())
CENARIOS_POR_LANG = {lg: {taxa: nome for nome, taxa in d.items()} for lg, d in CENARIOS_ALL.items()}

EXTRA = {
    "🇵🇹 Português": {"ex_nome": "ex: Casa"},
    "🇬🇧 English": {"ex_nome": "e.g. House"},
    "🇫🇷 Français": {"ex_nome": "ex : Maison"},
    "🇩🇪 Deutsch": {"ex_nome": "z. B. Haus"},
    "🇪🇸 Español": {"ex_nome": "ej: Casa"},
}
LX = EXTRA[lang]

L = {
    "🇵🇹 Português": {
        "titulo": "Objetivos Financeiros",
        "subtitulo": "Define os teus objetivos (casa, fundo de emergência, viagem...) e descobre quanto tempo demoras a atingi-los em diferentes cenários de retorno.",
        "sec_config": "🎯 Os teus objetivos",
        "nome_label": "Nome do objetivo", "valor_objetivo_label": "Valor a atingir (€)",
        "valor_atual_label": "Já tens poupado (€)", "alocacao_label": "Quanto alocas por mês (€)",
        "btn_add": "➕ Adicionar objetivo",
        "btn_calcular": "🎯 Calcular plano",
        "capacidade_info": lambda v: f"💡 Na página de Orçamento calculaste uma capacidade de investir de €{v:,.0f}/mês.",
        "sem_capacidade": "💡 Ainda não calculaste a tua capacidade de investir. Visita a página de Orçamento para uma sugestão automática.",
        "alocado_total": "Total alocado por mês", "excede_aviso": "⚠️ O total alocado excede a tua capacidade de investir mensal.",
        "progresso": "Progresso atual", "objetivo_titulo": "Objetivo",
        "tempo_estimado": "Tempo estimado", "anos_label": "anos", "meses_label": "meses",
        "nao_atingivel": "Não atingível com esta alocação (aumenta o valor mensal).",
        "ja_atingido": "🎉 Objetivo já atingido!",
        "cenarios_titulo": "Comparação de cenários de retorno",
        "insight": lambda nome, cenario, anos, meses, valor: f"No cenário **{cenario}**, atinges o objetivo **{nome}** em **{anos} anos e {meses} meses**, investindo €{valor:,.0f}/mês.",
        "aviso": "⚠️ Simulação baseada em retornos constantes, retornos reais variam. Não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Planeamento de objetivos financeiros",
    },
    "🇬🇧 English": {
        "titulo": "Financial Goals",
        "subtitulo": "Set your goals (house, emergency fund, trip...) and find out how long they take to reach under different return scenarios.",
        "sec_config": "🎯 Your goals",
        "nome_label": "Goal name", "valor_objetivo_label": "Target amount (€)",
        "valor_atual_label": "Already saved (€)", "alocacao_label": "Monthly allocation (€)",
        "btn_add": "➕ Add goal",
        "btn_calcular": "🎯 Calculate plan",
        "capacidade_info": lambda v: f"💡 On the Budget page you calculated an investing capacity of €{v:,.0f}/month.",
        "sem_capacidade": "💡 You haven't calculated your investing capacity yet. Visit the Budget page for an automatic suggestion.",
        "alocado_total": "Total allocated per month", "excede_aviso": "⚠️ The total allocated exceeds your monthly investing capacity.",
        "progresso": "Current progress", "objetivo_titulo": "Goal",
        "tempo_estimado": "Estimated time", "anos_label": "years", "meses_label": "months",
        "nao_atingivel": "Not reachable with this allocation (increase the monthly amount).",
        "ja_atingido": "🎉 Goal already reached!",
        "cenarios_titulo": "Return scenario comparison",
        "insight": lambda nome, cenario, anos, meses, valor: f"Under the **{cenario}** scenario, you reach **{nome}** in **{anos} years and {meses} months**, investing €{valor:,.0f}/month.",
        "aviso": "⚠️ Simulation based on constant returns, real returns vary. Does not constitute financial advice.",
        "rodape": "Freenomics · Financial goal planning",
    },
    "🇫🇷 Français": {
        "titulo": "Objectifs Financiers",
        "subtitulo": "Définissez vos objectifs (maison, fonds d'urgence, voyage...) et découvrez le temps nécessaire selon différents scénarios.",
        "sec_config": "🎯 Vos objectifs",
        "nome_label": "Nom de l'objectif", "valor_objetivo_label": "Montant cible (€)",
        "valor_atual_label": "Déjà épargné (€)", "alocacao_label": "Allocation mensuelle (€)",
        "btn_add": "➕ Ajouter un objectif",
        "btn_calcular": "🎯 Calculer le plan",
        "capacidade_info": lambda v: f"💡 Sur la page Budget, vous avez calculé une capacité d'investissement de €{v:,.0f}/mois.",
        "sem_capacidade": "💡 Vous n'avez pas encore calculé votre capacité d'investir. Visitez la page Budget.",
        "alocado_total": "Total alloué par mois", "excede_aviso": "⚠️ Le total alloué dépasse votre capacité mensuelle.",
        "progresso": "Progrès actuel", "objetivo_titulo": "Objectif",
        "tempo_estimado": "Temps estimé", "anos_label": "ans", "meses_label": "mois",
        "nao_atingivel": "Non atteignable avec cette allocation (augmentez le montant mensuel).",
        "ja_atingido": "🎉 Objectif déjà atteint!",
        "cenarios_titulo": "Comparaison des scénarios de rendement",
        "insight": lambda nome, cenario, anos, meses, valor: f"Dans le scénario **{cenario}**, vous atteignez **{nome}** en **{anos} ans et {meses} mois**, en investissant €{valor:,.0f}/mois.",
        "aviso": "⚠️ Simulation basée sur des rendements constants, ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Planification d'objectifs financiers",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Finanzielle Ziele",
        "subtitulo": "Legen Sie Ihre Ziele fest (Haus, Notfallfonds, Reise...) und finden Sie heraus, wie lange es unter verschiedenen Renditeszenarien dauert.",
        "sec_config": "🎯 Ihre Ziele",
        "nome_label": "Zielname", "valor_objetivo_label": "Zielbetrag (€)",
        "valor_atual_label": "Bereits gespart (€)", "alocacao_label": "Monatliche Zuweisung (€)",
        "btn_add": "➕ Ziel hinzufügen",
        "btn_calcular": "🎯 Plan berechnen",
        "capacidade_info": lambda v: f"💡 Auf der Budget-Seite haben Sie eine Investitionsfähigkeit von €{v:,.0f}/Monat berechnet.",
        "sem_capacidade": "💡 Sie haben Ihre Investitionsfähigkeit noch nicht berechnet. Besuchen Sie die Budget-Seite.",
        "alocado_total": "Gesamt zugewiesen pro Monat", "excede_aviso": "⚠️ Die Gesamtzuweisung übersteigt Ihre monatliche Kapazität.",
        "progresso": "Aktueller Fortschritt", "objetivo_titulo": "Ziel",
        "tempo_estimado": "Geschätzte Zeit", "anos_label": "Jahre", "meses_label": "Monate",
        "nao_atingivel": "Mit dieser Zuweisung nicht erreichbar (monatlichen Betrag erhöhen).",
        "ja_atingido": "🎉 Ziel bereits erreicht!",
        "cenarios_titulo": "Vergleich der Renditeszenarien",
        "insight": lambda nome, cenario, anos, meses, valor: f"Im Szenario **{cenario}** erreichen Sie **{nome}** in **{anos} Jahren und {meses} Monaten**, mit €{valor:,.0f}/Monat.",
        "aviso": "⚠️ Simulation basierend auf konstanten Renditen und stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Finanzzielplanung",
    },
    "🇪🇸 Español": {
        "titulo": "Objetivos Financieros",
        "subtitulo": "Define tus objetivos (casa, fondo de emergencia, viaje...) y descubre cuánto tiempo tardas en diferentes escenarios de rentabilidad.",
        "sec_config": "🎯 Tus objetivos",
        "nome_label": "Nombre del objetivo", "valor_objetivo_label": "Monto objetivo (€)",
        "valor_atual_label": "Ya ahorrado (€)", "alocacao_label": "Asignación mensual (€)",
        "btn_add": "➕ Añadir objetivo",
        "btn_calcular": "🎯 Calcular plan",
        "capacidade_info": lambda v: f"💡 En la página de Presupuesto calculaste una capacidad de inversión de €{v:,.0f}/mes.",
        "sem_capacidade": "💡 Aún no has calculado tu capacidad de inversión. Visita la página de Presupuesto.",
        "alocado_total": "Total asignado por mes", "excede_aviso": "⚠️ El total asignado excede tu capacidad mensual.",
        "progresso": "Progreso actual", "objetivo_titulo": "Objetivo",
        "tempo_estimado": "Tiempo estimado", "anos_label": "años", "meses_label": "meses",
        "nao_atingivel": "No alcanzable con esta asignación (aumenta el monto mensual).",
        "ja_atingido": "🎉 ¡Objetivo ya alcanzado!",
        "cenarios_titulo": "Comparación de escenarios de rentabilidad",
        "insight": lambda nome, cenario, anos, meses, valor: f"En el escenario **{cenario}**, alcanzas **{nome}** en **{anos} años y {meses} meses**, invirtiendo €{valor:,.0f}/mes.",
        "aviso": "⚠️ Simulación basada en rentabilidades constantes, no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Planificación de objetivos financieros",
    },
}[lang]

show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])
demo_bar("objetivos")

capacidade = capacidade_mensal()
patrimonio_guardado = patrimonio_total()
if capacidade is not None:
    st.info(L["capacidade_info"](capacidade))
else:
    st.info(L["sem_capacidade"])

st.markdown("---")

# ── LISTA DE OBJETIVOS ────────────────────────────────────────
# Valores iniciais por defeito: alocação = capacidade de investir do Orçamento (se existir)
# e "Já tens poupado" = património líquido da página Património (se existir).
_aloc_defeito = float(round(capacidade)) if capacidade else 100.0
if "objetivos" not in st.session_state:
    _at_defeito = float(round(patrimonio_guardado)) if patrimonio_guardado and patrimonio_guardado > 0 else 0.0
    st.session_state.objetivos = [
        {"nome": "", "valor_objetivo": 10000.0, "valor_atual": _at_defeito, "alocacao": _aloc_defeito,
         "_s_at": _at_defeito, "_s_al": _aloc_defeito},
    ]
else:
    # Objetivo inicial ainda por mexer (sem nome): atualiza os valores por defeito se entretanto
    # o utilizador preencheu o Orçamento ou o Património.
    _objs = st.session_state.objetivos
    if len(_objs) == 1 and not _objs[0]["nome"]:
        _o = _objs[0]
        if _o["alocacao"] in (100.0, _o.get("_s_al")) and capacidade:
            _o["alocacao"] = _o["_s_al"] = float(round(capacidade))
        if _o["valor_atual"] in (0.0, _o.get("_s_at")) and patrimonio_guardado and patrimonio_guardado > 0:
            _o["valor_atual"] = _o["_s_at"] = float(round(patrimonio_guardado))

st.header(L["sec_config"])
_PAT_INFO = {
    "🇵🇹 Português": lambda v: f"💎 Usámos o teu património líquido (€{v:,.0f}) como valor já poupado no primeiro objetivo. Ajusta se só parte for para ele.",
    "🇬🇧 English": lambda v: f"💎 We used your net worth (€{v:,.0f}) as the amount already saved in the first goal. Adjust it if only part of it is for this goal.",
    "🇫🇷 Français": lambda v: f"💎 Nous avons utilisé votre patrimoine net (€{v:,.0f}) comme montant déjà épargné pour le premier objectif. Ajustez si seule une partie lui est destinée.",
    "🇩🇪 Deutsch": lambda v: f"💎 Wir haben dein Nettovermögen (€{v:,.0f}) als bereits gespartes Geld für das erste Ziel übernommen. Passe es an, wenn nur ein Teil dafür gedacht ist.",
    "🇪🇸 Español": lambda v: f"💎 Hemos usado tu patrimonio neto (€{v:,.0f}) como importe ya ahorrado en el primer objetivo. Ajústalo si solo una parte es para él.",
}
if (patrimonio_guardado and patrimonio_guardado > 0 and len(st.session_state.objetivos) == 1
        and not st.session_state.objetivos[0]["nome"]
        and st.session_state.objetivos[0]["valor_atual"] == st.session_state.objetivos[0].get("_s_at")):
    st.caption(_PAT_INFO[lang](patrimonio_guardado))
remover = None
for i, obj in enumerate(st.session_state.objetivos):
    c1, c2, c3, c4, c5 = st.columns([2.5, 2, 2, 2, 0.4])
    with c1:
        st.session_state.objetivos[i]["nome"] = st.text_input(
            L["nome_label"], value=obj["nome"], key=f"obj_nome_{i}", placeholder=LX["ex_nome"])
    with c2:
        st.session_state.objetivos[i]["valor_objetivo"] = st.number_input(
            L["valor_objetivo_label"], min_value=0.0, value=float(obj["valor_objetivo"]),
            step=500.0, key=f"obj_valor_{i}")
    with c3:
        st.session_state.objetivos[i]["valor_atual"] = st.number_input(
            L["valor_atual_label"], min_value=0.0, value=float(obj["valor_atual"]),
            step=100.0, key=f"obj_atual_{i}")
    with c4:
        st.session_state.objetivos[i]["alocacao"] = st.number_input(
            L["alocacao_label"], min_value=0.0, value=float(obj["alocacao"]),
            step=25.0, key=f"obj_aloc_{i}")
    with c5:
        st.markdown("<br>", unsafe_allow_html=True)
        if len(st.session_state.objetivos) > 1:
            if st.button("🗑️", key=f"obj_rm_{i}"):
                remover = i

if remover is not None:
    st.session_state.objetivos.pop(remover)
    st.rerun()

if st.button(L["btn_add"]):
    # Nova alocação por defeito: o que ainda sobra da capacidade de investir (se existir)
    _novo_aloc = 100.0
    if capacidade:
        _sobra = capacidade - sum(o["alocacao"] for o in st.session_state.objetivos)
        _novo_aloc = float(round(_sobra)) if _sobra > 0 else 0.0
    st.session_state.objetivos.append(
        {"nome": "", "valor_objetivo": 10000.0, "valor_atual": 0.0, "alocacao": _novo_aloc})
    st.rerun()

total_alocado = sum(o["alocacao"] for o in st.session_state.objetivos)
st.caption(f"{L['alocado_total']}: €{total_alocado:,.0f}")
if capacidade is not None and total_alocado > capacidade:
    st.warning(L["excede_aviso"])

st.markdown("---")

calcular = st.button(L["btn_calcular"], type="primary", use_container_width=True)

if not calcular and "objetivos_resultado" not in st.session_state:
    st.stop()

if calcular:
    st.session_state["objetivos_resultado"] = {
        "objetivos": [o.copy() for o in st.session_state.objetivos if o["nome"]],
    }

cfg = st.session_state.get("objetivos_resultado", {})
objetivos_calc = cfg.get("objetivos", [o for o in st.session_state.objetivos if o["nome"]])

if not objetivos_calc:
    st.stop()

# ── CÁLCULO: MESES ATÉ ATINGIR O OBJETIVO EM CADA CENÁRIO ─────
def meses_ate_objetivo(valor_atual, valor_objetivo, contrib_mensal, taxa_anual, limite_meses=600):
    if valor_atual >= valor_objetivo:
        return 0
    if contrib_mensal <= 0 and taxa_anual == 0:
        return None
    r_m = taxa_anual / 12
    capital = valor_atual
    for m in range(1, limite_meses + 1):
        capital = capital * (1 + r_m) + contrib_mensal
        if capital >= valor_objetivo:
            return m
    return None

def formatar_tempo(meses):
    if meses is None:
        return None
    anos, resto = divmod(meses, 12)
    return anos, resto

export_objetivos = []
_full = auth.has_full_access()

for obj in objetivos_calc:
    nome = obj["nome"]
    valor_objetivo = obj["valor_objetivo"]
    valor_atual = obj["valor_atual"]
    alocacao = obj["alocacao"]

    st.markdown("---")
    st.subheader(f"🎯 {nome}")

    progresso = min(valor_atual / valor_objetivo, 1.0) if valor_objetivo > 0 else 0
    st.progress(progresso, text=f"{L['progresso']}: €{valor_atual:,.0f} / €{valor_objetivo:,.0f} ({progresso*100:.0f}%)")

    tempos = {}
    for taxa in TAXAS:
        meses = meses_ate_objetivo(valor_atual, valor_objetivo, alocacao, taxa)
        tempos[taxa] = meses  # chave interna = taxa

    # Cenário de referência "Moderado" (ou o primeiro disponível se não existir)
    taxa_ref = 0.06 if 0.06 in tempos else list(tempos.keys())[0]
    meses_ref = tempos[taxa_ref]

    # Amostra gratuita: só o cenário de referência; os 4 cenários completos são para subscritores
    taxas_mostrar = tempos if _full else {taxa_ref: tempos[taxa_ref]}
    cols_c = st.columns(len(taxas_mostrar))
    for col, (taxa_c, meses) in zip(cols_c, taxas_mostrar.items()):
        with col:
            st.markdown(f"**{NOME_CENARIO[taxa_c]}**")
            if meses is None:
                st.markdown(f"<div class='risco-box risco-alto'>{L['nao_atingivel']}</div>", unsafe_allow_html=True)
            elif meses == 0:
                st.markdown(f"<div class='insight-box'>{L['ja_atingido']}</div>", unsafe_allow_html=True)
            else:
                anos, resto = formatar_tempo(meses)
                st.markdown(f"""<div style="background:#0E2A3D;border-radius:10px;padding:14px 16px;
                    border-left:4px solid #C29A4B;">
                    <p style="color:#C8D3DA;font-size:0.8rem;margin:0 0 2px 0;">{L['tempo_estimado']}</p>
                    <p style="color:#FAF8F3;font-size:1.3rem;font-weight:700;margin:0;">{anos} {L['anos_label']}, {resto} {L['meses_label']}</p>
                </div>""", unsafe_allow_html=True)

    # Insight (só para subscritores)
    if _full and meses_ref and meses_ref > 0:
        anos_r, resto_r = formatar_tempo(meses_ref)
        st.markdown(f"<div class='insight-box'>{L['insight'](nome, NOME_CENARIO[taxa_ref], anos_r, resto_r, alocacao).replace('**','')}</div>",
                    unsafe_allow_html=True)

    export_objetivos.append({
        "nome": nome, "valor_objetivo": valor_objetivo, "valor_atual": valor_atual,
        "alocacao": alocacao, "tempos_meses": tempos,
    })

st.markdown("---")
if _full:
    # ── GRÁFICO COMPARATIVO (apenas se houver mais de um objetivo) ─
    if len(objetivos_calc) > 1:
        st.subheader(L["cenarios_titulo"])
        fig = go.Figure()
        for i, obj in enumerate(export_objetivos):
            y_vals = [obj["tempos_meses"][c] / 12 if obj["tempos_meses"][c] is not None else None for c in TAXAS]
            fig.add_trace(go.Bar(x=[NOME_CENARIO[c] for c in TAXAS], y=y_vals, name=obj["nome"],
                                  marker_color=PLOT_COLORS[i % len(PLOT_COLORS)], opacity=0.85))
        style_fig(fig, height=400, yaxis_title=L["anos_label"], barmode="group")
        st.plotly_chart(fig, use_container_width=True)
else:
    auth.render_locked_section()

# Guarda o estado desta página para a página de Exportar reutilizar
st.session_state["export_objetivos"] = {
    "objetivos": export_objetivos,
    # nomes dos cenários por língua (chave = taxa anual); o relatório usa a língua escolhida ao exportar
    "cenarios_por_lang": CENARIOS_POR_LANG,
}

st.markdown("---")
next_step("objetivos")

st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
