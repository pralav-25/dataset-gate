import json

from dataset_gate.cli import main


def test_runtime_diagnostics(capsys):
    assert main(["doctor"]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["limits"]["rows"] == 50000 and result["version"] == "0.1.0"
