# Intensivão Quant AI — ImpactUFSCar

Repositório central do Intensivão Quant AI da Diretoria de Quant da ImpactUFSCar.

**Objetivo:** preparar 7 equipes para o Desafio Quant AI da Itaú Asset Management, construindo ao longo de 5 semanas uma estratégia de momentum cross-seccional no IBOVESPA do zero.

---

## Como usar este repositório

vá direto para a pasta da aula corrente em `aulas/`. Cada pasta contém o notebook que o Felipe codificou ao vivo. Clone, rode, e replique no repositório da sua equipe.

---

## Estrutura

```
intensivao-quant-ai/
├── README.md                        # este arquivo
├── docs/
│   └── briefing.md                  # documento de trabalho do intensivão
├── aulas/
│   ├── aula-01-kickoff/
│   ├── aula-02-dados/
│   ├── aula-03-eda/
│   ├── aula-04-sinal-v1/
│   ├── aula-05-backtest-v1/
│   ├── aula-06-alocacao/
│   ├── aula-07-sinal-v2/
│   ├── aula-08-backtest-rigoroso/
│   └── aula-09-genai-relatorio/     # consolidado de GenAI, Relatório e Defesa
├── estrategia/
│   └── momentum-ibovespa/           # especificação e notebook baseline
└── equipes/
    └── README.md                    # instruções para o repo de cada equipe
```

---

## Cronograma (60 min por aula: 20m Teoria + 40m Código)

| Data | Aula / Marco | Tópicos |
|---|---|---|
| 18/05/2026 | Aula 01: Kick-off | Fundamentos, HME, anomalias e ecossistema (Apresentada). |
| 20/05/2026 | Aula 02: Setup + Dados | Coleta via `yfinance` (2012-2024), forward-fill, Parquet. |
| 22/05/2026 | Aula 03: EDA + Limpeza | Estatísticas, caudas pesadas, QQ-plot, correlações. |
| 25/05/2026 | Aula 04: Sinal v1 - Momentum 12-1 | Jegadeesh & Titman 1993, ranking percentil, Spearman IC. |
| 26/05/2026 | **Kick-off Oficial Desafio Itaú** | Início oficial do desafio da Itaú Asset. |
| 27/05/2026 | Aula 05: Backtest v1 | weights.shift(1), CAGR, Sharpe, Drawdown, Benchmark. |
| 29/05/2026 | Aula 06: Alocação — Markowitz | Markowitz (Teoria Moderna), `scipy.optimize`, restrições. |
| 01/06/2026 | Aula 07: Sinal v2 — Vol-Adjusted | Momentum crashes, normalização por vol rolling de 63d. |
| 03/06/2026 | Aula 08: Backtest Rigoroso com Custos | Turnover, custos reais (0.3%), walk-forward. |
| 05/06/2026 | Aula 09: GenAI, Relatório & Defesa | Prompts p/ Claude, 7 critérios Itaú, pitch final. |
| Mid-julho | Checkpoint interno | Backtest funcionando 100%. |
| Início de agosto | Checkpoint interno | Rascunho final do relatório técnico. |
| 17/08/2026 | **Entrega Final do Relatório** | Entrega oficial do projeto técnico ao Itaú. |

---

## Stack

```
python >= 3.10
yfinance
pandas
numpy
statsmodels
scikit-learn
vectorbt
matplotlib
scipy
```

---

## Princípio do intensivão

> O intensivão é a largada, não a linha de chegada. Cada aula tem duração estrita de **60 minutos**, divididos em **20 minutos de teoria intuitiva** e **40 minutos de live coding passo a passo**. Você sai daqui capaz de construir o robô — os dois meses seguintes são onde ele fica competitivo.

