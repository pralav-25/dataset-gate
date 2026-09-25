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
                    "check": "string_case",
                    "column": column,
                    "params": {"case": "lower"} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_unicode_lower_and_uncased_text():
    result = execute('value\ncafé\nstraße\n123\n中文\nABC\nMiXeD\n""')
    assert (result["checked"], result["failed"], list(result["records"])) == (6, 2, [5, 6])


def test_uppercase_expansion():
    result = execute("value\nSTRASSE\nCAFÉ\nstraße\n123", {"case": "upper"})
    assert result["failed"] == 1 and list(result["records"]) == [3]


@pytest.mark.parametrize("params", [{}, {"case": "title"}, {"case": True}, {"case": []}])
def test_malformed_case(params):
    with pytest.raises(GateError):
        execute("value\na", params)
