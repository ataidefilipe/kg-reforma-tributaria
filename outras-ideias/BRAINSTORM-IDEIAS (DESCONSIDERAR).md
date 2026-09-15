# Projeto de Deep Learning — Disciplina (Mestrado)

## Natureza do projeto
- É um **projeto de cadeira**, não um artigo científico nem um exercício simples.
- Abordagem: pegar um **código bom já existente** (baseline) e fazer **alterações direcionadas** rumo a um objetivo escolhido por nós.
- O que importa é a **análise**, não o código em si (o código é meio, não fim).
- **Limite: no máximo 8 páginas** no relatório/artigo final.
- Deve-se considerar **onde processar** (CPU/GPU/cloud) e usar **modelos bons** (relevantes/atuais para o problema escolhido).

## Requisitos vindos do slide "Datasets e Métricas"
Perguntas que o relatório final precisa responder:

**Sobre datasets:**
- Quantos datasets pretendemos usar?
- Temos acesso a esses datasets?
- Eles são suficientemente diferentes entre si?
- Possuem graus de dificuldade distintos?
- Para efeito de comparação: esses datasets são usados no artigo base e em outros trabalhos relacionados ao mesmo problema?

**Sobre métricas:**
- Que métricas pretendemos utilizar?
- Já temos código pronto para calculá-las?
- Para efeito de comparação: essas métricas são usadas no artigo base e em outros relacionados?
- Elas são relevantes para o problema considerado?

**Dica operacional:** salvar as métricas ao longo das épocas em arquivos `.csv`, para depois estudá-las com Pandas, Seaborn etc.

## Requisitos vindos do slide "Objetivo"
- Tem que ser algo do **interesse** de quem faz o projeto — critério de escolha número um.
- Mas precisa considerar restrições práticas:
  - **Tempo** disponível para dedicar ao projeto.
  - **Deadline** de entrega.
  - **Dados** disponíveis.
  - **Recursos computacionais** disponíveis.

## Requisitos vindos do slide "Artigo/Código Base"
- Perguntas de checagem antes de escolher o baseline:
  - O que estou **interessado** em pesquisar?
  - Existem artigos usando **Deep Learning** nesse problema? Se não, cuidado — talvez DL não seja adequado pro problema.
  - Tenho **infraestrutura** para suportar as exigências de hardware do artigo/código escolhido?
  - Os artigos encontrados são **recentes**? Têm código-fonte recente? Está no **GitHub**? É a implementação **original** do autor? Está em **PyTorch** ou **TensorFlow**? Em qual versão? Existem implementações alternativas?
