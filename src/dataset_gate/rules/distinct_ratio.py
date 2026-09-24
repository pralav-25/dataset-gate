"""Bound distinct nonblank values divided by the number of nonblank records."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite


def evaluate(data, rule):
    low, high = rule.params["min"], rule.params["max"]
    if low > high:
        raise GateError("distinct ratio min must not exceed max")
    values = [value for value in data.column(rule.column) if value.strip()]
    ratio = len(set(values)) / len(values) if values else 0
    return aggregate(low <= ratio <= high, f"Distinct ratio {ratio:.4f} is outside bounds")


SPEC = Spec(
    "distinct_ratio",
    "Bound distinct nonblank values divided by the number of nonblank records.",
    evaluate,
    {"min": lambda v: finite(v) and 0 <= v <= 1, "max": lambda v: finite(v) and 0 <= v <= 1},
    ("min", "max"),
    column=True,
)
