"""Restrict exact pairs across two columns, including blank values."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, text


def pairs(value):
    return (
        isinstance(value, list)
        and 0 < len(value) <= 200
        and all(
            isinstance(pair, list) and len(pair) == 2 and all(isinstance(v, str) for v in pair)
            for pair in value
        )
    )


def evaluate(data, rule):
    allowed = {tuple(pair) for pair in rule.params["pairs"]}
    failures = [
        i
        for i, pair in enumerate(
            zip(data.column(rule.column), data.column(rule.params["other"]), strict=True), 1
        )
        if pair not in allowed
    ]
    return Finding(
        len(data),
        len(failures),
        tuple(failures[:20]),
        "Disallowed value pair" if failures else "Check passed",
    )


SPEC = Spec(
    "allowed_pairs",
    "Restrict exact pairs across two columns, including blank values.",
    evaluate,
    {"other": text, "pairs": pairs},
    ("other", "pairs"),
    column=True,
)
