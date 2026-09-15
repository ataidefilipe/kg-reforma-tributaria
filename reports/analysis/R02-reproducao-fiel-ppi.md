# R02 — Reprodução fiel do GraphSAGE em PPI (GAP 2)

**Data:** 2026-09-15
**Substitui:** `R01-primeira-execucao-ppi.md`, cuja execução não reproduzia o mecanismo do artigo.
**Código:** `src/modeling/sage_manual.py`, `src/modeling/sage_sampler.py`, `src/modeling/reproduce_ppi.py`

---

## 1. O que foi feito

O GAP 2 exigia duas coisas: **reproduzir o artigo sem modificações** e **demonstrar entendimento do
código base** (slide 6 do professor). As duas foram atendidas reimplementando o mecanismo do zero.

### 1.1 Agregador mean, validado contra a implementação de referência

`sage_manual.py` implementa o Algoritmo 1 a partir do texto do artigo, sem usar message passing do
PyG. A validação transplanta os pesos do `SAGEConv` do PyG para a implementação própria e compara:

| Teste | Diferença máxima absoluta |
|---|---|
| Grafo aleatório (50 nós, in=16, out=8) | **0,000e+00** |
| Nó isolado (grau zero) | **0,000e+00** |
| Dimensões maiores (500 nós, in=128, out=64) | **0,000e+00** |

Equivalência exata. A leitura do Algoritmo 1 está correta.

> A equivalência vale porque `W · CONCAT(h_v, h_N(v))` se decompõe em blocos de colunas:
> `W·[a;b] = W_a·a + W_b·b`. O PyG usa duas lineares separadas (`lin_r` para o nó, `lin_l` para os
> vizinhos, com o bias); a forma com concatenação do artigo é a mesma coisa.

### 1.2 Amostragem de vizinhança — reimplementada

O `NeighborLoader` do PyG exige `pyg-lib` ou `torch-sparse`, **que não têm wheel para Python 3.13 +
torch 2.14 no Windows** e falham ao compilar. Isso forçou a reimplementação — que era desejável de
qualquer forma, já que a amostragem *é* a contribuição do artigo.

`sage_sampler.py` implementa o Algoritmo 2 em torch puro. Verificações:

| Teste | Resultado |
|---|---|
| Todo vizinho amostrado é vizinho real | 0 erros em 200 nós |
| Amostragem **com reposição** (grau 1, amostra 5) | `[7,7,7,7,7]` ✓ |
| Norma L2 da representação `z` | 1,000000 ✓ |
| Logits **não** normalizados | norma livre (0,23–0,48) ✓ |

---

## 2. Três pontos de fidelidade que implementações de biblioteca omitem

Descobertos lendo o artigo linha a linha. Cada um estava errado na primeira tentativa.

### (a) Ordem de S1 e S2 — contraintuitiva

O Apêndice A adverte explicitamente:

> "...this amounts to sampling **S2 of their immediate neighbors** and S1·S2 of their 2-hop neighbors."

O `num_neighbors` do PyG é indexado do nó-semente para fora. Logo a tradução correta é
`[S2, S1] = [10, 25]`, **não** `[25, 10]`. Inverter dá 25 vizinhos imediatos e 10 no segundo salto —
o oposto do artigo.

### (b) Normalização L2 por camada

Algoritmo 1, **linha 7**: `h_v^k ← h_v^k / ||h_v^k||_2`, a cada profundidade k.

O `SAGEConv` do PyG tem `normalize=False` por padrão — ou seja, **não faz isso**. Usar a biblioteca
com o padrão já é uma modificação silenciosa do artigo.

### (c) Subamostragem de grau

Apêndice A: *"we subsample edges so that no node has degree larger than 128."*

Medido no PPI de treino: grau médio 27, mediana 15, **máximo 720**; 2,7% dos nós passam de 128.
Aplicar o corte remove 6,3% das arestas (1.226.368 → 1.149.355).

---

## 3. Um erro meu, corrigido

Na primeira versão apliquei a normalização L2 **na saída final**, que são os logits de classificação.
Consequência: os logits ficam presos na esfera unitária, cada um com magnitude ~1/√121 ≈ 0,09, e a
perda praticamente não se move (0,6706 → 0,6623 em 10 épocas).

