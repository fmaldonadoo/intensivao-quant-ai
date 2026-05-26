# -*- coding: utf-8 -*-
import sys, io
# Força UTF-8 no stdout/stderr para evitar UnicodeEncodeError no Windows (cp1252)
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    sys.stderr.reconfigure(encoding='utf-8', errors='replace')
elif sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

"""
╔══════════════════════════════════════════════════════════════════════════════╗
║          INTENSIVÃO QUANT AI — CÓDIGO CONSOLIDADO DO PROJETO               ║
║          Impact UFSCAR · Diretoria de Quant · 2025                         ║
╠══════════════════════════════════════════════════════════════════════════════╣
║  Contém todo o pipeline da estratégia de momentum cross-sectional:          ║
║                                                                              ║
║   1. Setup do ambiente (VS Code / Google Colab)                              ║
║   2. Download e limpeza de dados (IBOVESPA via yfinance)                     ║
║   3. EDA: distribuições, correlações, estacionaridade                        ║
║   4. Sinal v1: momentum 12-1 + IC (Information Coefficient)                 ║
║   5. Backtest v1: métricas, equity curve, tearsheet                          ║
║   6. Alocação: equal-weight, vol-weight, Markowitz restrito                  ║
║   7. Sinal v2: vol-adjusted momentum (Moskowitz et al. 2012)                 ║
║   8. Backtest rigoroso: walk-forward OOS + Deflated Sharpe Ratio             ║
║   9. GenAI: narrativa de performance via API Anthropic                       ║
║                                                                              ║
║  Como usar:                                                                  ║
║    - Execute main() para rodar o pipeline completo                           ║
║    - Ou importe e chame cada função individualmente                          ║
║    - Configure DADOS_DIR antes de começar (veja Seção 0)                    ║
╚══════════════════════════════════════════════════════════════════════════════╝

Referências:
  Markowitz (1952) · Fama (1970) · Jegadeesh & Titman (1993)
  Fama & French (1993) · DeMiguel et al. (2009) · Moskowitz et al. (2012)
  Bailey & López de Prado (2014) · Harvey, Liu & Zhu (2016)
  López de Prado (2018)
"""

# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 0 — SETUP DO AMBIENTE (VS Code / Google Colab)
# ─────────────────────────────────────────────────────────────────────────────

import os
import sys
import warnings
warnings.filterwarnings('ignore')

# Detectar ambiente
try:
    import google.colab          # type: ignore
    IN_COLAB = True
except ImportError:
    IN_COLAB = False

if IN_COLAB:
    print("Ambiente: Google Colab")
    from google.colab import drive          # type: ignore
    drive.mount('/content/drive')
    import subprocess
    subprocess.run(['pip', 'install', '-q', 'yfinance', 'pyarrow', 'anthropic'], check=False)
    DADOS_DIR = '/content/drive/MyDrive/intensivao_quant/dados'
else:
    print("Ambiente: VS Code / Jupyter local")
    # Sobe até a raiz do repositório (.git)
    _p = os.path.abspath(os.getcwd())
    while _p != os.path.dirname(_p):
        if os.path.exists(os.path.join(_p, '.git')):
            break
        _p = os.path.dirname(_p)
    DADOS_DIR = os.path.join(_p, 'dados')

os.makedirs(DADOS_DIR, exist_ok=True)
print(f"DADOS_DIR = {DADOS_DIR}")


# ─────────────────────────────────────────────────────────────────────────────
# IMPORTS
# ─────────────────────────────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import yfinance as yf
from scipy import stats, optimize
from scipy.stats import spearmanr, norm

plt.rcParams['figure.figsize'] = (13, 5)
plt.rcParams['axes.grid']      = True
plt.rcParams['grid.alpha']     = 0.3


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 1 — UNIVERSO DE ATIVOS
# ─────────────────────────────────────────────────────────────────────────────

TICKERS_IBOV = [
    'ABEV3.SA', 'ASAI3.SA', 'AZUL4.SA', 'B3SA3.SA', 'BBAS3.SA',
    'BBDC3.SA', 'BBDC4.SA', 'BBSE3.SA', 'BPAC11.SA', 'BRAP4.SA',
    'BRFS3.SA', 'BRKM5.SA', 'CASH3.SA', 'CCRO3.SA', 'CIEL3.SA',
    'CMIG4.SA', 'CMIN3.SA', 'COGN3.SA', 'CPFE3.SA', 'CPLE6.SA',
    'CSAN3.SA', 'CSNA3.SA', 'CYRE3.SA', 'DXCO3.SA', 'EGIE3.SA',
    'ELET3.SA', 'ELET6.SA', 'EMBR3.SA', 'ENEV3.SA', 'ENGI11.SA',
    'EQTL3.SA', 'EZTC3.SA', 'FLRY3.SA', 'GGBR4.SA', 'GOAU4.SA',
    'GOLL4.SA', 'HAPV3.SA', 'HYPE3.SA', 'IGTI11.SA', 'IRBR3.SA',
    'ITSA4.SA', 'ITUB4.SA', 'JBSS3.SA', 'KLBN11.SA', 'LREN3.SA',
    'LWSA3.SA', 'MGLU3.SA', 'MRFG3.SA', 'MRVE3.SA', 'MULT3.SA',
    'NTCO3.SA', 'PCAR3.SA', 'PETR3.SA', 'PETR4.SA', 'PRIO3.SA',
    'QUAL3.SA', 'RADL3.SA', 'RAIL3.SA', 'RDOR3.SA', 'RENT3.SA',
    'RRRP3.SA', 'SANB11.SA', 'SBSP3.SA', 'SLCE3.SA', 'SMTO3.SA',
    'SULA11.SA', 'SUZB3.SA', 'TAEE11.SA', 'TIMS3.SA', 'TOTS3.SA',
    'UGPA3.SA', 'USIM5.SA', 'VALE3.SA', 'VBBR3.SA', 'VIVT3.SA',
    'WEGE3.SA', 'YDUQ3.SA',
]

