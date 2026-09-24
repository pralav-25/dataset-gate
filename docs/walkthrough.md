# Project and interview walkthrough

## A five-minute demonstration

1. Profile the clean ticket dataset and explain the difference between raw strings,
   inferred types, missingness, and numeric summaries.
2. Open the contract. Show why `not_null` and `unique` are separate requirements,
   and why the cross-column sum and date ordering checks catch errors a schema misses.
3. Validate the faulty dataset. Explain one duplicated id, one invalid category,
   the mismatched resolution total, and the conditionally required resolution timestamp.
4. Save both runs, promote the passing run as a baseline, and compare outcomes.
   Point to identical contract hashes and distinct dataset hashes.
5. Open the HTML report and filter failures. Demonstrate the same validation through
   the local API, then show the regression tests covering shared service behavior.

## Resume wording grounded in the implementation

- Built a Python data-quality application with 30 configurable contract checks, a CLI,
  FastAPI endpoints, and SQLite-backed validation history for CSV-based ML workflows.
- Implemented reproducible dataset/contract fingerprints, cross-field validation,
  batch gates, named baselines, and five report export formats with automated tests.
- Benchmarked a synthetic 10,000-row, 20-check workload locally at a median 0.157 seconds;
  documented resource limits, measurement methodology, and deployment limitations.

Use these as project claims after you can run and explain the implementation. They are
not claims of employment, real customers, production adoption, or measured business impact.

## Questions to prepare for

- Why are raw strings preserved? How can leading-zero identifiers be corrupted by coercion?
- Why does a quality failure exit 1, while an invalid contract exits 2?
- How do row checks differ from aggregate checks in scoring and failure counts?
- What do the two content hashes identify, and what makes an execution unique?
- Why does SQLite use transaction-scoped connections and foreign keys for baselines?
- Why are distribution comparisons descriptive rather than statistical conclusions?
- What breaks first beyond the in-memory limits? How would streaming profiles,
  asynchronous workers, object storage and tenant isolation change the design?

## References used for adapter behavior

- [Python CSV documentation](https://docs.python.org/3/library/csv.html)
- [FastAPI testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [FastAPI application lifecycle](https://fastapi.tiangolo.com/advanced/events/)
