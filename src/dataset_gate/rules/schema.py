"""Check exact column membership and optionally the declared order."""

from dataset_gate.rules._base import Spec, aggregate, names


def evaluate(data, rule):
    expected = rule.params["columns"]
    passed = (
        list(data.columns) == expected
        if rule.params.get("ordered", False)
        else set(data.columns) == set(expected)
    )
    return aggregate(passed, "Dataset columns differ from the declared schema")


SPEC = Spec(
    "schema",
    "Check exact column membership and optionally the declared order.",
    evaluate,
    {"columns": names, "ordered": lambda value: type(value) is bool},
    ("columns",),
    column=False,
)
