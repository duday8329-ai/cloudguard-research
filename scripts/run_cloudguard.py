"""Run the current CloudGuard prototype rules on benchmark files.

Rules are evaluated from source text and are intentionally limited to the five
policies listed in mappings/policy_sid_mapping.csv.
"""
from __future__ import annotations

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RULES = {
    "POL_AWS_S3_PUBLIC": re.compile(r"public-read|publicread|public-write|accesscontrol:\s*publicread", re.I),
    "POL_AWS_RDS_PUBLIC": re.compile(r"publicly_accessible\s*=\s*true|publiclyaccessible:\s*true", re.I),
    "POL_AWS_SG_UNRESTRICTED": re.compile(r"0\.0\.0\.0/0", re.I),
    "POL_AWS_IAM_WILDCARD": re.compile(r'"action"\s*:\s*"\*"|action\s*=\s*"\*"', re.I),
    "POL_AWS_RDS_ENCRYPTION": re.compile(r"storage_encrypted\s*=\s*false|storageencrypted:\s*false", re.I),
}


def main() -> None:
    out = ROOT / "results" / "cloudguard" / "predictions.csv"
    out.parent.mkdir(parents=True, exist_ok=True)
    with (ROOT / "benchmark" / "benchmark_manifest.csv").open(newline="", encoding="utf-8") as handle:
        manifest = list(csv.DictReader(handle))
    predictions = []
    for item in manifest:
        text = (ROOT / item["path"]).read_text(encoding="utf-8")
        for sid, pattern in RULES.items():
            if pattern.search(text):
                predictions.append({"file_id": item["file_id"], "policy_sid": sid, "violation": 1, "analyzer": "cloudguard"})
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_id", "policy_sid", "violation", "analyzer"])
        writer.writeheader()
        writer.writerows(predictions)
    print(f"Wrote {len(predictions)} CloudGuard predictions to {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
