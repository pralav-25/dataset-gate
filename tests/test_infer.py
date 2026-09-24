from dataset_gate.data import read_text
from dataset_gate.infer import infer_contract


def test_draft_does_not_invent_constraints():
    draft = infer_contract(read_text("id,score\n001,2.5\n002,3"))
    assert [rule.check for rule in draft.rules] == ["required_column", "type"] * 2
    assert draft.rules[1].params["type"] == "string"
    assert draft.rules[3].params["type"] == "number"
