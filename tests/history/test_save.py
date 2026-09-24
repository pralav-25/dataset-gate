import pytest

from dataset_gate.errors import GateError
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_immutable_history(tmp_path):
    store = Store(tmp_path / "runs.db")
    report = {
        "run_id": "x",
        "created_at": "now",
        "contract": "name",
        "status": "passed",
        "quality_score": 100,
        "dataset_hash": "d",
        "contract_hash": "c",
        "results": [],
    }
    assert save_run(store, report) == "x"
    with pytest.raises(GateError):
        save_run(store, {**report, "status": "failed"})
    with store.connect() as connection:
        assert connection.execute("SELECT status FROM runs").fetchone()[0] == "passed"
