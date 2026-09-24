from dataset_gate.exporters.markdown import render


def test_escaping():
    report = {
        "contract": "<script>|x",
        "status": "failed",
        "row_count": 2,
        "results": [
            {
                "id": "a|b",
                "severity": "error",
                "passed": False,
                "failed": 1,
                "checked": 2,
                "message": "<b>oops</b>\nnext",
            }
        ],
    }
    text = render(report)
    assert "<script>" not in text and "a&#124;b" in text and "&lt;b&gt;" in text
