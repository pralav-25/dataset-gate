"""Compare pairs of finite numbers; incomplete pairs are skipped."""

import operator

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, number, text


def evaluate(data, rule):
    operation = {
        "lt": operator.lt,
        "le": operator.le,
        "eq": operator.eq,
        "ge": operator.ge,
        "gt": operator.gt,
    }[rule.params["op"]]
    checked = failed = 0
    samples = []
    for record, (a, b) in enumerate(
        zip(data.column(rule.column), data.column(rule.params["other"]), strict=True), 1
    ):
        if not a.strip() or not b.strip():
            continue
        checked += 1
        x, y = number(a), number(b)
        if x is None or y is None or not operation(x, y):
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(
        checked, failed, tuple(samples), "Column comparison failed" if failed else "Check passed"
    )


SPEC = Spec(
    "compare_columns",
    "Compare pairs of finite numbers; incomplete pairs are skipped.",
    evaluate,
    {"other": text, "op": lambda value: value in ("lt", "le", "eq", "ge", "gt")},
    ("other", "op"),
    column=True,
)
