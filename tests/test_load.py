import gzip

from dataset_gate.load import load_dataset


def test_tsv_and_override(tmp_path):
    path = tmp_path / "data.tsv.gz"
    path.write_bytes(gzip.compress(b"a\tb\n1\t2"))
    assert load_dataset(path).columns == ("a", "b")
    other = tmp_path / "custom.csv"
    other.write_text("a;b\n1;2")
    assert load_dataset(other, delimiter=";").rows == (("1", "2"),)
