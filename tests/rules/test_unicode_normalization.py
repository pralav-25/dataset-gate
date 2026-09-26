import pytest

from dataset_gate.errors import GateError


@pytest.mark.parametrize(
    "form,passed,failed",
    [("NFC", "é", "e\u0301"), ("NFD", "e\u0301", "é"), ("NFKC", "A", "Ａ"), ("NFKD", "fi", "ﬁ")],
)
def test_canonical_and_compatibility_forms(run_rule, form, passed, failed):
    result = run_rule("unicode_normalization", f'value\n{passed}\n{failed}\n""', {"form": form})
    assert (result["checked"], result["failed"], list(result["records"])) == (2, 1, [2])


@pytest.mark.parametrize(
    "params", [{}, {"form": "nfc"}, {"form": None}, {"form": []}, {"form": "NFC", "typo": 1}]
)
def test_invalid_configuration(run_rule, params):
    with pytest.raises(GateError):
        run_rule("unicode_normalization", "value\n", params)
