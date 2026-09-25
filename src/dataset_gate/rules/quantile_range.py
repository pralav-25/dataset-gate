"""Bound an exact linearly interpolated sample quantile."""

from fractions import Fraction

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, finite, number


def evaluate(data, rule):
    low, high = number(rule.params["min"]), number(rule.params["max"])
    if low > high:
        raise GateError("quantile min must not exceed max")
    values = [number(v) for v in data.column(rule.column) if v.strip()]
    if not values or any(v is None for v in values):
        return aggregate(False, "Quantile requires finite numeric values")
    values = sorted(Fraction(v) for v in values)
    position = Fraction(number(rule.params["q"])) * (len(values) - 1)
    index = position.numerator // position.denominator
    quantile = values[index]
    if index + 1 < len(values):
        quantile += (position - index) * (values[index + 1] - values[index])
    return aggregate(
        Fraction(low) <= quantile <= Fraction(high), "Numeric quantile is outside bounds"
    )


SPEC = Spec(
    "quantile_range",
    "Bound an exact linearly interpolated sample quantile.",
    evaluate,
    {"q": lambda v: finite(v) and 0 <= v <= 1, "min": finite, "max": finite},
    ("q", "min", "max"),
)
