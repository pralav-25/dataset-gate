"""Descriptive numeric changes, not hypothesis tests or model-performance claims."""

from dataset_gate.profilers.numeric import analyze


def compare(before, after):
    result = []
    for name in before.columns:
        if name not in after.columns:
            continue
        a, b = (
            analyze([v for v in data.column(name) if v.strip()])["numeric"]
            for data in (before, after)
        )
        if not a["parsed"] and not b["parsed"]:
            continue
        result.append(
            {
                "column": name,
                "before": a,
                "after": b,
                "mean_delta": b["mean"] - a["mean"] if a["parsed"] and b["parsed"] else None,
            }
        )
    return {"numeric": result}
