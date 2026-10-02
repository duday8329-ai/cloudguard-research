"""Run controlled remediation guidance checks on the positive benchmark cases."""
from __future__ import annotations

import csv
import re
from pathlib import Path

from run_cloudguard import RULES

ROOT = Path(__file__).resolve().parents[1]

REPLACEMENTS = {
    "POL_AWS_S3_PUBLIC": [
        (re.compile(r"public-read", re.I), "private"),
        (re.compile(r"publicread", re.I), "Private"),
    ],
    "POL_AWS_RDS_PUBLIC": [
        (re.compile(r"(publicly_accessible\s*=\s*)true", re.I), r"\1false"),
        (re.compile(r"(publiclyaccessible:\s*)true", re.I), r"\1false"),
    ],
    "POL_AWS_RDS_ENCRYPTION": [
        (re.compile(r"(storage_encrypted\s*=\s*)false", re.I), r"\1true"),
        (re.compile(r"(storageencrypted:\s*)false", re.I), r"\1true"),
    ],
    "POL_AWS_SG_UNRESTRICTED": [
        (re.compile(r"0\.0\.0\.0/0"), "10.0.0.0/8"),
    ],
    "POL_AWS_IAM_WILDCARD": [
        (re.compile(r'("action"\s*:\s*")\*(")', re.I), r"\1s3:GetObject\2"),
        (re.compile(r"(action\s*=\s*\")\*(\")", re.I), r"\1s3:GetObject\2"),
        (re.compile(r"(Action:\s*[\"']?)\*(?=[\"']?\s*$)", re.I | re.M), r"\1s3:GetObject"),
    ],
}


def structural_check(text: str, extension: str) -> tuple[int, str]:
    if not text.strip() or text.count("{") != text.count("}"):
        return 0, "unbalanced_or_empty_configuration"
    if extension in {".yaml", ".yml"}:
        try:
            import yaml  # type: ignore
            if yaml.safe_load(text) is None:
                return 0, "yaml_parser_returned_empty_document"
            return 1, "yaml_parse_check"
        except ImportError:
            return 1, "yaml_parser_unavailable_lexical_check_only"
        except Exception as error:
            return 0, f"yaml_parse_failed:{type(error).__name__}"
    return 1, "lexical_structure_check_only_native_terraform_validator_unavailable"


def main() -> None:
    with (ROOT / "annotations" / "reviewer_consensus.csv").open(newline="", encoding="utf-8-sig") as handle:
        positives = [row for row in csv.DictReader(handle) if row["expected_violation"] == "1"]
    with (ROOT / "benchmark" / "benchmark_manifest.csv").open(newline="", encoding="utf-8-sig") as handle:
        manifest = {row["file_id"]: row for row in csv.DictReader(handle)}

    before_dir = ROOT / "experiments" / "remediation" / "before"
    after_dir = ROOT / "experiments" / "remediation" / "after"
    before_dir.mkdir(parents=True, exist_ok=True)
    after_dir.mkdir(parents=True, exist_ok=True)
    results = []

    for number, row in enumerate(positives, start=1):
        item = manifest[row["file_id"]]
        source_path = ROOT / item["path"]
        original = source_path.read_text(encoding="utf-8")
        replacements = REPLACEMENTS[row["policy_sid"]]
        updated = original
        for pattern, replacement in replacements:
            updated = pattern.sub(replacement, updated)
        changed = updated != original
        extension = source_path.suffix.lower()
        case_id = f"R{number:03d}_{row['file_id']}_{row['policy_sid']}"
        before_path = before_dir / source_path.name.replace(source_path.stem, case_id)
        after_path = after_dir / source_path.name.replace(source_path.stem, case_id)
        before_path.write_text(original, encoding="utf-8")
        after_path.write_text(updated, encoding="utf-8")
        gate1, gate1_reason = structural_check(updated, extension)
        gate2 = int(changed and not RULES[row["policy_sid"]].search(updated))
        failure = "" if gate1 and gate2 else gate1_reason if not gate1 else "target_policy_still_detected"
        results.append({
            "case_id": case_id,
            "file_id": row["file_id"],
            "format": row["format"],
            "target_sid": row["policy_sid"],
            "remediation_method": "controlled_rule_replacement",
            "remediation_generated": int(changed),
            "gate1": gate1,
            "gate1_reason": gate1_reason,
            "gate2": gate2,
            "failure_reason": failure,
            "before_path": str(before_path.relative_to(ROOT)),
            "after_path": str(after_path.relative_to(ROOT)),
        })

    output = ROOT / "results" / "remediation" / "remediation_results.csv"
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)
    print(f"Wrote {len(results)} remediation cases to {output}")
    print(f"Gate 1 passed: {sum(row['gate1'] for row in results)}/{len(results)}")
    print(f"Gate 2 passed: {sum(row['gate2'] for row in results)}/{len(results)}")
    print("Note: Gate 1 uses structural checks because native Terraform and CloudFormation validators are unavailable.")


if __name__ == "__main__":
    main()
