"""Require nonblank cells to match one of the case-sensitive allowed strings."""

from dataset_gate.rules._base import Spec, names, row_check


def evaluate(data, rule):
    allowed = set(rule.params["values"])
    return row_check(
        data, rule.column, lambda value: value in allowed, message="Unexpected category"
    )


SPEC = Spec(
    "enum",
    "Require nonblank cells to match one of the case-sensitive allowed strings.",
    evaluate,
    {"values": names},
    ("values",),
    column=True,
)