DATA_INICIO = '2010-01-01'
DATA_FIM    = '2024-12-31'

N_ATIVOS        = 10     # top N para a carteira (top ~13% do universo)
JANELA_MOMENTUM = 11     # meses de formação (shift(2).rolling(11) → sinal 12-1)
JANELA_VOL_DIAS = 63     # dias para vol rolling do sinal v2
COBERTURA_MIN   = 0.80   # % mínimo de dados válidos por ativo


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 2 — DOWNLOAD E LIMPEZA DE DADOS
# ─────────────────────────────────────────────────────────────────────────────

def baixar_dados(tickers=TICKERS_IBOV, start=DATA_INICIO, end=DATA_FIM):
    """
    Baixa preços ajustados via yfinance para todos os tickers do IBOVESPA.

    Retorna
    -------
    precos : pd.DataFrame  — fechamentos ajustados diários (linhas = datas, colunas = tickers)
    """
    print(f"Baixando {len(tickers)} ativos ({start} → {end})...")
    precos = yf.download(
        tickers, start=start, end=end,
        auto_adjust=True, progress=True
    )['Close']
    print(f"Shape bruto: {precos.shape}")
    return precos


def limpar_precos(precos, cobertura_min=COBERTURA_MIN, vol_min_diaria=1e5):
    """
    Remove ativos com cobertura insuficiente ou baixa liquidez.

    Passos
    ------
    1. Filtra ativos com ≥ cobertura_min de dados válidos.
    2. Baixa volume diário e filtra por volume mínimo médio.
    3. Forward-fill gaps de até 5 dias consecutivos.

    Retorna
    -------
    precos_limpo : pd.DataFrame
    tickers_finais : list[str]
    """
    # 1. Cobertura
    cobertura     = precos.notna().mean()
    tickers_ok    = cobertura[cobertura >= cobertura_min].index.tolist()
    tickers_rm    = [t for t in precos.columns if t not in tickers_ok]
    if tickers_rm:
        print(f"Removidos por cobertura < {cobertura_min:.0%}: {tickers_rm}")

    # 2. Liquidez — volume médio diário
    print("Verificando liquidez (volume)...")
    vol_raw = yf.download(tickers_ok, start=DATA_INICIO, end=DATA_FIM,
                          auto_adjust=True, progress=False)['Volume']
    vol_medio     = vol_raw.mean()
    tickers_liq   = vol_medio[vol_medio >= vol_min_diaria].index.tolist()
    tickers_rm2   = [t for t in tickers_ok if t not in tickers_liq]
    if tickers_rm2:
        print(f"Removidos por liquidez: {tickers_rm2}")

    tickers_finais = [t for t in tickers_liq if t in tickers_ok]

    # 3. Forward-fill gaps curtos
    precos_limpo = precos[tickers_finais].ffill(limit=5)

    print(f"\nDataset limpo: {len(tickers_finais)} ativos")
    return precos_limpo, tickers_finais


def calcular_retornos(precos):
    """
    Calcula retornos logarítmicos diários e mensais.

    Retorno log: r_t = ln(P_t / P_{t-1})
    Aditividade: retorno acumulado = soma dos retornos log

    Retorna
    -------
    ret_diarios  : pd.DataFrame  — retornos diários
    ret_mensais  : pd.DataFrame  — retornos mensais (resample ME)
    """
    ret_diarios  = np.log(precos / precos.shift(1)).iloc[1:]
    ret_mensais  = ret_diarios.resample('ME').sum()
    return ret_diarios, ret_mensais


def salvar_dados_base(precos, ret_diarios, ret_mensais):
    """Salva os três parquets base na DADOS_DIR."""
    precos.to_parquet(os.path.join(DADOS_DIR, 'precos_ibov.parquet'))
    ret_diarios.to_parquet(os.path.join(DADOS_DIR, 'retornos_diarios_limpo.parquet'))
    ret_mensais.to_parquet(os.path.join(DADOS_DIR, 'retornos_mensais_limpo.parquet'))
    print("Salvos: precos_ibov | retornos_diarios_limpo | retornos_mensais_limpo")


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 3 — EDA (ANÁLISE EXPLORATÓRIA)
# ─────────────────────────────────────────────────────────────────────────────

def plot_risk_return(ret_diarios, destaque=None):
    """Scatter retorno anual × volatilidade anual por ativo."""
    DIAS = 252
    media  = ret_diarios.mean() * DIAS
    vol    = ret_diarios.std()  * np.sqrt(DIAS)
    resumo = pd.DataFrame({'retorno_anual': media, 'vol_anual': vol})

    fig, ax = plt.subplots(figsize=(11, 6))
    ax.scatter(resumo['vol_anual'], resumo['retorno_anual'], alpha=0.5, s=40)

    if destaque is None:
        destaque = ['PETR4.SA', 'VALE3.SA', 'WEGE3.SA', 'MGLU3.SA', 'BBAS3.SA']
    for t in destaque:
        if t in resumo.index:
            ax.annotate(t.replace('.SA', ''),
                        (resumo.loc[t, 'vol_anual'], resumo.loc[t, 'retorno_anual']),
                        fontsize=8, ha='left')

    ax.axhline(0, color='black', linewidth=0.8)
    ax.set_xlabel('Volatilidade anualizada'); ax.set_ylabel('Retorno anualizado (log)')
    ax.set_title('Risk-Return: cada ponto é um ativo (2010–2024)')
    plt.tight_layout(); plt.show()


