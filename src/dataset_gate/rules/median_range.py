"""Bound the exact median of nonblank numeric cells."""

from fractions import Fraction

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("median min must not exceed max")
    values = [number(v) for v in data.column(rule.column) if v.strip()]
    if not values or any(v is None for v in values):
        return aggregate(False, "Median requires finite numeric values")
    values = sorted(Fraction(v) for v in values)
    middle = len(values) // 2
    median = values[middle] if len(values) % 2 else (values[middle - 1] + values[middle]) / 2
    return aggregate(Fraction(low) <= median <= Fraction(high), "Numeric median is outside bounds")


SPEC = Spec(
    "median_range",
    "Bound the exact median of nonblank numeric cells.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
)
