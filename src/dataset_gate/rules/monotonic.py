"""Check numeric order across nonblank records, with optional strictness."""

from dataset_gate.results import Finding
from dataset_gate.rules._base import Spec, number


def evaluate(data, rule):
    previous = None
    failed = checked = 0
    samples = []
    for record, raw in enumerate(data.column(rule.column), 1):
        if not raw.strip():
            continue
        checked += 1
        value = number(raw)
        valid = value is not None
        if valid and previous is not None:
            delta = value - previous if rule.params["order"] == "increasing" else previous - value
            valid = delta > 0 if rule.params.get("strict", False) else delta >= 0
        if not valid:
            failed += 1
            if len(samples) < 20:
                samples.append(record)
        if value is not None:
            previous = value
    return Finding(
        checked,
        failed,
        tuple(samples),
        "Values are not in the required numeric order" if failed else "Check passed",
    )


SPEC = Spec(
    "monotonic",
    "Check numeric order across nonblank records, with optional strictness.",
    evaluate,
    {
        "order": lambda value: value in ("increasing", "decreasing"),
        "strict": lambda value: type(value) is bool,
    },
    ("order",),
    column=True,
)
