from __future__ import annotations

SEVERITY_ORDER = {"INFO": 0, "LOW": 1, "MEDIUM": 2, "HIGH": 3, "CRITICAL": 4}


def evaluate(findings: list[dict], block_at: str = "HIGH", require_clean_repair: bool = False) -> dict:
    threshold = SEVERITY_ORDER[block_at.upper()]
    blocking = [f for f in findings if SEVERITY_ORDER.get(str(f.get("severity", "INFO")).upper(), 0) >= threshold]
    if require_clean_repair:
        blocking += [f for f in findings if f.get("repair_status") not in {"cleared", "not_applicable"}]
    unique = {(f.get("policy_sid"), f.get("file"), f.get("resource")) for f in blocking}
    return {"decision": "BLOCK" if unique else "ALLOW", "block_at": block_at.upper(), "blocking_count": len(unique), "reasons": blocking}
