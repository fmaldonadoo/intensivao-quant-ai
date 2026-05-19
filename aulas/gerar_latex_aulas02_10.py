#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera slides LaTeX Beamer para Aulas 02–10 do Intensivão Quant AI.
Compilar: lualatex slides-aula-XX-nome.tex  (rodar 2x)
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
      {INTENSIVÃO QUANT AI \textbullet{} IMPACT UFSCAR};
  \end{tikzpicture}
  \vspace{.65cm}
  \begin{center}
    {\color{gold}\scriptsize\bfseries INTENSIVÃO QUANT AI \textbullet{} IMPACT UFSCAR}\\[.4cm]
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
\date{Intensivão Quant AI 2025}
"""
    return base + "\\title{" + title + "}\n\\subtitle{" + subtitle + "}\n"


def fr(title, body, opts=""):
    o = f"[fragile,{opts}]" if opts else "[fragile]"
    return f"\\begin{{frame}}{o}{{{title}}}\n{body}\n\\end{{frame}}\n\n"


def its(*ii):
    return "\\begin{itemize}\n" + "".join(f"  \\item {i}\n" for i in ii) + "\\end{itemize}"


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


def construir(funcoes, entradas, saidas):
    """Slide padrão 'O que vamos construir'."""
    col_l = blk("Funções a implementar", its(*funcoes))
    col_r = (blk("Entradas (parquets)", its(*entradas)) +
             "\n\\vspace{.4em}\n" +
             blk("Saídas (parquets)", its(*saidas), "example"))
    return cols(col_l, col_r, lr=0.52)


def refs(*items):
    s = "\\begin{multicols}{2}\n\\tiny\n\\begin{itemize}\n"
    for item in items:
        s += f"  \\item {item}\n"
    s += "\\end{itemize}\n\\end{multicols}"
    return s


def save(content, pasta, filename):
    folder = os.path.join(BASE, pasta)
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, filename), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"  Salvo: {pasta}/{filename}")


def doc(preamble, frames):
    return preamble + "\n\\begin{document}\n\n" + frames + "\n\\end{document}\n"


# ── Aula 02 — Dados ───────────────────────────────────────────────────────────

def aula02():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "O universo IBOVESPA: composição e rebalanceamento",
            "Pipeline de dados: da fonte ao parquet",
            "Tratamento de outliers e dados faltantes",
            "Retornos compostos vs simples")),
        blk("Código (70 min)", its(
            r"\texttt{baixar\_dados()} — yfinance $\to$ DataFrame",
            r"\texttt{limpar\_precos()} — outliers, forward-fill",
            r"\texttt{calcular\_retornos\_mensais()} — resample + log-ret",
            "Salvar 3 parquets base",
            "Verificação de sanidade dos dados"))
    ))

    frames += fr("O Universo IBOVESPA", cols(
        its("Índice de retorno total da B3: ~90 ativos",
            r"Critério de inclusão: liquidez (VDLA $\geq$ 0{,}1\% do total)",
            "Rebalanceamento: janeiro, maio e setembro",
            "Composição histórica obtida via yfinance",
            r"Período de análise: 2015--2024 (120 meses)"),
        blk("Por que o IBOVESPA?", its(
            "Universo amplo o suficiente para cross-section",
            "Dados históricos de qualidade disponíveis",
            "Relevante para o Desafio Itaú",
            "Benchmark natural para estratégias Long Only")) +
        "\\vspace{.4em}\n" +
        blk("Atenção: Survivorship Bias", its(
            "yfinance retorna composição atual + histórico de preços",
            "Ativos que saíram do índice ainda têm dados históricos",
            "Bias reduzido, mas não eliminado — limitação declarada"), "alerted")
    ))

    frames += fr("Pipeline de Dados", r"""
\begin{center}
\begin{tikzpicture}[node distance=.6cm and .4cm,
  box/.style={draw=navy,fill=navy!8,rounded corners=3pt,
              text width=2.2cm,align=center,font=\scriptsize\bfseries,inner sep=5pt},
  arr/.style={-Stealth,navy,thick}]
  \node[box](a){yfinance\\{\tiny download}};
  \node[box,right=of a](b){precos\_ibov\\{\tiny parquet}};
  \node[box,right=of b](c){limpar\\{\tiny outliers}};
  \node[box,right=of c](d){ret diários\\{\tiny parquet}};
  \node[box,right=of d](e){resample\\{\tiny mensal}};
  \node[box,right=of e](f){ret mensais\\{\tiny parquet}};
  \draw[arr](a)--(b); \draw[arr](b)--(c); \draw[arr](c)--(d);
  \draw[arr](d)--(e); \draw[arr](e)--(f);
\end{tikzpicture}
\end{center}
\vspace{.3em}
\begin{columns}[T]
  \column{0.48\textwidth}
  \begin{block}{Outlier Detection}
    Retorno diário $|r_t| > 3\sigma$ rolling 60d $\Rightarrow$ substituído por NaN \\
    Forward-fill limitado a 5 dias consecutivos
  \end{block}
  \column{0.48\textwidth}
  \begin{block}{Retorno Composto Mensal}
    $r_\text{mês} = \prod_{t \in \text{mês}}(1+r_t) - 1$ \\
    Equivalente a \texttt{resample('ME').apply(retorno\_composto)}
  \end{block}
