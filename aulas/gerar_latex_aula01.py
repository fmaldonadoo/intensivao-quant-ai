#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera slides LaTeX Beamer para Aula 01 — Kickoff (17 slides).
Compilar: pdflatex slides-aula-01-kickoff.tex  (rodar 2x)
"""
import os

BASE = os.path.dirname(os.path.abspath(__file__))

# ── helpers ───────────────────────────────────────────────────────────────────

def pre(title, subtitle):
    base = r"""\documentclass[aspectratio=169,12pt]{beamer}
\usepackage{fontspec}
\usepackage[portuguese]{babel}
\usepackage{xcolor,listings,tikz,booktabs,amsmath,amssymb,graphicx,multicol,array,colortbl}
\usetikzlibrary{arrows.meta,positioning,shapes.geometric,calc}

\definecolor{navy}{HTML}{0D1B3E}
\definecolor{gold}{HTML}{F5A623}
\definecolor{qgreen}{HTML}{1E8B4C}
\definecolor{qblue}{HTML}{1A6EAE}
\definecolor{codebg}{HTML}{EEF3F8}

\usetheme{default}
\useinnertheme{circles}
\setbeamertemplate{navigation symbols}{}
\setbeamertemplate{footline}{%
  \hfill{\color{gray!60}\scriptsize\insertframenumber/\inserttotalframenumber}\hspace{.6em}\vspace{.4em}}

\setbeamercolor{frametitle}{bg=navy,fg=white}
\setbeamercolor{structure}{fg=navy}
\setbeamercolor{alerted text}{fg=gold}
\setbeamercolor{item}{fg=gold}
\setbeamercolor{subitem}{fg=navy}
\setbeamercolor{block title}{bg=qblue,fg=white}
\setbeamercolor{block body}{bg=qblue!8,fg=black}
\setbeamercolor{block title alerted}{bg=gold,fg=navy}
\setbeamercolor{block body alerted}{bg=gold!15,fg=navy}
\setbeamercolor{block title example}{bg=qgreen,fg=white}
\setbeamercolor{block body example}{bg=qgreen!10,fg=black}
\setbeamerfont{frametitle}{size=\large,series=\bfseries}
\setbeamerfont{block title}{series=\bfseries}

\setbeamertemplate{title page}{%
  \begin{tikzpicture}[remember picture,overlay]
    \fill[navy](current page.north west)rectangle(current page.south east);
    \fill[gold]([yshift=.7cm]current page.south west)rectangle(current page.south east);
    \node[anchor=south,yshift=.73cm,navy,font=\tiny\bfseries]at(current page.south)
      {INTENSIV\~{A}O QUANT AI \textbullet{} IMPACT UFSCAR};
  \end{tikzpicture}
  \vspace{.65cm}
  \begin{center}
    {\color{gold}\scriptsize\bfseries INTENSIV\~{A}O QUANT AI \textbullet{} IMPACT UFSCAR}\\[.4cm]
    {\color{white}\LARGE\bfseries\inserttitle}\\[.25cm]
    {\color{gold!85}\normalsize\insertsubtitle}\\[.5cm]
    {\color{white!70}\small\insertauthor}\\[.1cm]
    {\color{white!50}\footnotesize\insertdate}
  \end{center}}

\lstdefinestyle{python}{language=Python,
  basicstyle=\ttfamily\scriptsize\color{qblue},
  keywordstyle=\color{navy}\bfseries,
  stringstyle=\color{qgreen!80!black},
  commentstyle=\color{gray!70}\itshape,
  backgroundcolor=\color{codebg},
  frame=l,framerule=2pt,rulecolor=\color{gold},
  xleftmargin=1em,breaklines=true,showstringspaces=false,tabsize=4,
  extendedchars=false,inputencoding=ascii}
\lstset{style=python}

