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
                    "check": "mean_range",
                    "column": column,
                    "params": {"min": 2, "max": 4} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_valid():
    assert execute("value\n2\n4")["passed"]


def test_invalid_values():
    result = execute("value\n8\n10")
    assert not result["passed"]
    assert result["failed"] > 0


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n2\n4", {"typo": 1})


def test_cancellation_preserves_a_small_excess_over_the_mean_bound():
    # Every cell is within the supported numeric domain, including the extra digit.
    small = "3." + "0" * 100 + "1e-100"
    result = execute(f"value\n1e100\n{small}\n-1e100", {"min": 1e-100, "max": 1e-100})
    assert not result["passed"]


def test_cancellation_can_still_match_the_mean_bound():
    assert execute("value\n1e100\n3e-100\n-1e100", {"min": 1e-100, "max": 1e-100})["passed"]
