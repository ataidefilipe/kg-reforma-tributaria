"""
Amostragem de vizinhanca e forward em minibatch do GraphSAGE -- Algoritmo 2 do artigo.

Escrito do zero por dois motivos:

1. E a contribuicao central do artigo. O slide 6 do professor exige entender o codigo
   base; reimplementar o mecanismo e a forma mais direta de demonstrar isso.
2. O `NeighborLoader` do PyG exige `pyg-lib` ou `torch-sparse`, que nao tem wheel para
   Python 3.13 + torch 2.14 no Windows e falha ao compilar. Esta implementacao usa
   apenas torch puro e roda em qualquer lugar, inclusive Colab.

--------------------------------------------------------------------------------------
Fidelidade ao artigo -- tres pontos que implementacoes de biblioteca costumam omitir:

(a) NORMALIZACAO L2 POR CAMADA.
    Algoritmo 1, linha 7:   h_v^k <- h_v^k / ||h_v^k||_2  , para todo v, a cada k.
    O `SAGEConv` do PyG tem `normalize=False` por padrao -- ou seja, NAO faz isso.

(b) AMOSTRAGEM UNIFORME COM REPOSICAO.
    Apendice A: "We use a uniform sampling function in this work and sample with
    replacement in cases where the sample size is larger than the node's degree."

(c) AMOSTRAS INDEPENDENTES POR CAMADA.
    Apendice A: "We index this function by k to denote the fact that the random samples
    are independent across iterations over k."
    Por isso o forward abaixo carrega um conjunto de arestas DIFERENTE por camada, em vez
    de reaproveitar um unico subgrafo.

--------------------------------------------------------------------------------------
Sobre a ordem de S1 e S2 (Apendice A, contraintuitivo):

    "...this amounts to sampling S2 of their immediate neighbors and S1*S2 of their
     2-hop neighbors."

Entao, a partir do no-semente para fora:  1o salto = S2 = 10,  2o salto = S1 = 25.
Total de 2 saltos = 10 * 25 = 250 = S1 * S2.  Confere.

--------------------------------------------------------------------------------------
Nota de implementacao: como a amostragem e de tamanho FIXO com reposicao, os vizinhos
amostrados formam um tensor (n_nos, s, d) e a media do agregador vira um simples
`.mean(dim=1)` -- nao e preciso scatter. Nos de grau zero recebem vetor zero, mesmo
comportamento do PyG.
"""

from __future__ import annotations

import torch
from torch import Tensor


class NeighborSampler:
    """Amostrador uniforme de tamanho fixo, com reposicao (N_k do Algoritmo 2)."""

    def __init__(self, edge_index: Tensor, num_nodes: int):
        src, dst = edge_index[0], edge_index[1]
        # ordena as arestas por destino para montar uma estrutura tipo CSR:
        # os vizinhos de v ficam contiguos em src_sorted[ptr[v]:ptr[v+1]]
        perm = torch.argsort(dst)
        self.src_sorted = src[perm].contiguous()
        self.deg = torch.bincount(dst, minlength=num_nodes)
        self.ptr = torch.cat([torch.zeros(1, dtype=torch.long), self.deg.cumsum(0)])
        self.num_nodes = num_nodes

    def sample(self, nodes: Tensor, size: int) -> tuple[Tensor, Tensor]:
        """Amostra `size` vizinhos de cada no em `nodes`.

        Retorna:
            neigh : (len(nodes), size)  ids dos vizinhos amostrados
            valid : (len(nodes), 1)     0.0 para nos de grau zero, 1.0 caso contrario
        """
        d = self.deg[nodes]                                   # (n,)
        seguro = d.clamp(min=1)                               # evita modulo por zero
        r = torch.rand(nodes.size(0), size, device=nodes.device)
        offset = (r * seguro.unsqueeze(1).float()).long()     # uniforme COM reposicao
        idx = self.ptr[nodes].unsqueeze(1) + offset
        neigh = self.src_sorted[idx]
        valid = (d > 0).float().unsqueeze(1)
        return neigh, valid


