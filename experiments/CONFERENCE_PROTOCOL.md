# Conference Evaluation Protocol

The repository currently ships only a project-team sanity benchmark. The steps
below are required before reporting conference results.

1. Freeze a benchmark revision and record its manifest count, provenance, and
   policy-instance count.
2. Label every policy-instance pair using predeclared policy criteria. If there
   are two independent reviewers, save their original labels and compute
   Cohen's kappa; otherwise state that annotation was by the project team.
3. Run CloudGuard, Checkov, KICS, and Trivy on the identical benchmark with
   tool versions, rule settings, and execution environment saved in a run log.
4. Normalize each tool's raw output to `file_id,resource_id,policy_sid,violation`.
   Do not count unmatched rule semantics as equivalent.
5. Generate precision, recall, F1, false-positive, and false-negative counts
   exclusively from normalized predictions and consensus ground truth.
6. For ranking, collect independently assigned relevance labels, save the
   ordering seed, and calculate NDCG from those labels.
7. For remediation, store the before/after configuration, target policy,
   re-scan result, syntax validation result, and failure reason.
8. Run latency trials with a recorded machine description and report median,
   p95, and sample count.

Do not publish any numeric result until the raw inputs and generation script
exist in the repository.