- Fontes recomendadas para achar artigo/código base:
  - [paperswithcode.com](https://paperswithcode.com/) — trending research, ranking por tarefa/dataset, e link direto pro código oficial (via arXiv).
  - [arxiv.org](https://arxiv.org/) — para achar o paper e conferir se tem "Code Associated with this Article" (link pro repositório oficial no GitHub).
  - [huggingface.co/spaces](https://huggingface.co/spaces) — demos de modelos/apps rodando.
  - [universe.roboflow.com](https://universe.roboflow.com/) — datasets e modelos de visão computacional já anotados (detecção, classificação, segmentação, etc.).
- **Passo obrigatório antes de qualquer modificação:** tentar **reproduzir os resultados do artigo/código base SEM modificações**. Só depois de conseguir reproduzir é que se parte para ajustes/melhorias.
- **Importante — o artigo base não precisa ser do mesmo tema/domínio.** Pode (e muitas vezes deve) ser um artigo de **arquitetura genérica equivalente**, adaptado/retreinado para o nosso problema. O que importa é a equivalência estrutural do input/tarefa, não o domínio de aplicação. Exemplo: não precisa existir um paper específico de "previsão de vitória em Dota 2" — existe um problema equivalente de "classificação a partir de um **conjunto não-ordenado de itens categóricos**", que já tem arquiteturas consagradas com código oficial (ver seção de candidatos abaixo). Essa abordagem inclusive fortalece a "inovação": aplicar uma arquitetura de outro domínio a um problema novo já é, por si, uma contribuição.
- Temas cobertos no paperswithcode (categorias úteis pra navegar): Multimodal (Text-to-Image, VQA, Document QA, Graph ML, etc.), Computer Vision (Depth Estimation, Classification, Detection, Segmentation, Video, Zero-Shot, etc.), Reinforcement Learning, NLP (Text/Token Classification, QA, Summarization, Text Generation, Sentence Similarity, etc.), Audio (TTS, ASR, Audio Classification), Tabular (Classification, Regression).

## Requisitos vindos do slide "Inovação/Estudo"
- Qual **evolução/inovação** será proposta? É algo **não conhecido**? Ou pretende ser um **estudo comparativo**?
- Há **tempo hábil** para: adaptar o código base + fazer os experimentos + fazer as **análises** quantitativas/qualitativas + escrever o artigo/relatório?
- Quais **alternativas de evolução** serão testadas? **Por que** se supõe que vão funcionar bem? Já foi aplicado em outros casos (não no artigo/código base)?
- Existe **conforto/entendimento** suficiente do código base para implementar as alterações propostas? Existe implementação do que se está pensando em fazer em outros artigos (referência de como fazer)?

## Critérios centrais do projeto (avaliação)
Segundo o professor, os 4 pilares que precisam aparecer bem no relatório final são:
- **Concepção** — a ideia, a motivação, o porquê da escolha do baseline e da direção de alteração.
- **Experimentação** — a execução prática: reprodução do baseline + implementação das alterações propostas.
- **Análise** — leitura crítica dos resultados (quantitativa e qualitativa), não só "rodar e reportar número".
- **Resultado** — o que de fato foi obtido, comparado ao baseline e a outros trabalhos relacionados.

## Regras adicionais

### Áreas de pesquisa sugeridas pela disciplina (slide "Research projects")
Não é uma lista fechada ("but not restricted to"), mas indica o escopo esperado:
- Deep Networks Foundations: Initialization, Optimization, and Regularization
- Deep Learning for Tabular Data and Time Series
- Convolutional Neural Networks: ResNets, DenseNets, EfficientNets, etc.
- Computer Vision: Detection, Segmentation, and Advanced Tasks
- Recurrent Neural Networks: LSTM, GRU, QRNN, etc.
- Sequence-to-Sequence, Attention, Self-Attention, and Transformers
- Natural Language Processing and Language Models
- Generative Models: GANs, etc.
- Self-Supervision, Semi-Supervision, Graph Neural Networks, and Advanced Topics
- Neural Architecture Search and AutoML
- Meta-Learning, One-Shot, and Few-Shot Learning
- Limitations and Challenges: Out-of-Distribution Detection and Adversarial Robustness

*(demais regras a preencher conforme mais instruções da disciplina forem chegando)*

## Ideias em avaliação (brainstorm)

1. **Psicologia simulada em mundo virtual (ex. estilo RimWorld)** — não é sobre o jogo em si, é sobre atribuir um "nível de psicologia" (personalidade/traços) a agentes num mundo virtual e observar as consequências emergentes do comportamento ao longo do tempo. Precedente acadêmico direto: agentes generativos "Sims-like" (Stanford), simulação de 1.052 personalidades reais com LLM ([Stanford HAI](https://hai.stanford.edu/news/ai-agents-simulate-1052-individuals-personalities-impressive-accuracy)), e avaliação psicométrica de populações simuladas via HEXACO ([arXiv 2508.00742](https://arxiv.org/pdf/2508.00742)). Métrica possível: consistência de traços de personalidade (Big Five/HEXACO) ao longo da simulação. Enquadra em **NLP/Language Models** + **Self-Supervision/Advanced Topics**. Risco: métricas quantitativas mais difíceis de defender em 8 páginas.
2. **Previsão de vitória em Dota 2 com base nos picks** — classificação binária a partir da composição de heróis; baselines prontos em draft-only ([DotaWinPredictor](https://github.com/Estaheri7/DotaWinPredictor), [dota2-predictor](https://github.com/andreiapostoae/dota2-predictor)) e em série temporal com LSTM ([dota-predictor](https://github.com/amarcu/dota-predictor)). Dataset: OpenDota (público, fácil acesso). Enquadra em **Tabular/Time Series** + **RNN/LSTM** (dá pra evoluir para Transformer/self-attention). Risco baixo, métricas claras (AUC/acurácia).
3. **Reconhecimento de exercício específico — rosca direta** — restringir a um único exercício viabiliza o escopo em 8 páginas. Baselines com MediaPipe/pose estimation focados em bicep curl: [Exercise-Correction](https://github.com/NgoQuocBao1010/Exercise-Correction), [Biceps-Curl-Counting](https://github.com/jamal022/Biceps-Curl-Counting-with-Pose-Estimation-using-Mediapipe), paper [Pose Trainer](https://arxiv.org/pdf/2006.11718). Enquadra em **Computer Vision** (pose/ação). Direção de alteração possível: ir além da contagem de reps e classificar qualidade da execução (erro de forma).
4. **Pops sintéticos + grafos de conhecimento** (reaproveita/aprofunda o projeto de mestrado, sem conflito) — populações sintéticas geradas por LLM alimentando uma base de conhecimento em grafo, com criação/manutenção de nós a partir de novas entradas. Suporte direto: [Dynamic and Textual Graph Generation via LLM-based Agent Simulation](https://arxiv.org/html/2410.09824v2) (grafos dinâmicos com eventos de Birth-Death, Expand-Contract etc.). Enquadra em **Graph Neural Networks** + **NLP/Language Models**.
5. **Análise de posição política real via leitura de notícias/decisões oficiais + mapa de votos** — usar NLP/LLM para inferir a posição ideológica de atores políticos a partir de texto (notícias, decisões, discursos) e comparar/validar com o registro real de votos. Linha de pesquisa estabelecida como "ideal point estimation" e "stance detection":
   - Modelos prontos: [POLITICS (launchnlp)](https://github.com/launchnlp/POLITICS) — modelo pré-treinado + datasets BIGNEWS para ideologia/stance em notícias.
   - Estimação de posição a partir de texto legislativo: [Politext](https://github.com/sugatc/Politext), [An Embedding Model for Estimating Legislative Ideal Points (ACL 2020)](https://aclanthology.org/2020.emnlp-main.46.pdf), [Party Matters (arXiv 1805.08182)](https://arxiv.org/pdf/1805.08182).
   - Revisão de métodos (útil para justificar escolha de métricas/baseline): [Computational Measurement of Political Positions: A Review of Text-Based Ideal Point Estimation Algorithms](https://arxiv.org/pdf/2511.13238).
   - Datasets de votação legislativa multilíngues: [x-stance](https://arxiv.org/pdf/2306.08999) (Suíça), CoCoHD (audiências do Congresso dos EUA).
   - Enquadra em **NLP/Language Models** + **Transformers/Attention**. Métrica natural: correlação entre posição predita a partir do texto e posição real (registro de votos) — bem alinhado ao requisito do slide de "métricas relevantes e comparáveis com o artigo base". Ponto de atenção: para o Brasil, dataset teria que ser levantado (ex. votos nominais da Câmara/Senado, que são públicos via dados abertos) — verificar existência de dataset pronto anotado ou necessidade de montar um.

## Decisões e prioridades (2026-09-15)

Após avaliar as 5 ideias com baselines equivalentes, as prioridades e ajustes de escopo definidos foram:

1. **Psicologia em mundo virtual — prioridade baixa.** Apenas curiosidade, não é o foco.
2. **Dota 2 — refinar escopo.** Não seguir a linha de série temporal por minuto (dataset (b) da concepção anterior fica descartado). Em vez disso, usar **apenas partidas de campeonato ou partidas de alto nível fora de campeonato** (não partidas casuais). O modelo precisa refletir o **impacto das relações entre heróis**, ainda que indiretamente — heróis fortes em conjunto (sinergia) ou fracos contra um herói específico (contra-pick/counter).
3. **Rosca direta — prioridade mais baixa.** O trabalho de gravar, rotular e editar os vídeos pesa contra essa ideia.
4. **Pops sintéticos + grafos de conhecimento — prioridade mais alta (ligada ao mestrado).** Importante: **nada do pipeline está pronto**, seria construído do zero. Além de personas sintéticas, considerar também **documentos como políticas públicas ou informações mais soltas/não estruturadas** como fonte de nós/conteúdo do grafo (não só personas).
5. **Posição política via votos reais — prioridade alta, gosto pessoal, e potencial de virar um serviço online** (especialmente relevante em período eleitoral). Ajuste de escopo: **remover a parte de notícias** (não usar POLITICS/NLP de notícias). Usar **apenas o registro real de votos**. Isso exige: (a) **classificar todas as propostas votadas segundo algum critério** (ex. tema/área: economia, segurança, direitos sociais, etc.) para que os votos sejam interpretáveis e comparáveis; (b) **considerar abstenções** explicitamente (não é só sim/não — existe abstenção, e possivelmente ausência).

### Atualização (2026-09-15) — Ideia 5 rebaixada de prioridade

Depois de dimensionar o volume (algumas centenas a ~1.200 votações/ano por Casa) e confirmar que **cada proposição precisaria ser classificada individualmente** por tema (mesmo usando LLM + validação manual, é um custo recorrente por item, não uma etapa única), a relação custo/esforço ficou desfavorável para o prazo de uma disciplina. **A ideia 5 perde prioridade.**

**Candidatas finais: Ideia 2 (Dota 2, escopo campeonato/alto nível) e Ideia 4 (pops sintéticos/documentos + grafo).**

## Candidatos a Artigo/Código Base (checklist aplicado)

Para cada ideia, o candidato mais forte encontrado até agora, avaliado pelas perguntas do slide (recente? código oficial do autor? no GitHub? framework/versão?).

### 1. Psicologia simulada em mundo virtual
- **Opção A — específica do tema:** Park et al., *"Generative Agents: Interactive Simulacra of Human Behavior"*, UIST 2023 — [joonspk-research/generative_agents](https://github.com/joonspk-research/generative_agents), código oficial, mantido, ambiente completo estilo Sims. Robusta, mas pesada (simulação longa, custo de API alto, difícil de rodar e analisar em pouco tempo).
- **Opção B — reframing por arquitetura equivalente (mais leve):** o problema "atribuir um nível de psicologia e ver a consequência no comportamento" pode ser reduzido a **geração de texto/decisão controlada por atributo**, sem precisar de todo o aparato de simulação de mundo:
  - [PPLM — Plug and Play Language Model (Dathathri et al., ICLR 2020)](https://github.com/uber-research/PPLM) — código oficial (Uber AI), pega um GPT-2 pré-treinado e **direciona a geração usando classificadores de atributo simples** (ex. bag-of-words ou uma camada linear), sem retreinar o modelo de linguagem. Adaptação natural: usar classificadores de traços de personalidade (Big Five/HEXACO) como "atributo" para dirigir as decisões/falas de agentes num ambiente simples de texto, e comparar o comportamento resultante entre perfis diferentes.
  - [PersonaChat / ParlAI (Zhang et al., ACL 2018)](https://github.com/facebookresearch/ParlAI/tree/main/projects/personachat) — dataset e baselines oficiais (Facebook AI/Meta) de diálogo condicionado a persona; mais focado em consistência de personagem do que em traços psicológicos, mas é um baseline leve, bem documentado e fácil de reproduzir.
- **Avaliação:** a Opção B (PPLM) resolve o maior problema da Opção A: **custo computacional e de tempo**. É um baseline leve (GPT-2 pequeno, sem fine-tuning do LM), oficial, e permite medir diretamente o efeito de "grau de traço psicológico" na saída gerada — inclusive dá pra variar a intensidade do atributo (hyperparâmetro do PPLM) e tratar isso como o próprio "nível de psicologia" pedido na ideia original. Perde um pouco da riqueza de "mundo virtual com consequências sociais", mas ganha muito em viabilidade para 8 páginas.

### 2. Dota 2 — previsão de vitória
- **Sem paper específico do tema com código oficial forte** — mas o draft de 10 heróis é estruturalmente um **conjunto não-ordenado de itens categóricos** (a ordem em que os heróis foram escolhidos não deveria importar para o resultado, ou importa apenas parcialmente). Isso é exatamente o problema que arquiteturas de **permutation-invariant set learning** resolvem, e essas têm papers consagrados com código oficial:
  - [Set Transformer (Lee et al., ICML 2019)](https://github.com/juho-lee/set_transformer) — código oficial PyTorch, usa self-attention entre os elementos do conjunto (aqui, os heróis) para capturar interações (sinergias/contra-picks), com um mecanismo de saída permutation-invariant. **Candidato mais forte.**
  - [DeepSets (Zaheer et al., NeurIPS 2017)](https://github.com/manzilzaheer/DeepSets) — código oficial, mais simples (soma de embeddings), bom como baseline "mais fraco" para comparação dentro do próprio projeto.
- **Também disponível como referência de domínio (sem código forte):** [amarcu/dota-predictor](https://github.com/amarcu/dota-predictor) (LSTM, PyTorch, dados OpenDota) — útil para pipeline de dados e como baseline de comparação, mesmo não sendo "o" artigo base.
- **Avaliação:** ✅ agora com baseline oficial forte (Set Transformer) — a "adaptação" seria retreinar o Set Transformer trocando o domínio de aplicação original (nuvens de pontos 3D, few-shot classification) pelo conjunto de heróis do draft, prevendo vitória/derrota. Isso também vira a própria narrativa de inovação: mostrar que uma arquitetura de outro domínio (visão 3D) resolve bem um problema de e-sports. Dataset (OpenDota) continua fácil e público.

### 3. Reconhecimento de exercício (rosca direta)
- **Reframing:** o problema real, uma vez que os keypoints/esqueleto já foram extraídos (via MediaPipe/OpenPose), é **classificação de sequências de esqueleto ao longo do tempo** — exatamente a tarefa de "skeleton-based action recognition", que tem um paper canônico com código oficial:
  - [ST-GCN — Spatial Temporal Graph Convolutional Networks (Yan et al., AAAI 2018)](https://github.com/yysijie/st-gcn) — código oficial em PyTorch, trata o esqueleto como um grafo espaço-temporal (juntas = nós, ossos = arestas, tempo = dimensão extra) e classifica a ação. **Candidato mais forte** — é literalmente feito para o tipo de dado que MediaPipe produz.
- **Base geral de apoio (extração de pose, não o classificador):** [microsoft/human-pose-estimation.pytorch](https://github.com/microsoft/human-pose-estimation.pytorch) (ECCV 2018, oficial) ou o próprio MediaPipe como pipeline de pré-processamento.
- **Avaliação:** ✅ agora com baseline oficial forte e diretamente equivalente (ST-GCN foi desenhado para classificar ações a partir de sequências de esqueleto — trocar as classes originais (ex. NTU RGB+D: andar, acenar, etc.) por classes de "rosca direta correta" vs. "rosca direta com erro de forma" é uma adaptação natural e defensável. Continua existindo o gargalo de **dado próprio** (precisa gravar/rotular vídeos de rosca direta com e sem erro), mas agora a arquitetura de referência é sólida e oficial, o que resolve o ponto fraco anterior.

### 4. Pops sintéticos + grafos de conhecimento
- **Geração das personas (etapa 1):** Chan et al., *"Scaling Synthetic Data Creation with 1,000,000,000 Personas"*, 2024 — [tencent-ailab/persona-hub](https://github.com/tencent-ailab/persona-hub), código oficial (Tencent AI Lab), bem recente, ativo.
- **Reframing por arquitetura equivalente para a parte do grafo (etapa 2, o núcleo de DL da ideia):** o requisito "criação/manutenção de nós com novas entradas" é **exatamente** o problema que motivou o principal paper de GNN indutivo:
  - [GraphSAGE — Inductive Representation Learning on Large Graphs (Hamilton et al., NeurIPS 2017)](https://github.com/williamleif/GraphSAGE) — código oficial dos autores (Stanford). Ao contrário de métodos transdutivos (que exigem retreinar tudo quando um nó novo aparece), o GraphSAGE **aprende funções de agregação** que geram embeddings para nós nunca vistos durante o treino — ou seja, dá pra adicionar uma persona nova (nó novo) e gerar seu embedding sem retreinar a rede inteira. Isso é uma correspondência quase perfeita com o objetivo original da ideia.
- **Avaliação:** ✅ combinação forte — Persona Hub (LLM) gera o conteúdo/atributos das personas (texto), GraphSAGE aprende a estrutura do grafo de relações entre elas de forma indutiva. A "inovação" de vocês seria integrar as duas peças: transformar atributos textuais de cada persona em features de nó, definir as arestas (ex. similaridade de atributos, relações explícitas geradas pelo LLM) e demonstrar a atualização incremental do grafo com o GraphSAGE. Também dá pra comparar com [Dynamic and Textual Graph Generation via LLM-based Agent Simulation (arXiv 2410.09824)](https://arxiv.org/html/2410.09824v2) como related work mais próximo do tema específico.

### 5. Posição política via texto (notícias/decisões) vs. voto real
- **Opção A — específica do tema:** Liu et al., *"POLITICS: Pretraining with Same-story Article Comparison for Ideology Prediction and Stance Detection"*, NAACL Findings 2022 — [launchnlp/POLITICS](https://github.com/launchnlp/POLITICS), modelo pré-treinado no [Hugging Face](https://huggingface.co/launch/POLITICS), Transformers/PyTorch.
- **Opção B — reframing por arquitetura equivalente:** o núcleo de "prever a posição de um ator político combinando texto e um padrão real de voto" é estruturalmente idêntico a um problema de **sistema de recomendação com conteúdo** — parlamentar = usuário, proposta/notícia = item, voto = "avaliação" (like/dislike). Isso já tem arquitetura consagrada:
  - [ConvMF — Convolutional Matrix Factorization for Document Context-Aware Recommendation (Kim et al., RecSys 2016)](https://github.com/cartopy/ConvMF) — código oficial dos autores. Combina **fatoração de matriz** (aprendida a partir do padrão de "avaliações", aqui os votos) com uma **CNN sobre o texto do documento** (aqui, a notícia/proposta/decisão) — é quase um espelho exato do problema: texto + registro de comportamento real, juntos, para posicionar cada ator.
  - [Neural Collaborative Filtering (He et al., WWW 2017)](https://github.com/tensorflow/models/tree/master/official/recommendation) — versão mais simples/moderna (MLP em vez de produto interno), útil como baseline mais leve caso o ConvMF (mais antigo, Theano) seja difícil de rodar hoje.
- **Avaliação:** ✅ ambas as opções têm código oficial. A Opção A (POLITICS) é mais direta para a parte "classificar ideologia em texto" isoladamente. A Opção B (ConvMF/NCF) é mais fiel à ideia completa de "combinar leitura de texto com o registro real de comportamento/voto" e traz uma perspectiva de reframing mais criativa (tratar política como recomendação). Uma alternativa forte é **combinar as duas**: usar POLITICS (ou um encoder de texto equivalente) como o "componente de conteúdo" dentro de uma arquitetura estilo ConvMF, usando o padrão de votos reais como sinal de fatoração. Ponto de atenção comum às duas: ainda precisa de um dataset de votos reais (BR a construir, ou usar bases legislativas já prontas como [x-stance](https://arxiv.org/pdf/2306.08999)).

**Fonte sugerida para papers/baselines/datasets:** [paperswithcode.com](https://paperswithcode.com/)

## Concepção completa e avaliação por critérios (por ideia)

Para cada ideia: a concepção fechada (baseline, datasets, métricas, inovação proposta) e uma avaliação honesta nos critérios dos slides (Objetivo, Datasets/Métricas, Artigo/Código Base, Inovação, e os 4 pilares).

---

### Ideia 1 — Psicologia simulada em mundo virtual

**Concepção (com reframing PPLM — recomendada):**
- **Baseline:** [PPLM (Dathathri et al., ICLR 2020)](https://github.com/uber-research/PPLM) — GPT-2 pré-treinado + classificadores de atributo leves, sem retreinar o LM.
- **Dataset(s):** (a) corpus/bag-of-words ou exemplos rotulados por traço de personalidade (Big Five/HEXACO) para treinar os classificadores de atributo — mais simples; (b) um cenário textual estruturado (ex. um agente "decide" ações/falas num contexto fixo) para observar o efeito do atributo na saída — mais elaborado. Dá pra variar a intensidade do atributo como "grau de dificuldade".
- **Métricas:** as próprias do paper PPLM (fluência/perplexidade, taxa de acerto do atributo alvo na saída gerada via classificador externo), mais uma métrica própria de consistência do traço ao longo de gerações sucessivas.
- **Inovação proposta:** usar o mecanismo de "força do atributo" do PPLM como o "nível de psicologia" da ideia original, e comparar comportamentos/decisões geradas em diferentes intensidades e combinações de traços — uma forma leve e mensurável de "simular psicologia" sem precisar de todo o aparato de mundo virtual.

**Avaliação (opção PPLM):**
| Critério | Avaliação |
|---|---|
| Objetivo/Interesse | Alto potencial, mas subjetivo — só você sabe se topa esse tema |
| Tempo/Deadline | 🟢 Baixo-médio — GPT-2 pequeno + classificador de atributo simples, não exige simulação longa |
| Dados | 🟢 Fácil — bag-of-words de traços ou pequenos datasets de personalidade já existentes (ex. essays com rótulo Big Five) |
| Recursos computacionais | 🟢 GPT-2 pequeno roda em GPU única/Colab, sem custo de API de LLM grande |
| Datasets exigidos pelo slide | 🟢 Fácil justificar 2 datasets/cenários de dificuldade distinta |
| Métricas comparáveis ao artigo base | 🟢 O próprio PPLM já define métricas objetivas (acerto de atributo, fluência) |
| Concepção | Forte — narrativa clara, e agora com execução leve |
| Experimentação | 🟢 Código oficial simples de rodar e modificar |
| Análise | Boa combinação de quantitativo (métricas do PPLM) e qualitativo (leitura dos textos gerados) |
| Resultado | Resultado defensável e mensurável em 8 páginas |

**Nota:** a versão "mundo virtual completo" (Generative Agents) continua válida como direção mais ambiciosa, mas só recomendável com bastante tempo disponível — ver ressalvas na tabela comparativa final.

---

### Ideia 2 — Previsão de vitória em Dota 2 (escopo ajustado: alto nível/campeonato, sinergia e counter)

**Concepção (atualizada):**
- **Baseline:** [Set Transformer (Lee et al., ICML 2019)](https://github.com/juho-lee/set_transformer) — código oficial, tratando o draft (10 heróis, conjunto não-ordenado) como o "set" de entrada, com **self-attention entre heróis**. Essa escolha continua sendo a certa para o requisito de refletir relações entre heróis: os pesos de atenção entre pares de heróis (do mesmo time = sinergia; do time adversário = contra-pick) dão exatamente o sinal indireto de interação que foi pedido, mesmo sem modelar isso como uma tarefa explícita.
- **Dataset(s) — escopo revisado (sem série temporal por minuto):** **partidas profissionais/campeonato** via [OpenDota Pro Matches API](https://docs.opendota.com/) (`GET /proMatches`) ou consultas customizadas no [Data Explorer do OpenDota](https://www.opendota.com/explorer) (SQL sobre a base pública, incluindo tabela `matches`/`picks_bans` filtrando por `leagueid`); alternativa/complemento: **partidas públicas de alto nível** filtrando por MMR/rank alto via `GET /publicMatches` com parâmetro de rank mínimo. Isso dá 2 datasets de dificuldade e natureza distintas: (a) partidas de campeonato (times profissionais, meta mais "puro", amostra menor); (b) partidas públicas de alto nível fora de campeonato (amostra maior, mais ruído). Comparar os dois atende ao requisito de "datasets suficientemente diferentes e com dificuldade distinta".
- **Métricas:** acurácia, AUC-ROC, log-loss — padrão na literatura de previsão de partidas (ex. [arXiv 1711.06498](https://arxiv.org/pdf/1711.06498)). Adicionalmente, uma métrica de **interpretabilidade**: extrair os pares de heróis com maior peso de atenção e comparar com sinergias/counters já documentados publicamente (ex. tabelas de winrate por matchup do próprio OpenDota) — isso valida se o modelo está de fato capturando a relação entre heróis, não só "decorando" heróis fortes isoladamente.
- **Inovação proposta:** adaptar o Set Transformer (originalmente usado em nuvens de pontos 3D e few-shot classification) para o domínio de e-sports **restrito a partidas de alto nível**, comparando com baselines mais simples: [DeepSets](https://github.com/manzilzaheer/DeepSets) (soma de embeddings, sem atenção — não captura interação par a par) e um baseline de heróis isolados (ex. regressão logística em cima de winrate individual de cada herói, sem nenhuma interação). A comparação entre os três isola exatamente a contribuição de "capturar relação entre heróis" para a acurácia final — é a análise central do relatório.

**Avaliação:**
| Critério | Avaliação |
|---|---|
| Objetivo/Interesse | Depende do gosto pelo tema (jogos/esports) |
| Tempo/Deadline | 🟢 Baixo risco — pipeline simples, dataset já limpo/documentado |
| Dados | 🟢 Fácil acesso (OpenDota API/dumps públicos, milhões de partidas) |
| Recursos computacionais | 🟢 Roda em CPU ou GPU modesta, treina rápido |
| Datasets exigidos pelo slide | 🟢 Fácil ter 2+ variantes (draft-only vs. draft+timeseries) com dificuldade distinta |
| Métricas comparáveis ao artigo base | 🟢 Métricas padrão (AUC/acurácia), fácil comparar com outros trabalhos |
| Concepção | 🟢 Boa — reframing como "set learning" dá profundidade teórica que faltava (permutation invariance é um conceito defensável) |
| Experimentação | 🟢 Fácil de reproduzir e modificar; código oficial do Set Transformer disponível |
| Análise | Direta (curvas de aprendizado, importância de heróis, matriz de confusão, comparação set vs. sequência) |
| Resultado | Provável de dar um resultado limpo e comparável |

**Veredito:** com o reframing para "set learning" (Set Transformer/DeepSets como baseline oficial), deixou de ser fraco no critério "artigo/código base" — agora é forte em todos os critérios e continua o de menor risco geral.

---

### Ideia 3 — Reconhecimento de exercício (rosca direta)

**Concepção:**
- **Baseline:** extração de keypoints via MediaPipe (pipeline de pré-processamento, não é o modelo a treinar) + [ST-GCN (Yan et al., AAAI 2018)](https://github.com/yysijie/st-gcn) como classificador oficial de sequências de esqueleto, retreinado para classes de rosca direta em vez das classes originais (NTU RGB+D/Kinetics-skeleton).
- **Dataset(s):** vídeos de rosca direta — precisaria ser **gravado/coletado por vocês** (execuções corretas e incorretas) ou buscar dataset existente equivalente no [Roboflow Universe](https://universe.roboflow.com/) ou similares (verificar se existe algo pronto e anotado). Grau de dificuldade: execuções "de livro" vs. execuções com erro comum (balanço do tronco, amplitude incompleta).
- **Métricas:** acurácia de classificação (correto/incorreto), F1 por tipo de erro, acurácia de contagem de repetições (comparado à contagem manual) — as mesmas famílias de métrica usadas no paper ST-GCN (top-1/top-k accuracy), adaptadas ao número de classes do nosso problema.
- **Inovação proposta:** adaptar uma arquitetura pensada para reconhecimento de ação genérica (ST-GCN) a um problema de granularidade fina — não "qual ação é essa" mas "essa execução específica está correta ou tem qual erro" — e comparar com uma abordagem mais simples (ex. heurística de ângulos, como no Pose Trainer) para justificar se o custo extra do GCN compensa.

**Avaliação:**
| Critério | Avaliação |
|---|---|
| Objetivo/Interesse | Alto se houver interesse pessoal em fitness/CV |
| Tempo/Deadline | 🟡 Médio-alto risco — se precisar **coletar e rotular vídeo próprio**, consome tempo significativo |
| Dados | 🔴 Maior risco dos 5 — não há dataset pronto específico de rosca direta com anotação de "erro de forma"; provável que precise gravar |
| Recursos computacionais | 🟢 MediaPipe roda em CPU; classificador em cima é leve |
| Datasets exigidos pelo slide | 🔴 Difícil ter 2 datasets comparáveis prontos — provavelmente 1 dataset autoral |
| Métricas comparáveis ao artigo base | 🟢 Boas métricas padrão de classificação de ação (top-1 accuracy, F1), agora comparáveis ao paper ST-GCN |
| Concepção | 🟢 Boa e concreta (escopo bem definido ao restringir a 1 exercício, arquitetura oficial equivalente resolvida) |
| Experimentação | 🟡 Depende muito de quanto dado vocês conseguem gerar rápido — esse é o único gargalo real remanescente |
| Análise | Rica se o dataset autoral for bem construído |
| Resultado | Risco de amostra pequena limitar conclusões estatísticas |

**Veredito:** com o reframing para ST-GCN, a concepção e o baseline ficaram sólidos — o único gargalo real que resta é **dado próprio** (gravar/rotular vídeos de rosca direta). Se resolverem isso rápido (ex. gravação em grupo, poucas dezenas de execuções), essa ideia sobe bastante no ranking.

---

### Ideia 4 — Pops sintéticos + grafos de conhecimento (escopo ajustado: do zero, além de personas)

**Nota de escopo:** diferente do que se pensava inicialmente, **nada do pipeline de grafo está pronto** — seria construído do zero para este projeto (o que aumenta o tempo necessário, mas também a originalidade). Além disso, a fonte de conteúdo não precisa ser só personas sintéticas: pode incluir **documentos como políticas públicas ou informações mais soltas/não estruturadas**, o que generaliza a ideia de "extração de entidades/relações de texto para um grafo" além de perfis de pessoas.

**Atenção — Persona Hub resolve só metade do problema:** o Persona Hub entrega **conteúdo** (a descrição textual de cada persona), mas **não entrega relações entre personas** (é uma lista solta, sem arestas) nem "evolução" real (é um dataset estático, gerado de uma vez). Para o cenário de vocês (grafo com relações genuínas + manutenção incremental), isso significa que:
- **Se usarem Persona Hub:** o critério de aresta (quem se relaciona com quem) precisaria ser **inventado por vocês** (ex. similaridade de embedding, relação extraída via LLM a partir das descrições, atributo compartilhado) — é trabalho de design extra, e a relação resultante é artificial, não uma relação que já existia no mundo. A "evolução" também seria simulada (reservar um subconjunto de personas e liberá-las depois, fingindo chegada ao longo do tempo).
- **Se usarem documentos de política pública:** as relações já existem organicamente no mundo real (uma lei cita, emenda ou revoga outra) — a aresta não precisa ser inventada, só extraída. Isso torna o grafo mais fiel à ideia de "base de conhecimento" de verdade, e a chegada de documentos novos (uma lei nova sendo publicada) é uma simulação de evolução muito mais natural do que amostrar um dataset estático.
- **Recomendação:** usar documentos como fonte principal (mais fiel ao objetivo), e opcionalmente o Persona Hub como um segundo dataset "mais fácil"/controlado para comparação (ex. para validar o pipeline técnico antes de aplicar no dataset de documentos, que é mais trabalhoso de preparar).

**Concepção (com reframing GraphSAGE):**
- **Baseline (conteúdo/nós):** dois caminhos possíveis, não excludentes: (a) [Persona Hub (Tencent, 2024)](https://github.com/tencent-ailab/persona-hub) para personas sintéticas — bom para prototipar rápido, mas exige inventar o critério de aresta (ver nota acima); (b) qualquer LLM (ex. GPT/Llama via API ou local) usado como extrator de entidades/relações a partir de **documentos reais** (ex. textos de políticas públicas) — relações genuínas (citação, emenda, revogação), mais fiel ao objetivo de manutenção de grafo; apoiar-se na literatura de construção de KG via LLM, como [LLM-empowered Knowledge Graph Construction: A Survey (arXiv 2510.20345)](https://arxiv.org/html/2510.20345v1), para definir o pipeline de extração (etapa que "não está pronta" e precisaria ser montada).
- **Baseline (estrutura/DL principal):** [GraphSAGE (Hamilton et al., NeurIPS 2017)](https://github.com/williamleif/GraphSAGE) — GNN indutivo, gera embeddings para nós nunca vistos no treino, resolvendo diretamente o requisito de "criação/manutenção de nós com novas entradas". Como o pipeline completo (extração de entidades → features de nó → grafo → treino do GraphSAGE) é construído do zero, vale reservar tempo específico para essa engenharia antes mesmo de chegar na parte de "inovação".
- **Dataset(s):** (a) personas do Persona Hub (pronto, mais fácil de começar) e/ou (b) um corpus de documentos de política pública (ex. textos de leis/políticas públicas brasileiras, dados abertos) — mais difícil, exige a etapa de extração de entidades. Comparar os dois dá o par "dificuldade distinta" pedido pelo slide, e também testa se o pipeline generaliza além de personas.
- **Métricas:** as do paper GraphSAGE (acurácia de classificação/predição de nó indutiva, custo de inferência para nó novo vs. retreino completo) + métricas de qualidade de grafo (densidade, conectividade) + métricas de manutenção (quantos nós/relações são corretamente integrados a partir de novas entradas, com validação manual de amostra).
- **Inovação proposta:** construir o pipeline completo do zero (extração de entidades via LLM → grafo → GraphSAGE indutivo), demonstrando que o mesmo pipeline funciona tanto para personas sintéticas quanto para documentos reais de política pública — e que novas entradas (nova persona, novo documento) podem ser incorporadas sem retreinar o modelo do zero.

**Avaliação:**
| Critério | Avaliação |
|---|---|
| Objetivo/Interesse | Alto — conecta com o projeto de mestrado, aprendizado direto reaproveitável |
| Tempo/Deadline | 🟡 Médio — depende de quanto do pipeline de grafo já existe no seu trabalho de mestrado |
| Dados | 🟢 Dataset pronto (Persona Hub) + geração adicional controlada, fácil de escalar dificuldade |
| Recursos computacionais | 🟡 Custo de API de LLM para gerar/atualizar personas + GPU modesta para treinar o GraphSAGE (leve comparado a LLMs) |
| Datasets exigidos pelo slide | 🟢 Fácil justificar 2+ datasets de dificuldade distinta |
| Métricas comparáveis ao artigo base | 🟢 Agora comparáveis diretamente ao paper GraphSAGE (que já tem essa métrica de "nó novo sem retreino" como foco central) |
| Concepção | Muito forte — clara evolução sobre lacuna real do baseline, e agora com um componente de DL "de verdade" (GNN) além do LLM |
| Experimentação | 🟢 Provável reaproveitamento de código já feito no mestrado, acelera a experimentação; GraphSAGE tem código oficial simples de adaptar |
| Análise | Boa profundidade possível (qualidade do grafo, custo/benefício vs. abordagem sem grafo, indutivo vs. transdutivo) |
| Resultado | Bom potencial de resultado interessante e outputs reaproveitáveis |

**Veredito:** a que melhor concilia **interesse real + reaproveitamento de esforço + concepção forte**, e com o reframing GraphSAGE ganhou também um componente de DL clássico e bem avaliável (antes o "grafo" era mais um apêndice do LLM; agora é o objeto central de estudo).

---

### Ideia 5 — Posição política a partir de votos reais (escopo ajustado: sem notícias, foco em serviço prático)

**Nota de escopo (mudança importante):** removida a parte de notícias/POLITICS. O projeto passa a usar **apenas o registro real de votos** dos parlamentares. Isso simplifica a parte de NLP pesado, mas introduz duas necessidades novas explícitas:
1. **Classificar todas as propostas votadas por algum critério** (ex. tema: economia, segurança pública, direitos sociais, meio ambiente, etc.) — sem isso, um "voto" isolado não é interpretável nem comparável entre parlamentares/partidos.
2. **Modelar abstenção (e possivelmente ausência)** explicitamente, não só sim/não.
Também é uma ideia com potencial de virar um **serviço online real** (relevante em período eleitoral) — isso deve ser levado em conta na escrita do relatório como motivação/aplicação prática, mesmo que o entregável da disciplina seja o modelo, não o produto.

**Concepção (reframing: recomendação/fatoração de matriz com múltiplas classes, sem componente de notícia):**
- **Baseline central:** o problema agora é estruturalmente uma **matriz parlamentar × proposta**, com voto como valor categórico (sim / não / abstenção / ausência) — exatamente o problema de **estimação de posição ideal (ideal point estimation)** a partir de votos, com a complicação adicional de dados faltantes/categóricos que a própria literatura da área trata explicitamente:
  - Modelos bayesianos de "spatial voting" que tratam abstenção como categoria intermediária num modelo ordinal (não binário): ver revisão em [Bayesian spatial voting model — Colombian Senate (arXiv 2110.10250)](https://arxiv.org/pdf/2110.10250) e a discussão de estratégias de codificação (voto a favor = 1, contra = 0, abstenção = valor intermediário ou dado faltante) em [Operationalizing Legislative Bodies (arXiv 2211.17066)](https://arxiv.org/pdf/2211.17066).
  - Do lado de "arquitetura equivalente de outro domínio": o problema é análogo a um **sistema de recomendação com feedback não-binário** (parlamentar = usuário, proposta = item, voto = rating de 3-4 classes em vez de 1-5 estrelas). Base de código para adaptar: [Neural Collaborative Filtering (He et al., WWW 2017)](https://github.com/tensorflow/models/tree/master/official/recommendation), trocando a camada de saída binária/contínua por uma **saída multi-classe** (softmax sobre sim/não/abstenção/ausência) — mudança direta e bem documentada em arquiteturas de recomendação com feedback categórico.
- **Componente auxiliar (não é mais o núcleo, mas ainda necessário):** um classificador leve de **tema da proposta** a partir do texto da ementa/resumo (ex. fine-tuning de um BERT-base em português, como o [BERTimbau](https://huggingface.co/neuralmind/bert-base-portuguese-cased)), usado só para rotular cada proposta por categoria — permite depois agregar/comparar posições por tema (ex. "esse parlamentar vota de forma progressista em direitos sociais mas conservadora em economia").
- **Dataset(s):** votos nominais da Câmara dos Deputados e/ou Senado Federal (dados abertos, ex. [Dados Abertos da Câmara](https://dadosabertos.camara.leg.br/)) — inclui o registro de voto por parlamentar por proposição, incluindo abstenções e ausências. Dois datasets de dificuldade distinta possíveis: (a) uma legislatura/período específico (menor, mais controlado); (b) múltiplas legislaturas (maior, mais ruído, mudanças de partido/composição ao longo do tempo).
- **Métricas:** acurácia/F1 multi-classe na predição do voto (sim/não/abstenção/ausência) de um parlamentar numa proposta não vista; correlação entre a posição estimada (ideal point) e alinhamento partidário declarado (validação externa, já que não há "gabarito" de ideologia real); análise qualitativa dos parlamentares cuja posição estimada diverge do esperado pelo partido (achado interessante para o relatório).
- **Inovação proposta:** adaptar uma arquitetura de recomendação (NCF) — pensada para prever se um usuário vai gostar de um filme — para prever o voto de um parlamentar numa proposta, tratando abstenção como uma classe própria (não como dado ausente a ignorar, que é o que a literatura tradicional de ideal point costuma fazer) e enriquecendo o resultado com a classificação temática das propostas.

**Avaliação:**
| Critério | Avaliação |
|---|---|
| Objetivo/Interesse | 🟢 Alto — prioridade declarada, gosto pessoal, relevância de período eleitoral, potencial de virar serviço |
| Tempo/Deadline | 🟡 Médio — modelo em si (NCF adaptado) é rápido de treinar; o trabalho está em montar/limpar o dataset de votos e o classificador temático |
| Dados | 🟡 Dados abertos da Câmara/Senado existem e são públicos, mas exigem engenharia (juntar votos + ementas + tratar ausência/abstenção) — não vêm prontos para ML |
| Recursos computacionais | 🟢 NCF adaptado é leve; classificador temático (BERTimbau) roda em GPU única (Colab/Kaggle) |
| Datasets exigidos pelo slide | 🟢 Bom encaixe (uma legislatura vs. múltiplas legislaturas = dificuldade distinta) |
| Métricas comparáveis ao artigo base | 🟢 Acurácia multi-classe é direta de justificar e comparar com literatura de recomendação e de ideal point estimation |
| Concepção | 🟢 Muito forte — mais enxuta que a versão anterior (sem notícias) e com aplicação prática clara |
| Experimentação | 🟢 Baseline sólido (NCF) e simples de adaptar para saída multi-classe; risco concentrado na preparação do dataset |
| Análise | Rica — permite discutir parlamentares/partidos com posição divergente do esperado, padrões de abstenção por tema |
| Resultado | Alto potencial, e diretamente reaproveitável como base de um serviço/dashboard real |

**Veredito:** com o escopo enxuto (só votos, sem notícia), essa é agora a ideia com **melhor equilíbrio entre interesse pessoal declarado, viabilidade técnica e aplicação prática real**. Os dois itens de engenharia a resolver logo no início: (1) montar o dataset de votos com abstenção/ausência bem tratada, e (2) decidir o critério de classificação temática das propostas (manual em amostra pequena, ou automático via LLM/classificador).

---

## Comparativo final (com prioridades declaradas)

| Ideia | Prioridade declarada | Risco de tempo | Risco de dado | Recursos | Força da concepção | Baseline recomendado (equivalente de outro domínio) | Risco geral |
|---|---|---|---|---|---|---|---|
| 1. Psicologia em mundo virtual | 🔵 Baixa (curiosidade) | 🟢 Baixo-médio (com PPLM) | 🟢 Baixo | 🟢 Baixo (GPT-2 pequeno) | Forte | [PPLM](https://github.com/uber-research/PPLM) — geração de texto controlada por atributo | 🟢 Baixo-médio |
| 2. Dota 2 (alto nível/campeonato) | 🟢 Candidata final | 🟢 Baixo | 🟢 Baixo | 🟢 Baixo | 🟢 Boa (foco em sinergia/counter via atenção) | [Set Transformer](https://github.com/juho-lee/set_transformer) — classificação de conjuntos | 🟢 Baixo |
| 3. Rosca direta | 🔵 Baixa (custo de rotular/editar vídeo) | 🟡 Médio-alto | 🔴 Alto | 🟢 Baixo | 🟢 Boa | [ST-GCN](https://github.com/yysijie/st-gcn) — classificação de sequência de esqueleto | 🟡 Médio (gargalo só em dado) |
| 4. Pops sintéticos/documentos + grafo | 🟢 Candidata final (ligada ao mestrado) | 🔴 Alto (pipeline do zero) | 🟢 Baixo | 🟡 custo de API | Muito forte | [GraphSAGE](https://github.com/williamleif/GraphSAGE) — GNN indutivo | 🟡 Médio (esforço de engenharia, não de dado) |
| 5. Posição política via votos reais | 🔵 Rebaixada (custo de classificar cada proposição) | 🟡 Médio | 🔴 Alto (classificação individual recorrente por proposição) | 🟢 Baixo | Muito forte | [NCF adaptado](https://github.com/tensorflow/models/tree/master/official/recommendation) — recomendação multi-classe | 🟡 Médio-alto |

**Leitura geral (estado atual — 2 candidatas finais):**
- **1 (psicologia)** e **3 (rosca direta)** ficam de lado por decisão própria (curiosidade / custo de rotulagem).
- **5 (posição política)** foi rebaixada: mesmo com volume de dado tratável (centenas a ~1.200 votações/ano), o custo de **classificar cada proposição individualmente** por tema é recorrente e pesado demais para o prazo da disciplina — concepção continua forte, mas fica de fora por ora.
- **Restam 2 e 4 como candidatas finais**, com perfis de risco bem diferentes:
  - **2 (Dota 2, campeonato/alto nível):** menor risco geral, dado pronto (OpenDota), modelo leve (Set Transformer), execução rápida. Vantagem extra: serve como forma de praticar o fluxo completo (reproduzir baseline → modificar → analisar) de forma contida.
  - **4 (pops/documentos + grafo):** maior valor pessoal/acadêmico (reaproveita o mestrado), mas maior risco de tempo — pipeline inteiro a construir do zero (extração de entidades → grafo → GraphSAGE). Risco é de **engenharia**, não de disponibilidade de dado.

## Aprofundamento técnico das ideias priorizadas (4 e 5)

### Ideia 5 — Posição política via votos reais: pipeline concreto

**Fonte de dados (confirmada):** [Dados Abertos da Câmara dos Deputados](https://dadosabertos.camara.leg.br/) — API REST pública, sem necessidade de chave, com coleções relevantes:
- `/votacoes` — lista votações nominais (filtrável por período/legislatura).
- `/votacoes/{id}/votos` — voto individual de cada deputado naquela votação (valores como "Sim", "Não", "Abstenção", "Obstrução" — a Câmara já distingue abstenção de obstrução/ausência, o que atende diretamente ao requisito de considerar abstenções).
- `/votacoes/{id}` — metadados da votação, incluindo a proposição associada (ementa/resumo do que estava sendo votado — necessário para a classificação temática).
- `/deputados`, `/partidos` — metadados para validação externa (comparar posição estimada com partido/bloco declarado).
- Existe também o **Senado Aberto** (API equivalente do Senado Federal), caso queiram incluir as duas casas ou usar uma como dataset "fácil" e outra como "difícil"/validação cruzada.

**Pipeline proposto:**
1. **Coleta:** baixar todas as votações nominais de uma legislatura (ex. a atual, 2023–2027) via `/votacoes`, depois os votos individuais de cada uma via `/votacoes/{id}/votos`. Montar a matriz **deputado × votação → classe de voto** (Sim/Não/Abstenção/Obstrução-Ausente).
2. **Classificação temática das proposições:** usar as ementas coletadas em `/votacoes/{id}`. Estratégia recomendada para o prazo da disciplina: **bootstrapping com LLM + validação manual em amostra pequena** — usar um LLM para rotular automaticamente por tema (ex. economia, segurança, direitos sociais, meio ambiente, saúde, educação), validar manualmente ~100-200 exemplos, e opcionalmente fine-tunar um [BERTimbau](https://huggingface.co/neuralmind/bert-base-portuguese-cased) nesse conjunto para classificar o restante de forma mais barata/rápida.
3. **Modelo central:** adaptar [Neural Collaborative Filtering](https://github.com/tensorflow/models/tree/master/official/recommendation) — embedding de deputado + embedding de votação/proposição (pode incorporar o tema como feature adicional) → MLP → **softmax de 4 classes** (Sim/Não/Abstenção/Ausente), em vez da saída binária/de rating original.
4. **Avaliação:** split temporal (treinar em votações mais antigas, testar em mais recentes, simulando uso real de "prever posição futura") ou split aleatório de proposições não vistas. Atenção: classes desbalanceadas (Sim/Não dominam) — usar F1 macro, não só acurácia.
5. **Análise:** projetar embeddings de deputados (PCA/t-SNE) e colorir por partido — visualizar se o modelo recupera clusters partidários sem ter usado o partido como input; identificar outliers (deputados que "traem" o esperado do partido) como achado qualitativo.

**Ponto de atenção adicional:** para a visão de "serviço online", vale já pensar a interface como um mapa/dashboard de posições por tema — mas o entregável da disciplina é o modelo e a análise, não o produto (deixar isso explícito no relatório para não estourar as 8 páginas com preocupações de produto).

#### Estimativa de volume, tamanho e disponibilidade do texto (dimensionamento do dataset)

**Volume de proposições/votações por ano (números concretos encontrados):**
- **Câmara dos Deputados:** em 2023, o Plenário **aprovou** 137 projetos de lei, 22 medidas provisórias, 25 decretos legislativos, 8 projetos de resolução, 8 leis complementares e 3 PECs (total ~203 aprovadas em plenário); olhando de forma mais ampla (incluindo comissões com poder conclusivo), 2023 teve 213 proposições aprovadas. Em 2024, foram 340 projetos de lei aprovados + 209 decretos legislativos + 67 outras propostas (~616 aprovadas, somando plenário e comissões).
- **Senado Federal:** em 2024, foram **votadas** 1.197 proposições no total (408 PLs, 11 medidas provisórias, 56 projetos de resolução, 272 decretos legislativos, 7 PECs, 17 leis complementares, 389 requerimentos).
- **Importante distinguir:** esses números são de proposições **aprovadas/votadas**, que é um subconjunto pequeno das **proposições apresentadas** (a Câmara recebe dezenas de milhares de proposições por legislatura, a grande maioria nunca chega a ser votada em plenário). Para o dataset de "voto real", o que importa é justamente essas **votações nominais registradas** — na ordem de **algumas centenas por ano em cada Casa**, o que dá, ao longo de uma legislatura (4 anos), uma matriz de **~500-2500 votações × ~513 deputados (Câmara) ou ~81 senadores** — volume tratável e nada pesado computacionalmente (o gargalo não é volume de dado, é a coleta/organização via API).
- **Ainda não há um número exato e público de "quantas dessas foram votações nominais versus simbólicas"** — isso precisa ser filtrado diretamente via `/votacoes` (nem toda votação é nominal; nominal só ocorre em casos específicos do regimento — PECs, quórum especial, ou requerimento de verificação). Recomendo medir isso empiricamente assim que a coleta começar (é uma consulta simples à API), em vez de estimar de fonte externa.

**Tamanho do texto das proposições:**
- Não há estatística oficial pública sobre número médio de páginas/artigos — essa informação **não foi encontrada em nenhuma fonte** e provavelmente não existe consolidada. Pela estrutura conhecida de um projeto de lei brasileiro (parte preliminar + parte normativa em artigos + parte final), a expectativa qualitativa é de uma **distribuição bem assimétrica**: a maioria dos PLs é curta (poucos artigos, 1-5 páginas), enquanto PECs, códigos e leis orçamentárias podem ter dezenas a centenas de páginas. **Recomendação prática:** medir isso diretamente nos primeiros dados coletados (é barato — basta contar caracteres/páginas dos textos baixados) e usar essa distribuição real para decidir se o texto integral inteiro é necessário ou se a **ementa** (resumo curto, já vem no metadado da proposição, sem precisar baixar o inteiro teor) é suficiente para a classificação temática — provavelmente **é suficiente**, o que simplifica bastante o projeto (não precisaria processar textos longos).
- **Disponibilidade do texto integral:** confirmada. O endpoint `/proposicoes/{id}` da API retorna um campo **`urlInteiroTeor`**, com link direto para o texto completo (formato PDF, servido em `camara.leg.br/proposicoesWeb/prop_mostrarintegra?codteor=...`). Ou seja, o texto integral está disponível programaticamente, mas exigiria um passo extra de download + extração de PDF (não vem como texto plano na API) — mais uma razão para preferir a **ementa** como fonte principal de classificação temática, reservando o inteiro teor só se a análise exigir mais profundidade.

### Ideia 4 — Pops sintéticos/documentos + grafo: pipeline concreto

**Ferramentas específicas para montar o pipeline do zero:**
1. **Geração/coleta de conteúdo dos nós:**
   - Personas: [Persona Hub](https://github.com/tencent-ailab/persona-hub) (pronto).
   - Documentos: textos de políticas públicas/leis (ex. [Planalto](https://www.planalto.gov.br/ccivil_03/leis/) ou bases de dados abertos municipais/estaduais) — a coletar.
2. **Extração de entidades e relações (a etapa que "não existe pronta" e precisa ser montada):**
   - Opção rápida e leve: [GLiNER-Relex](https://arxiv.org/pdf/2605.10108) — modelo zero-shot (não precisa fine-tuning) que extrai entidades **e** relações (triplas sujeito-relação-objeto) num único passo, mais rápido que usar um LLM autoregressivo para isso. Boa opção para o prazo da disciplina.
   - Alternativa mais simples ainda: spaCy + [textacy](https://textacy.readthedocs.io/) (extração de triplas via dependency parsing) — menos preciso, mas sem custo de API/GPU.
   - Alternativa mais "no estado da arte": usar um LLM (GPT/Llama via API ou local) com prompt estruturado para extrair triplas — mais caro/lento, mas mais flexível para relações complexas.
3. **Construção do grafo:** cada persona/documento vira um nó; as triplas extraídas viram arestas; features de nó = embedding de texto (ex. `sentence-transformers`, leve e rápido) da descrição/resumo do nó.
4. **Modelo de GNN:** [PyTorch Geometric](https://pytorch-geometric.readthedocs.io/) já tem `SAGEConv`/`torch_geometric.nn.models.GraphSAGE` prontos — não precisa reimplementar o paper do zero, só montar o pipeline de dados em volta. Treinar para uma tarefa concreta, por exemplo:
   - **Predição de link** (a relação X existe entre os nós A e B?) — útil para "manutenção" do grafo.
   - **Classificação de nó** (ex. categoria da persona/documento).
5. **Teste do requisito central (nó novo sem retreino):** adicionar uma persona/documento novo depois do treino, gerar seu embedding via as funções de agregação já aprendidas (sem retreinar a rede), e avaliar a qualidade desse embedding (ex. acurácia de predição de link para esse nó novo) comparada a um baseline transdutivo que precisaria retreinar tudo.

**Ponto de atenção:** como o pipeline inteiro (passos 1–5) é novo, vale rodar uma versão pequena de ponta a ponta o quanto antes (ex. 20-30 nós) só para validar que as peças se encaixam, antes de escalar — isso reduz o risco de descobrir um problema de integração tarde demais.

#### Estudo de caso concreto: a Reforma Tributária como domínio do grafo

Definir o domínio como a **Reforma Tributária** resolve um problema prático importante: em vez de "documentos de política pública" em geral (universo enorme e vago), ganha-se um **corpus limitado, atual e com relações genuinamente documentadas**. Mapeamento do que já existe:

**Estrutura hierárquica/normativa (nós "lei"):**
- **EC 132/2023** — Emenda Constitucional que criou a reforma (o "nó raiz": substitui ICMS/ISS/PIS/COFINS por IBS/CBS).
- **LC 214/2025** (sancionada a partir do PLP 68/2024) — institui o IBS e a CBS; **499 artigos + 23 anexos**. Regulamenta diretamente a EC 132/2023.
- **PLP 108/2024** — regulamenta o Comitê Gestor do IBS, o processo administrativo fiscal e a distribuição da arrecadação; **197 artigos**; em fase final de tramitação (aprovado na Câmara e no Senado, indo à sanção).
- Isso já dá uma hierarquia natural de arestas: **EC → regulamentada por → LC 214/2025 e PLP 108/2024**; e dentro de cada lei, **artigos podem ser sub-nós** (ex. um artigo específico sendo citado por uma nota técnica).

**Documentos técnicos de entidades (nós "nota técnica"/"entendimento"):**
- [Notas Técnicas do CCiF — Centro de Cidadania Fiscal](https://ccif.com.br/categoria/notas-reforma-tributaria/) — entidade que formulou a proposta original da reforma; publica notas técnicas interpretando pontos específicos (ex. inclusão do IBS/CBS na base de cálculo de outros tributos).
- Notas técnicas conjuntas da **Receita Federal + Comitê Gestor do IBS (CGIBS)** — especificações técnicas de documentos fiscais (NF-e, NFC-e, CT-e, etc.) para operacionalizar IBS/CBS a partir de 2026.
- Posicionamentos técnicos de entidades setoriais: CNI, [CBIC — Câmara Brasileira da Indústria da Construção](https://cbic.org.br/), Conasems, entre outras — cada uma publica análises/notas sobre como a reforma afeta seu setor, frequentemente **citando artigos específicos** das leis acima.

**Relações genuínas que isso permite modelar (arestas reais, não inventadas):**
- `EC_132 --regulamentada_por--> LC_214`
- `LC_214 --regulamentada_por--> PLP_108` (ou relação equivalente entre os dois PLPs, que tratam de partes complementares)
- `Nota_técnica_CCiF --interpreta/cita--> Artigo_X_da_LC_214`
- `Posição_CNI --critica/comenta--> Artigo_Y_do_PLP_108`
- Isso é exatamente o tipo de estrutura que faltava no cenário com Persona Hub: aqui a aresta **já existe no mundo real** (a nota técnica de fato cita o artigo; a lei de fato regulamenta a emenda), só precisa ser **extraída** do texto (via GLiNER/LLM), não inventada por critério artificial.

**Disponibilidade do texto:**
- Textos oficiais (EC, LC, PLP): disponíveis integralmente via Planalto ([planalto.gov.br](https://www.planalto.gov.br/)), Câmara e Senado — mesmo mecanismo de `urlInteiroTeor` documentado antes para a ideia 5.
- Notas técnicas de entidades: publicadas nos próprios sites das entidades (ex. CCiF, CBIC) — geralmente PDF/HTML, precisam ser coletadas manualmente ou via scraping simples (universo pequeno, dezenas de documentos, não milhares — coleta manual é viável).

**Por que esse escopo é melhor que "políticas públicas em geral":** o volume é **conhecido e limitado** (2-3 normas principais + dezenas de notas técnicas, não milhares de leis), o tema é **atual e relevante** (2026 é o ano de teste do IBS/CBS), e as relações são **reais e verificáveis** — dá pra validar manualmente se o grafo extraído está correto, algo inviável num corpus muito grande.

**Ajuste na "evolução do grafo" com esse domínio:** a chegada de "novas entradas" deixa de ser simulada artificialmente — é literalmente o que está acontecendo agora: novas notas técnicas e regulamentações continuam sendo publicadas ao longo de 2026 conforme o novo sistema entra em vigor. Isso significa que dá pra demonstrar a capacidade indutiva do GraphSAGE com **dados genuinamente novos que surgem durante o período do projeto**, não apenas um subconjunto reservado artificialmente.

## O diferencial de cada candidata: o que já existe, o que muda, e o valor disso

Para as duas ideias finais, a pergunta central: **o que já existe hoje (o "de graça"), o que estamos de fato mudando (a inovação), e por que essa mudança importa.**

### Ideia 2 — Dota 2 (campeonato/alto nível)

| | Descrição |
|---|---|
| **O que já existe hoje** | (a) O **Set Transformer** já existe e já resolve bem "classificar/regressar a partir de um conjunto de itens" — mas foi validado em domínios como nuvens de pontos 3D e few-shot image classification, nunca em e-sports. (b) Já existem preditores de vitória em Dota 2 (LSTM, DeepSets, redes simples por herói) — mas nenhum deles usa **atenção explícita entre pares de heróis** nem foi restrito a **partidas de alto nível/campeonato**; a maioria usa dado casual de qualquer faixa de habilidade. |
| **O que estamos mudando** | 1) Trocar o domínio de aplicação do Set Transformer (visão 3D → draft de heróis). 2) Restringir o dado a partidas de campeonato/alto nível (em vez de série temporal por minuto de qualquer partida). 3) Usar os **pesos de atenção do próprio modelo como explicação** — extrair quais pares de heróis o modelo "olha" mais quando prevê vitória, e comparar isso com sinergias/counters já conhecidos no jogo. |
| **Valor da mudança** | Não é só "mais um preditor de Dota 2" — é uma demonstração de que uma arquitetura **permutation-invariant com atenção**, pensada para outro domínio, consegue capturar **interação entre itens categóricos sem que isso seja o objetivo explícito de treino**, e ainda produz uma leitura interpretável (quais heróis se completam/anulam). O valor acadêmico está nessa transferência de arquitetura + na validação por interpretabilidade, não no resultado de acurácia em si (que tende a ser parecido com os baselines existentes). |

### Ideia 4 — Populações sintéticas/documentos + grafo de conhecimento

| | Descrição |
|---|---|
| **O que já existe hoje** | As peças existem **separadas**, mas nunca conectadas: (a) **Persona Hub** gera personas em texto via LLM, mas entrega uma lista solta — sem estrutura, sem relação entre personas, sem grafo. (b) **GraphSAGE** aprende a gerar embeddings para nós novos sem retreinar — mas é um método genérico de ML em grafos, agnóstico ao domínio, e não resolve como transformar texto livre (personas, documentos de política pública) em nós/arestas de um grafo. (c) Ferramentas de extração de entidades/relações (GLiNER, LLMs) existem, mas cada aplicação de KG via LLM monta seu próprio pipeline particular — não há um "pacote pronto" que já faça personas/documentos → grafo → GraphSAGE. |
| **O que estamos mudando** | Construir a **ponte que falta**: um pipeline que pega conteúdo não-estruturado (personas sintéticas ou documentos de política pública) → extrai entidades e relações → monta um grafo → treina um GraphSAGE sobre esse grafo → e **demonstra na prática** que uma entrada nova (persona nova, documento novo) pode ser incorporada sem retreinar o modelo do zero. Nenhuma das peças isoladas faz isso hoje; a contribuição é a integração + a validação empírica de que a promessa "indutiva" do GraphSAGE realmente se sustenta nesse cenário específico de conteúdo gerado/textual. |
| **Valor da mudança** | Direto para o mestrado: é a demonstração de um mecanismo de **criação/manutenção incremental de base de conhecimento em grafo a partir de entradas novas** — exatamente o problema central que motivou a ideia desde o início. O valor aqui não é "mais uma aplicação de GraphSAGE", é a prova de conceito de um pipeline reaproveitável (troca-se a fonte de conteúdo — personas ou documentos — sem trocar a arquitetura de aprendizado), que pode virar a base de ferramentas futuras do próprio trabalho de mestrado. |

**Em uma frase cada:** a ideia 2 mostra que uma arquitetura de outro domínio **generaliza** para um problema novo e ainda **explica** sua decisão; a ideia 4 **constrói uma capacidade que não existe pronta em lugar nenhum** (grafo de conhecimento vivo, alimentável por texto, sem retreino) e que tem uso direto fora da disciplina.

## Próximos passos
1. Escolher 1 ideia (ou refinar uma delas) considerando: interesse real, tempo/deadline, dados disponíveis, recursos computacionais, existência de baseline/código bom, encaixe nas áreas de pesquisa sugeridas.
2. Achar o artigo/código base específico (via paperswithcode/arXiv/GitHub) — checar se é recente, se tem código oficial, framework/versão, se dá pra rodar com a infra disponível.
3. **Reproduzir os resultados do baseline sem modificações** antes de qualquer alteração.
4. Levantar 2-3 datasets candidatos e verificar critérios de diferença/dificuldade.
5. Levantar métricas usadas no artigo base (e em trabalhos relacionados) e ter código pronto pra calculá-las; salvar métricas por época em `.csv`.
6. Definir a(s) alteração(ões)/inovação(ões) a propor e justificar por que devem funcionar.
7. Definir onde processar (GPU local vs Colab/Kaggle/cloud).
8. Rodar experimentos, fazer análise quantitativa/qualitativa, e escrever o relatório (máx. 8 páginas) cobrindo concepção, experimentação, análise e resultado.
