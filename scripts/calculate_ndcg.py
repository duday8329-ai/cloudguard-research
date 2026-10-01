"""Calculate NDCG@k when an independently created relevance file is supplied."""
from __future__ import annotations

import csv
import math
import sys
from pathlib import Path


def dcg(scores: list[int]) -> float:
    return sum((2**score - 1) / math.log2(index + 2) for index, score in enumerate(scores))


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("Usage: python calculate_ndcg.py ranking.csv k")
    path, k = Path(sys.argv[1]), int(sys.argv[2])
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    observed = [int(row["expert_relevance"]) for row in rows[:k]]
    ideal = sorted((int(row["expert_relevance"]) for row in rows), reverse=True)[:k]
    value = dcg(observed) / dcg(ideal) if dcg(ideal) else 0.0
    print(f"NDCG@{k}: {value:.4f}")


if __name__ == "__main__":
    main()
