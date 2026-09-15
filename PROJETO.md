# Projeto de Deep Learning — Disciplina (Mestrado)

**Status: ideia fechada.** O histórico completo de brainstorm, outras 4 ideias avaliadas e o processo de decisão estão em [outras-ideias/BRAINSTORM-IDEIAS.md](outras-ideias/BRAINSTORM-IDEIAS.md).

## Objetivo principal

Construir um **grafo de conhecimento sobre a Reforma Tributária brasileira**, alimentado por normas legais e documentos técnicos de entidades, usando uma arquitetura de **GNN indutiva (GraphSAGE)** para permitir a **criação e manutenção de nós a partir de novas entradas** (novos documentos publicados) **sem a necessidade de retreinar o modelo do zero**.

Esse é o problema central do projeto de mestrado (populações/entradas sintéticas alimentando uma base de conhecimento em grafo), aplicado aqui a um domínio real, atual e bem delimitado.

## Natureza do projeto (regras da disciplina)
- Projeto de cadeira: não é artigo científico nem exercício simples. Parte de um **código bom já existente** (baseline) e evolui numa direção própria.
- O que importa é a **análise**, não o código em si.
- **Limite: no máximo 8 páginas** no relatório final.
- Os 4 pilares avaliados: **Concepção, Experimentação, Análise, Resultado**.
- Passo obrigatório: **reproduzir o baseline sem modificações antes de alterar qualquer coisa**.

## Por que este domínio (Reforma Tributária)

Comparado a "documentos de política pública" em geral (universo enorme e vago) ou a personas sintéticas do Persona Hub (conteúdo sem relações reais), a Reforma Tributária oferece:
- **Corpus limitado e conhecido** — poucas normas principais + dezenas (não milhares) de documentos técnicos, tamanho gerenciável para validar manualmente.
- **Relações genuínas, não inventadas** — uma nota técnica de fato cita um artigo de lei; uma lei de fato regulamenta uma emenda constitucional. A aresta do grafo é extraída da realidade, não é um critério de similaridade artificial (esse era o problema identificado com o Persona Hub).
- **Atualidade real** — 2026 é o ano de teste do novo sistema (IBS/CBS), então **novos documentos continuam sendo publicados durante o próprio período do projeto**, permitindo testar a capacidade indutiva do GraphSAGE com dados que chegam de verdade, não uma simulação artificial de "novo nó".

## Mapeamento do domínio

### Estrutura normativa (nós "lei", com hierarquia real)
- **EC 132/2023** — Emenda Constitucional que criou a reforma; substitui ICMS/ISS/PIS/COFINS por IBS/CBS. É o "nó raiz" da hierarquia normativa.
- **LC 214/2025** (sancionada a partir do PLP 68/2024) — institui o IBS e a CBS; **499 artigos + 23 anexos**; regulamenta diretamente a EC 132/2023.
- **PLP 108/2024** — regulamenta o Comitê Gestor do IBS, o processo administrativo fiscal e a distribuição da arrecadação; **197 artigos**; em fase final de tramitação/sanção.
- Cada artigo pode ser tratado como sub-nó (ex. um artigo específico sendo citado por uma nota técnica), dando granularidade adicional ao grafo.

