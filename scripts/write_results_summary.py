"""Create RESULTS.md from the generated CloudGuard metrics artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "cloudguard" / "metrics.json").read_text(encoding="utf-8"))
    matrix = data["confusion_matrix"]
    text = f"""# Reproduction Results

## Evidence status

This file is generated from the included 12-manifest project-team sanity
benchmark. It is **not conference evidence** and must not be substituted for a
larger benchmark, independent annotations, baseline comparisons, ranking,
remediation, or latency experiments.

## Included sanity run

- Manifests: 12
- Labelled policy instances: {data['labelled_policy_instances']}
- Annotation source: project team using predefined policy criteria
- Analyzer: CloudGuard prototype rules only

## Detection sanity check

- TP: {matrix['tp']}
- FP: {matrix['fp']}
- FN: {matrix['fn']}
- TN: {matrix['tn']}
- Precision: {data['precision']:.4f}
- Recall: {data['recall']:.4f}
- F1: {data['f1']:.4f}

These values are expected to be optimistic because the cases were created to
exercise the same limited rules as the prototype. They are useful as a pipeline
check only. Regenerate with `python scripts/reproduce_all.py`.
"""
    (ROOT / "RESULTS.md").write_text(text, encoding="utf-8")
    print("Wrote RESULTS.md")


if __name__ == "__main__":
    main()
