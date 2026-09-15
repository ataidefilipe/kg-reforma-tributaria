# Requisitos do Professor × Estado do Projeto

**Fonte:** `5. Projeto.pdf` — Cleber Zanchettin (cz@cin.ufpe.br), CIn.AI — 9 slides.
**Data da auditoria:** 2026-09-15

Este documento é o critério de aceitação do projeto. Toda decisão deve ser rastreável até um item daqui.

> Slide 3 ("Temas") é a taxonomia de tasks do HuggingFace. **"Graph Machine Learning"** aparece
> explicitamente na coluna *Multimodal* — o tema escolhido está dentro do escopo autorizado.

---

## Legenda

✅ atendido · ⚠️ parcialmente atendido / risco · ❌ não atendido · ❓ depende de informação que não temos

---

## Slide 2 — Objetivo

| Requisito | Status | Observação |
|---|---|---|
| Ser algo do seu interesse | ✅ | Alinhado ao tema do mestrado (manutenção incremental de base de conhecimento) |
| Tempo que você pode dedicar | ❓ | **Não sabemos.** Ver Q1 |
| Deadline para entrega | ❓ | **Não sabemos.** Ver Q1 — é a variável que mais afeta o escopo |
| Dados disponíveis | ✅ | ~1.950 artigos + 30 NTs CCiF. Ver `01-levantamento-corpus.md` |
| Recursos computacionais | ✅ | CPU local + Colab. Ver §"Onde executar" |

---

## Slide 6 — Artigo/Código Base

| Requisito | Status | Observação |
|---|---|---|
| Partir de um BOM artigo/código base | ✅ | GraphSAGE (NeurIPS 2017), 15k+ citações, baseline canônico da área |
| **Ser capaz de entender razoavelmente bem o artigo/código base** | ⚠️ | **GAP 2** — ver abaixo |
| **Reproduzir os resultados SEM MODIFICAÇÕES antes de qualquer coisa** | ⚠️ | Script escrito e rodando, mas com infidelidade a corrigir — **GAP 2** |
| A partir disso, partir para ajustes e melhorias | ⏳ | Depende do anterior |

### GAP 2 — Fidelidade ao artigo base e domínio sobre o código

Dois problemas, um meu e um do plano:

**(a) Meu script está infiel ao artigo.** A contribuição central do GraphSAGE **não é** a camada de
agregação — é o **treinamento em minibatch com amostragem de vizinhança de tamanho fixo**
(`S1=25, S2=10` no artigo), que é o que torna o método escalável e indutivo na prática.
O `baseline_graphsage.py` que escrevi faz forward *full-batch*. Funciona, dá números, **mas não
reproduz o mecanismo do artigo**. Precisa ser reescrito com `NeighborLoader`.

**(b) O plano trata `SAGEConv` como caixa-preta.** O professor exige entendimento do código base.
Chamar uma classe do PyG não demonstra isso.

**Correção proposta:** implementar a agregação manualmente (~30 linhas) e validar contra o `SAGEConv`
do PyG — se os dois produzirem o mesmo resultado, isso *é* a demonstração de que o artigo foi entendido,
e vira meia página forte na seção de Concepção.

---

## Slide 7 — Checklist do artigo base

| Requisito | Status | Resposta |
|---|---|---|
| O que estou interessado em pesquisar? | ✅ | Manutenção incremental de grafo de conhecimento sem retreino |
| Existem artigos usando DL nesse problema? | ✅ | GraphSAGE (2017) + CaseLink (SIGIR 2024) + CaseGNN — domínio jurídico com GNN é linha ativa |
| Infraestrutura suporta as exigências? | ✅ | Ver §"Onde executar" |
| Artigo recente? Código no GitHub? Original do autor? PyTorch/TF? Alternativas? | ✅ | Respondido em `PROJETO.md`. GraphSAGE original é TF/2017 → usamos PyG (PyTorch, mantido) |

---

## Slide 8 — Inovação/Estudo

