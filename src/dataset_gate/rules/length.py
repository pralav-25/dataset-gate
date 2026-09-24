"""Check inclusive Unicode code-point lengths of nonblank strings."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, nonnegative, row_check


def evaluate(data, rule):
    low, high = rule.params["min"], rule.params["max"]
    if low > high:
        raise GateError("length min must not exceed max")
    return row_check(
        data,
        rule.column,
        lambda value: low <= len(value) <= high,
        message="String length outside bounds",
    )


SPEC = Spec(
    "length",
    "Check inclusive Unicode code-point lengths of nonblank strings.",
    evaluate,
    {"min": nonnegative, "max": nonnegative},
    ("min", "max"),
    column=True,
)
