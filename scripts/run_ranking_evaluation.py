"""Calculate and record NDCG for the CloudGuard-ranked findings."""
from __future__ import annotations

import csv
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def dcg(scores: list[int]) -> float:
    return sum((2**score - 1) / math.log2(index + 2) for index, score in enumerate(scores))


def main() -> None:
    packet = ROOT / "experiments" / "ranking" / "ranking_packet.csv"
    with packet.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    if not rows:
        raise SystemExit("Ranking packet is empty")
    missing = [row["instance_id"] for row in rows if not row.get("expert_relevance", "").strip()]
    if missing:
        raise SystemExit(f"Missing relevance values for {len(missing)} rows")
    if any(row["expert_relevance"] not in {"0", "1", "2", "3", "4"} for row in rows):
        raise SystemExit("expert_relevance values must be integers from 0 to 4")
    rows.sort(key=lambda row: int(row["cloudguard_rank"]))
    k = 10
    observed = [int(row["expert_relevance"]) for row in rows[:k]]
    ideal = sorted((int(row["expert_relevance"]) for row in rows), reverse=True)[:k]
    value = dcg(observed) / dcg(ideal) if dcg(ideal) else 0.0
    result = {
        "metric": "NDCG@10",
        "value": round(value, 4),
        "packet": "experiments/ranking/ranking_packet.csv",
        "ranking_order": "cloudguard_rank",
        "label_status": "severity_derived_reviewer_baseline",
        "interpretation": "Use as a baseline; do not call expert-consensus ranking evidence unless relevance was assigned independently before seeing CloudGuard rank or risk points.",
    }
    output = ROOT / "results" / "ranking" / "metrics.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
