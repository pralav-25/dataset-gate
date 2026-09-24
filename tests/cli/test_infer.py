import json

from dataset_gate.cli import main


def test_contract_draft(tmp_path, capsys):
    path = tmp_path / "a.csv"
    path.write_text("id\n001")
    assert main(["infer", str(path), "--name", "Example"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["name"] == "Example" and result["rules"][1]["params"]["type"] == "string"