O artigo trata `z_v` como **representação** e aplica o objetivo supervisionado por cima
(seção 3.2: *"the unsupervised loss can simply be replaced by a task-specific objective, e.g.
cross-entropy loss"*). A arquitetura correta é:

```
x --[SAGE k=1]--> h¹ (256, L2) --[SAGE k=2]--> z (256, L2) --[linear]--> logits (121)
```

Depois da correção a perda passa a cair de verdade: **0,5485 → 0,3811**.

Registro do sintoma para o relatório: *perda estagnada perto de ln(2) com F1 aparentemente boa* é
assinatura de logits com escala travada — a F1 usa limiar em zero, que é invariante a escala, então
ela não denuncia o problema.

---

## 4. Resultado

Configuração do artigo: K=2, dim 256, batch 512, 10 épocas, lr 0,01, S1=25, S2=10, L2 por camada,
grau ≤ 128, inferência exata no teste, seleção de modelo pela validação.

| Época | loss | val micro-F1 | test micro-F1 |
|---|---|---|---|
| 1 | 0,5485 | 0,5212 | 0,5263 |
| 5 | 0,4268 | 0,6744 | 0,6892 |
| 10 | 0,3811 | **0,7193** | **0,7378** |

**test micro-F1 = 0,7378** (época 10, escolhida pela validação). Tempo: 33,6 s em CPU.

---

## 5. O número é maior que o do artigo — e isso precisa ser dito, não comemorado

| Fonte | GraphSAGE em PPI (micro-F1) |
|---|---|
| Artigo original, GraphSAGE-mean | **0,598** |
| **Esta reprodução** (2 camadas, mean) | **0,738** |
| GAT (ICLR 2018), Tabela 3, "GraphSAGE\*" | **0,768** |

O artigo do GAT reporta `GraphSAGE*` como *"the best GraphSAGE result we were able to obtain by just
modifying its architecture (this was with a three-layer GraphSAGE-LSTM with [512, 512, 726]...)"*.

Ou seja: **a própria literatura documenta que o GraphSAGE alcança 0,768 em PPI**, bem acima do 0,598
que seu artigo original reporta. Nosso 0,738 fica entre os dois — com arquitetura *menor* (2 camadas,
agregador mean) do que a do `GraphSAGE*`.

### Hipóteses para o excesso sobre 0,598 — não resolvidas

| Hipótese | Status |
|---|---|
| Padrões modernos de inicialização e do Adam (torch 2.14) vs. TensorFlow de 2017 | plausível, não testado |
| O próprio artigo reconhece um bug: *"corrected to account for an extraneous normalization by the batch size"* (nota de rodapé 7) | documentado no artigo |
| Inferência exata no teste; o artigo pode ter inferido com amostragem | plausível, não testado |
| Diferença no número efetivo de passos de gradiente por época | plausível, não testado |

**Classificação (`AGENT.MD` §21): o mecanismo foi reproduzido; o número não.** Não afirmar
"superamos o artigo" — a comparação envolve variáveis de implementação não controladas, e a
literatura já mostra que a faixa do GraphSAGE em PPI vai até 0,768.

---

## 6. Por que isto importa para o projeto

A linha **"Raw features 0,422"** da Tabela 1 do artigo (chamada "MLP" na Tabela 3 do GAT) é
exatamente o baseline *"só as features, sem grafo"* que o cenário C usa como hipótese nula
(decisão D7).

**O artigo base já faz a comparação que estruturamos.** No PPI supervisionado o ganho da estrutura
sobre as features puras é 0,422 → 0,598 (+45%, valor que o próprio artigo reporta na linha
"% gain over feat."). Isso deixa de ser uma escolha metodológica nossa e passa a ser
*reprodução do desenho experimental do artigo base* — argumento forte para as seções de Concepção
e Análise do relatório.

---

## 7. Ablações

Cada linha desliga **um** dos pontos de fidelidade da seção 2. Tudo o mais igual
(lr 0,01, 10 épocas, seed 42, seleção por validação).

| Configuração | val | test | Δ test vs. fiel |
|---|---:|---:|---:|
| **Fiel ao artigo** | 0,7193 | **0,7378** | — |
| Sem corte de grau (mantém grau até 720) | 0,7230 | 0,7411 | +0,003 |
| Sem normalização L2 por camada | 0,7347 | 0,7558 | +0,018 |
| **Sem amostragem** (vizinhança completa) | 0,8072 | **0,8252** | **+0,087** |

### 7.1 A amostragem custa 8,7 pontos de F1 — exatamente como o artigo diz

Este é o resultado mais importante. Desligar a amostragem e usar toda a vizinhança leva
0,738 → 0,825.

**A amostragem do GraphSAGE troca acurácia por escalabilidade.** Ela existe para tornar o método
viável em grafos como o Reddit (233 mil nós), não para melhorar a predição. A medição confirma
numericamente o que o `R01` havia apenas afirmado.

### 7.2 A normalização L2 do próprio artigo piora ligeiramente aqui (−1,8 pontos)

Resultado negativo honesto: o passo da linha 7 do Algoritmo 1 custa 1,8 pontos de F1 nesta
configuração. Não é motivo para removê-lo — a reprodução tem que seguir o artigo — mas é um dado
a registrar. Possivelmente a normalização importa mais no cenário **não-supervisionado**, onde os
embeddings são comparados por produto interno e a escala atrapalharia.

### 7.3 O corte de grau é irrelevante (+0,3 pontos)

Coerente com o artigo, que o justifica como *"a reasonable tradeoff"* feito por eficiência
computacional, não por acurácia.

### 7.4 Nenhuma ablação explica a diferença de +0,14 para o artigo

As três ablações **aumentam** a F1 em relação à configuração fiel. A configuração fiel é a mais
baixa das quatro — e ainda assim fica 0,14 acima do 0,598 do artigo.

**Conclusão (resultado negativo, `AGENT.MD` §20):** a hipótese de que os pontos de fidelidade da
seção 2 explicariam o excesso está **descartada**. A diferença vem de outro lugar — provavelmente
inicialização/otimizador da época (TensorFlow 2017 vs. torch 2.14) ou o bug de normalização por
batch que o próprio artigo admite na nota de rodapé 7. Não foi possível determinar com os dados
disponíveis.

---

## 8. Consequência prática para o projeto

O grafo da Reforma Tributária tem **~1.950 nós** — 115× menor que o Reddit (233 mil), e 23× menor
que o PPI de treino (44.906).

**Decisão técnica:** usar **agregação exata (vizinhança completa)** na camada de aplicação, não
amostragem. A amostragem só se justifica quando o grafo não cabe na memória; no nosso caso ela
custaria 8,7 pontos de F1 sem nenhum ganho. O `embed_full()` de `sage_sampler.py` já faz isso.

A amostragem permanece implementada e reproduzida porque é o mecanismo do artigo base e o slide 6
exige reproduzi-lo — mas não entra no pipeline da Reforma.

---

## 9. Próximos passos

1. Reproduzir `Raw features` (MLP sobre x, sem grafo) no nosso próprio código — é o baseline
   que o cenário C reutiliza como hipótese nula (D7).
2. Seguir para a ingestão do corpus da Reforma Tributária (semanas 2-3) — risco nº 1 do cronograma.
