from dataset_gate.comparators.numeric import compare
from dataset_gate.data import read_text


def test_mean_shift():
    result = compare(read_text("x\n1\n3"), read_text("x\n3\n5"))["numeric"][0]
    assert result["mean_delta"] == 2
    assert compare(read_text("x\na"), read_text("x\nb"))["numeric"] == []