\author{Felipe Maldonado\\{\scriptsize VP Diretoria Quant~\textbullet{}~Impact UFSCAR}}
\date{Intensiv\~{a}o Quant AI 2025}
"""
    return base + "\\title{" + title + "}\n\\subtitle{" + subtitle + "}\n"


def fr(title, body, opts=""):
    # lstlisting inside frames requires [fragile]
    base_opts = "fragile"
    if opts:
        o = f"[{base_opts},{opts}]"
    else:
        o = f"[{base_opts}]"
    return f"\\begin{{frame}}{o}{{{title}}}\n{body}\n\\end{{frame}}\n\n"


def its(*ii):
    return "\\begin{itemize}\n" + "".join(f"  \\item {i}\n" for i in ii) + "\\end{itemize}"


def subit(item, *subs):
    s = f"  \\item {item}\n  \\begin{{itemize}}\n"
    s += "".join(f"    \\item {sub}\n" for sub in subs)
    s += "  \\end{itemize}\n"
    return s


def cols(left, right, lr=0.5):
    rr = round(1 - lr - 0.03, 2)
    return (f"\\begin{{columns}}[T]\n  \\column{{{lr}\\textwidth}}\n{left}\n"
            f"  \\column{{{rr}\\textwidth}}\n{right}\n\\end{{columns}}")


def blk(title, body, kind=""):
    if kind == "alerted":
        e = "alertblock"
    elif kind == "example":
        e = "exampleblock"
    else:
        e = "block"
    return f"\\begin{{{e}}}{{{title}}}\n{body}\n\\end{{{e}}}"


def cod(s):
    return "\\begin{lstlisting}\n" + s + "\n\\end{lstlisting}"


# ── conteúdo ──────────────────────────────────────────────────────────────────

def aula01():
    frames = ""

    # 1 — titlepage
    frames += "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    # 2 — Agenda
    frames += fr("Agenda", r"""
\begin{multicols}{2}
\tableofcontents
\end{multicols}""")

    # 3 — Por que Quant?
    frames += "\\section{Motivação}\n"
    frames += fr("Por que Gestão Quantitativa?", cols(
        its(r"Retornos consistentes baseados em \textbf{processo}, não intuição",
            r"Escala: uma estratégia testa \alert{milhares} de ativos simultaneamente",
            r"Reprodutibilidade: resultados auditáveis e rastreáveis",
            r"Vantagem competitiva: explora anomalias antes do mercado precificar"),
        blk("Mercado Brasileiro", its(
            r"B3: \textasciitilde 450 ações listadas",
            r"IBOVESPA: \textasciitilde 90 ativos, revisado a cada 4 meses",
            r"Fundos quant no Brasil cresceram $>$200\% em 5 anos",
            r"Itaú, Verde, Giant Steps, Kadima, Ibiuna"))
    ))

    # 4 — Universos de Investimento
    frames += "\\section{Universos de Investimento}\n"
    frames += fr("Universos de Investimento", r"""
\begin{center}
\renewcommand{\arraystretch}{1.3}
\begin{tabular}{>{\bfseries\color{navy}}l p{2.8cm} p{2.8cm} p{3cm}}
\rowcolor{navy}\color{white}\textbf{Classe} & \color{white}\textbf{Exemplos} &
  \color{white}\textbf{Retorno} & \color{white}\textbf{Risco principal}\\
