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
                    "check": "pattern",
                    "column": column,
                    "params": {"glob": "T-*"} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute("value\nT-001\nT-xyz")["passed"]


def test_invalid_values():
    result = execute("value\nX-001")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\nT-001\nT-xyz", {"typo": 1})
