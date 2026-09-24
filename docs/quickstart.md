# Run a complete quality-gate workflow

The examples are synthetic support-ticket records. They contain no real customer data.
The dirty version deliberately introduces duplicates, bad dates, impossible values,
and missing required fields. This is a demonstration of the application, not evidence
about a deployed customer pipeline.

```bash
python -m pip install -e '.[api,dev]'
dataset-gate profile examples/tickets.clean.csv
dataset-gate infer examples/tickets.clean.csv --name 'Draft tickets' -o draft.json
dataset-gate validate examples/tickets.clean.csv --contract examples/tickets.contract.json --save --db reports/history.db -o reports/clean.json
dataset-gate validate examples/tickets.dirty.csv --contract examples/tickets.contract.json --save --db reports/history.db --format html -o reports/dirty.html
# The preceding dirty validation exits 1 intentionally.
dataset-gate compare examples/tickets.clean.csv examples/tickets.dirty.csv -o reports/comparison.json
dataset-gate history --db reports/history.db
dataset-gate serve --db reports/history.db
```

Open the local API documentation at `http://127.0.0.1:8765/docs`. A saved report
can be read at `/api/v1/runs/{run_id}/report`. The HTML file also opens offline.
Use `--force` only to replace an existing report; input aliases remain protected.
An inferred contract is a draft: review the business constraints before enforcement.
