# Plano de Execução — 8 semanas

**Criado:** 2026-09-15
**Janela:** 15/09/2026 → ~10/11/2026 (2 meses)
**Entregável final:** relatório de até 8 páginas (Concepção, Experimentação, Análise, Resultado)

> ⚠️ **A data exata de entrega não foi confirmada.** "2 meses" foi a informação dada. Se houver
> data fixa do professor, ajustar todas as semanas abaixo.

---

## 0. Estado atual

### Concluído

| Item | Onde |
|---|---|
| Leitura e auditoria do briefing do professor | `docs/03-requisitos-professor.md` |
| Levantamento e dimensionamento do corpus | `docs/01-levantamento-corpus.md` |
| Reenquadramento para o cenário C (três braços) | `docs/04-reenquadramento.md` |
| Orçamento de API (US$ 12–61 no projeto inteiro) | `docs/05-orcamento-api.md` |
| Ambiente CPU-only funcionando (torch 2.14 + PyG 2.8) | `requirements.txt` |
| **GAP 2 fechado** — reprodução fiel + 4 ablações | `reports/analysis/R02-reproducao-fiel-ppi.md` |
| Agregador mean próprio, equivalência exata com PyG | `src/modeling/sage_manual.py` |
| Amostrador de vizinhança próprio (Algoritmo 2) | `src/modeling/sage_sampler.py` |
| Decisões Q1–Q6 fechadas | `docs/02-decisoes-abertas.md` |

### Arquivos de dado já em disco

- `EC 132/2023` e `LC 214/2025` — HTML do Planalto, baixados e medidos (scratchpad; **mover para `data/raw/`**)
- PPI e Cora — `data/raw/`

---

## 1. Visão geral do cronograma

| Semana | Período | Foco | Risco |
|---|---|---|---|
| **S1** | 15–21 set | Fechar camada de reprodução | Baixo |
| **S2** | 22–28 set | **Ingestão e segmentação do corpus** | **ALTO** |
| **S3** | 29 set – 5 out | Citações, ground truth, verificação manual | **ALTO** |
| **S4** | 6–12 out | Grafo, features, split temporal | Médio |
| **S5** | 13–19 out | Braços 1 e 2 (extração + validação) | Médio |
| **S6** | 20–26 out | Braço 3 + baselines + varreduras | Baixo |
| **S7** | 27 out – 2 nov | Análise, sensibilidade, revisão crítica | Médio |
| **S8** | 3–9 nov | Relatório | Médio |

**Folga real: ~0.** As semanas 2-3 são o gargalo. Se estourarem, o corte é o dataset (b),
já decidido como meta esticada (Q6).

---

## S1 — Fechar a camada de reprodução (15–21 set)

Objetivo: ter a coluna PPI da Tabela 1 do artigo reproduzida no nosso próprio código, para que a
comparação do relatório seja interna e coerente.

### S1.1 — Baseline `Raw features` (MLP sem grafo)

| | |
|---|---|
| **O quê** | MLP de 1 camada oculta sobre `x`, sem nenhuma aresta. Mesmo treino, mesma avaliação |
| **Por quê** | É a linha `Raw features 0,422` do artigo — **e é a hipótese nula do cenário C** (D7). Tê-la no mesmo arcabouço torna a comparação direta |
| **Entregável** | `src/modeling/baseline_features.py` + linha em `R03` |
| **Aceitação** | micro-F1 na faixa de 0,42 ± 0,05. Fora disso, investigar antes de seguir |
| **Custo** | ~2 h |

### S1.2 — Baseline `Random`

| | |
|---|---|
| **O quê** | Predição aleatória respeitando a prevalência por classe |
| **Por quê** | Piso absoluto. Artigo: 0,396. Barato e evita interpretar 0,45 como "bom" |
| **Aceitação** | ~0,396 ± 0,02 |
| **Custo** | ~30 min |

### S1.3 — Relatório R03 consolidando a reprodução

| | |
|---|---|
| **Entregável** | `reports/analysis/R03-tabela1-reproduzida.md` — tabela com Random / Raw features / GraphSAGE-mean, nossos números vs. artigo vs. GAT |
| **Aceitação** | Ordem relativa preservada (Random < Raw features < GraphSAGE). **Se a ordem não bater, há bug** |
| **Custo** | ~2 h |

> **Não fazer nesta semana:** Cora. O D5 já estabeleceu que é transdutivo e não valida a tese.
> Só entra se sobrar tempo na S7, como sanidade adicional.

### S1.4 — Higiene do repositório

- Mover os HTML baixados do scratchpad para `data/raw/planalto/`
- `git init` + primeiro commit (o projeto **não é um repositório git hoje** — sem histórico, sem rollback)
- Congelar versões: `pip freeze > requirements-lock.txt`

---

