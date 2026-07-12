"""
Exportar Relatório — Freenomics
Página dedicada para gerar um PDF completo com as secções selecionadas.
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import requests
import io
import sys
import os
from datetime import datetime, timedelta
import sys as _sys, os as _os
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(__file__)))
from utils import show_logo
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table,
    TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from utils import show_logo
from translations import CSS

st.markdown(CSS, unsafe_allow_html=True)
lang = st.session_state.get("lang", "🇵🇹 Português")

# ── TRADUÇÕES DESTA PÁGINA ────────────────────────────────────
T = {
    "🇵🇹 Português": {
        "titulo": "Exportar Relatório Completo",
        "subtitulo": "Seleciona as secções que queres incluir e gera um PDF personalizado.",
        "config_global": "⚙️ Configuração geral",
        "tickers": "Tickers da carteira (separados por vírgula)",
        "periodo": "Período de análise",
        "investimento": "Capital investido (€)",
        "periodos": {"6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825},
        "secoes_titulo": "📋 Secções a incluir",
        "sec_dashboard": "📊 Análise de Carteira",
        "sec_comparador": "🔄 Comparador de Carteiras",
        "sec_simulador": "💰 Simulador de Investimento",
        "sec_risco": "⚠️ Análise de Risco",
        "sec_noticias": "📰 Notícias da Carteira",
        "noticias_max_pdf": "Notícias por ativo no relatório",
        "a_carregar_noticias": "A carregar notícias...",
        "config_comparador": "🔄 Configuração do Comparador",
        "tickers_a": "Carteira A (tickers)",
        "tickers_b": "Carteira B (tickers)",
        "config_simulador": "💰 Configuração do Simulador",
        "contrib": "Contribuição mensal (€)",
        "anos": "Anos de investimento",
        "retorno_esp": "Retorno anual esperado (%)",
        "inflacao": "Inflação estimada (%)",
        "api_titulo": "🤖 Análise com IA (opcional)",
        "api_key": "Anthropic API Key",
        "api_placeholder": "sk-ant-...",
        "api_help": "Se preenchida, os insights são gerados por IA. Caso contrário, usa análise automática.",
        "btn_gerar": "📄 Gerar e descarregar relatório PDF",
        "a_gerar": "A gerar relatório...",
        "a_carregar_dados": "A carregar dados de mercado...",
        "a_gerar_insights": "A gerar análise com IA...",
        "sucesso": "✅ Relatório gerado com sucesso!",
        "erro_tickers": "Não foi possível carregar dados para os tickers indicados.",
        "seleciona_uma": "Seleciona pelo menos uma secção para incluir no relatório.",
        "pdf_titulo": "Relatório de Investimento",
        "pdf_gerado": "Gerado por Freenomics",
        "pdf_periodo": "Período",
        "pdf_nome": "relatorio_freenomics_completo.pdf",
        "rodape": "Freenomics · Dados via Yahoo Finance · Não constitui aconselhamento financeiro.",
    },
    "🇬🇧 English": {
        "titulo": "Export Full Report",
        "subtitulo": "Select the sections you want to include and generate a personalised PDF.",
        "config_global": "⚙️ General configuration",
        "tickers": "Portfolio tickers (comma-separated)",
        "periodo": "Analysis period",
        "investimento": "Invested capital (€)",
        "periodos": {"6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825},
        "secoes_titulo": "📋 Sections to include",
        "sec_dashboard": "📊 Portfolio Analysis",
        "sec_comparador": "🔄 Portfolio Comparator",
        "sec_simulador": "💰 Investment Simulator",
        "sec_risco": "⚠️ Risk Analysis",
        "sec_noticias": "📰 Portfolio News",
        "noticias_max_pdf": "News per asset in report",
        "a_carregar_noticias": "Loading news...",
        "tickers_a": "Portfolio A (tickers)",
        "tickers_b": "Portfolio B (tickers)",
        "config_simulador": "💰 Simulator configuration",
        "contrib": "Monthly contribution (€)",
        "anos": "Investment years",
        "retorno_esp": "Expected annual return (%)",
        "inflacao": "Estimated inflation (%)",
        "api_titulo": "🤖 AI Analysis (optional)",
        "api_key": "Anthropic API Key",
        "api_placeholder": "sk-ant-...",
        "api_help": "If filled, insights are AI-generated. Otherwise, uses automatic analysis.",
        "btn_gerar": "📄 Generate and download PDF report",
        "a_gerar": "Generating report...",
        "a_carregar_dados": "Loading market data...",
        "a_gerar_insights": "Generating AI analysis...",
        "sucesso": "✅ Report successfully generated!",
        "erro_tickers": "Could not load data for the indicated tickers.",
        "seleciona_uma": "Select at least one section to include in the report.",
        "pdf_titulo": "Investment Report",
        "pdf_gerado": "Generated by Freenomics",
        "pdf_periodo": "Period",
        "pdf_nome": "freenomics_full_report.pdf",
        "rodape": "Freenomics · Data via Yahoo Finance · Does not constitute financial advice.",
    },
    "🇫🇷 Français": {
        "titulo": "Exporter le Rapport Complet",
        "subtitulo": "Sélectionnez les sections à inclure et générez un PDF personnalisé.",
        "config_global": "⚙️ Configuration générale",
        "tickers": "Tickers du portefeuille (séparés par virgule)",
        "periodo": "Période d'analyse",
        "investimento": "Capital investi (€)",
        "periodos": {"6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825},
        "secoes_titulo": "📋 Sections à inclure",
        "sec_dashboard": "📊 Analyse de Portefeuille",
        "sec_comparador": "🔄 Comparateur",
        "sec_simulador": "💰 Simulateur",
        "sec_risco": "⚠️ Analyse des Risques",
        "sec_noticias": "📰 Actualités du Portefeuille",
        "noticias_max_pdf": "Actualités par actif dans le rapport",
        "a_carregar_noticias": "Chargement des actualités...",
        "tickers_a": "Portefeuille A (tickers)",
        "tickers_b": "Portefeuille B (tickers)",
        "config_simulador": "💰 Configuration du simulateur",
        "contrib": "Contribution mensuelle (€)",
        "anos": "Années d'investissement",
        "retorno_esp": "Rendement annuel attendu (%)",
        "inflacao": "Inflation estimée (%)",
        "api_titulo": "🤖 Analyse IA (optionnel)",
        "api_key": "Clé API Anthropic",
        "api_placeholder": "sk-ant-...",
        "api_help": "Si renseignée, les insights sont générés par IA.",
        "btn_gerar": "📄 Générer et télécharger le rapport PDF",
        "a_gerar": "Génération du rapport...",
        "a_carregar_dados": "Chargement des données...",
        "a_gerar_insights": "Génération de l'analyse IA...",
        "sucesso": "✅ Rapport généré avec succès!",
        "erro_tickers": "Impossible de charger les données pour les tickers indiqués.",
        "seleciona_uma": "Sélectionnez au moins une section.",
        "pdf_titulo": "Rapport d'Investissement",
        "pdf_gerado": "Généré par Freenomics",
        "pdf_periodo": "Période",
        "pdf_nome": "rapport_freenomics_complet.pdf",
        "rodape": "Freenomics · Données via Yahoo Finance · Ne constitue pas un conseil financier.",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Vollständigen Bericht exportieren",
        "subtitulo": "Wählen Sie die gewünschten Abschnitte und erstellen Sie ein personalisiertes PDF.",
        "config_global": "⚙️ Allgemeine Konfiguration",
        "tickers": "Portfolio-Ticker (kommagetrennt)",
        "periodo": "Analysezeitraum",
        "investimento": "Investiertes Kapital (€)",
        "periodos": {"6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
        "secoes_titulo": "📋 Einzuschließende Abschnitte",
        "sec_dashboard": "📊 Portfolio-Analyse",
        "sec_comparador": "🔄 Portfolio-Vergleich",
        "sec_simulador": "💰 Investitionssimulator",
        "sec_risco": "⚠️ Risikoanalyse",
        "sec_noticias": "📰 Portfolio-Nachrichten",
        "noticias_max_pdf": "Nachrichten pro Anlage im Bericht",
        "a_carregar_noticias": "Nachrichten werden geladen...",
        "tickers_a": "Portfolio A (Ticker)",
        "tickers_b": "Portfolio B (Ticker)",
        "config_simulador": "💰 Simulatorkonfiguration",
        "contrib": "Monatlicher Beitrag (€)",
        "anos": "Anlagejahre",
        "retorno_esp": "Erwartete Jahresrendite (%)",
        "inflacao": "Geschätzte Inflation (%)",
        "api_titulo": "🤖 KI-Analyse (optional)",
        "api_key": "Anthropic API-Schlüssel",
        "api_placeholder": "sk-ant-...",
        "api_help": "Falls angegeben, werden Insights KI-generiert.",
        "btn_gerar": "📄 PDF-Bericht erstellen und herunterladen",
        "a_gerar": "Bericht wird erstellt...",
        "a_carregar_dados": "Marktdaten werden geladen...",
        "a_gerar_insights": "KI-Analyse wird generiert...",
        "sucesso": "✅ Bericht erfolgreich erstellt!",
        "erro_tickers": "Daten für die angegebenen Ticker konnten nicht geladen werden.",
        "seleciona_uma": "Wählen Sie mindestens einen Abschnitt aus.",
        "pdf_titulo": "Investitionsbericht",
        "pdf_gerado": "Erstellt von Freenomics",
        "pdf_periodo": "Zeitraum",
        "pdf_nome": "freenomics_vollstaendiger_bericht.pdf",
        "rodape": "Freenomics · Daten via Yahoo Finance · Stellt keine Finanzberatung dar.",
    },
    "🇪🇸 Español": {
        "titulo": "Exportar Informe Completo",
        "subtitulo": "Selecciona las secciones que quieres incluir y genera un PDF personalizado.",
        "config_global": "⚙️ Configuración general",
        "tickers": "Tickers de la cartera (separados por coma)",
        "periodo": "Período de análisis",
        "investimento": "Capital invertido (€)",
        "periodos": {"6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825},
        "secoes_titulo": "📋 Secciones a incluir",
        "sec_dashboard": "📊 Análisis de Cartera",
        "sec_comparador": "🔄 Comparador de Carteras",
        "sec_simulador": "💰 Simulador de Inversión",
        "sec_risco": "⚠️ Análisis de Riesgo",
        "sec_noticias": "📰 Noticias de la Cartera",
        "noticias_max_pdf": "Noticias por activo en el informe",
        "a_carregar_noticias": "Cargando noticias...",
        "tickers_a": "Cartera A (tickers)",
        "tickers_b": "Cartera B (tickers)",
        "config_simulador": "💰 Configuración del simulador",
        "contrib": "Contribución mensual (€)",
        "anos": "Años de inversión",
        "retorno_esp": "Rentabilidad anual esperada (%)",
        "inflacao": "Inflación estimada (%)",
        "api_titulo": "🤖 Análisis con IA (opcional)",
        "api_key": "Clave API de Anthropic",
        "api_placeholder": "sk-ant-...",
        "api_help": "Si se rellena, los insights son generados por IA.",
        "btn_gerar": "📄 Generar y descargar informe PDF",
        "a_gerar": "Generando informe...",
        "a_carregar_dados": "Cargando datos de mercado...",
        "a_gerar_insights": "Generando análisis con IA...",
        "sucesso": "✅ ¡Informe generado con éxito!",
        "erro_tickers": "No se pudieron cargar datos para los tickers indicados.",
        "seleciona_uma": "Selecciona al menos una sección para incluir en el informe.",
        "pdf_titulo": "Informe de Inversión",
        "pdf_gerado": "Generado por Freenomics",
        "pdf_periodo": "Período",
        "pdf_nome": "informe_freenomics_completo.pdf",
        "rodape": "Freenomics · Datos via Yahoo Finance · No constituye asesoramiento financiero.",
    },
}[lang]

# ── CABEÇALHO ────────────────────────────────────────────────
show_logo()
st.title(T["titulo"])
st.caption(T["subtitulo"])

# ── CONFIGURAÇÃO GERAL ───────────────────────────────────────
st.header(T.get("config_global", "⚙️ Configuration"))
col1, col2, col3 = st.columns(3)
with col1:
    tickers_input = st.text_input(T["tickers"], value="SPY, SOFI")
    tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
with col2:
    periodo_opcoes = T["periodos"]
    periodo_label = st.selectbox(T["periodo"], list(periodo_opcoes.keys()), index=2)
    dias = periodo_opcoes[periodo_label]
with col3:
    investimento = st.number_input(T["investimento"], value=10000, step=500)

# ── SECÇÕES ──────────────────────────────────────────────────
st.header(T.get("secoes_titulo", "📋 Sections"))
col_a, col_b, col_c, col_d, col_e = st.columns(5)
inc_dashboard  = col_a.checkbox(T["sec_dashboard"],  value=True)
inc_comparador = col_b.checkbox(T["sec_comparador"], value=True)
inc_simulador  = col_c.checkbox(T["sec_simulador"],  value=True)
inc_risco      = col_d.checkbox(T["sec_risco"],      value=True)
inc_noticias   = col_e.checkbox(T["sec_noticias"],   value=True)

if inc_noticias:
    noticias_max_pdf = st.slider(T["noticias_max_pdf"], 2, 8, 3)

# ── CONFIG COMPARADOR ────────────────────────────────────────
if inc_comparador:
    st.subheader(T.get("config_comparador", "🔄 Comparator"))
    cc1, cc2 = st.columns(2)
    tickers_a_str = cc1.text_input(T["tickers_a"], value=tickers_input)
    tickers_b_str = cc2.text_input(T["tickers_b"], value="QQQ, AAPL")

# ── CONFIG SIMULADOR ─────────────────────────────────────────
if inc_simulador:
    st.subheader(T.get("config_simulador", "💰 Simulator"))
    cs1, cs2, cs3, cs4 = st.columns(4)
    contrib     = cs1.number_input(T["contrib"], value=200, step=50)
    anos_sim    = cs2.slider(T["anos"], 1, 40, 10)
    retorno_esp = cs3.slider(T["retorno_esp"], 1.0, 20.0, 8.0, step=0.5)
    inflacao    = cs4.slider(T["inflacao"], 0.0, 6.0, 2.5, step=0.5)

# ── API KEY ──────────────────────────────────────────────────
st.header(T.get("api_titulo", "🤖 AI Analysis"))
api_key = st.text_input(T["api_key"], type="password",
                        placeholder=T["api_placeholder"], help=T["api_help"])

st.markdown("---")

# ── FUNÇÕES DE DADOS ─────────────────────────────────────────
@st.cache_data(ttl=3600)
def carregar(ticker, dias):
    end = datetime.today(); start = end - timedelta(days=dias)
    return yf.download(ticker, start=start, end=end, progress=False)

def calc_metricas(df):
    precos = df["Close"]
    if isinstance(precos, pd.DataFrame):
        precos = precos.iloc[:, 0]
    precos = precos.squeeze()
    ret    = float((precos.iloc[-1] / precos.iloc[0] - 1) * 100)
    rd     = precos.pct_change().dropna()
    vol    = float(rd.std() * np.sqrt(252) * 100)
    dd     = float(((precos - precos.cummax()) / precos.cummax()).min() * 100)
    sharpe = float((rd.mean() / rd.std()) * np.sqrt(252)) if rd.std().item() != 0 else 0.0
    return {"retorno_total": round(ret,2), "volatilidade": round(vol,2),
            "max_drawdown": round(dd,2), "sharpe": round(sharpe,2)}

def retorno_carteira(tickers_str, dias):
    tickers_l = [t.strip().upper() for t in tickers_str.split(",") if t.strip()]
    series = []
    for t in tickers_l:
        df = carregar(t, dias)
        if not df.empty:
            close = df["Close"]
            if isinstance(close, pd.DataFrame):
                close = close.iloc[:, 0]
            close = close.squeeze()
            series.append(close / close.iloc[0])
    if not series: return None, []
    return pd.concat(series, axis=1).mean(axis=1), tickers_l

LINGUA_NOME = {
    "🇵🇹 Português": "português europeu", "🇬🇧 English": "English",
    "🇫🇷 Français": "français", "🇩🇪 Deutsch": "Deutsch", "🇪🇸 Español": "español",
}

def chamar_api(prompt, api_key):
    try:
        r = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"x-api-key": api_key, "anthropic-version": "2023-06-01", "content-type": "application/json"},
            json={"model": "claude-haiku-4-5-20251001", "max_tokens": 500,
                  "messages": [{"role": "user", "content": prompt}]},
            timeout=30,
        )
        if r.status_code == 200:
            return r.json()["content"][0]["text"]
    except Exception:
        pass
    return None

# ── GERADOR DE PDF ───────────────────────────────────────────
def gerar_pdf_completo(secoes):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4,
                            leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=2*cm, bottomMargin=2*cm)
    AZUL    = colors.HexColor("#0E2A3D")
    DOURADO = colors.HexColor("#C29A4B")
    CREME   = colors.HexColor("#FAF8F3")
    CINZA   = colors.HexColor("#6B7280")

    e_capa    = ParagraphStyle("capa",   fontSize=28, textColor=AZUL,   fontName="Helvetica-Bold", alignment=TA_CENTER, spaceAfter=8)
    e_subcapa = ParagraphStyle("scapa",  fontSize=11, textColor=CINZA,  fontName="Helvetica",      alignment=TA_CENTER, spaceAfter=4)
    e_h1      = ParagraphStyle("h1",     fontSize=16, textColor=AZUL,   fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=6)
    e_h2      = ParagraphStyle("h2",     fontSize=12, textColor=AZUL,   fontName="Helvetica-Bold", spaceBefore=8,  spaceAfter=4)
    e_corpo   = ParagraphStyle("corpo",  fontSize=9,  textColor=colors.HexColor("#2A2A2A"),
                               fontName="Helvetica", leading=14, spaceAfter=5)
    e_aviso   = ParagraphStyle("aviso",  fontSize=7,  textColor=CINZA,  fontName="Helvetica-Oblique", leading=11)

    el = []

    # ── CAPA ──
    el.append(Spacer(1, 3*cm))
    el.append(Paragraph("📊 Freenomics", e_subcapa))
    el.append(Spacer(1, 0.5*cm))
    el.append(Paragraph(T["pdf_titulo"], e_capa))
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="60%", thickness=3, color=DOURADO, hAlign="CENTER"))
    el.append(Spacer(1, 0.5*cm))
    el.append(Paragraph(f"{T['pdf_gerado']} · {datetime.today().strftime('%d/%m/%Y')}", e_subcapa))
    el.append(Paragraph(f"{T['pdf_periodo']}: {periodo_label} · Capital: €{investimento:,.0f}", e_subcapa))
    secs_incluidas = [v for k, v in [
        ("dashboard", T["sec_dashboard"]), ("comparador", T["sec_comparador"]),
        ("simulador", T["sec_simulador"]), ("risco", T["sec_risco"]),
        ("noticias", T["sec_noticias"]),
    ] if k in secoes]
    el.append(Paragraph(" · ".join(secs_incluidas), e_subcapa))
    el.append(PageBreak())

    import re
    def limpar_md(texto):
        return re.sub(r"\*\*(.*?)\*\*", r"\1", texto)

    def tabela_metricas(dados_metricas, labels):
        cab = ["Ativo"] + labels
        linhas = [cab]
        for t, m in dados_metricas.items():
            linhas.append([t, f"{m['retorno_total']}%", f"{m['volatilidade']}%",
                          f"{m['max_drawdown']}%", str(m['sharpe'])])
        tab = Table(linhas, colWidths=[3.5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 3*cm])
        tab.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),AZUL), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[CREME,colors.white]),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E5DFD0")),
            ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("LINEBELOW",(0,0),(-1,0),1.5,DOURADO),
        ]))
        return tab

    def add_secao_titulo(titulo):
        el.append(HRFlowable(width="100%", thickness=2, color=DOURADO))
        el.append(Spacer(1, 0.2*cm))
        el.append(Paragraph(titulo, e_h1))
        el.append(Spacer(1, 0.2*cm))

    def add_insight(texto):
        for paragrafo in limpar_md(texto).split("\n\n"):
            if paragrafo.strip():
                el.append(Paragraph(paragrafo.strip(), e_corpo))
        el.append(Spacer(1, 0.3*cm))

    # ── SECÇÃO DASHBOARD ──
    if "dashboard" in secoes:
        add_secao_titulo(T["sec_dashboard"])
        metricas = secoes["dashboard"]["metricas"]
        labels = ["Retorno", "Volatilidade", "Max Drawdown", "Sharpe"]
        el.append(tabela_metricas(metricas, labels))
        el.append(Spacer(1, 0.4*cm))
        el.append(Paragraph(secoes["dashboard"].get("titulo_insights", "Análise"), e_h2))
        add_insight(secoes["dashboard"]["insight"])
        if "dashboard" in secoes and len(secoes) > 1:
            el.append(PageBreak())

    # ── SECÇÃO COMPARADOR ──
    if "comparador" in secoes:
        add_secao_titulo(T["sec_comparador"])
        comp = secoes["comparador"]
        val_a = investimento * (1 + comp["ma"]["retorno"]/100)
        val_b = investimento * (1 + comp["mb"]["retorno"]/100)
        cab = ["", "Retorno", "Volatilidade", "Max Drawdown", "Sharpe", "Valor final"]
        linhas_c = [
            cab,
            [comp["nome_a"], f"{comp['ma']['retorno']}%", f"{comp['ma']['vol']}%",
             f"{comp['ma']['dd']}%", str(comp['ma']['sharpe']), f"€{val_a:,.0f}"],
            [comp["nome_b"], f"{comp['mb']['retorno']}%", f"{comp['mb']['vol']}%",
             f"{comp['mb']['dd']}%", str(comp['mb']['sharpe']), f"€{val_b:,.0f}"],
        ]
        tab_c = Table(linhas_c, colWidths=[3*cm, 2.5*cm, 2.5*cm, 2.5*cm, 2*cm, 2.5*cm])
        tab_c.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),AZUL), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"), ("VALIGN",(0,0),(-1,-1),"MIDDLE"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[CREME,colors.white]),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E5DFD0")),
            ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),6), ("RIGHTPADDING",(0,0),(-1,-1),6),
            ("LINEBELOW",(0,0),(-1,0),1.5,DOURADO),
        ]))
        el.append(tab_c)
        el.append(Spacer(1, 0.4*cm))
        add_insight(comp["insight"])
        if "simulador" in secoes or "risco" in secoes:
            el.append(PageBreak())

    # ── SECÇÃO SIMULADOR ──
    if "simulador" in secoes:
        add_secao_titulo(T["sec_simulador"])
        sim = secoes["simulador"]
        dados_sim = [
            ["Parâmetro", "Valor"],
            ["Investimento inicial", f"€{investimento:,.0f}"],
            ["Contribuição mensal", f"€{sim['contrib']:,.0f}"],
            ["Horizonte temporal", f"{sim['anos']} anos"],
            ["Retorno anual esperado", f"{sim['retorno']}%"],
            ["Inflação estimada", f"{sim['inflacao']}%"],
            ["", ""],
            ["Total investido", f"€{sim['total_inv']:,.0f}"],
            ["Valor final (nominal)", f"€{sim['valor_final']:,.0f}"],
            ["Valor final (real, adj. inflação)", f"€{sim['valor_real']:,.0f}"],
            ["Ganhos via juro composto", f"€{sim['ganho']:,.0f}"],
            ["Multiplicador", f"{sim['multiplicador']:.1f}x"],
        ]
        tab_s = Table(dados_sim, colWidths=[9*cm, 8*cm])
        tab_s.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),AZUL), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),9),
            ("ALIGN",(1,0),(1,-1),"CENTER"), ("ALIGN",(0,0),(0,-1),"LEFT"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[CREME,colors.white]),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E5DFD0")),
            ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("FONTNAME",(0,7),(-1,-1),"Helvetica-Bold"),
            ("LINEBELOW",(0,0),(-1,0),1.5,DOURADO),
            ("LINEABOVE",(0,7),(-1,7),1,DOURADO),
        ]))
        el.append(tab_s)
        el.append(Spacer(1, 0.4*cm))
        add_insight(sim["insight"])
        if "risco" in secoes:
            el.append(PageBreak())

    # ── SECÇÃO RISCO ──
    if "risco" in secoes:
        add_secao_titulo(T["sec_risco"])
        risco = secoes["risco"]
        el.append(Paragraph("Volatilidade e Value at Risk", e_h2))
        dados_r = [["Ativo", "Volatilidade Anual", "VaR 95%/dia", "Nível de risco"]]
        for t, m in risco["metricas"].items():
            nivel = "Alto" if m["vol"] > 40 else ("Médio" if m["vol"] > 20 else "Baixo")
            dados_r.append([t, f"{m['vol']:.1f}%", f"{m['var']:.2f}%", nivel])
        tab_r = Table(dados_r, colWidths=[4*cm, 4.5*cm, 4.5*cm, 4*cm])
        tab_r.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),AZUL), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[CREME,colors.white]),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E5DFD0")),
            ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("LINEBELOW",(0,0),(-1,0),1.5,DOURADO),
        ]))
        el.append(tab_r)
        el.append(Spacer(1, 0.3*cm))
        el.append(Paragraph("Cenários de Stress", e_h2))
        cenarios = {"Correção leve (-10%)": -0.10, "Correção moderada (-20%)": -0.20,
                    "Bear market (-35%)": -0.35, "Crash severo (-50%)": -0.50}
        dados_stress = [["Cenário", "Capital restante", "Perda estimada"]]
        for nome, pct in cenarios.items():
            dados_stress.append([nome, f"€{investimento*(1+pct):,.0f}", f"€{investimento*pct:,.0f}"])
        tab_stress = Table(dados_stress, colWidths=[6*cm, 5.5*cm, 5.5*cm])
        tab_stress.setStyle(TableStyle([
            ("BACKGROUND",(0,0),(-1,0),AZUL), ("TEXTCOLOR",(0,0),(-1,0),colors.white),
            ("FONTNAME",(0,0),(-1,0),"Helvetica-Bold"), ("FONTSIZE",(0,0),(-1,-1),9),
            ("ALIGN",(0,0),(-1,-1),"CENTER"),
            ("ROWBACKGROUNDS",(0,1),(-1,-1),[CREME,colors.white]),
            ("FONTNAME",(0,1),(-1,-1),"Helvetica"),
            ("GRID",(0,0),(-1,-1),0.5,colors.HexColor("#E5DFD0")),
            ("TOPPADDING",(0,0),(-1,-1),6), ("BOTTOMPADDING",(0,0),(-1,-1),6),
            ("LEFTPADDING",(0,0),(-1,-1),8), ("RIGHTPADDING",(0,0),(-1,-1),8),
            ("LINEBELOW",(0,0),(-1,0),1.5,DOURADO),
        ]))
        el.append(tab_stress)
        el.append(Spacer(1, 0.4*cm))
        add_insight(risco["insight"])
        if "noticias" in secoes:
            el.append(PageBreak())

    # ── SECÇÃO NOTÍCIAS ──
    if "noticias" in secoes:
        add_secao_titulo(T["sec_noticias"])
        e_noticia_titulo = ParagraphStyle("nt", fontSize=10, textColor=AZUL,
                                          fontName="Helvetica-Bold", spaceAfter=2, spaceBefore=8)
        e_noticia_meta   = ParagraphStyle("nm", fontSize=7, textColor=CINZA,
                                          fontName="Helvetica-Oblique", spaceAfter=2)
        e_noticia_resumo = ParagraphStyle("nr", fontSize=8, textColor=colors.HexColor("#2A2A2A"),
                                          fontName="Helvetica", leading=12, spaceAfter=4)
        for ticker, artigos in secoes["noticias"].items():
            el.append(Paragraph(f"● {ticker}", ParagraphStyle("tb", fontSize=11, textColor=DOURADO,
                                fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)))
            el.append(HRFlowable(width="100%", thickness=0.5, color=colors.HexColor("#E5DFD0")))
            for a in artigos:
                el.append(Paragraph(a["titulo"], e_noticia_titulo))
                meta = f"{a['fonte']}  ·  {a['data']}" if a["fonte"] or a["data"] else ""
                if meta:
                    el.append(Paragraph(meta, e_noticia_meta))
                if a["resumo"]:
                    el.append(Paragraph(a["resumo"] + "...", e_noticia_resumo))
            el.append(Spacer(1, 0.3*cm))

    # ── RODAPÉ ──
    el.append(Spacer(1, 0.5*cm))
    el.append(HRFlowable(width="100%", thickness=1, color=DOURADO))
    el.append(Spacer(1, 0.3*cm))
    el.append(Paragraph(T["rodape"], e_aviso))

    doc.build(el)
    buffer.seek(0)
    return buffer

# ── BOTÃO GERAR ──────────────────────────────────────────────
if st.button(T["btn_gerar"], use_container_width=True, type="primary"):
    if not any([inc_dashboard, inc_comparador, inc_simulador, inc_risco, inc_noticias]):
        st.error(T["seleciona_uma"])
        st.stop()

    secoes = {}
    lingua = LINGUA_NOME.get(lang, "português")

    with st.status(T["a_gerar"], expanded=True) as status:

        # ── DASHBOARD ──
        if inc_dashboard:
            st.write(T["a_carregar_dados"])
            dados = {}
            for t in tickers:
                df = carregar(t, dias)
                if not df.empty:
                    dados[t] = df
            if dados:
                metricas = {t: calc_metricas(df) for t, df in dados.items()}
                if api_key:
                    st.write(T["a_gerar_insights"])
                    linhas = [f"- {t}: retorno {m['retorno_total']}%, volatilidade {m['volatilidade']}%, drawdown {m['max_drawdown']}%, Sharpe {m['sharpe']}" for t, m in metricas.items()]
                    prompt = f"Analisa estes dados de investimento do período {periodo_label} e escreve 3 parágrafos em {lingua} de forma clara para um investidor individual. Dados:\n" + "\n".join(linhas) + "\nFoca em: melhor performance, risco em euros reais, e conclusão prática. Sem bullet points, sem títulos."
                    fallback_txt = ", ".join([t + ": " + str(m["retorno_total"]) + "%" for t, m in metricas.items()])
                    insight = chamar_api(prompt, api_key) or "Análise automática: " + fallback_txt
                else:
                    melhor = max(metricas.items(), key=lambda x: x[1]["retorno_total"])
                    insight = f"{melhor[0]} registou o melhor retorno do período com {melhor[1]['retorno_total']}%. O ativo com maior volatilidade foi {max(metricas.items(), key=lambda x: x[1]['volatilidade'])[0]}."
                secoes["dashboard"] = {"metricas": metricas, "insight": insight, "titulo_insights": "Análise"}

        # ── COMPARADOR ──
        if inc_comparador:
            ret_a, lista_a = retorno_carteira(tickers_a_str, dias)
            ret_b, lista_b = retorno_carteira(tickers_b_str, dias)
            if ret_a is not None and ret_b is not None:
                def ms(serie):
                    d = serie.pct_change().dropna()
                    return {"retorno": round(float((serie.iloc[-1]-1)*100),2), "vol": round(float(d.std()*np.sqrt(252)*100),2), "dd": round(float(((serie-serie.cummax())/serie.cummax()).min()*100),2), "sharpe": round(float((d.mean()/d.std())*np.sqrt(252)) if d.std().item()!=0 else 0,2)}
                ma_c, mb_c = ms(ret_a), ms(ret_b)
                nome_a_c, nome_b_c = " + ".join(lista_a), " + ".join(lista_b)
                if api_key:
                    st.write(T["a_gerar_insights"])
                    val_a = investimento*(1+ma_c["retorno"]/100); val_b = investimento*(1+mb_c["retorno"]/100)
                    prompt_c = f"Compara estas duas carteiras em {lingua} em 3 parágrafos curtos para um investidor individual. Período: {periodo_label}. Carteira A ({nome_a_c}): retorno {ma_c['retorno']}% (€{val_a:,.0f}), vol {ma_c['vol']}%, drawdown {ma_c['dd']}%, Sharpe {ma_c['sharpe']}. Carteira B ({nome_b_c}): retorno {mb_c['retorno']}% (€{val_b:,.0f}), vol {mb_c['vol']}%, drawdown {mb_c['dd']}%, Sharpe {mb_c['sharpe']}. Foca em retorno em euros, risco real, e qual foi mais eficiente. Sem bullet points."
                    insight_c = chamar_api(prompt_c, api_key) or f"Comparação: {nome_a_c} ({ma_c['retorno']}%) vs {nome_b_c} ({mb_c['retorno']}%)."
                else:
                    venc = nome_a_c if ma_c["retorno"] > mb_c["retorno"] else nome_b_c
                    insight_c = f"{venc} registou o melhor retorno do período. Em termos de risco ajustado, o Sharpe ratio indica {'A' if ma_c['sharpe'] > mb_c['sharpe'] else 'B'} como a escolha mais eficiente."
                secoes["comparador"] = {"ma": ma_c, "mb": mb_c, "nome_a": nome_a_c, "nome_b": nome_b_c, "insight": insight_c}

        # ── SIMULADOR ──
        if inc_simulador:
            meses = anos_sim * 12
            r_m = retorno_esp / 100 / 12
            r_real_m = ((1+retorno_esp/100)/(1+inflacao/100)-1)/12
            vn, vr, ti = [], [], []
            cn, cr, inv_acc = investimento, investimento, investimento
            for _ in range(meses):
                cn = cn*(1+r_m)+contrib; cr = cr*(1+r_real_m)+contrib; inv_acc += contrib
                vn.append(cn); vr.append(cr); ti.append(inv_acc)
            vf = vn[-1]; vreal = vr[-1]; tinv = ti[-1]; ganho = vf - tinv; mult = vf/tinv if tinv>0 else 1
            if api_key:
                st.write(T["a_gerar_insights"])
                prompt_s = f"Explica em {lingua} em 2 parágrafos o poder do juro composto com estes dados: €{contrib}/mês durante {anos_sim} anos a {retorno_esp}%/ano. Total investido: €{tinv:,.0f}. Valor final: €{vf:,.0f}. Ganhos: €{ganho:,.0f}. Multiplicador: {mult:.1f}x. Ajustado a {inflacao}% inflação: €{vreal:,.0f}. Tom motivador mas realista. Sem bullet points."
                insight_s = chamar_api(prompt_s, api_key) or f"Ao investires €{contrib}/mês durante {anos_sim} anos, transformas €{tinv:,.0f} investidos em €{vf:,.0f} — um multiplicador de {mult:.1f}x."
            else:
                insight_s = f"Ao investires €{contrib:,.0f}/mês durante {anos_sim} anos com um retorno de {retorno_esp}%/ano, transformas um total investido de €{tinv:,.0f} em €{vf:,.0f} — os juros compostos geram €{ganho:,.0f} adicionais ({ganho/tinv*100:.0f}% do valor final vem de rendimento)."
            secoes["simulador"] = {"contrib": contrib, "anos": anos_sim, "retorno": retorno_esp, "inflacao": inflacao, "total_inv": tinv, "valor_final": vf, "valor_real": vreal, "ganho": ganho, "multiplicador": mult, "insight": insight_s}

        # ── RISCO ──
        if inc_risco:
            dados_r = {}
            for t in tickers:
                df = carregar(t, dias)
                if not df.empty:
                    close = df["Close"]
                    if isinstance(close, pd.DataFrame):
                        close = close.iloc[:, 0]
                    dados_r[t] = close.squeeze()
            if len(dados_r) >= 1:
                precos_r = pd.DataFrame(dados_r).dropna()
                if not precos_r.empty:
                    ret_r = precos_r.pct_change().dropna()
                    metricas_r = {}
                    for t in dados_r:
                        if t in ret_r.columns:
                            vol = float(ret_r[t].std()*np.sqrt(252)*100)
                            var = float(np.percentile(ret_r[t], 5)*100)
                            metricas_r[t] = {"vol": round(vol,1), "var": round(var,2)}
                    if api_key and metricas_r:
                        st.write(T["a_gerar_insights"])
                        linhas_r = [f"- {t}: volatilidade {m['vol']}%, VaR 95% {m['var']}%/dia" for t, m in metricas_r.items()]
                        prompt_r = f"Analisa este perfil de risco em {lingua} em 2 parágrafos. Capital: €{investimento:,.0f}. {chr(10).join(linhas_r)}. Explica o que significa o VaR em euros e como os cenários de stress (crash de 10%, 20%, 35%, 50%) afetariam este capital. Tom direto e educativo. Sem bullet points."
                        insight_r = chamar_api(prompt_r, api_key) or f"Os ativos apresentam volatilidades distintas. Num cenário de crash de 35%, o capital de €{investimento:,.0f} poderia recuar para €{investimento*0.65:,.0f}."
                    elif metricas_r:
                        mais_vol = max(metricas_r.items(), key=lambda x: x[1]["vol"])
                        insight_r = f"{mais_vol[0]} é o ativo com maior volatilidade ({mais_vol[1]['vol']}%). Num cenário de crash severo (-50%), o capital de €{investimento:,.0f} reduziria para €{investimento*0.5:,.0f}."
                    else:
                        insight_r = ""
                    if metricas_r:
                        secoes["risco"] = {"metricas": metricas_r, "insight": insight_r}

        # ── NOTÍCIAS ──
        if inc_noticias:
            st.write(T["a_carregar_noticias"])
            noticias_por_ticker = {}
            for t in tickers:
                try:
                    raw = yf.Ticker(t).news
                    if raw:
                        artigos = []
                        for n in raw[:noticias_max_pdf]:
                            titulo = n.get("content", {}).get("title", "")
                            resumo = n.get("content", {}).get("summary", "")
                            fonte  = n.get("content", {}).get("provider", {}).get("displayName", "")
                            data   = n.get("content", {}).get("pubDate", "")
                            url    = n.get("content", {}).get("canonicalUrl", {}).get("url", "")
                            if titulo:
                                artigos.append({"titulo": titulo, "resumo": resumo[:200] if resumo else "", "fonte": fonte, "data": data[:10] if data else "", "url": url})
                        if artigos:
                            noticias_por_ticker[t] = artigos
                except Exception:
                    pass
            if noticias_por_ticker:
                secoes["noticias"] = noticias_por_ticker

        status.update(label=T["sucesso"], state="complete")

    pdf = gerar_pdf_completo(secoes)
    st.download_button(
        label=T["btn_gerar"],
        data=pdf,
        file_name=T["pdf_nome"],
        mime="application/pdf",
        use_container_width=True,
    )

st.markdown("---")
st.caption(T["rodape"])
