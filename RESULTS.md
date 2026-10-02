# Reproduction Results

## Evidence status

This file is generated from the included 50-manifest project-team synthetic
mutation benchmark. It is reproducible prototype evidence, but it is **not a
production generalization study**. The ranking result is a severity-derived
baseline, remediation uses controlled replacements, native IaC validators were
unavailable, and no human-participant study was conducted.

## Included sanity run

- Manifests: 50
- Labelled policy instances: 70
- Annotation source: two reviewer files merged into consensus; synthetic cases
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
production AWS IaC.

## Reviewer-label consistency audit

- Reviewer rows: 70 per reviewer
- Agreements: 70
- Disagreements: 0
- Observed agreement: 1.0000
- Cohen's kappa: 1.0000 (diagnostic only; not reported as independent evidence)
- Reviewer consensus: `annotations/reviewer_consensus.csv`

The two files are retained for auditability, but independent blinded collection
was not documented. Therefore the paper does not report this kappa value as
inter-rater reliability. The benchmark remains a synthetic project-team study.

## Controlled remediation validation

- Cases: 30 positive policy instances
- Controlled replacements generated: 30/30
- Structural Gate 1 passed: 30/30
- CloudGuard re-scan Gate 2 passed: 30/30
- Native Terraform and CloudFormation validators: unavailable in the run environment

These results evaluate controlled rule replacements against the prototype's
five patterns. They measure remediation guidance clearance on the synthetic
benchmark; they do not establish automatic repair capability or production
syntax validation.

## Leave-one-policy-out ablation

The full system produced precision 1.0000, recall 1.0000, and F1 1.0000.
Removing any one of the five policy rules produced precision 1.0000, recall
0.8000, and F1 0.8889, with six false negatives. These results show that each
rule family contributes six positive cases in this balanced synthetic
benchmark. They are controlled component-sensitivity results, not evidence of
production generalization.

## Ranking baseline

- Evaluated findings: 30
- Ranking metric: NDCG@10
- CloudGuard-ranked value: 1.0000
- Label status: severity-derived reviewer baseline

The relevance values follow the predefined severity and risk-point rubric, so
this result is a ranking baseline. It must not be described as independent
expert-consensus NDCG unless relevance was assigned before reviewers saw the
CloudGuard ranking or risk points.

## CloudGuard latency measurement

- Trials: 10
- Median: 66.091 ms
- p95: 84.382 ms
- Environment: Windows-11-10.0.26300-SP0

This is a local prototype measurement on the synthetic benchmark, not a
production performance claim.


## Trivy raw baseline

- Version: 0.74.0
- Raw findings extracted: 199
- Semantic CloudGuard SID mapping: recorded for mapped policies

The raw scan and mapped predictions are retained. CloudFormation and Terraform
IAM wildcard cases are excluded because no validated equivalent Trivy rule was
identified.


## Raw baseline scans

- Checkov 3.3.22: 94 failed and 56 passed checks across 25 resources
- KICS v2.1.20: 342 findings across 50 files

These are raw tool findings; the mapped policy-instance metrics are reported in
the comparison table below. Unmatched rules are excluded.


## Mapped baseline comparison

| Tool | Coverage | Precision | Recall | F1 |
|---|---:|---:|---:|---:|
| checkov | 65/70 | 1.0000 | 1.0000 | 1.0000 |
| kics | 65/70 | 1.0000 | 1.0000 | 1.0000 |
| trivy | 60/70 | 1.0000 | 1.0000 | 1.0000 |

Metrics are computed from normalized findings and the frozen policy-instance labels. Coverage excludes policy/format pairs for which the tool has no validated equivalent rule. These are synthetic mutation benchmark results and are not production generalization evidence.

## Evidence boundary

The repository now contains measured artifacts for reviewer agreement,
severity-derived ranking, controlled remediation clearance, and leave-one-
policy-out ablation. These results are reportable only with the limitations
stated above and in `EVIDENCE_MATRIX.md`.

No human-participant study was conducted. The package does not claim a
developer usability result, independent expert study, automatic repair, or
native Terraform/CloudFormation syntax validation. Historical claims such as
120 manifests, 840 annotations, 318 violations, kappa 0.92, NDCG@10 0.916,
and 96% remediation remain unsupported and are excluded.
