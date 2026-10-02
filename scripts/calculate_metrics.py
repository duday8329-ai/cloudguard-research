"""Calculate a confusion matrix from raw predictions and consensus labels."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    truth_name = sys.argv[1] if len(sys.argv) > 1 else "annotations/consensus.csv"
    truth_path = ROOT / truth_name
    with truth_path.open(newline="", encoding="utf-8") as handle:
        truth = list(csv.DictReader(handle))
    with (ROOT / "results" / "cloudguard" / "predictions.csv").open(newline="", encoding="utf-8") as handle:
        predictions = {(r["file_id"], r["policy_sid"]) for r in csv.DictReader(handle) if r["violation"] == "1"}
    matrix = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    labelled = {(r["file_id"], r["policy_sid"]) for r in truth}
    for row in truth:
        predicted = (row["file_id"], row["policy_sid"]) in predictions
        actual = row["expected_violation"] == "1"
        matrix["tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"] += 1
    extra = predictions - labelled
    matrix["fp"] += len(extra)
    precision = matrix["tp"] / (matrix["tp"] + matrix["fp"]) if matrix["tp"] + matrix["fp"] else 0.0
    recall = matrix["tp"] / (matrix["tp"] + matrix["fn"]) if matrix["tp"] + matrix["fn"] else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    source = truth[0].get("annotation_source", "project_team_predefined_policy_criteria") if truth else "unknown"
    result = {"analyzer": "cloudguard", "benchmark_status": "reviewer_consensus_synthetic_benchmark", "annotation_source": source, "truth_file": Path(truth_name).as_posix(), "labelled_policy_instances": len(truth), "confusion_matrix": matrix, "precision": round(precision, 4), "recall": round(recall, 4), "f1": round(f1, 4)}
    output = ROOT / "results" / "cloudguard" / "metrics.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
