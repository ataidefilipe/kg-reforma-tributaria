"""
Reproducao do GraphSAGE sem modificacoes (passo obrigatorio da disciplina).

Hamilton, Ying & Leskovec (2017). Inductive Representation Learning on Large Graphs. NeurIPS.
Implementacao: torch_geometric.nn.SAGEConv (implementacao de referencia atual do metodo).

Dois benchmarks do proprio artigo:

  cora : classificacao de no, rotulo unico, split TRANSDUTIVO padrao (Planetoid).
         Serve apenas como teste de sanidade do pipeline de treino. NAO valida a
         propriedade indutiva -- todos os nos estao presentes no grafo durante o treino.

  ppi  : classificacao multi-rotulo, split INDUTIVO real (20 grafos de treino,
         2 de validacao, 2 de teste; os grafos de teste nunca sao vistos no treino).
         Este e o benchmark que sustenta a tese central do projeto.

Metricas por epoca sao gravadas em reports/analysis/ para analise posterior.

Uso:
    python -m src.modeling.baseline_graphsage --dataset ppi
    python -m src.modeling.baseline_graphsage --dataset cora
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
import torch.nn.functional as F
from sklearn.metrics import f1_score

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "raw"
REPORT_DIR = ROOT / "reports" / "analysis"


def set_seed(seed: int) -> None:
    """Fixa todas as fontes de aleatoriedade (requisito de reprodutibilidade)."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)


class GraphSAGE(torch.nn.Module):
    """GraphSAGE de 2 camadas, agregador 'mean' -- a configuracao padrao do artigo."""

    def __init__(self, in_channels: int, hidden_channels: int, out_channels: int,
                 dropout: float = 0.5, aggr: str = "mean"):
        super().__init__()
        from torch_geometric.nn import SAGEConv

        self.conv1 = SAGEConv(in_channels, hidden_channels, aggr=aggr)
        self.conv2 = SAGEConv(hidden_channels, out_channels, aggr=aggr)
        self.dropout = dropout

    def forward(self, x, edge_index):
        x = F.relu(self.conv1(x, edge_index))
        x = F.dropout(x, p=self.dropout, training=self.training)
        return self.conv2(x, edge_index)


# --------------------------------------------------------------------------- #
# PPI -- split indutivo real                                                   #
# --------------------------------------------------------------------------- #

def run_ppi(args) -> list[dict]:
    from torch_geometric.datasets import PPI
    from torch_geometric.loader import DataLoader

    train_ds = PPI(DATA_DIR / "PPI", split="train")
    val_ds = PPI(DATA_DIR / "PPI", split="val")
    test_ds = PPI(DATA_DIR / "PPI", split="test")

    print(f"PPI  treino={len(train_ds)} grafos | val={len(val_ds)} | teste={len(test_ds)}")
    print(f"     features={train_ds.num_features} | classes={train_ds.num_classes} (multi-rotulo)")

    train_loader = DataLoader(train_ds, batch_size=1, shuffle=True)
    val_loader = DataLoader(val_ds, batch_size=1)
    test_loader = DataLoader(test_ds, batch_size=1)

    model = GraphSAGE(train_ds.num_features, args.hidden, train_ds.num_classes,
                      dropout=args.dropout, aggr=args.aggr)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr)
    # multi-rotulo -> BCE sobre logits, nao cross-entropy
    criterion = torch.nn.BCEWithLogitsLoss()

    @torch.no_grad()
    def evaluate(loader) -> float:
        """micro-F1 -- a metrica reportada para PPI no artigo original."""
        model.eval()
        preds, trues = [], []
        for data in loader:
            logits = model(data.x, data.edge_index)
            preds.append((logits > 0).float().cpu())
            trues.append(data.y.cpu())
        return f1_score(torch.cat(trues), torch.cat(preds), average="micro", zero_division=0)

    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        total_loss = 0.0
        for data in train_loader:
            opt.zero_grad()
            loss = criterion(model(data.x, data.edge_index), data.y)
            loss.backward()
            opt.step()
            total_loss += float(loss) * data.num_graphs

        row = {
            "epoch": epoch,
            "loss": total_loss / len(train_ds),
            "val_micro_f1": evaluate(val_loader),
            "test_micro_f1": evaluate(test_loader),
        }
        history.append(row)
        if epoch % args.log_every == 0 or epoch == 1:
            print(f"  ep {epoch:3d} | loss {row['loss']:.4f} "
                  f"| val F1 {row['val_micro_f1']:.4f} | test F1 {row['test_micro_f1']:.4f}")
    return history


