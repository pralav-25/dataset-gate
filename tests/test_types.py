import pytest

from dataset_gate.types import infer_type, scalar_type


@pytest.mark.parametrize(
    "value,expected",
    [
        ("01", "string"),
        ("0", "integer"),
        ("-4", "integer"),
        ("1.5", "number"),
        ("NaN", "string"),
        ("2026-09-24", "date"),
        ("2026-02-30", "string"),
        ("true", "boolean"),
    ],
)
def test_lexical(value, expected):
    assert scalar_type(value) == expected


def test_inference():
    assert infer_type(["1", "2.5", ""]) == "number"
    assert infer_type([""]) == "unknown"
    assert infer_type(["1", "x"]) == "string"