## S2 — Ingestão e segmentação (22–28 set) ⚠️ RISCO Nº 1

Objetivo: transformar 5 documentos em ~1.950 registros de artigo, com identificador estável.

### S2.1 — Coleta dos 5 documentos

| Documento | Fonte | Formato | Status |
|---|---|---|---|
| EC 132/2023 | planalto.gov.br | HTML | ✅ baixado |
| LC 214/2025 | planalto.gov.br | HTML | ✅ baixado |
| LC 227/2026 | planalto.gov.br | HTML | pendente |
| Decreto 12.955/2026 | planalto.gov.br | HTML | pendente |
| Res. CGIBS 6/2026 | cgibs.gov.br | **PDF** | pendente — o mais arriscado |

**Entregável:** `src/ingestion/coletar.py` + arquivos em `data/raw/`
**Aceitação:** os 5 documentos em disco, com hash registrado (rastreabilidade, `AGENT.MD` §15)

### S2.2 — Segmentação por artigo ⚠️ o trabalho fino

**O problema já medido:** o regex ingênuo achou **598 segmentos para 499 artigos reais** na
LC 214 — superestimação de ~20%.

A causa é estrutural em lei brasileira: uma lei que altera outra **cita artigos alheios no próprio
corpo**, com a mesma formatação:

```
Art. 480. A Lei nº 9.430, de 1996, passa a vigorar com a seguinte redação:
    "Art. 5º  ..............................................."   <- NÃO é artigo da LC 214
```

O segmentador precisa distinguir:
- artigo **próprio** do documento (nó do grafo)
- artigo **citado dentro de uma alteração** (não é nó; é conteúdo)
- **anexos** (excluir — 2 segmentos são 13,2% do corpus e não têm relação normativa)

**Entregável:** `src/cleaning/segmentar.py` → `data/processed/artigos.parquet`
com colunas `id | documento | numero | texto | data_publicacao | tipo`

**Aceitação:**
- contagem por documento dentro de **±5%** do oficial (LC 214: 499, LC 227: ~197, Decreto: 620, Res.: 617)
- inspeção visual de 20 artigos amostrados: cabeçalho e corpo corretos
- nenhum anexo entre os nós

**Risco:** é aqui que o cronograma estoura. **Mitigação:** cronometrar. Se a LC 214 não estiver
segmentada com ±5% até o fim da S2, acionar o plano B (ver §Riscos).

### S2.3 — Extração de citações por regex

Padrões a cobrir:

```
art. 12 da Lei Complementar nº 214, de 2025      -> explícita qualificada  (tipo A)
art. 12, § 2º, inciso III da LC 214/2025          -> explícita com subdivisão (tipo A)
o disposto no caput                               -> relativa (tipo B)
o artigo anterior / § 2º deste artigo             -> relativa (tipo B)
```

**Entregável:** `src/cleaning/extrair_citacoes.py` → `data/processed/arestas_regex.parquet`
**Aceitação:** arestas tipo A produzidas e contadas por documento

---

## S3 — Ground truth e portões de decisão (29 set – 5 out) ⚠️

### S3.1 — Verificação manual da amostra 🧑 **TRABALHO SEU, INDELEGÁVEL**

| | |
|---|---|
| **O quê** | Amostra aleatória de **50 citações** extraídas pelo regex. Para cada uma: a aresta está correta? |
| **Por quê** | Mede a precisão do ground truth. **Todo o experimento depende deste número.** Exige julgamento sobre texto normativo |
| **Entregável** | `reports/analysis/R04-qualidade-ground-truth.md` com precisão medida e intervalo de confiança |
| **Aceitação** | precisão ≥ 0,95. Abaixo disso, corrigir o regex e reamostrar |
| **Custo** | 2–3 h suas |

### S3.2 — Confirmar a estrutura espelhada ⚠️ **PENDENTE DESDE O INÍCIO**

O cenário C depende de uma hipótese ainda não verificada: que o **Decreto 12.955 (CBS)** e a
**Res. CGIBS 6 (IBS)** têm Livro I de normas comuns e regulamentam os mesmos artigos da LC 214.

Isso é a fonte do **ground truth automático do tipo C** (co-citação). Li em fontes secundárias,
**nunca confirmei no texto oficial**.

**Entregável:** contagem de artigos da LC 214 citados por ambos os regulamentos
**Aceitação:** ≥ 100 artigos citados pelos dois → o ground truth tipo C existe
**Se falhar:** o tipo C perde a avaliação automática. Plano B: usar apenas co-citação dentro do
mesmo documento, ou rebaixar o tipo C a análise qualitativa

### S3.3 — 🚦 PORTÃO DE DECISÃO Q6 — dataset (b)

Conforme decidido: baixar as 30 notas do CCiF, extrair datas, rodar o regex e **contar arestas
reais contra o corpus normativo**.

