"""Portable offline report; all dataset-derived text is HTML escaped."""

from html import escape

EXTENSION = "html"
STYLE = """
:root{color-scheme:light;--ink:#142235;--muted:#526174;--blue:#1547cf;--line:#dce3ee}
*{box-sizing:border-box}body{margin:0;background:#f3f6fb;color:var(--ink);font:16px/1.55 system-ui,sans-serif}
header{background:#101f39;color:white;padding:24px max(24px,calc((100vw - 1160px)/2));border-bottom:4px solid #40d8bd}
.brand{font-size:14px;letter-spacing:.12em;text-transform:uppercase;color:#9ff1e2}h1{font-size:32px;line-height:1.2;margin:14px 0 8px}
main{max-width:1208px;margin:auto;padding:32px 24px}h2{font-size:22px;margin:32px 0 16px}.subtle{color:var(--muted)}
.metrics{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}.metric{background:white;padding:20px;border:1px solid var(--line);border-radius:10px}
.metric strong{font-size:32px;display:block;line-height:1.2;margin:6px 0}.metric span{font-size:14px;color:var(--muted)}
.table-wrap{overflow:auto;background:white;border:1px solid var(--line);border-radius:10px}table{border-collapse:collapse;width:100%;text-align:left}
th,td{padding:14px 18px;border-bottom:1px solid var(--line);vertical-align:top}th{font-size:14px;background:#edf2fb}td{font-size:14px}
.badge{display:inline-block;padding:3px 9px;border-radius:6px;font-size:13px;font-weight:650;white-space:nowrap}.passed{color:#065c4a;background:#d7f8ee}.failed{color:#991e31;background:#ffe2e7}.warning{color:#795100;background:#fff0c7}
code{font-size:13px;overflow-wrap:anywhere}footer{margin-top:28px;font-size:14px;color:var(--muted)}a{color:var(--blue)}
@media(max-width:700px){.metrics{grid-template-columns:repeat(2,1fr)}h1{font-size:26px}main{padding:24px 16px}}
@media print{header{background:white;color:var(--ink)}body{background:white}.table-wrap{overflow:visible}.metric{break-inside:avoid}}
"""


def render(report):
    def e(value):
        return escape(str(value), quote=True)

    summary = report["summary"]
    rows = []
    for result in report["results"]:
        status = (
            "passed"
            if result["passed"]
            else "failed"
            if result["severity"] == "error"
            else "warning"
        )
        records = ", ".join(map(str, result.get("records", ()))) or "—"
        rows.append(
            f'<tr data-status="{status}"><td><strong>{e(result["id"])}</strong><br><span class="subtle">{e(result["check"])} · {e(result.get("column") or "Dataset")}</span></td><td><span class="badge {status}">{status.title()}</span></td><td>{result["failed"]} / {result["checked"]}</td><td>{e(result["message"])}<br><span class="subtle">Records: {e(records)}</span></td></tr>'
        )
    metrics = "".join(
        f'<div class="metric"><span>{label}</span><strong>{value}</strong></div>'
        for label, value in [
            ("Records checked", report["row_count"]),
            ("Rules passed", summary["passed"]),
            ("Errors", summary["errors"]),
            ("Warnings", summary["warnings"]),
        ]
    )
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(report["contract"])} · Dataset Gate</title><style>{STYLE}</style></head><body>
<header><div class="brand">Dataset Gate / Quality report</div><h1>{e(report["contract"])}</h1><span class="badge {report["status"]}">{e(report["status"]).title()}</span></header>
<main><section class="metrics" aria-label="Run summary">{metrics}</section><h2>Validation results</h2><p class="subtle">Record numbers start after the header. Samples show at most 20 failures per rule; no source cell values are included.</p><!-- FILTERS --><div class="table-wrap"><table><caption class="subtle">{len(report["results"])} contract checks</caption><thead><tr><th scope="col">Rule</th><th scope="col">Result</th><th scope="col">Failed / checked</th><th scope="col">Details</th></tr></thead><tbody>{"".join(rows)}</tbody></table></div><footer>Run <code>{e(report["run_id"])}</code><br>Created {e(report["created_at"])}<br>Generated locally by Dataset Gate. A passing contract only confirms the configured checks.</footer></main><!-- SCRIPTS --></body></html>"""
