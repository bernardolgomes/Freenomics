"""
utils.py · Freenomics
Funções partilhadas entre todas as páginas.
"""
import streamlit as st
import os
import sys
import ast
import base64

def show_logo():
    """Mostra o logo + nome Freenomics no topo da página."""
    logo_path = os.path.join(os.path.dirname(__file__), "logo.png")
    if os.path.exists(logo_path):
        with open(logo_path, "rb") as f:
            logo_b64 = base64.b64encode(f.read()).decode()
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:12px;margin-bottom:8px;">
            <img src="data:image/png;base64,{logo_b64}"
                 style="width:42px;height:42px;border-radius:8px;"/>
            <span style="font-size:1.1rem;font-weight:700;
                         color:#4FB8C4;letter-spacing:0.5px;">Freenomics</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("### 📊 Freenomics")


# ── Reutilização de páginas dentro de separadores (st.tabs) ──────────────────

class PageStop(BaseException):
    """Substitui st.stop() dentro de run_page: termina só a página/separador
    actual, sem parar o resto do ecrã. (BaseException para não ser apanhada
    por 'except Exception' das páginas.)"""


def _page_stop():
    raise PageStop()


def _is_st_attr(func, attr):
    return (isinstance(func, ast.Attribute) and func.attr == attr
            and isinstance(func.value, ast.Name) and func.value.id == "st")


class _PageTransformer(ast.NodeTransformer):
    """Ajusta o código de uma página antiga para correr dentro de um separador:
    - st.stop()            -> __page_stop__()  (termina só este separador)
    - st.title(...)        -> removido (o título aparece uma vez na página nova)
    - show_logo()          -> removido (idem)
    - st.markdown(CSS...)  -> removido (a página nova injecta o CSS uma vez)
    - components.html(FIX_DROPDOWNS_JS, ...) -> removido (idem)
    Não toca em qualquer cálculo."""

    def visit_Call(self, node):
        self.generic_visit(node)
        f = node.func
        noop = ast.copy_location(ast.Constant(value=None), node)
        if _is_st_attr(f, "stop"):
            return ast.copy_location(
                ast.Call(func=ast.Name(id="__page_stop__", ctx=ast.Load()), args=[], keywords=[]), node)
        if _is_st_attr(f, "title"):
            return noop
        if isinstance(f, ast.Name) and f.id == "show_logo":
            return noop
        first = node.args[0] if node.args else None
        if _is_st_attr(f, "markdown") and isinstance(first, ast.Name) and first.id == "CSS":
            return noop
        if (isinstance(f, ast.Attribute) and f.attr == "html" and isinstance(f.value, ast.Name)
                and f.value.id == "components" and isinstance(first, ast.Name)
                and first.id == "FIX_DROPDOWNS_JS"):
            return noop
        return node


_PAGE_CODE_CACHE = {}


def _compile_page(path):
    mtime = os.path.getmtime(path)
    hit = _PAGE_CODE_CACHE.get(path)
    if hit and hit[0] == mtime:
        return hit[1]
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    tree = ast.parse(source, filename=path)
    tree = ast.fix_missing_locations(_PageTransformer().visit(tree))
    code = compile(tree, path, "exec")
    _PAGE_CODE_CACHE[path] = (mtime, code)
    return code


def run_page(path):
    """Executa o ficheiro de uma página antiga dentro do contexto actual
    (ex.: dentro de um 'with tab:'), com namespace próprio e __file__ correto.
    st.stop() nessa página só a termina a ela."""
    path = os.path.abspath(path)
    root = os.path.dirname(os.path.dirname(path))
    if root not in sys.path:
        sys.path.insert(0, root)
    stem = os.path.splitext(os.path.basename(path))[0]
    ns = {"__name__": "freenomics_page_" + stem, "__file__": path,
          "__page_stop__": _page_stop}
    try:
        exec(_compile_page(path), ns)
    except PageStop:
        pass


# ══════════════════════════════════════════════════════════════════════════════
# FIO CONDUTOR (Próximo passo) e MODO DEMONSTRAÇÃO
# ══════════════════════════════════════════════════════════════════════════════
import re as _re

_PT, _EN, _FR, _DE, _ES = "🇵🇹 Português", "🇬🇧 English", "🇫🇷 Français", "🇩🇪 Deutsch", "🇪🇸 Español"
_LANGS = [_PT, _EN, _FR, _DE, _ES]


