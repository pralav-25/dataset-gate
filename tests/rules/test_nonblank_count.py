import pytest

from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError


def execute(csv, params=None, column=None):
    contract = parse_contract(
        {
            "version": 1,
            "name": "test",
            "rules": [
                {
                    "id": "rule",
                    "check": "nonblank_count",
                    "column": column,
                    "params": {"columns": ["a", "b"], "min": 1, "max": 1}
                    if params is None
                    else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_exactly_one_counts_blank_records():
    result = execute("a,b\nx,\n,y\nx,y\n,\n ,z")
    assert (result["checked"], result["failed"], list(result["records"])) == (5, 2, [3, 4])


def test_at_least_one_empty_and_missing_columns():
    assert execute("a,b\nx,y", {"columns": ["a", "b"], "min": 1, "max": 2})["passed"]
    assert execute("a,b\n")["checked"] == 0
    result = execute("a\nx")
    assert result["failed"] == 1 and "Missing column" in result["message"]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"columns": ["a", "a"], "min": 0, "max": 1},
        {"columns": [], "min": 0, "max": 0},
        {"columns": ["a"], "min": 2, "max": 1},
        {"columns": ["a"], "min": 0, "max": 2},
        {"columns": ["a"], "min": True, "max": 1},
    ],
)
def test_malformed_parameters(params):
    with pytest.raises(GateError):
        execute("a\nx", params)


def test_column_is_not_accepted():
    with pytest.raises(GateError):
        execute("a,b\nx,y", column="a")