\rowcolor{qblue!10}Renda Fixa     & Tesouro, CDB, LCI & Juros + spread    & Crédito / duration\\
Renda Variável  & Ações, FIIs, BDRs & Dividendo + capital& Volatilidade\\
\rowcolor{qblue!10}Derivativos    & Futuros, Opções   & Assimétrico       & Alavancagem\\
Alternativos    & FIPs, Crypto      & Alta variância    & Liquidez\\
\end{tabular}
\end{center}""")

    # 5 — Renda Fixa
    frames += fr("Renda Fixa — Fundamentos", cols(
        its(r"\textbf{Tesouro Selic} — pós-fixado, risco soberano mínimo",
            r"\textbf{Tesouro IPCA+} — proteção contra inflação (duration longa)",
            r"\textbf{CDB / LCI / LCA} — risco bancário, cobertura FGC até R\$250k",
            r"\textbf{Debêntures} — spread de crédito, menor liquidez"),
        blk("Conceitos-chave",
            its(r"\textbf{Duration}: sensibilidade ao juro; $\Delta P \approx -D\,\Delta y$",
                r"\textbf{Spread}: prêmio sobre a taxa livre de risco",
                r"\textbf{Rating}: probabilidade implícita de default"))
    ))

    # 6 — Renda Variável
    frames += fr("Renda Variável — Ações e Derivados", cols(
        its(r"\textbf{Ações ordinárias (ON)}: direito a voto + dividendos",
            r"\textbf{Ações preferenciais (PN)}: prioridade no dividendo",
            r"\textbf{FIIs}: imóveis via bolsa, distribuição mensal obrigatória",
            r"\textbf{BDRs}: recibos de ações estrangeiras negociadas na B3"),
        blk("Componentes do retorno", its(
            r"$r_t = \dfrac{P_t - P_{t-1} + D_t}{P_{t-1}}$",
            r"$D_t$: dividendos e juros sobre capital próprio",
            r"Retorno total ex-dividendos $\neq$ retorno total"))
    ))

    # 7 — Derivativos
    frames += fr("Derivativos e Mercados Alternativos", cols(
        its(r"\textbf{Futuros}: obrigação de comprar/vender no vencimento (IBOV, DI, Dólar)",
            r"\textbf{Opções}: direito (não obrigação); Call e Put",
            r"\textbf{Swaps}: troca de fluxos de caixa (DI $\times$ IPCA, por ex.)",
            r"\textbf{Hedge vs especulação}: mesmo instrumento, propósitos opostos"),
        blk("Alternativos", its(
            r"FIPs: private equity ilíquido, horizonte $>$5 anos",
            r"Commodities: ouro, petróleo, agro — diversificação real",
            r"Cripto: alta vol, correlação baixa com RV tradicional"))
    ))

    # 8 — MPT Markowitz
    frames += "\\section{Teoria Financeira Clássica}\n"
    frames += fr("Teoria Moderna do Portfólio — Markowitz (1952)", cols(
        r"""\textbf{Problema de otimização:}
\[
\min_{\mathbf{w}}\;\mathbf{w}^\top\boldsymbol{\Sigma}\mathbf{w}
\quad\text{s.t.}\quad
\mathbf{w}^\top\boldsymbol{\mu}\ge r^*,\;
\mathbf{w}^\top\mathbf{1}=1
\]
\vspace{.3em}
\begin{itemize}
  \item $\mathbf{w}$: vetor de pesos
  \item $\boldsymbol{\Sigma}$: matriz de covariâncias $n\times n$
  \item $\boldsymbol{\mu}$: vetor de retornos esperados
  \item Resultado: \alert{fronteira eficiente}
\end{itemize}""",
        blk("Insight central",
            r"Diversificação reduz risco sem necessariamente reduzir retorno. "
            r"O risco de um portfólio depende das \textbf{covariâncias} entre ativos, não só das variâncias individuais.") +
        "\n\\vspace{.3em}\n" +
        blk("Limitação prática",
            r"Markowitz é extremamente sensível à estimação de $\boldsymbol{\mu}$ — "
            r"pequenos erros geram pesos concentrados e instáveis (Michaud, 1989).", "alerted")
    ))

    # 9 — HME
    frames += fr("Hipótese de Mercado Eficiente — Fama (1970)", r"""
