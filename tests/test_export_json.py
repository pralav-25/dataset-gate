import json

import pytest

from dataset_gate.errors import GateError
from dataset_gate.exporters import render


def test_json_roundtrip():
    report = {"status": "passed", "label": "🙂"}
    assert json.loads(render(report)) == report
    with pytest.raises(ValueError):
        render({"x": float("nan")})
    with pytest.raises(GateError):
        render(report, "unknown")
