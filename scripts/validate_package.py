"""Validate the schemas and provenance of the reproducibility package."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def main() -> None:
    manifest = read_csv(ROOT / "benchmark" / "benchmark_manifest.csv")
    labels = read_csv(ROOT / "annotations" / "consensus.csv")
    required_manifest = {"file_id", "format", "path", "provenance", "policy_family"}
    required_labels = {"instance_id", "file_id", "resource_id", "policy_sid", "expected_violation", "severity", "annotation_source"}
    errors = []
    if not manifest or not required_manifest.issubset(manifest[0]):
        errors.append("benchmark manifest schema")
    if not labels or not required_labels.issubset(labels[0]):
        errors.append("consensus schema")
    for row in manifest:
        if not (ROOT / row["path"]).exists():
            errors.append(f"missing file: {row['path']}")
    if any(row["provenance"] != "project_team_synthetic_mutation" for row in manifest):
        errors.append("unexpected benchmark provenance")
    if any(row["annotation_source"] != "project_team_predefined_policy_criteria" for row in labels):
        errors.append("unexpected annotation source")
    result = {
        "valid": not errors,
        "manifest_count": len(manifest),
        "label_count": len(labels),
        "errors": errors,
        "status": "project_team_synthetic_mutation_benchmark_not_conference_evidence",
    }
    output = ROOT / "results" / "package_validation.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
