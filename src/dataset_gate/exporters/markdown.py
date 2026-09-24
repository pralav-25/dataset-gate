"""Markdown summaries escape table delimiters and raw HTML."""

import html

EXTENSION = "md"


def cell(value):
    return html.escape(str(value)).replace("|", "&#124;").replace("\n", " ").replace("\r", " ")


def render(report):
    lines = [
        f"# Dataset Gate: {cell(report['contract'])}",
        "",
        f"Status: **{report['status']}** · Records: {report['row_count']}",
        "",
        "| Rule | Severity | Result | Failed / checked | Message |",
        "| --- | --- | --- | --- | --- |",
    ]
    for result in report["results"]:
        lines.append(
            f"| {cell(result['id'])} | {result['severity']} | {'PASS' if result['passed'] else 'FAIL'} | {result['failed']} / {result['checked']} | {cell(result['message'])} |"
        )
    return "\n".join(lines) + "\n"
