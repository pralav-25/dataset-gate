"""Compare a target against a decimal sum with a nonnegative absolute tolerance."""

from decimal import localcontext

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, finite, names, number


def evaluate(data, rule):
    target = data.column(rule.column)
    sources = [data.column(name) for name in rule.params["columns"]]
    tolerance = number(rule.params.get("tolerance", 0))
    checked = failed = 0
    samples = []
    for record, row in enumerate(zip(target, *sources, strict=True), 1):
        if any(not value.strip() for value in row):
            continue
        checked += 1
        values = [number(value) for value in row]
        with localcontext() as context:
            context.prec = 256
            valid = (
                all(value is not None for value in values)
                and abs(values[0] - sum(values[1:])) <= tolerance
            )
        if not valid:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Target differs from component sum" if failed else "Check passed",
    )


SPEC = Spec(
    "sum_equals",
    "Compare a target against a decimal sum with a nonnegative absolute tolerance.",
    evaluate,
    {"columns": names, "tolerance": lambda value: finite(value) and value >= 0},
    ("columns",),
    column=True,
)
