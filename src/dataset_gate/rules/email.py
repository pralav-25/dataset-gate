"""Check a conservative ASCII email shape; this does not verify ownership or delivery."""

import re

from dataset_gate.rules._base import Spec, row_check


def valid(value):
    if len(value) > 254 or value.count("@") != 1:
        return False
    local, domain = value.split("@")
    if not 1 <= len(local) <= 64 or local.startswith(".") or local.endswith(".") or ".." in local:
        return False
    return (
        bool(re.fullmatch(r"[A-Za-z0-9.!#$%&'*+/=?^_`{|}~-]+", local))
        and len(domain.split(".")) >= 2
        and all(
            re.fullmatch(r"[A-Za-z0-9](?:[A-Za-z0-9-]{0,61}[A-Za-z0-9])?", label)
            for label in domain.split(".")
        )
    )


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Invalid conservative email syntax")


SPEC = Spec(
    "email",
    "Check a conservative ASCII email shape; this does not verify ownership or delivery.",
    evaluate,
    {},
    (),
    column=True,
)
