"""Validate nonblank lexical types; string accepts any text and number accepts integers."""

from dataset_gate.rules._base import Spec, row_check
from dataset_gate.types import scalar_type


def evaluate(data, rule):
    kind = rule.params["type"]
    return row_check(
        data,
        rule.column,
        lambda value: (
            kind == "string"
            or scalar_type(value) == kind
            or (kind == "number" and scalar_type(value) == "integer")
        ),
        message=f"Expected {kind} values",
    )


SPEC = Spec(
    "type",
    "Validate nonblank lexical types; string accepts any text and number accepts integers.",
    evaluate,
    {"type": lambda value: value in ("string", "integer", "number", "boolean", "date")},
    ("type",),
    column=True,
)
