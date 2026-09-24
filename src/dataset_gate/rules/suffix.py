"""Require a literal case-sensitive suffix on nonblank cells."""

from dataset_gate.rules._base import Spec, row_check, text


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda value: value.endswith(rule.params["value"]),
        message="Missing required suffix",
    )


SPEC = Spec(
    "suffix",
    "Require a literal case-sensitive suffix on nonblank cells.",
    evaluate,
    {"value": text},
    ("value",),
    column=True,
)
