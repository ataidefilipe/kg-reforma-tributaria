# Decisões Abertas e Registro de Decisões

**Última atualização:** 2026-09-15

Classificação conforme `AGENT.MD` §17: **Técnica** (agente decide) / **Analítica** (agente recomenda,
usuário valida) / **Negócio** (usuário decide).

---

## Decisões já tomadas

| # | Decisão | Tipo | Escolha | Justificativa |
|---|---|---|---|---|
| D1 | Granularidade do nó | Analítica | **Artigo** | ~1.950 nós vs ~6 no nível-documento. Grafo de 6 nós não sustenta GNN. Ver `01-levantamento-corpus.md` §3.1 |
| D2 | Estratégia de split | Analítica | **Temporal** (por data de publicação) | Split aleatório vazaria informação e invalidaria a tese indutiva |
| D3 | Ambiente | Técnica | venv em `C:\Users\filipe.barbosa\venvs\mestrado-dl` | Fora do OneDrive — venv gera milhares de arquivos e trava o sync |
| D4 | Hardware | Técnica | **CPU-only** | Não há GPU NVIDIA na máquina (AMD integrada). Carga é leve o bastante |
| D5 | Benchmark de reprodução | Analítica | **PPI** (principal) + Cora (sanidade) | Cora tem split transdutivo — não valida a propriedade indutiva, que é a tese do projeto. PPI tem grafos de teste genuinamente não vistos |
| D6 | Masking de citações na feature | Analítica | **Obrigatório** | Sem isso a feature do nó contém o rótulo da aresta. Ver `01-levantamento-corpus.md` §3.3 |

---

## D7 — Baseline de recuperação ("RAG") — **RECOMENDADO, aguarda validação**

**Pergunta do usuário:** faria sentido comparar com um RAG normal?

**Resposta curta:** sim, mas só a metade *retrieval*. E é provavelmente o baseline mais importante
do projeto.

### Por que não comparar "RAG" inteiro

Um RAG completo (retrieval + geração) responde perguntas em linguagem natural. O GraphSAGE produz
embeddings. Comparar os dois em "qualidade da resposta" seria comparar coisas com saídas de tipos
diferentes — metodologicamente frágil e sem métrica comum. O estágio de geração não produz nenhuma
métrica que o GraphSAGE também produza.

### Por que o *retrieval* é comparável — e essencial

Reformulando a tarefa de predição de link como recuperação, os dois métodos passam a ter **entrada
idêntica, saída idêntica e métrica idêntica**:

> Dado um artigo novo (ex. art. 300 do Decreto 12.955/2026), quais artigos da LC 214/2025 ele regulamenta?

| | Entrada | Como decide | Saída |
|---|---|---|---|
| **Retrieval denso (RAG)** | embedding do texto do artigo novo | similaridade de cosseno com os embeddings dos artigos candidatos | top-k artigos |
| **BM25 (lexical)** | texto do artigo novo | sobreposição de termos ponderada | top-k artigos |
| **GraphSAGE** | embedding do texto + vizinhança no grafo | score de link a partir dos embeddings agregados | top-k artigos |

Métricas comuns: **Hits@k, MRR, AUC-ROC**.

### O ponto metodológico central

As features de nó do nosso grafo **já são embeddings de texto**. Logo, o retrieval denso é a
**hipótese nula exata** do projeto:

```
H0: a estrutura do grafo não acrescenta informação além do conteúdo textual dos artigos.
    (GraphSAGE ≈ retrieval denso sobre as mesmas features)
H1: a agregação de vizinhança melhora a recuperação de relações normativas.
    (GraphSAGE > retrieval denso)
```

Sem esse baseline, um resultado bom do GraphSAGE não prova nada — pode ser inteiramente atribuível
ao `sentence-transformers` que gerou as features. **Com** ele, o projeto tem uma pergunta de pesquisa
falseável, que é exatamente o que os pilares "Concepção" e "Análise" avaliam.

Se H0 não for rejeitada, isso é um **resultado negativo legítimo** (`AGENT.MD` §20) e deve ser
reportado, não contornado.

### Alerta: BM25 pode ser brutalmente forte aqui

Texto normativo brasileiro tem sobreposição lexical altíssima e vocabulário padronizado. É plausível
que o BM25 — 10 linhas de código, sem rede neural — supere os dois métodos neurais. Se isso acontecer,
é o achado mais interessante do relatório, não um problema.

