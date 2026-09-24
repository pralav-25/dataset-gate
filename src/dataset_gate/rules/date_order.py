"""Require a date or timezone-aware timestamp to be no later than another column."""

from datetime import date, datetime

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, text


def parse(value):
    if len(value) == 10:
        return date.fromisoformat(value)
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        raise ValueError("timezone required")
    return parsed


def evaluate(data, rule):
    checked = failed = 0
    samples = []
    for record, (a, b) in enumerate(
        zip(data.column(rule.column), data.column(rule.params["other"]), strict=True), 1
    ):
        if not a.strip() or not b.strip():
            continue
        checked += 1
        try:
            valid = parse(a) <= parse(b)
        except (ValueError, TypeError):
            valid = False
        if not valid:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Date ordering or date syntax is invalid" if failed else "Check passed",
    )


SPEC = Spec(
    "date_order",
    "Require a date or timezone-aware timestamp to be no later than another column.",
    evaluate,
    {"other": text},
    ("other",),
    column=True,
)
