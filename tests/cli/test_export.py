from dataset_gate.cli import main


def test_unknown_run_has_nonzero_exit(tmp_path):
    assert main(["export", "missing", "--db", str(tmp_path / "runs.db")]) == 2
