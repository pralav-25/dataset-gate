"""Require valid JSON in nonblank cells and reject nonfinite numeric literals."""

import json

from dataset_gate.rules._base import Spec, row_check


def valid(value):
    def constant(token):
        raise ValueError("nonfinite JSON")

    try:
        json.loads(value, parse_constant=constant)
        return True
    except (ValueError, RecursionError):
        return False


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Malformed JSON cell")


SPEC = Spec(
    "json",
    "Require valid JSON in nonblank cells and reject nonfinite numeric literals.",
    evaluate,
    {},
    (),
    column=True,
)
