import pytest

from dataset_gate.errors import GateError


def test_exact_matching_and_blank_skips(run_rule):
    result = run_rule(
        "not_in", 'value\nunknown\nUnknown\n unknown\nvalid\n""\n" "', {"values": ["unknown"]}
    )
    assert (result["checked"], result["failed"], list(result["records"])) == (4, 1, [1])


def test_failure_samples_are_bounded(run_rule):
    result = run_rule("not_in", "value\n" + "bad\n" * 30, {"values": ["bad"]})
    assert result["failed"] == 30 and len(result["records"]) == 20


@pytest.mark.parametrize(
    "params",
    [
        {},
        {"values": []},
        {"values": "bad"},
        {"values": ["bad", "bad"]},
        {"values": [1]},
        {"values": [""]},
        {"values": ["bad"], "typo": 1},
    ],
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("not_in", "value\n", params)
