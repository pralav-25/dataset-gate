"""Require distinct nonblank values; only later duplicate records fail."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec


def evaluate(data, rule):
    seen, samples = set(), []
    checked = failed = 0
    for record, value in enumerate(data.column(rule.column), 1):
        if not value.strip():
            continue
        checked += 1
        if value in seen:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        seen.add(value)
    return Finding(
        checked, failed, tuple(samples), "Duplicate values found" if failed else "Check passed"
    )


SPEC = Spec(
    "unique",
    "Require distinct nonblank values; only later duplicate records fail.",
    evaluate,
    {},
    (),
    column=True,
)
