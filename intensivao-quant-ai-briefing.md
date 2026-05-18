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

### Formato de cada aula (2h)

Cada aula alterna entre células markdown (teoria, motivação, contexto) e células de código (implementação). A teoria não existe separada do código — ela aparece como narração do que está sendo construído, no momento em que o código precisa dela.

Exemplo do que isso parece:

```
[markdown] Retorno log vs simples — por que usamos log?
[código]   df['ret_log'] = np.log(df['close'] / df['close'].shift(1))
           df['ret_sim'] = df['close'].pct_change()
[markdown] Para retornos diários a diferença é mínima. Para acumulado, diverge.
[código]   plot comparando os dois acumulados
```

**Distribuição de tempo por aula:** ~1h teoria (via markdown + explicação ao vivo) / ~1h codificação ativa.

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

## 4. Estrutura das 10 aulas

### Sprint 1 — Construir os trilhos (Semanas 1–2)

| # | Tema | Teoria do dia | O que Felipe constrói ao vivo | Replica em casa |
|---|---|---|---|---|
| 1 | Kick-off | O que é estratégia quant; os 7 critérios e pesos; o que é momentum (intuitivo); o que separa backtest honesto de ruim | Preview do produto final (mostrar o backtest da aula 5 pronto) | Instalar ambiente, clonar repo |
| 2 | Setup + dados | Série temporal de preços; retorno simples vs log; dividendos e splits; janelas de tempo | Baixar tickers do IBOV, montar DataFrame de retornos diários, primeiro plot | Rodar o notebook, explorar os dados |
| 3 | EDA + limpeza | Esperança e variância; distribuição de retornos (fat tails, curtose, assimetria); estacionariedade; autocorrelação; lei dos grandes números; por que filtrar liquidez | Tratar missing data, filtro de liquidez, distribuição dos retornos, rolling stats | EDA documentada do próprio dataset |
| 4 | Sinal v1 | Probabilidade condicional como fundamento do momentum; Jegadeesh & Titman 1993; cross-seccional vs time-series; por que janela 12-1; long-only vs long-short | Calcular sinal 12-1, ranquear ativos, selecionar top N, equal weight | Testar parâmetros diferentes (janela, N) |

### Sprint 2 — Sofisticar e validar (Semanas 3–4)

| # | Tema | Teoria do dia | O que Felipe constrói ao vivo | Replica em casa |
|---|---|---|---|---|
| 5 | Backtest v1 | Retorno acumulado; Sharpe ratio (derivação intuitiva, anualização); drawdown e max drawdown; alpha e beta | Backtest vetorizado, curva de capital, métricas vs IBOV | Gerar as métricas do próprio backtest |
| 6 | Alocação | Álgebra linear: portfólio como produto de vetores (`w · r`), variância como `wᵀΣw`; Markowitz (intuitivo); por que equal weight frequentemente vence; risk parity | Trocar equal weight por signal-weighted, calcular `wᵀΣw`, comparar abordagens | Testar risk parity como alternativa |
| 7 | Sinal v2 | Volatilidade e o que mede; rolling statistics; por que normalizar sinal por vol; o que é turnover | Dividir sinal por volatilidade rolling (vol-adjusted momentum), comparar v1 vs v2 | Comparar sinal v1 vs v2 no próprio backtest |
| 8 | Backtest rigoroso | Look-ahead bias; overfitting; multiple testing e p-value; deflated Sharpe (intuitivo); custos reais de transação; walk-forward | Adicionar custos, implementar walk-forward, discutir significância estatística | Rodar bateria completa de métricas |

### Sprint 3 — Fechar (Semana 5)

| # | Tema | Teoria do dia | O que Felipe constrói ao vivo | Replica em casa |
|---|---|---|---|---|
| 9 | GenAI + análise | Como LLMs funcionam (5 min); onde GenAI entra no processo quant; como escrever prompts técnicos; visualizações que a banca quer ver | Usar Claude para redigir seção de análise, gerar visualizações para o relatório | Rascunho das seções 1–4 do relatório |
| 10 | Relatório + defesa | Como a banca avalia pelos 7 critérios; por que o que NÃO funcionou conta; como defender escolhas metodológicas | Revisão cruzada ao vivo — cada equipe apresenta 5 min, Felipe comenta | Relatório quase final |

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

- **Janela:** 5 semanas, 10 aulas, 2h cada (20h totais).
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
