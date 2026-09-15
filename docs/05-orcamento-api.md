# Orçamento de API de LLM — Braço 1 (extração)

**Data:** 2026-09-15
**Escopo:** custo de usar LLM via API como extrator de triplas no braço 1 do cenário C.
**Preços:** tabela oficial Anthropic carregada via skill `claude-api` (cache: 2026-06-24).

---

## 1. Corpus medido

Baixado o texto oficial do Planalto e medido, não estimado:

| Documento | Artigos | Chars | Tokens (est.) | Origem |
|---|---|---|---|---|
| EC 132/2023 | 20 | 100.000 | 30.303 | **medido** |
| LC 214/2025 | 499 | 943.400 | 285.879 | **medido** |
| LC 227/2026 | 197 | 372.000 | 112.727 | extrapolado |
| Decreto 12.955/2026 | 620 | 1.172.000 | 355.152 | extrapolado |
| Res. CGIBS 6/2026 | 617 | 1.166.000 | 353.333 | extrapolado |
| **TOTAL** | **1.953** | **3.753.400** | **~1.137.000** | |

Média: **582 tokens por artigo**.

---

## 2. Distribuição é fortemente assimétrica — e isso é uma alavanca de custo

Medido na LC 214/2025 (598 segmentos):

| Estatística | Valor |
|---|---|
| Média | 1.576 chars |
| **Mediana** | **884 chars** |
| p90 | 3.388 chars |
| Máximo | **98.624 chars** |

| Corte | Participação no corpus |
|---|---|
| Maior segmento (1) | **10,5%** |
| Top 5 | 16,6% |
| Top 10 | 21,2% |
| Top 50 | 40,6% |

**Os 2 segmentos acima de 20.000 chars sozinhos são 13,2% do corpus.** São anexos (tabelas de NCM,
listas de produtos) — não contêm relações normativas.

**Recomendação:** excluir anexos da extração por LLM. Corta ~13% do custo com perda próxima de zero.

---

## 3. Modelo de custo

**Premissas:**

| Item | Valor |
|---|---|
| Prompt de extração (schema + few-shot), cacheável | 1.500 tok |
| Artigo (média) | 582 tok |
| Saída (triplas em JSON) | 250 tok |
| Chars por token (português jurídico) | 3,3 |
| Cache: escrita / leitura | 1,25× / 0,1× do input |
| Batch API | −50% |

**Cenário A** — artigo isolado.
**Cenário B** — artigo + 2 vizinhos (necessário para resolver anáfora: "o artigo anterior", "o caput").

---

## 4. Custo de uma passada completa (1.950 artigos) — USD

| Cenário | Modelo | Normal | + cache | + cache + batch |
|---|---|---:|---:|---:|
| A — artigo isolado | Opus 5 | 32,54 | 19,37 | **9,68** |
| A — artigo isolado | Sonnet 5 | 13,02 | 7,75 | **3,87** |
| A — artigo isolado | Haiku 4.5 | 6,51 | 3,87 | **1,94** |
| B — + 2 vizinhos | Opus 5 | 43,91 | 30,74 | **15,37** |
| B — + 2 vizinhos | Sonnet 5 | 17,57 | 12,30 | **6,15** |
| B — + 2 vizinhos | Haiku 4.5 | 8,78 | 6,15 | **3,07** |

## 5. Orçamento do projeto inteiro

Multiplicador **4×** sobre uma passada: desenvolvimento de prompt em subconjunto + 3 passadas finais.
Cenário B (o realista), com cache:

| Modelo | Sem Batch | **Com Batch API** |
|---|---:|---:|
| Opus 5 | $122,96 | **$61,48** |
| Sonnet 5 | $49,18 | **$24,59** |
| Haiku 4.5 | $24,59 | **$12,30** |

### Conclusão

**Custo não é restrição neste projeto.** A extração por LLM do corpus inteiro, com folga para iteração,
fica entre **US$ 12 e US$ 61** conforme o modelo.

Isso resolve a decisão **Q5**: não há motivo econômico para escolher entre GLiNER e LLM. **Fazer os dois**
e tratar "extrator" como mais um eixo de comparação — que é inclusive mais fiel ao TCC, cuja pergunta é
sobre arquiteturas baseadas em LLM.

---

## 6. Alavancas, em ordem de impacto

| Alavanca | Economia | Custo de implementação |
|---|---|---|
| **Batch API** | −50% | Trivial — a extração não tem requisito de latência. É o caso de uso canônico |
| **Prompt caching** | ~−30% | Baixo — manter o prompt de extração byte-idêntico entre chamadas |
| **Excluir anexos** | −13% | Trivial — filtro por tamanho |
| Escolher Sonnet 5 em vez de Opus 5 | −60% | Decisão de qualidade, não de engenharia — medir antes |

Batch + cache juntos já cortam ~65% do custo bruto.

---

## 7. Ressalvas — o que pode fazer este número errar

Classificação de certeza (`AGENT.MD` §21): **evidência moderada**. Tratar como **±2×**.

| Ressalva | Impacto |
|---|---|
| **`chars/token = 3,3` é estimativa, não medição.** Sem chave de API, não foi possível usar `count_tokens` | ±15% |
| **3 dos 5 documentos foram extrapolados** a partir da densidade da LC 214 — Decreto 12.955 e Res. CGIBS 6 são PDFs ainda não baixados | ±20% |
| **Multiplicador 4× é julgamento**, não medição. Pode ser 2× ou 8× conforme quantas vezes o prompt for refeito | ±2× |
| **250 tokens de saída por artigo é chute** | ±30% |
| **Segmentação imperfeita**: o regex achou 598 segmentos para 499 artigos reais — captura artigos de outras leis citados nas alterações | superestima ~20% |

Mesmo no pior caso (2× a estimativa), Sonnet 5 fica em ~US$ 50. A conclusão de que custo não é restrição
é robusta à incerteza.

**Para refinar:** com uma chave de API, `client.messages.count_tokens()` numa amostra de 50 artigos
substitui a estimativa por medição em minutos.
