# CloudGuard Project Explanation for Supervisor

## 1. Project Title

**CloudGuard: An Automated AWS Infrastructure-as-Code Analyzer for Policy Violation Detection, Explainable Risk Assessment, and Remediation Guidance**

## 2. One-Minute Explanation

CloudGuard is a browser-based security analyzer for Terraform and CloudFormation files that define AWS resources. A user uploads an IaC file, and CloudGuard checks five implemented security conditions: public S3 access, public RDS access, unrestricted security-group ingress, wildcard IAM actions, and disabled RDS encryption. Each finding is linked to a stable policy ID, severity, source evidence, control reference, heuristic score deduction, and remediation guidance.

The system does not deploy to AWS. It performs local analysis, can create controlled repair previews for limited safe patterns, re-scans a repaired copy, and returns a configurable local `ALLOW` or `BLOCK` decision.

## 3. Problem Being Addressed

Infrastructure as Code makes cloud deployment repeatable, but the same repeatability can spread insecure settings across environments. Existing scanners can report many findings, but their rule identifiers, severity labels, and remediation messages differ. A developer may therefore see a warning without a clear connection to the affected resource, the policy condition, the reason for its priority, or the next action.

CloudGuard focuses on making a small, inspectable set of AWS IaC findings traceable from source code to policy ID, evidence, score, guidance, and review decision.

## 4. Scope

CloudGuard currently supports:

- AWS Terraform files: `.tf`
- AWS CloudFormation files: `.yaml`, `.yml`, and `.json`
- Five deterministic policy conditions
- Local browser analysis without AWS credentials
- Heuristic risk prioritization
- Controlled repair previews and manual remediation guidance
- Re-scanning of a repaired copy
- Local `ALLOW`/`BLOCK` policy gating

The current implementation does not support Helm or Kubernetes, does not deploy resources to AWS, does not claim complete Terraform or CloudFormation semantic analysis, and is not a general automatic AST-repair system.

## 5. Implemented Policies

| Policy SID | Condition | Severity | Score deduction |
|---|---|---:|---:|
| `POL_AWS_S3_PUBLIC` | Public S3 access or public-read ACL | Critical | 28 |
| `POL_AWS_RDS_PUBLIC` | `publicly_accessible = true` | Critical | 25 |
| `POL_AWS_SG_UNRESTRICTED` | Ingress contains `0.0.0.0/0` | High | 18 |
| `POL_AWS_IAM_WILDCARD` | IAM action is `*` | High | 18 |
| `POL_AWS_RDS_ENCRYPTION` | Required database encryption is disabled | High | 14 |

The deductions are CloudGuard-defined heuristic weights. They provide transparent relative prioritization; they are not official AWS values, probabilities of compromise, expected loss, or compliance percentages.

## 6. How Detection Works

Each policy is implemented as a predicate over a source property. Examples:

- `acl = "public-read"` satisfies the public-S3 violation predicate.
- `publicly_accessible = true` satisfies the public-RDS violation predicate.
- `cidr_blocks = ["0.0.0.0/0"]` satisfies the unrestricted-ingress predicate.
- `action = "*"` satisfies the wildcard-IAM predicate.
- `storage_encrypted = false` satisfies the disabled-encryption predicate.

A safe value receives a non-violation label. Missing or ambiguous values are not silently converted into violations. The current browser rule matcher emits at most one finding for a given policy SID per file.

## 7. Risk-Score Formula

For the findings emitted for one file, CloudGuard calculates:

```text
S = max(0, 100 - sum of applicable heuristic deductions)
```

For example, if a file has public RDS access and disabled encryption:

```text
S = max(0, 100 - 25 - 14)
S = 61
```

The score helps order attention. It is not a calibrated probability or a guarantee that a resource will be compromised.

## 8. Architecture and Workflow

```text
Upload Terraform/CloudFormation file
                |
                v
      Apply five policy predicates
                |
                v
 Create SID, severity, evidence, and score records
                |
                v
  Show repair preview or manual guidance
                |
                v
       Re-scan a separate copy
                |
                v
       Return local ALLOW or BLOCK
```

These are logical responsibilities inside one browser prototype, not independently deployed services.

## 9. Complete Example: `tf_006`

The accompanying file `CloudGuard_Example_tf006.tf` contains a publicly accessible RDS instance with encryption enabled.

Important source lines:

```hcl
publicly_accessible = true
storage_encrypted   = true
```

Expected policy-instance labels:

| File | Resource | Policy SID | Source condition | Expected violation |
|---|---|---|---|---:|
| `tf_006` | `aws_db_instance.demo` | `POL_AWS_RDS_PUBLIC` | `publicly_accessible = true` | 1 |
| `tf_006` | `aws_db_instance.demo` | `POL_AWS_RDS_ENCRYPTION` | `storage_encrypted = true` | 0 |

