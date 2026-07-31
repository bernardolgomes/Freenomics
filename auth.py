"""
auth.py — Freenomics
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


def render_login_widget():
    """Widget de login/registo/sessão a colocar no topo da sidebar."""
    with st.sidebar:
        if not is_configured():
            st.caption("⚠️ Contas ainda não configuradas (falta ligar o Supabase).")
            st.markdown("---")
            return

        if is_logged_in():
            plano_labels = {"free": "🔓 Gratuito", "premium": "⭐ Premium", "admin": "👑 Admin"}
            st.markdown(f"👤 **{current_user()['email']}**")
            st.caption(plano_labels.get(current_plan(), current_plan()))
            if st.button("Sair", use_container_width=True, key="btn_logout"):
                sign_out()
                st.rerun()
        else:
            with st.expander("🔐 Entrar / Criar conta", expanded=False):
                tab_login, tab_signup = st.tabs(["Entrar", "Criar conta"])

                with tab_login:
                    email = st.text_input("Email", key="login_email")
                    pw = st.text_input("Password", type="password", key="login_pw")
                    if st.button("Entrar", key="btn_login", use_container_width=True):
                        try:
                            res = sign_in(email, pw)
                            profile = ensure_profile(res.user.id, email)
                            st.session_state["user"] = {"id": res.user.id, "email": email}
                            st.session_state["user_plan"] = profile.get("plan", "free")
                            st.rerun()
                        except Exception:
                            st.error("Email ou password inválidos.")

                with tab_signup:
                    email_s = st.text_input("Email", key="signup_email")
                    pw_s = st.text_input("Password (mín. 6 caracteres)", type="password", key="signup_pw")
                    if st.button("Criar conta", key="btn_signup", use_container_width=True):
                        if len(pw_s) < 6:
                            st.error("A password precisa de pelo menos 6 caracteres.")
                        else:
                            try:
                                sign_up(email_s, pw_s)
                                st.success("Conta criada! Verifica o teu email para confirmar (se pedido) e depois inicia sessão no separador 'Entrar'.")
                            except Exception as e:
                                st.error(f"Não foi possível criar a conta: {e}")
        st.markdown("---")


def render_locked_section(mensagem_extra=""):
    """Mostra um cartão de 'conteúdo bloqueado' — usar quando has_full_access() é False."""
    st.markdown(f"""
    <div style="background:#0E2A3D;border-radius:10px;padding:24px;border:2px dashed #C29A4B;text-align:center;margin:16px 0;">
        <p style="color:#FAF8F3;font-size:1.1rem;font-weight:700;margin:0 0 8px 0;">🔒 Resultados disponíveis para subscritores</p>
        <p style="color:#C8D3DA;font-size:0.9rem;margin:0;">Cria conta e subscreve para desbloqueares esta análise completa.{(' ' + mensagem_extra) if mensagem_extra else ''}</p>
    </div>
    """, unsafe_allow_html=True)