| Resultado | Ação |
|---|---|
| ≥ 100 arestas | (b-mínimo) entra como dataset 2 na S5 |
| < 30 arestas | cortar (b); defender tipos A/C como os dois níveis de dificuldade |
| entre os dois | decisão sua, com o dado na mão |

**Suspeita a confirmar:** ~22 das 30 notas parecem anteriores à LC 214/2025 (citam PEC 45/2019),
o que produziria poucas arestas úteis.

**Custo:** ~2 h

### S3.4 — 🚦 PORTÃO DE CRONOGRAMA

Se S2 e S3 não fecharem até 5/out, executar o plano B do §Riscos. Não seguir para a S4 com a
ingestão quebrada — todo o resto depende dela.

---

## S4 — Grafo, features e split (6–12 out)

### S4.1 — Masking de citações (D6, **obrigatório**)

Substituir toda referência normativa explícita por `<REF>` **antes** de gerar embeddings.

Sem isso a feature do nó contém o rótulo da aresta e qualquer resultado positivo é artefato.

**Aceitação:** teste automatizado — nenhum texto mascarado contém padrão de citação.
Este teste vai para `tests/`.

### S4.2 — Features de nó

- `sentence-transformers` sobre o texto **mascarado**
- Modelo: multilíngue ou português (decidir vendo o texto; `AGENT.MD` §9 — documentar alternativas)
- **Custo:** minutos em CPU para ~1.950 artigos

### S4.3 — Construção do grafo

**Entregável:** `data/processed/grafo.pt` (formato PyG `Data`)
**Aceitação:** relatório de sanidade — nº de nós, arestas, densidade, grau médio, componentes
conexas, nós isolados

### S4.4 — Split temporal (D2)

```
Treino          EC 132 (2023) + LC 214 (jan/2025)
Teste ind. 1    LC 227 (jan/2026)
Teste ind. 2    Decreto 12.955 + Res. CGIBS 6 (abr/2026)
```

**Aceitação:** teste automatizado — nenhum nó de teste aparece no grafo de treino.

### S4.5 — Ground truth tipo C

Co-citação derivada: dois artigos que citam o mesmo artigo-fonte. Retido como teste.

---

## S5 — Braços 1 e 2 (13–19 out)

### S5.1 — Braço 1: extração direta

Dois extratores (Q5 decidiu fazer os dois):

| Extrator | Onde | Custo |
|---|---|---|
| **GLiNER-Relex** | Colab (GPU) | grátis |
| **LLM via API** | local, Batch + cache | ~US$ 6–15 por passada |

**Lembrar das alavancas** (`05-orcamento-api.md`): Batch API −50%, prompt caching −30%,
excluir anexos −13%.

**Entregável:** `data/processed/triplas_braco1_{gliner,llm}.parquet`
**Aceitação:** precisão/recall/F1 contra o ground truth do regex, por extrator

### S5.2 — Braço 2: validação semântica

- deduplicação de entidades (`art. 12 da LC 214` = `artigo 12 da Lei Complementar 214/2025`)
- canonicalização para o identificador do nó
- filtro de plausibilidade (artigo citado existe? número dentro do intervalo do documento?)

**Aceitação:** precisão sobe em relação ao braço 1; recall não deve despencar. Reportar os dois.

### S5.3 — (b-mínimo), se o portão S3.3 autorizar

---

## S6 — Braço 3 e baselines (20–26 out)

### S6.1 — Baselines de recuperação (a hipótese nula, D7)

| Baseline | Implementação |
|---|---|
| **BM25** (lexical) | `rank_bm25`, ~10 linhas |
| **Retrieval denso** | cosseno sobre as features; `numpy`, sem vector DB |

> **Atenção:** o BM25 pode vencer os métodos neurais. Texto normativo tem sobreposição lexical
> altíssima. Se vencer, é o achado mais interessante do relatório (`AGENT.MD` §20).

### S6.2 — Braço 3: GraphSAGE

- **Agregação exata, sem amostragem** — decidido no R02 §8: o grafo tem 1.950 nós, a amostragem
  custaria 8,7 pontos de F1 sem ganho
- Tarefa: predição de link (D9)
- Duas funções: propor arestas faltantes (tipo C) e pontuar arestas implausíveis do braço 1
- **Embedding indutivo do nó novo sem retreino** — a tese. Usar `embed_full()`

**Aceitação:** Hits@k, MRR, AUC contra BM25 e retrieval denso, nos dois incrementos temporais

### S6.3 — Varreduras (GAP 4)

Eixos que vêm do próprio artigo base, portanto comparáveis:

| Eixo | Valores |
|---|---|
| Agregador | mean / max-pool / LSTM |
| Profundidade K | 1, 2, 3 |

Rodar no Colab (paralelizável). Métricas por época em CSV.

---

## S7 — Análise (27 out – 2 nov)

