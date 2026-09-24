from dataset_gate.cli import main


def test_missing_run(tmp_path, capsys):
    assert main(["show", "missing", "--db", str(tmp_path / "runs.db")]) == 2
    assert "run not found" in capsys.readouterr().err
