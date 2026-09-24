import pytest

from dataset_gate.errors import GateError
from dataset_gate.history.listing import list_runs
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_order_filter_and_injection(tmp_path):
    store = Store(tmp_path / "runs.db")
    for i in range(4):
        save_run(
            store,
            {
                "run_id": str(i),
                "created_at": "now",
                "contract": "A" if i % 2 else "B",
                "status": "passed",
                "quality_score": 100,
                "dataset_hash": "d",
                "contract_hash": "c",
            },
        )
    assert [r["id"] for r in list_runs(store, limit=2)["items"]] == ["3", "2"]
    assert list_runs(store, contract="A")["total"] == 2
    assert list_runs(store, contract="' OR 1=1 --")["total"] == 0
    with pytest.raises(GateError):
        list_runs(store, limit=0)