def _tr(d):
    """Texto de um dict {língua: texto} na língua atual (PT por defeito)."""
    lang = st.session_state.get("lang", _PT)
    return d.get(lang) or d[_PT]


def _idx():
    lang = st.session_state.get("lang", _PT)
    return _LANGS.index(lang) if lang in _LANGS else 0


def kcontainer(key):
    """st.container com key (para CSS .st-key-<key>); recua para container normal em versões antigas."""
    try:
        return st.container(key=key)
    except TypeError:
        return st.container()


def capacidade_mensal():
    """Capacidade de investir por mês guardada pelo Orçamento (ou None)."""
    v = st.session_state.get("capacidade_mensal")
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


def patrimonio_total():
    """Património líquido guardado pela página Património (ou None)."""
    v = st.session_state.get("patrimonio_total")
    if v is None:
        v = (st.session_state.get("export_patrimonio") or {}).get("patrimonio")
    try:
        return float(v) if v is not None else None
    except (TypeError, ValueError):
        return None


_NEXT_T = {
    "kicker": {_PT: "Próximo passo", _EN: "Next step", _FR: "Étape suivante",
               _DE: "Nächster Schritt", _ES: "Siguiente paso"},
    "orcamento": {
        _PT: "Já sabes quanto podes investir por mês. Agora define para onde vai esse dinheiro.",
        _EN: "You know how much you can invest each month. Now decide where that money goes.",
        _FR: "Vous savez combien vous pouvez investir chaque mois. Décidez maintenant où va cet argent.",
        _DE: "Du weißt jetzt, wie viel du monatlich investieren kannst. Lege nun fest, wohin das Geld fließt.",
        _ES: "Ya sabes cuánto puedes invertir cada mes. Ahora define adónde va ese dinero.",
    },
    "objetivos": {
        _PT: "Tens um plano para cada objetivo. Regista agora o que já tens para veres o teu ponto de partida.",
        _EN: "You have a plan for each goal. Now record what you already own to see your starting point.",
        _FR: "Vous avez un plan pour chaque objectif. Enregistrez maintenant ce que vous possédez déjà pour voir votre point de départ.",
        _DE: "Du hast für jedes Ziel einen Plan. Erfasse jetzt, was du schon besitzt, um deinen Ausgangspunkt zu sehen.",
        _ES: "Tienes un plan para cada objetivo. Registra ahora lo que ya tienes para ver tu punto de partida.",
    },
    "patrimonio": {
        _PT: "Já conheces o teu ponto de partida. Agora é hora de investir: analisa uma ação ou acompanha a tua carteira.",
        _EN: "You know your starting point. Time to invest: analyse a stock or track your portfolio.",
        _FR: "Vous connaissez votre point de départ. Place à l'investissement : analysez une action ou suivez votre portefeuille.",
        _DE: "Du kennst deinen Ausgangspunkt. Jetzt wird investiert: Analysiere eine Aktie oder verfolge dein Portfolio.",
        _ES: "Ya conoces tu punto de partida. Es hora de invertir: analiza una acción o sigue tu cartera.",
    },
}
_NEXT_LINKS = {
    "orcamento": [("objetivos", {_PT: "🎯 Ir para Objetivos", _EN: "🎯 Go to Goals", _FR: "🎯 Aller aux Objectifs",
                                 _DE: "🎯 Zu den Zielen", _ES: "🎯 Ir a Objetivos"})],
    "objetivos": [("patrimonio", {_PT: "💎 Ir para Património", _EN: "💎 Go to Net Worth", _FR: "💎 Aller au Patrimoine",
                                  _DE: "💎 Zum Vermögen", _ES: "💎 Ir a Patrimonio"})],
    "patrimonio": [
        ("analise", {_PT: "🔎 Analisar uma ação", _EN: "🔎 Analyse a stock", _FR: "🔎 Analyser une action",
                     _DE: "🔎 Aktie analysieren", _ES: "🔎 Analizar una acción"}),
        ("carteira", {_PT: "📈 Ver a minha carteira", _EN: "📈 View my portfolio", _FR: "📈 Voir mon portefeuille",
                      _DE: "📈 Mein Portfolio ansehen", _ES: "📈 Ver mi cartera"}),
    ],
}


