import streamlit as st
import streamlit.components.v1 as components
import json
import plotly.graph_objects as go
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS, FIX_DROPDOWNS_JS

st.markdown(CSS, unsafe_allow_html=True)
components.html(FIX_DROPDOWNS_JS, height=0)
lang = st.session_state.get("lang", "🇵🇹 Português")

L = {
    "🇵🇹 Português": {
        "titulo": "Valor de Património",
        "subtitulo": "Regista os teus ativos e passivos para acompanhar a evolução do teu património líquido ao longo do tempo.",
        "contas": "🏦 Contas Bancárias",
        "investimentos": "📈 Investimentos & Brokers",
        "reforma": "🏖️ Planos de Reforma",
        "imoveis": "🏠 Imóveis",
        "outros": "🚗 Outros Ativos",
        "passivos": "💳 Passivos & Dívidas",
        "nome_label": "Nome / Descrição",
        "valor_label": "Valor",
        "moeda_label": "Moeda",
        "btn_add": "➕ Adicionar",
        "btn_calcular": "💎 Calcular Património",
        "resumo_titulo": "💎 Resumo do Património",
        "total_ativos": "Total de Ativos",
        "total_passivos": "Total de Passivos",
        "patrimonio_liq": "Património Líquido",
        "dist_titulo": "Distribuição por categoria",
        "snap_titulo": "📅 Guardar / Comparar",
        "snap_desc": "Guarda um snapshot do teu património atual para comparar a evolução futura.",
        "btn_guardar": "💾 Guardar snapshot",
        "btn_upload": "📂 Carregar snapshot anterior",
        "upload_label": "Seleciona o ficheiro JSON de um snapshot anterior",
        "evolucao_titulo": "📈 Evolução desde o último snapshot",
        "data_anterior": "Data do snapshot anterior",
        "data_atual": "Data atual",
        "variacao": "Variação",
        "por_categoria": "Variação por categoria",
        "aviso": "Os valores são guardados localmente no teu dispositivo — os teus dados não são partilhados.",
        "rodape": "Freenomics · Calculadora de Património Líquido",
        "passivos_nota": "Os passivos são subtraídos do total para calcular o património líquido.",
        "snapshot_nome": "freenomics_patrimonio",
        "categorias": ["🏦 Contas Bancárias", "📈 Investimentos & Brokers", "🏖️ Planos de Reforma", "🏠 Imóveis", "🚗 Outros Ativos"],
        "cat_keys": ["contas", "investimentos", "reforma", "imoveis", "outros"],
    },
    "🇬🇧 English": {
        "titulo": "Net Worth Tracker",
        "subtitulo": "Record your assets and liabilities to track the evolution of your net worth over time.",
        "contas": "🏦 Bank Accounts",
        "investimentos": "📈 Investments & Brokers",
        "reforma": "🏖️ Retirement Plans",
        "imoveis": "🏠 Real Estate",
        "outros": "🚗 Other Assets",
        "passivos": "💳 Liabilities & Debts",
        "nome_label": "Name / Description",
        "valor_label": "Value",
        "moeda_label": "Currency",
        "btn_add": "➕ Add",
        "btn_calcular": "💎 Calculate Net Worth",
        "resumo_titulo": "💎 Net Worth Summary",
        "total_ativos": "Total Assets",
        "total_passivos": "Total Liabilities",
        "patrimonio_liq": "Net Worth",
        "dist_titulo": "Distribution by category",
        "snap_titulo": "📅 Save / Compare",
        "snap_desc": "Save a snapshot of your current net worth to compare future evolution.",
        "btn_guardar": "💾 Save snapshot",
        "btn_upload": "📂 Load previous snapshot",
        "upload_label": "Select the JSON file from a previous snapshot",
        "evolucao_titulo": "📈 Evolution since last snapshot",
        "data_anterior": "Previous snapshot date",
        "data_atual": "Current date",
        "variacao": "Change",
        "por_categoria": "Change by category",
        "aviso": "Values are saved locally on your device — your data is not shared.",
        "rodape": "Freenomics · Net Worth Calculator",
        "passivos_nota": "Liabilities are subtracted from the total to calculate net worth.",
        "snapshot_nome": "freenomics_networth",
        "categorias": ["🏦 Bank Accounts", "📈 Investments & Brokers", "🏖️ Retirement Plans", "🏠 Real Estate", "🚗 Other Assets"],
        "cat_keys": ["contas", "investimentos", "reforma", "imoveis", "outros"],
    },
    "🇫🇷 Français": {
        "titulo": "Patrimoine Net",
        "subtitulo": "Enregistrez vos actifs et passifs pour suivre l'évolution de votre patrimoine net.",
        "contas": "🏦 Comptes Bancaires",
        "investimentos": "📈 Investissements & Brokers",
        "reforma": "🏖️ Plans Retraite",
        "imoveis": "🏠 Immobilier",
        "outros": "🚗 Autres Actifs",
        "passivos": "💳 Passifs & Dettes",
        "nome_label": "Nom / Description",
        "valor_label": "Valeur",
        "moeda_label": "Devise",
        "btn_add": "➕ Ajouter",
        "btn_calcular": "💎 Calculer le Patrimoine",
        "resumo_titulo": "💎 Résumé du Patrimoine",
        "total_ativos": "Total des Actifs",
        "total_passivos": "Total des Passifs",
        "patrimonio_liq": "Patrimoine Net",
        "dist_titulo": "Répartition par catégorie",
        "snap_titulo": "📅 Sauvegarder / Comparer",
        "snap_desc": "Sauvegardez un instantané de votre patrimoine actuel pour comparer l'évolution future.",
        "btn_guardar": "💾 Sauvegarder",
        "btn_upload": "📂 Charger un instantané précédent",
        "upload_label": "Sélectionnez le fichier JSON d'un instantané précédent",
        "evolucao_titulo": "📈 Évolution depuis le dernier instantané",
        "data_anterior": "Date de l'instantané précédent",
        "data_atual": "Date actuelle",
        "variacao": "Variation",
        "por_categoria": "Variation par catégorie",
        "aviso": "Les valeurs sont sauvegardées localement sur votre appareil.",
        "rodape": "Freenomics · Calculateur de Patrimoine Net",
        "passivos_nota": "Les passifs sont soustraits du total pour calculer le patrimoine net.",
        "snapshot_nome": "freenomics_patrimoine",
        "categorias": ["🏦 Comptes Bancaires", "📈 Investissements & Brokers", "🏖️ Plans Retraite", "🏠 Immobilier", "🚗 Autres Actifs"],
        "cat_keys": ["contas", "investimentos", "reforma", "imoveis", "outros"],
    },
    "🇩🇪 Deutsch": {
        "titulo": "Vermögensrechner",
        "subtitulo": "Erfassen Sie Ihre Vermögenswerte und Schulden, um die Entwicklung Ihres Nettovermögens zu verfolgen.",
        "contas": "🏦 Bankkonten",
        "investimentos": "📈 Investitionen & Broker",
        "reforma": "🏖️ Rentenpläne",
        "imoveis": "🏠 Immobilien",
        "outros": "🚗 Sonstige Vermögenswerte",
        "passivos": "💳 Verbindlichkeiten & Schulden",
        "nome_label": "Name / Beschreibung",
        "valor_label": "Wert",
        "moeda_label": "Währung",
        "btn_add": "➕ Hinzufügen",
        "btn_calcular": "💎 Vermögen berechnen",
        "resumo_titulo": "💎 Vermögensübersicht",
        "total_ativos": "Gesamtvermögen",
        "total_passivos": "Gesamtschulden",
        "patrimonio_liq": "Nettovermögen",
        "dist_titulo": "Verteilung nach Kategorie",
        "snap_titulo": "📅 Speichern / Vergleichen",
        "snap_desc": "Speichern Sie einen Schnappschuss Ihres aktuellen Vermögens.",
        "btn_guardar": "💾 Schnappschuss speichern",
        "btn_upload": "📂 Vorherigen Schnappschuss laden",
        "upload_label": "Wählen Sie die JSON-Datei eines vorherigen Schnappschusses",
        "evolucao_titulo": "📈 Entwicklung seit dem letzten Schnappschuss",
        "data_anterior": "Datum des vorherigen Schnappschusses",
        "data_atual": "Aktuelles Datum",
        "variacao": "Veränderung",
        "por_categoria": "Veränderung nach Kategorie",
        "aviso": "Werte werden lokal auf Ihrem Gerät gespeichert — Ihre Daten werden nicht geteilt.",
        "rodape": "Freenomics · Nettovermögensrechner",
        "passivos_nota": "Verbindlichkeiten werden vom Gesamtvermögen abgezogen.",
        "snapshot_nome": "freenomics_vermoegen",
        "categorias": ["🏦 Bankkonten", "📈 Investitionen & Broker", "🏖️ Rentenpläne", "🏠 Immobilien", "🚗 Sonstige Vermögenswerte"],
        "cat_keys": ["contas", "investimentos", "reforma", "imoveis", "outros"],
    },
    "🇪🇸 Español": {
        "titulo": "Patrimonio Neto",
        "subtitulo": "Registra tus activos y pasivos para seguir la evolución de tu patrimonio neto a lo largo del tiempo.",
        "contas": "🏦 Cuentas Bancarias",
        "investimentos": "📈 Inversiones & Brokers",
        "reforma": "🏖️ Planes de Jubilación",
        "imoveis": "🏠 Inmuebles",
        "outros": "🚗 Otros Activos",
        "passivos": "💳 Pasivos & Deudas",
        "nome_label": "Nombre / Descripción",
        "valor_label": "Valor",
        "moeda_label": "Divisa",
        "btn_add": "➕ Añadir",
        "btn_calcular": "💎 Calcular Patrimonio",
        "resumo_titulo": "💎 Resumen del Patrimonio",
        "total_ativos": "Total de Activos",
        "total_passivos": "Total de Pasivos",
        "patrimonio_liq": "Patrimonio Neto",
        "dist_titulo": "Distribución por categoría",
        "snap_titulo": "📅 Guardar / Comparar",
        "snap_desc": "Guarda un instantáneo de tu patrimonio actual para comparar la evolución futura.",
        "btn_guardar": "💾 Guardar instantáneo",
        "btn_upload": "📂 Cargar instantáneo anterior",
        "upload_label": "Selecciona el archivo JSON de un instantáneo anterior",
        "evolucao_titulo": "📈 Evolución desde el último instantáneo",
        "data_anterior": "Fecha del instantáneo anterior",
        "data_atual": "Fecha actual",
        "variacao": "Variación",
        "por_categoria": "Variación por categoría",
        "aviso": "Los valores se guardan localmente en tu dispositivo — tus datos no se comparten.",
        "rodape": "Freenomics · Calculadora de Patrimonio Neto",
        "passivos_nota": "Los pasivos se restan del total para calcular el patrimonio neto.",
        "snapshot_nome": "freenomics_patrimonio",
        "categorias": ["🏦 Cuentas Bancarias", "📈 Inversiones & Brokers", "🏖️ Planes de Jubilación", "🏠 Inmuebles", "🚗 Otros Activos"],
        "cat_keys": ["contas", "investimentos", "reforma", "imoveis", "outros"],
    },
}.get(lang, {})

