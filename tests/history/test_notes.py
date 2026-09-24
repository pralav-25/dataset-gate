from dataset_gate.history.notes import get_note, set_note
from dataset_gate.history.save import save_run
from dataset_gate.history.store import Store


def test_review_notes(tmp_path):
    store = Store(tmp_path / "runs.db")
    save_run(
        store,
        {
            "run_id": "x",
            "created_at": "now",
            "contract": "A",
            "status": "passed",
            "quality_score": 100,
            "dataset_hash": "d",
            "contract_hash": "c",
        },
    )
    set_note(store, "x", "Investigating missing values")
    set_note(store, "x", "Resolved upstream")
    assert get_note(store, "x") == "Resolved upstream"