\begin{columns}[T]
  \column{0.32\textwidth}
  \begin{block}{Forma Fraca}
    Preços refletem todo o histórico de preços e volumes.\\[.3em]
    \textbf{Implicação}: análise técnica não gera alpha.
  \end{block}
  \column{0.32\textwidth}
  \begin{block}{Forma Semiforte}
    + informações públicas (relatórios, dividendos).\\[.3em]
    \textbf{Implicação}: análise fundamentalista não gera alpha.
  \end{block}
  \column{0.32\textwidth}
  \begin{alertblock}{Forma Forte}
    + informações privadas (insider).\\[.3em]
    \textbf{Implicação}: ninguém bate o mercado consistentemente.
  \end{alertblock}
\end{columns}
\vspace{.4em}
\begin{exampleblock}{Por que estudamos anomalias então?}
  Evidências empíricas contra a HME: anomalias persistentes sugerem que mercados são
  \textit{aproximadamente} eficientes — e as ineficiências são nossa oportunidade.
\end{exampleblock}""")

    # 10 — Anomalias
    frames += "\\section{Anomalias e Factor Investing}\n"
    frames += fr("Anomalias de Mercado", cols(
        its(r"\textbf{Size} (Banz, 1981): small caps superam large caps em risco ajustado",
            r"\textbf{Value} (Stattman, 1980): alto P/VPA $\Rightarrow$ baixo retorno futuro",
            r"\textbf{Momentum} (Jegadeesh \& Titman, 1993): vencedores continuam vencendo",
            r"\textbf{Low Volatility} (Black, 1972): ativos de baixa vol superam CAPM",
            r"\textbf{Quality} (Novy-Marx, 2013): empresas rentáveis superam"),
        blk("Persistência no Brasil", its(
            r"Mussa et al.\ (2012): momentum e value significativos no IBOVESPA",
            r"Fama-French 3F aplicado ao Brasil por Málaga \& Securato (2004)",
            r"Prêmios menores que EUA, mas estatisticamente presentes")) +
        "\n\\vspace{.3em}\n" +
        blk("Explicações", its(
            r"Risco não capturado pelo CAPM",
            r"Vieses comportamentais dos investidores",
            r"Fricções de mercado (liquidez, custos)"), "alerted")
    ))

    # 11 — Factor Investing
    frames += fr("Factor Investing — Fama \\& French (1993)", cols(
        r"""\textbf{CAPM} (Sharpe, 1964):
\[ r_i - r_f = \alpha + \beta_{\text{MKT}}\,(r_m-r_f) + \varepsilon \]

\textbf{Fama-French 3F} (1993):
\[ r_i - r_f = \alpha + \beta_M\,\text{MKT} + \beta_S\,\text{SMB} + \beta_V\,\text{HML} + \varepsilon \]

\textbf{Fama-French 5F} (2015):
\[ +\;\beta_R\,\text{RMW} + \beta_I\,\text{CMA} \]

\vspace{.2em}
\begin{itemize}
  \item SMB: \textit{Small Minus Big}
  \item HML: \textit{High Minus Low} (book-to-market)
  \item RMW: \textit{Robust Minus Weak} (rentabilidade)
  \item CMA: \textit{Conservative Minus Aggressive} (investimento)
\end{itemize}""",
        blk("Nossa estratégia", its(
            r"Foco em \textbf{Momentum} — não coberto pelo modelo 5F original",
            r"Carhart (1997) adicionou MOM como 4º fator",
            r"Momentum é o fator com maior Sharpe histórico (Asness et al., 2013)")) +
        "\n\\vspace{.3em}\n" +
        blk("Smart Beta", its(
            r"ETFs que replicam fatores sistematicamente",
            r"Ex: BOVA11 (mercado), SMALL11 (size)",
            r"Fundos quant = seleção dinâmica de ativos"), "example")
    ))

    # 12 — Momentum
    frames += "\\section{Momentum e Behavioral Finance}\n"
    frames += fr("O Fator Momentum — Jegadeesh \\& Titman (1993)", cols(
        r"""\textbf{Definição do sinal 12-1:}
