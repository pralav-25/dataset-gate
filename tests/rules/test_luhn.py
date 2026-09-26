import pytest

from dataset_gate.errors import GateError


def test_known_checksums_and_single_digit_corruptions(run_rule):
    for value in ["79927398713", "1234567812345670", "18", "00", "091"]:
        assert run_rule("luhn", f"value\n{value}", {})["passed"]
        for index, char in enumerate(value):
            corrupted = value[:index] + str((int(char) + 1) % 10) + value[index + 1 :]
            assert not run_rule("luhn", f"value\n{corrupted}", {})["passed"]


def test_syntax_and_null_counts(run_rule):
    result = run_rule("luhn", 'value\n18\n""\n8\n 18\n１8\n1-8\n18.0', {})
    assert (result["checked"], result["failed"], list(result["records"])) == (6, 5, [3, 4, 5, 6, 7])


def test_unknown_parameter(run_rule):
    with pytest.raises(GateError):
        run_rule("luhn", "value\n", {"typo": 1})
