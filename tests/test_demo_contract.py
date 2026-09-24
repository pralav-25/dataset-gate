from pathlib import Path

from dataset_gate.contracts import loads_contract
from dataset_gate.data import read_text
from dataset_gate.demo import sample_csv
from dataset_gate.run import run_validation


def test_demo_expected_outcomes():
    contract = loads_contract(Path("examples/tickets.contract.json").read_text())
    clean = run_validation(read_text(sample_csv()), contract)
    dirty = run_validation(read_text(sample_csv(dirty=True)), contract)
    assert clean["status"] == "passed" and clean["quality_score"] == 100
    assert (
        dirty["status"] == "failed"
        and dirty["summary"]["errors"] >= 8
        and dirty["summary"]["warnings"] == 1
    )
