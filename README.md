# CloudGuard Research Supplement

This repository is the reproducibility companion for the CloudGuard capstone:
an AWS Infrastructure-as-Code analyzer for Terraform and CloudFormation.

Repository URL: https://github.com/duday8329-ai/cloudguard-research

## Evidence status

The included benchmark is a **50-manifest project-team synthetic mutation
benchmark** containing 70 labelled policy-instance pairs. It is a reproducible
engineering evaluation of the current prototype, not a claim of independent
conference evidence. The repository records unavailable experiments explicitly;
it does not invent expert annotation, baseline output, ranking judgments, or
remediation success.

## Reproduce the included sanity run

```text
python scripts/bootstrap_benchmark.py
python scripts/reproduce_all.py
```

This creates the benchmark, labels, CloudGuard predictions, confusion matrix,
package validation report, and measured CloudGuard latency artifact. The
scripts only use the Python standard library.

After running Checkov, KICS, and Trivy, summarize their retained raw reports
with `python scripts/summarize_baselines.py`. The summary intentionally stops
before comparative scoring until semantic policy-SID mappings are validated.
Then run `python scripts/score_baselines.py` to generate normalized predictions
and mapped precision, recall, F1, coverage, and confusion matrices.

## Repository layout

- `benchmark/` contains the versioned Terraform and CloudFormation cases.
- `annotations/` records the annotation protocol and consensus labels.
- `mappings/` maps CloudGuard policy SIDs to comparable concepts.
- `experiments/` describes the conference-study protocol and raw-data schemas.
- `results/` contains generated artefacts and must never be hand-edited.
- `scripts/` regenerates benchmark outputs and metrics.

Read `CONFERENCE_METHODS.md` for the paper-ready methodology and
`EVIDENCE_MATRIX.md` for the exact boundary between measured evidence and
experiments that still require human or external-tool execution.

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
