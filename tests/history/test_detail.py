import pytest

from dataset_gate.errors import GateError
from dataset_gate.history.detail import get_run
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_retrieve_exact_report(tmp_path):
    store = Store(tmp_path / "runs.db")
    report = {
        "run_id": "x",
        "created_at": "now",
        "contract": "A",
        "status": "passed",
        "quality_score": 100,
        "dataset_hash": "d",
        "contract_hash": "c",
    }
    save_run(store, report)
    assert get_run(store, "x") == report
    with pytest.raises(GateError):
        get_run(store, "missing")
