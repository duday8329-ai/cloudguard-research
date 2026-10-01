# Reproduction Results

## Evidence status

This file is generated from the included 12-manifest project-team sanity
benchmark. It is **not conference evidence** and must not be substituted for a
larger benchmark, independent annotations, baseline comparisons, ranking,
remediation, or latency experiments.

## Included sanity run

- Manifests: 12
- Labelled policy instances: 16
- Annotation source: project team using predefined policy criteria
- Analyzer: CloudGuard prototype rules only

## Detection sanity check

- TP: 6
- FP: 0
- FN: 0
- TN: 10
- Precision: 1.0000
- Recall: 1.0000
- F1: 1.0000

These values are expected to be optimistic because the cases were created to
exercise the same limited rules as the prototype. They are useful as a pipeline
check only. Regenerate with `python scripts/reproduce_all.py`.
