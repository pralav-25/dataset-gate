import pytest

from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.engine import validate


@pytest.fixture
def run_rule():
    def execute(check, csv, params, column="value"):
        contract = parse_contract(
            {
                "version": 1,
                "name": "Boundary tests",
                "rules": [{"id": "check", "check": check, "column": column, "params": params}],
            }
        )
        return validate(read_text(csv), contract)["results"][0]

    return execute
