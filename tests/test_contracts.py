import pytest

from dataset_gate.contracts import loads_contract, parse_contract
from dataset_gate.errors import GateError

VALID = {
    "version": 1,
    "name": "Tickets",
    "rules": [{"id": "id", "check": "unique", "column": "id"}],
}


def test_roundtrip():
    contract = parse_contract(VALID)
    assert parse_contract(contract.to_dict()) == contract
    assert contract.rules[0].severity == "error"


@pytest.mark.parametrize(
    "value",
    [
        {},
        {**VALID, "version": True},
        {**VALID, "rules": []},
        {**VALID, "unknown": 1},
        {**VALID, "rules": VALID["rules"] * 2},
        {**VALID, "name": ""},
    ],
)
def test_invalid(value):
    with pytest.raises(GateError):
        parse_contract(value)


def test_duplicate_json():
    with pytest.raises(GateError):
        loads_contract('{"version":1,"version":1}')
    with pytest.raises(GateError):
        loads_contract("NaN")
