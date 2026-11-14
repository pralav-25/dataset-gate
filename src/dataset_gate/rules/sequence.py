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
        # Decimal subtraction obeys the active precision and can round away
        # small gaps between large integer identifiers. Integer arithmetic is exact.
        integer = int(value) if valid else None
        if valid and previous is not None:
            valid = integer - previous == rule.params["step"]
        if not valid:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        if integer is not None:
            previous = integer
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
