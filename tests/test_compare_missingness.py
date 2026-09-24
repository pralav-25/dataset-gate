from dataset_gate.comparators.missingness import compare
from dataset_gate.data import read_text


def test_delta():
    result = compare(read_text("a,b\n1,x\n2,y"), read_text("a,b\n,x\n2,y"))
    assert result["missingness"][0]["delta"] == 0.5