\[
\text{Sinal}_t = \sum_{k=2}^{12} r_{t-k}
\]
equivalente a:
\begin{lstlisting}
ret.shift(2).rolling(11).sum()
\end{lstlisting}
\vspace{.3em}
\begin{itemize}
  \item Janela de 12 meses; exclui mês mais recente (reversão de curto prazo)
  \item Ranking cross-sectional: compra top decil, vende bottom decil
  \item Horizonte de holding: 3--12 meses
\end{itemize}""",
        blk("Evidências Empíricas", its(
            r"EUA (1927--1989): prêmio de 3--12\% a.a.\ (J\&T, 1993)",
            r"Internacional: 40 países (Rouwenhorst, 1998)",
            r"Brasil: significativo em períodos $>$6 meses (Mussa et al., 2012)",
            r"Ativos: ações, moedas, commodities, bonds (Asness et al., 2013)")) +
        "\n\\vspace{.3em}\n" +
        blk("Momentum Crash", its(
            r"Crises de liquidez revertem momentum abruptamente",
            r"Controle: ajuste por volatilidade (Moskowitz et al., 2012)"), "alerted")
    ))

    # 13 — Behavioral Finance
    frames += fr("Finanças Comportamentais", cols(
        its(r"\textbf{Herding}: investidores seguem a maioria, amplificando tendências",
            r"\textbf{Underreaction}: mercado demora a incorporar novas informações",
            r"\textbf{Overreaction}: eventual correção exagerada (reversão de longo prazo)",
            r"\textbf{Disposition Effect}: vende ganhador cedo, segura perdedor"),
        blk("Hong \\& Stein (1999)", r"""
\textit{A unified theory of underreaction, momentum trading and overreaction.}\\[.3em]
Dois tipos de agentes:
\begin{itemize}
  \item \textbf{News watchers}: agem em fundamentos, propagação lenta
  \item \textbf{Momentum traders}: agem em preço passado
\end{itemize}
Interação gera momentum no curto prazo e reversão no longo prazo.""") +
        "\n\\vspace{.2em}\n" +
        blk("Kahneman (2011)", r"Sistema 1 (rápido, intuitivo) vs Sistema 2 (lento, racional). Vieses cognitivos são previsíveis e exploráveis.", "example")
    ))

    # 14 — Desafio Itaú
    frames += "\\section{O Desafio Itaú}\n"
    frames += fr("O Desafio Itaú Asset Management", cols(
        blk("O que é?", its(
            r"Competição nacional de gestão quantitativa de portfólios",
            r"Promovida pela Itaú Asset Management",
            r"Foco em estratégias sistemáticas com dados reais",
            r"Participantes: universidades e grupos de pesquisa")) +
        "\n\\vspace{.3em}\n" +
        blk("Critérios de Avaliação", its(
            r"\textbf{Rigor metodológico}: backtest sem viés, walk-forward",
            r"\textbf{Fundamentação econômica}: por que o fator funciona?",
            r"\textbf{Qualidade do código}: reprodutível, documentado",
            r"\textbf{Comunicação}: clareza, honestidade sobre limitações")),
        blk("Entregáveis", its(
            r"Relatório técnico (PDF)",
            r"Código reprodutível (GitHub)",
            r"Apresentação oral de 10 min + 5 min de perguntas",
            r"Pipeline completo: dados $\to$ sinal $\to$ portfólio $\to$ backtest $\to$ validação")) +
        "\n\\vspace{.3em}\n" +
        blk("Nossa preparação", its(
            r"10 semanas de treinamento intensivo",
            r"Pipeline completo em Python com dados reais do IBOVESPA",
            r"Sinal de momentum academicamente fundamentado",
            r"Backtest rigoroso com DSR e walk-forward"), "example")
    ))

    # 15 — Nossa Abordagem
    frames += "\\section{Nossa Abordagem}\n"
    frames += fr("Pipeline Técnico do Intensivão", r"""
