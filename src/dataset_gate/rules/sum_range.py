"""Bound the exact sum of finite nonblank numeric values."""

from decimal import Decimal, localcontext

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("sum_range min must not exceed max")
    values = [number(value) for value in data.column(rule.column) if value.strip()]
    if any(value is None for value in values):
        return aggregate(False, "Sum requires finite numeric values")
    with localcontext() as context:
        # Covers 128-character numeric cells, adjusted exponents within +/-100,
        # and the application's 50,000-row limit without cancellation loss.
        context.prec = 512
        total = sum(values, Decimal(0))
    return aggregate(low <= total <= high, "Numeric sum is outside bounds")


SPEC = Spec(
    "sum_range",
    "Bound the exact sum of finite nonblank numeric values.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
)
