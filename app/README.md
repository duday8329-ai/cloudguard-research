# CloudGuard

## An Automated Cloud Security Analyzer for Policy Violation Detection, Risk Assessment, and Remediation

CloudGuard is a browser-based AWS Infrastructure as Code prototype. It intentionally supports only:

- Terraform
- AWS CloudFormation

It does not claim Helm or Kubernetes support.

## Features

- Uploads and analyzes local `.tf`, `.yaml`, `.yml`, and `.json` files in the browser
- Includes an editable configuration area and a sample vulnerable AWS configuration
- Detects public S3 bucket access
- Detects publicly accessible RDS instances
- Detects unrestricted SSH ingress
- Detects wildcard IAM actions
- Calculates an explainable 0-100 security score from policy deductions
- Shows rule IDs, severity, source evidence, risk points, and remediation guidance
- Presents a research evaluation plan without inventing precision, recall, F1, or remediation results

## Run Locally

Open `index.html` in a browser, or run the following from this folder. Select a
Terraform or CloudFormation configuration, then choose **Analyze configuration**.

```powershell
python -m http.server 4173 --bind 127.0.0.1
```

Then open `http://127.0.0.1:4173`.

## Research Paper Scope

The accompanying paper studies CloudGuard as an AWS IaC analyzer. The base paper on Helm charts is cited only as related work and methodological inspiration. CloudGuard's proposed contribution is transparent risk assessment and remediation validation across Terraform and CloudFormation configurations.