def next_step(passo):
    """Cartão 'Próximo passo' com st.page_link para a página seguinte da jornada.
    passo: 'orcamento' | 'objetivos' | 'patrimonio'. Se st.session_state['_paginas']
    não existir, mostra só o texto (sem botão)."""
    st.markdown(f"""
    <div class="fn-next-card">
        <p class="fn-kicker">{_tr(_NEXT_T["kicker"])}</p>
        <p class="fn-txt">{_tr(_NEXT_T[passo])}</p>
    </div>""", unsafe_allow_html=True)
    paginas = st.session_state.get("_paginas") or {}
    destinos = [(k, lbl) for k, lbl in _NEXT_LINKS[passo] if k in paginas]
    if not destinos:
        return
    with kcontainer("fn_next"):
        cols = st.columns(len(destinos))
        for col, (k, lbl) in zip(cols, destinos):
            with col:
                try:
                    st.page_link(paginas[k], label=_tr(lbl), use_container_width=True)
                except Exception:
                    pass


# ── Modo demonstração ─────────────────────────────────────────────────────────

_DEMO_T = {
    "load": {_PT: "🎬 Carregar dados de exemplo", _EN: "🎬 Load sample data", _FR: "🎬 Charger des données d'exemple",
             _DE: "🎬 Beispieldaten laden", _ES: "🎬 Cargar datos de ejemplo"},
    "clear": {_PT: "🧹 Limpar exemplo", _EN: "🧹 Clear sample data", _FR: "🧹 Effacer l'exemple",
              _DE: "🧹 Beispiel löschen", _ES: "🧹 Borrar ejemplo"},
    "ativo": {_PT: "🎬 Modo demonstração ativo · dados fictícios", _EN: "🎬 Demo mode on · fictional data",
              _FR: "🎬 Mode démo actif · données fictives", _DE: "🎬 Demo-Modus aktiv · fiktive Daten",
              _ES: "🎬 Modo demo activo · datos ficticios"},
    "dica": {_PT: "Vê tudo preenchido num clique, sem escreveres nada.",
             _EN: "See everything filled in with one click, no typing needed.",
             _FR: "Voyez tout rempli en un clic, sans rien saisir.",
             _DE: "Sieh alles mit einem Klick ausgefüllt, ganz ohne Tippen.",
             _ES: "Mira todo rellenado con un clic, sin escribir nada."},
}

# Nomes dos exemplos (ordem das línguas: PT, EN, FR, DE, ES)
_DEMO_OBJ = [
    ("Fundo de emergência", "Emergency fund", "Fonds d'urgence", "Notfallfonds", "Fondo de emergencia"),
    ("Entrada para casa", "House down payment", "Apport pour la maison", "Anzahlung fürs Haus", "Entrada de la casa"),
    ("Viagem ao Japão", "Trip to Japan", "Voyage au Japon", "Reise nach Japan", "Viaje a Japón"),
]
_DEMO_PAT = {
    "contas": [(("Conta à ordem", "Checking account", "Compte courant", "Girokonto", "Cuenta corriente"), 2400.0),
               (("Depósito a prazo", "Term deposit", "Dépôt à terme", "Festgeld", "Depósito a plazo"), 6000.0)],
    "investimentos": [(("ETF VWCE",) * 5, 9800.0), (("ETF IWDA",) * 5, 4200.0)],
    "reforma": [(("PPR", "Retirement plan", "Plan retraite", "Rentenplan", "Plan de jubilación"), 3500.0)],
    "imoveis": [(("Apartamento (quota-parte)", "Apartment (share)", "Appartement (quote-part)",
                  "Wohnung (Anteil)", "Piso (parte)"), 35000.0)],
    "outros": [(("Carro", "Car", "Voiture", "Auto", "Coche"), 6000.0)],
    "passivos": [(("Crédito habitação", "Mortgage", "Prêt immobilier", "Immobilienkredit", "Hipoteca"), 30000.0)],
}

