"""Reusable rule schemas and row evaluators."""

from dataclasses import dataclass
from decimal import Decimal, InvalidOperation

from dataset_gate.errors import GateError
from dataset_gate.results import Finding


@dataclass(frozen=True)
class Spec:
    name: str
    description: str
    evaluate: object
    parameters: dict
    required: tuple = ()
    column: bool = True

    def validate(self, rule):
        if self.column and rule.column is None:
            raise GateError(f"{self.name} requires column")
        if not self.column and rule.column is not None:
            raise GateError(f"{self.name} does not accept column")
        if set(rule.params) - self.parameters.keys():
            raise GateError(f"{self.name}: unknown parameter")
        if set(self.required) - rule.params.keys():
            raise GateError(f"{self.name}: missing parameter")
        for key, value in rule.params.items():
            if not self.parameters[key](value):
                raise GateError(f"{self.name}: invalid {key}")


def number(value):
    try:
        if isinstance(value, bool) or len(str(value)) > 128:
            return None
        result = Decimal(str(value))
        return (
            result if result.is_finite() and (not result or abs(result.adjusted()) <= 100) else None
        )
    except (InvalidOperation, ValueError):
        return None


def nonnegative(value):
    return type(value) is int and value >= 0


def finite(value):
    return type(value) in (int, float) and number(value) is not None


def text(value):
    return isinstance(value, str) and 0 < len(value) <= 200


def names(value):
    return (
        isinstance(value, list)
        and 0 < len(value) <= 200
        and all(text(v) for v in value)
        and len(value) == len(set(value))
    )


def row_check(
    data, column, predicate, *, skip_blank=True, message="Values do not satisfy the rule"
):
    checked = failed = 0
    samples = []
    for record, value in enumerate(data.column(column), 1):
        if skip_blank and not value.strip():
            continue
        checked += 1
        if not predicate(value):
            failed += 1
            if len(samples) < 20:
                samples.append(record)
    return Finding(checked, failed, tuple(samples), message if failed else "Check passed")


def aggregate(passed, message):
    return Finding(1, int(not passed), (), message if not passed else "Check passed")
