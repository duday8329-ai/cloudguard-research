"""Extract Trivy findings while preserving unresolved policy semantics."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = ROOT / "results" / "baselines" / "trivy" / "raw.json"
    output = ROOT / "results" / "baselines" / "trivy" / "findings_unmapped.csv"
    report = json.loads(source.read_text(encoding="utf-8"))
    rows = []
    for result in report.get("Results", []):
        target = result.get("Target", "")
        for finding in result.get("Misconfigurations", []):
            rows.append({
                "target": target,
                "check_id": finding.get("ID", ""),
                "severity": finding.get("Severity", ""),
                "title": finding.get("Title", ""),
                "status": finding.get("Status", ""),
                "policy_sid": "",
                "mapping_status": "pending_validation",
            })
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]) if rows else ["target", "check_id", "severity", "title", "status", "policy_sid", "mapping_status"])
        writer.writeheader()
        writer.writerows(rows)
    print(f"Extracted {len(rows)} Trivy findings with unresolved semantic mappings.")


if __name__ == "__main__":
    main()