def plot_distribuicao(ret_diarios, ticker='PETR4.SA'):
    """Histograma + QQ-plot: testa se retornos são normais."""
    r = ret_diarios[ticker].dropna()
    fig, axes = plt.subplots(1, 2, figsize=(13, 5))

    # Histograma
    x = np.linspace(r.min(), r.max(), 300)
    axes[0].hist(r, bins=80, density=True, alpha=0.6, color='steelblue', label='Observado')
    axes[0].plot(x, stats.norm.pdf(x, r.mean(), r.std()), 'r--', lw=2, label='Normal')
    axes[0].set_title(f'{ticker} — Distribuição dos retornos diários')
    axes[0].legend()

    # QQ-plot
    stats.probplot(r, dist='norm', plot=axes[1])
    axes[1].set_title('QQ-Plot (desvios nas caudas = fat tails)')
    plt.tight_layout(); plt.show()

    print(f"Kurtosis: {r.kurtosis():.2f}  (Normal = 0 em excesso)")
    print(f"Skewness: {r.skew():.2f}")


def testar_estacionaridade(ret_diarios, n_amostras=10):
    """Roda o teste ADF em uma amostra de ativos."""
    from statsmodels.tsa.stattools import adfuller   # type: ignore
    tickers = ret_diarios.columns[:n_amostras].tolist()
    print(f"{'Ativo':<14} {'ADF stat':>10} {'p-valor':>10} {'Estacionário?':>15}")
    print("-" * 55)
    for t in tickers:
        r = ret_diarios[t].dropna()
        stat, pval, *_ = adfuller(r)
        ok = "SIM" if pval < 0.05 else "NÃO"
        print(f"{t:<14} {stat:>10.3f} {pval:>10.4f} {ok:>15}")


def plot_heatmap_correlacao(ret_mensais, n_ativos=20):
    """Heatmap de correlação dos retornos mensais."""
    import matplotlib.pyplot as plt
    corr = ret_mensais.iloc[:, :n_ativos].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    im = ax.imshow(corr, cmap='RdYlGn', vmin=-1, vmax=1)
    plt.colorbar(im, ax=ax)
    tickers_label = [t.replace('.SA', '') for t in corr.columns]
    ax.set_xticks(range(len(tickers_label))); ax.set_yticks(range(len(tickers_label)))
    ax.set_xticklabels(tickers_label, rotation=90, fontsize=7)
    ax.set_yticklabels(tickers_label, fontsize=7)
    ax.set_title(f'Correlação mensal — {n_ativos} ativos')
    plt.tight_layout(); plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 4 — SINAL V1: MOMENTUM CROSS-SECTIONAL 12-1
# ─────────────────────────────────────────────────────────────────────────────

def calcular_sinal_v1(ret_mensais, janela=JANELA_MOMENTUM):
    """
    Sinal de momentum 12-1 (Jegadeesh & Titman, 1993).

    Para cada ativo i e mês t:
        Sinal(i,t) = Σ r(i, t-k)  para k de 2 a 12

    Em pandas:
        ret_mensais.shift(2).rolling(janela).sum()

    shift(2): exclui o mês imediatamente anterior (reversão de curto prazo).
    rolling(janela=11): soma os 11 meses anteriores ao mês excluído.
    Total: janela de formação de 12 meses, skip 1 mês.
    """
    sinal = ret_mensais.shift(2).rolling(janela).sum()
    print(f"Sinal v1 calculado — shape: {sinal.shape}")
    print(f"Primeiro mês disponível: {sinal.dropna(how='all').index[0].date()}")
    return sinal


def calcular_ic_serie(sinal, ret_mensais):
    """
    Information Coefficient mensal: Spearman(sinal_t, retorno_{t+1}).

    IC > 0 → sinal tem poder preditivo.
    Referência: IC médio > 0.05 é considerado bom em gestão ativa.

    Retorna
    -------
    ic_serie : pd.Series  — IC mês a mês
    """
    ic_list = []
    datas   = sinal.index

    for i in range(len(datas) - 1):
        t_sinal = datas[i]
        t_ret   = datas[i + 1]
        if t_ret not in ret_mensais.index:
            continue
        s = sinal.loc[t_sinal].dropna()
        r = ret_mensais.loc[t_ret, s.index].dropna()
        s = s.reindex(r.index).dropna()
        if len(s) > 10:
            ic, _ = spearmanr(s, r)
            ic_list.append({'data': t_ret, 'ic': ic})

    ic_serie = pd.DataFrame(ic_list).set_index('data')['ic']
    print(f"IC médio: {ic_serie.mean():.4f}  |  t-stat: "
          f"{ic_serie.mean() / ic_serie.std() * np.sqrt(len(ic_serie)):.2f}")
    return ic_serie


def plot_ic(ic_serie):
    """Barras de IC mensais + rolling 12 meses."""
    fig, axes = plt.subplots(2, 1, figsize=(13, 7), sharex=True)
    colors = ['#1E8B4C' if x > 0 else '#E74C3C' for x in ic_serie]
    axes[0].bar(ic_serie.index, ic_serie.values, color=colors, alpha=0.7, width=20)
    axes[0].axhline(0, color='black', lw=0.8)
    axes[0].axhline(ic_serie.mean(), color='navy', lw=1.5, ls='--',
                    label=f'Média: {ic_serie.mean():.3f}')
    axes[0].set_title('Information Coefficient (IC) mensal')
    axes[0].legend()

    ic_serie.rolling(12).mean().plot(ax=axes[1], color='navy', lw=2)
    axes[1].axhline(0, color='black', lw=0.8)
    axes[1].set_title('IC Rolling 12 meses')
    plt.tight_layout(); plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 5 — BACKTEST V1: MÉTRICAS E TEARSHEET