# ── CABEÇALHO ─────────────────────────────────────────────────
show_logo()
st.title(L["titulo"])
st.caption(L["subtitulo"])

# ── INICIALIZAR SESSION STATE ─────────────────────────────────
cat_keys    = L["cat_keys"]
cat_labels  = L["categorias"]

for key in cat_keys + ["passivos"]:
    if f"pat_{key}" not in st.session_state:
        st.session_state[f"pat_{key}"] = [
            {"nome": "", "valor": 0.0, "moeda": "EUR"}
        ]

# ── FUNÇÃO PARA RENDERIZAR UMA CATEGORIA ─────────────────────
def render_categoria(key, titulo, cor_borda="#C29A4B"):
    lista = st.session_state[f"pat_{key}"]
    remover = None

    st.markdown(f"""
    <div style="border-left:4px solid {cor_borda};padding-left:12px;margin-bottom:8px;">
        <p style="color:#0E2A3D;font-size:1.1rem;font-weight:700;margin:0;">{titulo}</p>
    </div>""", unsafe_allow_html=True)

    for i, item in enumerate(lista):
        c1, c2, c3, c4 = st.columns([3, 2, 1, 0.4])
        with c1:
            lista[i]["nome"] = st.text_input(
                L["nome_label"], value=item["nome"],
                key=f"{key}_nome_{i}",
                placeholder="ex: Conta CGD",
                label_visibility="collapsed" if i > 0 else "visible")
        with c2:
            lista[i]["valor"] = st.number_input(
                L["valor_label"], value=float(item["valor"]),
                min_value=0.0, step=100.0, format="%.2f",
                key=f"{key}_val_{i}",
                label_visibility="collapsed" if i > 0 else "visible")
        with c3:
            lista[i]["moeda"] = st.selectbox(
                L["moeda_label"], ["EUR", "USD"],
                index=0 if item["moeda"] == "EUR" else 1,
                key=f"{key}_mo_{i}",
                label_visibility="collapsed" if i > 0 else "visible")
        with c4:
            if len(lista) > 1:
                st.markdown("<br>" if i == 0 else "", unsafe_allow_html=True)
                if st.button("🗑️", key=f"{key}_rm_{i}"):
                    remover = i

    if remover is not None:
        lista.pop(remover)
        st.rerun()

    if st.button(L["btn_add"], key=f"{key}_add"):
        lista.append({"nome": "", "valor": 0.0, "moeda": "EUR"})
        st.rerun()

    st.markdown("")

