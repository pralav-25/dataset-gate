import pytest

from dataset_gate.errors import GateError
from dataset_gate.history.baselines import list_baselines, set_baseline
from dataset_gate.history.retention import prune_runs
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_baselines_protect_retention(tmp_path):
    store = Store(tmp_path / "runs.db")
    for i, status in enumerate(["passed", "failed", "passed"]):
        save_run(
            store,
            {
                "run_id": str(i),
                "created_at": str(i),
                "contract": "A",
                "status": status,
                "quality_score": 100,
                "dataset_hash": "d",
                "contract_hash": "c",
            },
        )
    set_baseline(store, "release", "0")
    assert list_baselines(store) == [{"name": "release", "run_id": "0"}]
    with pytest.raises(GateError):
        set_baseline(store, "release", "2")
    with pytest.raises(GateError):
        set_baseline(store, "bad", "1")
    assert prune_runs(store, keep=1, dry_run=False)["run_ids"] == ["1"]
