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
                    "check": "json",
                    "column": column,
                    "params": {} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute('value\n"{""a"":1}"')["passed"]


def test_invalid_values():
    result = execute("value\n{broken")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute('value\n"{""a"":1}"', {"typo": 1})
