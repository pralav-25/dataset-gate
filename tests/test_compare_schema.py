from dataset_gate.comparators.schema import compare
from dataset_gate.data import read_text


def test_schema_events():
    assert compare(read_text("a,b"), read_text("b,a"))["schema"]["reordered"]
    assert compare(read_text("a,b"), read_text("a,c"))["schema"] == {
        "added": ["c"],
        "removed": ["b"],
        "reordered": False,
    }
