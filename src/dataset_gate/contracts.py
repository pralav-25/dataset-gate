"""Strict, bounded version-one contract structure; rule parameters validate at execution."""

import json
import re
from dataclasses import asdict, dataclass

from dataset_gate.errors import GateError


@dataclass(frozen=True)
class Rule:
    id: str
    check: str
    column: str | None
    severity: str
    params: dict


@dataclass(frozen=True)
class Contract:
    name: str
    rules: tuple[Rule, ...]
    version: int = 1

    def to_dict(self):
        return {
            "version": self.version,
            "name": self.name,
            "rules": [asdict(rule) for rule in self.rules],
        }


def parse_contract(value):
    if not isinstance(value, dict) or set(value) - {"version", "name", "rules"}:
        raise GateError("contract must contain only version, name and rules")
    if type(value.get("version")) is not int or value["version"] != 1:
        raise GateError("contract version must be 1")
    name = value.get("name")
    if not isinstance(name, str) or not 1 <= len(name.strip()) <= 120:
        raise GateError("contract name must contain 1..120 characters")
    rules = value.get("rules")
    if not isinstance(rules, list) or not 1 <= len(rules) <= 100:
        raise GateError("contract must have 1..100 rules")
    result, ids = [], set()
    for raw in rules:
        if not isinstance(raw, dict) or set(raw) - {"id", "check", "column", "severity", "params"}:
            raise GateError("rule has unsupported fields")
        rule_id, check = raw.get("id"), raw.get("check")
        if not isinstance(rule_id, str) or not re.fullmatch(
            r"[A-Za-z][A-Za-z0-9_-]{0,63}", rule_id
        ):
            raise GateError("rule id must be a short identifier starting with a letter")
        if rule_id in ids or not isinstance(check, str):
            raise GateError("rule ids must be unique and check must be a string")
        ids.add(rule_id)
        column = raw.get("column")
        if column is not None and (not isinstance(column, str) or not column):
            raise GateError("column must be a nonempty string or null")
        severity, params = raw.get("severity", "error"), raw.get("params", {})
        if severity not in ("error", "warning") or not isinstance(params, dict):
            raise GateError("invalid severity or params")
        result.append(Rule(rule_id, check, column, severity, params.copy()))
    return Contract(name, tuple(result))


def loads_contract(text):
    if len(text.encode("utf-8")) > 100_000:
        raise GateError("contract exceeds 100 KB")

    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise GateError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        return parse_contract(
            json.loads(
                text,
                object_pairs_hook=pairs,
                parse_constant=lambda value: (_ for _ in ()).throw(
                    GateError("nonfinite JSON number")
                ),
            )
        )
    except (ValueError, RecursionError) as exc:
        raise GateError("contract is not valid JSON") from exc
