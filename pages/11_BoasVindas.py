"""
Boas-vindas · Freenomics
Primeira página que qualquer pessoa vê ao abrir a app: missão, visão e
como o Freenomics ajuda a organizar a vida financeira rumo à liberdade financeira.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo, demo_bar, kcontainer
from translations import CSS, FIX_DROPDOWNS_JS

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Bem-vindo(a) ao Freenomics",
        "subtitulo": "A tua bússola para organizares a vida financeira e caminhares, passo a passo, rumo à liberdade financeira.",
        "missao_titulo": "🎯 A nossa missão",
        "missao_texto": "Dar a qualquer pessoa, independentemente do que sabe sobre finanças, ferramentas simples e claras para perceber onde está o seu dinheiro, quanto pode investir e quanto tempo falta para atingir os seus objetivos.",
        "visao_titulo": "🔭 A nossa visão",
        "visao_texto": "Um mundo onde a literacia financeira não é um privilégio de quem estudou economia, mas um hábito acessível a toda a gente, com decisões informadas em vez de medo ou adivinhação.",
        "valores_titulo": "🧭 Como pensamos",
        "valores": [
            ("🔒 Privacidade em primeiro lugar", "Os teus dados financeiros ficam no teu browser. Nunca guardamos rendimentos, despesas ou carteiras nos nossos servidores."),
            ("📊 Clareza acima de tudo", "Sem jargão desnecessário: números, gráficos e explicações simples para decisões reais."),
            ("🌱 Progresso, não perfeição", "Não prometemos ficares rico da noite para o dia. Ajudamos-te a dar o próximo passo certo, de forma consistente."),
        ],
        "como_titulo": "🛠️ O que encontras aqui",
        "como": [
            "Orçamento: descobre a tua taxa de poupança e capacidade de investir",
            "Objetivos: simula quanto tempo falta para cada objetivo em vários cenários",
            "Dashboard, Comparador e Simulador: analisa e testa a tua carteira de investimentos",
            "Dividendos, Risco e Notícias: acompanha o que importa sobre os teus ativos",
            "Exportar Relatório: leva a tua análise contigo em PDF ou Excel",
        ],
        "btn_comecar": "🚀 Começar agora",
        "btn_precos": "✨ Ver planos",
        "aviso": "⚠️ O Freenomics é uma ferramenta educativa de organização financeira. Não constitui aconselhamento financeiro, fiscal ou de investimento.",
        "rodape": "Freenomics · Dinheiro, mentalidade e liberdade financeira",
    },
    "🇬🇧 English": {
        "titulo": "Welcome to Freenomics",
        "subtitulo": "Your compass for organizing your finances and moving, step by step, towards financial freedom.",
        "missao_titulo": "🎯 Our mission",
        "missao_texto": "Give everyone, regardless of financial background, simple and clear tools to understand where their money goes, how much they can invest, and how long it takes to reach their goals.",
        "visao_titulo": "🔭 Our vision",
        "visao_texto": "A world where financial literacy isn't a privilege reserved for those who studied economics, but an accessible habit for everyone, built on informed decisions instead of fear or guesswork.",
        "valores_titulo": "🧭 How we think",
        "valores": [
            ("🔒 Privacy first", "Your financial data stays in your browser. We never store income, expenses or portfolios on our servers."),
            ("📊 Clarity above all", "No unnecessary jargon: numbers, charts and simple explanations for real decisions."),
            ("🌱 Progress, not perfection", "We don't promise overnight wealth. We help you take the right next step, consistently."),
        ],
        "como_titulo": "🛠️ What you'll find here",
        "como": [
            "Budget: find your savings rate and investing capacity",
            "Goals: simulate how long each goal takes under different scenarios",
            "Dashboard, Comparator and Simulator: analyze and test your investment portfolio",
            "Dividends, Risk and News: keep track of what matters about your assets",
            "Export Report: take your analysis with you as PDF or Excel",
        ],
        "btn_comecar": "🚀 Get started",
        "btn_precos": "✨ See plans",
        "aviso": "⚠️ Freenomics is an educational tool for financial organization. It does not constitute financial, tax or investment advice.",
        "rodape": "Freenomics · Money, mindset and financial freedom",
    },
    "🇫🇷 Français": {
        "titulo": "Bienvenue sur Freenomics",
        "subtitulo": "Votre boussole pour organiser vos finances et avancer, étape par étape, vers la liberté financière.",
        "missao_titulo": "🎯 Notre mission",
        "missao_texto": "Donner à chacun, quel que soit son niveau en finance, des outils simples et clairs pour comprendre où va son argent, combien il peut investir et le temps nécessaire pour atteindre ses objectifs.",
        "visao_titulo": "🔭 Notre vision",
        "visao_texto": "Un monde où l'éducation financière n'est pas un privilège réservé à ceux qui ont étudié l'économie, mais une habitude accessible à tous, fondée sur des décisions informées plutôt que sur la peur ou le hasard.",
        "valores_titulo": "🧭 Notre philosophie",
        "valores": [
            ("🔒 La confidentialité d'abord", "Vos données financières restent dans votre navigateur. Nous ne stockons jamais vos revenus, dépenses ou portefeuilles sur nos serveurs."),
            ("📊 La clarté avant tout", "Pas de jargon inutile : des chiffres, des graphiques et des explications simples pour de vraies décisions."),
            ("🌱 Le progrès, pas la perfection", "Nous ne promettons pas de vous enrichir du jour au lendemain. Nous vous aidons à faire le prochain pas, de façon constante."),
        ],
        "como_titulo": "🛠️ Ce que vous trouverez ici",
        "como": [
            "Budget : découvrez votre taux d'épargne et votre capacité d'investissement",
            "Objectifs : simulez le temps nécessaire pour chaque objectif selon différents scénarios",
            "Dashboard, Comparateur et Simulateur : analysez et testez votre portefeuille",
            "Dividendes, Risque et Actualités : suivez ce qui compte sur vos actifs",
            "Exporter Rapport : emportez votre analyse en PDF ou Excel",
        ],
        "btn_comecar": "🚀 Commencer",
        "btn_precos": "✨ Voir les tarifs",
        "aviso": "⚠️ Freenomics est un outil éducatif d'organisation financière. Il ne constitue pas un conseil financier, fiscal ou d'investissement.",
        "rodape": "Freenomics · Argent, mentalité et liberté financière",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Willkommen bei Freenomics",
        "subtitulo": "Dein Kompass, um deine Finanzen zu organisieren und Schritt für Schritt finanzielle Freiheit zu erreichen.",
        "missao_titulo": "🎯 Unsere Mission",
        "missao_texto": "Jedem, unabhängig vom Finanzwissen, einfache und klare Werkzeuge zu geben, um zu verstehen, wohin sein Geld fließt, wie viel er investieren kann und wie lange es dauert, seine Ziele zu erreichen.",
        "visao_titulo": "🔭 Unsere Vision",
        "visao_texto": "Eine Welt, in der Finanzbildung kein Privileg von Wirtschaftsstudierenden ist, sondern eine für alle zugängliche Gewohnheit, basierend auf informierten Entscheidungen statt Angst oder Rätselraten.",
        "valores_titulo": "🧭 Wie wir denken",
        "valores": [
            ("🔒 Privatsphäre zuerst", "Deine Finanzdaten bleiben in deinem Browser. Wir speichern niemals Einkommen, Ausgaben oder Portfolios auf unseren Servern."),
            ("📊 Klarheit vor allem", "Kein unnötiger Fachjargon: Zahlen, Diagramme und einfache Erklärungen für echte Entscheidungen."),
            ("🌱 Fortschritt statt Perfektion", "Wir versprechen keinen Reichtum über Nacht. Wir helfen dir, konsequent den richtigen nächsten Schritt zu machen."),
        ],
        "como_titulo": "🛠️ Was du hier findest",
        "como": [
            "Budget: finde deine Sparquote und Investitionsfähigkeit heraus",
            "Ziele: simuliere, wie lange jedes Ziel unter verschiedenen Szenarien dauert",
            "Dashboard, Vergleich und Simulator: analysiere und teste dein Portfolio",
            "Dividenden, Risiko und Nachrichten: verfolge, was bei deinen Anlagen wichtig ist",
            "Bericht exportieren: nimm deine Analyse als PDF oder Excel mit",
        ],
        "btn_comecar": "🚀 Jetzt starten",
        "btn_precos": "✨ Preise ansehen",
        "aviso": "⚠️ Freenomics ist ein Bildungswerkzeug zur Finanzorganisation. Es stellt keine Finanz-, Steuer- oder Anlageberatung dar.",
        "rodape": "Freenomics · Geld, Mindset und finanzielle Freiheit",
    },
    "🇪🇸 Español": {
        "titulo": "Bienvenido a Freenomics",
        "subtitulo": "Tu brújula para organizar tus finanzas y avanzar, paso a paso, hacia la libertad financiera.",
        "missao_titulo": "🎯 Nuestra misión",
        "missao_texto": "Dar a cualquier persona, sin importar su nivel de conocimiento financiero, herramientas simples y claras para entender adónde va su dinero, cuánto puede invertir y cuánto tiempo falta para alcanzar sus objetivos.",
        "visao_titulo": "🔭 Nuestra visión",
        "visao_texto": "Un mundo donde la educación financiera no sea un privilegio de quienes estudiaron economía, sino un hábito accesible para todos, basado en decisiones informadas en lugar de miedo o adivinanzas.",
        "valores_titulo": "🧭 Cómo pensamos",
        "valores": [
            ("🔒 La privacidad primero", "Tus datos financieros permanecen en tu navegador. Nunca almacenamos ingresos, gastos ni carteras en nuestros servidores."),
            ("📊 Claridad ante todo", "Sin jerga innecesaria: números, gráficos y explicaciones simples para decisiones reales."),
            ("🌱 Progreso, no perfección", "No prometemos hacerte rico de la noche a la mañana. Te ayudamos a dar el siguiente paso correcto, de forma constante."),
        ],
        "como_titulo": "🛠️ Qué encontrarás aquí",
        "como": [
            "Presupuesto: descubre tu tasa de ahorro y capacidad de inversión",
            "Objetivos: simula cuánto tiempo falta para cada objetivo en varios escenarios",
            "Dashboard, Comparador y Simulador: analiza y prueba tu cartera de inversión",
            "Dividendos, Riesgo y Noticias: sigue lo importante sobre tus activos",
            "Exportar Informe: llévate tu análisis en PDF o Excel",
        ],
        "btn_comecar": "🚀 Empezar ahora",
        "btn_precos": "✨ Ver planes",
        "aviso": "⚠️ Freenomics es una herramienta educativa de organización financiera. No constituye asesoramiento financiero, fiscal ni de inversión.",
        "rodape": "Freenomics · Dinero, mentalidad y libertad financiera",
    },
}[lang]

INICIO = {
    "🇵🇹 Português": {
        "onde_titulo": "🧭 Por onde começar",
        "onde_sub": "Quatro passos simples, por esta ordem. Em poucos minutos tens o teu plano.",
        "passos": [
            ("Orçamento", "Descobre quanto sobra todos os meses para investir.", "🧾 Orçamento"),
            ("Objetivos", "Define o que queres alcançar e quanto tempo demora.", "🎯 Objetivos"),
            ("Património", "Regista o que tens e o que deves, e vê o teu ponto de partida.", "💎 Património"),
            ("Investir", "Analisa ações e acompanha a tua carteira.", None),
        ],
        "l_analise": "🔎 Análise de Ação", "l_carteira": "📈 Carteira",
        "demo_ok": "Exemplo carregado com dados fictícios. Abre o Orçamento, os Objetivos, o Património ou a Carteira: já têm resultados.",
    },
    "🇬🇧 English": {
        "onde_titulo": "🧭 Where to start",
        "onde_sub": "Four simple steps, in this order. In a few minutes you have your plan.",
        "passos": [
            ("Budget", "Find out how much is left each month to invest.", "🧾 Budget"),
            ("Goals", "Set what you want to achieve and how long it takes.", "🎯 Goals"),
            ("Net Worth", "Record what you own and owe, and see your starting point.", "💎 Net Worth"),
            ("Invest", "Analyse stocks and track your portfolio.", None),
        ],
        "l_analise": "🔎 Stock Analysis", "l_carteira": "📈 Portfolio",
        "demo_ok": "Sample loaded with fictional data. Open Budget, Goals, Net Worth or Portfolio: they already show results.",
    },
    "🇫🇷 Français": {
        "onde_titulo": "🧭 Par où commencer",
        "onde_sub": "Quatre étapes simples, dans cet ordre. En quelques minutes, votre plan est prêt.",
        "passos": [
            ("Budget", "Découvrez ce qu'il reste chaque mois pour investir.", "🧾 Budget"),
            ("Objectifs", "Définissez ce que vous voulez atteindre et en combien de temps.", "🎯 Objectifs"),
            ("Patrimoine", "Enregistrez ce que vous possédez et devez, et voyez votre point de départ.", "💎 Patrimoine"),
            ("Investir", "Analysez des actions et suivez votre portefeuille.", None),
        ],
        "l_analise": "🔎 Analyse d'Action", "l_carteira": "📈 Portefeuille",
        "demo_ok": "Exemple chargé avec des données fictives. Ouvrez Budget, Objectifs, Patrimoine ou Portefeuille : les résultats sont déjà là.",
    },
    "🇩🇪 Deutsch": {
        "onde_titulo": "🧭 Wo du anfängst",
        "onde_sub": "Vier einfache Schritte, in dieser Reihenfolge. In wenigen Minuten steht dein Plan.",
        "passos": [
            ("Budget", "Finde heraus, wie viel jeden Monat zum Investieren übrig bleibt.", "🧾 Budget"),
            ("Ziele", "Lege fest, was du erreichen willst und wie lange es dauert.", "🎯 Ziele"),
            ("Vermögen", "Erfasse, was du besitzt und schuldest, und sieh deinen Ausgangspunkt.", "💎 Vermögen"),
            ("Investieren", "Analysiere Aktien und verfolge dein Portfolio.", None),
        ],
        "l_analise": "🔎 Aktienanalyse", "l_carteira": "📈 Portfolio",
        "demo_ok": "Beispiel mit fiktiven Daten geladen. Öffne Budget, Ziele, Vermögen oder Portfolio: Die Ergebnisse sind schon da.",
    },
    "🇪🇸 Español": {
        "onde_titulo": "🧭 Por dónde empezar",
        "onde_sub": "Cuatro pasos sencillos, en este orden. En pocos minutos tienes tu plan.",
        "passos": [
            ("Presupuesto", "Descubre cuánto sobra cada mes para invertir.", "🧾 Presupuesto"),
            ("Objetivos", "Define qué quieres lograr y cuánto tarda.", "🎯 Objetivos"),
            ("Patrimonio", "Registra lo que tienes y lo que debes, y mira tu punto de partida.", "💎 Patrimonio"),
            ("Invertir", "Analiza acciones y sigue tu cartera.", None),
        ],
        "l_analise": "🔎 Análisis de Acción", "l_carteira": "📈 Cartera",
        "demo_ok": "Ejemplo cargado con datos ficticios. Abre Presupuesto, Objetivos, Patrimonio o Cartera: ya muestran resultados.",
    },
}[lang]

paginas = st.session_state.get("_paginas") or {}


def _link(chave, label):
    """st.page_link seguro: ignora se a página não estiver registada."""
    if chave in paginas:
        try:
            st.page_link(paginas[chave], label=label, use_container_width=True)
        except Exception:
            pass


show_logo()
st.title(L["titulo"])
st.markdown(f"<p style='font-size:1.15rem;color:#C8D3DA;'>{L['subtitulo']}</p>", unsafe_allow_html=True)

# ── Botão grande "Começar" + modo demonstração ────────────────
with kcontainer("fn_hero"):
    _link("orcamento", L["btn_comecar"])
demo_bar("home")
if st.session_state.get("demo_ativo"):
    st.success(INICIO["demo_ok"])

# ── Por onde começar ──────────────────────────────────────────
st.markdown("---")
st.markdown(f"#### {INICIO['onde_titulo']}")
st.caption(INICIO["onde_sub"])
_chaves = ["orcamento", "objetivos", "patrimonio"]
cols_p = st.columns(4)
for n, (col, (tit, txt, lbl)) in enumerate(zip(cols_p, INICIO["passos"]), start=1):
    with col:
        st.markdown(f"""
        <div class="fn-card">
            <span class="fn-num">{n}</span>
            <p class="fn-tit">{tit}</p>
            <p class="fn-txt">{txt}</p>
        </div>""", unsafe_allow_html=True)
        if n <= 3:
            _link(_chaves[n - 1], lbl)
        else:
            _link("analise", INICIO["l_analise"])
            _link("carteira", INICIO["l_carteira"])

st.markdown("---")

col_m, col_v = st.columns(2)
with col_m:
    st.markdown(f"#### {L['missao_titulo']}")
    st.write(L["missao_texto"])
with col_v:
    st.markdown(f"#### {L['visao_titulo']}")
    st.write(L["visao_texto"])

st.markdown("---")
st.markdown(f"#### {L['valores_titulo']}")
col1, col2, col3 = st.columns(3)
for col, (titulo, texto) in zip([col1, col2, col3], L["valores"]):
    with col:
        st.markdown(f"""
        <div style="background:#0E2A3D;border-radius:10px;padding:20px;border:1px solid #2A3F52;height:100%;">
            <p style="color:#FAF8F3;font-weight:700;margin:0 0 8px 0;">{titulo}</p>
            <p style="color:#C8D3DA;font-size:0.92rem;margin:0;">{texto}</p>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")
st.markdown(f"#### {L['como_titulo']}")
for item in L["como"]:
    st.markdown(f"- {item}")

st.write("")
st.caption(L["aviso"])
st.markdown("---")
st.caption(L["rodape"])
