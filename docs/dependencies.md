# Dependencies and packaging

The Python core has no runtime dependencies. Install `.[api]` for FastAPI/Uvicorn and
`.[api,dev]` to develop. Optional top-level versions are pinned in pyproject.toml.
`requirements-dev.lock` records the complete resolved development environment used for
this release; reproduce it with `pip install -r requirements-dev.lock` followed by
`pip install -e . --no-deps`. Re-resolve pins deliberately when updating supported Python
versions or responding to dependency advisories.

Run `python -m build`, then `python scripts/package_smoke.py dist/dataset_gate-0.1.0-py3-none-any.whl`.
The smoke script creates a temporary environment, installs the wheel without dependencies,
and validates a sample dataset through the installed CLI. It proves that optional API
imports do not accidentally become core installation requirements.
