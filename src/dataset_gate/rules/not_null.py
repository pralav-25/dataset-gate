"""Reject empty and whitespace-only cells; every record is checked."""

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda value: bool(value.strip()),
        skip_blank=False,
        message="Blank values found",
    )


SPEC = Spec(
    "not_null",
    "Reject empty and whitespace-only cells; every record is checked.",
    evaluate,
    {},
    (),
    column=True,
)
