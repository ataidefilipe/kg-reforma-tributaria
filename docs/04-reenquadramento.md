# Reenquadramento do Projeto — Alinhamento com o TCC

**Data:** 2026-09-15
**Motivo:** o projeto da disciplina passa a ser explicitamente um ensaio para o TCC de mestrado.

---

## 1. Contexto novo

**Pergunta do TCC:**

> Uma arquitetura híbrida baseada em LLMs, validação semântica e pós-processamento de grafos melhora
> a qualidade da construção incremental de knowledge graphs corporativos a partir de POPs sintéticos,
> quando comparada a abordagens de extração direta e ao pipeline estático com validação?

**Três braços de comparação do TCC:**

| Braço | Composição |
|---|---|
| 1. Extração direta | LLM extrai triplas → grafo |
| 2. Pipeline estático com validação | extração + validação semântica |
| 3. Híbrido | extração + validação + **pós-processamento de grafos** |

**Restrições da disciplina:** 2 meses · entregável = relatório (≤8 páginas) · desenvolvimento assistido por agentes.

---

## 2. Diagnóstico do plano atual

O plano atual (GraphSAGE + predição de link + baseline de recuperação) cobre **apenas o braço 3** do TCC,
e mesmo assim de forma indireta. Não toca em extração por LLM nem em validação semântica.

Se o objetivo é usar a disciplina como ensaio do TCC, o plano atual **treina a habilidade errada**.

---

## 3. Achado central da pesquisa

