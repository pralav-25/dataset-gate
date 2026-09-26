import pytest

from dataset_gate.errors import GateError


def test_decimal_exactness_and_cancellation(run_rule):
    assert run_rule("sum_range", "value\n0.1\n0.2", {"min": 0.3, "max": 0.3})["passed"]
    result = run_rule(
        "sum_range", 'value\n1e100\n1e-100\n-1e100\n""', {"min": 1e-100, "max": 1e-100}
    )
    assert result["checked"] == 1 and result["passed"] and result["records"] == ()


@pytest.mark.parametrize("csv", ["value\n", 'value\n""\n" "'])
def test_empty_sum_is_zero(run_rule, csv):
    assert run_rule("sum_range", csv, {"min": 0, "max": 0})["passed"]
    assert not run_rule("sum_range", csv, {"min": 1, "max": 2})["passed"]


@pytest.mark.parametrize("value", ["bad", "NaN", "Infinity", "1e101", "1e-101"])
def test_invalid_numbers_fail_one_aggregate(run_rule, value):
    result = run_rule("sum_range", f"value\n1\n{value}", {"min": 0, "max": 10})
    assert (result["checked"], result["failed"]) == (1, 1)


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"min": 2, "max": 1},
        {"min": True, "max": 1},
        {"min": 0, "max": float("inf")},
        {"min": 0, "max": 1, "typo": 1},
    ],
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("sum_range", "value\n", params)
