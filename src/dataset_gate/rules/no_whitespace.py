"""Reject surrounding whitespace while preserving internal spaces."""

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda value: value == value.strip(),
        skip_blank=False,
        message="Surrounding whitespace found",
    )


SPEC = Spec(
    "no_whitespace",
    "Reject surrounding whitespace while preserving internal spaces.",
    evaluate,
    {},
    (),
    column=True,
)