Executar `AGENT.MD` §18 e §19 integralmente.

### S7.1 — Análise de sensibilidade

Classificar cada conclusão como **Robusto / Sensível / Inconclusivo** variando:
- limiar de decisão da predição de link
- modelo de embedding
- estratégia de amostragem negativa
- janela temporal (só incremento 1 vs. os dois)

### S7.2 — Revisão crítica

As quatro frentes do `AGENT.MD` §18: dados, método, resultado, interpretação, comunicação.

### S7.3 — Análise qualitativa

O professor pede análise *"quantitativa E qualitativa"* (slide 8). Inspecionar:
- 10 arestas que o GraphSAGE propôs e o extrator não achou — fazem sentido juridicamente?
- 10 arestas que ele marcou como implausíveis — eram alucinação mesmo?

Esta parte exige seu julgamento e é o que diferencia o relatório de um dump de tabelas.

---

## S8 — Relatório (3–9 nov)

### Estrutura proposta — 8 páginas, mapeada aos 4 pilares

| Seção | Páginas | Pilar |
|---|---|---|
| 1. Problema e pergunta de pesquisa | 0,75 | **Concepção** |
| 2. Artigo base e trabalho relacionado (GraphSAGE, iText2KG, CaseLink) | 0,75 | **Concepção** |
| 3. Reprodução do baseline sem modificações + ablações | 1,25 | **Experimentação** |
| 4. Corpus, grafo e qualidade dos dados | 1,0 | **Experimentação** |
| 5. Os três braços e o protocolo de avaliação | 1,0 | **Experimentação** |
| 6. Resultados quantitativos | 1,5 | **Resultado** |
| 7. Análise qualitativa, sensibilidade e limitações | 1,25 | **Análise** |
| 8. Conclusão e trabalho futuro (ponte para o TCC) | 0,5 | **Resultado** |

### Pontos que precisam estar explícitos no texto

1. **A reprodução dá 0,738 contra 0,598 do artigo.** Declarar, com a faixa do `GraphSAGE*` (0,768)
   do artigo do GAT, e dizer que a causa não foi determinada. Não esconder.
2. **Os datasets não são os do artigo base** (GAP 1). Declarar a estrutura de dois níveis:
   reprodução (PPI) para comparação externa, aplicação (Reforma) para comparação interna.
3. **As métricas divergem do artigo base** (GAP 5) porque a tarefa mudou; justificar pelo CaseLink.
4. **Resultados negativos preservados** — se o BM25 vencer, ou se o braço 3 não superar o braço 2,
   isso vai no relatório como resultado.

---

## Registro de riscos

| # | Risco | Prob. | Impacto | Mitigação | Plano B |
|---|---|---|---|---|---|
| **R1** | Segmentação por artigo não fecha em ±5% | **Alta** | **Crítico** | Cronometrar; portão em 5/out | Reduzir para 2 documentos (LC 214 + Decreto 12.955) ≈ 1.119 artigos. Ainda suficiente |
| **R2** | PDF da Res. CGIBS 6 não extrai texto limpo | Média | Alto | Testar cedo, na S2.1 | Cortar a Resolução; usar só fontes HTML do Planalto |
| **R3** | Estrutura espelhada não se confirma (S3.2) | Média | Alto | Verificar na S3 | Tipo C vira análise qualitativa em vez de métrica |
| **R4** | Precisão do regex < 0,95 | Baixa | **Crítico** | Medir na S3.1 | Restringir aos padrões de maior precisão, aceitando recall menor |
| **R5** | Notas CCiF rendem poucas arestas | **Alta** | Baixo | Já previsto no portão Q6 | Cortar (b) — já decidido |
| **R6** | Braço 3 não supera o braço 2 | Média | **Nenhum** | — | É um resultado válido. `AGENT.MD` §20 |
| **R7** | 8 páginas não cabem | Média | Médio | Escrever a estrutura na S7, não na S8 | Mover detalhe de implementação para apêndice/anexo |

---

## O que é indelegável (não pode ir para agente)

1. **Verificação da amostra de citações** (S3.1) — julgamento sobre texto normativo
2. **Análise qualitativa das arestas** (S7.3) — é o que dá substância ao pilar Análise
3. **Entender o artigo do GraphSAGE** — exigência explícita do slide 6; a implementação própria em
   `sage_manual.py` e `sage_sampler.py` existe para apoiar isso, não para substituir a leitura
4. **Escrever o relatório** — na sua voz, defensável em arguição

---

## Próxima ação concreta

**S1.1 — baseline `Raw features`.** ~2 h, destrava a tabela de reprodução completa, e é a mesma
hipótese nula que o cenário C reutiliza.

Antes disso, **`git init`** — o projeto hoje não tem controle de versão, e a partir da S2 vamos
mexer em pipeline de dados onde rollback importa.
