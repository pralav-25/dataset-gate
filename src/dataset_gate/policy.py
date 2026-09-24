"""Exit 0 passes, 1 fails the quality gate, 2 is reserved by the CLI for usage/input errors."""

from dataset_gate.errors import GateError
from dataset_gate.rules._base import finite


def gate_passes(report, *, fail_on_warning=False, min_score=0):
    if not finite(min_score) or not 0 <= min_score <= 100:
        raise GateError("min_score must be 0..100")
    return (
        report["summary"]["errors"] == 0
        and (not fail_on_warning or report["summary"]["warnings"] == 0)
        and report["quality_score"] >= min_score
    )
