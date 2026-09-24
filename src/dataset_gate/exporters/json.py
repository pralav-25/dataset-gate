"""Strict JSON with stable key order and readable Unicode."""

import json

EXTENSION = "json"


def render(report):
    return json.dumps(report, indent=2, sort_keys=True, ensure_ascii=False, allow_nan=False) + "\n"
