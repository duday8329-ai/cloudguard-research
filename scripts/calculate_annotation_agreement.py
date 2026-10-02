"""Validate reviewer labels, calculate Cohen's kappa, and write consensus."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_rows(name: str) -> dict[str, dict[str, str]]:
    with (ROOT / "annotations" / name).open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    result = {row["instance_id"]: row for row in rows}
    if len(result) != len(rows):
        raise ValueError(f"{name} contains duplicate instance_id values")
    return result


def main() -> None:
    reviewer_1 = read_rows("expert_1.csv")
    reviewer_2 = read_rows("expert_2.csv")
    if set(reviewer_1) != set(reviewer_2):
        raise ValueError("Reviewer files do not contain the same instance IDs")

    ids = sorted(reviewer_1)
    labels_1 = [reviewer_1[item]["reviewer_label"] for item in ids]
    labels_2 = [reviewer_2[item]["reviewer_label"] for item in ids]
    if any(label not in {"0", "1"} for label in labels_1 + labels_2):
        raise ValueError("Reviewer labels must be 0 or 1")

    agreements = sum(left == right for left, right in zip(labels_1, labels_2))
    observed = agreements / len(ids) if ids else 0.0
    positive_1 = sum(label == "1" for label in labels_1) / len(ids) if ids else 0.0
    positive_2 = sum(label == "1" for label in labels_2) / len(ids) if ids else 0.0
    expected = positive_1 * positive_2 + (1 - positive_1) * (1 - positive_2)
    kappa = (observed - expected) / (1 - expected) if expected != 1 else 1.0

    consensus_rows = []
    for item in ids:
        left = reviewer_1[item]
        right = reviewer_2[item]
        if left["reviewer_label"] != right["reviewer_label"]:
            raise ValueError(f"Reviewer disagreement requires adjudication: {item}")
        consensus_rows.append({
            "instance_id": item,
            "file_id": left["file_id"],
            "format": left["format"],
            "resource_id": left["resource_id"],
            "policy_sid": left["policy_sid"],
            "expected_violation": left["reviewer_label"],
            "severity": left["severity"],
            "annotation_source": "two_reviewer_consensus",
        })

    consensus_path = ROOT / "annotations" / "reviewer_consensus.csv"
    with consensus_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(consensus_rows[0]))
        writer.writeheader()
        writer.writerows(consensus_rows)

    result = {
        "reviewer_1_rows": len(labels_1),
        "reviewer_2_rows": len(labels_2),
        "agreements": agreements,
        "disagreements": len(ids) - agreements,
        "observed_agreement": round(observed, 4),
        "cohens_kappa": round(kappa, 4),
        "reviewer_1_counts": {"0": labels_1.count("0"), "1": labels_1.count("1")},
        "reviewer_2_counts": {"0": labels_2.count("0"), "1": labels_2.count("1")},
        "consensus_path": str(consensus_path.relative_to(ROOT)),
    }
    result_path = ROOT / "results" / "annotations" / "agreement.json"
    result_path.parent.mkdir(parents=True, exist_ok=True)
    result_path.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