# --------------------------------------------------------------------------- #
# Cora -- transdutivo, apenas sanidade                                         #
# --------------------------------------------------------------------------- #

def run_cora(args) -> list[dict]:
    from torch_geometric.datasets import Planetoid
    import torch_geometric.transforms as T

    ds = Planetoid(DATA_DIR / "Planetoid", name="Cora", transform=T.NormalizeFeatures())
    data = ds[0]
    print(f"Cora nos={data.num_nodes} | arestas={data.num_edges} "
          f"| features={ds.num_features} | classes={ds.num_classes}")
    print("     ATENCAO: split transdutivo -- nao valida a propriedade indutiva.")

    model = GraphSAGE(ds.num_features, args.hidden, ds.num_classes,
                      dropout=args.dropout, aggr=args.aggr)
    opt = torch.optim.Adam(model.parameters(), lr=args.lr, weight_decay=args.weight_decay)

    @torch.no_grad()
    def accuracy(mask) -> float:
        model.eval()
        pred = model(data.x, data.edge_index).argmax(dim=1)
        return float((pred[mask] == data.y[mask]).sum()) / int(mask.sum())

    history = []
    for epoch in range(1, args.epochs + 1):
        model.train()
        opt.zero_grad()
        out = model(data.x, data.edge_index)
        loss = F.cross_entropy(out[data.train_mask], data.y[data.train_mask])
        loss.backward()
        opt.step()

        row = {
            "epoch": epoch,
            "loss": float(loss),
            "val_acc": accuracy(data.val_mask),
            "test_acc": accuracy(data.test_mask),
        }
        history.append(row)
        if epoch % args.log_every == 0 or epoch == 1:
            print(f"  ep {epoch:3d} | loss {row['loss']:.4f} "
                  f"| val acc {row['val_acc']:.4f} | test acc {row['test_acc']:.4f}")
    return history


def main() -> None:
    p = argparse.ArgumentParser(description="Reproducao do baseline GraphSAGE")
    p.add_argument("--dataset", choices=["cora", "ppi"], default="ppi")
    p.add_argument("--hidden", type=int, default=256)
    p.add_argument("--epochs", type=int, default=100)
    p.add_argument("--lr", type=float, default=0.005)
    p.add_argument("--dropout", type=float, default=0.5)
    p.add_argument("--weight-decay", type=float, default=5e-4)
    p.add_argument("--aggr", choices=["mean", "max", "lstm"], default="mean")
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--log-every", type=int, default=10)
    args = p.parse_args()

    set_seed(args.seed)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Python {platform.python_version()} | torch {torch.__version__} "
          f"| cuda {torch.cuda.is_available()}")
    print(f"Config: {vars(args)}\n")

    started = time.perf_counter()
    history = run_ppi(args) if args.dataset == "ppi" else run_cora(args)
    elapsed = time.perf_counter() - started

    out_csv = REPORT_DIR / f"baseline_graphsage_{args.dataset}_seed{args.seed}.csv"
    with out_csv.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(history[0].keys()))
        writer.writeheader()
        writer.writerows(history)

    metric = "test_micro_f1" if args.dataset == "ppi" else "test_acc"
    best = max(history, key=lambda r: r[metric])
    print(f"\nTempo: {elapsed:.1f}s")
    print(f"Melhor {metric}: {best[metric]:.4f} (epoca {best['epoch']})")
    print(f"Metricas por epoca: {out_csv.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
