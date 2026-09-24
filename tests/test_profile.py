from dataset_gate.data import read_text
from dataset_gate.profile import profile


def test_overview():
    result = profile(read_text("a,b\n1,\n1,\n2,x"))
    assert result["row_count"] == 3 and result["duplicate_rows"] == 1
    assert result["columns"][1]["missing"] == 2
    assert result["columns"][0]["distinct"] == 2
    assert profile(read_text("a,b"))["row_count"] == 0
