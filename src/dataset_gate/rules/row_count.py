"""Require a dataset record count within inclusive bounds."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, nonnegative


def evaluate(data, rule):
    low, high = rule.params["min"], rule.params["max"]
    if low > high:
        raise GateError("row count min must not exceed max")
    return aggregate(low <= len(data) <= high, f"Found {len(data)} records; expected {low}..{high}")


SPEC = Spec(
    "row_count",
    "Require a dataset record count within inclusive bounds.",
    evaluate,
    {"min": nonnegative, "max": nonnegative},
    ("min", "max"),
    column=False,
)
