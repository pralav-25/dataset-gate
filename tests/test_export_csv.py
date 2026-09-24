import csv
import io

from dataset_gate.exporters.csv import render, safe


def test_formula_neutralization():
    assert safe(" =1+1").startswith("'") and safe("@SUM(A1)").startswith("'")
    report = {
        "results": [
            {
                "id": "r",
                "check": "type",
                "column": "=danger",
                "severity": "error",
                "passed": False,
                "failed": 1,
                "checked": 2,
                "records": [2],
                "message": "bad, cell",
            }
        ]
    }
    rows = list(csv.reader(io.StringIO(render(report))))
    assert rows[1][2] == "'=danger" and rows[1][-1] == "bad, cell"