# ─────────────────────────────────────────────────────────────────────────────

def construir_portfolio(sinal, ret_mensais, n_ativos=N_ATIVOS):
    """
    Constrói carteira long-only equal-weight com top N ativos do sinal.

    IMPORTANTE: pesos formados em t → aplicados ao retorno de t+1 (shift implícito).
    Isso garante ausência de look-ahead bias.

    Retorna
    -------
    pesos       : pd.DataFrame  — pesos mensais
    ret_carteira: pd.Series     — retorno log mensal da carteira
    """
    ranking = sinal.rank(axis=1, ascending=True, pct=True)

    def pesos_linha(row):
        validos = row.dropna()
        if len(validos) < n_ativos:
            return pd.Series(0.0, index=row.index)
        top = validos.nlargest(n_ativos).index
        p   = pd.Series(0.0, index=row.index)
        p[top] = 1.0 / n_ativos
        return p

    pesos = ranking.apply(pesos_linha, axis=1)

    # shift(1): pesos de M usados no retorno de M+1
    ret_carteira = (pesos.shift(1) * ret_mensais).sum(axis=1)
    ret_carteira = ret_carteira[pesos.sum(axis=1) > 0]

    print(f"Carteira construída — {len(ret_carteira)} meses de retorno")
    return pesos, ret_carteira


def calcular_metricas(retornos, benchmark=None, nome='Estratégia', rf_mensal=0.0):
    """
    Métricas completas de desempenho para retornos log mensais.

    Retorna dict com: CAGR, Vol, Sharpe, Sortino, MDD, Calmar, Alpha, Beta.
    """
    r = retornos.dropna()
    excesso = r - rf_mensal

    sharpe  = excesso.mean() / excesso.std() * np.sqrt(12) if excesso.std() > 0 else np.nan
    sortino = (excesso.mean() / excesso[excesso < 0].std() * np.sqrt(12)
               if len(excesso[excesso < 0]) > 0 else np.nan)

    n_anos = len(r) / 12
    cagr   = (np.exp(r.sum()) ** (1 / n_anos)) - 1
    vol    = r.std() * np.sqrt(12)

    valor  = np.exp(r.cumsum())
    pico   = valor.cummax()
    mdd    = ((valor - pico) / pico).min()
    calmar = cagr / abs(mdd) if mdd != 0 else np.nan

    alpha, beta = np.nan, np.nan
    if benchmark is not None:
        bm = benchmark.reindex(r.index).dropna()
        rv = r.reindex(bm.index)
        if len(rv) > 10:
            beta, intercept, *_ = stats.linregress(bm, rv)
            alpha = intercept * 12  # anualizado

    return {
        'nome': nome, 'n_meses': len(r),
        'CAGR': cagr, 'Vol': vol, 'Sharpe': sharpe,
        'Sortino': sortino, 'MDD': mdd, 'Calmar': calmar,
        'Alpha': alpha, 'Beta': beta,
    }


def exibir_metricas(*metricas):
    """Tabela comparativa de métricas."""
    fmt = {
        'CAGR': '{:.1%}', 'Vol': '{:.1%}', 'Sharpe': '{:.2f}',
        'Sortino': '{:.2f}', 'MDD': '{:.1%}', 'Calmar': '{:.2f}',
        'Alpha': '{:.1%}', 'Beta': '{:.2f}',
    }
    keys = ['CAGR', 'Vol', 'Sharpe', 'Sortino', 'MDD', 'Calmar', 'Alpha', 'Beta']
    header = f"{'Métrica':<12}" + "".join(f"{m['nome']:>14}" for m in metricas)
    print(header)
    print("-" * len(header))
    for k in keys:
        vals = "".join(
            f"{fmt[k].format(m[k]) if m[k] is not None and not (isinstance(m[k], float) and np.isnan(m[k])) else 'N/A':>14}"
            for m in metricas
        )
        print(f"{k:<12}{vals}")


def plot_tearsheet(ret_estrategia, ret_benchmark, nome='Estratégia'):
    """Painel completo: equity curve, drawdown, retornos mensais, QQ-plot."""
    bm = ret_benchmark.reindex(ret_estrategia.index).dropna()
    re = ret_estrategia.reindex(bm.index)

    fig = plt.figure(figsize=(14, 10))
    gs  = gridspec.GridSpec(3, 2, figure=fig, hspace=0.4, wspace=0.3)

    # Equity curve
    ax1 = fig.add_subplot(gs[0, :])
    np.exp(re.cumsum()).plot(ax=ax1, label=nome, lw=2, color='#1A6EAE')
    np.exp(bm.cumsum()).plot(ax=ax1, label='IBOVESPA', lw=1.5, ls='--', color='gray')
    ax1.set_title('Retorno Acumulado (base 1)')
    ax1.legend(); ax1.grid(alpha=0.3)

    # Drawdown
    ax2 = fig.add_subplot(gs[1, :])
    val = np.exp(re.cumsum())
    dd  = (val - val.cummax()) / val.cummax()
    ax2.fill_between(dd.index, dd.values, 0, color='#E74C3C', alpha=0.5)
    ax2.set_title(f'Drawdown (MDD = {dd.min():.1%})')
    ax2.grid(alpha=0.3)

    # Retornos mensais
    ax3 = fig.add_subplot(gs[2, 0])
    colors = ['#1E8B4C' if x > 0 else '#E74C3C' for x in re.values]
    ax3.bar(range(len(re)), re.values, color=colors, alpha=0.7, width=0.8)
    ax3.axhline(0, color='black', lw=0.8)
    ax3.set_title('Retornos Mensais'); ax3.grid(alpha=0.2, axis='y')

    # QQ-plot
    ax4 = fig.add_subplot(gs[2, 1])
    stats.probplot(re.dropna(), dist='norm', plot=ax4)
    ax4.set_title('QQ-Plot Retornos'); ax4.grid(alpha=0.3)

    plt.suptitle(f'Tearsheet — {nome}', fontsize=13, fontweight='bold')
    plt.savefig(os.path.join(DADOS_DIR, f'tearsheet_{nome.lower().replace(" ","_")}.png'),
                dpi=150, bbox_inches='tight')
    plt.show()


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 6 — ALOCAÇÃO DE PORTFÓLIO
# ─────────────────────────────────────────────────────────────────────────────

