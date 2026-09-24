"""Require unique tuples across multiple columns; tuples containing blanks are included."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, names


def evaluate(data, rule):
    columns = [data.column(name) for name in rule.params["columns"]]
    seen, samples = set(), []
    failed = 0
    for record, values in enumerate(zip(*columns, strict=True), 1):
        if values in seen:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        seen.add(values)
    return Finding(
        len(data), failed, tuple(samples), "Duplicate composite keys" if failed else "Check passed"
    )


SPEC = Spec(
    "composite_unique",
    "Require unique tuples across multiple columns; tuples containing blanks are included.",
    evaluate,
    {"columns": names},
    ("columns",),
    column=False,
)
