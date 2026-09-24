"""Require an exact number of columns."""

from dataset_gate.rules._base import Spec, aggregate, nonnegative


def evaluate(data, rule):
    return aggregate(
        len(data.columns) == rule.params["count"],
        f"Expected {rule.params['count']} columns, found {len(data.columns)}",
    )


SPEC = Spec(
    "column_count",
    "Require an exact number of columns.",
    evaluate,
    {"count": nonnegative},
    ("count",),
    column=False,
)