# ── FUNÇÃO PARA SOMAR UMA CATEGORIA ──────────────────────────
@st.cache_data(ttl=3600)
def get_eurusd_rate():
    try:
        import yfinance as yf
        fx = yf.download("EURUSD=X", period="1d", progress=False)
        close = fx["Close"]
        if hasattr(close, 'iloc'):
            import pandas as pd
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            return float(close.squeeze().iloc[-1])
    except Exception:
        pass
    return 1.08

def total_categoria_eur(key):
    eurusd = get_eurusd_rate()
    usdeur = 1 / eurusd
    total = 0.0
    for item in st.session_state[f"pat_{key}"]:
        v = item["valor"]
        if item["moeda"] == "USD":
            v = v * usdeur
        total += v
    return total

# ── FORMULÁRIO ────────────────────────────────────────────────
st.markdown("---")

# Ativos
for key, label in zip(cat_keys, cat_labels):
    render_categoria(key, label)
    st.markdown("")

st.markdown("---")

# Passivos
render_categoria("passivos", L["passivos"], cor_borda="#F44336")
st.caption(L["passivos_nota"])

st.markdown("---")

# Botão calcular
calcular = st.button(L["btn_calcular"], type="primary", use_container_width=True)

if not calcular and "pat_resultado" not in st.session_state:
    st.stop()

