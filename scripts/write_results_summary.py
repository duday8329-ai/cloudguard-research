"""Create RESULTS.md from the generated CloudGuard metrics artifact."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    data = json.loads((ROOT / "results" / "cloudguard" / "metrics.json").read_text(encoding="utf-8"))
    matrix = data["confusion_matrix"]
    latency_path = ROOT / "results" / "latency" / "metrics.json"
    latency = json.loads(latency_path.read_text(encoding="utf-8")) if latency_path.exists() else None
    latency_section = ""
    if latency:
        latency_section = f"""\n## CloudGuard latency measurement\n\n- Trials: {latency['trials']}\n- Median: {latency['median_ms']:.3f} ms\n- p95: {latency['p95_ms']:.3f} ms\n- Environment: {latency['platform']}\n\nThis is a local prototype measurement on the synthetic benchmark, not a\nproduction performance claim.\n"""
    trivy_path = ROOT / "results" / "baselines" / "trivy" / "findings_unmapped.csv"
    trivy_section = ""
    if trivy_path.exists():
        with trivy_path.open(encoding="utf-8") as handle:
            trivy_count = max(0, sum(1 for _ in handle) - 1)
        trivy_section = f"""\n## Trivy raw baseline\n\n- Version: 0.74.0\n- Raw findings extracted: {trivy_count}\n- Semantic CloudGuard SID mapping: pending validation\n\nThe raw scan is retained for later normalization. It is not included in the\ndetection comparison because unresolved tool semantics cannot be scored as\nCloudGuard policy instances.\n"""
    baseline_path = ROOT / "results" / "baselines" / "summary.json"
    baseline_section = ""
    if baseline_path.exists():
        baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
        checkov = baseline["checkov"]
        kics = baseline["kics"]
        baseline_section = f"""\n## Raw baseline scans\n\n- Checkov {checkov['version']}: {checkov['failed_checks']} failed and {checkov['passed_checks']} passed checks across {checkov['resources']} resources\n- KICS {kics['version']}: {kics['total_findings']} findings across {kics['files_scanned']} files\n\nThese are raw tool findings, not comparable policy-instance metrics. Semantic\nSID mapping remains pending validation.\n"""
    text = f"""# Reproduction Results

## Evidence status

This file is generated from the included 50-manifest project-team synthetic
mutation benchmark. It is **not complete conference evidence** and must not be
substituted for a larger benchmark, independent annotations, baseline
comparisons, ranking, or remediation experiments.

## Included sanity run

- Manifests: 50
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
exercise the same limited rules as the prototype. They are useful as a
reproducible synthetic mutation study, not as a generalization claim about
production AWS IaC. Regenerate with `python scripts/reproduce_all.py`.
{latency_section}
{trivy_section}
{baseline_section}
## Not yet measured

No independent annotation agreement, Checkov/KICS/Trivy comparison, NDCG,
remediation success rate, gate validation, ablation, or human-subject study is
reported because the required raw evidence is not present.
"""
    (ROOT / "RESULTS.md").write_text(text, encoding="utf-8")
    print("Wrote RESULTS.md")


if __name__ == "__main__":
    main()
