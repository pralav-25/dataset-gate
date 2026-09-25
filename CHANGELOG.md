# Changelog

## 0.2.0

- Add eight opt-in checks for UUIDs, IP addresses, decimal scale, exact multiples,
  median and quantile bounds, Unicode case, and populated field counts.
- Retain contract version 1 and existing report formats; old contracts are unchanged.
- Add core and HTTP regression coverage for every new check.

## 0.1.0

First complete local application release.

- Bounded CSV, TSV and gzip ingestion with conservative profiling and inference.
- Versioned contracts with 30 configurable scalar, aggregate and cross-column checks.
- Reproducible reports, descriptive dataset comparisons and configurable CI gate policy.
- SQLite history, review notes, passing baselines, saved-run diffs and protected retention.
- Fourteen CLI commands and an optional versioned FastAPI adapter with OpenAPI docs.
- Five export formats, including searchable offline HTML and CI-friendly JUnit XML.
- Synthetic clean/faulty demonstrations, reproducible benchmark harness and wheel smoke test.
- Automated tests and GitHub Actions configuration for Python 3.11–3.13.

This release is designed for local, single-user operation. Container definitions are
provided but require execution on a Docker-enabled host before deployment reliance.
