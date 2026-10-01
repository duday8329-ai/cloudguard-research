"""Summarize retained baseline scans without scoring unresolved semantics."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def first_json(directory: Path) -> Path:
    files = sorted(path for path in directory.rglob("*.json") if path.is_file())
    if not files:
        raise FileNotFoundError(f"No JSON report found in {directory}")
    return files[0]


def main() -> None:
    checkov = json.loads(first_json(ROOT / "results" / "baselines" / "checkov").read_text(encoding="utf-8"))
    checkov_summary = checkov[-1]["summary"] if isinstance(checkov, list) else checkov["summary"]
    kics = json.loads((ROOT / "results" / "baselines" / "kics" / "results.json").read_text(encoding="utf-8"))
    trivy = json.loads((ROOT / "results" / "baselines" / "trivy" / "raw.json").read_text(encoding="utf-8"))
    trivy_findings = sum(len(result.get("Misconfigurations", [])) for result in trivy.get("Results", []))
    result = {
        "status": "raw_baselines_collected_semantic_policy_mapping_pending",
        "checkov": {
            "version": checkov_summary.get("checkov_version"),
            "resources": checkov_summary.get("resource_count"),
            "passed_checks": checkov_summary.get("passed"),
            "failed_checks": checkov_summary.get("failed"),
        },
        "kics": {
            "version": kics.get("kics_version"),
            "files_scanned": kics.get("files_scanned"),
            "total_findings": kics.get("total_counter"),
            "severity_counters": kics.get("severity_counters", {}),
        },
        "trivy": {
            "version": trivy.get("Trivy", {}).get("Version"),
            "raw_findings": trivy_findings,
        },
    }
    output = ROOT / "results" / "baselines" / "summary.json"
    output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
