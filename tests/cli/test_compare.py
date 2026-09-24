import json

from dataset_gate.cli import main


def test_dataset_comparison(tmp_path, capsys):
    a = tmp_path / "a.csv"
    a.write_text("x\n1")
    b = tmp_path / "b.csv"
    b.write_text("x\n2\n3")
    assert main(["compare", str(a), str(b)]) == 0
    assert json.loads(capsys.readouterr().out)["rows"]["delta"] == 1
