"""Issue summaries neutralize leading spreadsheet formula/control prefixes."""

import csv
import io

EXTENSION = "csv"


def safe(value):
    text = str(value)
    return (
        "'" + text
        if text.lstrip().startswith(("=", "+", "-", "@")) or text.startswith(("\t", "\r", "\n"))
        else text
    )


def render(report):
    stream = io.StringIO(newline="")
    writer = csv.writer(stream)
    writer.writerow(
        ["rule", "check", "column", "severity", "passed", "failed", "checked", "records", "message"]
    )
    for result in report["results"]:
        writer.writerow(
            [
                safe(value)
                for value in [
                    result["id"],
                    result["check"],
                    result.get("column") or "",
                    result["severity"],
                    result["passed"],
                    result["failed"],
                    result["checked"],
                    ",".join(map(str, result["records"])),
                    result["message"],
                ]
            ]
        )
    return stream.getvalue()
