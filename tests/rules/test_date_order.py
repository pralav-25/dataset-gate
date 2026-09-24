import pytest

from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError


def execute(csv, params=None, column="value"):
    contract = parse_contract(
        {
            "version": 1,
            "name": "test",
            "rules": [
                {
                    "id": "rule",
                    "check": "date_order",
                    "column": column,
                    "params": {"other": "other"} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute("value,other\n2026-01-01,2026-01-02")["passed"]


def test_invalid_values():
    result = execute("value,other\n2026-01-03,2026-01-02")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value,other\n2026-01-01,2026-01-02", {"typo": 1})
