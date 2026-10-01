# Generated results

Run `python scripts/reproduce_all.py` from the repository root to regenerate
the CloudGuard sanity-benchmark outputs. Trivy raw output is retained under
`results/baselines/trivy/`, but it is not included in comparative metrics until
semantic policy-SID mappings are independently validated. Do not add Checkov,
KICS, ranking, remediation, or independent-annotation result files until the
relevant experiment has really been run and its raw artefacts have been
retained.
