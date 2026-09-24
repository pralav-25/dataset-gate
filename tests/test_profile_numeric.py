import pytest

from dataset_gate.profilers.numeric import analyze


def test_summary():
    stats = analyze(["1", "2", "3", "4", "NaN", "bad"])["numeric"]
    assert stats["mean"] == stats["median"] == 2.5
    assert stats["p25"] == 1.75 and stats["p75"] == 3.25
    assert stats["stddev"] == pytest.approx(1.11803398875)
    assert stats["invalid"] == 2
    assert analyze([])["numeric"] == {"parsed": 0, "invalid": 0}
