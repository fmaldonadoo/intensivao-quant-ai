# Intensivão Quant AI — Briefing de reformulação

> Documento de trabalho para reformular o intensivão da Diretoria de Quant da ImpactUFSCar. Abordagem: live coding centrada na construção de uma estratégia real do Desafio Quant AI do Itaú. Auto-contido o suficiente para que outra instância de Claude consiga continuar a partir daqui.

---

## 1. Contexto resumido

**Entidade.** ImpactUFSCar — entidade estudantil da UFSCar focada em Quantitative Finance, AI Safety e Sistemas Complexos. Após o PSel 2026.1, tem cerca de 25 membros.

**Quem conduz.** Felipe Maldonado — Vice-Presidente e líder técnico da Diretoria de Quant. Formação em economia com ênfase em métodos quantitativos, séries temporais e mercados financeiros. Trabalha profissionalmente com pesquisa de ETFs.

**Objetivo do intensivão.** Preparar ~25 membros distribuídos em 7 equipes para o Desafio Quant AI da Itaú Asset Management. Benchmark interno: na edição anterior, uma equipe ficou em 15º entre mais de 900 equipes.

**O que o desafio avalia (pesos exatos — edital 2025).**

| Critério | Peso |
|---|---|
| Conceito da Estratégia | 20% |
| Modelagem | 20% |
| Uso de IA Generativa | 15% |
| Backtest | 15% |
| Análise dos Resultados | 15% |
| Conclusão e Próximos Passos | 10% |
| Apresentação do Robô (nome e identidade) | 5% |

A organização valoriza processo e rigor acima do retorno bruto. Um robô que rendeu menos, modelado com rigor, vence um que rendeu mais com backtest mal-feito.

---

## 2. Formato do intensivão

### Abordagem: live coding com replicação em casa

Felipe constrói uma estratégia quantitativa real do zero ao longo das 10 aulas, ao vivo, explicando cada decisão enquanto escreve. Os alunos assistem e replicam em casa no próprio repositório.

**Não é** aula expositiva seguida de exercício. É o instrutor mostrando a cozinha — a tese vira código, o código vira backtest, o backtest vira relatório.

### Formato de cada aula (60 min)

Cada aula alterna entre células markdown (teoria, motivação, contexto) e células de código (implementação). A teoria não existe separada do código — ela aparece como narração do que está sendo construído, no momento em que o código precisa dela.

Exemplo do que isso parece:

```
[markdown] Retorno log vs simples — por que usamos log?
[código]   df['ret_log'] = np.log(df['close'] / df['close'].shift(1))
           df['ret_sim'] = df['close'].pct_change()
[markdown] Para retornos diários a diferença é mínima. Para acumulado, diverge.
[código]   plot comparando os dois acumulados
```

**Distribuição de tempo por aula:** 20 minutos de teoria intuitiva (visuais claros, matemática simplificada e conceitual) / 40 minutos de codificação ativa (passo a passo detalhado).

### Material principal

O **notebook de cada aula** é o material principal — não uma apostila separada. Cada notebook é auto-contido o suficiente para o aluno mais fraco conseguir replicar em casa sem o instrutor do lado. Isso exige que as células markdown sejam narrativas claras, não apenas títulos.

---

## 3. A estratégia — Momentum Cross-Seccional no IBOVESPA

### Decisão fechada

Todas as 7 equipes constroem a **mesma estratégia** que Felipe constrói ao vivo: momentum cross-seccional em ações do IBOVESPA.

### Por que momentum

- Tese intuitiva ("ações que subiram mais tendem a continuar subindo") — acessível para alunos sem bagagem
- Progressão natural ao longo das 10 aulas: sinal simples → filtros → alocação → backtest rigoroso
- Dados gratuitos via `yfinance`, sem dependência de API paga
- O 1º lugar de 2024 ("Persistence") usou momentum — validação pela banca
- Espaço natural para GenAI entrar (análise, documentação, interpretação de resultados)

### Especificação

