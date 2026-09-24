from dataset_gate.exporters.html import render


def test_html_is_escaped_and_self_contained():
    report = {
        "contract": "<img src=x onerror=alert(1)>",
        "status": "failed",
        "row_count": 1,
        "summary": {"passed": 0, "errors": 1, "warnings": 0},
        "run_id": "x",
        "created_at": "now",
        "results": [
            {
                "id": "x",
                "check": "not_null",
                "column": "<script>",
                "severity": "error",
                "passed": False,
                "failed": 1,
                "checked": 1,
                "message": "<script>alert(1)</script>",
                "records": [1],
            }
        ],
    }
    output = render(report)
    assert "<script>alert(1)</script>" not in output and "&lt;script&gt;" in output
    assert 'scope="col"' in output and 'name="viewport"' in output
    assert 'src="http' not in output
