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
                    "check": "multiple_of",
                    "column": column,
                    "params": {"divisor": 0.05} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_exact_decimal_divisibility():
    result = execute('value\n0.15\n-0.10\n0\n1e-1\n0.151\nNaN\n""')
    assert (result["checked"], result["failed"], list(result["records"])) == (6, 2, [5, 6])


def test_large_integers_do_not_round():
    assert execute("value\n123456789012345678901234567890", {"divisor": 10})["passed"]
    assert not execute("value\n123456789012345678901234567891", {"divisor": 10})["passed"]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"divisor": 0},
        {"divisor": -1},
        {"divisor": True},
        {"divisor": "0.1"},
        {"divisor": float("inf")},
    ],
)
def test_malformed_divisor(params):
    with pytest.raises(GateError):
        execute("value\n1", params)