\end{columns}""")

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{baixar\_dados(tickers, start, end)} $\to$ DataFrame de preços",
         r"\texttt{limpar\_precos(df)} $\to$ DataFrame limpo, outliers removidos",
         r"\texttt{calcular\_retornos\_mensais(precos)} $\to$ DataFrame mensal",
         r"\texttt{verificar\_sanidade(df)} $\to$ estatísticas de qualidade"],
        ["Nenhum (download direto via yfinance)"],
        [r"\texttt{precos\_ibov.parquet}",
         r"\texttt{retornos\_diarios\_limpo.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Cont, R.} (2001). Empirical properties of asset returns: stylized facts and statistical issues. \textit{Quantitative Finance}, 1(2), 223--236.",
        r"\textbf{Harvey, C. et al.} (2016). ... and the cross-section of expected returns. \textit{RFS}, 29(1), 5--68.",
        r"\textbf{yfinance} (2019). Yahoo Finance Python wrapper. \textit{GitHub: ranaroussi/yfinance}.",
        r"\textbf{Mussa, A. et al.} (2012). Hipótese de mercados eficientes e finanças comportamentais. \textit{REGE}, 19(2)."
    ))

    p = pre("Aula 02 --- Dados", "Coleta, Limpeza e Preparação de Dados Financeiros")
    save(doc(p, frames), "aula-02-dados", "slides-aula-02-dados.tex")


# ── Aula 03 — EDA ────────────────────────────────────────────────────────────

def aula03():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "Distribuições de retorno: normalidade vs fat tails",
            "Skewness, kurtosis e o Teorema do Limite Central",
            "Correlações: estáticas e rolling",
            "Estacionaridade e o teste ADF")),
        blk("Código (70 min)", its(
            "Histograma + QQ-plot para diagnóstico de normalidade",
            "Scatter risk-return por ativo",
            "Heatmap de correlação com clusterização",
            "Correlação rolling de 12 meses",
            "Teste ADF: quais ativos são estacionários?"))
    ))

    frames += fr("Distribuição de Retornos Financeiros", cols(
        r"""
\textbf{Hipótese Normal (incorreta):}
\[ r_t \sim \mathcal{N}(\mu, \sigma^2) \]

\textbf{Realidade empírica:}
\begin{itemize}
  \item \textbf{Kurtosis} $> 3$: caudas mais pesadas que Normal
  \item \textbf{Skewness} $\neq 0$: assimetria, geralmente negativa
  \item \textbf{Autocorrelação} de $r_t$: próxima de zero
  \item \textbf{Autocorrelação} de $|r_t|$: positiva (volatility clustering)
\end{itemize}
\vspace{.3em}
\begin{alertblock}{Implicação para risco}
VaR e CVaR calculados com Normal \textbf{subestimam} eventos extremos.
Distribuições: $t$-Student, GED, misturas de normais.
\end{alertblock}""",
        blk("Stylized Facts (Cont, 2001)", its(
            r"Heavy tails: kurtosis $\approx$ 4--10 em ações",
            "Gain/Loss Asymmetry: quedas mais abruptas que altas",
            r"Volatility Clustering: $|\varepsilon_t|$ correlacionado",
            r"Leverage Effect: $\text{Corr}(r_t, \sigma_{t+k}^2) < 0$",
            "Long memory em volatilidade (GARCH)")) +
        "\\vspace{.3em}\n" +
        blk("QQ-Plot", r"Quantis empíricos vs Normal: pontos nas caudas \textbf{acima} da linha $\Rightarrow$ fat tails.", "example")
    ))

    frames += fr("Correlações e Estacionaridade", cols(
        blk("Matriz de Correlação", its(
            "Correlações cross-sectional: como os ativos se movem juntos",
            r"Hierarquical clustering: agrupa setores similares",
            r"Em crises: correlações convergem para 1 (diversificação falha)",
            "Rolling 12m: evolução temporal das relações")) +
        "\\vspace{.3em}\n" +
        blk("Correlação Espúria", r"Séries não-estacionárias têm alta correlação por tendência compartilhada — não por relação causal.", "alerted"),
        blk("Teste ADF", its(
            r"$H_0$: série tem raiz unitária (não-estacionária)",
            r"$H_1$: série é estacionária",
            r"Retornos $r_t$: geralmente estacionários ($p < 0{,}05$)",
            r"Preços $P_t$: geralmente não-estacionários (random walk)")) +
        "\\vspace{.3em}\n" +
        blk("Por que importa?", r"Modelos de regressão em séries não-estacionárias produzem regressão espúria. Sempre transforme preços em retornos antes de modelar.", "example")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{plot\_histograma\_qqplot(ret)} $\to$ diagnóstico de normalidade",
         r"\texttt{plot\_risk\_return(ret)} $\to$ scatter por ativo",
         r"\texttt{plot\_heatmap\_correlacao(ret)} $\to$ matriz com cluster",
         r"\texttt{plot\_rolling\_corr(ret, janela=12)} $\to$ evolução temporal",
         r"\texttt{testar\_estacionaridade(ret)} $\to$ ADF por ativo"],
        [r"\texttt{retornos\_mensais\_limpo.parquet}",
         r"\texttt{retornos\_diarios\_limpo.parquet}"],
        ["Gráficos PNG para o relatório",
         r"DataFrame com p-valores do ADF"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Cont, R.} (2001). Empirical properties of asset returns. \textit{Quantitative Finance}, 1(2), 223--236.",
        r"\textbf{Mandelbrot, B.} (1963). The variation of certain speculative prices. \textit{Journal of Business}, 36(4), 394--419.",
        r"\textbf{Engle, R.} (1982). Autoregressive conditional heteroscedasticity. \textit{Econometrica}, 50(4), 987--1007.",
        r"\textbf{Dickey, D. \& Fuller, W.} (1979). Distribution of the estimators for autoregressive time series. \textit{JASA}, 74(366), 427--431."
    ))

    p = pre("Aula 03 --- EDA", "Análise Exploratória de Dados Financeiros")
    save(doc(p, frames), "aula-03-eda", "slides-aula-03-eda.tex")


# ── Aula 04 — Sinal v1 ───────────────────────────────────────────────────────

def aula04():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "O pipeline quant de geração de alfa",
            "Anatomia do sinal 12-1 de momentum",
            "Information Coefficient (IC): o que é e por que importa",
            "IC ratio e IR: avaliando poder preditivo")),
        blk("Código (70 min)", its(
            r"\texttt{calcular\_sinal\_v1()} — implementação do sinal 12-1",
            "Ranking cross-sectional mensal",
            r"\texttt{calcular\_ic\_serie()} — Spearman mês a mês",
            "Visualização: IC barras e rolling IC",
            r"Salvar \texttt{sinal\_v1.parquet}"))
    ))

    frames += fr("O Fator Momentum — Sinal 12-1", cols(
        r"""\textbf{Definição formal:}
\[
\text{Sinal}_{i,t} = \sum_{k=2}^{12} r_{i,t-k}
\]
\vspace{.1em}
Em pandas:
\begin{lstlisting}
ret.shift(2).rolling(11).sum()
\end{lstlisting}
\vspace{.3em}
\begin{itemize}
  \item \texttt{shift(2)}: exclui o mês mais recente (reversão de curto prazo: Jegadeesh, 1990)
  \item \texttt{rolling(11)}: soma dos 11 meses anteriores ao mês exluído
  \item Total: janela de formação de 12 meses, skip 1 mês
