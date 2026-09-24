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
                    "check": "date_format",
                    "column": column,
                    "params": {"format": "date"} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute("value\n2026-09-24")["passed"]


def test_invalid_values():
    result = execute("value\n2026-02-30")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n2026-09-24", {"typo": 1})


def test_timezone_requirement():
    assert execute("value\n2026-09-24T12:00:00Z", {"format": "datetime"})["passed"]
    assert not execute("value\n2026-09-24T12:00:00", {"format": "datetime"})["passed"]
