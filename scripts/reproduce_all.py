"""Regenerate all currently available, non-human-subject benchmark outputs."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent


def run(name: str) -> None:
    subprocess.run([sys.executable, str(HERE / name)], check=True)


if __name__ == "__main__":
    run("bootstrap_benchmark.py")
    run("run_cloudguard.py")
    run("calculate_metrics.py")
    run("write_results_summary.py")
    print("Reproduction complete. Results are a 50-manifest synthetic mutation run, not general conference evidence.")
