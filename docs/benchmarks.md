# Reproduce performance measurements

Run `python scripts/benchmark.py --rows 10000 --repeats 3` from the repository root.
The script measures ingestion, 20 contract checks, fingerprints, and profiling.
It also reports a separate Python allocation peak using `tracemalloc`.

The workload is deterministic synthetic support-ticket data. It is bounded by
5 MB, 50,000 records, and 200 columns. The application loads each dataset into
memory; it does not claim streaming or distributed execution. Compare runs only
on comparable hardware and Python environments. This harness makes no timing
assertions in tests.
