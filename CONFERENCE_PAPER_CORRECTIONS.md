# Required Conference-Paper Corrections

## Remove immediately

Remove the unresolved artefact URL `https://github.com/cloudguard-project/cloudguard-core` and every claim that all benchmark files, annotations, mappings, and scripts are available there. A 404 repository cannot support an availability statement.

Remove or mark as **planned evaluation** every unverified numerical claim,
including 120 configurations, 840 policy instances, 318 violations, baseline
F1 values, NDCG values, expert consensus, Cohen's kappa, remediation counts,
latency trials, and participant-study outcomes. Do not create records after the
fact solely to reproduce those claimed numbers.

## Safe replacement text

> The CloudGuard reproducibility companion is available at https://github.com/duday8329-ai/cloudguard-research. It currently provides a versioned 50-manifest project-team synthetic mutation benchmark, policy-instance ground truth, a CloudGuard confusion matrix, a local latency measurement, and a retained raw Trivy scan with unresolved semantic mappings. Broader comparative, ranking, remediation, and independent human-annotation results are reported only after their underlying raw data is available.

## Honest current method statement

> The initial benchmark labels were created by the project team using predefined policy criteria. This is not an independent expert-annotation study; therefore, no inter-rater agreement statistic is reported.

## Before changing this document

Before submitting, verify that this repository URL remains public and that the
paper describes exactly the artefacts and evidence it contains at submission.