\end{itemize}""",
        blk("Intuição Econômica", its(
            r"Underreaction de investidores a notícias (Hong \& Stein, 1999)",
            "Herding: fundos seguem vencedores recentes",
            "Momentum institucional: trimestral window dressing",
            r"Prêmio por risco de crash (Daniel \& Moskowitz, 2016)")) +
        "\\vspace{.3em}\n" +
        blk("Ranking Cross-Sectional", r"""
Cada mês $t$: ranquear todos os ativos pelo sinal.\\
Comprar \textbf{top 20\%} (quintil superior).\\
Portfólio long-only, equal-weight entre selecionados.""")
    ))

    frames += fr("Information Coefficient (IC)", cols(
        r"""\textbf{Definição:}
\[ \text{IC}_t = \rho_S\!\left(\text{Sinal}_{i,t},\; r_{i,t+1}\right) \]
onde $\rho_S$ é a correlação de Spearman.
\vspace{.4em}
\begin{itemize}
  \item $\text{IC} > 0$: sinal tem poder preditivo
  \item $\text{IC} = 0$: sinal aleatório
  \item Referência: IC médio $> 0{,}05$ é considerado bom
  \item Spearman (vs Pearson): robusto a outliers de retorno
\end{itemize}
\vspace{.3em}
\begin{alertblock}{IC vs t-statistic}
IC médio isolado é insuficiente. Calcule $t = \frac{\overline{IC}}{\sigma_{IC}/\sqrt{T}}$.
Um IC de 0{,}04 com $T=60$ meses dá $t \approx 2{,}0$ — marginalmente significativo.
\end{alertblock}""",
        blk("IR — Information Ratio", r"""
\[ \text{IR} = \frac{\overline{IC}}{\sigma_{IC}} \]
\begin{itemize}
  \item Análogo ao Sharpe do sinal
  \item IR $> 0{,}5$: sinal de qualidade institucional
  \item Fundamento da Fundamental Law of Active Management (Grinold, 1989):
\end{itemize}
\[ \text{IR} \approx \text{IC} \times \sqrt{N} \]
onde $N$ = número de apostas independentes por período.""")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{calcular\_sinal\_v1(ret\_mensais)} $\to$ DataFrame de sinais",
         r"\texttt{rankear\_sinal(sinal)} $\to$ ranks normalizados 0--1",
         r"\texttt{calcular\_ic\_serie(sinal, ret)} $\to$ Series de IC mensais",
         r"\texttt{plot\_ic\_barras(ic\_serie)} $\to$ gráfico de barras com IC rolling"],
        [r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{sinal\_v1.parquet}",
         "Gráfico IC mensal e rolling"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners and selling losers. \textit{Journal of Finance}, 48(1), 65--91.",
        r"\textbf{Jegadeesh, N.} (1990). Evidence of predictable behavior of security returns. \textit{Journal of Finance}, 45(3), 881--898.",
        r"\textbf{Grinold, R.} (1989). The fundamental law of active management. \textit{Journal of Portfolio Management}, 15(3), 30--37.",
        r"\textbf{Hong, H. \& Stein, J.} (1999). A unified theory of underreaction, momentum trading and overreaction. \textit{Journal of Finance}, 54(6), 2143--2184.",
        r"\textbf{Daniel, K. \& Moskowitz, T.} (2016). Momentum crashes. \textit{JFE}, 122(2), 221--247."
    ))

    p = pre("Aula 04 --- Sinal v1", "Construindo o Sinal de Momentum Cross-Sectional")
    save(doc(p, frames), "aula-04-sinal-v1", "slides-aula-04-sinal-v1.tex")


# ── Aula 05 — Backtest v1 ────────────────────────────────────────────────────

def aula05():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "Hipóteses do backtest: o que estamos testando?",
            "Métricas de performance: Sharpe, Sortino, MDD, Calmar",
            "O problema do look-ahead bias: shift(1)",
            "Custos de transação: modelagem simplificada")),
        blk("Código (70 min)", its(
            r"\texttt{construir\_portfolio()} — top 20\%, shift(1)",
            r"\texttt{calcular\_metricas()} — todas as métricas de uma vez",
            "Equity curve e drawdown chart",
            "Análise de retornos por ano (heatmap)",
            r"Salvar \texttt{pesos\_v1.parquet} e \texttt{retorno\_carteira.parquet}"))
    ))

    frames += fr("Métricas de Performance", cols(
        r"""\textbf{Sharpe Ratio:}
\[ S = \frac{\overline{r} - r_f}{\sigma_r} \times \sqrt{12} \]
\vspace{.1em}
\textbf{Sortino Ratio:}
\[ \text{Sort} = \frac{\overline{r} - r_f}{\sigma_{\text{neg}}} \times \sqrt{12} \]
$\sigma_{\text{neg}}$: desvio padrão apenas dos retornos negativos.
\vspace{.2em}
\textbf{Maximum Drawdown (MDD):}
\[ \text{MDD} = \min_t \frac{V_t - \max_{s \leq t} V_s}{\max_{s \leq t} V_s} \]
\textbf{Calmar Ratio:}
\[ \text{Calmar} = \frac{\text{CAGR}}{|\text{MDD}|} \]""",
        blk("Referências de Mercado", its(
            r"Sharpe $> 1{,}0$: bom (geralmente difícil de alcançar)",
            r"Sharpe $> 0{,}5$: aceitável para long-only",
            r"MDD $< 20\%$: confortável para maioria dos mandatos",
            r"Calmar $> 0{,}5$: risco/retorno razoável")) +
        "\\vspace{.3em}\n" +
        blk("CAGR — Retorno Anualizado", r"""
\[ \text{CAGR} = \left(\prod_{t=1}^{T}(1+r_t)\right)^{12/T} - 1 \]
Compõe retornos mensais e anualiza pelo número de meses $T$.""", "example")
    ))

    frames += fr("Estrutura do Backtest", cols(
        r"""\textbf{Por que shift(1)?}
\vspace{.3em}
\begin{itemize}
  \item Sinal calculado no \textbf{final do mês $t-1$}
  \item Portfólio formado no \textbf{início do mês $t$}
  \item Retorno realizado no \textbf{mês $t$}
