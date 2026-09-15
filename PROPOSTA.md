# Proposta de Projeto — Especialização em Deep Learning

## Título da proposta
**Grafo de Conhecimento Indutivo para a Reforma Tributária Brasileira: Criação e Manutenção de Nós a partir de Novos Documentos com GraphSAGE**

## Equipe
- Filipe Ataíde — filipeataide@gmail.com

## Link para o artigo base
Hamilton, W. L., Ying, R., & Leskovec, J. (2017). **Inductive Representation Learning on Large Graphs.** NeurIPS 2017.
- arXiv: https://arxiv.org/abs/1706.02216

## Link para o código base
Repositório oficial dos autores (Stanford), TensorFlow:
- https://github.com/williamleif/GraphSAGE

*(Observação: para a implementação prática do pipeline, será usada a versão de referência do GraphSAGE disponível em [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) — `torch_geometric.nn.models.GraphSAGE`/`SAGEConv` —, mantendo fidelidade à arquitetura e aos experimentos do artigo original antes de qualquer modificação.)*

## Quais dados serão usados para validar a proposta

Dois conjuntos de dados, com dificuldade crescente, construídos a partir de documentos públicos sobre a Reforma Tributária brasileira:

**Dataset (a) — Núcleo normativo (mais controlado):**
- Emenda Constitucional 132/2023 (EC 132/2023) — texto integral via [Planalto](https://www.planalto.gov.br/).
- Lei Complementar 214/2025 (originada do PLP 68/2024) — 499 artigos + 23 anexos, institui IBS e CBS.
- PLP 108/2024 — 197 artigos, regulamenta o Comitê Gestor do IBS.
- Relações extraídas: hierarquia de regulamentação entre a emenda e as leis complementares, e entre artigos internos.

**Dataset (b) — Núcleo normativo + documentos técnicos de entidades (mais ruidoso e desafiador):**
- Notas técnicas do [CCiF — Centro de Cidadania Fiscal](https://ccif.com.br/categoria/notas-reforma-tributaria/) (entidade que formulou a proposta original da reforma).
- Notas técnicas conjuntas da Receita Federal e do Comitê Gestor do IBS (CGIBS) sobre documentos fiscais eletrônicos (NF-e, NFC-e, CT-e, etc.).
- Posicionamentos técnicos de entidades setoriais (CNI, CBIC, Conasems, entre outras) comentando artigos específicos das normas acima.
- Relações extraídas: citação/interpretação de artigos específicos pelas entidades.

Ambos os conjuntos serão usados também para o teste central da proposta: a chegada de **documentos genuinamente novos**, publicados ao longo de 2026 (ano de teste do novo sistema IBS/CBS), permitindo avaliar a capacidade indutiva do GraphSAGE com dados reais, sem necessidade de simulação artificial de "novo nó".

## Resumo da proposta

A Reforma Tributária brasileira (EC 132/2023 e sua regulamentação) gerou um conjunto crescente e interligado de normas legais e documentos técnicos publicados por diferentes entidades, cujas relações (regulamentação, citação, interpretação) hoje não estão organizadas de forma estruturada e consultável. Este projeto propõe construir um **grafo de conhecimento** desse domínio e usar o **GraphSAGE** — uma arquitetura de rede neural em grafos (GNN) capaz de gerar embeddings para nós nunca vistos durante o treino, sem necessidade de retreinamento completo — para permitir que o grafo seja **atualizado de forma incremental** conforme novos documentos são publicados.

O pipeline proposto parte da reprodução do GraphSAGE original (em benchmarks padrão do próprio artigo) e evolui em três frentes que hoje não existem integradas: (1) extração automática de entidades e relações a partir do texto das normas e notas técnicas (via modelo zero-shot, ex. GLiNER-Relex), (2) construção do grafo com features de nó baseadas em embeddings de texto, e (3) treinamento do GraphSAGE para tarefas de predição de link e classificação de nó sobre esse grafo. A contribuição central do projeto é demonstrar empiricamente que documentos novos, publicados durante o próprio período de execução do trabalho, podem ser incorporados ao grafo sem retreinar o modelo — validando na prática o requisito de manutenção incremental de bases de conhecimento que motiva a proposta.

---
*Documento de trabalho completo (histórico de ideias avaliadas e descartadas) em [PROJETO.md](PROJETO.md) e [outras-ideias/BRAINSTORM-IDEIAS.md](outras-ideias/BRAINSTORM-IDEIAS.md).*
