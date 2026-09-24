import pytest

from dataset_gate.data import read_csv, read_text
from dataset_gate.errors import GateError


def test_quoted_multiline_and_preservation(tmp_path):
    source = 'id,note\r\n1,"a,b"\r\n2,"line1\nline2"\r\n3,  \r\n'
    data = read_text(source)
    assert data.column("note") == ("a,b", "line1\nline2", "  ")
    file = tmp_path / "data.csv"
    file.write_text("\ufeff" + source)
    assert read_csv(file) == data


@pytest.mark.parametrize("source", ["", "a,a\n1,2", ",b\n1,2", "a,b\n1", 'a\n"oops', "a\nx\x00"])
def test_invalid(source):
    with pytest.raises(GateError):
        read_text(source)


def test_header_only_and_blank_record():
    assert len(read_text("a,b\n")) == 0
    with pytest.raises(GateError):
        read_text("a,b\n\n")
