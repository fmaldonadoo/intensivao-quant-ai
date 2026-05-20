#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera slides LaTeX Beamer para Aulas 02–09 do Intensivão Quant AI.
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
\date{Intensivão Quant AI 2026}
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
        blk("Teoria (20 min)", its(
            "O universo IBOVESPA: composição e rebalanceamento",
            "Pipeline de dados: da fonte ao parquet",
            "Tratamento de outliers e dados faltantes",
            "Retornos compostos vs simples")),
        blk("Código (40 min)", its(
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
            r"Período de análise: 2012--2024 (12 anos)"),
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
        blk("Teoria (20 min)", its(
            "Distribuições de retorno: normalidade vs fat tails",
            "Skewness, kurtosis e o Teorema do Limite Central",
            "Correlações: estáticas e rolling",
            "Estacionaridade e o teste ADF")),
        blk("Código (40 min)", its(
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
        blk("Teoria (20 min)", its(
            "O pipeline quant de geração de alfa",
            "Anatomia do sinal 12-1 de momentum",
            "Information Coefficient (IC): o que é e por que importa",
            "IC ratio e IR: avaliando poder preditivo")),
        blk("Código (40 min)", its(
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
Comprar \textbf{top 10\%} (quintil superior).\\
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
        blk("Teoria (20 min)", its(
            "Hipóteses do backtest: o que estamos testando?",
            "Métricas de performance: Sharpe, Sortino, MDD, Calmar",
            "O problema do look-ahead bias: shift(1)",
            "A importância de usar pesos realistas")),
        blk("Código (40 min)", its(
            r"\texttt{construir\_portfolio()} — top 10\%, weights.shift(1)",
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
            r"Sharpe $> 1{,}0$: excelente (difícil na realidade brasileira)",
            r"Sharpe $> 0{,}5$: bom para estratégias long-only no IBOV",
            r"MDD $< 20\%$: confortável para a maioria das gestoras",
            r"Calmar $> 0{,}5$: relação risco/retorno aceitável")) +
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
        blk("Hipóteses do backtest", its(
            "Execução ao preço de fechamento do mês",
            "Liquidez infinita (sem market impact inicial)",
            "Sem short: long-only com equal-weight no top 10\\%",
            "Benchmark: IBOVESPA (BOVA11)"), "alerted")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{construir\_portfolio(sinal, ret, n\_pct=0.1)} $\to$ retornos da carteira",
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
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{JPM}, 40(5)."
    ))

    p = pre("Aula 05 --- Backtest v1", "Construindo e Avaliando o Primeiro Backtest")
    save(doc(p, frames), "aula-05-backtest-v1", "slides-aula-05-backtest-v1.tex")


# ── Aula 06 — Alocação — Markowitz ───────────────────────────────────────────

def aula06():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (20 min)", its(
            "Teoria Moderna de Portfólio (Markowitz 1952)",
            "O trade-off risco-retorno e fronteira eficiente",
            "Por que a otimização de Markowitz clássica é instável na prática",
            "A importância de restrições rígidas (long-only, caps)")),
        blk("Código (40 min)", its(
            r"\texttt{pesos\_equal\_weight()} — robustez do benchmark 1/N",
            r"\texttt{pesos\_markowitz()} — otimização com scipy.optimize",
            "Configurar função objetivo (max Sharpe) e restrições",
            "Comparação de turnover e Sharpe de Markowitz vs. EW",
            r"Salvar \texttt{pesos\_markowitz.parquet}"))
    ))

    frames += fr("Equal-Weight vs Markowitz", cols(
        blk(r"DeMiguel et al.\ (2009)", r"""
\textit{Optimal versus naive diversification: how inefficient is the 1/N portfolio strategy?}
\vspace{.3em}
\begin{itemize}
  \item O portfólio 1/N (Equal-Weight) é um benchmark fortíssimo
  \item Otimização clássica sofre com erro de estimação dos parâmetros ($\boldsymbol{\mu}, \boldsymbol{\Sigma}$)
  \item Sem restrições, Markowitz gera pesos extremos e instáveis out-of-sample
  \item Solução prática: impor restrições long-only e limites máximos por ativo (caps)
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Restrições no scipy.optimize", r"Impedir short selling ($w_i \in [0, 0.20]$) e forçar a soma dos pesos a ser exatamente $1$. Isso estabiliza os pesos.", "alerted"),
        r"""
\textbf{Problema de Markowitz (Sharpe Máx.):}
\[
\max_{\mathbf{w}}\; \frac{\mathbf{w}^\top\boldsymbol{\mu} - r_f}{\sqrt{\mathbf{w}^\top\boldsymbol{\Sigma}\mathbf{w}}}
\]
\vspace{.1em}
\textbf{Com as Restrições:}
\[
\sum_{i=1}^N w_i = 1 \quad \text{e} \quad 0 \leq w_i \leq 0{,}20
\]

\vspace{.3em}
\begin{exampleblock}{Estimativa de Risco}
Usamos a matriz de covariância histórica dos retornos mensais do portfólio selecionado para a otimização.
\end{exampleblock}"""
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{pesos\_equal\_weight(sinal)} $\to$ DataFrame de pesos iguais",
         r"\texttt{pesos\_markowitz(sinal, ret\_mensais)} $\to$ pesos otimizados (Sharpe Máx.)",
         r"\texttt{calcular\_turnover(pesos)} $\to$ Series de turnover mensal"],
        [r"\texttt{sinal\_v1.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{pesos\_markowitz.parquet}",
         "Tabela comparativa de Sharpe e turnover: Markowitz vs EW"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Markowitz, H.} (1952). Portfolio Selection. \textit{Journal of Finance}, 7(1), 77--91.",
        r"\textbf{DeMiguel, V. et al.} (2009). Optimal versus naive diversification. \textit{Review of Financial Studies}, 22(5), 1915--1953.",
        r"\textbf{Ledoit, O. \& Wolf, M.} (2004). Honey, I shrunk the covariance matrix. \textit{JPM}.",
        r"\textbf{Michaud, R.} (1989). The Markowitz optimization enigma: is optimized optimal? \textit{FAJ}, 45(1), 31--42."
    ))

    p = pre("Aula 06 --- Alocação", "Alocação Clássica vs Otimizada (Markowitz)")
    save(doc(p, frames), "aula-06-alocacao", "slides-aula-06-alocacao.tex")


# ── Aula 07 — Sinal v2 ───────────────────────────────────────────────────────

def aula07():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (20 min)", its(
            "Limitação crítica do sinal v1: momentum crash",
            "Vol-adjusted momentum: Moskowitz, Ooi \\& Pedersen (2012)",
            "Comparação justa entre sinais: IC médio e Sharpe",
            "Por que normalizar por volatilidade reduz tail risk")),
        blk("Código (40 min)", its(
            r"\texttt{calcular\_vol\_rolling()} — volatilidade de 63 dias úteis",
            r"\texttt{calcular\_sinal\_v2()} — normalização do sinal pela vol",
            "Comparação de IC: v1 vs v2 (rolling e médio)",
            "Backtest comparativo: equity curves lado a lado",
            r"Salvar \texttt{sinal\_v2.parquet}"))
    ))

    frames += fr("Limitação do Sinal v1 — Momentum Crash", cols(
        r"""\textbf{O fenômeno do Momentum Crash:}
\vspace{.3em}
\begin{itemize}
  \item Em pânicos de mercado, o momentum seleciona ações de \textbf{alto beta} (que caíram muito ou subiram muito de forma volátil)
  \item Na recuperação pós-crise, os perdedores de alto beta disparam, e os \"vencedores\" defensivos sobem menos ou caem
  \item Momentum v1 sofre perdas severas em viradas rápidas de regime (drawdowns de 40-60\%)
\end{itemize}
\vspace{.3em}
\begin{alertblock}{Solução de Normalização}
  Dividir o sinal pela volatilidade rolling de 63 dias úteis remove o viés de alto beta e estabiliza a exposição ao fator de momentum.
\end{alertblock}""",
        blk("Vol-Adjustment", r"""
\textbf{Moskowitz, Ooi \& Pedersen (2012):}
\[
\text{Sinal}^{v2}_{i,t} = \frac{\text{Sinal}^{v1}_{i,t}}{\hat\sigma_{i,t}}
\]
$\hat\sigma_{i,t}$: volatilidade rolling dos últimos 63 dias úteis.
\vspace{.3em}
\begin{itemize}
  \item Normaliza o sinal pela volatilidade corrente
  \item Ativos mais voláteis recebem sinal ``deflacionado''
  \item Melhora substancial do IC ajustado a risco
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Evidência", r"Moskowitz et al.\ documentam melhora robusta de Sharpe em múltiplas classes de ativos.", "example")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{calcular\_vol\_rolling(ret\_diarios, janela=63)} $\to$ vol rolling diária",
         r"\texttt{calcular\_sinal\_v2(sinal\_v1, vol)} $\to$ sinal normalizado",
         r"\texttt{comparar\_ic(sinal\_v1, sinal\_v2, ret)} $\to$ DataFrame de Spearman IC"],
        [r"\texttt{sinal\_v1.parquet}",
         r"\texttt{retornos\_diarios\_limpo.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{sinal\_v2.parquet}",
         r"\texttt{pesos\_v2.parquet}",
         "Gráfico comparativo de performance v1 vs v2"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Moskowitz, T., Ooi, Y. \& Pedersen, L.} (2012). Time series momentum. \textit{Journal of Financial Economics}, 104(2), 228--250.",
        r"\textbf{Daniel, K. \& Moskowitz, T.} (2016). Momentum crashes. \textit{JFE}, 122(2), 221--247.",
        r"\textbf{Barroso, P. \& Santa-Clara, P.} (2015). Momentum has its moments. \textit{JFE}, 116(1), 111--120.",
        r"\textbf{Asness, C. et al.} (2013). Value and momentum everywhere. \textit{Journal of Finance}, 68(3), 929--985."
    ))

    p = pre("Aula 07 --- Sinal v2", "Vol-Adjusted Momentum: Mitigando Momentum Crashes")
    save(doc(p, frames), "aula-07-sinal-v2", "slides-aula-07-sinal-v2.tex")


