"""Validate hyphenated UUID text without coercion."""

from uuid import UUID

from dataset_gate.rules._base import Spec, row_check


def valid(value):
    try:
        return len(value) == 36 and str(UUID(value)) == value.lower()
    except ValueError:
        return False


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Invalid hyphenated UUID")


SPEC = Spec("uuid", "Validate hyphenated UUID text without coercion.", evaluate, {})
