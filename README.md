# Intensivão Quant AI — ImpactUFSCar

Repositório central do Intensivão Quant AI da Diretoria de Quant da ImpactUFSCar.

**Objetivo:** preparar 7 equipes (~25 membros) para o Desafio Quant AI da Itaú Asset Management, construindo ao longo de 5 semanas uma estratégia de momentum cross-seccional no IBOVESPA do zero.

---

## Como usar este repositório

- **Se você é aluno:** vá direto para a pasta da aula corrente em `aulas/`. Cada pasta contém o notebook que o Felipe codificou ao vivo. Clone, rode, e replique no repositório da sua equipe.
- **Se você é instrutor:** consulte o `docs/briefing.md` para o contexto completo do intensivão e a pasta `estrategia/momentum-ibovespa/` para a especificação da estratégia.

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
│   ├── aula-09-genai-analise/
│   └── aula-10-relatorio-defesa/
├── estrategia/
│   └── momentum-ibovespa/           # especificação e notebook baseline
└── equipes/
    └── README.md                    # instruções para o repo de cada equipe
```

---

## Cronograma

| Data | Marco |
|---|---|
| 18/05/2026 | Início do intensivão (Aula 1) |
| 26/05/2026 | Kick-off oficial do Desafio Itaú |
| ~22/06/2026 | Fim do intensivão (Aula 10) |
| Mid-julho | Checkpoint interno — backtest funcionando |
| Início de agosto | Checkpoint interno — relatório em rascunho |
| 17/08/2026 | Entrega final do relatório |

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
```

---

## Princípio do intensivão

> O intensivão é a largada, não a linha de chegada. Você sai daqui capaz de construir o robô — os dois meses seguintes são onde ele fica competitivo.
