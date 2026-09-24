import pytest

from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError
from dataset_gate.rules._base import number, row_check


def test_unknown_rule():
    contract = parse_contract(
        {"version": 1, "name": "test", "rules": [{"id": "x", "check": "unknown"}]}
    )
    with pytest.raises(GateError):
        validate(read_text("a\n1"), contract)


def test_finite_parser_and_bounded_findings():
    assert number("NaN") is None and number("1e999") is None and number(True) is None
    data = read_text("a\n" + ("no\n" * 50))
    result = row_check(data, "a", lambda value: value == "yes")
    assert result.failed == 50 and result.records == tuple(range(1, 21))