def pesos_vol_weight(sinal, ret_diarios, n_ativos=N_ATIVOS, janela_vol=JANELA_VOL_DIAS):
    """
    Vol-weight (risk parity simplificado): w_i ∝ 1 / σ_i.

    A ação de menor volatilidade recebe o maior peso.
    Sem estimação de retornos esperados → evita o principal source de erro do Markowitz.
    """
    vol_rolling = (ret_diarios.rolling(janela_vol).std() * np.sqrt(252)
                   ).resample('ME').last()

    pesos = pd.DataFrame(0.0, index=sinal.index, columns=sinal.columns)

    for data in sinal.index:
        s = sinal.loc[data].dropna()
        if len(s) < n_ativos:
            continue
        top_n = s.nlargest(n_ativos).index

        if data not in vol_rolling.index:
            continue
        v = vol_rolling.loc[data, top_n].dropna().replace(0, np.nan).dropna()
        if len(v) < 2:
            continue

        w = (1.0 / v) / (1.0 / v).sum()
        pesos.loc[data, w.index] = w.values

    return pesos


def pesos_markowitz_restrito(sinal, ret_mensais, n_ativos=N_ATIVOS, janela=36, cap=0.20):
    """
    Markowitz com restrição de peso por ativo (0% a cap%).

    DeMiguel et al. (2009): Markowitz puro raramente vence 1/N fora da amostra.
    Restrições melhoram estabilidade ao custo de sub-otimização teórica.
    """
    pesos = pd.DataFrame(0.0, index=sinal.index, columns=sinal.columns)

    for i, data in enumerate(sinal.index):
        if i < janela:
            continue
        s = sinal.loc[data].dropna()
        if len(s) < n_ativos:
            continue
        top_n = s.nlargest(n_ativos).index

        hist = ret_mensais.loc[:data].iloc[-janela:][top_n].dropna(axis=1)
        if hist.shape[1] < 2:
            continue
        Sigma = hist.cov().values
        n     = Sigma.shape[0]
        ativos = hist.columns

        # Minimizar variância do portfólio
        def portfolio_vol(w):
            return w @ Sigma @ w

        constraints = [{'type': 'eq', 'fun': lambda w: w.sum() - 1}]
        bounds      = [(0, cap)] * n
        w0          = np.ones(n) / n

        res = optimize.minimize(portfolio_vol, w0,
                                method='SLSQP',
                                bounds=bounds,
                                constraints=constraints,
                                options={'ftol': 1e-9, 'maxiter': 500})
        if res.success:
            pesos.loc[data, ativos] = res.x

    return pesos


def calcular_turnover(pesos_df):
    """Turnover mensal: percentual da carteira que muda a cada rebalanceamento."""
    delta = pesos_df.diff().abs().sum(axis=1) / 2
    return delta[pesos_df.sum(axis=1) > 0].iloc[1:]


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 7 — SINAL V2: VOL-ADJUSTED MOMENTUM
# ─────────────────────────────────────────────────────────────────────────────

def calcular_sinal_v2(sinal_v1, ret_diarios, janela_vol=JANELA_VOL_DIAS):
    """
    Sinal v2 = Sinal_v1 / σ_rolling (Moskowitz, Ooi & Pedersen, 2012).

    Normaliza o sinal pela volatilidade corrente do ativo.
    Ativos mais voláteis recebem sinal "deflacionado" → reduz momentum crash.

    Momentum crash (Daniel & Moskowitz, 2016): em crises, os "vencedores" do
    sinal v1 tendem a ser ativos de alto beta, que caem mais. O ajuste por vol
    reduz esse risco de cauda.
    """
    # Volatilidade rolling diária → reamostrada para mensal (última obs. do mês)
    vol_rolling = (ret_diarios.rolling(janela_vol).std() * np.sqrt(252)
                   ).resample('ME').last()

    # Alinhar índice com o sinal
    vol_alinhada = vol_rolling.reindex(sinal_v1.index, method='ffill')

    # Dividir sinal pela vol (substituir vol = 0 por NaN)
    sinal_v2 = sinal_v1 / vol_alinhada.replace(0, np.nan)

    print(f"Sinal v2 calculado — NaNs adicionais vs v1: "
          f"{sinal_v2.isna().sum().sum() - sinal_v1.isna().sum().sum():,}")
    return sinal_v2


def comparar_sinais(sinal_v1, sinal_v2, ret_mensais):
    """Compara IC médio e t-stat entre sinal v1 e v2."""
    ic1 = calcular_ic_serie(sinal_v1, ret_mensais)
    ic2 = calcular_ic_serie(sinal_v2, ret_mensais)

    print(f"\n{'':25} {'IC médio':>10} {'t-stat':>10} {'IC > 0 (%)':>12}")
    print("-" * 60)
    for nome, ic in [('Sinal v1 (raw)', ic1), ('Sinal v2 (vol-adj)', ic2)]:
        t = ic.mean() / ic.std() * np.sqrt(len(ic))
        pct = (ic > 0).mean()
        print(f"{nome:<25} {ic.mean():>10.4f} {t:>10.2f} {pct:>12.1%}")
    return ic1, ic2


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 8 — BACKTEST RIGOROSO: WALK-FORWARD E DSR
# ─────────────────────────────────────────────────────────────────────────────