| Requisito | Status | Observação |
|---|---|---|
| Qual evolução/inovação será proposta? | ⚠️ | **GAP 3** |
| O que se propõe é algo não conhecido? | ⚠️ | **Honestamente: não.** O método é conhecido; a aplicação é nova |
| **Pretende fazer um estudo comparativo?** | ✅ | **Esta é a saída.** Ver GAP 3 |
| Há tempo hábil para adaptar + experimentos + ANÁLISES + escrever? | ❓ | Depende de Q1 |
| **Quais alternativas de evolução pretende testar?** | ❌ | **GAP 4** |
| Por que supõe que irá funcionar bem? | ⚠️ | Precisa de justificativa explícita no relatório |
| Está sendo aplicado em outros casos? | ✅ | CaseLink aplica GNN indutivo a documentos jurídicos |
| Está confortável em alterar o código base? | ⚠️ | Ligado ao GAP 2 |

### GAP 3 — A "inovação" é fraca sozinha; o estudo comparativo resolve

"Aplicar GraphSAGE a um domínio novo" é a forma mais fraca de contribuição, e o professor pergunta
diretamente se o que se propõe é algo não conhecido. A resposta honesta é não.

Mas o slide oferece a alternativa explícita: **"Pretende fazer um estudo comparativo?"**

O baseline de recuperação (D7 em `02-decisoes-abertas.md`) converte o projeto de *aplicação* em
*estudo comparativo* com hipótese falseável:

> A estrutura do grafo acrescenta informação além do conteúdo textual dos artigos, na tarefa de
> recuperar relações normativas entre documentos legais?

Comparando **BM25 (lexical) × retrieval denso (as features sozinhas) × GraphSAGE (features + estrutura)**.

**Isto deixa de ser opcional.** É o que faz o projeto atender ao slide 8.

### GAP 4 — Nenhuma alternativa de evolução definida

O professor pergunta no plural: "Quais alternativas de evolução você pretende testar?". Hoje temos
um eixo só. Alternativas baratas e que vêm **do próprio artigo base** (portanto comparáveis):

| Eixo | Variações | Custo | Vem do artigo? |
|---|---|---|---|
| Agregador | `mean` / `max-pool` / `LSTM` | baixo | ✅ Tabela 1 do artigo compara os três |
| Profundidade (K) | K=1, 2, 3 | baixo | ✅ §4.4 do artigo |
| Tamanho da amostra de vizinhança | S1×S2 | baixo | ✅ Figura 2 do artigo |
| Loss | supervisionada vs. não-supervisionada | médio | ✅ o artigo faz os dois |

Recomendo **agregador + profundidade** como eixos principais: são os do artigo, são baratos em CPU,
e geram tabela comparativa direta com a Tabela 1 original.

---

## Slide 9 — Datasets e Métricas

| Requisito | Status | Observação |
|---|---|---|
| Quantos datasets? | ✅ | 2 próprios (a, b) + 1-2 de reprodução (PPI, Cora) |
| Tem acesso? | ✅ | Todos públicos |
| São suficientemente diferentes? | ✅ | (a) normativo limpo × (b) notas técnicas ruidosas |
| Têm graus de dificuldade distintos? | ✅ | (a) relações explícitas por regex × (b) relações semânticas |
| **Esses datasets são usados no artigo base e em outros relacionados?** | ❌ | **GAP 1** |
| Que métricas pretende usar? | ⚠️ | **GAP 5** |
| Tem código pronto para calculá-las? | ✅ | `sklearn.metrics` + implementação própria de Hits@k/MRR |
| **Essas métricas são usadas no artigo base e em outros relacionados?** | ⚠️ | **GAP 5** |
| São relevantes para o problema? | ✅ | |
| **Dica: salvar métricas por época em CSV** | ✅ | Já implementado em `baseline_graphsage.py` |

### GAP 1 — Nossos datasets não existem na literatura

