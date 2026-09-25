"""Require canonical Unicode lowercase or uppercase text."""

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    transform = str.lower if rule.params["case"] == "lower" else str.upper
    return row_check(
        data,
        rule.column,
        lambda value: value == transform(value),
        message="Text does not use the required case",
    )


SPEC = Spec(
    "string_case",
    "Require canonical Unicode lowercase or uppercase text.",
    evaluate,
    {"case": lambda v: isinstance(v, str) and v in ("lower", "upper")},
    ("case",),
)
