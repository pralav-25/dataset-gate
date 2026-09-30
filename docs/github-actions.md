# Check CSV data in GitHub Actions

Use Dataset Gate to catch duplicate identifiers, missing fields and out-of-range values
when a dataset changes. The action runs the same validator as the CLI and creates a job
summary plus JSON, offline HTML, Markdown and JUnit reports from a single validation run.

## Add a quality gate

Commit a CSV and a [version-one contract](rules.md) to your repository. Save this workflow
as `.github/workflows/data-quality.yml`, changing the two input paths to match your files:

```yaml
name: Data quality
on: [push, pull_request]
permissions:
  contents: read
jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@fbc6f3992d24b796d5a048ff273f7fcc4a7b6c09 # v5
        with:
          persist-credentials: false
      - name: Validate dataset
        id: gate
        uses: pralav-25/dataset-gate@main
        with:
          dataset: data/tickets.csv
          contract: data/tickets.contract.json
          fail-on-warning: 'false'
      - name: Save quality reports
        if: ${{ always() && steps.gate.outputs.report-directory != '' }}
        uses: actions/upload-artifact@ea165f8d65b6e75b540449e92b4886f43607fa02 # v4
        with:
          name: data-quality-reports
          path: ${{ steps.gate.outputs.report-directory }}
          retention-days: 7
```

`@main` follows ongoing development. For a reproducible workflow, replace it with the
full commit SHA you have reviewed. The action sets up Python 3.12 and runs its bundled,
standard-library-only core; it does not install a package into your project's environment.
Use a separate job if another part of your workflow needs a different Python version.
The integration workflow verifies the action on GitHub-hosted Ubuntu runners.

The report upload runs even when validation fails. Opening a failed job's **Summary**
shows each rule's result. Download its artifact and open `report.html` for an offline
searchable report. No PR comments, tokens, API server or database are required.

## Inputs and outputs

| Input | Required | Meaning |
| --- | --- | --- |
| `dataset` | Yes | CSV, TSV or gzip file; relative paths start at `GITHUB_WORKSPACE`. |
| `contract` | Yes | JSON contract file; relative paths start at `GITHUB_WORKSPACE`. |
| `fail-on-warning` | No | Exactly `'true'` or `'false'`; defaults to `'false'`. |

| Output | Meaning |
| --- | --- |
| `status` | `passed`, `failed`, or `error` for invalid inputs. |
| `report-directory` | Unique runner-temporary directory with `report.json`, `report.html`, `report.md` and `report.xml`. Empty if validation could not produce a report. |

Error-severity failures always fail the action. Warning-only failures pass by default;
set `fail-on-warning: 'true'` to make them fail. The summary shows the **quality gate**
outcome separately from the report's `warning` status. Invalid paths, malformed contracts
and invalid input options fail the action. The underlying exit codes are 0 (pass), 1
(quality failure), and 2 (input/output error).

Reports go into a fresh temporary directory for every invocation. The action leaves the
checked-out CSV and contract unchanged, including when called repeatedly in the same job.
Uploaded reports contain column names, contract names, aggregate statistics, hashes and
failing record indices; use appropriate artifact visibility and retention for your data.
The same [bounded input limits](../README.md#evidence-and-limits) apply as in the CLI.

## Try the maintained example

The repository's [Action integration workflow](../.github/workflows/action-smoke.yml)
runs the supplied clean and deliberately faulty datasets. It checks that clean data passes,
faulty data fails, and both runs retain reports. The faulty step uses `continue-on-error`
only so the demo can verify the expected failure; leave that option off in a real gate.

[Open integration runs and download a report](https://github.com/pralav-25/dataset-gate/actions/workflows/action-smoke.yml).
