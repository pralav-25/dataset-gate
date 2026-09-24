import json

from dataset_gate.cli import main


def test_profile_command(tmp_path, capsys):
    data = tmp_path / "a.csv"
    data.write_text("a\n1\n2")
    assert main(["profile", str(data)]) == 0
    assert json.loads(capsys.readouterr().out)["row_count"] == 2
    assert main(["profile", str(data), "-o", str(data), "--force"]) == 2
