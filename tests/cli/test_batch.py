import json

from dataset_gate.cli import main


def test_mixed_batch_and_missing_files(tmp_path, capsys):
    args = [
        "batch",
        "examples/tickets.clean.csv",
        "examples/tickets.dirty.csv",
        "--contract",
        "examples/tickets.contract.json",
    ]
    assert main(args) == 1
    result = json.loads(capsys.readouterr().out)
    assert result["results"][0]["gate_passed"] and not result["results"][1]["gate_passed"]
    args.insert(1, str(tmp_path / "missing.csv"))
    assert main(args) == 2
    result = json.loads(capsys.readouterr().out)
    assert len(result["results"]) == 3 and "input_error" in result["results"][0]
