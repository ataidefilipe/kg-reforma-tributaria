"""
Reproducao FIEL do GraphSAGE supervisionado em PPI.

Hamilton, Ying & Leskovec (2017), NeurIPS. arXiv:1706.02216

Usa a implementacao propria (`sage_sampler.py`), nao o `SAGEConv`/`NeighborLoader` do PyG.
Motivos e pontos de fidelidade estao documentados naquele arquivo.

--------------------------------------------------------------------------------------
Configuracao declarada no artigo (Apendice, "Hyperparameter selection"):

    K (profundidade)            2
    dimensao de h^k             256 em toda profundidade k
    tamanho de batch            512
    epocas (supervisionado)     10
    learning rate               varrido em {0.01, 0.001, 0.0001}
    nao-linearidade             ReLU
    amostragem                  S1 = 25, S2 = 10
    normalizacao                L2 por camada (Algoritmo 1, linha 7)

Resultado do artigo, Tabela 1, coluna PPI supervisionado:

    Random               0.396
    Raw features         0.422    <- baseline "so features, sem grafo"
    GraphSAGE-GCN        0.500
    GraphSAGE-mean       0.598    <- alvo desta reproducao
    GraphSAGE-LSTM       0.612
    GraphSAGE-pool       0.600

--------------------------------------------------------------------------------------
Uso:
    python -m src.modeling.reproduce_ppi                      # fiel ao artigo
    python -m src.modeling.reproduce_ppi --lr-sweep           # varredura do artigo
    python -m src.modeling.reproduce_ppi --sampling full      # ablacao: sem amostragem
    python -m src.modeling.reproduce_ppi --no-normalize       # ablacao: sem L2
"""

from __future__ import annotations

import argparse
import csv
import platform
import random
import time
from pathlib import Path

import numpy as np
import torch
from sklearn.metrics import f1_score

from src.modeling.sage_sampler import NeighborSampler, SampledGraphSAGE

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
REPORT_DIR = ROOT / "reports" / "analysis"

PAPER_PPI_SUP = {
    "Random": 0.396,
    "Raw features": 0.422,
    "GraphSAGE-GCN": 0.500,
    "GraphSAGE-mean": 0.598,
    "GraphSAGE-LSTM": 0.612,
    "GraphSAGE-pool": 0.600,
}
ALVO = PAPER_PPI_SUP["GraphSAGE-mean"]


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def cap_degree(edge_index: torch.Tensor, num_nodes: int, max_degree: int,
               seed: int = 42) -> torch.Tensor:
    """Subamostra arestas para que nenhum no tenha grau maior que `max_degree`.

    O artigo faz isso como pre-processamento (Apendice A):

        "we subsample edges so that no node has degree larger than 128. Since we only
         sample at most 25 neighbors per node, this is a reasonable tradeoff."

    Embaralha as arestas antes de cortar, para que as mantidas sejam uma amostra
    uniforme da vizinhanca e nao as primeiras da lista.
    """
    g = torch.Generator().manual_seed(seed)
    ei = edge_index[:, torch.randperm(edge_index.size(1), generator=g)]

    ordem = torch.argsort(ei[1], stable=True)          # agrupa por destino
    dst_ord = ei[1][ordem]
    deg = torch.bincount(dst_ord, minlength=num_nodes)
    ptr = torch.cat([torch.zeros(1, dtype=torch.long), deg.cumsum(0)])
    # posicao de cada aresta dentro do seu grupo de destino
    rank = torch.arange(dst_ord.size(0)) - ptr[dst_ord]
    return ei[:, ordem[rank < max_degree]]


def load_ppi(max_degree: int | None = 128):
    from torch_geometric.data import Batch
    from torch_geometric.datasets import PPI

    train_ds = PPI(DATA_DIR / "PPI", split="train")
    val_ds = PPI(DATA_DIR / "PPI", split="val")
    test_ds = PPI(DATA_DIR / "PPI", split="test")
    # os 20 grafos de treino viram um Data unico com componentes desconexas;
    # nenhuma aresta espuria e criada
    train_data = Batch.from_data_list(list(train_ds))

    if max_degree:
        antes = train_data.num_edges
        train_data.edge_index = cap_degree(train_data.edge_index,
                                           train_data.num_nodes, max_degree)
        print(f"     subamostragem de grau <= {max_degree}: "
              f"{antes:,} -> {train_data.num_edges:,} arestas "
              f"({(1 - train_data.num_edges/antes)*100:.1f}% removidas)")
    return train_ds, train_data, list(val_ds), list(test_ds)


@torch.no_grad()
def evaluate(model, graphs) -> float:
    """micro-F1 com inferencia EXATA (vizinhanca completa), como o artigo faz no teste."""
    model.eval()
    preds, trues = [], []
    for g in graphs:
        logits = model.forward_full(g.x, g.edge_index)
        preds.append((logits > 0).float())
        trues.append(g.y)
    return f1_score(torch.cat(trues), torch.cat(preds), average="micro", zero_division=0)


