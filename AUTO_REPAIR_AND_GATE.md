# Automatic repair and deployment gate

CloudGuard now supports a conservative detect -> repair -> re-scan workflow for
known source patterns in Terraform and CloudFormation-oriented inputs.

## Automatic repair boundary

The implementation safely automates only deterministic changes:

- `POL_AWS_S3_PUBLIC`: remove a public ACL and add a public-access block when the
  configured bucket can be identified.
- `POL_AWS_RDS_PUBLIC`: change `publicly_accessible` / `PubliclyAccessible` to
  false.
- `POL_AWS_RDS_ENCRYPTION`: change `storage_encrypted` /
  `StorageEncrypted` to true.

Security-group unrestricted ingress is manual unless an approved CIDR is
provided. IAM wildcard permissions are always manual because least privilege
cannot be inferred from a string replacement. Every repair must be re-scanned;
the repaired source is a new copy and does not overwrite the original.

## Deployment gate

`cloudguard/deployment/gate.py` evaluates normalized findings against a
configurable severity threshold. The command exits with status `1` for `BLOCK`
and `0` for `ALLOW`, so a CI job can stop a deployment before an apply step.
This is a policy gate, not an AWS deployment and not proof that an infrastructure
plan is safe in every environment.

Example:

```text
python scripts/deployment_gate.py findings.json --block-at HIGH
```

## Local verification

```text
python -m unittest discover -s tests -v
python scripts/remediate.py path/to/source.tf --sid POL_AWS_RDS_PUBLIC --output repaired.tf
```

The implementation smoke tests are engineering checks only. They are not new
conference evidence until the experiment protocol is run on the frozen
benchmark and the generated artifacts are retained.
