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
                    "check": "decimal_scale",
                    "column": column,
                    "params": {"places": 2} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_exact_scale_and_blank_counts():
    result = execute('value\n1.2300\n1e-2\n-2.00\n0.000000\n1.234\n1e-3\nNaN\n""')
    assert (result["checked"], result["failed"], list(result["records"])) == (7, 3, [5, 6, 7])


def test_precision_is_not_rounded_by_decimal_context():
    result = execute("value\n1234567890123456789012345678.001", {"places": 2})
    assert result["failed"] == 1
    assert execute("value\n1000.000", {"places": 0})["passed"]
    assert execute("value\n1e-18", {"places": 18})["passed"]


@pytest.mark.parametrize(
    "params", [{}, {"places": -1}, {"places": 19}, {"places": True}, {"places": 2.0}]
)
def test_malformed_places(params):
    with pytest.raises(GateError):
        execute("value\n1", params)
