"""Create a ranking relevance packet without CloudGuard rank or risk points."""
from __future__ import annotations

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    source = ROOT / "experiments" / "ranking" / "ranking_packet.csv"
    output = ROOT / "experiments" / "ranking" / "blinded_relevance_packet.csv"
    with source.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.DictReader(handle))
    rows.sort(key=lambda row: row["instance_id"])
    fields = ["instance_id", "file_id", "format", "resource_id", "policy_sid", "severity", "expert_relevance"]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row[field] if field != "expert_relevance" else "" for field in fields})
    print(f"Wrote {len(rows)} blinded ranking rows to {output}")


if __name__ == "__main__":
    main()
