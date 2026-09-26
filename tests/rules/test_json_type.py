import csv
import io

import pytest

from dataset_gate.errors import GateError


def csv_text(values):
    stream = io.StringIO()
    writer = csv.writer(stream)
    writer.writerow(["value"])
    writer.writerows([value] for value in values)
    return stream.getvalue()


@pytest.mark.parametrize(
    "kind,value",
    [
        ("object", '{"key": 1}'),
        ("array", "[1,2]"),
        ("string", '"text"'),
        ("number", "1.25"),
        ("number", "1e99999"),
        ("boolean", "true"),
        ("null", "null"),
    ],
)
def test_json_types_do_not_confuse_booleans_and_numbers(run_rule, kind, value):
    for expected in ["object", "array", "string", "number", "boolean", "null"]:
        result = run_rule("json_type", csv_text([value, ""]), {"type": expected})
        assert result["checked"] == 1 and result["passed"] == (expected == kind)


@pytest.mark.parametrize(
    "value",
    [
        "{",
        "[NaN]",
        "Infinity",
        '{"x": -Infinity}',
        "01",
        "1e999999999999999999999999999",
        "[" * 1500,
    ],
)
def test_malformed_json_is_a_finding(run_rule, value):
    result = run_rule("json_type", csv_text([value]), {"type": "number"})
    assert result["failed"] == 1


@pytest.mark.parametrize(
    "params", [{}, {"type": "integer"}, {"type": []}, {"type": True}, {"type": "object", "typo": 1}]
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("json_type", "value\n", params)
