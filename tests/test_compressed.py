import gzip

import pytest

from dataset_gate.compressed import read_gzip
from dataset_gate.errors import GateError


def test_compressed(tmp_path):
    path = tmp_path / "data.csv.gz"
    path.write_bytes(gzip.compress(b"a\n1"))
    assert read_gzip(path).rows == (("1",),)
    path.write_bytes(b"bad")
    with pytest.raises(GateError):
        read_gzip(path)