- **Universo:** componentes do IBOVESPA
- **Sinal base:** retorno acumulado 12-1 meses (janela de 12 meses, skip 1 mês)
- **Lógica:** ranquear ativos pelo sinal, alocar nos top N
- **Refinamento (Aula 7):** normalizar sinal por volatilidade rolling

---

## 4. Estrutura das 9 aulas (60 min: 20m Teoria + 40m Código)

### Sprint 1 — Construir os trilhos (Semanas 1–2)

| # | Tema | Teoria do dia (20 min) | O que Felipe constrói ao vivo (40 min) | Replica em casa |
|---|---|---|---|---|
| 1 | Kick-off | O que é estratégia quant; os 7 critérios e pesos do Itaú; o que é momentum; o que separa backtest honesto de ruim. | Apresentação do produto final (ver o backtest da aula 5 funcionando) | Instalar ambiente, clonar repo. |
| 2 | Setup + dados | Universo IBOVESPA; pipeline de dados; dividendos/splits de forma simples; sobrevivência (survivorship bias) intuitiva. | Coleta real via `yfinance` (2012-2024), forward-fill e Parquet (`dados/precos_ibov.parquet`). | Rodar o notebook, explorar os dados. |
| 3 | EDA + limpeza | Média, desvio padrão, assimetria, curtose. Por que retornos de ações reais têm caudas pesadas e a Normal falha. | Plotar histograma + QQ-Plot vs. Normal. Scatter plot de Risco vs Retorno. Heatmap de correlações setoriais simples. | EDA documentada do próprio dataset. |
| 4 | Sinal v1 — Momentum | Jegadeesh & Titman 1993; por que janela 12-1 e skip do mês recente; Information Coefficient (IC) de Spearman. | Calcular sinal 12-1 em pandas, ranking percentil cross-seccional (`.rank(pct=True)`), calcular/plotar IC. | Testar parâmetros diferentes de janela e N. |
| 5 | Backtest v1 | Simulação sem look-ahead bias; por que usar `weights.shift(1)`; CAGR e Sharpe Ratio explicados detalhadamente. | Selecionar Top 10 ativos, portfólio Equal-Weight, curva de capital acumulada, Sharpe, Max Drawdown vs. IBOVESPA. | Gerar as métricas do próprio backtest. |

### Sprint 2 — Sofisticar e validar (Semanas 3–4)

| # | Tema | Teoria do dia (20 min) | O que Felipe constrói ao vivo (40 min) | Replica em casa |
|---|---|---|---|---|
| 6 | Alocação — Markowitz | Teoria Moderna de Portfólio (1952); trade-off risco-retorno; instabilidade prática de Markowitz; restrições long-only e caps. | Implementar otimização de Markowitz para Sharpe máx. via `scipy.optimize.minimize`. Comparar curvas e turnover vs EW. | Testar otimização com limites diferentes por ativo. |
| 7 | Sinal v2 — Vol-Adjusted | Momentum Crashes (Daniel & Moskowitz 2016); por que momentum compra alto beta em bolhas; normalização por vol rolling. | Calcular vol rolling de 63d, sinal v2 (retorno 12-1 / vol). Comparar IC e drawdown de v1 vs v2. | Comparar v1 vs v2 no próprio backtest. |
| 8 | Backtest rigoroso | Look-ahead bias avançado, turnover mensal, custos reais de transação (0.3% corretagem/taxas/slippage). | Calcular turnover mensal ($\sum \|w_t - w_{t-1}\| / 2$), aplicar drag de 0.3%, simular curva de retorno líquida. | Rodar bateria completa de métricas líquidas. |

### Sprint 3 — Fechar e Apresentar (Semana 5)

| # | Tema | Teoria do dia (20 min) | O que Felipe constrói ao vivo (40 min) | Replica em casa |
|---|---|---|---|---|
| 9 | GenAI, Relatório & Defesa | Como a banca do Itaú avalia pelos 7 critérios; uso prático de LLMs (Claude) para redação técnica, análise crítica e pitch. | Criar prompts estruturados para Claude analisar métricas líquidas, gerar narrativa de risco e estruturar o PDF do relatório. | Rascunho final do relatório e pitch de 5 min. |

