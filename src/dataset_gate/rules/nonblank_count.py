"""Bound the number of populated fields in each record."""

from dataset_gate.errors import GateError
from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, names, nonnegative


def evaluate(data, rule):
    columns = rule.params["columns"]
    low, high = rule.params["min"], rule.params["max"]
    if low > high or high > len(columns):
        raise GateError("nonblank count requires min <= max <= number of columns")
    values = [data.column(column) for column in columns]
    checked = failed = 0
    samples = []
    for record, row in enumerate(zip(*values, strict=True), 1):
        checked += 1
        count = sum(bool(value.strip()) for value in row)
        if not low <= count <= high:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Populated field count is outside bounds" if failed else "Check passed",
    )


SPEC = Spec(
    "nonblank_count",
    "Bound the number of populated fields in each record.",
    evaluate,
    {"columns": names, "min": nonnegative, "max": nonnegative},
    ("columns", "min", "max"),
    column=False,
)
