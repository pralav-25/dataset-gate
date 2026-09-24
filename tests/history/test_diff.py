from dataset_gate.history.diff import diff_runs


def test_rule_identity_and_contract_change():
    a = {
        "run_id": "a",
        "contract_hash": "1",
        "quality_score": 100,
        "results": [{"id": "r", "failed": 0, "passed": True}],
    }
    b = {
        "run_id": "b",
        "contract_hash": "2",
        "quality_score": 0,
        "results": [{"id": "r", "failed": 2, "passed": False}],
    }
    result = diff_runs(a, b)
    assert result["contract_changed"] and result["score_delta"] == -100
    assert result["changes"][0]["regressed"]