def backtest_walkforward(sinal, ret_mensais, janela_treino=36, janela_teste=6,
                         n_ativos=N_ATIVOS):
    """
    Walk-Forward Analysis — retornos puramente out-of-sample.

    A cada iteração:
      - Janela de treino: parâmetros calculados em [0, treino_end]
      - Janela de teste:  retornos OOS em [treino_end+1, treino_end+janela_teste]
      - A janela avança janela_teste meses e repete.

    Nenhum retorno OOS usa informação de datas futuras.

    Retorna
    -------
    ret_oos : pd.Series — retornos mensais OOS (puramente out-of-sample)
    """
    datas     = sinal.dropna(how='all').index.sort_values()
    resultados = []
    inicio    = janela_treino

    while inicio + janela_teste <= len(datas):
        datas_oos = datas[inicio: inicio + janela_teste]

        for data in datas_oos:
            if data not in sinal.index:
                continue
            s = sinal.loc[data].dropna()
            if len(s) < n_ativos:
                continue
            top = s.nlargest(n_ativos).index

            if data not in ret_mensais.index:
                continue
            r_mes = ret_mensais.loc[data, top].dropna()
            p     = pd.Series(1.0 / len(r_mes), index=r_mes.index)
            resultados.append({'data': data, 'retorno': (r_mes * p).sum(),
                               'n_ativos': len(top)})

        inicio += janela_teste

    ret_oos = pd.DataFrame(resultados).set_index('data')['retorno']
    print(f"Walk-forward OOS: {len(ret_oos)} meses "
          f"({ret_oos.index.min().date()} → {ret_oos.index.max().date()})")
    return ret_oos


def calcular_dsr(retornos, n_estrategias=5):
    """
    Deflated Sharpe Ratio (Bailey & López de Prado, 2014).

    Penaliza o Sharpe observado por:
      1. Número de estratégias testadas (n_estrategias) → múltiplos testes
      2. Não-normalidade dos retornos (skewness, kurtosis)

    Interpretação: DSR ∈ [0, 1]
      > 0.95  → resultado estatisticamente robusto
      < 0.50  → forte suspeita de overfitting

    Retorna
    -------
    dict com sharpe_obs, sharpe_corr, e_maxsr, dsr
    """
    r  = retornos.dropna()
    n  = len(r)
    sr = r.mean() / r.std() * np.sqrt(12)
    sk = r.skew()
    ku = r.kurtosis()   # kurtosis em excesso (Normal = 0)

    # Expected Maximum Sharpe Ratio dado n_estrategias tentativas
    e_maxsr = np.sqrt(2) * norm.ppf(1 - 1.0 / n_estrategias) if n_estrategias > 1 else 0.0

    # Correção do Sharpe por não-normalidade
    sr_corr = sr / np.sqrt(1 - sk / 6 * sr + (ku - 3) / 24 * sr ** 2 + 1e-10)

    # DSR: probabilidade de superar o E[MaxSR]
    denom = np.sqrt(max(1 - sr_corr * e_maxsr + sr_corr ** 2 * (ku + 1) / 4, 1e-10))
    dsr   = norm.cdf((sr_corr - e_maxsr) * np.sqrt(n - 1) / denom)

    resultado = {
        'sharpe_obs':  round(sr, 3),
        'sharpe_corr': round(sr_corr, 3),
        'e_maxsr':     round(e_maxsr, 3),
        'dsr':         round(dsr, 4),
    }
    print(f"  Sharpe observado:   {resultado['sharpe_obs']}")
    print(f"  Sharpe corrigido:   {resultado['sharpe_corr']}")
    print(f"  E[MaxSR] esperado:  {resultado['e_maxsr']}")
    print(f"  DSR (probabilidade): {resultado['dsr']:.4f}  "
          f"({'ROBUSTO' if dsr > 0.95 else 'ATENÇÃO' if dsr > 0.5 else 'OVERFITTING?'})")
    return resultado


