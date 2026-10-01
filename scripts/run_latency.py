"""Measure local CloudGuard scan time on the frozen benchmark."""
from __future__ import annotations

import csv
import json
import platform
import statistics
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TRIALS = 10


def main() -> None:
    output_dir = ROOT / "results" / "latency"
    output_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for trial in range(1, TRIALS + 1):
        started = time.perf_counter()
        subprocess.run([sys.executable, str(ROOT / "scripts" / "run_cloudguard.py")], check=True, stdout=subprocess.DEVNULL)
        elapsed_ms = (time.perf_counter() - started) * 1000
        rows.append({"analyzer": "cloudguard", "trial": trial, "elapsed_ms": round(elapsed_ms, 3)})
    values = [row["elapsed_ms"] for row in rows]
    ordered = sorted(values)
    p95 = ordered[max(0, int(len(ordered) * 0.95) - 1)]
    with (output_dir / "cloudguard.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["analyzer", "trial", "elapsed_ms"])
        writer.writeheader()
        writer.writerows(rows)
    metrics = {
        "analyzer": "cloudguard",
        "benchmark_status": "project_team_synthetic_mutation_benchmark_not_conference_evidence",
        "trials": TRIALS,
        "median_ms": round(statistics.median(values), 3),
        "p95_ms": round(p95, 3),
        "python": platform.python_version(),
        "platform": platform.platform(),
    }
    (output_dir / "metrics.json").write_text(json.dumps(metrics, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()