\end{itemize}
\vspace{.3em}
\begin{lstlisting}
# ERRADO: look-ahead bias
ret_carteira = (sinal > 0) * ret_mensais

# CORRETO: shift(1) evita o bias
pesos = construir_pesos(sinal)
ret_carteira = (pesos.shift(1) * ret_mensais).sum(axis=1)
\end{lstlisting}""",
        blk("Custos de Transação", its(
            r"Modelagem simplificada: $c = 0{,}1\%$ por operação",
            r"Turnover mensal: $\sum_i |w_{i,t} - w_{i,t-1}|$",
            r"Custo total: Turnover $\times c$",
            r"Em média: momentum tem turnover de 30--50\% a.m.")) +
        "\\vspace{.3em}\n" +
        blk("Hipóteses do backtest", its(
            "Execução ao preço de fechamento do mês",
            "Liquidez infinita (sem market impact)",
            "Sem short: long-only com equal-weight no top 20\\%",
            "Benchmark: IBOVESPA (BOVA11)"), "alerted")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{construir\_portfolio(sinal, ret, n\_pct=0.2)} $\to$ retornos da carteira",
         r"\texttt{calcular\_metricas(ret, rf=0.1025)} $\to$ dicionário de métricas",
         r"\texttt{exibir\_metricas(metricas)} $\to$ tabela formatada",
         r"\texttt{plot\_equity\_drawdown(ret)} $\to$ equity curve + MDD"],
        [r"\texttt{sinal\_v1.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{pesos\_v1.parquet}",
         r"\texttt{retorno\_carteira.parquet}"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Sharpe, W.} (1966). Mutual fund performance. \textit{Journal of Business}, 39(1), 119--138.",
        r"\textbf{Sortino, F. \& van der Meer, R.} (1991). Downside risk. \textit{Journal of Portfolio Management}, 17(4), 27--31.",
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1), 65--91.",
        r"\textbf{Korajczyk, R. \& Sadka, R.} (2004). Are momentum profits robust to trading costs? \textit{Journal of Finance}, 59(3), 1039--1082.",
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{JPM}, 40(5)."
    ))

    p = pre("Aula 05 --- Backtest v1", "Construindo e Avaliando o Primeiro Backtest")
    save(doc(p, frames), "aula-05-backtest-v1", "slides-aula-05-backtest-v1.tex")


# ── Aula 06 — Alocação ───────────────────────────────────────────────────────

def aula06():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "Dimensões da decisão de alocação de portfólio",
            "Equal-weight: a surpreendente robustez do 1/N",
            "Vol-weight: alocação inversa à volatilidade (risk parity)",
            "Markowitz na prática: problemas e soluções")),
        blk("Código (70 min)", its(
            r"\texttt{pesos\_equal\_weight()} — benchmark de comparação",
            r"\texttt{pesos\_vol\_weight()} — risco parity simplificado",
            r"\texttt{pesos\_markowitz()} — otimização com scipy",
            "Comparação de turnover e Sharpe",
            r"Salvar \texttt{pesos\_v2.parquet}"))
    ))

    frames += fr("Equal-Weight vs Markowitz", cols(
        blk(r"DeMiguel et al.\ (2009)", r"""
\textit{Optimal versus naive diversification: how inefficient is the 1/N portfolio strategy?}
\vspace{.3em}
\begin{itemize}
  \item Testaram 14 modelos de otimização vs 1/N em 7 datasets
  \item \textbf{Resultado}: 1/N vence ou empata em out-of-sample Sharpe em $\approx$90\% dos casos
  \item Razão: erro de estimação de $\boldsymbol{\mu}$ domina o ganho teórico da otimização
  \item Janela necessária para Markowitz vencer 1/N: $\approx$3.000 meses de dados
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Implicação prática", r"Com 10 anos de dados mensais (120 obs), Markowitz é instável. \textbf{Use restrições}: long-only, cap por ativo, shrinkage de covariância.", "alerted"),
        r"""
\textbf{Problema de Markowitz:}
\[
\min_{\mathbf{w}}\;\mathbf{w}^\top\boldsymbol{\hat\Sigma}\mathbf{w}
\]
\vspace{.1em}
\textbf{Erros se propagam:}
\[
\boldsymbol{\hat\Sigma} = \boldsymbol{\Sigma} + \boldsymbol{\varepsilon}_\Sigma
\]
$\boldsymbol{\varepsilon}_\Sigma$ introduz peso excessivo em ativos de baixa variância estimada.

\vspace{.3em}
\begin{exampleblock}{Ledoit-Wolf Shrinkage}
$\boldsymbol{\hat\Sigma}_{\text{shrink}} = (1-\alpha)\boldsymbol{\hat\Sigma} + \alpha\,\mathbf{I}\,\bar\sigma^2$\\
Reduz erros de estimação da matriz de covariância.
\end{exampleblock}"""
    ))

    frames += fr("Vol-Weight e Risk Parity", cols(
        r"""\textbf{Vol-Weight (Risk Parity Simplificado):}
\[
w_i = \frac{1/\hat\sigma_i}{\sum_j 1/\hat\sigma_j}
\]
\vspace{.1em}
\begin{itemize}
  \item Ativos de menor volatilidade recebem maior peso
  \item Sem estimação de retornos esperados: evita o principal source de erro
  \item Rolling 60 dias: estável, reativo a mudanças de regime
  \item Turnover: menor que Markowitz, maior que EW
\end{itemize}""",
        blk("Comparação das Estratégias", its(
            r"\textbf{Equal-weight}: simples, baixo turnover, baseline forte",
            r"\textbf{Vol-weight}: melhor ajuste a risco, fundamento em risk parity",
            r"\textbf{Markowitz}: teoricamente ótimo, instável na prática",
            r"\textbf{Usaremos}: vol-weight como pesos\_v2")) +
        "\\vspace{.3em}\n" +
        blk("Referência Histórica", r"""
Bridgewater All Weather (Ray Dalio) usa risk parity como filosofia central — alocar risco igualmente entre classes de ativos, não capital.""", "example")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{pesos\_equal\_weight(sinal)} $\to$ DataFrame de pesos iguais",
         r"\texttt{pesos\_vol\_weight(sinal, ret\_diarios)} $\to$ pesos inversos à vol",
         r"\texttt{pesos\_markowitz(sinal, ret\_mensais)} $\to$ pesos otimizados",
         r"\texttt{calcular\_turnover(pesos)} $\to$ Series de turnover mensal"],
        [r"\texttt{sinal\_v1.parquet}",
         r"\texttt{retornos\_diarios\_limpo.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{pesos\_v2.parquet} (vol-weight)",
         "Tabela comparativa de Sharpe e turnover"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Markowitz, H.} (1952). Portfolio Selection. \textit{Journal of Finance}, 7(1), 77--91.",
        r"\textbf{DeMiguel, V. et al.} (2009). Optimal versus naive diversification. \textit{Review of Financial Studies}, 22(5), 1915--1953.",
        r"\textbf{Ledoit, O. \& Wolf, M.} (2004). A well-conditioned estimator for large-dimensional covariance matrices. \textit{Journal of Multivariate Analysis}, 88(2), 365--411.",
        r"\textbf{Maillard, S. et al.} (2010). The properties of equally weighted risk contributions portfolios. \textit{JPM}, 36(4), 60--70.",
        r"\textbf{Michaud, R.} (1989). The Markowitz optimization enigma: is optimized optimal? \textit{FAJ}, 45(1), 31--42."
    ))

    p = pre("Aula 06 --- Alocação", "Estratégias de Alocação de Portfólio")
    save(doc(p, frames), "aula-06-alocacao", "slides-aula-06-alocacao.tex")


