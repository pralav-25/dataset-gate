"""Validate ISO dates or ISO datetimes with explicit timezone offsets."""

from datetime import date, datetime

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    def valid(value):
        try:
            if rule.params["format"] == "date":
                return len(value) == 10 and date.fromisoformat(value).isoformat() == value
            parsed = datetime.fromisoformat(value)
            return parsed.tzinfo is not None and ("T" in value or " " in value)
        except ValueError:
            return False

    return row_check(
        data, rule.column, valid, message="Invalid ISO date or timezone-aware datetime"
    )


SPEC = Spec(
    "date_format",
    "Validate ISO dates or ISO datetimes with explicit timezone offsets.",
    evaluate,
    {"format": lambda value: value in ("date", "datetime")},
    ("format",),
    column=True,
)
