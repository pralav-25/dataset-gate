"""Check the mean of finite nonblank numbers; empty or malformed numeric data fails."""

from decimal import localcontext

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("mean min must not exceed max")
    values = [number(value) for value in data.column(rule.column) if value.strip()]
    if not values or any(value is None for value in values):
        return aggregate(False, "Mean requires finite numeric values")
    with localcontext() as context:
        context.prec = 256
        mean = sum(values) / len(values)
    return aggregate(low <= mean <= high, "Numeric mean is outside bounds")


SPEC = Spec(
    "mean_range",
    "Check the mean of finite nonblank numbers; empty or malformed numeric data fails.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
    column=True,
)
