"""Normalize mapped baseline findings and calculate policy-instance metrics."""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load_mappings() -> list[dict[str, str]]:
    with (ROOT / "mappings" / "policy_sid_mapping.csv").open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def file_info(path: str) -> tuple[str, str] | None:
    normalized = path.replace("\\", "/")
    match = re.search(r"(?:^|/)(terraform|cloudformation)/(tf|cf)_(\d+)", normalized)
    if not match:
        return None
    return f"{match.group(2)}_{match.group(3)}", match.group(1)


def checkov_predictions(mappings: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    rule_map = {(row["format"], row["rule_id"]): row["policy_sid"] for row in mappings if row["tool"] == "checkov"}
    reports = sorted(path for path in (ROOT / "results/baselines/checkov/raw.json").rglob("*.json") if path.is_file())
    report = json.loads(reports[-1].read_text(encoding="utf-8"))
    predictions = set()
    for section in report:
        for finding in section["results"]["failed_checks"]:
            info = file_info(finding.get("file_path", ""))
            if not info:
                continue
            file_id, fmt = info
            sid = rule_map.get((fmt, finding["check_id"]))
            if sid:
                resource = finding.get("resource", "")
                if fmt == "cloudformation":
                    resource = resource.split(".")[-1]
                predictions.add((file_id, resource, sid))
    return predictions


def kics_predictions(mappings: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    rule_map = {(row["format"], row["rule_id"]): row["policy_sid"] for row in mappings if row["tool"] == "kics"}
    report = json.loads((ROOT / "results/baselines/kics/results.json").read_text(encoding="utf-8"))
    predictions = set()
    for query in report["queries"]:
        sid = rule_map.get((query.get("platform", "").lower(), query["query_id"]))
        if not sid:
            continue
        for finding in query.get("files", []):
            info = file_info(finding.get("file_name", ""))
            if info:
                resource = finding.get("resource_name", "")
                if info[1] == "terraform":
                    resource = f"{finding.get('resource_type', '')}.{resource}"
                predictions.add((info[0], resource, sid))
    return predictions


def trivy_predictions(mappings: list[dict[str, str]]) -> set[tuple[str, str, str]]:
    rule_map = {(row["format"], row["rule_id"]): row["policy_sid"] for row in mappings if row["tool"] == "trivy"}
    report = json.loads((ROOT / "results/baselines/trivy/raw.json").read_text(encoding="utf-8"))
    predictions = set()
    for result in report.get("Results", []):
        info = file_info(result.get("Target", ""))
        if not info:
            continue
        file_id, fmt = info
        for finding in result.get("Misconfigurations", []):
            sid = rule_map.get((fmt, finding.get("ID", "")))
            if sid:
                predictions.add((file_id, "", sid))
    return predictions


def score(tool: str, predictions: set[tuple[str, str, str]], mappings: list[dict[str, str]]) -> dict:
    with (ROOT / "annotations/consensus.csv").open(newline="", encoding="utf-8") as handle:
        truth_rows = list(csv.DictReader(handle))
    supported = {(row["format"], row["policy_sid"]) for row in mappings if row["tool"] == tool}
    covered = [row for row in truth_rows if (row["format"], row["policy_sid"]) in supported]
    matrix = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    for row in covered:
        exact = (row["file_id"], row["resource_id"], row["policy_sid"]) in predictions
        by_file = any(file_id == row["file_id"] and sid == row["policy_sid"] for file_id, _resource, sid in predictions)
        predicted = exact or by_file
        actual = row["expected_violation"] == "1"
        matrix["tp" if predicted and actual else "fp" if predicted else "fn" if actual else "tn"] += 1
    precision = matrix["tp"] / (matrix["tp"] + matrix["fp"]) if matrix["tp"] + matrix["fp"] else 0.0
    recall = matrix["tp"] / (matrix["tp"] + matrix["fn"]) if matrix["tp"] + matrix["fn"] else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "tool": tool,
        "benchmark_status": "project_team_synthetic_mutation_benchmark_not_conference_evidence",
        "covered_policy_instances": len(covered),
        "total_policy_instances": len(truth_rows),
        "coverage": round(len(covered) / len(truth_rows), 4),
        "confusion_matrix": matrix,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "mapping_status": "project_team_semantic_validation_for_frozen_benchmark",
    }


def write_normalized(tool: str, predictions: set[tuple[str, str, str]]) -> None:
    output = ROOT / "results/normalized"
    output.mkdir(parents=True, exist_ok=True)
    with (output / f"{tool}.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file_id", "resource_id", "policy_sid", "violation", "tool"])
        writer.writeheader()
        for file_id, resource_id, sid in sorted(predictions):
            writer.writerow({"file_id": file_id, "resource_id": resource_id, "policy_sid": sid, "violation": 1, "tool": tool})


def main() -> None:
    mappings = load_mappings()
    detectors = {"checkov": checkov_predictions, "kics": kics_predictions, "trivy": trivy_predictions}
    output = ROOT / "results/detection"
    output.mkdir(parents=True, exist_ok=True)
    summary = {}
    for tool, detector in detectors.items():
        predictions = detector(mappings)
        write_normalized(tool, predictions)
        summary[tool] = score(tool, predictions, mappings)
        (output / f"{tool}_metrics.json").write_text(json.dumps(summary[tool], indent=2) + "\n", encoding="utf-8")
    (output / "summary.json").write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
