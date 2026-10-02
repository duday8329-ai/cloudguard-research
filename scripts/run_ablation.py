"""Run leave-one-policy-out ablations on the frozen benchmark."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from run_cloudguard import RULES

ROOT = Path(__file__).resolve().parents[1]
POLICIES = list(RULES)


def main() -> None:
    with (ROOT / "annotations" / "reviewer_consensus.csv").open(newline="", encoding="utf-8-sig") as handle:
        truth = list(csv.DictReader(handle))
    with (ROOT / "benchmark" / "benchmark_manifest.csv").open(newline="", encoding="utf-8-sig") as handle:
        manifest = list(csv.DictReader(handle))

    predictions_by_file = {}
    for item in manifest:
        text = (ROOT / item["path"]).read_text(encoding="utf-8")
        predictions_by_file[item["file_id"]] = {sid for sid, pattern in RULES.items() if pattern.search(text)}

    variants = {"full": None} | {f"without_{sid}": sid for sid in POLICIES}
    output_dir = ROOT / "results" / "ablation"
    output_dir.mkdir(parents=True, exist_ok=True)
    summary = []
    for variant, removed in variants.items():
        predictions = {(file_id, sid) for file_id, found in predictions_by_file.items() for sid in found if sid != removed}
        matrix = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
        labelled = {(row["file_id"], row["policy_sid"]) for row in truth}
        for row in truth:
            actual = row["expected_violation"] == "1"
            predicted = (row["file_id"], row["policy_sid"]) in predictions
            matrix["tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"] += 1
        matrix["fp"] += len(predictions - labelled)
        precision = matrix["tp"] / (matrix["tp"] + matrix["fp"]) if matrix["tp"] + matrix["fp"] else 0.0
        recall = matrix["tp"] / (matrix["tp"] + matrix["fn"]) if matrix["tp"] + matrix["fn"] else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        result = {"variant": variant, "removed_policy": removed or "none", **matrix, "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}
        summary.append(result)
        (output_dir / f"{variant}.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    with (output_dir / "summary.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
