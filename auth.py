"""
auth.py · Freenomics
Autenticação e planos de subscrição, usando Supabase (Auth + tabela "profiles").

Planos possíveis em profiles.plan: "free", "premium", "admin".
- free: pode navegar e preencher todas as páginas, mas os resultados ficam bloqueados.
- premium: acesso completo (subscritor pago).
- admin: acesso completo (a tua conta).
"""

import streamlit as st

try:
    from supabase import create_client
except ImportError:
    create_client = None


# ── Traduções ──────────────────────────────────────────────────────────────
_PT, _EN, _FR, _DE, _ES = "🇵🇹 Português", "🇬🇧 English", "🇫🇷 Français", "🇩🇪 Deutsch", "🇪🇸 Español"

AUTH_T = {
    "not_configured_side": {
        _PT: "⚠️ Contas ainda não configuradas (falta ligar o Supabase).",
        _EN: "⚠️ Accounts not configured yet (Supabase is not connected).",
        _FR: "⚠️ Comptes pas encore configurés (Supabase non connecté).",
        _DE: "⚠️ Konten noch nicht konfiguriert (Supabase nicht verbunden).",
        _ES: "⚠️ Cuentas aún no configuradas (falta conectar Supabase).",
    },
    "not_configured_top": {
        _PT: "⚠️ Contas por configurar",
        _EN: "⚠️ Accounts not set up",
        _FR: "⚠️ Comptes à configurer",
        _DE: "⚠️ Konten nicht eingerichtet",
        _ES: "⚠️ Cuentas por configurar",
    },
    "plan_free": {
        _PT: "🔓 Gratuito", _EN: "🔓 Free", _FR: "🔓 Gratuit", _DE: "🔓 Kostenlos", _ES: "🔓 Gratuito",
    },
    "plan_premium": {
        _PT: "⭐ Premium", _EN: "⭐ Premium", _FR: "⭐ Premium", _DE: "⭐ Premium", _ES: "⭐ Premium",
    },
    "plan_admin": {
        _PT: "👑 Admin", _EN: "👑 Admin", _FR: "👑 Admin", _DE: "👑 Admin", _ES: "👑 Admin",
    },
    "logout": {
        _PT: "Sair", _EN: "Log out", _FR: "Se déconnecter", _DE: "Abmelden", _ES: "Cerrar sesión",
    },
    "login_expander": {
        _PT: "🔐 Entrar / Criar conta",
        _EN: "🔐 Log in / Sign up",
        _FR: "🔐 Se connecter / Créer un compte",
        _DE: "🔐 Anmelden / Konto erstellen",
        _ES: "🔐 Entrar / Crear cuenta",
    },
    "login_popover": {
        _PT: "🔐 Entrar", _EN: "🔐 Log in", _FR: "🔐 Connexion", _DE: "🔐 Anmelden", _ES: "🔐 Entrar",
    },
    "tab_login": {
        _PT: "Entrar", _EN: "Log in", _FR: "Connexion", _DE: "Anmelden", _ES: "Entrar",
    },
    "tab_signup": {
        _PT: "Criar conta", _EN: "Sign up", _FR: "Créer un compte", _DE: "Konto erstellen", _ES: "Crear cuenta",
    },
    "email": {
        _PT: "Email", _EN: "Email", _FR: "E-mail", _DE: "E-Mail", _ES: "Correo electrónico",
    },
    "password": {
        _PT: "Password", _EN: "Password", _FR: "Mot de passe", _DE: "Passwort", _ES: "Contraseña",
    },
    "password_min": {
        _PT: "Password (mín. 6 caracteres)",
        _EN: "Password (min. 6 characters)",
        _FR: "Mot de passe (min. 6 caractères)",
        _DE: "Passwort (mind. 6 Zeichen)",
        _ES: "Contraseña (mín. 6 caracteres)",
    },
    "btn_login": {
        _PT: "Entrar", _EN: "Log in", _FR: "Se connecter", _DE: "Anmelden", _ES: "Entrar",
    },
    "btn_signup": {
        _PT: "Criar conta", _EN: "Sign up", _FR: "Créer un compte", _DE: "Konto erstellen", _ES: "Crear cuenta",
    },
    "err_login": {
        _PT: "Email ou password inválidos.",
        _EN: "Invalid email or password.",
        _FR: "E-mail ou mot de passe invalide.",
        _DE: "Ungültige E-Mail oder ungültiges Passwort.",
        _ES: "Correo electrónico o contraseña no válidos.",
    },
    "err_pw_short": {
        _PT: "A password precisa de pelo menos 6 caracteres.",
        _EN: "The password must have at least 6 characters.",
        _FR: "Le mot de passe doit contenir au moins 6 caractères.",
        _DE: "Das Passwort muss mindestens 6 Zeichen lang sein.",
        _ES: "La contraseña debe tener al menos 6 caracteres.",
    },
    "ok_signup": {
        _PT: "Conta criada! Verifica o teu email para confirmar (se pedido) e depois inicia sessão no separador 'Entrar'.",
        _EN: "Account created! Check your email to confirm it (if requested) and then log in on the 'Log in' tab.",
        _FR: "Compte créé ! Vérifie ton e-mail pour confirmer (si demandé), puis connecte-toi dans l'onglet 'Connexion'.",
        _DE: "Konto erstellt! Bestätige deine E-Mail (falls erforderlich) und melde dich dann im Tab 'Anmelden' an.",
        _ES: "¡Cuenta creada! Revisa tu correo para confirmar (si se pide) y luego inicia sesión en la pestaña 'Entrar'.",
    },
    "err_signup": {
        _PT: "Não foi possível criar a conta: {e}",
        _EN: "Could not create the account: {e}",
        _FR: "Impossible de créer le compte : {e}",
        _DE: "Das Konto konnte nicht erstellt werden: {e}",
        _ES: "No se pudo crear la cuenta: {e}",
    },
    "locked_title": {
        _PT: "🔒 Resultados disponíveis para subscritores",
        _EN: "🔒 Results available to subscribers",
        _FR: "🔒 Résultats disponibles pour les abonnés",
        _DE: "🔒 Ergebnisse für Abonnenten verfügbar",
        _ES: "🔒 Resultados disponibles para suscriptores",
    },
    "locked_body": {
        _PT: "Cria conta e subscreve para desbloqueares esta análise completa.",
        _EN: "Create an account and subscribe to unlock this full analysis.",
        _FR: "Crée un compte et abonne-toi pour débloquer cette analyse complète.",
        _DE: "Erstelle ein Konto und abonniere, um diese vollständige Analyse freizuschalten.",
        _ES: "Crea una cuenta y suscríbete para desbloquear este análisis completo.",
    },
}


