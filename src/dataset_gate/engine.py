"""Run all rules after preflight; malformed contracts fail before any data checks."""

from dataset_gate.errors import GateError
from dataset_gate.results import Finding, RuleResult, report
from dataset_gate.rules import catalog


def validate(data, contract):
    available = catalog()
    for rule in contract.rules:
        if rule.check not in available:
            raise GateError(f"unknown check: {rule.check}")
        available[rule.check].validate(rule)
    results = []
    for rule in contract.rules:
        try:
            finding = available[rule.check].evaluate(data, rule)
        except KeyError as exc:
            finding = Finding(1, 1, (), f"Missing column: {exc.args[0]}")
        results.append(
            RuleResult(
                rule.id,
                rule.check,
                rule.column,
                rule.severity,
                finding.checked,
                finding.failed,
                finding.records,
                finding.message,
            )
        )
    return report(contract, data, results)