O professor pergunta explicitamente se os datasets são os do artigo base "para efeito de comparação".
Os nossos são construídos do zero — **não há ponto de comparação externo**. Ninguém publicou número
sobre o grafo da Reforma Tributária.

**Mitigação (estrutura de dois níveis):**

| Nível | Dataset | Papel | Comparável a |
|---|---|---|---|
| **Reprodução** | PPI (do artigo) | provar que o pipeline está correto | Tabela 1 do artigo original |
| **Reprodução** | Cora (grafo de citação) | mesma *natureza* do nosso grafo: citação entre documentos | literatura de GNN |
| **Aplicação** | Reforma (a) | domínio novo, relações limpas | baselines internos (BM25, retrieval) |
| **Aplicação** | Reforma (b) | domínio novo, relações ruidosas | baselines internos |

A comparação externa é satisfeita pela camada de **reprodução**; a camada de **aplicação** é comparada
internamente contra baselines. Isso precisa estar declarado explicitamente no relatório, não escondido.

### GAP 5 — Métricas divergem do artigo base

O artigo do GraphSAGE reporta **micro-F1** em classificação de nó. Nossa tarefa principal (D9) é
**predição de link**, cujas métricas são **Hits@k, MRR, AUC** — que não aparecem no artigo base.

**Justificativa a usar no relatório:** a tarefa mudou, logo a métrica muda. As métricas de recuperação
são as padrão do **trabalho relacionado do mesmo domínio** — CaseLink (SIGIR 2024) avalia recuperação
de casos jurídicos com métricas de ranking. O professor pede métricas usadas "no artigo base **e outros
relacionados ao mesmo problema**" — a segunda metade da frase cobre isso.

**Plano:** reportar micro-F1 na camada de reprodução (comparável ao artigo) **e** Hits@k/MRR/AUC na
camada de aplicação (comparável ao CaseLink). Declarar explicitamente por quê.

---

## Onde executar — decisão

| Etapa | Custo | Onde | Justificativa |
|---|---|---|---|
| Reprodução PPI/Cora | leve-médio | **local (CPU)** | Medido empiricamente — ver `reports/analysis/` |
| Coleta e parsing dos documentos | leve, I/O | **local** | Dados ficam versionados no projeto |
| Embeddings (`sentence-transformers`, ~2.000 artigos) | minutos em CPU | **local** | Não justifica GPU |
| **Extração com GLiNER-Relex** (dataset b) | médio-pesado | **Colab (GPU)** | Único ponto que ganha muito com GPU |
| Treino GraphSAGE no grafo da Reforma (~2.000 nós) | trivial | **local** | Grafo menor que Cora |
| Varredura de hiperparâmetros (GAP 4) | médio | **Colab** | Paralelizável, sem custo local |

**Conclusão:** híbrido. Local como padrão (iteração rápida, dados versionados); Colab só para GLiNER e
varredura. Não vale mover o projeto inteiro para o Colab — o overhead de sincronizar dados a cada sessão
custa mais do que a GPU economiza, dado o tamanho do grafo.

---

## Perguntas que precisam de resposta

**Q1 — Qual é o deadline e quantas horas/semana você consegue dedicar?**
É a informação que mais define o escopo. Com prazo curto, corta-se o dataset (b) e o GLiNER inteiros
(GAP 4 vira só agregadores). Com prazo folgado, o projeto completo cabe.

**Q2 — O entregável é "relatório de 8 páginas" ou "artigo"?**
O slide 8 diz "escrever o artigo"; o `PROJETO.md` diz "relatório, máx. 8 páginas". Se for artigo em
formato de conferência (SBC/IEEE, 2 colunas), a estrutura e o volume de texto mudam.

**Q3 — Existe outro documento do professor** (rubrica de avaliação, template, data de entrega)?
Os 4 pilares citados no `PROJETO.md` (Concepção, Experimentação, Análise, Resultado) **não estão neste
PDF** — vieram de outra fonte. Se existir uma rubrica, ela mudaria os pesos desta auditoria.