### Escopo (`AGENT.MD` §25)

Implementar **apenas** o estágio de recuperação. Não construir geração, não construir interface,
não usar vector DB (com ~2.000 artigos, `numpy` + cosseno resolve). No relatório, descrever como
"o componente de recuperação de um pipeline RAG", não como "um RAG".

**Custo estimado:** ~1 dia. **Valor:** alto — é o que transforma o projeto de demonstração em experimento.

---

## D8 — Papel do GLiNER-Relex — **EM ABERTO, precisa de decisão**

Citações normativas explícitas ("nos termos do art. 12 da Lei Complementar nº 214, de 2025") são
extraíveis por **regex** com precisão próxima de 100% em texto legal brasileiro. Isso torna o
GLiNER-Relex desnecessário para o dataset (a).

Três caminhos:

| Opção | Extração dataset (a) | Extração dataset (b) | Consequência |
|---|---|---|---|
| **A** | regex | regex + GLiNER | Mantém o pipeline do `PROJETO.md`. Duas etapas a validar |
| **B** | regex | regex apenas | Mais simples e confiável; perde as relações não-explícitas (interpreta/critica), que eram a diferença entre os datasets (a) e (b) |
| **C** | regex | LLM via API | Mais flexível para relações semânticas; custo de tokens; menos reproduzível |

**Recomendação:** **A**, com regex como *ground truth* e GLiNER usado só onde a relação não é
explícita. Isso preserva a distinção de dificuldade entre os datasets (exigida pela disciplina)
sem apostar a validade do grafo inteiro num modelo zero-shot.

**Trade-off que é seu:** a extração passa a não ser a contribuição do projeto — a contribuição fica
concentrada no lado GNN. Isso é um ganho de rigor e uma perda de "novidade aparente" no relatório.

---

## D9 — Tarefa principal do GraphSAGE — **EM ABERTO**

`PROJETO.md` cita predição de link **e/ou** classificação de nó. Com 8 páginas de limite, fazer as
duas bem é improvável.

| Tarefa | A favor | Contra |
|---|---|---|
| **Predição de link** | Alinha com a tese (documento novo → a quais artigos se conecta?); comparável ao baseline de retrieval; rótulos vêm de graça do regex | Precisa de estratégia de amostragem negativa bem definida |
| **Classificação de nó** | Mais simples de avaliar | Exige rotular categorias de artigo manualmente; não tem baseline de retrieval natural |

**Recomendação:** **predição de link como tarefa única**. É a que responde à pergunta do projeto e a
única que permite a comparação com o baseline de recuperação (D7).

---

## Questões em aberto (sem decisão necessária ainda)

- Qualidade do HTML do Planalto para segmentação automática por artigo — risco de engenharia nº 1.
- Modelo de embedding para features de nó (multilíngue vs. português). Definir após ver o texto.
- Incluir ou não a Portaria Conjunta MF/CGIBS 7/2026 no corpus (volume ainda não apurado).

---

## Decisões fechadas em 2026-09-15 (sessão 1)

| # | Decisão | Escolha |
|---|---|---|
| **Q1** | Prazo e dedicação | 2 meses, desenvolvimento assistido por agentes |
| **Q2** | Entregável | Relatório (≤8 páginas), não artigo de conferência |
| **Q3** | Rubrica | Os 4 pilares vieram de fala em aula; não há documento além do `5. Projeto.pdf` |
| **Q4** | **Cenário C adotado** | Três braços (extração direta / + validação / + pós-processamento GNN). Ver `04-reenquadramento.md` |
| **Q5** | Extrator do braço 1 | **GLiNER e LLM**, ambos — custo não é restrição (US$ 12–61 no projeto inteiro). Ver `05-orcamento-api.md` |
| **Q6** | Dataset (b) | **Fora do caminho crítico das semanas 1-6.** Vira decisão medida na semana 3: contar quantas arestas reais as notas CCiF produzem contra o corpus normativo. ≥100 → entra como (b-mínimo); <30 → corta |
| **GAP 2** | Fidelidade ao artigo base | Aprovado: reescrever com `NeighborLoader` (S1/S2) + agregação manual validada contra `SAGEConv` |
