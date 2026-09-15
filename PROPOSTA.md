# Proposta de Projeto — Especialização em Deep Learning


## Título

**Construção Incremental de Grafo de Conhecimento a partir de Documentos Legais: estudo comparativo
entre extração direta por LLM, validação semântica e pós-processamento com GraphSAGE**

## Equipe

Filipe Ataíde — filipeataide@gmail.com

## Artigo base

Hamilton, W. L., Ying, R., & Leskovec, J. (2017). **Inductive Representation Learning on Large
Graphs.** NeurIPS 2017. — [arXiv:1706.02216](https://arxiv.org/abs/1706.02216)

## Código base

Repositório oficial dos autores (Stanford, TensorFlow):
<https://github.com/williamleif/GraphSAGE>

O mecanismo do artigo (Algoritmos 1 e 2) foi **reimplementado do zero em PyTorch** e validado com
equivalência numérica exata contra o `SAGEConv` do PyTorch Geometric. Isso atende à exigência de
compreender o código base e resolve a obsolescência do código original de 2017.

## Trabalhos relacionados usados como comparação

| Trabalho | Papel na proposta |
|---|---|
| **iText2KG** (WISE 2024) — [arXiv:2409.03284](https://arxiv.org/abs/2409.03284) | Adversário. Afirma construir KG incremental *"without post-processing"* — a hipótese contrária à desta proposta |
| **CaseLink** (SIGIR 2024) | Referência de domínio (GNN indutivo em documentos jurídicos) e das métricas de ranking |
| **GAT** (ICLR 2018) — [arXiv:1710.10903](https://arxiv.org/abs/1710.10903) | Estabelece a faixa conhecida do GraphSAGE em PPI (`GraphSAGE*` = 0,768) |

---

## Pergunta de pesquisa

> A construção incremental de um grafo de conhecimento a partir de documentos legais se beneficia de
> **validação semântica** e **pós-processamento estrutural (GNN)**, ou a **extração incremental
> direta por LLM** já é suficiente?

Hipóteses:

```
H0: a estrutura do grafo não acrescenta informação além do conteúdo textual dos artigos.
H1: a agregação de vizinhança melhora a recuperação de relações normativas.
```

---

## Desenho experimental

### Três braços

| Braço | Composição | Representa |
|---|---|---|
| 1. Extração direta | GLiNER / LLM → triplas → grafo | a tese do iText2KG |
| 2. + validação semântica | deduplicação, canonicalização, filtro de plausibilidade | pipeline estático com validação |
| 3. + pós-processamento | GraphSAGE propõe arestas faltantes e pontua as implausíveis | arquitetura híbrida |

### Baselines (a hipótese nula)

**BM25** (lexical) e **retrieval denso** (cosseno sobre as features de texto, sem grafo). Este
último corresponde exatamente à linha `Raw features` da Tabela 1 do artigo base — ou seja, a
comparação reproduz o desenho experimental do próprio GraphSAGE.

---

## Dados

### Corpus normativo — ~1.950 artigos, split temporal

| Documento | Publicação | Artigos | Partição |
|---|---|---|---|
| EC 132/2023 | 20/12/2023 | ~20 | treino |
| LC 214/2025 | 16/01/2025 | 499 | treino |
| LC 227/2026 | 13/01/2026 | ~197 | teste indutivo 1 |
| Decreto 12.955/2026 — Regulamento da CBS | 29/04/2026 | 620 | teste indutivo 2 |
| Resolução CGIBS 6/2026 — Regulamento do IBS | 30/04/2026 | 617 | teste indutivo 2 |

Todos os textos são públicos (Planalto e CGIBS). **Nenhum nó de teste existe no grafo de treino** —
a capacidade indutiva é avaliada com documentos que de fato não existiam no momento do treino, sem
simulação artificial de "nó novo".

### Dois níveis de dificuldade

| Tipo de aresta | Dificuldade | Ground truth |
|---|---|---|
| **A** — citação explícita qualificada ("art. 12 da LC nº 214, de 2025") | fácil | regex, automático |
| **C** — relação semântica não escrita em lugar nenhum | difícil | co-citação, automático |

Conjunto adicional (meta esticada): notas técnicas de entidades — CCiF, RFB/CGIBS, CNI, CBIC —
com relações de interpretação em vez de regulamentação. Entra apenas se um levantamento medido
mostrar volume suficiente de arestas.

---

## Métricas

| Camada | Métrica | Comparável a |
|---|---|---|
| Reprodução do baseline (PPI) | micro-F1 | Tabela 1 do artigo base |
| Qualidade das triplas (3 braços) | precisão / recall / F1 | iText2KG |
| Recuperação de arestas | Hits@k, MRR, AUC | CaseLink |
| Custo de manutenção | tempo e chamadas de API por documento novo | argumento prático |

Métricas por época são gravadas em `.csv` para análise posterior.

---

## Infraestrutura

CPU-only para todo o caminho principal (a reprodução do baseline roda em 34 s). Colab com GPU apenas
para o extrator GLiNER e para varreduras de hiperparâmetro. Custo de API estimado entre US$ 12 e
US$ 61 no projeto inteiro, com Batch API e prompt caching.

---

## Estado da reprodução do baseline

Concluída antes de qualquer modificação, conforme exigido.

| Fonte | PPI micro-F1 |
|---|---|
| Artigo original, GraphSAGE-mean | 0,598 |
| **Esta reprodução** | **0,738** |
| GAT (2018), `GraphSAGE*` | 0,768 |

O valor obtido não coincide com o do artigo. Quatro ablações (amostragem, normalização L2,
subamostragem de grau, learning rate) mostraram que a diferença **não** é explicada por desvios de
fidelidade — removê-los aumenta a F1, não reduz. A causa permanece não determinada e está declarada
como tal.

---

## Contribuição proposta

Não se propõe um método novo. Propõe-se um **estudo comparativo** com hipótese falseável, aplicando
três arquiteturas de construção incremental de grafo de conhecimento a um corpus legal real, com
avaliação automática viabilizada por *ground truth* derivado de citações normativas explícitas.

O resultado pode ser negativo — o pós-processamento pode não melhorar a qualidade, ou o BM25 pode
superar os métodos neurais. Nesse caso, o resultado negativo é reportado, não contornado.

---

*Documentação completa em [docs/](docs/). Definição do projeto em [PROJETO.md](PROJETO.md).
Plano de execução em [docs/06-plano-execucao.md](docs/06-plano-execucao.md).*

*Histórico das decisões de escopo em [docs/04-reenquadramento.md](docs/04-reenquadramento.md).*
