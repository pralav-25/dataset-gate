"""Require each determinant value to map to only one dependent value."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, text


def evaluate(data, rule):
    mapping, samples = {}, []
    failed = 0
    for record, (key, value) in enumerate(
        zip(data.column(rule.column), data.column(rule.params["dependent"]), strict=True), 1
    ):
        if key in mapping and mapping[key] != value:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        else:
            mapping[key] = value
    return Finding(
        len(data),
        failed,
        tuple(samples),
        "Inconsistent dependent value for a determinant" if failed else "Check passed",
    )


SPEC = Spec(
    "functional_dependency",
    "Require each determinant value to map to only one dependent value.",
    evaluate,
    {"dependent": text},
    ("dependent",),
    column=True,
)