def plot_is_vs_oos(ret_is, ret_oos, nome='Estratégia v2'):
    """Compara curva acumulada in-sample vs out-of-sample."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    # Acumulado
    np.exp(ret_is.cumsum()).plot(ax=axes[0], label='In-Sample', color='#1A6EAE', lw=2)
    np.exp(ret_oos.cumsum()).plot(ax=axes[0], label='Walk-Forward OOS', color='#F5A623', lw=2, ls='--')
    axes[0].set_title('Retorno Acumulado: IS vs OOS')
    axes[0].legend(); axes[0].grid(alpha=0.3)

    # Distribuição
    axes[1].hist(ret_is,  bins=30, alpha=0.5, label='In-Sample',    color='#1A6EAE')
    axes[1].hist(ret_oos, bins=30, alpha=0.5, label='OOS',          color='#F5A623')
    axes[1].axvline(ret_is.mean(),  color='#1A6EAE', lw=2, ls='--')
    axes[1].axvline(ret_oos.mean(), color='#F5A623', lw=2, ls='--')
    axes[1].set_title('Distribuição de Retornos Mensais')
    axes[1].legend(); axes[1].grid(alpha=0.3)

    plt.suptitle(f'Validação Out-of-Sample — {nome}', fontweight='bold')
    plt.tight_layout(); plt.show()


def analise_sensibilidade(ret_mensais, lookbacks=None, n_pcts=None):
    """
    Testa Sharpe para diferentes lookbacks e tamanhos de portfólio.
    Robustez: resultados estáveis indicam sinal genuíno, não overfitted.
    """
    if lookbacks is None:
        lookbacks = [6, 9, 11, 12, 15, 18]
    if n_pcts is None:
        n_pcts    = [0.10, 0.15, 0.20, 0.25, 0.30]

    print("=== Sensibilidade ao lookback ===")
    for lb in lookbacks:
        s = ret_mensais.shift(2).rolling(lb).sum()
        n = max(int(ret_mensais.shape[1] * 0.20), 5)
        _, r = construir_portfolio(s, ret_mensais, n_ativos=n)
        sr = r.mean() / r.std() * np.sqrt(12)
        print(f"  Lookback {lb:2d}m → Sharpe: {sr:.2f}")

    print("\n=== Sensibilidade ao tamanho do portfólio ===")
    s_base = ret_mensais.shift(2).rolling(11).sum()
    for pct in n_pcts:
        n = max(int(ret_mensais.shape[1] * pct), 2)
        _, r = construir_portfolio(s_base, ret_mensais, n_ativos=n)
        sr = r.mean() / r.std() * np.sqrt(12)
        print(f"  Top {pct:.0%} ({n} ativos) → Sharpe: {sr:.2f}")


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 9 — GENAI: NARRATIVA VIA API ANTHROPIC
# ─────────────────────────────────────────────────────────────────────────────

def gerar_narrativa_performance(ret_is, ret_oos, modelo='claude-haiku-4-5-20251001'):
    """
    Gera comentário de performance via API Claude (Anthropic).

    Requer: pip install anthropic  |  variável ANTHROPIC_API_KEY configurada.

    Parâmetros
    ----------
    ret_is  : pd.Series — retornos in-sample
    ret_oos : pd.Series — retornos out-of-sample (walk-forward)
    modelo  : str — ID do modelo Anthropic
    """
    try:
        import anthropic   # type: ignore
    except ImportError:
        print("Instale o SDK: pip install anthropic")
        return None

    def _metricas_str(r, nome):
        sr   = r.mean() / r.std() * np.sqrt(12)
        cagr = np.exp(r.sum()) ** (12 / len(r)) - 1
        mdd  = ((np.exp(r.cumsum()) / np.exp(r.cumsum()).cummax()) - 1).min()
        return (f"{nome}: Sharpe={sr:.2f}, CAGR={cagr:.1%}, "
                f"MDD={mdd:.1%}, N={len(r)} meses")

    system = (
        "Você é um analista quantitativo sênior de uma gestora brasileira. "
        "Escreva em português formal e técnico. Cite os números exatos fornecidos. "
        "Tamanho: 200–250 palavras."
    )
    prompt = (
        "Analise a performance da seguinte estratégia de momentum cross-sectional "
        "no IBOVESPA (sinal 12-1 com ajuste de volatilidade).\n\n"
        f"IN-SAMPLE: {_metricas_str(ret_is, 'IS')}\n"
        f"OUT-OF-SAMPLE (walk-forward): {_metricas_str(ret_oos, 'OOS')}\n\n"
        "Interprete os resultados, compare IS vs OOS, aponte robustez e limitações, "
        "e conclua com recomendação para comitê de investimentos."
    )

    client   = anthropic.Anthropic()
    mensagem = client.messages.create(
        model=modelo, max_tokens=1024, temperature=0.0,
        system=system,
        messages=[{'role': 'user', 'content': prompt}]
    )
    narrativa = mensagem.content[0].text
    print(narrativa)

    # Salvar em arquivo
    path = os.path.join(DADOS_DIR, 'narrativa_performance.txt')
    with open(path, 'w', encoding='utf-8') as f:
        f.write(narrativa)
    print(f"\nNarrativa salva em: {path}")
    return narrativa


# ─────────────────────────────────────────────────────────────────────────────
# SEÇÃO 10 — PIPELINE COMPLETO (main)
# ─────────────────────────────────────────────────────────────────────────────

def main(pular_download=False, pular_eda=False):
    """
    Executa o pipeline completo do projeto.

    Parâmetros
    ----------
    pular_download : bool — True se os parquets base já existem
    pular_eda      : bool — True para pular gráficos de EDA
    """
    print("=" * 70)
    print("  INTENSIVÃO QUANT AI — PIPELINE COMPLETO")
    print("=" * 70)

    # ── DADOS ────────────────────────────────────────────────────────────────
    print("\n[1/8] DOWNLOAD E LIMPEZA DE DADOS")
    precos_path = os.path.join(DADOS_DIR, 'precos_ibov.parquet')

    if pular_download and os.path.exists(precos_path):
        print("  Carregando parquets existentes...")
        precos       = pd.read_parquet(precos_path)
        ret_diarios  = pd.read_parquet(os.path.join(DADOS_DIR, 'retornos_diarios_limpo.parquet'))
        ret_mensais  = pd.read_parquet(os.path.join(DADOS_DIR, 'retornos_mensais_limpo.parquet'))
    else:
        precos_raw           = baixar_dados()
        precos, tickers_ok   = limpar_precos(precos_raw)
        ret_diarios, ret_mensais = calcular_retornos(precos)
        salvar_dados_base(precos, ret_diarios, ret_mensais)

    print(f"  Shape: {ret_mensais.shape}  |  "
          f"Período: {ret_mensais.index[0].date()} → {ret_mensais.index[-1].date()}")

    # ── EDA ──────────────────────────────────────────────────────────────────
    if not pular_eda:
        print("\n[2/8] EDA")
        plot_distribuicao(ret_diarios)
        plot_risk_return(ret_diarios)
        plot_heatmap_correlacao(ret_mensais)

    # ── SINAL V1 ─────────────────────────────────────────────────────────────
    print("\n[3/8] SINAL V1 — MOMENTUM 12-1")
    sinal_v1 = calcular_sinal_v1(ret_mensais)
    sinal_v1.to_parquet(os.path.join(DADOS_DIR, 'sinal_v1.parquet'))

    ic_v1 = calcular_ic_serie(sinal_v1, ret_mensais)
    if not pular_eda:
        plot_ic(ic_v1)

    # ── BACKTEST V1 ───────────────────────────────────────────────────────────
    print("\n[4/8] BACKTEST V1 — EQUAL WEIGHT")
    pesos_v1, ret_v1 = construir_portfolio(sinal_v1, ret_mensais)
    pesos_v1.to_parquet(os.path.join(DADOS_DIR, 'pesos_v1.parquet'))
    ret_v1.to_frame('retorno').to_parquet(os.path.join(DADOS_DIR, 'retorno_carteira_v1.parquet'))

    # IBOVESPA como benchmark
    ibov_raw = yf.download("^BVSP", start=DATA_INICIO, end=DATA_FIM,
                           auto_adjust=True, progress=False)['Close'].squeeze()
    ret_ibov = np.log(ibov_raw / ibov_raw.shift(1)).resample('ME').sum()

    m_v1 = calcular_metricas(ret_v1, ret_ibov, 'Momentum v1')
    m_bm = calcular_metricas(ret_ibov, nome='IBOVESPA')
    exibir_metricas(m_v1, m_bm)
    if not pular_eda:
        plot_tearsheet(ret_v1, ret_ibov, 'Momentum v1')

    # ── ALOCAÇÃO ─────────────────────────────────────────────────────────────
    print("\n[5/8] ALOCAÇÃO — VOL-WEIGHT")
    pesos_vw = pesos_vol_weight(sinal_v1, ret_diarios)
    ret_vw   = (pesos_vw.shift(1) * ret_mensais).sum(axis=1)
    ret_vw   = ret_vw[pesos_vw.sum(axis=1) > 0]
    pesos_vw.to_parquet(os.path.join(DADOS_DIR, 'pesos_v2.parquet'))
    ret_vw.to_frame('retorno').to_parquet(os.path.join(DADOS_DIR, 'retorno_carteira_v2.parquet'))

    m_vw = calcular_metricas(ret_vw, ret_ibov, 'Vol-Weight')
    exibir_metricas(m_v1, m_vw, m_bm)

    # ── SINAL V2 ─────────────────────────────────────────────────────────────
    print("\n[6/8] SINAL V2 — VOL-ADJUSTED MOMENTUM")
    sinal_v2 = calcular_sinal_v2(sinal_v1, ret_diarios)
    sinal_v2.to_parquet(os.path.join(DADOS_DIR, 'sinal_v2.parquet'))

    pesos_v2, ret_v2 = construir_portfolio(sinal_v2, ret_mensais)
    pesos_v2.to_parquet(os.path.join(DADOS_DIR, 'pesos_sinal_v2.parquet'))
    ret_v2.to_frame('retorno').to_parquet(os.path.join(DADOS_DIR, 'retorno_carteira_sinal_v2.parquet'))

    ic_v1, ic_v2 = comparar_sinais(sinal_v1, sinal_v2, ret_mensais)
    m_v2 = calcular_metricas(ret_v2, ret_ibov, 'Momentum v2')
    exibir_metricas(m_v1, m_v2, m_bm)

    # ── BACKTEST RIGOROSO ────────────────────────────────────────────────────
    print("\n[7/8] BACKTEST RIGOROSO — WALK-FORWARD + DSR")
    ret_oos = backtest_walkforward(sinal_v2, ret_mensais)
    ret_oos.to_frame('retorno').to_parquet(
        os.path.join(DADOS_DIR, 'retorno_walkforward_liquido.parquet'))

    print("\nDSR — Deflated Sharpe Ratio:")
    dsr = calcular_dsr(ret_oos, n_estrategias=5)

    if not pular_eda:
        plot_is_vs_oos(ret_v2, ret_oos)
        analise_sensibilidade(ret_mensais)

    # ── RELATÓRIO FINAL ───────────────────────────────────────────────────────
    print("\n[8/8] RELATÓRIO FINAL")
    print("\n── Métricas consolidadas ──")
    m_oos = calcular_metricas(ret_oos, ret_ibov, 'OOS Walk-Forward')
    exibir_metricas(m_v1, m_v2, m_oos, m_bm)

    print(f"\n── DSR: {dsr['dsr']:.4f} "
          f"({'✓ Robusto' if dsr['dsr'] > 0.95 else '⚠ Verificar' if dsr['dsr'] > 0.5 else '✗ Overfitting?'})")

    print("\nArquivos gerados em", DADOS_DIR)
    for f in sorted(os.listdir(DADOS_DIR)):
        if f.endswith('.parquet'):
            size = os.path.getsize(os.path.join(DADOS_DIR, f)) / 1024
            print(f"  {f:<45} {size:6.0f} KB")

    print("\nPipeline concluído!")
    return {
        'ret_v1': ret_v1, 'ret_v2': ret_v2, 'ret_oos': ret_oos,
        'ret_ibov': ret_ibov, 'sinal_v1': sinal_v1, 'sinal_v2': sinal_v2,
        'dsr': dsr,
    }


# ─────────────────────────────────────────────────────────────────────────────
if __name__ == '__main__':
    # Para rodar o pipeline completo:
    #   python intensivao_quant_ai_completo.py
    #
    # Para pular o download (dados já existem na DADOS_DIR):
    #   resultado = main(pular_download=True, pular_eda=True)

    resultado = main(pular_download=False, pular_eda=False)
