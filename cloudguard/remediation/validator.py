from __future__ import annotations

from cloudguard.remediation.engine import repair


PATTERNS = {
    "POL_AWS_S3_PUBLIC": ("public-read", "public-write", "publicread"),
    "POL_AWS_RDS_PUBLIC": ("publicly_accessible = true", "publiclyaccessible: true"),
    "POL_AWS_RDS_ENCRYPTION": ("storage_encrypted = false", "storageencrypted: false"),
    "POL_AWS_SG_UNRESTRICTED": ("0.0.0.0/0",),
    "POL_AWS_IAM_WILDCARD": ('"action": "*"', 'action = "*"'),
}


def scan(source: str) -> set[str]:
    lowered = source.lower().replace("\t", " ")
    return {sid for sid, needles in PATTERNS.items() if any(needle in lowered for needle in needles)}


def repair_and_validate(source: str, policy_sids: list[str], approved_cidr: str | None = None) -> dict:
    before = scan(source)
    current = source
    cases = []
    for sid in policy_sids:
        result = repair(current, sid, approved_cidr)
        current = result.source
        after = scan(current)
        cases.append({"policy_sid": sid, "changed": result.changed, "auto_fixable": result.auto_fixable, "cleared": sid not in after, "message": result.message})
    return {"before": sorted(before), "after": sorted(scan(current)), "source": current, "cases": cases, "structural_check": bool(current.strip())}
