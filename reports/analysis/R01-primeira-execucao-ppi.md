# R01 — Primeira execução do GraphSAGE em PPI

**Data:** 2026-09-15
**Script:** `src/modeling/baseline_graphsage.py`
**Métricas por época:** `reports/analysis/baseline_graphsage_ppi_seed42.csv`

## Configuração

```
Python 3.13.5 | torch 2.14.0+cpu | CUDA: não disponível
dataset=ppi  hidden=256  epochs=30  lr=0.005  dropout=0.5  aggr=mean  seed=42
PPI: 20 grafos treino / 2 val / 2 teste | 50 features | 121 classes (multi-rótulo)
```

## Resultado

| Época | loss | val micro-F1 | test micro-F1 |
|---|---|---|---|
| 1 | 0.5731 | 0.4334 | 0.4352 |
| 10 | 0.4507 | 0.5926 | 0.6097 |
| 20 | 0.4264 | 0.6272 | 0.6472 |
| 30 | 0.4153 | 0.6505 | 0.6707 |

**Melhor test micro-F1: 0.6749 (época 27). Tempo total: 92,2 s em CPU.**

## Análise

### 1. O pipeline de treino está correto

Loss cai monotonicamente, val e test sobem juntos, sem divergência entre eles. Não há sinal de
overfitting em 30 épocas. O ambiente (torch 2.14 CPU + PyG 2.8) funciona.

### 2. O modelo não convergiu

A curva ainda sobe na época 30 (val 0.6443 → 0.6505 entre as épocas 25 e 30). **Este número não é
o teto** — precisa rodar mais épocas antes de qualquer comparação com o artigo.

### 3. Custo em CPU é irrelevante — Colab não é necessário para esta etapa

92 s para 30 épocas → ~3 s/época. 200 épocas custam ~10 min em CPU. **Decisão confirmada:** a camada
de reprodução roda local.

### 4. ⚠️ Este resultado NÃO é uma reprodução do artigo

O artigo do GraphSAGE reporta micro-F1 em PPI na faixa de ~0,60 para o agregador `mean`
(**número a conferir diretamente na Tabela 1 do artigo — citado aqui de memória, não verificado**).
Nosso 0,675 está acima.

**Não se deve concluir que "superamos o artigo".** A diferença é quase certamente explicada por três
desvios da configuração original:

1. **Sem amostragem de vizinhança.** O script faz forward *full-batch* — usa todos os vizinhos.
   O artigo amostra `S1=25, S2=10`. Mais informação por nó tende a dar F1 maior; a amostragem é uma
   troca de acurácia por escalabilidade, não um ganho.
2. **Dimensão oculta maior** (256) do que a configuração padrão do artigo.
3. **Protocolo de avaliação** possivelmente diferente (o artigo faz early stopping em validação).

Enquanto os três não forem alinhados, **comparar este número com o do artigo é inválido**.

## Conclusão

| Pergunta | Resposta | Nível de certeza (`AGENT.MD` §21) |
|---|---|---|
| O ambiente funciona? | Sim | Fato observado |
| O pipeline treina corretamente? | Sim | Evidência forte |
| Isto reproduz o artigo? | **Não** | Fato observado — falta a amostragem de vizinhança |
| Precisamos de GPU/Colab aqui? | Não | Fato observado (92 s) |
| 0,675 > artigo significa algo? | **Não** | Comparação inválida até alinhar a configuração |

## Próximos passos

1. Reescrever com `NeighborLoader` (S1=25, S2=10) — requisito do GAP 2.
2. Implementar a agregação manualmente e validar contra `SAGEConv`.
3. Conferir os números reais da Tabela 1 do artigo (não confiar em memória).
4. Rodar até convergência, com early stopping em validação.
5. Só então comparar com o artigo.
