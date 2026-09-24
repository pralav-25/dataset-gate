from dataset_gate.history.listing import list_runs
from dataset_gate.history.retention import prune_runs
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_dry_run_then_prune(tmp_path):
    store = Store(tmp_path / "runs.db")
    for i in range(4):
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
    assert prune_runs(store, keep=2)["count"] == 2
    assert list_runs(store)["total"] == 4
    assert prune_runs(store, keep=2, dry_run=False)["count"] == 2
    assert list_runs(store)["total"] == 2
