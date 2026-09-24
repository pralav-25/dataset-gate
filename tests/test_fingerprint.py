from dataset_gate.data import read_text
from dataset_gate.fingerprint import dataset_fingerprint


def test_semantic_csv_hash():
    assert dataset_fingerprint(read_text('a,b\n1,"x"')) == dataset_fingerprint(
        read_text("a,b\r\n1,x")
    )
    assert dataset_fingerprint(read_text("a,b\n1,x")) != dataset_fingerprint(read_text("b,a\nx,1"))
