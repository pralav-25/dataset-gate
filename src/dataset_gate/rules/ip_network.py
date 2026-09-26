"""Validate unscoped CIDR networks with no host bits set."""

from ipaddress import ip_network

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    version = rule.params.get("version", "any")

    def valid(value):
        if "%" in value or value.count("/") != 1:
            return False
        prefix = value.rsplit("/", 1)[1]
        if not prefix or any(char < "0" or char > "9" for char in prefix):
            return False
        try:
            network = ip_network(value, strict=True)
            return version == "any" or network.version == version
        except ValueError:
            return False

    return row_check(data, rule.column, valid, message="Invalid CIDR network or address version")


SPEC = Spec(
    "ip_network",
    "Validate unscoped CIDR networks with no host bits set.",
    evaluate,
    {"version": lambda v: v == "any" or (type(v) is int and v in (4, 6))},
)
