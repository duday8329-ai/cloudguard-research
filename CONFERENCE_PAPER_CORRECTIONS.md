# Required Conference-Paper Corrections

## Remove immediately

Remove the unresolved artefact URL `https://github.com/cloudguard-project/cloudguard-core` and every claim that all benchmark files, annotations, mappings, and scripts are available there. A 404 repository cannot support an availability statement.

Remove or mark as **planned evaluation** every unverified numerical claim,
including 120 configurations, 840 policy instances, 318 violations, baseline
F1 values, NDCG values, expert consensus, Cohen's kappa, remediation counts,
latency trials, and participant-study outcomes. Do not create records after the
fact solely to reproduce those claimed numbers.

## Safe replacement text

> CloudGuard is evaluated using a versioned AWS IaC benchmark whose policy-instance ground truth and metric-generation scripts will be released at a persistent repository URL upon publication. At the time of submission, the included project-team sanity benchmark verifies the evaluation pipeline; broader comparative and human-annotation results are reported only after their underlying raw data is available.

## Honest current method statement

> The initial benchmark labels were created by the project team using predefined policy criteria. This is not an independent expert-annotation study; therefore, no inter-rater agreement statistic is reported.

## Before changing this document

Replace the placeholder repository language only after the target GitHub
repository exists, contains the stated artefacts, and has a permanent URL.
