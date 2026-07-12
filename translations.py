"""
translations.py — Freenomics
Todas as traduções num só ficheiro. Importado por todas as páginas.
"""

LINGUAS = ["🇵🇹 Português", "🇬🇧 English", "🇫🇷 Français", "🇩🇪 Deutsch", "🇪🇸 Español"]

NOMES_PAGINAS = {
    "🇵🇹 Português": {
        "dashboard":  "🏠 Análise de Carteira",
        "comparador": "📊 Comparador",
        "simulador":  "💰 Simulador",
        "dividendos": "📅 Dividendos",
        "risco":      "⚠️ Risco",
        "noticias":   "📰 Notícias",
    },
    "🇬🇧 English": {
        "dashboard":  "🏠 Portfolio Analysis",
        "comparador": "📊 Comparator",
        "simulador":  "💰 Simulator",
        "dividendos": "📅 Dividends",
        "risco":      "⚠️ Risk",
        "noticias":   "📰 News",
    },
    "🇫🇷 Français": {
        "dashboard":  "🏠 Analyse de Portefeuille",
        "comparador": "📊 Comparateur",
        "simulador":  "💰 Simulateur",
        "dividendos": "📅 Dividendes",
        "risco":      "⚠️ Risque",
        "noticias":   "📰 Actualités",
    },
    "🇩🇪 Deutsch": {
        "dashboard":  "🏠 Portfolio-Analyse",
        "comparador": "📊 Vergleich",
        "simulador":  "💰 Simulator",
        "dividendos": "📅 Dividenden",
        "risco":      "⚠️ Risiko",
        "noticias":   "📰 Nachrichten",
    },
    "🇪🇸 Español": {
        "dashboard":  "🏠 Análisis de Cartera",
        "comparador": "📊 Comparador",
        "simulador":  "💰 Simulador",
        "dividendos": "📅 Dividendos",
        "risco":      "⚠️ Riesgo",
        "noticias":   "📰 Noticias",
    },
}

