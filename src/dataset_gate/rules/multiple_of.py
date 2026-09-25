"""Check exact numeric multiples of a positive divisor."""

from dataset_gate.rules._base import Spec, finite, number, row_check


def evaluate(data, rule):
    divisor = number(rule.params["divisor"])
    numerator, denominator = divisor.as_integer_ratio()

    def valid(raw):
        value = number(raw)
        if value is None:
            return False
        a, b = value.as_integer_ratio()
        return (a * denominator) % (b * numerator) == 0

    return row_check(data, rule.column, valid, message="Invalid number or not an exact multiple")


SPEC = Spec(
    "multiple_of",
    "Check exact numeric multiples of a positive divisor.",
    evaluate,
    {"divisor": lambda v: finite(v) and v > 0},
    ("divisor",),
)
