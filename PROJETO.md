# Projeto de Deep Learning — Disciplina (Mestrado)

**Última revisão:** 2026-09-15

> **Aviso de versão.** Este documento foi reescrito em 15/09/2026. A versão anterior descrevia um
> projeto de escopo menor (só GraphSAGE + predição de link) e um corpus desatualizado — foi escrita
> quando o PLP 108/2024 ainda tramitava e os regulamentos do IBS/CBS não existiam. O que mudou e por
> quê está em [docs/04-reenquadramento.md](docs/04-reenquadramento.md). A versão original permanece
> no histórico do git. O brainstorm inicial está em
> [outras-ideias/](outras-ideias/) e foi marcado como desconsiderado.

---

## 1. Pergunta de pesquisa

> A construção incremental de um grafo de conhecimento a partir de documentos legais se beneficia de
> **validação semântica** e **pós-processamento estrutural (GNN)**, ou a **extração incremental
> direta por LLM** já é suficiente?

O domínio é a Reforma Tributária brasileira: corpus público, delimitado, com relações genuínas
(uma lei de fato regulamenta uma emenda; um regulamento de fato cita um artigo) e cronologia real
que permite testar chegada incremental de documentos sem simulação artificial.

### Relação com o TCC

Este projeto é ensaio metodológico para a pergunta do TCC:

> Uma arquitetura híbrida baseada em LLMs, validação semântica e pós-processamento de grafos melhora
> a qualidade da construção incremental de knowledge graphs corporativos a partir de POPs sintéticos,
> quando comparada a abordagens de extração direta e ao pipeline estático com validação?

Mesma estrutura de três braços, corpus real no lugar de POPs sintéticos. A intenção é descobrir
agora — com dado público, em dois meses — onde cada braço quebra.

---

## 2. Desenho experimental

### Três braços

| Braço | Composição | Acha tipo A | Acha tipo B | Acha tipo C |
|---|---|---|---|---|
| **1. Extração direta** | GLiNER / LLM → triplas | quase tudo | parcial | **não** |
| **2. + validação semântica** | dedup, canonicalização, filtro | melhor | melhor | **não** |
| **3. + pós-processamento** | GraphSAGE sobre o grafo do braço 2 | igual ao 2 | igual ao 2 | **sim** |

### Baselines — a hipótese nula

As features de nó já são embeddings de texto. Logo, recuperação sobre elas é a hipótese nula exata:

```
H0: a estrutura do grafo não acrescenta informação além do conteúdo textual dos artigos.
H1: a agregação de vizinhança melhora a recuperação de relações normativas.
```

Comparadores: **BM25** (lexical) e **retrieval denso** (cosseno sobre as features).

O artigo base faz essa mesma comparação: a linha `Raw features` da Tabela 1 é precisamente esse
baseline, e o próprio artigo reporta o ganho da estrutura sobre ela (+45% em PPI supervisionado).
Nosso desenho reproduz o desenho experimental do artigo base, não inventa um.

> **Alerta registrado:** o BM25 pode vencer os métodos neurais. Texto normativo tem sobreposição
> lexical altíssima e vocabulário padronizado. Se vencer, é o achado mais interessante do relatório,
> não um problema a contornar (`AGENT.MD` §20).

---

## 3. Dados

### Corpus normativo — ~1.950 artigos

| Documento | Publicação | Artigos | Partição temporal |
|---|---|---|---|
| EC 132/2023 | 20/12/2023 | ~20 | treino |
| LC 214/2025 | 16/01/2025 | 499 | treino |
| LC 227/2026 (ex-PLP 108/2024) | 13/01/2026 | ~197 | teste indutivo 1 |
| Decreto 12.955/2026 — Regulamento da CBS | 29/04/2026 | 620 | teste indutivo 2 |
| Resolução CGIBS 6/2026 — Regulamento do IBS | 30/04/2026 | 617 | teste indutivo 2 |

**Granularidade do nó: artigo** (decisão D1). Nível-documento daria ~6 nós, insuficiente para GNN.

