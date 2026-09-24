"""Validation reports never include raw cell values. Sample indices are bounded."""

from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from uuid import uuid4


@dataclass(frozen=True)
class Finding:
    checked: int
    failed: int
    records: tuple[int, ...] = ()
    message: str = ""


@dataclass(frozen=True)
class RuleResult:
    id: str
    check: str
    column: str | None
    severity: str
    checked: int
    failed: int
    records: tuple[int, ...]
    message: str

    @property
    def passed(self):
        return self.failed == 0


def report(contract, dataset, results):
    errors = sum(not result.passed and result.severity == "error" for result in results)
    warnings = sum(not result.passed and result.severity == "warning" for result in results)
    return {
        "schema_version": 1,
        "run_id": str(uuid4()),
        "created_at": datetime.now(UTC).isoformat(),
        "contract": contract.name,
        "row_count": len(dataset),
        "columns": list(dataset.columns),
        "status": "failed" if errors else "warning" if warnings else "passed",
        "summary": {
            "rules": len(results),
            "errors": errors,
            "warnings": warnings,
            "passed": sum(result.passed for result in results),
        },
        "results": [{**asdict(result), "passed": result.passed} for result in results],
    }
