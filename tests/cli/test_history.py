import json

from dataset_gate.cli import main


def test_empty_history_and_invalid_page(tmp_path, capsys):
    db = tmp_path / "runs.db"
    assert main(["history", "--db", str(db)]) == 0
    assert json.loads(capsys.readouterr().out)["total"] == 0
    assert main(["history", "--db", str(db), "--limit", "0"]) == 2