\begin{center}
\begin{tikzpicture}[node distance=.7cm and .5cm,
  box/.style={draw=navy,fill=navy!8,rounded corners=3pt,text width=1.7cm,align=center,
              font=\scriptsize\bfseries,inner sep=4pt},
  arr/.style={-Stealth,navy,thick}]
  \node[box](d){Dados\\{\tiny yfinance}};
  \node[box,right=of d](e){EDA\\{\tiny análise}};
  \node[box,right=of e](s){Sinal v1\\{\tiny 12-1}};
  \node[box,right=of s](p){Portfólio\\{\tiny top 20\%}};
  \node[box,right=of p](b){Backtest\\{\tiny IS}};
  \node[box,right=of b](v){Validação\\{\tiny OOS/DSR}};
  \node[box,right=of v](r){Relatório\\{\tiny defesa}};

  \draw[arr](d)--(e); \draw[arr](e)--(s); \draw[arr](s)--(p);
  \draw[arr](p)--(b); \draw[arr](b)--(v); \draw[arr](v)--(r);

  \node[below=.4cm of s,font=\scriptsize,gold]{\textbf{Sinal v2}};
  \node[below=.4cm of p,font=\scriptsize,gold]{\textbf{Vol-weight}};
  \node[below=.4cm of v,font=\scriptsize,gold]{\textbf{Walk-forward}};
\end{tikzpicture}
\end{center}
\vspace{.2em}
\begin{columns}[T]
  \column{0.33\textwidth}
  \begin{block}{Dados (Aulas 2--3)}
    IBOVESPA via yfinance\\Limpeza, retornos mensais\\EDA: fat tails, correlações
  \end{block}
  \column{0.33\textwidth}
  \begin{block}{Estratégia (Aulas 4--7)}
    Sinal momentum 12-1\\Alocação: EW, vol-weight\\Backtest e métricas
  \end{block}
  \column{0.33\textwidth}
  \begin{block}{Validação (Aulas 8--10)}
    Walk-forward OOS\\DSR, análise de sensibilidade\\GenAI + relatório final
  \end{block}
\end{columns}""")

    # 16 — Roadmap
    frames += fr("Roadmap --- 10 Aulas", r"""
\begin{center}
\renewcommand{\arraystretch}{1.25}
\begin{tabular}{>{\bfseries\color{navy}}c >{\bfseries}l p{5.5cm} l}
\rowcolor{navy}\color{white}\# & \color{white}Tema & \color{white}Conteúdo principal & \color{white}Entregável\\
\rowcolor{gold!15}01 & Kickoff        & Teoria, mercados, pipeline, roadmap        & Este slide\\
02 & Dados          & yfinance, limpeza, retornos mensais       & 3 parquets\\
\rowcolor{gold!15}03 & EDA            & Distribuições, fat tails, correlações     & Gráficos\\
04 & Sinal v1       & Momentum 12-1, IC, ranking                & sinal\_v1.parquet\\
\rowcolor{gold!15}05 & Backtest v1    & Sharpe, MDD, equity curve                 & ret\_carteira.parquet\\
06 & Alocação       & Equal-weight, vol-weight, Markowitz       & pesos\_v2.parquet\\
\rowcolor{gold!15}07 & Sinal v2       & Vol-adjusted momentum, IC melhorado       & sinal\_v2.parquet\\
08 & Backtest Rig.  & Walk-forward, DSR, look-ahead bias        & ret\_oos.parquet\\
\rowcolor{gold!15}09 & GenAI          & API Anthropic, narrativas, pesquisa       & Relatório narrativo\\
10 & Relatório      & Painel final, sensibilidade, defesa       & PDF + GitHub\\
\end{tabular}
\end{center}""")

    # 17 — Referências
    frames += fr("Referências Bibliográficas", r"""
