"""Responsive, self-contained reports with no external assets or cell values."""

import base64
import hashlib
from datetime import datetime
from html import escape
from importlib.resources import files

EXTENSION = "html"
SCRIPT = files("dataset_gate").joinpath("templates/report.js").read_text(encoding="utf-8")
FILTERS = """
<section class="filters" aria-label="Filter checks">
  <label class="search-field" for="rule-search"><span class="sr-only">Find a rule</span>
    <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" aria-hidden="true"><circle cx="10.5" cy="10.5" r="6.5"/><path d="m16 16 4 4"/></svg>
    <input id="rule-search" type="search" placeholder="Search rules, columns, or details…" autocomplete="off">
  </label>
  <label class="select-field" for="result-filter"><span class="sr-only">Show results</span>
    <select id="result-filter"><option value="all">All results</option><option value="failed">Errors</option><option value="warning">Warnings</option><option value="passed">Passed</option></select>
  </label>
</section>
<div class="table-meta"><p id="visible-count" role="status" aria-live="polite"></p><span>Errors first</span></div>
"""
CSP = (
    "default-src 'none'; style-src 'unsafe-inline'; script-src 'sha256-"
    + base64.b64encode(hashlib.sha256(SCRIPT.encode()).digest()).decode()
    + "'; base-uri 'none'; form-action 'none'"
)
STYLE = files("dataset_gate").joinpath("templates/report.css").read_text(encoding="utf-8")


def _status(result):
    return (
        "passed" if result["passed"] else "failed" if result["severity"] == "error" else "warning"
    )


def render(report):
    def e(value):
        return escape(str(value), quote=True)

    summary = report["summary"]
    total = len(report["results"])
    passed = summary["passed"]
    errors = summary["errors"]
    warnings = summary["warnings"]
    score = round(passed / total * 100, 2) if total else 0
    run_status = "failed" if errors else "warning" if warnings else "passed"
    if errors:
        title = (
            f"{errors} check{'s' if errors != 1 else ''} need{'s' if errors == 1 else ''} attention"
        )
        description = '<span class="status-word">Gate failed.</span> Review the errors below.'
        icon = "×"
    elif warnings:
        title = f"{warnings} warning{'s' if warnings != 1 else ''} to review"
        description = '<span class="status-word warning">No blocking errors.</span> Review the warnings below.'
        icon = "!"
    elif total:
        title = "All checks passed"
        description = (
            '<span class="status-word passed">Gate passed.</span> Your data meets this contract.'
        )
        icon = "✓"
    else:
        title = "No checks in this report"
        description = "Add rules to your contract to validate this dataset."
        icon = "–"
    created_at = str(report["created_at"])
    try:
        date = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        display_date = date.strftime("%d %b %Y · %H:%M %Z").strip()
    except ValueError:
        display_date = created_at
    rows = []
    priority = {"failed": 0, "warning": 1, "passed": 2}
    for result in sorted(report["results"], key=lambda r: priority[_status(r)]):
        status = _status(result)
        records = result.get("records", ())
        samples = (
            '<div class="record-samples"><span>Sample records</span>'
            + "".join(f"<code>{e(record)}</code>" for record in records)
            + "</div>"
            if records
            else ""
        )
        label = {"passed": "Passed", "failed": "Error", "warning": "Warning"}[status]
        rows.append(f"""<tr role="row" data-status="{status}">
<td role="cell" class="rule-cell"><strong class="rule-name">{e(result["id"])}</strong><div class="rule-meta"><code>{e(result.get("column") or "Dataset")}</code><span class="rule-type">{e(result["check"])}</span></div></td>
<td role="cell" class="status-cell"><span class="badge {status}">{label}</span></td>
<td role="cell" class="count-cell"><span class="record-total"><strong>{e(result["failed"])}</strong> / {e(result["checked"])}</span><span class="record-label">failed / checked</span></td>
<td role="cell" class="detail-cell"><p class="detail-message">{e(result["message"])}</p>{samples}</td>
</tr>""")
    metrics = "".join(
        f'<div class="metric {kind}"><dt>{label}</dt><dd>{e(value)}</dd></div>'
        for label, value, kind in [
            ("Records checked", report["row_count"], ""),
            ("Total checks", total, ""),
            ("Errors", errors, "error"),
            ("Warnings", warnings, "warn"),
        ]
    )
    bars = "".join(
        f'<span class="score-{kind}" style="flex:{int(value)}"></span>'
        for kind, value in [("pass", passed), ("warning", warnings), ("error", errors)]
        if value
    )
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(report["contract"])} · Dataset Gate</title><meta http-equiv="Content-Security-Policy" content="{e(CSP)}"><style>{STYLE}</style></head>
<body><header class="topbar"><div class="topbar-inner"><div class="brand"><span class="brand-mark" aria-hidden="true"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20V5h6v15M14 20V5h6v15M2 20h20M10 9h4M10 15h4"/></svg></span>Dataset Gate</div><span class="topbar-note">Local validation report</span></div></header>
<main><div class="report-heading"><div><p class="eyebrow">Data quality / Run report</p><h1>{e(report["contract"])}</h1><p class="run-date">Run {e(str(report["run_id"])[:8])}<span> / </span><time datetime="{e(created_at)}">{e(display_date)}</time></p></div><button class="button print-button" id="print-report" type="button" aria-label="Print full report"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 9V3h12v6M6 17H3V9h18v8h-3M6 14h12v7H6zM17 12h1"/></svg><span>Print report</span></button></div>
<section class="summary" aria-label="Run summary"><div class="summary-main"><div class="summary-copy"><h2 class="summary-title"><span class="summary-icon {run_status}" aria-hidden="true">{icon}</span>{title}</h2><p>{description}</p></div><div class="score"><div class="score-line"><strong class="score-value">{score:g}%</strong><span class="score-label">Checks passed</span></div><div class="score-bar" role="img" aria-label="{passed} passed, {warnings} warnings, {errors} errors">{bars}</div></div></div><dl class="metrics">{metrics}</dl></section>
<section class="results" aria-labelledby="results-heading"><div class="section-heading"><h2 id="results-heading">Validation results</h2><span>{total}</span></div>{FILTERS}
<div class="table-wrap"><table id="results-table" role="table"><caption class="sr-only">{total} contract checks, errors first</caption><thead role="rowgroup"><tr role="row"><th role="columnheader" scope="col">Rule / column</th><th role="columnheader" scope="col">Result</th><th role="columnheader" scope="col">Failed / checked</th><th role="columnheader" scope="col">Check details</th></tr></thead><tbody role="rowgroup">{"".join(rows)}</tbody></table></div>
<div class="empty-state" id="empty-state" hidden><h3>No matching checks</h3><p>Try a different search or show all results.</p><button class="button" id="clear-filters" type="button">Clear filters</button></div>
<p class="report-note">Record numbers start after the header. Each rule shows up to 20 failing record indices; source cell values stay private.</p></section>
<footer><p><span class="footer-brand">Dataset Gate</span> · Generated locally<br>A passing contract confirms only the configured checks.</p><p>Run ID<br><code>{e(report["run_id"])}</code></p></footer></main><script>{SCRIPT}</script></body></html>"""
