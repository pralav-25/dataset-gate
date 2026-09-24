from concurrent.futures import ThreadPoolExecutor

import pytest

from dataset_gate.cli import main
from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError
from dataset_gate.history.listing import list_runs
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store
from dataset_gate.infer import infer_contract
from dataset_gate.rules._base import finite


def test_huge_numeric_configuration_is_rejected():
    assert not finite(10**1000)
    contract = parse_contract(
        {
            "version": 1,
            "name": "x",
            "rules": [
                {"id": "x", "check": "range", "column": "a", "params": {"min": 0, "max": 10**1000}}
            ],
        }
    )
    with pytest.raises(GateError):
        validate(read_text("a\n1"), contract)


def test_wide_inference_never_silently_truncates():
    data = read_text(",".join("c" + str(i) for i in range(51)))
    with pytest.raises(GateError):
        infer_contract(data)


def test_contract_file_bounds(tmp_path):
    data = tmp_path / "a.csv"
    data.write_text("a\n1")
    contract = tmp_path / "big.json"
    contract.write_bytes(b" " * 100001)
    assert main(["validate", str(data), "--contract", str(contract)]) == 2
    contract.write_bytes(b"\xff")
    assert main(["validate", str(data), "--contract", str(contract)]) == 2


def test_concurrent_history_writes_are_not_lost(tmp_path):
    store = Store(tmp_path / "runs.db")

    def save(i):
        save_run(
            store,
            {
                "run_id": str(i),
                "created_at": "now",
                "contract": "A",
                "status": "passed",
                "quality_score": 100,
                "dataset_hash": "d",
                "contract_hash": "c",
            },
        )

    with ThreadPoolExecutor(max_workers=8) as pool:
        list(pool.map(save, range(40)))
    assert list_runs(store)["total"] == 40


def test_malformed_history_error_is_actionable(tmp_path, capsys):
    db = tmp_path / "invalid.db"
    db.write_text("not a database")
    assert main(["history", "--db", str(db)]) == 2
    assert "history database" in capsys.readouterr().err