if calcular:
    totais = {key: total_categoria_eur(key) for key in cat_keys}
    totais["passivos"] = total_categoria_eur("passivos")
    st.session_state["pat_resultado"] = {
        "totais": totais,
        "data": datetime.today().strftime("%Y-%m-%d %H:%M"),
        "items": {key: list(st.session_state[f"pat_{key}"]) for key in cat_keys + ["passivos"]},
    }

res = st.session_state.get("pat_resultado", {})
totais = res.get("totais", {})
data_atual = res.get("data", datetime.today().strftime("%Y-%m-%d %H:%M"))

total_ativos   = sum(totais.get(k, 0) for k in cat_keys)
total_passivos = totais.get("passivos", 0)
patrimonio     = total_ativos - total_passivos

def cor(v): return "#4CAF50" if v >= 0 else "#F44336"

# ── RESUMO ────────────────────────────────────────────────────
st.markdown("---")
st.subheader(L["resumo_titulo"])

c1, c2, c3 = st.columns(3)
def big_card(label, valor, cor_hex):
    return f"""<div style="background:#0E2A3D;border-radius:10px;padding:20px 24px;
        border-left:4px solid {cor_hex};margin-bottom:12px;">
        <p style="color:#C8D3DA;font-size:0.85rem;margin:0 0 6px 0;">{label}</p>
        <p style="color:{cor_hex};font-size:2rem;font-weight:700;margin:0;">€{valor:,.0f}</p>
    </div>"""

with c1: st.markdown(big_card(L["total_ativos"],   total_ativos,   "#C29A4B"), unsafe_allow_html=True)
with c2: st.markdown(big_card(L["total_passivos"], total_passivos, "#F44336"), unsafe_allow_html=True)
with c3: st.markdown(big_card(L["patrimonio_liq"], patrimonio,     cor(patrimonio)), unsafe_allow_html=True)

# Guarda o estado atual desta página para a página de Exportar reutilizar
st.session_state["export_patrimonio"] = {
    "total_ativos": total_ativos, "total_passivos": total_passivos,
    "patrimonio": patrimonio,
    "categorias": [(label, totais.get(k, 0)) for k, label in zip(cat_keys, cat_labels)],
    "data": data_atual,
}

# ── GRÁFICOS ──────────────────────────────────────────────────
col_pie, col_bar = st.columns(2)

