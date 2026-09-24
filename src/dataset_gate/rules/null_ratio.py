"""Limit the fraction of blank records; an empty dataset has zero missingness."""

from dataset_gate.rules._base import Spec, aggregate, finite


def evaluate(data, rule):
    values = data.column(rule.column)
    ratio = sum(not value.strip() for value in values) / len(values) if values else 0
    return aggregate(ratio <= rule.params["max"], f"Blank ratio {ratio:.4f} exceeds limit")


SPEC = Spec(
    "null_ratio",
    "Limit the fraction of blank records; an empty dataset has zero missingness.",
    evaluate,
    {"max": lambda v: finite(v) and 0 <= v <= 1},
    ("max",),
    column=True,
)