# ── Aula 08 — Backtest Rigoroso ──────────────────────────────────────────────

def aula08():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (20 min)", its(
            "Os três grandes vieses: look-ahead, survivorship, multiple testing",
            "Rotação de carteira (Turnover) e custos reais de transação",
            "Por que os custos de transação devoram estratégias quantitativas",
            "A metodologia walk-forward (Out-of-Sample pura)")),
        blk("Código (40 min)", its(
            r"\texttt{calcular\_turnover()} — turnover mensal da carteira",
            r"\texttt{aplicar\_custos()} — implementar custos reais de transação (0.3\%)",
            "Simular curva líquida e comparar com a curva bruta",
            "Avaliar o impacto do rebalanceamento frequente no Sharpe",
            r"Salvar \texttt{retorno\_walkforward\_liquido.parquet}"))
    ))

    frames += fr("Rigor Máximo: Custos e Turnover", cols(
        r"""\textbf{O perigo mortal dos custos:}
\vspace{.3em}
\begin{itemize}
  \item Estratégias quantitativas (especialmente momentum) têm alto giro (turnover)
  \item Ignorar corretagem, taxas B3, e slippage gera um backtest fantasioso
  \item Usamos um drag realista de **0.3% por transação** (compra/venda)
\end{itemize}
\vspace{.3em}
\begin{block}{Definição de Turnover Mensal}
\[
\text{Turnover}_t = \frac{1}{2} \sum_{i=1}^N |w_{i,t} - w_{i,t-1}^+|
\]
onde $w_{i,t-1}^+$ é o peso no fim do mês devido à variação de preços.
\end{block}""",
        blk("Metodologia Walk-Forward", r"""
Para simular a performance out-of-sample real:
\begin{itemize}
  \item Dividimos o histórico em blocos de treino (48m) e teste (12m)
  \item Os parâmetros de alocação/vol são estimados *apenas* no treino e aplicados no teste
  \item Garante que o Sharpe reportado não é fruto de overfitting de parâmetros
\end{itemize}""") +
        "\\vspace{.3em}\n" +
        blk("Regra dos 3 Vieses", r"Sempre shift(2) no sinal, shift(1) nos pesos, custos no turnover e histórico com constituintes corretos.", "alerted")
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{calcular\_turnover(pesos)} $\to$ Series de turnover mensal",
         r"\texttt{simular\_backtest\_liquido(ret, pesos, custo=0.003)} $\to$ retornos líquidos",
         r"\texttt{backtest\_walkforward(sinal, ret)} $\to$ retornos walk-forward"],
        [r"\texttt{sinal\_v2.parquet}",
         r"\texttt{pesos\_v2.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}"],
        [r"\texttt{retorno\_walkforward\_liquido.parquet}",
         "Gráfico comparativo Bruto vs Líquido de Custos"]
    ))

    frames += fr("Referências", refs(
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{JPM}, 40(5).",
        r"\textbf{Harvey, C., Liu, Y. \& Zhu, H.} (2016). ... and the cross-section of expected returns. \textit{RFS}, 29(1), 5--68.",
        r"\textbf{López de Prado, M.} (2018). \textit{Advances in Financial Machine Learning}. Wiley.",
        r"\textbf{Korajczyk, R. \& Sadka, R.} (2004). Are momentum profits robust to trading costs? \textit{Journal of Finance}, 59(3)."
    ))

    p = pre("Aula 08 --- Backtest Rigoroso", "Walk-Forward, Custos e Simulação Realista")
    save(doc(p, frames), "aula-08-backtest-rigoroso", "slides-aula-08-backtest-rigoroso.tex")


