import json

from dataset_gate.cli import main


def test_exit_codes_and_reports(tmp_path, capsys):
    data = tmp_path / "a.csv"
    data.write_text("a\nx\nx")
    contract = tmp_path / "contract.json"
    contract.write_text(
        json.dumps(
            {
                "version": 1,
                "name": "Demo",
                "rules": [{"id": "unique", "check": "unique", "column": "a"}],
            }
        )
    )
    args = ["validate", str(data), "--contract", str(contract)]
    assert main(args) == 1
    assert json.loads(capsys.readouterr().out)["summary"]["errors"] == 1
    data.write_text("a\nx\ny")
    assert main(args) == 0
    capsys.readouterr()
    assert main(args + ["--min-score", "101"]) == 2
