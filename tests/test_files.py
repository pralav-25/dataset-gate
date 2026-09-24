import os

import pytest

from dataset_gate.errors import GateError
from dataset_gate.files import write_output


def test_atomic_and_aliases(tmp_path):
    source = tmp_path / "input.csv"
    source.write_text("a\n1")
    alias = tmp_path / "alias"
    os.link(source, alias)
    with pytest.raises(GateError):
        write_output(alias, "bad", force=True, protected=[source])
    assert source.read_text() == "a\n1"
    target = tmp_path / "nested/report.json"
    write_output(target, "first")
    with pytest.raises(GateError):
        write_output(target, "second")
    write_output(target, "second", force=True)
    assert target.read_text() == "second"
    assert not list(target.parent.glob(".gate-*"))
