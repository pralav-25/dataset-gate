from dataset_gate.profilers.text import analyze


def test_lengths_unicode_and_empty():
    assert analyze(["x", " hi ", "🙂"])["text"] == {
        "min_length": 1,
        "max_length": 4,
        "surrounding_whitespace": 1,
    }
    assert analyze([])["text"]["max_length"] is None
