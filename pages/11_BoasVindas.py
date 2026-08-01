"""
Boas-vindas · Freenomics
Primeira página que qualquer pessoa vê ao abrir a app: missão, visão e
como o Freenomics ajuda a organizar a vida financeira rumo à liberdade financeira.
"""

import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
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

show_logo()
st.title(L["titulo"])
st.markdown(f"<p style='font-size:1.15rem;color:#C8D3DA;'>{L['subtitulo']}</p>", unsafe_allow_html=True)
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
