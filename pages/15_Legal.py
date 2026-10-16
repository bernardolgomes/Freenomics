"""
Termos e Privacidade · Freenomics
Termos de utilização, política de privacidade e aviso legal.
NOTA: texto-base, convém ser revisto por um profissional antes do lançamento comercial.
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

# Preenche com os teus dados antes de lançar
RESPONSAVEL = "Freenomics"
CONTACTO = "berrygoody91@gmail.com"

L = {
    "🇵🇹 Português": {
        "titulo": "Termos e Privacidade",
        "atualizado": "Última atualização: outubro de 2026",
        "tabs": ["Termos de utilização", "Privacidade", "Aviso legal"],
        "termos": [
            ("1. O serviço", "O Freenomics é uma aplicação educativa de organização financeira pessoal, com calculadoras, simulações e análises. Ao utilizá-la aceitas estes termos."),
            ("2. Contas e planos", "Podes usar o plano Gratuito sem custos. O plano Premium (mensal ou anual) desbloqueia os resultados completos e a exportação de relatórios. És responsável por manter a tua palavra-passe segura."),
            ("3. Pagamentos e cancelamento", "As subscrições são cobradas através de um processador de pagamentos externo. Podes cancelar a qualquer momento e o acesso Premium mantém-se até ao fim do período já pago. Os reembolsos seguem a lei aplicável em matéria de direitos do consumidor."),
            ("4. Utilização aceitável", "Não podes tentar aceder a áreas restritas, contornar o plano contratado, copiar a aplicação para revenda nem fazer um uso que prejudique o serviço ou outros utilizadores."),
            ("5. Disponibilidade", "Fazemos o possível para manter a aplicação disponível, mas não garantimos funcionamento ininterrupto. Os dados de mercado provêm de fontes de terceiros e podem ter atrasos ou falhas."),
            ("6. Limitação de responsabilidade", "O serviço é fornecido 'como está'. Não nos responsabilizamos por decisões financeiras tomadas com base na aplicação."),
        ],
        "privacidade": [
            ("Quem é o responsável", f"{RESPONSAVEL}. Contacto para questões de privacidade: {CONTACTO}."),
            ("Que dados guardamos", "Apenas o teu email e o teu plano (gratuito, premium ou admin), através do serviço de autenticação Supabase. Não guardamos rendimentos, despesas, carteiras, objetivos nem outros valores financeiros que introduzes: esses dados ficam apenas na sessão do teu browser e desaparecem quando a fechas."),
            ("Para que usamos os dados", "Para criar a tua conta, saber que acesso tens e processar a subscrição. Não vendemos nem partilhamos os teus dados para publicidade."),
            ("Serviços de terceiros", "Supabase (autenticação e base de dados), o processador de pagamentos (dados de pagamento tratados por eles, nunca por nós), Yahoo Finance e Google News (dados de mercado e notícias, sem enviarmos dados pessoais)."),
            ("Os teus direitos (RGPD)", f"Podes pedir acesso, correção ou eliminação da tua conta e dos dados associados a qualquer momento, enviando um email para {CONTACTO}. Também podes apresentar reclamação à autoridade de controlo (em Portugal, a CNPD)."),
            ("Cookies", "Usamos apenas o armazenamento técnico necessário para manter a tua sessão ativa."),
        ],
        "aviso": [
            ("Não é aconselhamento financeiro", "O Freenomics é uma ferramenta educativa. Nada na aplicação constitui aconselhamento financeiro, fiscal, jurídico ou recomendação de investimento. As simulações e projeções baseiam-se em pressupostos teus e não garantem resultados futuros."),
            ("Risco", "Investir envolve risco, incluindo a perda total do capital investido. Rentabilidades passadas não garantem rentabilidades futuras. Consulta um profissional qualificado antes de decidires."),
        ],
    },
    "🇬🇧 English": {
        "titulo": "Terms & Privacy",
        "atualizado": "Last updated: October 2026",
        "tabs": ["Terms of use", "Privacy", "Disclaimer"],
        "termos": [
            ("1. The service", "Freenomics is an educational personal-finance app with calculators, simulations and analyses. By using it you accept these terms."),
            ("2. Accounts and plans", "You can use the Free plan at no cost. The Premium plan (monthly or yearly) unlocks full results and report exports. You are responsible for keeping your password secure."),
            ("3. Payments and cancellation", "Subscriptions are billed through an external payment processor. You can cancel at any time and Premium access remains until the end of the period already paid. Refunds follow applicable consumer law."),
            ("4. Acceptable use", "You may not try to access restricted areas, bypass your plan, copy the app for resale, or use it in a way that harms the service or other users."),
            ("5. Availability", "We do our best to keep the app available but do not guarantee uninterrupted operation. Market data comes from third parties and may be delayed or fail."),
            ("6. Limitation of liability", "The service is provided 'as is'. We are not liable for financial decisions made based on the app."),
        ],
        "privacidade": [
            ("Who is responsible", f"{RESPONSAVEL}. Privacy contact: {CONTACTO}."),
            ("What data we store", "Only your email and your plan (free, premium or admin), through the Supabase authentication service. We do not store income, expenses, portfolios, goals or other financial values you enter: they stay only in your browser session and disappear when you close it."),
            ("What we use data for", "To create your account, know your access level and process your subscription. We do not sell or share your data for advertising."),
            ("Third-party services", "Supabase (authentication and database), the payment processor (payment details handled by them, never by us), Yahoo Finance and Google News (market data and news, with no personal data sent)."),
            ("Your rights (GDPR)", f"You can request access, correction or deletion of your account and related data at any time by emailing {CONTACTO}. You can also lodge a complaint with your supervisory authority."),
            ("Cookies", "We only use the technical storage needed to keep your session active."),
        ],
        "aviso": [
            ("Not financial advice", "Freenomics is an educational tool. Nothing in the app is financial, tax or legal advice or an investment recommendation. Simulations and projections are based on your own assumptions and do not guarantee future results."),
            ("Risk", "Investing involves risk, including total loss of capital. Past performance does not guarantee future returns. Consult a qualified professional before deciding."),
        ],
    },
    "🇫🇷 Français": {
        "titulo": "Conditions et Confidentialité",
        "atualizado": "Dernière mise à jour : octobre 2026",
        "tabs": ["Conditions d'utilisation", "Confidentialité", "Avertissement"],
        "termos": [
            ("1. Le service", "Freenomics est une application éducative de gestion financière personnelle, avec calculatrices, simulations et analyses. En l'utilisant, vous acceptez ces conditions."),
            ("2. Comptes et offres", "Vous pouvez utiliser l'offre Gratuite sans frais. L'offre Premium (mensuelle ou annuelle) débloque les résultats complets et l'export de rapports. Vous êtes responsable de la sécurité de votre mot de passe."),
            ("3. Paiements et résiliation", "Les abonnements sont facturés via un prestataire de paiement externe. Vous pouvez résilier à tout moment et l'accès Premium reste actif jusqu'à la fin de la période payée. Les remboursements suivent le droit de la consommation applicable."),
            ("4. Utilisation acceptable", "Il est interdit d'accéder à des zones restreintes, de contourner votre offre, de copier l'application pour la revendre ou de nuire au service ou aux autres utilisateurs."),
            ("5. Disponibilité", "Nous faisons de notre mieux pour maintenir l'application disponible sans garantir un fonctionnement ininterrompu. Les données de marché proviennent de tiers et peuvent être retardées ou indisponibles."),
            ("6. Limitation de responsabilité", "Le service est fourni « en l'état ». Nous ne sommes pas responsables des décisions financières prises sur la base de l'application."),
        ],
        "privacidade": [
            ("Responsable", f"{RESPONSAVEL}. Contact confidentialité : {CONTACTO}."),
            ("Données conservées", "Uniquement votre email et votre offre (gratuite, premium ou admin), via le service d'authentification Supabase. Nous ne conservons ni revenus, dépenses, portefeuilles, objectifs ni autres valeurs financières saisies : elles restent dans la session de votre navigateur et disparaissent à sa fermeture."),
            ("Utilisation des données", "Pour créer votre compte, connaître votre niveau d'accès et traiter l'abonnement. Nous ne vendons ni ne partageons vos données à des fins publicitaires."),
            ("Services tiers", "Supabase (authentification et base de données), le prestataire de paiement (données de paiement gérées par lui, jamais par nous), Yahoo Finance et Google News (données de marché et actualités, sans envoi de données personnelles)."),
            ("Vos droits (RGPD)", f"Vous pouvez demander l'accès, la rectification ou la suppression de votre compte et des données associées à tout moment à {CONTACTO}. Vous pouvez aussi saisir votre autorité de contrôle."),
            ("Cookies", "Nous utilisons uniquement le stockage technique nécessaire au maintien de votre session."),
        ],
        "aviso": [
            ("Pas un conseil financier", "Freenomics est un outil éducatif. Rien dans l'application ne constitue un conseil financier, fiscal ou juridique, ni une recommandation d'investissement. Les simulations reposent sur vos propres hypothèses et ne garantissent aucun résultat."),
            ("Risque", "Investir comporte des risques, y compris la perte totale du capital. Les performances passées ne préjugent pas des performances futures. Consultez un professionnel qualifié avant de décider."),
        ],
    },
    "🇩🇪 Deutsch": {
        "titulo": "AGB & Datenschutz",
        "atualizado": "Zuletzt aktualisiert: Oktober 2026",
        "tabs": ["Nutzungsbedingungen", "Datenschutz", "Haftungsausschluss"],
        "termos": [
            ("1. Der Dienst", "Freenomics ist eine Bildungs-App für die persönliche Finanzorganisation mit Rechnern, Simulationen und Analysen. Mit der Nutzung akzeptierst du diese Bedingungen."),
            ("2. Konten und Pläne", "Den kostenlosen Plan kannst du ohne Kosten nutzen. Der Premium-Plan (monatlich oder jährlich) schaltet vollständige Ergebnisse und Berichtsexporte frei. Du bist für die Sicherheit deines Passworts verantwortlich."),
            ("3. Zahlungen und Kündigung", "Abonnements werden über einen externen Zahlungsdienstleister abgerechnet. Du kannst jederzeit kündigen; der Premium-Zugang bleibt bis zum Ende des bezahlten Zeitraums bestehen. Erstattungen richten sich nach geltendem Verbraucherrecht."),
            ("4. Zulässige Nutzung", "Es ist untersagt, auf gesperrte Bereiche zuzugreifen, deinen Plan zu umgehen, die App zum Weiterverkauf zu kopieren oder den Dienst bzw. andere Nutzer zu beeinträchtigen."),
            ("5. Verfügbarkeit", "Wir bemühen uns um Verfügbarkeit, garantieren aber keinen unterbrechungsfreien Betrieb. Marktdaten stammen von Dritten und können verzögert sein oder ausfallen."),
            ("6. Haftungsbeschränkung", "Der Dienst wird „wie besehen“ bereitgestellt. Wir haften nicht für Finanzentscheidungen auf Grundlage der App."),
        ],
        "privacidade": [
            ("Verantwortlicher", f"{RESPONSAVEL}. Datenschutzkontakt: {CONTACTO}."),
            ("Gespeicherte Daten", "Nur deine E-Mail und dein Plan (kostenlos, premium oder admin) über den Authentifizierungsdienst Supabase. Eingegebene Einkommen, Ausgaben, Portfolios, Ziele oder andere Finanzwerte speichern wir nicht: Sie bleiben nur in deiner Browsersitzung und verschwinden beim Schließen."),
            ("Verwendungszweck", "Zur Kontoerstellung, zur Zugriffsprüfung und zur Abwicklung des Abonnements. Wir verkaufen oder teilen deine Daten nicht für Werbung."),
            ("Drittanbieter", "Supabase (Authentifizierung und Datenbank), der Zahlungsdienstleister (Zahlungsdaten verarbeitet er, nie wir), Yahoo Finance und Google News (Marktdaten und Nachrichten, ohne Übermittlung personenbezogener Daten)."),
            ("Deine Rechte (DSGVO)", f"Du kannst jederzeit Auskunft, Berichtigung oder Löschung deines Kontos und der Daten verlangen: {CONTACTO}. Du kannst dich auch bei deiner Aufsichtsbehörde beschweren."),
            ("Cookies", "Wir nutzen nur den technisch notwendigen Speicher, um deine Sitzung aktiv zu halten."),
        ],
        "aviso": [
            ("Keine Finanzberatung", "Freenomics ist ein Bildungswerkzeug. Nichts in der App ist Finanz-, Steuer- oder Rechtsberatung oder eine Anlageempfehlung. Simulationen basieren auf deinen eigenen Annahmen und garantieren keine Ergebnisse."),
            ("Risiko", "Investieren birgt Risiken bis hin zum Totalverlust. Vergangene Wertentwicklung ist kein Indikator für die Zukunft. Konsultiere vor Entscheidungen einen qualifizierten Fachmann."),
        ],
    },
    "🇪🇸 Español": {
        "titulo": "Términos y Privacidad",
        "atualizado": "Última actualización: octubre de 2026",
        "tabs": ["Términos de uso", "Privacidad", "Aviso legal"],
        "termos": [
            ("1. El servicio", "Freenomics es una aplicación educativa de organización financiera personal, con calculadoras, simulaciones y análisis. Al usarla aceptas estos términos."),
            ("2. Cuentas y planes", "Puedes usar el plan Gratis sin coste. El plan Premium (mensual o anual) desbloquea los resultados completos y la exportación de informes. Eres responsable de mantener segura tu contraseña."),
            ("3. Pagos y cancelación", "Las suscripciones se cobran mediante un procesador de pagos externo. Puedes cancelar en cualquier momento y el acceso Premium continúa hasta el final del período pagado. Los reembolsos siguen la ley de consumidores aplicable."),
            ("4. Uso aceptable", "No puedes intentar acceder a áreas restringidas, eludir tu plan, copiar la aplicación para revenderla ni perjudicar el servicio u otros usuarios."),
            ("5. Disponibilidad", "Hacemos lo posible por mantener la aplicación disponible, pero no garantizamos un funcionamiento ininterrumpido. Los datos de mercado proceden de terceros y pueden retrasarse o fallar."),
            ("6. Limitación de responsabilidad", "El servicio se ofrece «tal cual». No somos responsables de las decisiones financieras tomadas con base en la aplicación."),
        ],
        "privacidade": [
            ("Responsable", f"{RESPONSAVEL}. Contacto de privacidad: {CONTACTO}."),
            ("Datos que guardamos", "Solo tu email y tu plan (gratis, premium o admin), mediante el servicio de autenticación Supabase. No guardamos ingresos, gastos, carteras, objetivos ni otros valores financieros que introduces: permanecen solo en la sesión de tu navegador y desaparecen al cerrarla."),
            ("Para qué usamos los datos", "Para crear tu cuenta, conocer tu nivel de acceso y procesar la suscripción. No vendemos ni compartimos tus datos con fines publicitarios."),
            ("Servicios de terceros", "Supabase (autenticación y base de datos), el procesador de pagos (los datos de pago los trata él, nunca nosotros), Yahoo Finance y Google News (datos de mercado y noticias, sin enviar datos personales)."),
            ("Tus derechos (RGPD)", f"Puedes solicitar acceso, rectificación o eliminación de tu cuenta y datos asociados en cualquier momento escribiendo a {CONTACTO}. También puedes reclamar ante tu autoridad de control."),
            ("Cookies", "Solo usamos el almacenamiento técnico necesario para mantener tu sesión activa."),
        ],
        "aviso": [
            ("No es asesoramiento financiero", "Freenomics es una herramienta educativa. Nada en la aplicación constituye asesoramiento financiero, fiscal o jurídico ni recomendación de inversión. Las simulaciones se basan en tus propios supuestos y no garantizan resultados."),
            ("Riesgo", "Invertir conlleva riesgo, incluida la pérdida total del capital. La rentabilidad pasada no garantiza la futura. Consulta a un profesional cualificado antes de decidir."),
        ],
    },
}[lang]

show_logo()
st.title(L["titulo"])
st.caption(L["atualizado"])

tab_t, tab_p, tab_a = st.tabs(L["tabs"])
for tab, chave in ((tab_t, "termos"), (tab_p, "privacidade"), (tab_a, "aviso")):
    with tab:
        for titulo, texto in L[chave]:
            st.markdown(f"**{titulo}**")
            st.write(texto)