The first row is a true policy violation. The second row is a non-violation because encryption is enabled.

## 10. Example Scanner Interpretation

The same example can be scanned by CloudGuard, Checkov, KICS, and Trivy. Their native rule IDs are not automatically treated as equivalent. A finding is mapped to a CloudGuard SID only when the documented condition matches the CloudGuard predicate.

For the example:

| Policy SID | Ground truth | CloudGuard | Checkov | KICS | Trivy |
|---|---:|---:|---:|---:|---:|
| `POL_AWS_RDS_PUBLIC` | 1 | 1 | 1 when validated mapping exists | 1 when validated mapping exists | 1 when validated mapping exists |
| `POL_AWS_RDS_ENCRYPTION` | 0 | 0 | 0 when validated mapping exists | 0 when validated mapping exists | 0 when validated mapping exists |

An unmapped scanner rule is excluded from mapped precision, recall, and F1. It contributes to the coverage limitation instead of being counted as a true negative.

## 11. Benchmark and Evidence

The current reproducibility package contains:

- 50 synthetic manifests.
- 25 Terraform and 25 CloudFormation files.
- 70 policy-instance labels.
- 70 rows in the retained consensus file.
- No repeated file--policy-SID pair in the current benchmark.
- Raw and normalized scanner evidence.
- Generated confusion matrices and summary tables.
- Ten local latency trials.
- Controlled remediation records.

The benchmark is an implementation sanity and regression benchmark. It is not a production benchmark and does not prove general AWS IaC accuracy.

## 12. Metrics

For each policy instance:

```text
Precision = TP / (TP + FP)
Recall    = TP / (TP + FN)
F1        = 2 * Precision * Recall / (Precision + Recall)
Coverage  = mapped policy instances / all labelled policy instances
```

Current CloudGuard sanity result:

```text
TP = 30, FP = 0, FN = 0, TN = 40
Precision = 1.0000
Recall    = 1.0000
F1        = 1.0000
```

These values are optimistic because the synthetic cases were constructed around the same five implemented rules.

## 13. Remediation and Gate Explanation

CloudGuard separates safe source-pattern previews from ambiguous access-control changes. For supported patterns, it creates a separate repaired copy, re-scans that copy, and allows the user to download it. For unrestricted network access or wildcard IAM permissions, it provides copyable manual guidance rather than inventing an approved replacement.

The local policy gate checks the configured severity threshold:

- `BLOCK`: at least one finding meets or exceeds the threshold.
- `ALLOW`: no finding meets the threshold.

The gate does not deploy to AWS and does not replace Terraform validation, CloudFormation validation, code review, or organizational approval.

## 14. What to Say About the Results

Recommended wording for a supervisor:

> “CloudGuard successfully reproduced its five implemented policy predicates on a frozen 50-manifest synthetic benchmark. The generated matrix was TP=30, FP=0, FN=0, and TN=40, giving F1=1.0000. Because the benchmark was constructed around the same five rules, this is an implementation sanity result rather than evidence of production accuracy. The cross-tool comparison is coverage-led and uses mapped metrics only where semantic rule mappings were validated.”

## 15. Honest Limitations

- No production configuration benchmark.
- No independent expert annotation study.
- No human usability study.
- No native Terraform or CloudFormation validation logs.
- No general AST-based automatic repair.
- Pattern-based detection can miss variables, modules, intrinsic functions, indirection, or uncommon syntax.
- NDCG is a severity-derived consistency check, not independent ranking evidence.

## 16. Suggested Supervisor Questions and Answers

**Why is the F1 score 1.0000?**  The benchmark is synthetic and designed around the five implemented predicates. The result verifies the implementation and metric pipeline; it is not a claim of production accuracy.

**Why compare coverage with Checkov, KICS, and Trivy?**  Different tools use different rule IDs and semantics. Coverage shows how many policy instances could be compared after a documented semantic mapping.

**Does CloudGuard automatically repair everything?**  No. It provides controlled previews for limited safe patterns and manual guidance for ambiguous access-control changes.

**Does the gate deploy or block AWS directly?**  No. It returns a local `ALLOW` or `BLOCK` decision for review or CI use. It does not call AWS.

**Why is Kubernetes not included?**  The project scope is AWS Terraform and CloudFormation. Helm/Kubernetes is discussed only as related work, not as an implemented feature.

**What is the main contribution?**  A traceable workflow that connects an AWS IaC source condition to a stable policy SID, severity, heuristic score, evidence, remediation guidance, re-scan, and local review decision.
