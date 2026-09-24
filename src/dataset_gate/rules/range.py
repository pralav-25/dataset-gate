"""Require finite numeric cells inside inclusive lower and upper bounds."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, finite, number, row_check


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("range min must not exceed max")
    return row_check(
        data,
        rule.column,
        lambda value: number(value) is not None and low <= number(value) <= high,
        message="Numeric values outside allowed range",
    )


SPEC = Spec(
    "range",
    "Require finite numeric cells inside inclusive lower and upper bounds.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
    column=True,
)
