"""Require an absolute HTTP or HTTPS URL with a valid host and no embedded credentials."""

import ipaddress
import re
from urllib.parse import urlsplit

from dataset_gate.rules._base import Spec, row_check


def valid_host(host):
    try:
        ipaddress.ip_address(host)
        return True
    except ValueError:
        try:
            host = host.encode("idna").decode("ascii").rstrip(".")
        except UnicodeError:
            return False
        return 0 < len(host) <= 253 and all(
            re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
            for label in host.split(".")
        )


def valid(value):
    try:
        parsed = urlsplit(value)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and valid_host(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and "\\" not in value
            and not any(char.isspace() or ord(char) < 32 for char in value)
            and (parsed.port is None or 0 < parsed.port <= 65535)
        )
    except ValueError:
        return False


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Invalid absolute HTTP URL")


SPEC = Spec(
    "url",
    "Require an absolute HTTP or HTTPS URL with a valid host and no embedded credentials.",
    evaluate,
    {},
    (),
    column=True,
)
