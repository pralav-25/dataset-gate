"""Match whole nonblank cells using shell-style globs, not executable regular expressions."""

from fnmatch import fnmatchcase

from dataset_gate.rules._base import Spec, row_check, text


def evaluate(data, rule):
    return row_check(
        data,
        rule.column,
        lambda value: fnmatchcase(value, rule.params["glob"]),
        message="Value does not match the required glob",
    )


SPEC = Spec(
    "pattern",
    "Match whole nonblank cells using shell-style globs, not executable regular expressions.",
    evaluate,
    {"glob": text},
    ("glob",),
    column=True,
)
