from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.run import run_validation


def test_reproducibility_and_score():
    contract = parse_contract(
        {"version": 1, "name": "x", "rules": [{"id": "r", "check": "unique", "column": "a"}]}
    )
    first = run_validation(read_text("a\nx\nx"), contract)
    second = run_validation(read_text("a\nx\nx"), contract)
    assert (
        first["dataset_hash"] == second["dataset_hash"]
        and first["contract_hash"] == second["contract_hash"]
    )
    assert first["run_id"] != second["run_id"] and first["quality_score"] == 0
    assert "x" not in first["profile"]["columns"][0].get("values", [])
