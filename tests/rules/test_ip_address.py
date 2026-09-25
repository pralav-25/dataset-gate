import pytest

from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate
from dataset_gate.errors import GateError


def execute(csv, params=None, column="value"):
    contract = parse_contract(
        {
            "version": 1,
            "name": "test",
            "rules": [
                {
                    "id": "rule",
                    "check": "ip_address",
                    "column": column,
                    "params": {"version": "any"} if params is None else params,
                }
            ],
        }
    )
    return validate(read_text(csv), contract)["results"][0]


def test_unknown_parameter():
    with pytest.raises(GateError):
        execute("value\n1", {"typo": 1})


def test_address_syntax_and_blank_counts():
    result = execute(
        'value\n127.0.0.1\n::1\n2001:db8::abcd\n""\n256.0.0.1\n192.168.1.01\nfe80::1%eth0\n10.0.0.0/8\n ::1'
    )
    assert (result["checked"], result["failed"], list(result["records"])) == (8, 5, [5, 6, 7, 8, 9])


def test_version_filter_and_default():
    for version in [4, 6]:
        result = execute("value\n127.0.0.1\n::1", {"version": version})
        assert result["checked"] == 2 and result["failed"] == 1
    assert execute("value\n::1", {})["passed"]


@pytest.mark.parametrize("version", [True, False, 4.0, "4", 5, None, []])
def test_malformed_version(version):
    with pytest.raises(GateError):
        execute("value\n::1", {"version": version})