with col_pie:
    st.subheader(L["dist_titulo"])
    labels_pie = [L[k] for k in cat_keys if totais.get(k, 0) > 0]
    values_pie = [totais.get(k, 0) for k in cat_keys if totais.get(k, 0) > 0]
    cores = ["#0E2A3D", "#C29A4B", "#6B8E7F", "#A8453E", "#5C6B73"]
    if values_pie:
        fig_pie = go.Figure(go.Pie(
            labels=labels_pie, values=values_pie,
            marker=dict(colors=cores[:len(values_pie)]),
            textinfo="label+percent", hole=0.4))
        fig_pie.update_layout(
            paper_bgcolor="#FAF8F3", showlegend=False, height=320,
            margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_pie, use_container_width=True)

with col_bar:
    st.subheader("€ por categoria")
    todas_cats   = cat_labels + [L["passivos"]]
    todas_values = [totais.get(k, 0) for k in cat_keys] + [totais.get("passivos", 0)]
    todas_cores  = cores[:len(cat_keys)] + ["#F44336"]
    fig_bar = go.Figure(go.Bar(
        x=todas_cats, y=todas_values,
        marker_color=todas_cores, opacity=0.85))
    fig_bar.update_layout(
        plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
        yaxis_title="€", height=320,
        margin=dict(l=0, r=0, t=10, b=0))
    st.plotly_chart(fig_bar, use_container_width=True)

# ── SNAPSHOT: GUARDAR ─────────────────────────────────────────
st.markdown("---")
st.subheader(L["snap_titulo"])
st.caption(L["snap_desc"])

snapshot_data = {
    "data": data_atual,
    "lingua": lang,
    "patrimonio_liquido": patrimonio,
    "total_ativos": total_ativos,
    "total_passivos": total_passivos,
    "totais_por_categoria": totais,
    "items": res.get("items", {}),
}

nome_ficheiro = f"{L['snapshot_nome']}_{data_atual[:10]}.json"
st.download_button(
    label=L["btn_guardar"],
    data=json.dumps(snapshot_data, ensure_ascii=False, indent=2),
    file_name=nome_ficheiro,
    mime="application/json",
    use_container_width=True,
)
st.caption(f"💡 {L['aviso']}")

# ── SNAPSHOT: COMPARAR ────────────────────────────────────────
st.markdown("---")
uploaded = st.file_uploader(L["btn_upload"], type=["json"], label_visibility="visible")

if uploaded:
    try:
        anterior = json.loads(uploaded.read())
        pat_anterior = anterior.get("patrimonio_liquido", 0)
        totais_ant   = anterior.get("totais_por_categoria", {})
        data_ant     = anterior.get("data", "?")

        st.subheader(L["evolucao_titulo"])

        col_d1, col_d2, col_d3 = st.columns(3)
        variacao_total = patrimonio - pat_anterior
        variacao_pct   = (variacao_total / pat_anterior * 100) if pat_anterior != 0 else 0

        with col_d1:
            st.markdown(big_card(L["data_anterior"], pat_anterior, "#6B7280"), unsafe_allow_html=True)
            st.caption(f"📅 {data_ant}")
        with col_d2:
            st.markdown(big_card(L["data_atual"], patrimonio, "#C29A4B"), unsafe_allow_html=True)
            st.caption(f"📅 {data_atual}")
        with col_d3:
            st.markdown(big_card(L["variacao"],
                variacao_total, cor(variacao_total)), unsafe_allow_html=True)
            st.caption(f"{variacao_pct:+.1f}%")

        # Variação por categoria
        st.subheader(L["por_categoria"])
        cat_vars   = []
        cat_names  = []
        cat_colors = []
        for k, label in zip(cat_keys, cat_labels):
            atual_v = totais.get(k, 0)
            ant_v   = totais_ant.get(k, 0)
            diff    = atual_v - ant_v
            cat_vars.append(diff)
            cat_names.append(label)
            cat_colors.append("#4CAF50" if diff >= 0 else "#F44336")

        fig_ev = go.Figure(go.Bar(
            x=cat_names, y=cat_vars,
            marker_color=cat_colors, opacity=0.85,
            text=[f"€{v:+,.0f}" for v in cat_vars],
            textposition="outside"))
        fig_ev.update_layout(
            plot_bgcolor="#FAF8F3", paper_bgcolor="#FAF8F3",
            yaxis_title="€ variação", height=380,
            margin=dict(l=0, r=0, t=30, b=0))
        fig_ev.add_hline(y=0, line_color="#888888", line_width=1)
        st.plotly_chart(fig_ev, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao ler o ficheiro: {e}")

st.markdown("---")
st.caption(L["rodape"])
