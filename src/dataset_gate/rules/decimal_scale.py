"""Require numeric values representable at a declared decimal scale."""

from dataset_gate.rules._base import Spec, number, row_check


def evaluate(data, rule):
    places = rule.params["places"]

    def valid(raw):
        value = number(raw)
        if value is None:
            return False
        if not value:
            return True
        parts = value.as_tuple()
        digits = list(parts.digits)
        exponent = parts.exponent
        while digits and digits[-1] == 0:
            digits.pop()
            exponent += 1
        return exponent >= -places

    return row_check(data, rule.column, valid, message="Invalid number or excessive decimal scale")


SPEC = Spec(
    "decimal_scale",
    "Require numbers representable at a declared decimal scale.",
    evaluate,
    {"places": lambda v: type(v) is int and 0 <= v <= 18},
    ("places",),
)