def _t(key, **kw):
    """Devolve o texto de AUTH_T na língua atual (PT por defeito)."""
    lang = st.session_state.get("lang", _PT)
    d = AUTH_T[key]
    txt = d.get(lang) or d[_PT]
    return txt.format(**kw) if kw else txt


def _plan_labels():
    return {"free": _t("plan_free"), "premium": _t("plan_premium"), "admin": _t("plan_admin")}


@st.cache_resource
def get_client():
    """Cria (e reutiliza) o cliente Supabase a partir dos secrets. Devolve None se não configurado."""
    if create_client is None:
        return None
    url = st.secrets.get("SUPABASE_URL")
    key = st.secrets.get("SUPABASE_ANON_KEY")
    if not url or not key:
        return None
    return create_client(url, key)


def is_configured():
    return get_client() is not None


def sign_up(email, password):
    client = get_client()
    return client.auth.sign_up({"email": email, "password": password})


def sign_in(email, password):
    client = get_client()
    return client.auth.sign_in_with_password({"email": email, "password": password})


def sign_out():
    client = get_client()
    if client:
        try:
            client.auth.sign_out()
        except Exception:
            pass
    st.session_state.pop("user", None)
    st.session_state.pop("user_plan", None)


def get_profile(user_id):
    client = get_client()
    try:
        res = client.table("profiles").select("*").eq("id", user_id).single().execute()
        return res.data
    except Exception:
        return None


def ensure_profile(user_id, email):
    """Vai buscar o perfil do utilizador; cria-o com plano 'free' se ainda não existir."""
    client = get_client()
    profile = get_profile(user_id)
    if profile is None:
        try:
            client.table("profiles").insert({"id": user_id, "email": email, "plan": "free"}).execute()
        except Exception:
            pass
        profile = {"id": user_id, "email": email, "plan": "free"}
    return profile


