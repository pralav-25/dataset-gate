# Reproduce release verification

From the repository root:

```bash
python -m pip install -e '.[api,dev]'
pytest --cov=dataset_gate --cov-report=term-missing
ruff check .
ruff format --check .
python -m build
python scripts/package_smoke.py dist/dataset_gate-0.1.0-py3-none-any.whl
python scripts/benchmark.py --rows 10000 --repeats 3
```

The clean synthetic batch passes all 20 configured checks. The dirty batch produces
10 failing checks, one warning and nine passing checks; the gate exits 1. The end-to-end
test verifies equivalent CLI/API findings, saved history, named baselines and report exports.

Browser verification covered a rendered HTML report, rule search (2 matching checks for
“resolution”), error filtering (10 checks), warning filtering (one check), and the small-screen
layout. The screenshot in the README was captured from the running local API report.
The HTML uses an inline script hash in its Content Security Policy and has no external assets.

A clean temporary wheel installation exercises the CLI with optional API dependencies absent.
Docker was unavailable locally, so container execution is not part of the verified evidence.
The current dependency set emits an upstream Starlette/httpx deprecation warning in tests;
it does not change test outcomes. Dependencies are pinned to make that behavior reproducible.

The benchmark JSON is an observed local measurement, not a promised throughput target.
Test coverage measures exercised Python statements, not the absence of defects or complete
security coverage.
