"""Require every nonblank integer to advance by a declared step in record order."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, number


def evaluate(data, rule):
    previous = None
    checked = failed = 0
    samples = []
    for record, raw in enumerate(data.column(rule.column), 1):
        if not raw.strip():
            continue
        checked += 1
        value = number(raw)
        valid = value is not None and value == value.to_integral_value()
        if valid and previous is not None:
            valid = value - previous == rule.params["step"]
        if not valid:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        if value is not None and value == value.to_integral_value():
            previous = value
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Sequence gap or invalid integer" if failed else "Check passed",
    )


SPEC = Spec(
    "sequence",
    "Require every nonblank integer to advance by a declared step in record order.",
    evaluate,
    {"step": lambda value: type(value) is int and value != 0 and abs(value) <= 10**9},
    ("step",),
    column=True,
)