class SampledGraphSAGE(torch.nn.Module):
    """GraphSAGE K=2, agregador mean, com amostragem -- Algoritmos 1 e 2 combinados.

    Arquitetura conforme o artigo:

        x --[SAGE k=1]--> h^1 (256, L2) --[SAGE k=2]--> z = h^2 (256, L2) --[linear]--> logits

    O artigo fixa "the output dimension of the h^k vectors at every depth k to be 256" e
    trata a saida z_v como REPRESENTACAO. A perda supervisionada e aplicada por cima dela
    ("the unsupervised loss can simply be replaced by a task-specific objective, e.g.
    cross-entropy loss", secao 3.2) -- por isso o classificador linear separado.

    Nao normalizar os logits e essencial: a normalizacao L2 do Algoritmo 1 vale para as
    representacoes h^k, nao para a saida do classificador. Normalizar logits prende a
    escala na esfera unitaria e trava a perda.
    """

    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int,
                 normalize: bool = True):
        super().__init__()
        # cada camada tem um bloco para o proprio no e um para os vizinhos.
        # equivale a W^k . CONCAT(h_v, h_N(v)) -- ver sage_manual.py
        self.l1_self = torch.nn.Linear(in_channels, hidden_channels, bias=False)
        self.l1_neigh = torch.nn.Linear(in_channels, hidden_channels, bias=True)
        self.l2_self = torch.nn.Linear(hidden_channels, hidden_channels, bias=False)
        self.l2_neigh = torch.nn.Linear(hidden_channels, hidden_channels, bias=True)
        # objetivo especifico da tarefa, aplicado sobre a representacao z
        self.classifier = torch.nn.Linear(hidden_channels, out_channels)
        self.normalize = normalize

    @staticmethod
    def _l2(h: Tensor) -> Tensor:
        """Algoritmo 1, linha 7."""
        return h / h.norm(p=2, dim=-1, keepdim=True).clamp(min=1e-12)

    def forward_sampled(self, x: Tensor, sampler: NeighborSampler, seeds: Tensor,
                        s_hop1: int, s_hop2: int) -> Tensor:
        """Forward em minibatch (Algoritmo 2) para os nos em `seeds`.

        s_hop1 = vizinhos imediatos das sementes  (= S2 do artigo)
        s_hop2 = vizinhos de 2o salto por no      (= S1 do artigo)
        """
        n = seeds.size(0)

        # --- construcao dos blocos (Algoritmo 2, linhas 1-7) ---
        n1, v1 = sampler.sample(seeds, s_hop1)          # (n, s1)
        b1 = torch.cat([seeds, n1.reshape(-1)])         # nos que precisam de h^1
        n2, v2 = sampler.sample(b1, s_hop2)             # (n*(1+s1), s2)

        # --- camada k=1: h^1 para todos os nos de b1, a partir de x ---
        agg1 = x[n2].mean(dim=1) * v2                   # media dos vizinhos amostrados
        h1 = torch.relu(self.l1_neigh(agg1) + self.l1_self(x[b1]))
        if self.normalize:
            h1 = self._l2(h1)

        # h1 vem empilhado: primeiro as n sementes, depois os n*s1 vizinhos de 1o salto
        h1_seeds = h1[:n]
        h1_n1 = h1[n:].view(n, s_hop1, -1)

        # --- camada k=2: h^2 apenas para as sementes ---
        agg2 = h1_n1.mean(dim=1) * v1
        z = self.l2_neigh(agg2) + self.l2_self(h1_seeds)
        if self.normalize:
            z = self._l2(z)                  # z = representacao (Algoritmo 1, linha 7)
        return self.classifier(z)            # logits -- NAO normalizados

    def embed_full(self, x: Tensor, edge_index: Tensor) -> Tensor:
        """Representacao z exata, sem amostragem -- usa TODOS os vizinhos.

        E o que sera reaproveitado no grafo da Reforma Tributaria para gerar o
        embedding de um documento novo sem retreinar (a tese do projeto).
        """
        from src.modeling.sage_manual import ManualSAGEConv

        agg1 = ManualSAGEConv.mean_aggregate(x, edge_index)
        h1 = torch.relu(self.l1_neigh(agg1) + self.l1_self(x))
        if self.normalize:
            h1 = self._l2(h1)

        agg2 = ManualSAGEConv.mean_aggregate(h1, edge_index)
        z = self.l2_neigh(agg2) + self.l2_self(h1)
        if self.normalize:
            z = self._l2(z)
        return z

    def forward_full(self, x: Tensor, edge_index: Tensor) -> Tensor:
        """Logits com inferencia exata (o artigo infere sem amostragem no teste)."""
        return self.classifier(self.embed_full(x, edge_index))