T_DASHBOARD = {
    "🇵🇹 Português": {
        "titulo": "Análise de Carteira",
        "subtitulo": "Relatório automático de performance, risco e contexto de mercado",
        "sidebar_carteira": "A tua carteira",
        "sidebar_tickers": "Tickers (separados por vírgula)",
        "sidebar_periodo": "Período de análise",
        "sidebar_investimento": "Investimento inicial por ativo (€)",
        "periodos": {"6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825},
        "a_carregar": "A carregar dados de mercado...",
        "erro_ticker": "Não foi possível carregar dados para",
        "erro_nenhum": "Nenhum ticker válido encontrado. Verifica os símbolos inseridos.",
        "metrica_retorno": "Retorno total",
        "metrica_vol": "Volatilidade anual.",
        "metrica_drawdown": "Max drawdown",
        "metrica_sharpe": "Sharpe (aprox.)",
        "grafico_titulo": "Evolução comparada (base 100)",
        "grafico_y": "Valor (base 100)", "grafico_x": "Data",
        "insights_titulo": "📝 Leitura automática dos resultados",
        "aviso": "⚠️ Esta análise é gerada automaticamente a partir de dados históricos e serve apenas para fins informativos/educativos — não constitui aconselhamento financeiro.",
        "rodape": "Relatório gerado por Freenomics · Dados via Yahoo Finance",
        "queda_maxima": "de queda máxima",
        "caption_base100": "💡 **Base 100:** todos os ativos começam no mesmo ponto para comparar performance relativa. Ex: um valor de 180 significa que o ativo subiu 80% desde o início do período.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** a linha tracejada representa o índice S&P 500 — o principal referencial do mercado americano. Serve para perceber se a tua carteira está a superar ou ficar abaixo do mercado.",
        "btn_pdf": "📄 Exportar relatório PDF",
        "pdf_titulo": "Relatório de Análise de Carteira",
        "pdf_gerado": "Gerado por Freenomics",
        "pdf_periodo": "Período", "pdf_metricas": "Métricas por ativo",
        "pdf_insights": "Análise automática",
        "pdf_aviso": "Este relatório é gerado automaticamente a partir de dados históricos — não constitui aconselhamento financeiro.",
        "pdf_nome": "relatorio_freenomics.pdf",
        "insight_melhor": lambda m, p, r: f"Nos últimos **{p.lower()}**, **{m}** teve a melhor performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"enquanto **{p}** registou a menor subida ({r}%).",
        "insight_pior_queda": lambda p, r: f"enquanto **{p}** registou uma queda ({r}%).",
        "insight_unico": lambda t, p, r: f"Nos últimos {p.lower()}, **{t}** registou um retorno de {r}%.",
        "insight_volatil": lambda t, v: f"Em termos de risco, **{t}** foi o ativo mais instável, com uma volatilidade anualizada de {v}% — isto significa oscilações de preço mais acentuadas ao longo do tempo.",
        "insight_drawdown": lambda t, d: f"**{t}** sofreu uma queda máxima (drawdown) de {d}% face ao seu pico no período — um valor considerável que vale a pena teres em conta na tua tolerância ao risco.",
        "insight_sharpe": lambda t: f"Ajustando ao risco (Sharpe ratio), **{t}** foi quem ofereceu o melhor equilíbrio entre retorno e volatilidade neste período.",
    },
    "🇬🇧 English": {
        "titulo": "Portfolio Analysis",
        "subtitulo": "Automated report on performance, risk and market context",
        "sidebar_carteira": "Your portfolio",
        "sidebar_tickers": "Tickers (comma-separated)",
        "sidebar_periodo": "Analysis period",
        "sidebar_investimento": "Initial investment per asset (€)",
        "periodos": {"6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825},
        "a_carregar": "Loading market data...",
        "erro_ticker": "Could not load data for",
        "erro_nenhum": "No valid tickers found. Please check the symbols entered.",
        "metrica_retorno": "Total return",
        "metrica_vol": "Ann. volatility",
        "metrica_drawdown": "Max drawdown",
        "metrica_sharpe": "Sharpe (approx.)",
        "grafico_titulo": "Comparative evolution (base 100)",
        "grafico_y": "Value (base 100)", "grafico_x": "Date",
        "insights_titulo": "📝 Automatic reading of results",
        "aviso": "⚠️ This analysis is generated automatically from historical data and is for informational/educational purposes only — it does not constitute financial advice.",
        "rodape": "Report generated by Freenomics · Data via Yahoo Finance",
        "queda_maxima": "max drawdown reached",
        "caption_base100": "💡 **Base 100:** all assets start at the same point to compare relative performance. E.g. a value of 180 means the asset rose 80% since the start of the period.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** the dashed line represents the S&P 500 index — the main US market reference. It shows whether your portfolio is outperforming or underperforming the market.",
        "btn_pdf": "📄 Export PDF report",
        "pdf_titulo": "Portfolio Analysis Report",
        "pdf_gerado": "Generated by Freenomics",
        "pdf_periodo": "Period", "pdf_metricas": "Metrics per asset",
        "pdf_insights": "Automatic analysis",
        "pdf_aviso": "This report is generated automatically from historical data — it does not constitute financial advice.",
        "pdf_nome": "freenomics_report.pdf",
        "insight_melhor": lambda m, p, r: f"Over the last **{p.lower()}**, **{m}** had the best performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"while **{p}** recorded the smallest gain ({r}%).",
        "insight_pior_queda": lambda p, r: f"while **{p}** recorded a decline ({r}%).",
        "insight_unico": lambda t, p, r: f"Over the last {p.lower()}, **{t}** recorded a return of {r}%.",
        "insight_volatil": lambda t, v: f"In terms of risk, **{t}** was the most volatile asset, with an annualised volatility of {v}% — meaning more pronounced price swings over time.",
        "insight_drawdown": lambda t, d: f"**{t}** suffered a maximum drawdown of {d}% from its peak — a significant figure worth considering for your risk tolerance.",
        "insight_sharpe": lambda t: f"Risk-adjusted (Sharpe ratio), **{t}** offered the best balance between return and volatility during this period.",
    },
    "🇫🇷 Français": {
        "titulo": "Analyse de Portefeuille",
        "subtitulo": "Rapport automatique sur la performance, le risque et le contexte de marché",
        "sidebar_carteira": "Votre portefeuille",
        "sidebar_tickers": "Tickers (séparés par virgule)",
        "sidebar_periodo": "Période d'analyse",
        "sidebar_investimento": "Investissement initial par actif (€)",
        "periodos": {"6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825},
        "a_carregar": "Chargement des données de marché...",
        "erro_ticker": "Impossible de charger les données pour",
        "erro_nenhum": "Aucun ticker valide trouvé. Vérifiez les symboles saisis.",
        "metrica_retorno": "Rendement total",
        "metrica_vol": "Volatilité ann.",
        "metrica_drawdown": "Drawdown max",
        "metrica_sharpe": "Sharpe (approx.)",
        "grafico_titulo": "Évolution comparée (base 100)",
        "grafico_y": "Valeur (base 100)", "grafico_x": "Date",
        "insights_titulo": "📝 Lecture automatique des résultats",
        "aviso": "⚠️ Cette analyse est générée automatiquement à partir de données historiques — elle ne constitue pas un conseil financier.",
        "rodape": "Rapport généré par Freenomics · Données via Yahoo Finance",
        "queda_maxima": "de baisse maximale",
        "caption_base100": "💡 **Base 100 :** tous les actifs partent du même point pour comparer la performance relative. Ex : une valeur de 180 signifie que l'actif a progressé de 80% depuis le début de la période.",
        "caption_benchmark": "📊 **S&P 500 (benchmark) :** la ligne en pointillés représente l'indice S&P 500 — la principale référence du marché américain. Elle indique si votre portefeuille surperforme ou sous-performe le marché.",
        "btn_pdf": "📄 Exporter le rapport PDF",
        "pdf_titulo": "Rapport d'Analyse de Portefeuille",
        "pdf_gerado": "Généré par Freenomics",
        "pdf_periodo": "Période", "pdf_metricas": "Métriques par actif",
        "pdf_insights": "Analyse automatique",
        "pdf_aviso": "Ce rapport est généré automatiquement à partir de données historiques — il ne constitue pas un conseil financier.",
        "pdf_nome": "rapport_freenomics.pdf",
        "insight_melhor": lambda m, p, r: f"Au cours des **{p.lower()}** derniers, **{m}** a affiché la meilleure performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"tandis que **{p}** a enregistré la plus faible hausse ({r}%).",
        "insight_pior_queda": lambda p, r: f"tandis que **{p}** a enregistré une baisse ({r}%).",
        "insight_unico": lambda t, p, r: f"Au cours des {p.lower()} derniers, **{t}** a enregistré un rendement de {r}%.",
        "insight_volatil": lambda t, v: f"En termes de risque, **{t}** a été l'actif le plus instable, avec une volatilité annualisée de {v}%.",
        "insight_drawdown": lambda t, d: f"**{t}** a subi une baisse maximale de {d}% par rapport à son pic — à prendre en compte dans votre tolérance au risque.",
        "insight_sharpe": lambda t: f"Ajusté au risque (Sharpe), **{t}** a offert le meilleur équilibre entre rendement et volatilité.",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Portfolio-Analyse",
        "subtitulo": "Automatischer Bericht über Performance, Risiko und Marktkontext",
        "sidebar_carteira": "Ihr Portfolio",
        "sidebar_tickers": "Ticker (kommagetrennt)",
        "sidebar_periodo": "Analysezeitraum",
        "sidebar_investimento": "Anfangsinvestition pro Anlage (€)",
        "periodos": {"6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
        "a_carregar": "Marktdaten werden geladen...",
        "erro_ticker": "Daten konnten nicht geladen werden für",
        "erro_nenhum": "Keine gültigen Ticker gefunden. Bitte überprüfen Sie die Symbole.",
        "metrica_retorno": "Gesamtrendite",
        "metrica_vol": "Jährl. Volatilität",
        "metrica_drawdown": "Max. Drawdown",
        "metrica_sharpe": "Sharpe (ca.)",
        "grafico_titulo": "Vergleichende Entwicklung (Basis 100)",
        "grafico_y": "Wert (Basis 100)", "grafico_x": "Datum",
        "insights_titulo": "📝 Automatische Auswertung",
        "aviso": "⚠️ Diese Analyse wird automatisch aus historischen Daten generiert — sie stellt keine Finanzberatung dar.",
        "rodape": "Bericht erstellt von Freenomics · Daten via Yahoo Finance",
        "queda_maxima": "maximaler Rückgang",
        "caption_base100": "💡 **Basis 100:** Alle Anlagen starten am selben Punkt, um die relative Performance zu vergleichen. Bsp.: Ein Wert von 180 bedeutet, dass die Anlage seit Beginn des Zeitraums um 80% gestiegen ist.",
        "caption_benchmark": "📊 **S&P 500 (Benchmark):** Die gestrichelte Linie zeigt den S&P 500 Index — den wichtigsten US-Marktindex. Sie zeigt, ob Ihr Portfolio den Markt übertrifft oder hinter ihm zurückbleibt.",
        "btn_pdf": "📄 PDF-Bericht exportieren",
        "pdf_titulo": "Portfolio-Analysebericht",
        "pdf_gerado": "Erstellt von Freenomics",
        "pdf_periodo": "Zeitraum", "pdf_metricas": "Kennzahlen pro Anlage",
        "pdf_insights": "Automatische Analyse",
        "pdf_aviso": "Dieser Bericht wird automatisch generiert — er stellt keine Finanzberatung dar.",
        "pdf_nome": "freenomics_bericht.pdf",
        "insight_melhor": lambda m, p, r: f"In den letzten **{p.lower()}** hatte **{m}** die beste Performance ({r}%).",
        "insight_pior_subida": lambda p, r: f"während **{p}** den geringsten Anstieg verzeichnete ({r}%).",
        "insight_pior_queda": lambda p, r: f"während **{p}** einen Rückgang verzeichnete ({r}%).",
        "insight_unico": lambda t, p, r: f"In den letzten {p.lower()} verzeichnete **{t}** eine Rendite von {r}%.",
        "insight_volatil": lambda t, v: f"**{t}** war der volatilste Vermögenswert mit einer Volatilität von {v}% p.a.",
        "insight_drawdown": lambda t, d: f"**{t}** erlitt einen maximalen Drawdown von {d}% — bei der Risikotoleranz zu berücksichtigen.",
        "insight_sharpe": lambda t: f"Risikoadjustiert (Sharpe) bot **{t}** das beste Gleichgewicht zwischen Rendite und Volatilität.",
    },
    "🇪🇸 Español": {
        "titulo": "Análisis de Cartera",
        "subtitulo": "Informe automático de rendimiento, riesgo y contexto de mercado",
        "sidebar_carteira": "Tu cartera",
        "sidebar_tickers": "Tickers (separados por coma)",
        "sidebar_periodo": "Período de análisis",
        "sidebar_investimento": "Inversión inicial por activo (€)",
        "periodos": {"6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825},
        "a_carregar": "Cargando datos de mercado...",
        "erro_ticker": "No se pudieron cargar los datos de",
        "erro_nenhum": "No se encontraron tickers válidos. Verifica los símbolos introducidos.",
        "metrica_retorno": "Rendimiento total",
        "metrica_vol": "Volatilidad anual.",
        "metrica_drawdown": "Max drawdown",
        "metrica_sharpe": "Sharpe (aprox.)",
        "grafico_titulo": "Evolución comparada (base 100)",
        "grafico_y": "Valor (base 100)", "grafico_x": "Fecha",
        "insights_titulo": "📝 Lectura automática de resultados",
        "aviso": "⚠️ Este análisis se genera automáticamente a partir de datos históricos — no constituye asesoramiento financiero.",
        "rodape": "Informe generado por Freenomics · Datos via Yahoo Finance",
        "queda_maxima": "de caída máxima",
        "caption_base100": "💡 **Base 100:** todos los activos parten del mismo punto para comparar el rendimiento relativo. Ej: un valor de 180 significa que el activo subió un 80% desde el inicio del período.",
        "caption_benchmark": "📊 **S&P 500 (benchmark):** la línea discontinua representa el índice S&P 500 — la principal referencia del mercado americano. Sirve para ver si tu cartera está superando o quedándose por debajo del mercado.",
        "btn_pdf": "📄 Exportar informe PDF",
        "pdf_titulo": "Informe de Análisis de Cartera",
        "pdf_gerado": "Generado por Freenomics",
        "pdf_periodo": "Período", "pdf_metricas": "Métricas por activo",
        "pdf_insights": "Análisis automático",
        "pdf_aviso": "Este informe se genera automáticamente a partir de datos históricos — no constituye asesoramiento financiero.",
        "pdf_nome": "informe_freenomics.pdf",
        "insight_melhor": lambda m, p, r: f"En los últimos **{p.lower()}**, **{m}** tuvo el mejor rendimiento ({r}%).",
        "insight_pior_subida": lambda p, r: f"mientras **{p}** registró la menor subida ({r}%).",
        "insight_pior_queda": lambda p, r: f"mientras **{p}** registró una caída ({r}%).",
        "insight_unico": lambda t, p, r: f"En los últimos {p.lower()}, **{t}** registró un rendimiento de {r}%.",
        "insight_volatil": lambda t, v: f"En términos de riesgo, **{t}** fue el activo más volátil, con una volatilidad anualizada de {v}%.",
        "insight_drawdown": lambda t, d: f"**{t}** sufrió una caída máxima (drawdown) de {d}% desde su pico — a tener en cuenta en tu tolerancia al riesgo.",
        "insight_sharpe": lambda t: f"Ajustado al riesgo (Sharpe), **{t}** ofreció el mejor equilibrio entre rendimiento y volatilidad.",
    },
}

T_COMPARADOR = {
    "🇵🇹 Português": {
        "titulo": "Comparador de Carteiras",
        "subtitulo": "Compara duas estratégias de investimento lado a lado.",
        "sidebar_a": "Carteira A", "sidebar_b": "Carteira B",
        "tickers_a": "Tickers Carteira A", "tickers_b": "Tickers Carteira B",
        "periodo": "Período de análise", "investimento": "Investimento inicial (€)",
        "a_carregar": "A carregar dados...",
        "vencedor": "🏆 Melhor performance no período",
        "carteira_a": "Carteira A", "carteira_b": "Carteira B",
        "retorno": "Retorno total", "vol": "Volatilidade anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final (€)",
        "grafico": "Evolução comparada (base 100)",
        "grafico_y": "Valor (base 100)", "grafico_x": "Data",
        "rodape": "Freenomics · Dados via Yahoo Finance · Não constitui aconselhamento financeiro.",
        "queda_maxima": "de queda máxima",
        "de_ganho": "de ganho",
        "caption_base100": "💡 **Base 100:** todos os ativos começam no mesmo ponto para comparar performance relativa. Ex: um valor de 180 significa que o ativo subiu 80% desde o início do período.",
        "periodos": {"6 meses": 180, "1 ano": 365, "2 anos": 730, "5 anos": 1825},
    },
    "🇬🇧 English": {
        "titulo": "Portfolio Comparator",
        "subtitulo": "Compare two investment strategies side by side.",
        "sidebar_a": "Portfolio A", "sidebar_b": "Portfolio B",
        "tickers_a": "Portfolio A Tickers", "tickers_b": "Portfolio B Tickers",
        "periodo": "Analysis period", "investimento": "Initial investment (€)",
        "a_carregar": "Loading data...",
        "vencedor": "🏆 Best performance in the period",
        "carteira_a": "Portfolio A", "carteira_b": "Portfolio B",
        "retorno": "Total return", "vol": "Ann. volatility",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (approx.)",
        "valor_final": "Final value (€)",
        "grafico": "Comparative evolution (base 100)",
        "grafico_y": "Value (base 100)", "grafico_x": "Date",
        "rodape": "Freenomics · Data via Yahoo Finance · Does not constitute financial advice.",
        "queda_maxima": "max drawdown reached",
        "de_ganho": "gain",
        "caption_base100": "💡 **Base 100:** all assets start at the same point to compare relative performance. E.g. a value of 180 means the asset rose 80% since the start of the period.",
        "periodos": {"6 months": 180, "1 year": 365, "2 years": 730, "5 years": 1825},
    },
    "🇫🇷 Français": {
        "titulo": "Comparateur de Portefeuilles",
        "subtitulo": "Comparez deux stratégies d'investissement côte à côte.",
        "sidebar_a": "Portefeuille A", "sidebar_b": "Portefeuille B",
        "tickers_a": "Tickers Portefeuille A", "tickers_b": "Tickers Portefeuille B",
        "periodo": "Période d'analyse", "investimento": "Investissement initial (€)",
        "a_carregar": "Chargement des données...",
        "vencedor": "🏆 Meilleure performance sur la période",
        "carteira_a": "Portefeuille A", "carteira_b": "Portefeuille B",
        "retorno": "Rendement total", "vol": "Volatilité ann.",
        "drawdown": "Drawdown max", "sharpe": "Sharpe (approx.)",
        "valor_final": "Valeur finale (€)",
        "grafico": "Évolution comparée (base 100)",
        "grafico_y": "Valeur (base 100)", "grafico_x": "Date",
        "rodape": "Freenomics · Données via Yahoo Finance · Ne constitue pas un conseil financier.",
        "queda_maxima": "de baisse maximale",
        "de_ganho": "de gain",
        "caption_base100": "💡 **Base 100 :** tous les actifs partent du même point pour comparer la performance relative. Ex : une valeur de 180 signifie que l'actif a progressé de 80% depuis le début de la période.",
        "periodos": {"6 mois": 180, "1 an": 365, "2 ans": 730, "5 ans": 1825},
    },
    "🇩🇪 Deutsch": {
        "titulo": "Portfolio-Vergleich",
        "subtitulo": "Vergleichen Sie zwei Anlagestrategien nebeneinander.",
        "sidebar_a": "Portfolio A", "sidebar_b": "Portfolio B",
        "tickers_a": "Ticker Portfolio A", "tickers_b": "Ticker Portfolio B",
        "periodo": "Analysezeitraum", "investimento": "Anfangsinvestition (€)",
        "a_carregar": "Daten werden geladen...",
        "vencedor": "🏆 Beste Performance im Zeitraum",
        "carteira_a": "Portfolio A", "carteira_b": "Portfolio B",
        "retorno": "Gesamtrendite", "vol": "Jährl. Volatilität",
        "drawdown": "Max. Drawdown", "sharpe": "Sharpe (ca.)",
        "valor_final": "Endwert (€)",
        "grafico": "Vergleichende Entwicklung (Basis 100)",
        "grafico_y": "Wert (Basis 100)", "grafico_x": "Datum",
        "rodape": "Freenomics · Daten via Yahoo Finance · Stellt keine Finanzberatung dar.",
        "queda_maxima": "maximaler Rückgang",
        "de_ganho": "Gewinn",
        "caption_base100": "💡 **Basis 100:** Alle Anlagen starten am selben Punkt, um die relative Performance zu vergleichen. Bsp.: Ein Wert von 180 bedeutet, dass die Anlage um 80% gestiegen ist.",
        "periodos": {"6 Monate": 180, "1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
    },
    "🇪🇸 Español": {
        "titulo": "Comparador de Carteras",
        "subtitulo": "Compara dos estrategias de inversión lado a lado.",
        "sidebar_a": "Cartera A", "sidebar_b": "Cartera B",
        "tickers_a": "Tickers Cartera A", "tickers_b": "Tickers Cartera B",
        "periodo": "Período de análisis", "investimento": "Inversión inicial (€)",
        "a_carregar": "Cargando datos...",
        "vencedor": "🏆 Mejor rendimiento en el período",
        "carteira_a": "Cartera A", "carteira_b": "Cartera B",
        "retorno": "Rendimiento total", "vol": "Volatilidad anual.",
        "drawdown": "Max drawdown", "sharpe": "Sharpe (aprox.)",
        "valor_final": "Valor final (€)",
        "grafico": "Evolución comparada (base 100)",
        "grafico_y": "Valor (base 100)", "grafico_x": "Fecha",
        "rodape": "Freenomics · Datos via Yahoo Finance · No constituye asesoramiento financiero.",
        "queda_maxima": "de caída máxima",
        "de_ganho": "de ganancia",
        "caption_base100": "💡 **Base 100:** todos los activos parten del mismo punto para comparar el rendimiento relativo. Ej: un valor de 180 significa que el activo subió un 80% desde el inicio del período.",
        "periodos": {"6 meses": 180, "1 año": 365, "2 años": 730, "5 años": 1825},
    },
}

T_SIMULADOR = {
    "🇵🇹 Português": {
        "titulo": "Simulador de Investimento Regular",
        "subtitulo": "Descobre quanto acumulas ao investir uma quantia fixa todos os meses.",
        "sidebar": "Parâmetros",
        "inv_inicial": "Investimento inicial (€)",
        "contrib": "Contribuição mensal (€)",
        "anos": "Horizonte temporal (anos)",
        "retorno": "Retorno anual esperado (%)",
        "inflacao": "Inflação estimada (%)",
        "dica": "💡 O SP500 teve um retorno histórico médio de ~10% ao ano. Ajustando à inflação (~7% real).",
        "grafico": "Evolução do capital ao longo do tempo",
        "grafico_y": "Valor (€)", "grafico_x": "Anos",
        "capital_nominal": "Capital acumulado (nominal)",
        "total_investido": "Total investido",
        "capital_real": "Capital real (adj. inflação)",
        "marcos": "Marcos ao longo do tempo",
        "anos_label": "anos", "investido_label": "investido",
        "valor_final": "Valor final (nominal)", "valor_real": "Valor final (real)",
        "adj_inflacao": "ajustado à inflação",
        "total_inv": "Total investido", "multiplicador": "Multiplicador",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Ao investires **€{cm:.0f}/mês** durante **{anos} anos** com um retorno de **{r}%/ano**, transformas um total investido de **€{ti:,.0f}** em **€{vf:,.0f}** — os juros compostos geram **€{g:,.0f}** adicionais. Ajustando à inflação de {inf}%, o poder de compra real seria de **€{vr:,.0f}**.",
        "aviso": "⚠️ Simulação baseada em retorno constante. Retornos reais variam — não constitui aconselhamento financeiro.",
        "rodape": "Freenomics · Calculadora de juro composto",
    },
    "🇬🇧 English": {
        "titulo": "Regular Investment Simulator",
        "subtitulo": "Find out how much you accumulate by investing a fixed amount every month.",
        "sidebar": "Parameters",
        "inv_inicial": "Initial investment (€)",
        "contrib": "Monthly contribution (€)",
        "anos": "Time horizon (years)",
        "retorno": "Expected annual return (%)",
        "inflacao": "Estimated inflation (%)",
        "dica": "💡 The S&P500 had a historical average return of ~10%/year. Inflation-adjusted (~7% real).",
        "grafico": "Capital growth over time",
        "grafico_y": "Value (€)", "grafico_x": "Years",
        "capital_nominal": "Accumulated capital (nominal)",
        "total_investido": "Total invested",
        "capital_real": "Real capital (inflation-adj.)",
        "marcos": "Milestones over time",
        "anos_label": "years", "investido_label": "invested",
        "valor_final": "Final value (nominal)", "valor_real": "Final value (real)",
        "adj_inflacao": "inflation-adjusted",
        "total_inv": "Total invested", "multiplicador": "Multiplier",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"By investing **€{cm:.0f}/month** for **{anos} years** at **{r}%/year**, you turn a total investment of **€{ti:,.0f}** into **€{vf:,.0f}** — compound interest generates an extra **€{g:,.0f}**. Adjusted for {inf}% inflation, real purchasing power would be **€{vr:,.0f}**.",
        "aviso": "⚠️ Simulation based on constant return. Real returns vary — does not constitute financial advice.",
        "rodape": "Freenomics · Compound interest calculator",
    },
    "🇫🇷 Français": {
        "titulo": "Simulateur d'Investissement Régulier",
        "subtitulo": "Découvrez combien vous accumulez en investissant chaque mois.",
        "sidebar": "Paramètres",
        "inv_inicial": "Investissement initial (€)",
        "contrib": "Contribution mensuelle (€)",
        "anos": "Horizon temporel (années)",
        "retorno": "Rendement annuel attendu (%)",
        "inflacao": "Inflation estimée (%)",
        "dica": "💡 Le S&P500 a eu un rendement moyen historique de ~10%/an. Ajusté à l'inflation (~7% réel).",
        "grafico": "Évolution du capital dans le temps",
        "grafico_y": "Valeur (€)", "grafico_x": "Années",
        "capital_nominal": "Capital accumulé (nominal)",
        "total_investido": "Total investi",
        "capital_real": "Capital réel (adj. inflation)",
        "marcos": "Jalons dans le temps",
        "anos_label": "ans", "investido_label": "investi",
        "valor_final": "Valeur finale (nominale)", "valor_real": "Valeur finale (réelle)",
        "adj_inflacao": "ajusté à l'inflation",
        "total_inv": "Total investi", "multiplicador": "Multiplicateur",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"En investissant **€{cm:.0f}/mois** pendant **{anos} ans** à **{r}%/an**, vous transformez **€{ti:,.0f}** investis en **€{vf:,.0f}** — les intérêts composés génèrent **€{g:,.0f}** supplémentaires. Ajusté à {inf}% d'inflation, la valeur réelle serait de **€{vr:,.0f}**.",
        "aviso": "⚠️ Simulation basée sur un rendement constant — ne constitue pas un conseil financier.",
        "rodape": "Freenomics · Calculateur d'intérêts composés",
    },
    "🇩🇪 Deutsch": {
        "titulo": "Regelmäßiger Investitionssimulator",
        "subtitulo": "Berechnen Sie, wie viel Sie durch monatliche Einzahlungen ansparen.",
        "sidebar": "Parameter",
        "inv_inicial": "Anfangsinvestition (€)",
        "contrib": "Monatlicher Beitrag (€)",
        "anos": "Anlagehorizont (Jahre)",
        "retorno": "Erwartete Jahresrendite (%)",
        "inflacao": "Geschätzte Inflation (%)",
        "dica": "💡 Der S&P500 erzielte historisch ~10%/Jahr. Inflationsbereinigt ~7% real.",
        "grafico": "Kapitalentwicklung über die Zeit",
        "grafico_y": "Wert (€)", "grafico_x": "Jahre",
        "capital_nominal": "Angespartes Kapital (nominal)",
        "total_investido": "Gesamt investiert",
        "capital_real": "Reales Kapital (inflationsbereinigt)",
        "marcos": "Meilensteine",
        "anos_label": "Jahre", "investido_label": "investiert",
        "valor_final": "Endwert (nominal)", "valor_real": "Endwert (real)",
        "adj_inflacao": "inflationsbereinigt",
        "total_inv": "Gesamt investiert", "multiplicador": "Multiplikator",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Durch monatliche Einzahlungen von **€{cm:.0f}** über **{anos} Jahre** bei **{r}%/Jahr** werden aus **€{ti:,.0f}** investiertem Kapital **€{vf:,.0f}** — der Zinseszins generiert zusätzliche **€{g:,.0f}**. Bei {inf}% Inflation beträgt die reale Kaufkraft **€{vr:,.0f}**.",
        "aviso": "⚠️ Simulation auf Basis konstanter Rendite — stellt keine Finanzberatung dar.",
        "rodape": "Freenomics · Zinseszinsrechner",
    },
    "🇪🇸 Español": {
        "titulo": "Simulador de Inversión Regular",
        "subtitulo": "Descubre cuánto acumulas invirtiendo una cantidad fija cada mes.",
        "sidebar": "Parámetros",
        "inv_inicial": "Inversión inicial (€)",
        "contrib": "Contribución mensual (€)",
        "anos": "Horizonte temporal (años)",
        "retorno": "Rentabilidad anual esperada (%)",
        "inflacao": "Inflación estimada (%)",
        "dica": "💡 El S&P500 tuvo una rentabilidad histórica media de ~10%/año. Ajustada a inflación (~7% real).",
        "grafico": "Evolución del capital a lo largo del tiempo",
        "grafico_y": "Valor (€)", "grafico_x": "Años",
        "capital_nominal": "Capital acumulado (nominal)",
        "total_investido": "Total invertido",
        "capital_real": "Capital real (adj. inflación)",
        "marcos": "Hitos a lo largo del tiempo",
        "anos_label": "años", "investido_label": "invertido",
        "valor_final": "Valor final (nominal)", "valor_real": "Valor final (real)",
        "adj_inflacao": "ajustado a inflación",
        "total_inv": "Total invertido", "multiplicador": "Multiplicador",
        "insight": lambda cm, anos, r, ti, vf, g, inf, vr: f"Al invertir **€{cm:.0f}/mes** durante **{anos} años** con una rentabilidad de **{r}%/año**, conviertes **€{ti:,.0f}** invertidos en **€{vf:,.0f}** — el interés compuesto genera **€{g:,.0f}** adicionales. Ajustando a {inf}% de inflación, el poder adquisitivo real sería de **€{vr:,.0f}**.",
        "aviso": "⚠️ Simulación basada en rentabilidad constante — no constituye asesoramiento financiero.",
        "rodape": "Freenomics · Calculadora de interés compuesto",
    },
}

T_GERAL = {
    "🇵🇹 Português": {
        "div_titulo": "Calendário de Dividendos",
        "div_sub": "Consulta o histórico de dividendos e o dividend yield dos ativos da tua carteira.",
        "div_carteira": "Carteira", "div_tickers": "Tickers (separados por vírgula)",
        "div_anos": "Anos de histórico", "div_a_carregar": "A carregar dados de dividendos...",
        "div_aviso_sem": "Nenhum dos tickers tem histórico de dividendos (ex: SOFI e outros growth stocks não pagam dividendos).",
        "div_info": "Experimenta tickers como: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "div_resumo": "Resumo de dividendos por ativo", "div_yield": "yield",
        "div_ano_acao": "€/ano por ação", "div_historico": "Histórico de dividendos — últimos",
        "div_anos_label": "anos", "div_y": "Dividendo por ação (€/$)", "div_x": "Data de pagamento",
        "div_ultimos": "Últimos pagamentos de dividendos", "div_ultimos_label": "últimos",
        "div_pagamentos": "pagamentos", "div_ticker": "Ticker", "div_data": "Data", "div_div": "Dividendo por ação",
        "div_nota_titulo": "O que é o Dividend Yield?",
        "div_nota": "É a percentagem do preço da ação que recebes em dividendos por ano. Ex: um yield de 3% num ativo de €100 significa que recebes €3/ano por ação. Atenção: um yield muito alto pode ser sinal de que o preço da ação caiu significativamente.",
        "div_rodape": "Freenomics · Dados via Yahoo Finance · Não constitui aconselhamento financeiro.",
        "risco_titulo": "Análise de Risco",
        "risco_sub": "Correlação entre ativos, volatilidade histórica e simulação de cenários adversos.",
        "risco_carteira": "Carteira", "risco_tickers": "Tickers (mín. 2)",
        "risco_periodo": "Período", "risco_capital": "Capital total investido (€)",
        "risco_a_carregar": "A carregar dados...",
        "risco_erro": "Precisas de pelo menos 2 tickers válidos para a análise de risco.",
        "risco_vol_titulo": "Volatilidade e risco por ativo",
        "risco_var": "VaR 95%", "risco_perda": "Num dia mau (5% piores), podes perder até",
        "risco_capital_label": "num capital de",
        "risco_corr_titulo": "Correlação entre ativos",
        "risco_corr_sub": "Valores próximos de 1 = movem-se juntos | próximos de -1 = direções opostas | 0 = sem relação",
        "risco_dd_titulo": "Drawdown histórico (queda face ao pico)",
        "risco_stress_titulo": "Simulação de cenários adversos",
        "risco_stress_sub": "Impacto estimado no teu capital em diferentes cenários de mercado",
        "risco_cenarios": {"Correção leve (-10%)": -0.10, "Correção moderada (-20%)": -0.20, "Bear market (-35%)": -0.35, "Crash severo (-50%)": -0.50},
        "risco_rodape": "Freenomics · VaR = Value at Risk (percentil 5%) · Não constitui aconselhamento financeiro.",
        "risco_periodos": {"1 ano": 365, "2 anos": 730, "5 anos": 1825},
        "noticias_titulo": "Notícias da Carteira",
        "noticias_sub": "Últimas notícias relacionadas com os ativos da tua carteira.",
        "noticias_carteira": "Carteira", "noticias_tickers": "Tickers (separados por vírgula)",
        "noticias_max": "Notícias por ticker", "noticias_a_carregar": "A carregar notícias...",
        "noticias_aviso": "Não foi possível carregar notícias para",
        "noticias_sem": "Não foram encontradas notícias. Tenta outros tickers ou volta mais tarde.",
        "noticias_filtro": "Filtrar por ticker", "noticias_todos": "Todos",
        "noticias_encontradas": "notícias encontradas", "noticias_ler": "Ler artigo completo ↗",
        "noticias_rodape": "Freenomics · Notícias via Yahoo Finance · Conteúdo de terceiros.",
    },
    "🇬🇧 English": {
        "div_titulo": "Dividend Calendar",
        "div_sub": "Check the dividend history and dividend yield of your portfolio assets.",
        "div_carteira": "Portfolio", "div_tickers": "Tickers (comma-separated)",
        "div_anos": "Years of history", "div_a_carregar": "Loading dividend data...",
        "div_aviso_sem": "None of the tickers have dividend history (e.g. SOFI and other growth stocks don't pay dividends).",
        "div_info": "Try tickers like: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "div_resumo": "Dividend summary per asset", "div_yield": "yield",
        "div_ano_acao": "€/year per share", "div_historico": "Dividend history — last",
        "div_anos_label": "years", "div_y": "Dividend per share (€/$)", "div_x": "Payment date",
        "div_ultimos": "Latest dividend payments", "div_ultimos_label": "last",
        "div_pagamentos": "payments", "div_ticker": "Ticker", "div_data": "Date", "div_div": "Dividend per share",
        "div_nota_titulo": "What is Dividend Yield?",
        "div_nota": "It's the percentage of the share price you receive in dividends per year. E.g. a 3% yield on a €100 asset means you receive €3/year per share. Note: a very high yield may signal that the share price has fallen significantly.",
        "div_rodape": "Freenomics · Data via Yahoo Finance · Does not constitute financial advice.",
        "risco_titulo": "Risk Analysis",
        "risco_sub": "Asset correlation, historical volatility and adverse scenario simulation.",
        "risco_carteira": "Portfolio", "risco_tickers": "Tickers (min. 2)",
        "risco_periodo": "Period", "risco_capital": "Total invested capital (€)",
        "risco_a_carregar": "Loading data...",
        "risco_erro": "You need at least 2 valid tickers for the risk analysis.",
        "risco_vol_titulo": "Volatility and risk per asset",
        "risco_var": "VaR 95%", "risco_perda": "On a bad day (worst 5%), you could lose up to",
        "risco_capital_label": "on a capital of",
        "risco_corr_titulo": "Asset correlation",
        "risco_corr_sub": "Values near 1 = move together | near -1 = opposite directions | 0 = no relation",
        "risco_dd_titulo": "Historical drawdown (fall from peak)",
        "risco_stress_titulo": "Stress scenario simulation",
        "risco_stress_sub": "Estimated impact on your capital in different market scenarios",
        "risco_cenarios": {"Mild correction (-10%)": -0.10, "Moderate correction (-20%)": -0.20, "Bear market (-35%)": -0.35, "Severe crash (-50%)": -0.50},
        "risco_rodape": "Freenomics · VaR = Value at Risk (5th percentile) · Does not constitute financial advice.",
        "risco_periodos": {"1 year": 365, "2 years": 730, "5 years": 1825},
        "noticias_titulo": "Portfolio News",
        "noticias_sub": "Latest news related to your portfolio assets.",
        "noticias_carteira": "Portfolio", "noticias_tickers": "Tickers (comma-separated)",
        "noticias_max": "News per ticker", "noticias_a_carregar": "Loading news...",
        "noticias_aviso": "Could not load news for",
        "noticias_sem": "No news found. Try other tickers or come back later.",
        "noticias_filtro": "Filter by ticker", "noticias_todos": "All",
        "noticias_encontradas": "news found", "noticias_ler": "Read full article ↗",
        "noticias_rodape": "Freenomics · News via Yahoo Finance · Third-party content.",
    },
    "🇫🇷 Français": {
        "div_titulo": "Calendrier des Dividendes",
        "div_sub": "Consultez l'historique des dividendes et le rendement de vos actifs.",
        "div_carteira": "Portefeuille", "div_tickers": "Tickers (séparés par virgule)",
        "div_anos": "Années d'historique", "div_a_carregar": "Chargement des données de dividendes...",
        "div_aviso_sem": "Aucun des tickers n'a d'historique de dividendes.",
        "div_info": "Essayez des tickers comme: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "div_resumo": "Résumé des dividendes par actif", "div_yield": "rendement",
        "div_ano_acao": "€/an par action", "div_historico": "Historique des dividendes — dernières",
        "div_anos_label": "années", "div_y": "Dividende par action (€/$)", "div_x": "Date de paiement",
        "div_ultimos": "Derniers paiements de dividendes", "div_ultimos_label": "derniers",
        "div_pagamentos": "paiements", "div_ticker": "Ticker", "div_data": "Date", "div_div": "Dividende par action",
        "div_nota_titulo": "Qu'est-ce que le Dividend Yield?",
        "div_nota": "C'est le pourcentage du prix de l'action que vous recevez en dividendes par an. Ex: un rendement de 3% sur un actif de €100 signifie €3/an par action.",
        "div_rodape": "Freenomics · Données via Yahoo Finance · Ne constitue pas un conseil financier.",
        "risco_titulo": "Analyse des Risques",
        "risco_sub": "Corrélation entre actifs, volatilité historique et simulation de scénarios adverses.",
        "risco_carteira": "Portefeuille", "risco_tickers": "Tickers (min. 2)",
        "risco_periodo": "Période", "risco_capital": "Capital total investi (€)",
        "risco_a_carregar": "Chargement des données...",
        "risco_erro": "Vous avez besoin d'au moins 2 tickers valides pour l'analyse des risques.",
        "risco_vol_titulo": "Volatilité et risque par actif",
        "risco_var": "VaR 95%", "risco_perda": "Un mauvais jour (5% pires), vous pourriez perdre jusqu'à",
        "risco_capital_label": "sur un capital de",
        "risco_corr_titulo": "Corrélation entre actifs",
        "risco_corr_sub": "Valeurs proches de 1 = évoluent ensemble | proches de -1 = directions opposées | 0 = sans relation",
        "risco_dd_titulo": "Drawdown historique (chute depuis le pic)",
        "risco_stress_titulo": "Simulation de scénarios de stress",
        "risco_stress_sub": "Impact estimé sur votre capital dans différents scénarios de marché",
        "risco_cenarios": {"Correction légère (-10%)": -0.10, "Correction modérée (-20%)": -0.20, "Bear market (-35%)": -0.35, "Krach sévère (-50%)": -0.50},
        "risco_rodape": "Freenomics · VaR = Value at Risk (5e percentile) · Ne constitue pas un conseil financier.",
        "risco_periodos": {"1 an": 365, "2 ans": 730, "5 ans": 1825},
        "noticias_titulo": "Actualités du Portefeuille",
        "noticias_sub": "Dernières actualités liées aux actifs de votre portefeuille.",
        "noticias_carteira": "Portefeuille", "noticias_tickers": "Tickers (séparés par virgule)",
        "noticias_max": "Actualités par ticker", "noticias_a_carregar": "Chargement des actualités...",
        "noticias_aviso": "Impossible de charger les actualités pour",
        "noticias_sem": "Aucune actualité trouvée. Essayez d'autres tickers.",
        "noticias_filtro": "Filtrer par ticker", "noticias_todos": "Tous",
        "noticias_encontradas": "actualités trouvées", "noticias_ler": "Lire l'article complet ↗",
        "noticias_rodape": "Freenomics · Actualités via Yahoo Finance · Contenu tiers.",
    },
    "🇩🇪 Deutsch": {
        "div_titulo": "Dividendenkalender",
        "div_sub": "Sehen Sie die Dividendenhistorie und die Dividendenrendite Ihrer Portfolio-Anlagen.",
        "div_carteira": "Portfolio", "div_tickers": "Ticker (kommagetrennt)",
        "div_anos": "Jahre Historik", "div_a_carregar": "Dividendendaten werden geladen...",
        "div_aviso_sem": "Keiner der Ticker hat eine Dividendenhistorie.",
        "div_info": "Versuchen Sie Ticker wie: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "div_resumo": "Dividendenzusammenfassung je Anlage", "div_yield": "Rendite",
        "div_ano_acao": "€/Jahr je Aktie", "div_historico": "Dividendenhistorie — letzte",
        "div_anos_label": "Jahre", "div_y": "Dividende je Aktie (€/$)", "div_x": "Zahlungsdatum",
        "div_ultimos": "Letzte Dividendenzahlungen", "div_ultimos_label": "letzte",
        "div_pagamentos": "Zahlungen", "div_ticker": "Ticker", "div_data": "Datum", "div_div": "Dividende je Aktie",
        "div_nota_titulo": "Was ist die Dividendenrendite?",
        "div_nota": "Es ist der Prozentsatz des Aktienkurses, den Sie jährlich als Dividende erhalten. Beispiel: Eine Rendite von 3% bei einem €100-Aktie bedeutet €3/Jahr je Aktie.",
        "div_rodape": "Freenomics · Daten via Yahoo Finance · Stellt keine Finanzberatung dar.",
        "risco_titulo": "Risikoanalyse",
        "risco_sub": "Korrelation zwischen Anlagen, historische Volatilität und Stressszenarien.",
        "risco_carteira": "Portfolio", "risco_tickers": "Ticker (mind. 2)",
        "risco_periodo": "Zeitraum", "risco_capital": "Gesamtinvestiertes Kapital (€)",
        "risco_a_carregar": "Daten werden geladen...",
        "risco_erro": "Sie benötigen mindestens 2 gültige Ticker für die Risikoanalyse.",
        "risco_vol_titulo": "Volatilität und Risiko je Anlage",
        "risco_var": "VaR 95%", "risco_perda": "An einem schlechten Tag (schlechteste 5%) könnten Sie bis zu verlieren",
        "risco_capital_label": "bei einem Kapital von",
        "risco_corr_titulo": "Korrelation zwischen Anlagen",
        "risco_corr_sub": "Werte nahe 1 = bewegen sich zusammen | nahe -1 = entgegengesetzte Richtungen | 0 = kein Zusammenhang",
        "risco_dd_titulo": "Historischer Drawdown (Rückgang vom Höchststand)",
        "risco_stress_titulo": "Stressszenario-Simulation",
        "risco_stress_sub": "Geschätzte Auswirkungen auf Ihr Kapital in verschiedenen Marktszenarien",
        "risco_cenarios": {"Leichte Korrektur (-10%)": -0.10, "Moderate Korrektur (-20%)": -0.20, "Bärenmarkt (-35%)": -0.35, "Schwerer Crash (-50%)": -0.50},
        "risco_rodape": "Freenomics · VaR = Value at Risk (5. Perzentil) · Stellt keine Finanzberatung dar.",
        "risco_periodos": {"1 Jahr": 365, "2 Jahre": 730, "5 Jahre": 1825},
        "noticias_titulo": "Portfolio-Nachrichten",
        "noticias_sub": "Neueste Nachrichten zu Ihren Portfolio-Anlagen.",
        "noticias_carteira": "Portfolio", "noticias_tickers": "Ticker (kommagetrennt)",
        "noticias_max": "Nachrichten pro Ticker", "noticias_a_carregar": "Nachrichten werden geladen...",
        "noticias_aviso": "Nachrichten konnten nicht geladen werden für",
        "noticias_sem": "Keine Nachrichten gefunden. Versuchen Sie andere Ticker.",
        "noticias_filtro": "Nach Ticker filtern", "noticias_todos": "Alle",
        "noticias_encontradas": "Nachrichten gefunden", "noticias_ler": "Vollständigen Artikel lesen ↗",
        "noticias_rodape": "Freenomics · Nachrichten via Yahoo Finance · Drittanbieterinhalte.",
    },
    "🇪🇸 Español": {
        "div_titulo": "Calendario de Dividendos",
        "div_sub": "Consulta el historial de dividendos y el dividend yield de los activos de tu cartera.",
        "div_carteira": "Cartera", "div_tickers": "Tickers (separados por coma)",
        "div_anos": "Años de historial", "div_a_carregar": "Cargando datos de dividendos...",
        "div_aviso_sem": "Ninguno de los tickers tiene historial de dividendos.",
        "div_info": "Prueba tickers como: SPY, AAPL, JNJ, KO, VYM, SCHD",
        "div_resumo": "Resumen de dividendos por activo", "div_yield": "yield",
        "div_ano_acao": "€/año por acción", "div_historico": "Historial de dividendos — últimos",
        "div_anos_label": "años", "div_y": "Dividendo por acción (€/$)", "div_x": "Fecha de pago",
        "div_ultimos": "Últimos pagos de dividendos", "div_ultimos_label": "últimos",
        "div_pagamentos": "pagos", "div_ticker": "Ticker", "div_data": "Fecha", "div_div": "Dividendo por acción",
        "div_nota_titulo": "¿Qué es el Dividend Yield?",
        "div_nota": "Es el porcentaje del precio de la acción que recibes en dividendos al año. Ej: un yield de 3% en un activo de €100 significa que recibes €3/año por acción. Atención: un yield muy alto puede ser señal de que el precio ha caído significativamente.",
        "div_rodape": "Freenomics · Datos via Yahoo Finance · No constituye asesoramiento financiero.",
        "risco_titulo": "Análisis de Riesgo",
        "risco_sub": "Correlación entre activos, volatilidad histórica y simulación de escenarios adversos.",
        "risco_carteira": "Cartera", "risco_tickers": "Tickers (mín. 2)",
        "risco_periodo": "Período", "risco_capital": "Capital total invertido (€)",
        "risco_a_carregar": "Cargando datos...",
        "risco_erro": "Necesitas al menos 2 tickers válidos para el análisis de riesgo.",
        "risco_vol_titulo": "Volatilidad y riesgo por activo",
        "risco_var": "VaR 95%", "risco_perda": "En un mal día (peor 5%), podrías perder hasta",
        "risco_capital_label": "sobre un capital de",
        "risco_corr_titulo": "Correlación entre activos",
        "risco_corr_sub": "Valores cerca de 1 = se mueven juntos | cerca de -1 = direcciones opuestas | 0 = sin relación",
        "risco_dd_titulo": "Drawdown histórico (caída desde el pico)",
        "risco_stress_titulo": "Simulación de escenarios adversos",
        "risco_stress_sub": "Impacto estimado en tu capital en diferentes escenarios de mercado",
        "risco_cenarios": {"Corrección leve (-10%)": -0.10, "Corrección moderada (-20%)": -0.20, "Bear market (-35%)": -0.35, "Crash severo (-50%)": -0.50},
        "risco_rodape": "Freenomics · VaR = Value at Risk (percentil 5%) · No constituye asesoramiento financiero.",
        "risco_periodos": {"1 año": 365, "2 años": 730, "5 años": 1825},
        "noticias_titulo": "Noticias de la Cartera",
        "noticias_sub": "Últimas noticias relacionadas con los activos de tu cartera.",
        "noticias_carteira": "Cartera", "noticias_tickers": "Tickers (separados por coma)",
        "noticias_max": "Noticias por ticker", "noticias_a_carregar": "Cargando noticias...",
        "noticias_aviso": "No se pudieron cargar noticias para",
        "noticias_sem": "No se encontraron noticias. Prueba otros tickers o vuelve más tarde.",
        "noticias_filtro": "Filtrar por ticker", "noticias_todos": "Todos",
        "noticias_encontradas": "noticias encontradas", "noticias_ler": "Leer artículo completo ↗",
        "noticias_rodape": "Freenomics · Noticias via Yahoo Finance · Contenido de terceros.",
    },
}

CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Source+Serif+4:wght@600;700&family=Inter:wght@400;500;600&display=swap');

    /* ── Fontes base ── */
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    /* ── LIGHT MODE ── */
    .stApp { background-color: #FAF8F3; }
    h1, h2, h3 { font-family: 'Source Serif 4', serif !important; color: #0E2A3D; }
    p, label, span, div { color: #1A1A1A; }
    [data-testid="stSidebar"] { background-color: #F0EDE6; }
    [data-testid="stSidebar"] * { color: #0E2A3D !important; }

    /* ── DARK MODE ── */
    @media (prefers-color-scheme: dark) {
        .stApp { background-color: #0A1628 !important; }
        h1, h2, h3 { color: #FFFFFF !important; }
        p, label, span { color: #E8EDF2 !important; }
        [data-testid="stSidebar"] { background-color: #0D1E35 !important; }
        [data-testid="stSidebar"] * { color: #E8EDF2 !important; }
        .stSelectbox label, .stTextInput label, .stNumberInput label,
        .stSlider label, .stFileUploader label, .stCheckbox label,
        .stToggle label, .stRadio label {
            color: #E8EDF2 !important;
        }
        [data-testid="stMarkdownContainer"] p { color: #E8EDF2 !important; }
        [data-testid="stCaptionContainer"] { color: #9BAEC8 !important; }
    }

    /* ── Forçar dark mode quando Streamlit usa tema escuro ── */
    [data-theme="dark"] .stApp,
    .st-emotion-cache-dark .stApp { background-color: #0A1628 !important; }

    [data-theme="dark"] h1, [data-theme="dark"] h2, [data-theme="dark"] h3 {
        color: #FFFFFF !important;
    }
    [data-theme="dark"] label,
    [data-theme="dark"] .stSelectbox label,
    [data-theme="dark"] .stTextInput label,
    [data-theme="dark"] .stNumberInput label,
    [data-theme="dark"] .stSlider label,
    [data-theme="dark"] p {
        color: #E8EDF2 !important;
    }
    [data-theme="dark"] [data-testid="stSidebar"] {
        background-color: #0D1E35 !important;
    }
    [data-theme="dark"] [data-testid="stSidebar"] * {
        color: #E8EDF2 !important;
    }

    /* ── Métricas (sempre dark card) ── */
    div[data-testid="stMetric"] {
        background-color: #0E2A3D; border-radius: 10px;
        padding: 16px 18px; border-left: 4px solid #C29A4B;
    }
    div[data-testid="stMetric"] label { color: #C8D3DA !important; }
    div[data-testid="stMetricValue"] { color: #FAF8F3 !important; }
    div[data-testid="stMetricDelta"] svg { display: none; }

    /* ── Caixas de insight ── */
    .insight-box {
        background-color: #0E2A3D; border: 1px solid #1E4060;
        border-left: 4px solid #C29A4B; border-radius: 8px;
        padding: 18px 22px; margin: 12px 0;
        font-size: 0.95rem; line-height: 1.6; color: #E8EDF2;
    }

    /* ── Winner box ── */
    .winner-box {
        background-color: #0E2A3D; border-radius: 10px;
        padding: 20px; text-align: center; color: #C29A4B;
        font-size: 1.1rem; font-weight: 600; margin: 10px 0;
    }

    /* ── Info box ── */
    .info-box {
        background-color: #0E2A3D; border: 1px solid #1E4060;
        border-left: 4px solid #C29A4B; border-radius: 8px;
        padding: 14px 18px; margin: 8px 0;
        font-size: 0.9rem; line-height: 1.5; color: #E8EDF2;
    }

    /* ── Risco ── */
    .risco-box { border-radius: 8px; padding: 16px 20px; margin: 8px 0; font-size: 0.9rem; line-height: 1.5; }
    .risco-alto  { background:#3D1515; border-left: 4px solid #DC2626; color: #FCA5A5; }
    .risco-medio { background:#3D2D00; border-left: 4px solid #CA8A04; color: #FDE68A; }
    .risco-baixo { background:#0F3D1F; border-left: 4px solid #16A34A; color: #86EFAC; }

    /* ── Notícias ── */
    .noticia-card {
        background-color: #0E2A3D; border: 1px solid #1E4060;
        border-left: 4px solid #C29A4B; border-radius: 8px;
        padding: 16px 20px; margin: 10px 0;
    }
    .noticia-titulo { font-size: 1rem; font-weight: 600; color: #FFFFFF; margin-bottom: 6px; }
    .noticia-meta { font-size: 0.8rem; color: #9BAEC8; margin-bottom: 8px; }
    .noticia-resumo { font-size: 0.88rem; color: #C8D3DA; line-height: 1.5; }
    .ticker-badge {
        display: inline-block; background: #4A9FD4; color: #0A1628;
        border-radius: 4px; padding: 2px 8px; font-size: 0.75rem; font-weight: 700; margin-right: 6px;
    }

    /* ── Dropdowns / Selectbox em dark mode ── */
    [data-theme="dark"] [data-baseweb="select"] > div,
    [data-theme="dark"] [data-baseweb="select"] input {
        background-color: #1A2F4A !important;
        color: #FFFFFF !important;
        border-color: #2B5F8E !important;
    }
    [data-theme="dark"] [data-baseweb="popover"],
    [data-theme="dark"] [data-baseweb="menu"],
    [data-theme="dark"] [role="listbox"] {
        background-color: #1A2F4A !important;
    }
    [data-theme="dark"] [data-baseweb="option"],
    [data-theme="dark"] [role="option"] {
        background-color: #1A2F4A !important;
        color: #FFFFFF !important;
    }
    [data-theme="dark"] [data-baseweb="option"]:hover,
    [data-theme="dark"] [role="option"]:hover {
        background-color: #2B5F8E !important;
    }
    [data-theme="dark"] [data-baseweb="tag"] {
        background-color: #2B5F8E !important;
        color: #FFFFFF !important;
    }
    /* Inputs de texto em dark mode */
    [data-theme="dark"] input,
    [data-theme="dark"] textarea,
    [data-theme="dark"] [data-baseweb="input"] input {
        background-color: #1A2F4A !important;
        color: #FFFFFF !important;
        border-color: #2B5F8E !important;
    }
    [data-theme="dark"] input::placeholder {
        color: #6B8FAD !important;
    }
    /* Number inputs */
    [data-theme="dark"] [data-testid="stNumberInput"] input {
        background-color: #1A2F4A !important;
        color: #FFFFFF !important;
    }

    /* ── Botões ── */
    [data-theme="dark"] .stButton > button {
        background-color: #2B5F8E; color: #FFFFFF; border: none;
    }
    [data-theme="dark"] .stButton > button:hover {
        background-color: #3B8FC4;
    }
    [data-theme="dark"] .stButton > button[kind="primary"] {
        background-color: #3B8FC4 !important;
    }
</style>
"""

PLOT_COLORS = ["#0E2A3D", "#C29A4B", "#6B8E7F", "#A8453E", "#5C6B73"]
