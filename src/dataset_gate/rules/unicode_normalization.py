"""Require a declared Unicode normalization form without rewriting values."""

import unicodedata

from dataset_gate.rules._base import Spec, row_check


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda v: unicodedata.is_normalized(rule.params["form"], v),
        message="Text is not in the required Unicode normalization form",
    )


SPEC = Spec(
    "unicode_normalization",
    "Require a declared Unicode normalization form.",
    evaluate,
    {"form": lambda v: v in ("NFC", "NFD", "NFKC", "NFKD")},
    ("form",),
)