# --------------------------------------------------------------------------- #
# Verificacoes                                                                 #
# --------------------------------------------------------------------------- #

def _check_sampler() -> bool:
    """Todo vizinho amostrado deve ser um vizinho real do no."""
    torch.manual_seed(0)
    n_nodes, n_edges = 200, 2000
    edge_index = torch.randint(0, n_nodes, (2, n_edges))
    s = NeighborSampler(edge_index, n_nodes)

    nodes = torch.arange(n_nodes)
    neigh, valid = s.sample(nodes, 12)

    # conjunto de referencia, calculado de forma ingenua
    real = [set(edge_index[0][edge_index[1] == v].tolist()) for v in range(n_nodes)]
    erros = 0
    for v in range(n_nodes):
        if not real[v]:
            continue
        if not set(neigh[v].tolist()).issubset(real[v]):
            erros += 1
    isolados = int((valid.squeeze() == 0).sum())
    print(f"  nos com vizinho amostrado invalido: {erros} / {n_nodes}")
    print(f"  nos de grau zero (marcados invalidos): {isolados}")
    return erros == 0


def _check_replacement() -> bool:
    """Grau 1 e amostra 5 -> o mesmo vizinho deve repetir 5 vezes (com reposicao)."""
    edge_index = torch.tensor([[7], [3]])   # unica aresta: 7 -> 3
    s = NeighborSampler(edge_index, 10)
    neigh, valid = s.sample(torch.tensor([3]), 5)
    ok = bool((neigh == 7).all()) and float(valid[0]) == 1.0
    print(f"  grau 1, amostra 5 -> {neigh.tolist()[0]}  {'OK' if ok else 'FALHOU'}")
    return ok


def _check_l2() -> bool:
    """A REPRESENTACAO z deve ter norma 1; os LOGITS nao devem ser normalizados."""
    m = SampledGraphSAGE(8, 16, 4, normalize=True)
    x = torch.randn(30, 8)
    edge_index = torch.randint(0, 30, (2, 150))

    normas_z = m.embed_full(x, edge_index).norm(dim=-1)
    z_ok = torch.allclose(normas_z, torch.ones_like(normas_z), atol=1e-5)
    print(f"  norma L2 de z: min={normas_z.min():.6f} max={normas_z.max():.6f} "
          f"{'OK' if z_ok else 'FALHOU'}")

    normas_logit = m.forward_full(x, edge_index).norm(dim=-1)
    logit_ok = not torch.allclose(normas_logit, torch.ones_like(normas_logit), atol=1e-3)
    print(f"  norma dos logits: min={normas_logit.min():.4f} max={normas_logit.max():.4f} "
          f"-> {'livre, OK' if logit_ok else 'presa em 1, FALHOU'}")
    return z_ok and logit_ok


def _check_shapes() -> bool:
    """O forward amostrado deve devolver uma linha por semente."""
    torch.manual_seed(3)
    n_nodes = 500
    edge_index = torch.randint(0, n_nodes, (2, 5000))
    x = torch.randn(n_nodes, 12)
    m = SampledGraphSAGE(12, 32, 7)
    s = NeighborSampler(edge_index, n_nodes)
    seeds = torch.randperm(n_nodes)[:64]
    out = m.forward_sampled(x, s, seeds, s_hop1=10, s_hop2=25)
    ok = out.shape == (64, 7)
    print(f"  forward_sampled: {tuple(out.shape)} esperado (64, 7)  "
          f"{'OK' if ok else 'FALHOU'}")
    return ok


def main() -> None:
    print("Verificacao da amostragem de vizinhanca (Algoritmo 2)")
    print("=" * 58)
    print("\n[1] Vizinhos amostrados sao vizinhos reais:")
    a = _check_sampler()
    print("\n[2] Amostragem com reposicao:")
    b = _check_replacement()
    print("\n[3] Normalizacao L2 por camada (Algoritmo 1, linha 7):")
    c = _check_l2()
    print("\n[4] Shapes do forward em minibatch:")
    d = _check_shapes()
    print("\n" + "=" * 58)
    print("RESULTADO:", "todas as verificacoes passaram" if all((a, b, c, d))
          else "HA FALHA -- revisar")


if __name__ == "__main__":
    main()
