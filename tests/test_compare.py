from dataset_gate.compare import compare_datasets
from dataset_gate.data import read_text


def test_equal_data_has_zero_changes():
    data = read_text("a,b\n1,x\n2,y")
    result = compare_datasets(data, data)
    assert result["before_hash"] == result["after_hash"] and result["rows"]["delta"] == 0
    assert all(row["delta"] == 0 for row in result["missingness"])
    assert all(row["total_variation"] == 0 for row in result["categories"])
