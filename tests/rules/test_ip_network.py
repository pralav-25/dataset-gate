import pytest

from dataset_gate.errors import GateError


def test_cidr_boundaries_and_host_bits(run_rule):
    result = run_rule(
        "ip_network",
        'value\n192.0.2.0/24\n2001:db8::/32\n0.0.0.0/0\n::/0\n192.0.2.1/32\n::1/128\n""\n192.0.2.1/24\n192.0.2.0\n192.0.2.0/255.255.255.0\nfe80::%eth0/64\n::/129\n::/-1',
        {},
    )
    assert (result["checked"], result["failed"], list(result["records"])) == (
        12,
        6,
        [8, 9, 10, 11, 12, 13],
    )


@pytest.mark.parametrize("version", [4, 6])
def test_version_filter(run_rule, version):
    result = run_rule("ip_network", "value\n0.0.0.0/0\n::/0", {"version": version})
    assert result["checked"] == 2 and result["failed"] == 1


@pytest.mark.parametrize(
    "params", [{"version": True}, {"version": 4.0}, {"version": "4"}, {"version": []}, {"typo": 1}]
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("ip_network", "value\n", params)
