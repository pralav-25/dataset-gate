"""Require an absolute HTTP or HTTPS URL with a host and no embedded credentials."""

from urllib.parse import urlsplit

from dataset_gate.rules._base import Spec, row_check


def valid(value):
    try:
        parsed = urlsplit(value)
        return (
            parsed.scheme in ("http", "https")
            and bool(parsed.hostname)
            and parsed.username is None
            and parsed.password is None
            and not any(char.isspace() or ord(char) < 32 for char in value)
            and (parsed.port is None or 0 < parsed.port <= 65535)
        )
    except ValueError:
        return False


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Invalid absolute HTTP URL")


SPEC = Spec(
    "url",
    "Require an absolute HTTP or HTTPS URL with a host and no embedded credentials.",
    evaluate,
    {},
    (),
    column=True,
)
