"""
Implementacao manual do agregador mean do GraphSAGE, a partir do Algoritmo 1 do artigo.

Objetivo: demonstrar entendimento do codigo base (exigencia do slide 6 do professor),
validando a implementacao propria contra o `SAGEConv` do PyTorch Geometric.

--------------------------------------------------------------------------------------
Algoritmo 1 do artigo (Hamilton et al., 2017), passo de agregacao para K camadas:

    h_N(v)^k  <-  AGGREGATE_k ( { h_u^(k-1), u in N(v) } )
    h_v^k     <-  sigma ( W^k . CONCAT( h_v^(k-1), h_N(v)^k ) )

Com AGGREGATE = mean, isto e:

    h_v^k = sigma( W . [ h_v^(k-1) ; mean_{u in N(v)} h_u^(k-1) ] + b )

--------------------------------------------------------------------------------------
Equivalencia com o SAGEConv do PyG:

O PyG nao usa CONCAT + uma matriz W. Usa duas matrizes lineares separadas:

    out = lin_l( mean(vizinhos) )  +  lin_r( x_proprio )

Isso e algebricamente identico a concatenacao, porque uma matriz W aplicada a um vetor
concatenado se decompoe em blocos:

    W . [a ; b] = W_a . a  +  W_b . b

onde W_a e W_b sao os blocos de colunas de W. Logo:
    lin_r  <->  bloco do no proprio   (bias=False no PyG)
    lin_l  <->  bloco dos vizinhos    (carrega o bias)

A funcao `check_equivalence()` abaixo prova isso numericamente.

--------------------------------------------------------------------------------------
Uso:
    python -m src.modeling.sage_manual
"""

from __future__ import annotations

import torch
from torch import Tensor


class ManualSAGEConv(torch.nn.Module):
    """Camada GraphSAGE com agregador mean, escrita do zero.

    Nao usa message passing do PyG -- a agregacao e feita explicitamente com
    `index_add_`, para deixar visivel o que o Algoritmo 1 faz.
    """

    def __init__(self, in_channels: int, out_channels: int, bias: bool = True):
        super().__init__()
        # bloco dos vizinhos (carrega o bias, como no PyG)
        self.lin_neigh = torch.nn.Linear(in_channels, out_channels, bias=bias)
        # bloco do proprio no (sem bias, como no PyG)
        self.lin_self = torch.nn.Linear(in_channels, out_channels, bias=False)

    @staticmethod
    def mean_aggregate(x: Tensor, edge_index: Tensor) -> Tensor:
        """Media das features dos vizinhos de cada no.

        edge_index[0] = origem (u), edge_index[1] = destino (v).
        Convencao do PyG: a mensagem flui de u para v, entao agregamos em v as
        features de u.

        Nos sem vizinho recebem vetor zero -- mesmo comportamento do PyG.
        """
        src, dst = edge_index[0], edge_index[1]
        num_nodes = x.size(0)

        soma = torch.zeros(num_nodes, x.size(1), dtype=x.dtype, device=x.device)
        soma.index_add_(0, dst, x[src])

        grau = torch.zeros(num_nodes, dtype=x.dtype, device=x.device)
        grau.index_add_(0, dst, torch.ones_like(dst, dtype=x.dtype))
        grau = grau.clamp(min=1).unsqueeze(-1)  # evita divisao por zero

        return soma / grau

    def forward(self, x: Tensor, edge_index: Tensor) -> Tensor:
        h_neigh = self.mean_aggregate(x, edge_index)
        return self.lin_neigh(h_neigh) + self.lin_self(x)


# --------------------------------------------------------------------------- #
# Validacao contra a implementacao de referencia                              #
# --------------------------------------------------------------------------- #

def check_equivalence(in_ch: int = 16, out_ch: int = 8, num_nodes: int = 50,
                      num_edges: int = 200, seed: int = 0, tol: float = 1e-5) -> bool:
    """Copia os pesos do SAGEConv do PyG para a implementacao manual e compara a saida.

    Se as duas baterem, a leitura do Algoritmo 1 esta correta.
    """
    from torch_geometric.nn import SAGEConv

    torch.manual_seed(seed)

    x = torch.randn(num_nodes, in_ch)
    edge_index = torch.randint(0, num_nodes, (2, num_edges))

    ref = SAGEConv(in_ch, out_ch, aggr="mean")
    meu = ManualSAGEConv(in_ch, out_ch)

    # transplante de pesos: lin_l = vizinhos (com bias), lin_r = no proprio
    with torch.no_grad():
        meu.lin_neigh.weight.copy_(ref.lin_l.weight)
        meu.lin_neigh.bias.copy_(ref.lin_l.bias)
        meu.lin_self.weight.copy_(ref.lin_r.weight)

    ref.eval()
    meu.eval()
    with torch.no_grad():
        out_ref = ref(x, edge_index)
        out_meu = meu(x, edge_index)

    diff = (out_ref - out_meu).abs().max().item()
    ok = diff < tol

    print(f"  shape PyG    : {tuple(out_ref.shape)}")
    print(f"  shape manual : {tuple(out_meu.shape)}")
    print(f"  diferenca maxima absoluta: {diff:.3e}  (tolerancia {tol:.0e})")
    print(f"  {'EQUIVALENTE' if ok else 'DIVERGENTE'}")
    return ok


def check_isolated_nodes() -> bool:
    """Caso limite: no sem nenhum vizinho deve receber agregacao zero."""
    from torch_geometric.nn import SAGEConv

    torch.manual_seed(1)
    x = torch.randn(5, 4)
    # no 4 fica isolado; nenhuma aresta aponta para ele
    edge_index = torch.tensor([[0, 1, 2], [1, 2, 3]])

    ref = SAGEConv(4, 3, aggr="mean")
    meu = ManualSAGEConv(4, 3)
    with torch.no_grad():
        meu.lin_neigh.weight.copy_(ref.lin_l.weight)
        meu.lin_neigh.bias.copy_(ref.lin_l.bias)
        meu.lin_self.weight.copy_(ref.lin_r.weight)

    ref.eval(); meu.eval()
    with torch.no_grad():
        diff = (ref(x, edge_index) - meu(x, edge_index)).abs().max().item()
    ok = diff < 1e-5
    print(f"  no isolado -> diferenca maxima: {diff:.3e}  {'OK' if ok else 'FALHOU'}")
    return ok


def main() -> None:
    print("Validacao da implementacao manual do GraphSAGE (agregador mean)")
    print("=" * 62)
    print("\n[1] Grafo aleatorio, pesos transplantados do SAGEConv do PyG:")
    a = check_equivalence()
    print("\n[2] Caso limite -- no sem vizinhos:")
    b = check_isolated_nodes()
    print("\n[3] Dimensoes maiores (in=128, out=64, 500 nos):")
    c = check_equivalence(in_ch=128, out_ch=64, num_nodes=500, num_edges=3000, seed=7)

    print("\n" + "=" * 62)
    print("RESULTADO:", "todas as verificacoes passaram" if (a and b and c)
          else "HA DIVERGENCIA -- revisar a implementacao")


if __name__ == "__main__":
    main()
