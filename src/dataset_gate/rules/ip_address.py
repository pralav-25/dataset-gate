"""Validate unscoped IPv4 or IPv6 addresses."""

from ipaddress import ip_address

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    version = rule.params.get("version", "any")

    def valid(value):
        if "%" in value:
            return False
        try:
            address = ip_address(value)
            return version == "any" or address.version == version
        except ValueError:
            return False

    return row_check(data, rule.column, valid, message="Invalid IP address or address version")


SPEC = Spec(
    "ip_address",
    "Validate unscoped IPv4 or IPv6 addresses.",
    evaluate,
    {"version": lambda v: v == "any" or (type(v) is int and v in (4, 6))},
)
