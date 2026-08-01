"""
Preços & Boas-vindas · Freenomics
Explica o que é a app, compara o plano Gratuito com o Premium, e serve de
ponto de entrada para a subscrição (o botão de pagamento liga-se depois via Stripe).
"""

import streamlit as st
import streamlit.components.v1 as components
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, FIX_DROPDOWNS_JS
import auth

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Planos & Preços",
        "free_nome": "🔓 Gratuito",
        "free_preco": "€0",
        "free_periodo": "para sempre",
        "free_desc": "Explora todas as páginas e ferramentas à vontade.",
        "free_items": [
            "Acesso a todas as calculadoras e páginas",
            "Preenchimento livre de dados (orçamento, objetivos, carteira)",
            "Pré-visualização dos gráficos e resultados",
        ],
        "free_limite": "Os resultados detalhados e a exportação de relatórios ficam bloqueados.",
        "premium_nome": "⭐ Premium",
        "premium_preco": "€4,99",
        "premium_periodo": "/mês",
        "premium_desc": "Acesso completo a todas as análises, sem limites.",
        "premium_items": [
            "Resultados completos em todas as páginas",
            "Exportação de relatórios em PDF e Excel",
            "Comparador de carteiras ilimitado",
            "Simulações e cenários de objetivos completos",
        ],
        "btn_premium": "⭐ Subscrever Premium",
        "btn_free": "🔓 Continuar no plano Gratuito",
        "em_breve": "🚧 Os pagamentos ainda não estão ligados. Em breve podes subscrever diretamente aqui.",
        "atual_titulo": "O teu plano atual",
        "faq_titulo": "Perguntas frequentes",
        "faq": [
            ("Os meus dados financeiros ficam guardados algures?", "Não. Todos os valores que preenches ficam apenas na tua sessão do browser. Não guardamos rendimentos, despesas, carteiras nem valores de investimento em nenhum servidor."),
            ("Posso cancelar quando quiser?", "Sim, a subscrição Premium pode ser cancelada a qualquer momento, sem fidelização."),
            ("O que é guardado na minha conta?", "Apenas o teu email e o teu plano (gratuito ou premium), para sabermos se tens acesso completo."),
        ],
        "rodape": "Freenomics · Dinheiro, mentalidade e liberdade financeira",
    },
    "🇬🇧 English": {
        "titulo": "Plans & Pricing",
        "free_nome": "🔓 Free",
        "free_preco": "€0",
        "free_periodo": "forever",
        "free_desc": "Explore every page and tool freely.",
        "free_items": [
            "Access to all calculators and pages",
            "Free data entry (budget, goals, portfolio)",
            "Preview of charts and results",
        ],
        "free_limite": "Detailed results and report exports are locked.",
        "premium_nome": "⭐ Premium",
        "premium_preco": "€4.99",
        "premium_periodo": "/month",
        "premium_desc": "Full access to every analysis, with no limits.",
        "premium_items": [
            "Full results on every page",
            "PDF and Excel report exports",
            "Unlimited portfolio comparator",
            "Full goal simulations and scenarios",
        ],
        "btn_premium": "⭐ Subscribe to Premium",
        "btn_free": "🔓 Continue on the Free plan",
        "em_breve": "🚧 Payments aren't connected yet. You'll soon be able to subscribe directly here.",
        "atual_titulo": "Your current plan",
        "faq_titulo": "Frequently asked questions",
        "faq": [
            ("Is my financial data stored anywhere?", "No. Everything you enter stays only in your browser session. We don't store income, expenses, portfolios or investment values on any server."),
            ("Can I cancel anytime?", "Yes, the Premium subscription can be cancelled at any time, with no commitment."),
            ("What is stored in my account?", "Only your email and your plan (free or premium), so we know if you have full access."),
        ],
        "rodape": "Freenomics · Money, mindset and financial freedom",
    },
    "🇫🇷 Français": {
        "titulo": "Offres & Tarifs",
        "free_nome": "🔓 Gratuit",
        "free_preco": "€0",
        "free_periodo": "pour toujours",
        "free_desc": "Explorez librement toutes les pages et outils.",
        "free_items": [
            "Accès à toutes les calculatrices et pages",
            "Saisie libre des données (budget, objectifs, portefeuille)",
            "Aperçu des graphiques et résultats",
        ],
        "free_limite": "Les résultats détaillés et l'export de rapports sont verrouillés.",
        "premium_nome": "⭐ Premium",
        "premium_preco": "€4,99",
        "premium_periodo": "/mois",
        "premium_desc": "Accès complet à toutes les analyses, sans limites.",
        "premium_items": [
            "Résultats complets sur toutes les pages",
            "Export de rapports en PDF et Excel",
            "Comparateur de portefeuilles illimité",
            "Simulations et scénarios d'objectifs complets",
        ],
        "btn_premium": "⭐ S'abonner à Premium",
        "btn_free": "🔓 Continuer avec le plan Gratuit",
        "em_breve": "🚧 Les paiements ne sont pas encore connectés. Vous pourrez bientôt vous abonner directement ici.",
        "atual_titulo": "Votre plan actuel",
        "faq_titulo": "Questions fréquentes",
        "faq": [
            ("Mes données financières sont-elles stockées quelque part ?", "Non. Tout ce que vous saisissez reste uniquement dans votre session de navigateur. Nous ne stockons ni revenus, ni dépenses, ni portefeuilles sur aucun serveur."),
            ("Puis-je annuler à tout moment ?", "Oui, l'abonnement Premium peut être annulé à tout moment, sans engagement."),
            ("Que stockons-nous dans votre compte ?", "Seulement votre email et votre plan (gratuit ou premium), pour savoir si vous avez un accès complet."),
        ],
        "rodape": "Freenomics · Argent, mentalité et liberté financière",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Pläne & Preise",
        "free_nome": "🔓 Kostenlos",
        "free_preco": "€0",
        "free_periodo": "für immer",
        "free_desc": "Erkunde alle Seiten und Tools frei.",
        "free_items": [
            "Zugang zu allen Rechnern und Seiten",
            "Freie Dateneingabe (Budget, Ziele, Portfolio)",
            "Vorschau von Diagrammen und Ergebnissen",
        ],
        "free_limite": "Detaillierte Ergebnisse und Berichtsexporte sind gesperrt.",
        "premium_nome": "⭐ Premium",
        "premium_preco": "€4,99",
        "premium_periodo": "/Monat",
        "premium_desc": "Voller Zugriff auf alle Analysen, ohne Limits.",
        "premium_items": [
            "Vollständige Ergebnisse auf allen Seiten",
            "PDF- und Excel-Berichtsexport",
            "Unbegrenzter Portfolio-Vergleich",
            "Vollständige Zielsimulationen und Szenarien",
        ],
        "btn_premium": "⭐ Premium abonnieren",
        "btn_free": "🔓 Mit dem kostenlosen Plan fortfahren",
        "em_breve": "🚧 Zahlungen sind noch nicht verbunden. Bald kannst du direkt hier abonnieren.",
        "atual_titulo": "Dein aktueller Plan",
        "faq_titulo": "Häufig gestellte Fragen",
        "faq": [
            ("Werden meine Finanzdaten irgendwo gespeichert?", "Nein. Alles, was du eingibst, bleibt nur in deiner Browsersitzung. Wir speichern keine Einkommen, Ausgaben, Portfolios oder Investitionswerte auf einem Server."),
            ("Kann ich jederzeit kündigen?", "Ja, das Premium-Abonnement kann jederzeit ohne Bindung gekündigt werden."),
            ("Was wird in deinem Konto gespeichert?", "Nur deine E-Mail und dein Plan (kostenlos oder premium), damit wir wissen, ob du vollen Zugriff hast."),
        ],
        "rodape": "Freenomics · Geld, Mindset und finanzielle Freiheit",
    },
    "🇪🇸 Español": {
        "titulo": "Planes & Precios",
        "free_nome": "🔓 Gratis",
        "free_preco": "€0",
        "free_periodo": "para siempre",
        "free_desc": "Explora todas las páginas y herramientas libremente.",
        "free_items": [
            "Acceso a todas las calculadoras y páginas",
            "Introducción libre de datos (presupuesto, objetivos, cartera)",
            "Vista previa de gráficos y resultados",
        ],
        "free_limite": "Los resultados detallados y la exportación de informes están bloqueados.",
        "premium_nome": "⭐ Premium",
        "premium_preco": "€4,99",
        "premium_periodo": "/mes",
        "premium_desc": "Acceso completo a todos los análisis, sin límites.",
        "premium_items": [
            "Resultados completos en todas las páginas",
            "Exportación de informes en PDF y Excel",
            "Comparador de carteras ilimitado",
            "Simulaciones y escenarios de objetivos completos",
        ],
        "btn_premium": "⭐ Suscribirse a Premium",
        "btn_free": "🔓 Continuar con el plan Gratis",
        "em_breve": "🚧 Los pagos aún no están conectados. Pronto podrás suscribirte directamente aquí.",
        "atual_titulo": "Tu plan actual",
        "faq_titulo": "Preguntas frecuentes",
        "faq": [
            ("¿Mis datos financieros se guardan en algún sitio?", "No. Todo lo que introduces permanece solo en tu sesión del navegador. No almacenamos ingresos, gastos, carteras ni valores de inversión en ningún servidor."),
            ("¿Puedo cancelar cuando quiera?", "Sí, la suscripción Premium se puede cancelar en cualquier momento, sin permanencia."),
            ("¿Qué se guarda en tu cuenta?", "Solo tu email y tu plan (gratis o premium), para saber si tienes acceso completo."),
        ],
        "rodape": "Freenomics · Dinero, mentalidad y libertad financiera",
    },
}[lang]