### Documentos técnicos de entidades (nós "nota técnica"/"entendimento")
- [Notas Técnicas do CCiF — Centro de Cidadania Fiscal](https://ccif.com.br/categoria/notas-reforma-tributaria/) — entidade que formulou a proposta original da reforma.
- Notas técnicas conjuntas **Receita Federal + Comitê Gestor do IBS (CGIBS)** — especificações técnicas de documentos fiscais (NF-e, NFC-e, CT-e, etc.) para operacionalizar IBS/CBS a partir de 2026.
- Posicionamentos técnicos de entidades setoriais: CNI, [CBIC](https://cbic.org.br/), Conasems, entre outras — análises comentando artigos específicos das leis acima.

### Relações a modelar (arestas reais)
- `EC_132 --regulamentada_por--> LC_214`
- `LC_214 --regulamentada_por--> PLP_108` (ou relação equivalente entre partes complementares)
- `Nota_técnica_CCiF --interpreta/cita--> Artigo_X_da_LC_214`
- `Posição_CNI --critica/comenta--> Artigo_Y_do_PLP_108`

### Disponibilidade do texto
- **Normas oficiais** (EC, LC, PLP): texto integral disponível via [Planalto](https://www.planalto.gov.br/), Câmara e Senado (mesmo mecanismo de `urlInteiroTeor` da API de Dados Abertos da Câmara).
- **Notas técnicas de entidades:** publicadas nos sites das próprias entidades (CCiF, CBIC, etc.), em PDF/HTML — universo pequeno, viável coletar manualmente ou via scraping simples.

## Baselines (artigo/código base)

Como nenhuma peça pronta faz tudo isso junta, o projeto combina três blocos, cada um com base oficial:

1. **Extração de entidades/relações do texto → triplas do grafo.**
   Opção recomendada para o prazo da disciplina: **GLiNER-Relex** — modelo zero-shot (não exige fine-tuning) que extrai entidades e relações (triplas sujeito-relação-objeto) num único passo. Alternativas: spaCy + `textacy` (mais simples, sem custo de API/GPU) ou um LLM com prompt estruturado (mais flexível, mais caro).
   Referência de estado da arte para justificar a escolha: [LLM-empowered Knowledge Graph Construction: A Survey (arXiv 2510.20345)](https://arxiv.org/html/2510.20345v1).

2. **Features de nó.**
   Embedding de texto leve (ex. `sentence-transformers`) sobre a ementa/resumo de cada norma ou nota técnica.

3. **Núcleo de Deep Learning — GraphSAGE (base principal) + CaseLink (referência recente do domínio jurídico).**
   - **Base principal:** [GraphSAGE — Inductive Representation Learning on Large Graphs (Hamilton et al., NeurIPS 2017)](https://github.com/williamleif/GraphSAGE) — código oficial dos autores (Stanford). Ao contrário de métodos transdutivos (que exigem retreinar tudo quando um nó novo aparece), aprende funções de agregação que geram embeddings para nós nunca vistos no treino. Implementação prática: [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) já traz `SAGEConv`/`torch_geometric.nn.models.GraphSAGE` prontos — não é necessário reimplementar o paper, só montar o pipeline de dados em volta.
   - **Referência recente e do mesmo domínio (fortalece a resposta a "existem artigos recentes usando DL nesse problema"):** [CaseLink — Inductive Graph Learning for Legal Case Retrieval (Tang et al., SIGIR 2024)](https://github.com/yanran-tang/CaseLink) — código oficial, publicado em 2024, aplica exatamente **aprendizado indutivo em grafo (a mesma família do GraphSAGE) a documentos jurídicos**, usando um "Global Case Graph" para capturar relações semânticas e de citação entre casos. Serve como validação de que a combinação "GNN indutivo + domínio legal" já é uma linha de pesquisa ativa e recente, não uma aplicação forçada.

**Passo obrigatório antes de inovar:** reproduzir o GraphSAGE oficial (nos datasets de benchmark do próprio paper, ex. Cora/PPI) sem modificações, para garantir que o pipeline de treino está correto antes de aplicá-lo ao grafo da reforma tributária.

## Checklist "Artigo/Código Base" (respondido)

### O que estou interessado em pesquisar?
Como um grafo de conhecimento pode ser construído e **mantido de forma incremental** — permitindo a chegada de novas entradas (novos documentos) sem exigir retreinamento completo do modelo — aplicado a um domínio real de documentos legais/técnicos interligados (a Reforma Tributária brasileira).

### Existem artigos utilizando Deep Learning nesse problema?
**Sim, em duas camadas:**
- **O método em si (aprendizado indutivo em grafos)** é uma linha de pesquisa consolidada desde o GraphSAGE (NeurIPS 2017), com desenvolvimentos recentes em grafos dinâmicos/temporais (ex. Temporal Graph Networks, GraphMixer, EvolveGCN — ver [Comprehensive Survey of Dynamic GNNs, arXiv 2405.00476](https://arxiv.org/pdf/2405.00476)), mostrando que o tema segue ativo.
- **A aplicação a documentos jurídicos/legislativos com GNN** também é uma linha de pesquisa ativa e recente, não uma combinação forçada: [CaseLink (SIGIR 2024)](https://github.com/yanran-tang/CaseLink) faz aprendizado indutivo em grafo para recuperação de casos jurídicos; [CaseGNN (arXiv 2312.11229)](https://arxiv.org/pdf/2312.11229) usa GNN sobre grafos de texto jurídico; há também trabalho em predição de citação legal via GNN heterogêneo ("The Missing Link: Joint Legal Citation Prediction Using Heterogeneous Graph Enrichment") e em gestão de conhecimento legislativo via grafos. **Conclusão: Deep Learning é claramente adequado ao problema — não é uma zona sem precedente.**

### Você tem infraestrutura para suportar as exigências de hardware desse artigo/código?
**Sim, as exigências são leves:**
- GraphSAGE via PyTorch Geometric: para grafos pequenos/médios (nosso caso — dezenas a poucas centenas de nós), o treino usa tipicamente **até ~8GB de RAM em CPU** ou **4-8GB de VRAM em GPU** — perfeitamente viável em notebook comum ou em Colab/Kaggle gratuitos, sem necessidade de GPU dedicada de alto desempenho.
- GLiNER-Relex (extração de entidades): modelo baseado em encoder (não autoregressivo), leve, roda em CPU ou GPU modesta.
- Nenhuma etapa do pipeline exige treinar ou rodar um LLM grande localmente — o ponto mais pesado seria usar um LLM via API para extração (opcional, alternativa ao GLiNER), o que é custo de tokens, não de hardware.
- **Ainda a definir:** qual hardware específico será usado (notebook próprio, Colab, Kaggle) — recomendação é usar Colab/Kaggle gratuito como padrão, já que nenhuma etapa exige mais que isso.

### Os artigos são recentes? Têm código-fonte recente? Está no GitHub? É a implementação original do autor? PyTorch ou TensorFlow? Alternativas?

| | GraphSAGE (base principal) | CaseLink (referência de domínio) |
|---|---|---|
| **Ano** | 2017 (NeurIPS) — não é recente, mas é o paper fundador do aprendizado indutivo em grafos, ainda amplamente usado e ensinado como baseline padrão da área | 2024 (SIGIR) — recente |
| **Código no GitHub** | ✅ [williamleif/GraphSAGE](https://github.com/williamleif/GraphSAGE) | ✅ [yanran-tang/CaseLink](https://github.com/yanran-tang/CaseLink) |
| **Implementação original do autor** | ✅ Sim (Stanford, autores do paper) | ✅ Sim |
| **Framework/versão** | TensorFlow (implementação original de 2017 — desatualizada em termos de versão do framework) | A confirmar ao acessar o repositório (padrão da área de GNN em 2024 é PyTorch/PyTorch Geometric) |
| **Implementações alternativas** | ✅ Sim, e é a que será usada: [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) mantém `SAGEConv`/`GraphSAGE` como módulo oficial da biblioteca, ativamente mantido, em PyTorch atual | Não necessário — o código já está em estado ativo |

**Decisão sobre framework:** usar a implementação de GraphSAGE do **PyTorch Geometric** (não o código original em TensorFlow de 2017) como base prática de trabalho — isso resolve o problema de "código antigo/desatualizado" mantendo fidelidade total à arquitetura e às garantias teóricas do paper original, já que o PyG é a implementação de referência mais usada e citada pela comunidade atualmente. O CaseLink permanece como referência de comparação/contexto para justificar a escolha do domínio, não como base de código a reproduzir diretamente (seu problema — recuperação de casos jurídicos — é diferente do nosso — grafo de normas/documentos técnicos).

## Pipeline proposto

1. **Coleta:** baixar os textos das normas principais (EC 132, LC 214, PLP 108) e um conjunto inicial de notas técnicas/posicionamentos de entidades (CCiF, Receita Federal/CGIBS, CNI, CBIC, etc.).
2. **Extração de entidades e relações:** aplicar GLiNER-Relex (ou alternativa escolhida) sobre os textos para gerar as triplas (nó, relação, nó).
3. **Construção do grafo:** cada norma/artigo/nota técnica vira um nó; as triplas extraídas viram arestas; features de nó = embedding de texto da ementa/resumo.
4. **Validação manual de amostra:** como o universo é pequeno, checar manualmente uma amostra das triplas extraídas para medir a qualidade da extração antes de treinar o modelo.
5. **Treino do GraphSAGE:** para uma tarefa concreta — predição de link (a relação X existe entre os nós A e B?) e/ou classificação de nó (categoria do documento).
6. **Teste do requisito central (nó novo sem retreino):** incorporar um documento genuinamente novo (uma nota técnica publicada depois do treino, ou uma norma nova de 2026) e gerar seu embedding via as funções de agregação já aprendidas, sem retreinar a rede. Avaliar a qualidade desse embedding (ex. acurácia de predição de link para esse nó novo) comparada a um baseline transdutivo que exigiria retreino completo.

## Datasets (dificuldade distinta, conforme exigido)
- **(a) Núcleo normativo** — EC 132 + LC 214 + PLP 108 e seus artigos: menor, mais controlado, relações bem definidas (regulamentação).
- **(b) Núcleo + notas técnicas de entidades**: maior, mais ruidoso, relações de citação/interpretação mais variadas e ambíguas de extrair.

## Métricas
- Métricas do próprio paper GraphSAGE (acurácia de classificação/predição de nó indutiva, custo de inferência para nó novo vs. retreino completo).
- Métricas de qualidade do grafo (densidade, conectividade).
- Métricas de manutenção: quantos nós/relações são corretamente integrados a partir de novas entradas, com validação manual de amostra.
- Salvar métricas por época em `.csv` para análise posterior (Pandas/Seaborn).

## Inovação proposta
Construir, do zero, um pipeline que liga três peças que hoje existem separadas — extração de entidades via LLM, construção de grafo, e aprendizado indutivo via GraphSAGE — aplicado a um domínio real (Reforma Tributária) onde as relações do grafo são genuínas, e demonstrar empiricamente que documentos novos publicados durante o próprio andamento da reforma podem ser incorporados ao grafo sem retreinar o modelo do zero.

## Pontos de atenção / riscos conhecidos
- **Risco principal: esforço de engenharia**, não de disponibilidade de dado — o pipeline inteiro (extração → grafo → GraphSAGE) é novo e precisa ser construído do zero.
- Mitigação: validar uma versão pequena de ponta a ponta o quanto antes (ex. 20-30 nós, só com as 3 normas principais) antes de escalar para as notas técnicas, reduzindo o risco de descobrir um problema de integração tarde demais.
- Onde processar: extração de entidades e embeddings de texto são leves (CPU ou GPU modesta); GraphSAGE via PyTorch Geometric também é leve comparado a treinar um LLM — Colab/Kaggle resolve.

## Próximos passos
1. Levantar a lista concreta de documentos disponíveis (quantas notas técnicas existem hoje de cada entidade) para dimensionar o dataset (b).
2. Montar a versão mínima do pipeline (3 normas principais, poucas dezenas de nós) e validar de ponta a ponta.
3. Reproduzir o GraphSAGE oficial num benchmark padrão (Cora/PPI) sem modificações.
4. Aplicar o pipeline completo ao dataset (a) e depois (b).
5. Rodar o teste de "nó novo sem retreino" com um documento genuinamente novo.
6. Analisar resultados (quantitativo + qualitativo) e escrever o relatório (máx. 8 páginas) cobrindo concepção, experimentação, análise e resultado.