# ── Aula 07 — Sinal v2 ───────────────────────────────────────────────────────

def aula07():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (30 min)", its(
            "Limitação crítica do sinal v1: momentum crash",
            "Vol-adjusted momentum: Moskowitz, Ooi \\& Pedersen (2012)",
            "Comparação fair entre sinais: IC médio e Sharpe OOS",
            "Quando o ajuste de volatilidade ajuda (e quando não)")),
        blk("Código (70 min)", its(
            r"\texttt{calcular\_vol\_rolling(ret, janela=63)} — vol diária rolling",
            r"\texttt{calcular\_sinal\_v2(sinal\_v1, vol)} — sinal normalizado",
            "Comparação de IC: v1 vs v2 (bar chart)",
            "Backtest comparativo: equity curves lado a lado",
            r"Salvar \texttt{sinal\_v2.parquet} e \texttt{pesos\_v2\_final.parquet}"))
    ))

    frames += fr("Limitação do Sinal v1 — Momentum Crash", cols(
        r"""\textbf{Problema identificado por Daniel \& Moskowitz (2016):}
\vspace{.3em}
\begin{itemize}
  \item Em crises de mercado (2008, 2020), os ``vencedores'' do sinal v1 são tipicamente ativos de \textbf{alta beta}
  \item No crash, estes ativos caem mais que o mercado
  \item O sinal de momentum ``captura'' um risco de mercado latente
  \item Resultado: drawdown de 40--60\% em crises severas
\end{itemize}
\vspace{.3em}
\begin{alertblock}{Sinal 12-1 sem ajuste de vol}
  Compra ativos de alto retorno recente $\approx$ compra ativos de alta vol/beta.
  Em crises, isso amplifica as perdas.
\end{alertblock}""",
        blk("Solução: Vol-Adjustment", r"""
\textbf{Moskowitz, Ooi \& Pedersen (2012):}
\[
\text{Sinal}^{v2}_{i,t} = \frac{\text{Sinal}^{v1}_{i,t}}{\hat\sigma_{i,t}}
\]
$\hat\sigma_{i,t}$: volatilidade rolling dos últimos 63 dias úteis.
\vspace{.3em}
\begin{itemize}
  \item Normaliza o sinal pela volatilidade corrente
  \item Ativos mais voláteis recebem sinal ``deflacionado''
  \item Melhora IC e reduz tail risk
  \item Alinha com risk parity dos pesos
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Evidência", r"Moskowitz et al.\ documentam melhora de Sharpe em ações, bonds, commodities e moedas.", "example")
    ))

    frames += fr("Comparação Fair: v1 vs v2", cols(
        r"""\textbf{Protocolo de comparação:}
\begin{enumerate}
  \item Mesmo universo de ativos
  \item Mesmo período de análise
  \item Mesma regra de portfólio (top 20\%, equal-weight)
  \item Mesma modelagem de custos (turnover $\times$ 0{,}1\%)
\end{enumerate}
\vspace{.3em}
\textbf{Métricas de comparação:}
\begin{itemize}
  \item IC médio: poder preditivo bruto do sinal
  \item Sharpe ratio do portfólio
  \item Maximum drawdown
  \item Correlation entre sinal v1 e v2: quanto diferem?
\end{itemize}""",
        blk("Quando v2 ajuda?", its(
            r"Ambientes de alta volatilidade (crises, pandemia)",
            r"Quando os ``vencedores'' são concentrados em setores de alto beta",
            r"Quando há momentum crash latente (beta do portfólio > 1{,}2)")) +
        "\\vspace{.3em}\n" +
        blk("Quando v2 não ajuda?", its(
            r"Mercados trending com baixa dispersão de vol",
            r"Quando todos os ativos têm vol similar (correlação alta)",
            r"Períodos de vol muito baixa — normalização é instável"), "alerted")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{calcular\_vol\_rolling(ret\_diarios, janela=63)} $\to$ vol mensal estimada",
         r"\texttt{alinhar\_vol\_com\_sinal(vol, sinal)} $\to$ vol no mesmo index",
         r"\texttt{calcular\_sinal\_v2(sinal\_v1, vol)} $\to$ sinal normalizado",
         r"\texttt{comparar\_ic(sinal\_v1, sinal\_v2, ret)} $\to$ DataFrame comparativo"],
        [r"\texttt{sinal\_v1.parquet}",
         r"\texttt{retornos\_diarios\_limpo.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{sinal\_v2.parquet}",
         r"\texttt{pesos\_v2.parquet}",
         "Gráfico comparativo IS v1 vs v2"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Moskowitz, T., Ooi, Y. \& Pedersen, L.} (2012). Time series momentum. \textit{Journal of Financial Economics}, 104(2), 228--250.",
        r"\textbf{Daniel, K. \& Moskowitz, T.} (2016). Momentum crashes. \textit{JFE}, 122(2), 221--247.",
        r"\textbf{Barroso, P. \& Santa-Clara, P.} (2015). Momentum has its moments. \textit{JFE}, 116(1), 111--120.",
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1), 65--91.",
        r"\textbf{Asness, C. et al.} (2013). Value and momentum everywhere. \textit{Journal of Finance}, 68(3), 929--985."
    ))

    p = pre("Aula 07 --- Sinal v2", "Vol-Adjusted Momentum: Melhorando o Sinal")
    save(doc(p, frames), "aula-07-sinal-v2", "slides-aula-07-sinal-v2.tex")


# ── Aula 08 — Backtest Rigoroso ──────────────────────────────────────────────

def aula08():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (35 min)", its(
            "Os três grandes vieses em backtests",
            "Look-ahead bias: detecção e prevenção",
            "Multiple testing bias: Harvey, Liu \\& Zhu (2016)",
            "Walk-forward analysis: metodologia e implementação",
            "Deflated Sharpe Ratio (DSR): Bailey \\& López de Prado (2014)")),
        blk("Código (65 min)", its(
            r"\texttt{backtest\_walkforward()} — OOS puro",
            r"\texttt{calcular\_dsr()} — penalização por múltiplos testes",
            "Visualização: IS vs OOS, distribuição de retornos",
            r"Salvar \texttt{retorno\_walkforward\_liquido.parquet}"))
    ))

    frames += fr("Os Três Vieses do Backtest", cols(
        r"""\begin{block}{1. Look-ahead Bias}
Uso de informação futura na decisão de hoje.\\
\textbf{Exemplo}: usar $r_t$ para formar o sinal de $t$.\\
\textbf{Prevenção}: sempre \texttt{shift(1)} no backtest.
\end{block}
\vspace{.3em}
\begin{block}{2. Survivorship Bias}
Só analisa ativos que sobreviveram até hoje.\\
\textbf{Exemplo}: dataset com só as empresas que não faliram.\\
\textbf{Prevenção}: incluir composição histórica do índice.
\end{block}
\vspace{.3em}
\begin{alertblock}{3. Multiple Testing Bias}
Testar $N$ variações e reportar apenas a melhor.\\
Com $N=100$ e $\alpha=5\%$, esperam-se 5 falsos positivos por acaso.\\
\textbf{Correção}: ajuste de Bonferroni ou DSR.
\end{alertblock}""",
        blk("Harvey, Liu \\& Zhu (2016)", r"""
Analisaram $>$300 fatores publicados em finanças.\\
\vspace{.2em}
\textbf{Conclusão}: a maioria são \textbf{falsos positivos}.\\
O $t$-statistic mínimo aceitável evoluiu:
\begin{itemize}
  \item 1960s: $t > 2{,}0$ (Sharpe)
  \item 2000s: $t > 3{,}0$ (Harvey et al.)
  \item Hoje: DSR $> 0{,}95$ (López de Prado)
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Walk-Forward", r"""
Treina em janela rolling (36m), testa nos próximos 6m.
Cada retorno OOS foi gerado com parâmetros calculados \textbf{antes} do período de teste.""", "example")
    ))

    frames += fr("Deflated Sharpe Ratio", cols(
        r"""\textbf{Sharpe Ratio não ajustado:}
\[ \hat{S} = \frac{\overline{r}}{\hat\sigma}\,\sqrt{12} \]

\textbf{Deflated Sharpe Ratio (Bailey \& López de Prado, 2014):}
\[ \text{DSR} = \Phi\!\left(\frac{(\hat{S} - E[\max S]) \sqrt{T-1}}{\sqrt{1 - \hat\rho\,E[\max S] + \hat{S}^2\,(\hat\kappa-1)/4}}\right) \]

Onde $E[\max S]$ cresce com o número de estratégias testadas $N$:
\[ E[\max S] \approx \sqrt{2}\,\Phi^{-1}\!\!\left(1 - \frac{1}{N}\right) \]""",
        blk("Interpretação do DSR", its(
            r"$\text{DSR} \in [0, 1]$: probabilidade de que o resultado é genuíno",
            r"$\text{DSR} > 0{,}95$: robusto (nível de confiança 95\%)",
            r"$\text{DSR} < 0{,}5$: forte suspeita de overfitting",
            r"Penaliza por: número de testes, skewness e kurtosis dos retornos")) +
        "\\vspace{.3em}\n" +
        blk("Fórmula captura", its(
            r"Correção por não-normalidade ($\hat\gamma$, $\hat\kappa$)",
            r"Penalização por $N$ estratégias testadas",
            r"Incerteza estatística de $\hat{S}$ com $T$ observações"), "example")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{backtest\_walkforward(sinal, ret, treino=36, teste=6)} $\to$ ret OOS",
         r"\texttt{calcular\_dsr(retornos, n\_estrategias=5)} $\to$ dicionário de métricas",
         r"\texttt{plot\_is\_vs\_oos(ret\_is, ret\_oos)} $\to$ comparação visual"],
        [r"\texttt{sinal\_v2.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}",
         r"\texttt{retorno\_carteira.parquet}"],
        [r"\texttt{retorno\_walkforward\_liquido.parquet}",
         "Gráfico IS vs OOS",
         "Tabela DSR e métricas OOS"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{Journal of Portfolio Management}, 40(5).",
        r"\textbf{Harvey, C., Liu, Y. \& Zhu, H.} (2016). ... and the cross-section of expected returns. \textit{Review of Financial Studies}, 29(1), 5--68.",
        r"\textbf{López de Prado, M.} (2018). \textit{Advances in Financial Machine Learning}. Wiley.",
        r"\textbf{White, H.} (2000). A reality check for data snooping. \textit{Econometrica}, 68(5), 1097--1126.",
        r"\textbf{Romano, J. \& Wolf, M.} (2005). Stepwise multiple testing as formalized data snooping. \textit{Econometrica}, 73(4), 1237--1282."
    ))

    p = pre("Aula 08 --- Backtest Rigoroso", "Walk-Forward, DSR e Validação Estatística")
    save(doc(p, frames), "aula-08-backtest-rigoroso", "slides-aula-08-backtest-rigoroso.tex")


# ── Aula 09 — GenAI ──────────────────────────────────────────────────────────

def aula09():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (25 min)", its(
            "LLMs no contexto de finanças quantitativas",
            "Anatomia de uma API de LLM: messages, tokens, temperature",
            "Prompt engineering para análise financeira",
            "Casos de uso: sentiment, narrativa, assistência a código")),
        blk("Código (75 min)", its(
            r"Setup: \texttt{anthropic} SDK, API key segura",
            r"\texttt{chamar\_claude(prompt, system)} — wrapper genérico",
            r"\texttt{gerar\_comentario\_performance()} — narrativa institucional",
            r"\texttt{sugerir\_melhorias()} — pesquisa assistida por LLM",
            "Salvar narrativa em .txt para o relatório"))
    ))

    frames += fr("LLMs no Contexto Quant", cols(
        its(r"\textbf{Análise de Sentimento}: processar earnings calls, atas do COPOM, releases — extrair score de sentimento com LLM",
            r"\textbf{Geração de Narrativa}: dado Sharpe, MDD, IC $\Rightarrow$ comentário de performance no estilo gestora institucional",
            r"\textbf{Assistência a Código}: descrever sinal em linguagem natural, LLM propõe implementação em Python",
            r"\textbf{Pesquisa Assistida}: perguntar sobre literatura acadêmica, LLM cita papers e mecanismos relevantes"),
        blk("Modelos Anthropic", its(
            r"\textbf{Claude Haiku}: rápido, barato — experimentação",
            r"\textbf{Claude Sonnet}: balanceado — produção",
            r"\textbf{Claude Opus}: máxima capacidade — análises complexas")) +
        "\\vspace{.3em}\n" +
        blk("Limitações importantes", its(
            r"LLM não acessa internet nem dados em tempo real",
            r"Alucinações: sempre verifique citações e números",
            r"Contexto de treinamento: conhecimento até data de corte",
            r"Custo por token: dimensione prompts com cuidado"), "alerted")
    ))

    frames += fr("Prompt Engineering Financeiro", cols(
        r"""\textbf{Prompt ruim:}
\begin{lstlisting}
"Analise minha estrategia."
\end{lstlisting}
\vspace{.2em}
\textbf{Prompt bom (estrutura completa):}
\begin{lstlisting}
system = '''Voce e um analista quantitativo
senior de uma gestora brasileira.
Estilo: tecnico, formal, preciso.
Tamanho: 200-250 palavras.'''

user = f'''Estrategia: momentum cross-sectional IBOVESPA.
Sharpe OOS: {sharpe:.2f}
CAGR: {cagr:.1%}
Max Drawdown: {mdd:.1%}
Escreva comentario de performance.'''
\end{lstlisting}""",
        blk("Boas práticas", its(
            r"System prompt: define personalidade e formato",
            r"User prompt: dados concretos + instrução específica",
            r"Temperature $\approx 0$: respostas determinísticas para números",
            r"Temperature $\approx 0{,}3$: mais criatividade para narrativa",
            r"few-shot: inclua 1--2 exemplos do formato desejado")) +
        "\\vspace{.3em}\n" +
        blk("Segurança", r"Nunca inclua API key no código. Use variável de ambiente: \texttt{ANTHROPIC\_API\_KEY}. Nunca suba \texttt{.env} para o GitHub.", "alerted")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{chamar\_claude(prompt, system, modelo, temp)} $\to$ str",
         r"\texttt{resumo\_metricas(ret, nome)} $\to$ dicionário formatado",
         r"\texttt{gerar\_comentario\_performance(m\_is, m\_oos)} $\to$ texto",
         r"\texttt{sugerir\_melhorias(m\_oos)} $\to$ sugestões da literatura"],
        [r"\texttt{retorno\_carteira.parquet}",
         r"\texttt{retorno\_walkforward\_liquido.parquet}",
         "API key da Anthropic configurada"],
        [r"\texttt{narrativa\_performance.txt}",
         "Sugestões de melhoria baseadas em literatura"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Brown, T. et al.} (2020). Language models are few-shot learners (GPT-3). \textit{NeurIPS}.",
        r"\textbf{Anthropic} (2024). Claude model card. \textit{anthropic.com}.",
        r"\textbf{Wei, J. et al.} (2022). Chain-of-thought prompting elicits reasoning. \textit{NeurIPS}.",
        r"\textbf{Lopez-Lira, A. \& Tang, Y.} (2023). Can ChatGPT forecast stock price movements? \textit{SSRN}.",
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1), 65--91."
    ))

    p = pre("Aula 09 --- GenAI", "LLMs e a API Claude no Pipeline Quantitativo")
    save(doc(p, frames), "aula-09-genai", "slides-aula-09-genai.tex")


# ── Aula 10 — Relatório e Defesa ─────────────────────────────────────────────

def aula10():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (20 min)", its(
            "Estrutura do relatório técnico para o Desafio Itaú",
            "Quatro dimensões avaliadas pelos juízes",
            "Como defender sob pressão: perguntas difíceis",
            "Erros comuns a evitar")),
        blk("Código (80 min)", its(
            r"\texttt{painel\_relatorio\_final()} — figura principal com 4 subplots",
            r"\texttt{analise\_sensibilidade()} — lookback e n\_long\_pct",
            r"\texttt{ic\_temporal()} — IC mensal e rolling 12m",
            "Montar todos os resultados em estrutura de relatório",
            "Simulação de defesa: perguntas e respostas"))
    ))

    frames += fr("Estrutura do Relatório Final", cols(
        its(r"\textbf{1. Sumário Executivo} (1 pág.): hipótese, metodologia, resultado principal, limitações",
            r"\textbf{2. Dados e Universo}: fonte, período, limpeza, survivorship bias",
            r"\textbf{3. Metodologia}: sinal (fórmula + código), portfólio, backtest, rigor OOS",
            r"\textbf{4. Resultados}: tabela IS/OOS, equity curve, IC, DSR",
            r"\textbf{5. Sensibilidade}: variação de lookback e tamanho do portfólio",
            r"\textbf{6. Limitações e Trabalhos Futuros}: honestidade sobre lacunas",
            r"\textbf{7. Referências}: papers completos (APA ou ABNT)"),
        blk("Critérios dos Juízes", its(
            r"\textbf{Rigor metodológico}: walk-forward, shift(1), sem look-ahead",
            r"\textbf{Fundamentação econômica}: por que momentum funciona?",
            r"\textbf{Qualidade do código}: reprodutível, versionado no GitHub",
            r"\textbf{Comunicação}: proporcional à evidência, limitações declaradas")) +
        "\\vspace{.3em}\n" +
        blk("Regra de ouro", r"Um resultado honesto com limitações bem articuladas vale mais que um resultado inflado com lacunas escondidas.", "alerted")
    ))

    frames += fr("Pipeline Completo — Resumo", r"""
\begin{center}
\begin{tikzpicture}[node distance=.55cm and .3cm,
  box/.style={draw=navy,fill=navy!8,rounded corners=3pt,
              text width=1.55cm,align=center,font=\tiny\bfseries,inner sep=3pt},
  lbl/.style={font=\tiny,gold},
  arr/.style={-Stealth,navy,thick}]
  \node[box](d){Dados\\yfinance};
  \node[box,right=of d](e){EDA\\análise};
  \node[box,right=of e](s1){Sinal v1\\12-1};
  \node[box,right=of s1](s2){Sinal v2\\vol-adj};
  \node[box,right=of s2](p){Portfólio\\top 20\%};
  \node[box,right=of p](b){Backtest\\IS};
  \node[box,right=of b](v){WF-OOS\\DSR};
  \node[box,right=of v](g){GenAI\\narrativa};
  \node[box,right=of g](r){Relatório\\defesa};

  \draw[arr](d)--(e);\draw[arr](e)--(s1);\draw[arr](s1)--(s2);
  \draw[arr](s2)--(p);\draw[arr](p)--(b);\draw[arr](b)--(v);
  \draw[arr](v)--(g);\draw[arr](g)--(r);

  \node[lbl,below=.3cm of d]{Aula 2};
  \node[lbl,below=.3cm of e]{Aula 3};
  \node[lbl,below=.3cm of s1]{Aula 4};
  \node[lbl,below=.3cm of s2]{Aula 7};
  \node[lbl,below=.3cm of p]{Aulas 5-6};
  \node[lbl,below=.3cm of b]{Aula 5};
  \node[lbl,below=.3cm of v]{Aula 8};
  \node[lbl,below=.3cm of g]{Aula 9};
  \node[lbl,below=.3cm of r]{Aula 10};
\end{tikzpicture}
\end{center}
\vspace{.2em}
\begin{columns}[T]
  \column{0.48\textwidth}
  \begin{block}{Parquets produzidos}
    \texttt{precos\_ibov} $\cdot$ \texttt{ret\_diarios\_limpo} $\cdot$ \texttt{ret\_mensais\_limpo}\\
    \texttt{sinal\_v1} $\cdot$ \texttt{sinal\_v2} $\cdot$ \texttt{pesos\_v1} $\cdot$ \texttt{pesos\_v2}\\
    \texttt{retorno\_carteira} $\cdot$ \texttt{retorno\_walkforward\_liquido}
  \end{block}
  \column{0.48\textwidth}
  \begin{exampleblock}{Entregáveis do Desafio}
    Relatório PDF $\cdot$ Código no GitHub\\
    Apresentação 10 min + 5 min Q\&A\\
    Notebook reprodutível do zero
  \end{exampleblock}
\end{columns}""")

    frames += fr("Como Defender — Perguntas Difíceis", cols(
        blk("Pergunta 1", r"""
\textit{``Seu Sharpe é atribuível ao momentum ou ao beta de mercado?''}\\[.3em]
\textbf{Resposta}: Compare correlação da carteira com IBOVESPA. Mostre alpha de Jensen $\alpha = r_p - \beta\,r_m$.
""") +
        "\\vspace{.3em}\n" +
        blk("Pergunta 2", r"""
\textit{``Como controlaram survivorship bias?''}\\[.3em]
\textbf{Resposta}: Declarar como limitação. Explicar que yfinance com histórico minimiza, mas não elimina. Citar na seção 6.
""") +
        "\\vspace{.3em}\n" +
        blk("Pergunta 3", r"""
\textit{``Por que equal-weight e não Markowitz?''}\\[.3em]
\textbf{Resposta}: DeMiguel et al.\ (2009) — 1/N vence Markowitz OOS. Mostrar tabela de Sharpe comparativo.
"""),
        blk("Regras da Defesa", its(
            r"Nunca finja saber o que não sabe",
            r"\textit{``Boa pergunta, não testamos, mas hipotetizamos que...''} é melhor que erro com confiança",
            r"Cite papers para todo claim quantitativo",
            r"Mostre os gráficos — visuais vencem palavras",
            r"Declare limitações antes de te perguntarem")) +
        "\\vspace{.3em}\n" +
        blk("Encerramento", r"""
Em 10 semanas: dados reais, sinal acadêmico, backtest rigoroso, validação OOS, GenAI.
\textbf{Façam bonito no Desafio!}""", "example")
    ))

    frames += fr("Referências — Pipeline Completo", refs(
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1).",
        r"\textbf{Moskowitz, T. et al.} (2012). Time series momentum. \textit{JFE}, 104(2), 228--250.",
        r"\textbf{Fama, E. \& French, K.} (1993). Common risk factors. \textit{JFE}, 33(1), 3--56.",
        r"\textbf{DeMiguel, V. et al.} (2009). Optimal versus naive diversification. \textit{RFS}, 22(5).",
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{JPM}, 40(5).",
        r"\textbf{Harvey, C. et al.} (2016). Cross-section of expected returns. \textit{RFS}, 29(1).",
        r"\textbf{López de Prado, M.} (2018). \textit{Advances in Financial Machine Learning}. Wiley.",
        r"\textbf{Daniel, K. \& Moskowitz, T.} (2016). Momentum crashes. \textit{JFE}, 122(2).",
        r"\textbf{Cont, R.} (2001). Empirical properties of asset returns. \textit{Quantitative Finance}, 1(2).",
        r"\textbf{Markowitz, H.} (1952). Portfolio Selection. \textit{Journal of Finance}, 7(1)."
    ))

    p = pre("Aula 10 --- Relatório e Defesa",
            "Relatório Final, Análise de Sensibilidade e Simulação de Defesa")
    save(doc(p, frames), "aula-10-relatorio-defesa", "slides-aula-10-relatorio-defesa.tex")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Gerando LaTeX Aulas 02-10...")
    aula02(); aula03(); aula04(); aula05()
    aula06(); aula07(); aula08(); aula09(); aula10()
    print("Concluido!")