show_logo()
st.title(L["titulo"])
st.markdown("---")

col_free, col_premium = st.columns(2)

with col_free:
    st.markdown(f"""
    <div style="background:#0E2A3D;border-radius:12px;padding:28px;border:1px solid #2A3F52;height:100%;">
        <h3 style="color:#FAF8F3;margin:0;">{L['free_nome']}</h3>
        <p style="font-size:2rem;font-weight:800;color:#FAF8F3;margin:8px 0 0 0;">{L['free_preco']}<span style="font-size:1rem;font-weight:400;color:#C8D3DA;"> {L['free_periodo']}</span></p>
        <p style="color:#C8D3DA;margin-top:8px;">{L['free_desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    for item in L["free_items"]:
        st.markdown(f"✅ {item}")
    st.caption(f"🔒 {L['free_limite']}")

with col_premium:
    st.markdown(f"""
    <div style="background:#1A2F4A;border-radius:12px;padding:28px;border:2px solid #C29A4B;height:100%;">
        <h3 style="color:#FAF8F3;margin:0;">{L['premium_nome']}</h3>
        <p style="font-size:2rem;font-weight:800;color:#C29A4B;margin:8px 0 0 0;">{L['premium_preco']}<span style="font-size:1rem;font-weight:400;color:#C8D3DA;"> {L['premium_periodo']}</span></p>
        <p style="color:#C8D3DA;margin-top:8px;">{L['premium_desc']}</p>
    </div>
    """, unsafe_allow_html=True)
    st.write("")
    for item in L["premium_items"]:
        st.markdown(f"⭐ {item}")

st.write("")
col_a, col_b = st.columns(2)
with col_a:
    st.button(L["btn_free"], use_container_width=True, disabled=True, key="btn_free_plano")
with col_b:
    if st.button(L["btn_premium"], use_container_width=True, type="primary", key="btn_premium_plano"):
        st.info(L["em_breve"])

if auth.is_logged_in():
    plano_labels = {"free": L["free_nome"], "premium": L["premium_nome"], "admin": "👑 Admin"}
    st.markdown("---")
    st.markdown(f"**{L['atual_titulo']}:** {plano_labels.get(auth.current_plan(), auth.current_plan())}")

st.markdown("---")
st.subheader(L["faq_titulo"])
for pergunta, resposta in L["faq"]:
    with st.expander(pergunta):
        st.write(resposta)

st.markdown("---")
st.caption(L["rodape"])
