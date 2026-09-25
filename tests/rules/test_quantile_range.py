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
                    "check": "quantile_range",
                    "column": column,
                    "params": {"q": 0.9, "min": 0, "max": 30} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


@pytest.mark.parametrize("q,expected", [(0, 0), (0.25, 7.5), (0.5, 15), (0.9, 27), (1, 30)])
def test_known_interpolated_quantiles(q, expected):
    result = execute('value\n30\n0\n20\n10\n""', {"q": q, "min": expected, "max": expected})
    assert result["passed"] and result["checked"] == 1
    assert not execute("value\n30\n0\n20\n10", {"q": q, "min": expected + 1, "max": expected + 2})[
        "passed"
    ]


def test_singleton_and_invalid_data():
    assert execute("value\n3", {"q": 0.3, "min": 3, "max": 3})["passed"]
    for csv in ["value\n", 'value\n""', "value\n1\nNaN"]:
        assert execute(csv)["failed"] == 1


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"q": -0.1, "min": 0, "max": 1},
        {"q": 1.1, "min": 0, "max": 1},
        {"q": True, "min": 0, "max": 1},
        {"q": 0.5, "min": 2, "max": 1},
    ],
)
def test_malformed_parameters(params):
    with pytest.raises(GateError):
        execute("value\n1", params)