**[iText2KG (WISE 2024, arXiv 2409.03284)](https://arxiv.org/abs/2409.03284)** — construção **incremental**
de KG com LLMs. Código oficial dos autores: <https://github.com/AuvaLab/itext2kg>.

O abstract afirma literalmente:

> "we propose iText2KG, a method for incremental, topic-independent KG construction **without post-processing**"

E justifica dizendo que abordagens existentes geram "inconsistent graphs and requiring extensive post-processing".

**Isto é a tese contrária à do TCC.** O TCC hipotetiza que validação semântica + pós-processamento de grafos
*melhoram* a qualidade; o iText2KG afirma que o pós-processamento é dispensável.

Ter um artigo recente, com código oficial, que sustenta a hipótese nula do TCC é o melhor cenário possível
para um estudo comparativo — dá um adversário concreto em vez de um straw man.

**A literatura do tema é ativa** (responde ao slide 7 do professor):
- [Refining Noisy Knowledge Graph with LLMs (ACL GenAIK 2025)](https://aclanthology.org/2025.genaik-1.9/)
- [Less is More: Denoising Knowledge Graphs for RAG (arXiv 2510.14271)](https://arxiv.org/pdf/2510.14271)
- [Are LLMs Better GNN Helpers? (arXiv 2510.01910)](https://arxiv.org/html/2510.01910v1)

---

## 4. Opções avaliadas

| | Opção | Alinhamento TCC | Requisitos do professor | Veredito |
|---|---|---|---|---|
| **A** | Manter GraphSAGE + baseline de recuperação (plano atual) | Fraco — só o braço 3 | Bom após correções | Insuficiente para o novo objetivo |
| **B** | Trocar base para iText2KG (LLM no núcleo) | Forte | **Ruim** — método zero-shot, sem treino, sem épocas, sem CSV de métricas; reprodução exige API paga; avaliação parcialmente qualitativa | Rejeitado |
| **C** | **Reenquadrar: três braços, GraphSAGE como pós-processamento** | **Forte — espelha o TCC 1:1** | **Bom** — estudo comparativo + treino com épocas + base reproduzível de graça | **Recomendado** |
| **D** | Trocar para GNN temporal (TGN, EvolveGCN) | Moderado | Bom, mas mais pesado | Rejeitado — não toca extração nem validação |
| **E** | Trocar domínio para POPs sintéticos | = fazer o TCC direto | **Ruim** — relações sintéticas não são genuínas (mesmo problema já identificado com o Persona Hub); sem comparação externa | Rejeitado — e queima a novidade do TCC |

---

## 5. Opção C — desenho proposto

### Pergunta de pesquisa

> A construção incremental de um grafo de conhecimento a partir de documentos legais se beneficia de
> validação semântica e pós-processamento estrutural (GNN), ou a extração incremental direta por LLM
> já é suficiente?

Mesma pergunta do TCC, com corpus real (Reforma Tributária) no lugar de POPs sintéticos.

### Três braços — espelham o TCC

| Braço | Composição | Representa |
|---|---|---|
| **1. Extração direta** | GLiNER/LLM → triplas → grafo | a tese do iText2KG |
| **2. Estático com validação** | + deduplicação, canonicalização de entidades, filtro de plausibilidade | validação semântica |
| **3. Híbrido** | + GraphSAGE prediz arestas faltantes e pontua arestas implausíveis | pós-processamento de grafos |

### Ground truth — o ponto que viabiliza 2 meses

Citações normativas explícitas ("nos termos do art. 12 da Lei Complementar nº 214, de 2025") são
extraíveis por **regex** com precisão próxima de 100% em texto legal brasileiro.

**Consequência:** o ground truth é gerado automaticamente. A avaliação dos três braços é automática.
Elimina-se o gargalo de rotulagem manual, que era o maior risco de cronograma.

O trabalho manual reduz-se a **verificar uma amostra (~50 citações) para medir a precisão do regex** —
algumas horas, e vira uma tabela de qualidade de dados no relatório (`AGENT.MD` §5).

> **Atenção — o masking continua obrigatório.** Se a citação está no texto e também é o rótulo, a feature
> do nó contém a resposta. Mascarar antes de gerar embeddings. Ver `01-levantamento-corpus.md` §3.3.

### Métricas

| Camada | Métrica | Comparável a |
|---|---|---|
| Reprodução (PPI) | micro-F1 | Tabela 1 do artigo GraphSAGE |
| Qualidade das triplas (3 braços) | precisão / recall / F1 contra o ground truth | iText2KG e a literatura de construção de KG |
| Recuperação de arestas | Hits@k, MRR, AUC | CaseLink (SIGIR 2024) |
| Custo | tempo e chamadas de API por documento novo | argumento prático de manutenção incremental |

### Papéis dos artigos

| Artigo | Papel |
|---|---|
| **GraphSAGE (NeurIPS 2017)** | **Base a reproduzir** — reproduzível de graça (92 s em CPU), fornece o laço de treino com épocas que o professor espera |
| **iText2KG (WISE 2024)** | Referência recente + **adversário** do estudo comparativo; sustenta a hipótese nula |
| **CaseLink (SIGIR 2024)** | Justifica domínio jurídico + métricas de ranking |

Mantém GraphSAGE como base única a reproduzir (slide 6 fala em artigo/código base no singular) e resolve
a objeção "o artigo é de 2017" trazendo o iText2KG como camada recente.

### Como cada GAP é resolvido

| GAP | Resolução |
|---|---|
| **GAP 1** (datasets não são da literatura) | Camada de reprodução (PPI) mantém comparação externa; camada de aplicação compara três braços internamente |
| **GAP 2** (fidelidade e domínio do código base) | Inalterado — reescrever com `NeighborLoader` + agregação manual validada contra `SAGEConv`. **Já aprovado** |
| **GAP 3** (inovação fraca) | **Resolvido** — vira estudo comparativo de três braços contra um artigo de 2024 que afirma o contrário |
| **GAP 4** (sem alternativas de evolução) | Os três braços *são* as alternativas; + agregador (mean/max/LSTM) e profundidade K, ambos do artigo base |
| **GAP 5** (métricas divergem) | Camada dupla: micro-F1 na reprodução, ranking + P/R/F1 na aplicação, justificado por CaseLink e iText2KG |

---

## 6. Cronograma — 2 meses

| Semana | Entrega | Risco |
|---|---|---|
| 1 | Reprodução fiel do GraphSAGE (NeighborLoader + agregação manual + convergência) | Baixo — parcialmente feito |
| 2-3 | Ingestão dos ~1.950 artigos (HTML Planalto + PDF CGIBS) + regex de citações + verificação da amostra | **Alto — ver §7** |
| 4 | Construção do grafo + masking + embeddings + split temporal | Médio |
| 5 | Braços 1 e 2 (extração + validação) | Médio |
| 6 | Braço 3 (GraphSAGE) + varredura de agregador/profundidade | Baixo |
| 7 | Análise, sensibilidade, revisão crítica (`AGENT.MD` §18-19) | Médio |
| 8 | Relatório | Médio |

**Dataset (b) — notas técnicas do CCiF — passa a ser meta esticada**, não escopo central. Se as semanas 2-3
estourarem, corta-se (b) sem comprometer o projeto: o dataset (a) já tem dois níveis de dificuldade
(citações explícitas vs. relações implícitas entre artigos).

---

## 7. Pushback sobre o cronograma

> "vai ser desenvolvimento usando agentes, então é mais rápido"

Parcialmente verdade. Agentes aceleram escrever código. **Não aceleram:**

1. **Ingestão dos documentos** — parsing de HTML do Planalto e PDF do CGIBS para 1.950 artigos com
   segmentação correta é trabalho sujo e imprevisível. É o risco nº 1 do cronograma, e agentes iteram
   rápido mas ainda dependem de inspeção humana do resultado.
2. **Você entender o artigo do GraphSAGE.** O professor exige isso explicitamente (slide 6) e é
   indelegável.
3. **Escrever o relatório** — 8 páginas na sua voz, defendendo escolhas que você precisa conseguir
   sustentar em arguição.
4. **Verificar a amostra do regex** — exige seu julgamento sobre texto normativo.

Com o dataset (b) como meta esticada, 2 meses é viável. Sem esse corte, é apertado.

---

## 8. Decisões que são suas

**Q4 — Adotar a Opção C?** É a recomendação. Amplia o escopo em relação ao plano atual (três braços em
vez de um), mas é o que converte a disciplina em ensaio real do TCC.

**Q5 — Qual extrator no braço 1?** GLiNER (grátis, roda em Colab) ou LLM via API (fiel ao TCC, custa tokens).
Recomendo **ambos**, se o orçamento permitir: vira mais um eixo de comparação, e o TCC é sobre LLMs.
Se houver restrição de custo, GLiNER sozinho resolve a disciplina.

**Q6 — Confirmar o corte do dataset (b) para meta esticada.** Decisão de priorização, portanto sua.
