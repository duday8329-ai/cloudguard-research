# CloudGuard Research Supplement

This repository is the reproducibility companion for the CloudGuard capstone:
an AWS Infrastructure-as-Code analyzer for Terraform and CloudFormation.

## Evidence status

The included benchmark is a **12-manifest project-team sanity benchmark**. It
contains 16 labelled policy-instance pairs and is useful for verifying that the
data format and metric pipeline work end to end. It is not a replacement for a
conference evaluation. Do not claim that it is independently annotated, that it
contains 120 manifests, or that it supports comparisons with Checkov, KICS, or
Trivy until those activities have actually been completed.

## Reproduce the included sanity run

```text
python scripts/bootstrap_benchmark.py
python scripts/reproduce_all.py
```

This creates the sample manifests, labels, CloudGuard predictions, and a
confusion matrix at `results/cloudguard/metrics.json`. The scripts only use the
Python standard library.

## Repository layout

- `benchmark/` contains the versioned Terraform and CloudFormation cases.
- `annotations/` records the annotation protocol and consensus labels.
- `mappings/` maps CloudGuard policy SIDs to comparable concepts.
- `experiments/` describes the future conference-study protocol.
- `results/` contains generated artefacts and must never be hand-edited.
- `scripts/` regenerates benchmark outputs and metrics.

## Before conference submission

1. Expand the benchmark with real configurations and preserve provenance.
2. Obtain independent annotations or state honestly that the project team did
   the annotation.
3. Install and run each baseline on the same frozen benchmark.
4. Populate the policy mapping with validated semantic equivalences.
5. Replace planned evaluation language in the paper only with generated data.
6. Publish this repository to a real GitHub URL and update the paper link.

The historical `github.com/cloudguard-project/cloudguard-core` URL must not be
used: it does not resolve and should be removed from the paper until a real
repository is published.
