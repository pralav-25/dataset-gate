"""Require a named column even when there are no data records."""

from dataset_gate.rules._base import Spec, aggregate


def evaluate(data, rule):
    return aggregate(rule.column in data.columns, f"Missing required column: {rule.column}")


SPEC = Spec(
    "required_column",
    "Require a named column even when there are no data records.",
    evaluate,
    {},
    (),
    column=True,
)
