"""Measure the complete local application service on deterministic synthetic data."""

import argparse
import json
import platform
import statistics
import time
import tracemalloc
from pathlib import Path

from dataset_gate.contracts import loads_contract
from dataset_gate.data import read_text
from dataset_gate.demo import sample_csv
from dataset_gate.run import run_validation


def benchmark(rows, repeats):
    source = sample_csv(rows)
    contract = loads_contract(Path("examples/tickets.contract.json").read_text())
    times = []
    for _ in range(repeats):
        start = time.perf_counter()
        report = run_validation(read_text(source), contract)
        times.append(time.perf_counter() - start)
        assert report["status"] == "passed"
    tracemalloc.start()
    run_validation(read_text(source), contract)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return {
        "rows": rows,
        "rules": len(contract.rules),
        "repeats": repeats,
        "seconds": times,
        "median_seconds": statistics.median(times),
        "peak_python_bytes": peak,
        "python": platform.python_version(),
        "platform": platform.platform(),
        "method": "Timing excludes source generation and contract loading; peak memory is a separate tracemalloc pass. Local results are not a deployment guarantee.",
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rows", type=int, default=10000)
    parser.add_argument("--repeats", type=int, default=3)
    args = parser.parse_args()
    if not 1 <= args.repeats <= 20:
        parser.error("repeats must be 1..20")
    print(json.dumps(benchmark(args.rows, args.repeats), indent=2))
