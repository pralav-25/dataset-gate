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
                    "check": "uuid",
                    "column": column,
                    "params": {} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_valid_invalid_and_blank_counts():
    result = execute(
        'value\n550e8400-e29b-41d4-a716-446655440000\n550E8400-E29B-41D4-A716-446655440000\n00000000-0000-0000-0000-000000000000\n""\ninvalid\n550e8400e29b41d4a716446655440000\n 550e8400-e29b-41d4-a716-446655440000'
    )
    assert (result["checked"], result["failed"], list(result["records"])) == (6, 3, [5, 6, 7])


def test_empty_and_sample_limit():
    assert execute("value\n")["checked"] == 0
    result = execute("value\n" + "bad\n" * 30)
    assert result["failed"] == 30 and list(result["records"]) == list(range(1, 21))


def test_column_required():
    with pytest.raises(GateError):
        execute("value\n1", column=None)
