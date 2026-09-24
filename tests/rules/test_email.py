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
                    "check": "email",
                    "column": column,
                    "params": {} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute("value\na+b@example.com")["passed"]


def test_invalid_values():
    result = execute("value\na@@example.com")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\na+b@example.com", {"typo": 1})


@pytest.mark.parametrize(
    "email", ["a..b@example.com", "a@-bad.com", "a@localhost", " a@example.com"]
)
def test_email_boundaries(email):
    assert not execute("value\n" + email)["passed"]