# Chaves de session_state escritas pelo modo demonstração (para limpar)
_DEMO_EXACT = {
    "orcamento_resultado", "capacidade_mensal", "objetivos", "objetivos_resultado", "patrimonio_total",
    "pat_resultado", "ativos", "freenomics_resultado", "dash_periodo_dias",
    "risco_tickers", "risco_resultado", "risco_periodo_dias", "risco_capital",
    "div_tickers", "div_resultado", "div_anos",
    "comp_portfolios", "comp_resultado", "comp_periodo_dias",
    "sim_resultado", "aa_ticker", "aa_dados", "aa_proj", "aa_editor", "aa_calc", "aa_auto_load",
    "aa_preco", "aa_ret", "aa_mos", "aa_bench", "demo_ativo",
}
_DEMO_PREFIXES = (
    "orc_", "desp_", "obj_", "pat_", "tk_", "mo_", "pc_", "na_", "risco_t_", "div_t_", "sim_", "export_",
    "contas_", "investimentos_", "reforma_", "imoveis_", "outros_", "passivos_",
)
_DEMO_REGEX = _re.compile(r"^(p\d+_(t|m|pc|na|ra)\d+|add_ativ_\d+|del_port_\d+)$")


def clear_demo():
    """Remove do session_state tudo o que o modo demonstração (ou as páginas) guardaram."""
    ss = st.session_state
    for k in list(ss.keys()):
        if k in _DEMO_EXACT or k.startswith(_DEMO_PREFIXES) or _DEMO_REGEX.match(k):
            try:
                del ss[k]
            except Exception:
                pass


def load_demo():
    """Preenche todas as páginas com dados fictícios e ativa os resultados.
    Corre como callback (on_click), ou seja ANTES de os widgets serem criados no
    rerun seguinte, por isso pode escrever nas keys dos widgets."""
    from datetime import datetime
    clear_demo()
    ss = st.session_state
    i = _idx()

    # 1) Orçamento: salário 1800 €, despesas típicas -> sobram 500 €/mês
    desp = {"habitacao": 550.0, "alimentacao": 280.0, "transportes": 120.0,
            "subscricoes": 35.0, "lazer": 160.0, "saude": 45.0, "outros": 110.0}
    ss["orc_salario"] = 1800.0
    ss["orc_outras"] = 0.0
    for k, v in desp.items():
        ss[f"desp_{k}"] = v
    ss["orcamento_resultado"] = {"salario": 1800.0, "outras_receitas": 0.0, "despesas": dict(desp)}
    capacidade = 1800.0 - sum(desp.values())
    ss["capacidade_mensal"] = capacidade

    # 2) Objetivos (a soma das alocações = capacidade de investir)
    valores = [(6000.0, 2000.0, 150.0), (30000.0, 5000.0, 250.0), (3000.0, 600.0, 100.0)]
    objs = [{"nome": nomes[i], "valor_objetivo": vo, "valor_atual": va, "alocacao": al}
            for nomes, (vo, va, al) in zip(_DEMO_OBJ, valores)]
    ss["objetivos"] = [dict(o) for o in objs]
    for n, o in enumerate(objs):
        ss[f"obj_nome_{n}"] = o["nome"]
        ss[f"obj_valor_{n}"] = o["valor_objetivo"]
        ss[f"obj_atual_{n}"] = o["valor_atual"]
        ss[f"obj_aloc_{n}"] = o["alocacao"]
    ss["objetivos_resultado"] = {"objetivos": [dict(o) for o in objs]}

    # 3) Património (tudo em EUR para não depender da taxa de câmbio)
    totais, items = {}, {}
    for cat, lista in _DEMO_PAT.items():
        its = [{"nome": nomes[i], "valor": val, "moeda": "EUR"} for nomes, val in lista]
        ss[f"pat_{cat}"] = [dict(x) for x in its]
        for n, it in enumerate(its):
            ss[f"{cat}_nome_{n}"] = it["nome"]
            ss[f"{cat}_val_{n}"] = it["valor"]
            ss[f"{cat}_mo_{n}"] = "EUR"
        totais[cat] = sum(x["valor"] for x in its)
        items[cat] = its
    ss["pat_resultado"] = {"totais": totais, "data": datetime.today().strftime("%Y-%m-%d %H:%M"), "items": items}
    ss["patrimonio_total"] = sum(v for k, v in totais.items() if k != "passivos") - totais.get("passivos", 0.0)

    # 4) Carteira (Dashboard): VOO, MSFT, AAPL em USD, 1 ano
    ativos = [{"ticker": "VOO", "moeda": "USD", "preco": 430.0, "acoes": 6.0},
              {"ticker": "MSFT", "moeda": "USD", "preco": 380.0, "acoes": 5.0},
              {"ticker": "AAPL", "moeda": "USD", "preco": 175.0, "acoes": 8.0}]
    ss["ativos"] = [dict(a) for a in ativos]
    for n, a in enumerate(ativos):
        ss[f"tk_{n}"] = a["ticker"]
        ss[f"mo_{n}"] = a["moeda"]
        ss[f"pc_{n}"] = a["preco"]
        ss[f"na_{n}"] = a["acoes"]
    ss["dash_periodo_dias"] = 365
    ss["freenomics_resultado"] = {"ativos": [dict(a) for a in ativos], "dias": 365}

    # 5) Risco
    tk = ["VOO", "MSFT", "AAPL"]
    ss["risco_tickers"] = list(tk)
    for n, t in enumerate(tk):
        ss[f"risco_t_{n}"] = t
    ss["risco_periodo_dias"] = 365
    ss["risco_capital"] = 10000
    ss["risco_resultado"] = {"tickers": list(tk), "dias": 365, "capital": 10000}

    # 6) Dividendos
    dv = ["VOO", "MSFT", "KO"]
    ss["div_tickers"] = list(dv)
    for n, t in enumerate(dv):
        ss[f"div_t_{n}"] = t
    ss["div_anos"] = 5
    ss["div_resultado"] = {"tickers": list(dv), "anos": 5}

    # 7) Comparador: carteira A (só VOO) vs carteira B (MSFT + AAPL), 2 anos
    ports = [[{"ticker": "VOO", "moeda": "USD", "preco": 430.0, "acoes": 6.0}],
             [{"ticker": "MSFT", "moeda": "USD", "preco": 380.0, "acoes": 5.0},
              {"ticker": "AAPL", "moeda": "USD", "preco": 175.0, "acoes": 8.0}]]
    ss["comp_portfolios"] = [[dict(a) for a in p] for p in ports]
    for pi, p in enumerate(ports):
        for ai, a in enumerate(p):
            ss[f"p{pi}_t{ai}"] = a["ticker"]
            ss[f"p{pi}_m{ai}"] = a["moeda"]
            ss[f"p{pi}_pc{ai}"] = a["preco"]
            ss[f"p{pi}_na{ai}"] = a["acoes"]
    ss["comp_periodo_dias"] = 730
    ss["comp_resultado"] = {"portfolios": [[dict(a) for a in p] for p in ports], "dias": 730}

    # 8) Simulador: contribuição = capacidade de investir do Orçamento
    contrib = int(round(capacidade))
    ss["sim_inv_inicial"] = 2000
    ss["sim_contrib"] = contrib
    ss["sim_anos"] = 15
    ss["sim_retorno"] = 7.0
    ss["sim_inflacao"] = 2.5
    ss["sim_resultado"] = {"inv_inicial": 2000, "contrib": contrib, "anos": 15, "retorno": 7.0, "inflacao": 2.5}

    # 9) Análise de Ação: MSFT (a página carrega os dados e calcula sozinha)
    ss["aa_ticker"] = "MSFT"
    ss["aa_calc"] = True
    ss["aa_auto_load"] = True

    ss["demo_ativo"] = True


