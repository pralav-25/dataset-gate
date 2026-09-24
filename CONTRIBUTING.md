# Contributing

Use Python 3.11 or later. Install `python -m pip install -e '.[api,dev]'`.
Run `pytest`, `ruff check .`, `ruff format --check .`, and `python -m build`.

A rule must document null handling, checked/failed counts, and parameter constraints.
Add valid, invalid, malformed-configuration and boundary cases. Prefer independent
expected results and realistic integration tests over tests that repeat implementation.
Test adapters against the shared application service. Keep external network access out
of the test suite, and never commit real customer data, credentials or history databases.

Generated reports are disposable; source CSV files must never be overwritten. Changes to
contract/report formats require an explicit versioning decision and migration notes.
