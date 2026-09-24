"""Require a literal case-sensitive prefix on nonblank cells."""

from dataset_gate.rules._base import Spec, row_check, text


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda value: value.startswith(rule.params["value"]),
        message="Missing required prefix",
    )


SPEC = Spec(
    "prefix",
    "Require a literal case-sensitive prefix on nonblank cells.",
    evaluate,
    {"value": text},
    ("value",),
    column=True,
)
