import pytest

from dataset_gate.errors import GateError


def test_exact_values_and_blank_exclusion(run_rule):
    result = run_rule("distinct_count", 'value\na\na\nA\n a\n""\n" "', {"min": 3, "max": 3})
    assert result["passed"] and result["checked"] == 1
    assert not run_rule("distinct_count", "value\na\nb", {"min": 0, "max": 1})["passed"]


def test_empty_and_all_blank(run_rule):
    for csv in ["value\n", 'value\n""']:
        assert run_rule("distinct_count", csv, {"min": 0, "max": 0})["passed"]


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"min": -1, "max": 2},
        {"min": True, "max": 2},
        {"min": 0, "max": 2.0},
        {"min": 3, "max": 2},
        {"min": 0, "max": 2, "typo": 1},
    ],
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("distinct_count", "value\n", params)