def train_one(args, dados, verbose: bool = True) -> list[dict]:
    train_ds, train_data, val_graphs, test_graphs = dados

    model = SampledGraphSAGE(train_ds.num_features, args.hidden, train_ds.num_classes,
                             normalize=not args.no_normalize)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    criterion = torch.nn.BCEWithLogitsLoss()

    sampler = NeighborSampler(train_data.edge_index, train_data.num_nodes)
    n_nodes = train_data.num_nodes
    x, y = train_data.x, train_data.y

    if verbose:
        print(f"PPI  treino={len(train_ds)} grafos ({n_nodes:,} nos, "
              f"{train_data.num_edges:,} arestas) | val={len(val_graphs)} | "
              f"teste={len(test_graphs)}")
        print(f"     features={train_ds.num_features} | classes={train_ds.num_classes}")
        modo = (f"amostragem S1={args.s1} S2={args.s2} (1o salto={args.s2}, "
                f"2o salto={args.s1}), batch={args.batch_size}"
                if args.sampling == "neighbor" else "FULL-BATCH (ablacao)")
        print(f"     {modo} | L2 por camada: {not args.no_normalize}")

    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        perm = torch.randperm(n_nodes)
        total_loss, n_seen = 0.0, 0

        for i in range(0, n_nodes, args.batch_size):
            seeds = perm[i:i + args.batch_size]
            opt.zero_grad()
            if args.sampling == "neighbor":
                out = model.forward_sampled(x, sampler, seeds, args.s2, args.s1)
            else:
                out = model.forward_full(x, train_data.edge_index)[seeds]
            loss = criterion(out, y[seeds])
            loss.backward()
            opt.step()
            total_loss += float(loss.detach()) * seeds.size(0)
            n_seen += seeds.size(0)

        row = {
            "epoch": epoch,
            "loss": total_loss / n_seen,
            "val_micro_f1": evaluate(model, val_graphs),
            "test_micro_f1": evaluate(model, test_graphs),
        }
        history.append(row)
        if verbose:
            print(f"  ep {epoch:3d} | loss {row['loss']:.4f} "
                  f"| val F1 {row['val_micro_f1']:.4f} | test F1 {row['test_micro_f1']:.4f}")
    return history


def report(history: list[dict], elapsed: float, tag: str, verbose: bool = True) -> dict:
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    out_csv = REPORT_DIR / f"reproduce_ppi_{tag}.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(history[0].keys()))
        w.writeheader()
        w.writerows(history)

    # selecao de modelo pela VALIDACAO, nunca pelo teste
    best = max(history, key=lambda r: r["val_micro_f1"])
    if verbose:
        print(f"\n  tempo: {elapsed:.1f}s | csv: {out_csv.relative_to(ROOT)}")
        print(f"  melhor epoca por validacao : {best['epoch']} "
              f"(val {best['val_micro_f1']:.4f})")
        print(f"  test micro-F1 nessa epoca  : {best['test_micro_f1']:.4f}")
        print(f"  artigo, GraphSAGE-mean     : {ALVO:.4f}  "
              f"(delta {best['test_micro_f1'] - ALVO:+.4f})")
    return best


def main() -> None:
    p = argparse.ArgumentParser(description="Reproducao fiel do GraphSAGE em PPI")
    p.add_argument("--sampling", choices=["neighbor", "full"], default="neighbor")
    p.add_argument("--hidden", type=int, default=256, help="artigo: 256")
    p.add_argument("--epochs", type=int, default=10, help="artigo: 10")
    p.add_argument("--batch-size", type=int, default=512, help="artigo: 512")
    p.add_argument("--lr", type=float, default=0.01)
    p.add_argument("--s1", type=int, default=25, help="artigo: 25 (2o salto)")
    p.add_argument("--s2", type=int, default=10, help="artigo: 10 (1o salto)")
    p.add_argument("--no-normalize", action="store_true",
                   help="ablacao: desliga a normalizacao L2 do Algoritmo 1")
    p.add_argument("--max-degree", type=int, default=128,
                   help="artigo: subamostra arestas p/ grau <= 128 (0 desliga)")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--lr-sweep", action="store_true")
    args = p.parse_args()

    print(f"Python {platform.python_version()} | torch {torch.__version__} "
          f"| cuda {torch.cuda.is_available()}")
    dados = load_ppi(max_degree=args.max_degree or None)

    if args.lr_sweep:
        print("\nVarredura de learning rate do artigo: {0.01, 0.001, 0.0001}")
        print("=" * 62)
        res = {}
        for lr in (0.01, 0.001, 0.0001):
            args.lr = lr
            set_seed(args.seed)
            t0 = time.perf_counter()
            hist = train_one(args, dados, verbose=False)
            best = report(hist, time.perf_counter() - t0,
                          f"{args.sampling}_lr{lr}", verbose=False)
            res[lr] = best
            print(f"  lr={lr:<8} val {best['val_micro_f1']:.4f} | "
                  f"test {best['test_micro_f1']:.4f} | epoca {best['epoch']} "
                  f"| {time.perf_counter()-t0:.0f}s")
        melhor = max(res, key=lambda k: res[k]["val_micro_f1"])
        print("=" * 62)
        print(f"  melhor lr por validacao: {melhor}")
        print(f"  test micro-F1          : {res[melhor]['test_micro_f1']:.4f}")
        print(f"  artigo GraphSAGE-mean  : {ALVO:.4f}  "
              f"(delta {res[melhor]['test_micro_f1'] - ALVO:+.4f})")
        return

    set_seed(args.seed)
    print(f"Config: {vars(args)}\n")
    t0 = time.perf_counter()
    hist = train_one(args, dados)
    tag = f"{args.sampling}_lr{args.lr}" + ("_nonorm" if args.no_normalize else "")
    report(hist, time.perf_counter() - t0, tag)


if __name__ == "__main__":
    main()
