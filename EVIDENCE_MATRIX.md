# Conference Evidence Matrix

| Claim or artifact | Current status | Evidence location | Can be reported now? |
|---|---|---|---|
| 50 frozen manifests | Complete | `benchmark/benchmark_manifest.csv` | Yes, as synthetic project-team data |
| 70 policy-instance labels | Complete | `annotations/consensus.csv` | Yes, with annotation limitation |
| CloudGuard TP/FP/FN/TN | Complete | `results/cloudguard/metrics.json` | Yes, as sanity evidence |
| Checkov comparison | Complete for 65 mapped instances | `results/detection/checkov_metrics.json` | Yes, synthetic benchmark only |
| KICS comparison | Complete for 65 mapped instances | `results/detection/kics_metrics.json` | Yes, synthetic benchmark only |
| Trivy comparison | Complete for 60 mapped instances | `results/detection/trivy_metrics.json` | Yes, synthetic benchmark only |
| Reviewer-label consistency audit | Complete as an internal diagnostic; not independent annotation evidence | `annotations/expert_1.csv`, `expert_2.csv`, `results/annotations/agreement.json` | No, unless independent blinded collection is documented |
| NDCG@10 severity baseline | Complete | `results/ranking/metrics.json` | Yes, as a derived baseline |
| Remediation clearance and prototype gates | Complete with limitations | `results/remediation/remediation_results.csv` | Yes, as controlled replacement evidence; not automatic repair or native syntax validation |
| CloudGuard latency | Complete for prototype | `results/latency/cloudguard.csv` and `metrics.json` | Yes, with machine details |
| Leave-one-policy-out ablation | Complete with limitations | `results/ablation/summary.csv` | Yes, synthetic component-sensitivity evidence |
| Human developer study | Not conducted | none | No |

The historical claims of 120 configurations, 840 annotations, 318 violations,
κ=0.92, NDCG@10=0.916, and remediation percentages are not supported by this
repository and remain excluded from the conference paper. The current NDCG
value is severity-derived, the reviewer kappa is retained only as an internal
diagnostic because independent blinded collection was not documented, and the
remediation gates are prototype checks.
