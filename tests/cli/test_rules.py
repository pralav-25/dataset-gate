import json

from dataset_gate.cli import main


def test_catalog(capsys):
    assert main(["rules"]) == 0
    catalog = json.loads(capsys.readouterr().out)
    assert len(catalog) == 39 and any(rule["name"] == "sum_equals" for rule in catalog)
