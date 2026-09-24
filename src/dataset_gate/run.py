"""Application service: validation with profiling, identity, timing and a rule-pass score."""

from time import perf_counter

from dataset_gate.contract_hash import contract_fingerprint
from dataset_gate.engine import validate
from dataset_gate.fingerprint import dataset_fingerprint
from dataset_gate.profile import profile


def run_validation(data, contract):
    started = perf_counter()
    result = validate(data, contract)
    result["dataset_hash"] = dataset_fingerprint(data)
    result["contract_hash"] = contract_fingerprint(contract)
    result["profile"] = profile(data)
    result["quality_score"] = round(
        100 * result["summary"]["passed"] / result["summary"]["rules"], 2
    )
    result["duration_ms"] = round((perf_counter() - started) * 1000, 3)
    return result
