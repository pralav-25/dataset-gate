from dataset_gate.contracts import Contract
from dataset_gate.data import read_text
from dataset_gate.results import RuleResult, report


def test_report_severity_and_no_values():
    result = RuleResult("x", "unique", "a", "warning", 2, 1, (2,), "duplicate")
    output = report(Contract("test", ()), read_text("a\nsecret\nsecret"), [result])
    assert output["status"] == "warning"
    assert output["summary"] == {"rules": 1, "errors": 0, "warnings": 1, "passed": 0}
    assert "secret" not in str(output)
