import gzip

import pytest

from dataset_gate.compressed import read_gzip
from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError
from dataset_gate.rules.url import valid
from dataset_gate.types import scalar_type


def test_corrupt_deflate_is_a_user_error(tmp_path):
    data = bytearray(gzip.compress(b"value\n1\n2"))
    data[10] = 255
    path = tmp_path / "corrupt.csv.gz"
    path.write_bytes(data)
    with pytest.raises(GateError):
        read_gzip(path)


@pytest.mark.parametrize(
    "url",
    [
        "http://bad_host/a",
        "http://-bad.example",
        "http://a\\b",
        "http://user:pass@example.com",
        "http://example.com:99999",
    ],
)
def test_malformed_hosts(url):
    assert not valid(url)


@pytest.mark.parametrize(
    "url",
    ["https://example.com/a", "http://127.0.0.1:8765", "http://[::1]/", "https://münich.example/"],
)
def test_valid_hosts(url):
    assert valid(url)


def test_numeric_domain_is_consistent_with_type_inference():
    assert scalar_type("9" * 128) == "string"
    assert scalar_type("9" * 100) == "integer"


def test_missing_column_is_reported_without_crashing():
    contract = parse_contract(
        {
            "version": 1,
            "name": "missing",
            "rules": [{"id": "x", "check": "unique", "column": "absent"}],
        }
    )
    result = validate(read_text("present\n1"), contract)
    assert result["status"] == "failed" and result["results"][0]["failed"] == 1
