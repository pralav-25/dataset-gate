"""Check the mean of finite nonblank numbers; empty or malformed numeric data fails."""

from fractions import Fraction

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number
from dataset_gate.rules._numeric import exact_sum


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("mean min must not exceed max")
    values = [number(value) for value in data.column(rule.column) if value.strip()]
    if not values or any(value is None for value in values):
        return aggregate(False, "Mean requires finite numeric values")
    # Compare the rational mean without rounding a repeating decimal at a bound.
    mean = Fraction(exact_sum(values)) / len(values)
    return aggregate(Fraction(low) <= mean <= Fraction(high), "Numeric mean is outside bounds")


SPEC = Spec(
    "mean_range",
    "Check the mean of finite nonblank numbers; empty or malformed numeric data fails.",
    evaluate,
    {"min": finite, "max": finite},
    ("min", "max"),
    column=True,
)