# ── Aula 09 — GenAI, Relatório & Defesa ──────────────────────────────────────

def aula09():
    frames = "\\begin{frame}[plain]\n\\titlepage\n\\end{frame}\n\n"

    frames += fr("Nesta Aula", cols(
        blk("Teoria (20 min)", its(
            "Onde GenAI (LLMs) se encaixa de forma prática no pipeline quant",
            "Como redigir prompts estruturados para análise técnica do Claude",
            "Os 7 critérios de avaliação da banca do Itaú Asset",
            "A estrutura do relatório final e regras da defesa oral")),
        blk("Código (40 min)", its(
            r"Setup: wrappers para a API do Claude (\texttt{anthropic} SDK)",
            r"\texttt{gerar\_draft\_secao()} — automatizar seções via LLM",
            r"\texttt{painel\_tear\_sheet()} — figura consolidada de 5 painéis",
            "Geração automática do rascunho em markdown",
            "Simulação da banca de defesa oral com IA"))
    ))

    frames += fr("LLMs no Pipeline Quantitativo", cols(
        its(r"\textbf{Análise de Resultados}: LLM recebe Sharpe, MDD e volatilidade, interpretando regimes de risco e gerando comentários.",
            r"\textbf{Redação Estruturada}: Geração rápida do Sumário Executivo, Metodologia (LaTeX) e Limitações técnicas.",
            r"\textbf{Revisão Crítica}: Atuar como advogado do diabo, questionando fragilidades no nosso próprio backtest.",
            r"\textbf{Preparação da Defesa}: Simular perguntas difíceis da banca da Itaú Asset."),
        blk("Boas Práticas de Prompt", its(
            r"Use System Prompts claros (defina persona de analista sênior)",
            r"Passe dados estruturados (não mande 'analisar minha estratégia', passe a tabela)",
            r"Peça Chain of Thought (ex: 'raciocine sobre regimes de mercado antes de concluir')",
            r"Configure temperature baixa para dados numéricos precisos")) +
        "\\vspace{.2em}\n" +
        blk("Segurança e API Keys", r"Nunca insira chaves no código. Use variáveis de ambiente (\texttt{ANTHROPIC\_API\_KEY}) e suba apenas o build.", "alerted")
    ))

    frames += fr("Os 7 Critérios da Banca do Itaú", cols(
        its(r"\textbf{1. Conceito da Estratégia (20\%)}: Tese econômica clara (underreaction comportamental, Jegadeesh \& Titman).",
            r"\textbf{2. Modelagem (20\%)}: Justificativa dos parâmetros, tratamento de outliers e Markowitz caps.",
            r"\textbf{3. Uso de GenAI (15\%)}: Claude usado para análise qualitativa, redação e críticas do relatório.",
            r"\textbf{4. Backtest (15\%)}: Sem look-ahead bias, weights.shift(1), custos realistas (0.3\%) e walk-forward.",
            r"\textbf{5. Análise de Resultados (15\%)}: Sharpe, MDD, Calmar, Alpha/Beta vs IBOVESPA.",
            r"\textbf{6. Conclusão e Próximos Passos (10\%)}: Limitações quantificadas de forma madura.",
            r"\textbf{7. Apresentação (5\%)}: Identidade e clareza."),
        blk("Regra de Ouro", r"O rigor técnico e a honestidade intelectual sobre as limitações do backtest contam muito mais para a banca do Itaú do que o retorno absoluto.", "alerted")
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
  \node[box,right=of s2](p){Portfólio\\Markowitz};
  \node[box,right=of p](b){Backtest\\EW vs MW};
  \node[box,right=of b](v){WF-OOS\\Custos 0.3\%};
  \node[box,right=of v](g){GenAI\\Claude};
  \node[box,right=of g](r){Relatório\\Defesa};

  \draw[arr](d)--(e);\draw[arr](e)--(s1);\draw[arr](s1)--(s2);
  \draw[arr](s2)--(p);\draw[arr](p)--(b);\draw[arr](b)--(v);
  \draw[arr](v)--(g);\draw[arr](g)--(r);

  \node[lbl,below=.3cm of d]{Aula 2};
  \node[lbl,below=.3cm of e]{Aula 3};
  \node[lbl,below=.3cm of s1]{Aula 4};
  \node[lbl,below=.3cm of s2]{Aula 7};
  \node[lbl,below=.3cm of p]{Aula 6};
  \node[lbl,below=.3cm of b]{Aulas 5-6};
  \node[lbl,below=.3cm of v]{Aula 8};
  \node[lbl,below=.3cm of g]{Aula 9};
  \node[lbl,below=.3cm of r]{Aula 9};
\end{tikzpicture}
\end{center}
\vspace{.2em}
\begin{columns}[T]
  \column{0.48\textwidth}
  \begin{block}{Entregáveis da nossa estratégia}
    \texttt{precos\_ibov} $\cdot$ \texttt{sinal\_v2} $\cdot$ \texttt{pesos\_markowitz}\\
    \texttt{retorno\_walkforward\_liquido} $\cdot$ \texttt{tearsheet\_final.png}
  \end{block}
  \column{0.48\textwidth}
  \begin{exampleblock}{Dica para a Defesa}
    Apresente as limitações (como survivorship bias) antes que a banca pergunte. Isso demonstra maturidade acadêmica e prática.
  \end{exampleblock}
\end{columns}""")

    frames += fr("Como Defender — Perguntas Difíceis", cols(
        blk("Janela 12-1 e Parâmetros", r"""
\textit{``Por que 12-1 e não outra janela?''}\\[.3em]
\textbf{Defesa}: Fixamos o parâmetro baseados na literatura de Jegadeesh \& Titman (1993) antes de ver os dados para evitar overfitting de parâmetros.
""") + "\n\\vspace{.2em}\n" +
        blk("Equal-Weight vs Otimizado", r"""
\textit{``Por que usar Equal-Weight ou Markowitz restrito?''}\\[.3em]
\textbf{Defesa}: Otimização pura é instável devido a erros de estimação. Impor restrições de peso ($w_i \in [0, 0.20]$) nos protege contra pesos extremos.
"""),
        blk("Regras da Apresentação", its(
            r"Nunca invente dados: admita o que não sabe",
            r"Foque nos gráficos: a imagem da Tear Sheet final conta a história inteira",
            r"Cuidado com o turnover: demonstre que a estratégia sobrevive à fricção de transação"))
    ))

    frames += fr("O que Vamos Construir", construir(
        [r"\texttt{chamar\_claude(prompt, system)} $\to$ chamada Anthropic",
         r"\texttt{painel\_tear\_sheet(ret\_wf, ret\_ibov)} $\to$ Tearsheet PNG",
         r"\texttt{gerar\_relatorio\_completo()} $\to$ exportar draft markdown"],
        [r"\texttt{retorno\_walkforward\_liquido.parquet}",
         r"\texttt{retornos\_mensais\_limpo.parquet}",
         "API key da Anthropic"],
        [r"\texttt{relatorio\_final\_draft.md}",
         r"\texttt{tearsheet\_final.png}"]
    ))

    frames += fr("Referências — Pipeline Completo", refs(
        r"\textbf{Jegadeesh, N. \& Titman, S.} (1993). Returns to buying winners. \textit{Journal of Finance}, 48(1).",
        r"\textbf{Moskowitz, T. et al.} (2012). Time series momentum. \textit{JFE}, 104(2), 228--250.",
        r"\textbf{DeMiguel, V. et al.} (2009). Optimal versus naive diversification. \textit{RFS}, 22(5).",
        r"\textbf{Bailey, D. \& López de Prado, M.} (2014). The deflated Sharpe ratio. \textit{JPM}, 40(5).",
        r"\textbf{Daniel, K. \& Moskowitz, T.} (2016). Momentum crashes. \textit{JFE}, 122(2).",
        r"\textbf{Markowitz, H.} (1952). Portfolio Selection. \textit{Journal of Finance}, 7(1)."
    ))

    p = pre("Aula 09 --- GenAI, Relatório \& Defesa", "LLMs, Geração de Relatório e Simulado de Defesa")
    save(doc(p, frames), "aula-09-genai-relatorio", "slides-aula-09-genai-relatorio.tex")


# ── main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("Gerando LaTeX Aulas 02-09...")
    aula02(); aula03(); aula04(); aula05()
    aula06(); aula07(); aula08(); aula09()
    print("Concluido!")