**Pós-intensivão (Junho–Agosto).** Mentoria quinzenal por equipe até a entrega. Dois checkpoints internos: backtest funcionando (mid-julho) e relatório em rascunho (início de agosto).

---

## 5. Decisões fechadas

| Decisão | Resolução |
|---|---|
| Estratégia | Momentum cross-seccional no IBOVESPA |
| Teses | Única — todas as equipes seguem a mesma estratégia |
| Composição das equipes | Dirigida pela Diretoria, com ≥1 âncora técnica por equipe |
| Formato das aulas | Live coding — Felipe constrói ao vivo, alunos replicam em casa |
| Material principal | Notebooks (teoria via markdown cells, código integrado) |
| Stack | Python + `yfinance`, `pandas`, `numpy`, `statsmodels`, `vectorbt`, `matplotlib` |
| Versionamento | GitHub — 1 repo central do intensivão + 1 repo por equipe |
| Idioma | Português brasileiro em tudo |

---

## 6. Constraints fixos

- **Janela:** 5 semanas, 9 aulas, 1h cada (9h totais).
- **Início recomendado:** semana de 18/05/2026, para ganhar uma semana antes do kick-off oficial do Itaú em 26/05/2026.
- **Entrega final do relatório:** 17/08/2026.
- **Calendário UFSCar 2026/1:** período termina em 18/07; recesso 21/07–16/08; período 2026/2 começa em 17/08 — dia da entrega.
- **Composição da turma:** ~25 membros, 7 equipes. Mix de trainees recém-chegados e membros mais avançados. O aluno mais fraco tem Python básico e pouca bagagem estatística.

---

## 7. Material a produzir (ordem de prioridade)

1. **Estrutura do repositório** — esqueleto de pastas e READMEs
2. **Notebook de cada aula** — o artefato principal; começar pela Aula 1
3. **README da estratégia momentum-ibovespa** — tese, especificação, riscos de modelagem
4. **Handbook do projeto** — referência consultável pelo aluno entre aulas (glossário, receitas, estrutura do relatório)
5. **Plano de mentoria pós-intensivão** — cadência, checkpoints, o que o mentor faz em cada sessão

---

## 8. Riscos identificados

| Risco | Probabilidade | Mitigação |
|---|---|---|
| Aluno mais fraco não consegue replicar em casa | Alta | Células markdown narrativas; ambiente Colab nas primeiras aulas; âncora técnica por equipe |
| Equipes em estágios muito diferentes | Alta | Checkpoints ao fim de cada Sprint; monitoria entre aulas |
| Instrutor sobrecarregado — todas as equipes mesma estratégia, dúvidas em série | Média | Mesma estratégia reduz variedade de dúvidas; notebook auto-contido reduz dependência do instrutor |
| Recesso UFSCar (21/07–16/08) coincide com sprint de polimento | Certo | Mentoria quinzenal estruturada com dois checkpoints antes da entrega |
| Datas oficiais do desafio 2026 ainda não confirmadas | Certo | Ajustar cronograma após kick-off de 26/05/2026 |

---

## 9. Notas para o Claude Code

- Felipe trabalha melhor com outputs tangíveis (arquivos, código, planos concretos). Proponha uma versão e itere — não monte listas de opções sem uma recomendação clara.
- Nível do aluno mais fraco: Python básico, Git introdutório, probabilidade intuitiva. As células markdown dos notebooks precisam ser acessíveis para esse nível.
- Identidade visual da entidade: paleta vinho/bege/branco-creme, tipografia serif para títulos, sem-serifa para corpo.
- Princípio que sobrevive à reformulação: **"o intensivão é a largada, não a linha de chegada"**. Os alunos não saem com o robô pronto — saem capazes de construir o robô com mentoria nos meses seguintes.
- Consultar sempre a data atual antes de propor datas específicas (hoje: 17/05/2026 — kick-off do Itaú em 26/05/2026).
