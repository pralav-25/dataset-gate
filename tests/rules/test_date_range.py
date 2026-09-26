import pytest

from dataset_gate.errors import GateError

BOUNDS = {"min": "2024-02-28", "max": "2024-03-01"}


def test_leap_day_inclusive_bounds_and_record_numbers(run_rule):
    result = run_rule(
        "date_range",
        'value\n2024-02-28\n2024-02-29\n2024-03-01\n""\n2024-03-02\n2023-02-29\n20240229\n 2024-02-29',
        BOUNDS,
    )
    assert (result["checked"], result["failed"], list(result["records"])) == (7, 4, [5, 6, 7, 8])


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"min": "2024-02-30", "max": "2024-03-01"},
        {"min": True, "max": "2024-03-01"},
        {"min": "2025-01-01", "max": "2024-01-01"},
        {**BOUNDS, "typo": 1},
    ],
)
def test_invalid_configuration_even_without_rows(run_rule, params):
    with pytest.raises(GateError):
        run_rule("date_range", "value\n", params)


def test_blank_column_skipped_and_missing_column_fails(run_rule):
    assert run_rule("date_range", 'value\n""', BOUNDS)["checked"] == 0
    assert not run_rule("date_range", "other\n1", BOUNDS)["passed"]
