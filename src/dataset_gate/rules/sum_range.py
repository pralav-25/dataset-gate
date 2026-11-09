"""Bound the exact sum of finite nonblank numeric values."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number
from dataset_gate.rules._numeric import exact_sum


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("sum_range min must not exceed max")
    values = [number(value) for value in data.column(rule.column) if value.strip()]
    if any(value is None for value in values):
        return aggregate(False, "Sum requires finite numeric values")
    total = exact_sum(values)
    return aggregate(low <= total <= high, "Numeric sum is outside bounds")


SPEC = Spec(
    "sum_range",
    "Bound the exact sum of finite nonblank numeric values.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
)
