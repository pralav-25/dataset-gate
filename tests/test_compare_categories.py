from dataset_gate.comparators.categories import compare
from dataset_gate.data import read_text


def test_distributions_without_raw_labels():
    result = compare(read_text("x\nprivate-a\nprivate-b"), read_text("x\nprivate-c\nprivate-c"))
    assert result["categories"][0]["total_variation"] == 1
    assert result["categories"][0]["new_categories"] == 1
    assert "private" not in str(result)
    assert compare(read_text("x"), read_text("x"))["categories"][0]["total_variation"] is None