**Split temporal** (decisão D2). Split aleatório vazaria informação e invalidaria a tese indutiva.

### Dois níveis de dificuldade

Exigência do slide 9 do professor, atendida dentro do próprio corpus normativo:

| Tipo de aresta | Dificuldade | Ground truth |
|---|---|---|
| **A** — citação explícita qualificada | fácil | regex, precisão ~100% (a medir) |
| **C** — relação semântica não escrita | difícil | co-citação entre os dois regulamentos |

### Dataset (b) — meta esticada

Notas técnicas de entidades (CCiF, RFB/CGIBS, CNI, CBIC). **Fora do caminho crítico** (decisão Q6).
Vira decisão medida na semana 3: contar quantas arestas reais as 30 notas do CCiF produzem contra o
corpus normativo. ≥100 → entra como `(b-mínimo)`; <30 → corta.

---

## 4. Artigo e código base

| Papel | Trabalho | Por quê |
|---|---|---|
| **Base a reproduzir** | GraphSAGE (NeurIPS 2017) | Reproduzível de graça em 34 s; fornece o laço de treino com épocas que a disciplina espera; é o método indutivo fundador |
| **Adversário** | iText2KG (WISE 2024) | Afirma construir KG incremental *"without post-processing"* — a tese contrária à nossa |
| **Domínio e métricas** | CaseLink (SIGIR 2024) | GNN indutivo em documentos jurídicos; justifica as métricas de ranking |
| **Faixa de referência** | GAT (ICLR 2018) | Reporta `GraphSAGE*` = 0,768 em PPI, contra 0,598 do artigo original |

### Passo obrigatório — cumprido

O slide 6 exige reproduzir o artigo base **sem modificações** antes de qualquer alteração.
Concluído: ver [reports/analysis/R02-reproducao-fiel-ppi.md](reports/analysis/R02-reproducao-fiel-ppi.md).

O mecanismo do artigo foi **reimplementado do zero** (`sage_manual.py`, `sage_sampler.py`) e validado
com equivalência exata contra o `SAGEConv` do PyG. Isso atende também à exigência do mesmo slide de
"ser capaz de entender razoavelmente bem o artigo/código base".

---

## 5. Métricas

Camada dupla, porque a tarefa da aplicação não é a mesma do artigo base:

| Camada | Métrica | Comparável a |
|---|---|---|
| Reprodução (PPI) | micro-F1 | Tabela 1 do GraphSAGE |
| Qualidade das triplas (3 braços) | precisão / recall / F1 | iText2KG |
| Recuperação de arestas | Hits@k, MRR, AUC | CaseLink |
| Custo de manutenção | tempo e chamadas de API por documento novo | argumento prático |

Métricas por época gravadas em `.csv` (dica explícita do slide 9).

---

## 6. Infraestrutura

- **CPU-only.** Não há GPU NVIDIA na máquina; a reprodução roda em 34 s.
- **Colab (GPU)** apenas para GLiNER e varreduras de hiperparâmetro.
- **Custo de API:** US$ 12–61 no projeto inteiro, conforme o modelo
  ([docs/05-orcamento-api.md](docs/05-orcamento-api.md)). Custo não é restrição.

---

## 7. Riscos principais

| Risco | Onde |
|---|---|
| **Segmentação por artigo** — regex ingênuo erra ~20% (captura artigos de outras leis citados em alterações) | semanas 2-3, risco nº 1 |
| **Estrutura espelhada não confirmada** — o ground truth do tipo C depende dela | portão na semana 3 |
| **Vazamento de citação na feature** — mitigação obrigatória por masking | decisão D6 |

Registro completo: [docs/06-plano-execucao.md](docs/06-plano-execucao.md).

---

## 8. Entregável

Relatório de até 8 páginas, avaliado em **Concepção, Experimentação, Análise, Resultado**.
Estrutura proposta e mapeamento aos pilares em
[docs/06-plano-execucao.md](docs/06-plano-execucao.md) §S8.
