"""Infer a conservative draft, never claim that observed data defines business truth."""

from dataset_gate.contracts import parse_contract
from dataset_gate.types import infer_type


def infer_contract(data, *, name="Inferred dataset contract"):
    rules = []
    for position, column in enumerate(data.columns):
        rules.append({"id": f"column-{position}", "check": "required_column", "column": column})
        kind = infer_type(data.column(column))
        if kind != "unknown" and len(rules) < 100:
            rules.append(
                {
                    "id": f"type-{position}",
                    "check": "type",
                    "column": column,
                    "params": {"type": kind},
                }
            )
        if len(rules) >= 100:
            break
    return parse_contract({"version": 1, "name": name, "rules": rules})
