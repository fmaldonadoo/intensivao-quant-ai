# Estratégia: Momentum Cross-Seccional no IBOVESPA

## A tese em uma frase

Ações do IBOVESPA que tiveram os maiores retornos nos últimos 12 meses (excluindo o mês mais recente) tendem a continuar superando as demais nos próximos meses.

---

## Por que funciona

Momentum é um dos fenômenos mais documentados em finanças. A explicação mais aceita vem de finanças comportamentais:

- **Underreaction:** investidores demoram a incorporar novas informações — o preço sobe, mas devagar
- **Herding:** à medida que outros investidores notam a alta, entram na mesma direção, prolongando o movimento
- **Ancoragem:** investidores ancoram expectativas em preços passados, subestimando a continuidade da tendência

Referência fundamental: Jegadeesh & Titman (1993) — *"Returns to Buying Winners and Selling Losers"*, Journal of Finance.

---

## Especificação técnica

| Parâmetro | Valor base | O que varia nas equipes |
|---|---|---|
| Universo | Componentes do IBOVESPA | — |
| Janela do sinal | 12 meses, skip 1 mês (retorno de t-13 a t-1) | Janela de 6, 9 ou 12 meses |
| Seleção | Top N ativos pelo sinal | N = 5, 10, 15 |
| Alocação | Equal weight → signal-weighted (Aula 6) | Risk parity como alternativa |
| Refinamento | Vol-adjusted momentum (Aula 7) | — |
| Rebalanceamento | Mensal | — |
| Período de backtest | 2010–2024 | — |
| Benchmark | IBOVESPA (^BVSP) | — |

---

## Riscos de modelagem

Estes são os erros mais comuns em estratégias de momentum. A banca os conhece e vai procurar:

1. **Look-ahead bias no sinal:** usar retorno do mês t no ranking do mês t (o sinal deve ser calculado com dados disponíveis no início do período de holding)
2. **Survivorship bias:** usar apenas ações que ainda existem hoje para construir o backtest histórico
3. **Custos ignorados:** momentum tem alto turnover — sem custos de transação, o Sharpe é inflado
4. **Overfitting de janela:** testar muitas janelas e reportar a que melhor funciona sem correção para multiple testing
5. **Rebalanceamento no preço de fechamento:** na prática, você rebalanceia no próximo dia útil ao preço de abertura

---

## Métricas-alvo

Uma estratégia competitiva no desafio deve apresentar:

- Sharpe anualizado > 0.5 (net de custos)
- Max drawdown documentado e discutido
- Comparação explícita com o IBOVESPA (alpha positivo)
- Walk-forward com resultados consistentes (não apenas in-sample)

---

## Evolução da estratégia ao longo das aulas

```
Aula 4  → Sinal v1: retorno 12-1, top N, equal weight
Aula 5  → Backtest v1: métricas básicas (CAGR, Sharpe, DD) vs IBOV (Equal-Weight)
Aula 6  → Alocação: otimização de Markowitz via scipy.optimize (Sharpe máx.)
Aula 7  → Sinal v2: vol-adjusted momentum (sinal v1 / vol rolling 63d)
Aula 8  → Backtest rigoroso: turnover mensal, custos reais (0.3%), retorno líquido
Aula 9  → GenAI, Relatório & Defesa: análise com Claude, PDF do relatório e defesa
```
