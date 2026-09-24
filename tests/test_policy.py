import pytest

from dataset_gate.errors import GateError
from dataset_gate.policy import gate_passes


def test_gate_policies():
    report = {"summary": {"errors": 0, "warnings": 1}, "quality_score": 75}
    assert gate_passes(report)
    assert not gate_passes(report, fail_on_warning=True)
    assert not gate_passes(report, min_score=80)
    with pytest.raises(GateError):
        gate_passes(report, min_score=101)
