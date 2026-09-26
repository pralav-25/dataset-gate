"""Reject explicitly forbidden nonblank values with exact string matching."""

from dataset_gate.rules._base import Spec, names, row_check


def evaluate(data, rule):
    forbidden = set(rule.params["values"])
    return row_check(
        data, rule.column, lambda v: v not in forbidden, message="Forbidden value found"
    )


SPEC = Spec(
    "not_in",
    "Reject explicitly forbidden nonblank values with exact string matching.",
    evaluate,
    {"values": names},
    ("values",),
)
