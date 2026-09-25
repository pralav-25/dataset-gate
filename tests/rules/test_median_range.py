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
                    "check": "median_range",
                    "column": column,
                    "params": {"min": 2, "max": 4} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_odd_even_and_inclusive_bounds():
    for csv in ["value\n1\n3\n99", "value\n1\n5", "value\n2", 'value\n4\n""']:
        result = execute(csv)
        assert result["passed"] and result["checked"] == 1 and list(result["records"]) == []
    assert not execute("value\n8\n10")["passed"]


@pytest.mark.parametrize("csv", ["value\n", 'value\n""', "value\n1\nNaN", "value\ntext"])
def test_empty_or_malformed_data(csv):
    assert execute(csv)["failed"] == 1


@pytest.mark.parametrize(
    "params", [{}, {"min": 5, "max": 1}, {"min": True, "max": 3}, {"min": 1, "max": float("inf")}]
)
def test_malformed_bounds(params):
    with pytest.raises(GateError):
        execute("value\n1", params)