def demo_bar(where="page"):
    """Linha com 'Carregar dados de exemplo' e, se ativo, 'Limpar exemplo'.
    where: sufixo único para as keys dos botões (um por página)."""
    ativo = bool(st.session_state.get("demo_ativo"))
    c1, c2, c3 = st.columns([2.2, 1.6, 3.2]) if ativo else st.columns([2.2, 4.8])[:2] + [None]
    with c1:
        st.button(_tr(_DEMO_T["load"]), key=f"demo_load_{where}", on_click=load_demo,
                  use_container_width=True, help=_tr(_DEMO_T["dica"]))
    if ativo:
        with c2:
            st.button(_tr(_DEMO_T["clear"]), key=f"demo_clear_{where}", on_click=clear_demo,
                      use_container_width=True)
        with c3:
            st.markdown(f"<div style='padding-top:6px'><span class='fn-demo-badge'>{_tr(_DEMO_T['ativo'])}</span></div>",
                        unsafe_allow_html=True)
    else:
        with c2:
            st.caption(_tr(_DEMO_T["dica"]))


def page_chrome(titulo):
    """CSS, correção de dropdowns, logo e título: uma só vez, no topo da página."""
    import streamlit.components.v1 as components
    from translations import CSS, FIX_DROPDOWNS_JS
    st.markdown(CSS, unsafe_allow_html=True)
    components.html(FIX_DROPDOWNS_JS, height=0)
    show_logo()
    st.title(titulo)
