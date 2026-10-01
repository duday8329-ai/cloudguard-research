# Conference Evidence Matrix

| Claim or artifact | Current status | Evidence location | Can be reported now? |
|---|---|---|---|
| 50 frozen manifests | Complete | `benchmark/benchmark_manifest.csv` | Yes, as synthetic project-team data |
| 70 policy-instance labels | Complete | `annotations/consensus.csv` | Yes, with annotation limitation |
| CloudGuard TP/FP/FN/TN | Complete | `results/cloudguard/metrics.json` | Yes, as sanity evidence |
| Checkov comparison | Pending | `results/baselines/` | No |
| KICS comparison | Pending | `results/baselines/` | No |
| Trivy raw scan | Complete; semantic mapping pending | `results/baselines/trivy/` | Raw scan only |
| Independent expert agreement | Pending | `annotations/expert_1.csv`, `expert_2.csv` | No |
| NDCG@10 | Pending | `experiments/ranking/` | No |
| Remediation clearance and gates | Pending | `experiments/remediation/` | No |
| CloudGuard latency | Complete for prototype | `results/latency/cloudguard.csv` and `metrics.json` | Yes, with machine details |
| Ablation study | Pending | `experiments/ablation/` | No |
| Human developer study | Not conducted | none | No |

The historical claims of 120 configurations, 840 annotations, 318 violations,
κ=0.92, NDCG@10=0.916, and remediation percentages are not supported by this
repository and must remain removed from the conference paper until genuinely
reproduced.
