"""Require a nonblank target when another column equals a declared string."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, text


def evaluate(data, rule):
    checked = failed = 0
    samples = []
    for record, (value, condition) in enumerate(
        zip(data.column(rule.column), data.column(rule.params["when"]), strict=True), 1
    ):
        if condition != rule.params["equals"]:
            continue
        checked += 1
        if not value.strip():
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Conditionally required value is missing" if failed else "Check passed",
    )


SPEC = Spec(
    "conditional_required",
    "Require a nonblank target when another column equals a declared string.",
    evaluate,
    {"when": text, "equals": lambda value: isinstance(value, str)},
    ("when", "equals"),
    column=True,
)
