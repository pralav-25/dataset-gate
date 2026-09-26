"""Bound canonical ISO calendar dates inclusively."""

from datetime import date

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, row_check


def iso_date(value):
    if not isinstance(value, str) or len(value) != 10:
        return False
    try:
        return date.fromisoformat(value).isoformat() == value
    except ValueError:
        return False


def evaluate(data, rule):
    low, high = rule.params["min"], rule.params["max"]
    if low > high:
        raise GateError("date_range min must not exceed max")
    return row_check(
        data,
        rule.column,
        lambda v: iso_date(v) and low <= v <= high,
        message="Date is invalid or outside bounds",
    )


SPEC = Spec(
    "date_range",
    "Bound canonical ISO calendar dates inclusively.",
    evaluate,
    {"min": iso_date, "max": iso_date},
    ("min", "max"),
)