\begin{multicols}{2}
\tiny
\begin{itemize}
  \item \textbf{Markowitz, H.} (1952). Portfolio Selection. \textit{Journal of Finance}, 7(1), 77--91.
  \item \textbf{Sharpe, W.} (1964). Capital asset prices. \textit{Journal of Finance}, 19(3), 425--442.
  \item \textbf{Fama, E.} (1970). Efficient capital markets. \textit{Journal of Finance}, 25(2), 383--417.
  \item \textbf{Black, F.} (1972). Capital market equilibrium with restricted borrowing. \textit{Journal of Business}, 45(3).
  \item \textbf{Banz, R.} (1981). The relationship between return and market value. \textit{JFE}, 9(1), 3--18.
  \item \textbf{Stattman, D.} (1980). Book values and stock returns. \textit{Chicago MBA}, 4, 25--45.
  \item \textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1), 65--91.
  \item \textbf{Fama, E. \& French, K.} (1993). Common risk factors. \textit{JFE}, 33(1), 3--56.
  \item \textbf{Rouwenhorst, K.} (1998). International momentum strategies. \textit{Journal of Finance}, 53(1), 267--284.
  \item \textbf{Hong, H. \& Stein, J.} (1999). A unified theory of underreaction. \textit{Journal of Finance}, 54(6), 2143--2184.
  \item \textbf{Carhart, M.} (1997). On persistence in mutual fund performance. \textit{Journal of Finance}, 52(1), 57--82.
  \item \textbf{Kahneman, D.} (2011). \textit{Thinking, Fast and Slow}. Farrar, Straus and Giroux.
  \item \textbf{DeMiguel, V.\ et al.} (2009). Optimal versus naive diversification. \textit{RFS}, 22(5), 1915--1953.
  \item \textbf{Fama, E. \& French, K.} (2015). A five-factor asset pricing model. \textit{JFE}, 116(1), 1--22.
  \item \textbf{Moskowitz, T.\ et al.} (2012). Time series momentum. \textit{JFE}, 104(2), 228--250.
  \item \textbf{Asness, C.\ et al.} (2013). Value and momentum everywhere. \textit{Journal of Finance}, 68(3), 929--985.
  \item \textbf{Novy-Marx, R.} (2013). The other side of value. \textit{JFE}, 108(1), 1--28.
  \item \textbf{Mussa, A.\ et al.} (2012). Hipótese de mercados eficientes e finanças comportamentais. \textit{REGE}, 19(2).
  \item \textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{Journal of Portfolio Management}, 40(5).
  \item \textbf{López de Prado, M.} (2018). \textit{Advances in Financial Machine Learning}. Wiley.
\end{itemize}
\end{multicols}""")

    # montar documento
    doc = (pre("Aula 01 --- Kickoff",
               "Do Zero ao Portfólio Quant em 10 Semanas")
           + "\n\\begin{document}\n\n"
           + "\\section{Motivação}\n"
           + "\\section{Universos de Investimento}\n"
           + "\\section{Teoria Financeira Clássica}\n"
           + "\\section{Anomalias e Factor Investing}\n"
           + "\\section{Momentum e Behavioral Finance}\n"
           + "\\section{O Desafio Itaú}\n"
           + "\\section{Nossa Abordagem}\n"
           + "\\section{Referências}\n\n")

    # rewrite: sections já no body
    doc = (pre("Aula 01 --- Kickoff",
               "Do Zero ao Portfólio Quant em 10 Semanas")
           + "\n\\begin{document}\n\n"
           + frames
           + "\\end{document}\n")

    folder = os.path.join(BASE, "aula-01-kickoff")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, "slides-aula-01-kickoff.tex")
    with open(path, "w", encoding="utf-8") as f:
        f.write(doc)
    print("  Aula 01: slides-aula-01-kickoff.tex")


if __name__ == "__main__":
    print("Gerando LaTeX Aula 01...")
    aula01()
    print("Concluido!")