def current_user():
    return st.session_state.get("user")


def current_plan():
    return st.session_state.get("user_plan", "free")


def is_logged_in():
    return current_user() is not None


def has_full_access():
    """True se o utilizador tem acesso completo às funcionalidades (premium ou admin)."""
    return current_plan() in ("premium", "admin")


def _login_form(suffix):
    """Separadores de login e registo; suffix distingue as keys entre sidebar e topo."""
    tab_login, tab_signup = st.tabs([_t("tab_login"), _t("tab_signup")])

    with tab_login:
        email = st.text_input(_t("email"), key=f"login_email{suffix}")
        pw = st.text_input(_t("password"), type="password", key=f"login_pw{suffix}")
        if st.button(_t("btn_login"), key=f"btn_login{suffix}", use_container_width=True):
            try:
                res = sign_in(email, pw)
                profile = ensure_profile(res.user.id, email)
                st.session_state["user"] = {"id": res.user.id, "email": email}
                st.session_state["user_plan"] = profile.get("plan", "free")
                st.rerun()
            except Exception:
                st.error(_t("err_login"))

    with tab_signup:
        email_s = st.text_input(_t("email"), key=f"signup_email{suffix}")
        pw_s = st.text_input(_t("password_min"), type="password", key=f"signup_pw{suffix}")
        if st.button(_t("btn_signup"), key=f"btn_signup{suffix}", use_container_width=True):
            if len(pw_s) < 6:
                st.error(_t("err_pw_short"))
            else:
                try:
                    sign_up(email_s, pw_s)
                    st.success(_t("ok_signup"))
                except Exception as e:
                    st.error(_t("err_signup", e=e))


def render_login_widget():
    """Widget de login/registo/sessão a colocar no topo da sidebar."""
    with st.sidebar:
        if not is_configured():
            st.caption(_t("not_configured_side"))
            st.markdown("---")
            return

        if is_logged_in():
            plano_labels = _plan_labels()
            st.markdown(f"👤 **{current_user()['email']}**")
            st.caption(plano_labels.get(current_plan(), current_plan()))
            if st.button(_t("logout"), use_container_width=True, key="btn_logout"):
                sign_out()
                st.rerun()
        else:
            with st.expander(_t("login_expander"), expanded=False):
                _login_form("")
        st.markdown("---")


def render_login_widget_top_right():
    """Widget de login/registo/sessão compacto, no canto superior direito de cada página."""
    st.markdown("""
    <style>
    div[data-testid="stPopover"] {
        display: flex;
        justify-content: flex-end;
    }
    </style>
    """, unsafe_allow_html=True)

    _, col_right = st.columns([5, 1])
    with col_right:
        if not is_configured():
            st.caption(_t("not_configured_top"))
            return

        if is_logged_in():
            plano_labels = _plan_labels()
            rotulo = f"👤 {current_user()['email'].split('@')[0]}"
            with st.popover(rotulo, use_container_width=True):
                st.markdown(f"**{current_user()['email']}**")
                st.caption(plano_labels.get(current_plan(), current_plan()))
                if st.button(_t("logout"), use_container_width=True, key="btn_logout_top"):
                    sign_out()
                    st.rerun()
        else:
            with st.popover(_t("login_popover"), use_container_width=True):
                _login_form("_top")


def render_locked_section(mensagem_extra=""):
    """Mostra um cartão de 'conteúdo bloqueado', usar quando has_full_access() é False."""
    extra = (" " + mensagem_extra) if mensagem_extra else ""
    st.markdown(f"""
    <div style="background:#0E2A3D;border-radius:10px;padding:24px;border:2px dashed #C29A4B;text-align:center;margin:16px 0;">
        <p style="color:#FAF8F3;font-size:1.1rem;font-weight:700;margin:0 0 8px 0;">{_t("locked_title")}</p>
        <p style="color:#C8D3DA;font-size:0.9rem;margin:0;">{_t("locked_body")}{extra}</p>
    </div>
    """, unsafe_allow_html=True)
