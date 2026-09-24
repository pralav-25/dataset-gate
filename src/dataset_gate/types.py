"""Conservative lexical types. Leading-zero identifiers remain strings."""

import re
from datetime import date

from dataset_gate.rules._base import number


def scalar_type(value):
    if not value.strip():
        return "null"
    if value in ("true", "false"):
        return "boolean"
    if re.fullmatch(r"-?(0|[1-9][0-9]*)", value):
        return "integer" if number(value) is not None else "string"
    if re.fullmatch(r"-?0[0-9]+", value):
        return "string"
    if number(value) is not None:
        return "number"
    try:
        if len(value) == 10 and date.fromisoformat(value).isoformat() == value:
            return "date"
    except ValueError:
        pass
    return "string"


def infer_type(values):
    types = {scalar_type(value) for value in values} - {"null"}
    if not types:
        return "unknown"
    if types <= {"integer", "number"}:
        return "integer" if types == {"integer"} else "number"
    return next(iter(types)) if len(types) == 1 else "string"
