# Reproduction Results

## Evidence status

This file is generated from the included 50-manifest project-team synthetic
mutation benchmark. It is **not complete conference evidence** and must not be
substituted for a larger benchmark, independent annotations, baseline
comparisons, ranking, or remediation experiments.

## Included sanity run

- Manifests: 50
- Labelled policy instances: 70
- Annotation source: project team using predefined policy criteria
- Analyzer: CloudGuard prototype rules only

## Detection sanity check

- TP: 30
- FP: 0
- FN: 0
- TN: 40
- Precision: 1.0000
- Recall: 1.0000
- F1: 1.0000

These values are expected to be optimistic because the cases were created to
exercise the same limited rules as the prototype. They are useful as a
reproducible synthetic mutation study, not as a generalization claim about
production AWS IaC. Regenerate with `python scripts/reproduce_all.py`.

## CloudGuard latency measurement

- Trials: 10
- Median: 67.748 ms
- p95: 113.376 ms
- Environment: Windows-11-10.0.26300-SP0

This is a local prototype measurement on the synthetic benchmark, not a
production performance claim.


## Trivy raw baseline

- Version: 0.74.0
- Raw findings extracted: 199
- Semantic CloudGuard SID mapping: pending validation

The raw scan is retained for later normalization. It is not included in the
detection comparison because unresolved tool semantics cannot be scored as
CloudGuard policy instances.

## Not yet measured

No independent annotation agreement, Checkov/KICS/Trivy comparison, NDCG,
remediation success rate, gate validation, ablation, or human-subject study is
reported because the required raw evidence is not present.
