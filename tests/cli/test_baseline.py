import json

from dataset_gate.cli import main


def test_baseline_listing_and_incomplete_selection(tmp_path, capsys):
    args = ["baseline", "--db", str(tmp_path / "runs.db")]
    assert main(args) == 0 and json.loads(capsys.readouterr().out) == []
    assert main(args + ["--name", "main"]) == 2
