"""Require valid JSON cells with a specified top-level JSON type."""

import json
from decimal import Decimal, InvalidOperation

from dataset_gate.rules._base import Spec, row_check

TYPES = {
    "object": dict,
    "array": list,
    "string": str,
    "number": Decimal,
    "boolean": bool,
    "null": type(None),
}


def evaluate(data, rule):
    expected = TYPES[rule.params["type"]]

    def constant(token):
        raise ValueError("nonfinite JSON literal")

    def valid(value):
        try:
            parsed = json.loads(
                value, parse_int=Decimal, parse_float=Decimal, parse_constant=constant
            )
            return type(parsed) is expected
        except (ValueError, RecursionError, InvalidOperation):
            return False

    return row_check(data, rule.column, valid, message="Malformed JSON or incorrect JSON type")


SPEC = Spec(
    "json_type",
    "Require valid JSON cells with a specified top-level JSON type.",
    evaluate,
    {"type": lambda v: isinstance(v, str) and v in TYPES},
    ("type",),
)
