"""Bound the number of distinct nonblank strings without trimming them."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import Spec, aggregate, nonnegative


def evaluate(data, rule):
    low, high = rule.params["min"], rule.params["max"]
    if low > high:
        raise GateError("distinct_count min must not exceed max")
    count = len({value for value in data.column(rule.column) if value.strip()})
    return aggregate(low <= count <= high, f"Distinct count {count} is outside bounds")


SPEC = Spec(
    "distinct_count",
    "Bound the number of distinct nonblank strings without trimming them.",
    evaluate,
    {"min": nonnegative, "max": nonnegative},
    ("min", "max"),
)
