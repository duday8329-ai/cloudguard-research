"""Create a ranked packet for independent expert relevance scoring."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEIGHTS = {
    "POL_AWS_S3_PUBLIC": 28,
    "POL_AWS_RDS_PUBLIC": 25,
    "POL_AWS_SG_UNRESTRICTED": 18,
    "POL_AWS_IAM_WILDCARD": 18,
    "POL_AWS_RDS_ENCRYPTION": 14,
}


def main() -> None:
    with (ROOT / "annotations" / "reviewer_consensus.csv").open(newline="", encoding="utf-8-sig") as handle:
        truth = list(csv.DictReader(handle))
    positives = [row for row in truth if row["expected_violation"] == "1"]
    positives.sort(key=lambda row: (-WEIGHTS[row["policy_sid"]], row["file_id"], row["policy_sid"]))
    output = ROOT / "experiments" / "ranking" / "ranking_packet.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = ["cloudguard_rank", "instance_id", "file_id", "format", "resource_id", "policy_sid", "severity", "risk_points", "expert_relevance"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for rank, row in enumerate(positives, start=1):
            writer.writerow({
                "cloudguard_rank": rank,
                "instance_id": row["instance_id"],
                "file_id": row["file_id"],
                "format": row["format"],
                "resource_id": row["resource_id"],
                "policy_sid": row["policy_sid"],
                "severity": row["severity"],
                "risk_points": WEIGHTS[row["policy_sid"]],
                "expert_relevance": "",
            })
    print(f"Wrote {len(positives)} ranked findings to {output}")
    print("Fill expert_relevance with an independent value from 0 to 4 before running calculate_ndcg.py.")


if __name__ == "__main__":
    main()
