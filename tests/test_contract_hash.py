from dataset_gate.contract_hash import contract_fingerprint
from dataset_gate.contracts import parse_contract


def test_defaults_and_key_order():
    a = parse_contract(
        {"version": 1, "name": "x", "rules": [{"id": "r", "check": "unique", "column": "a"}]}
    )
    b = parse_contract(
        {
            "name": "x",
            "rules": [
                {"severity": "error", "column": "a", "check": "unique", "id": "r", "params": {}}
            ],
            "version": 1,
        }
    )
    assert contract_fingerprint(a) == contract_fingerprint(b)
