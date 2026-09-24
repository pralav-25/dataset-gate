"""HTTP validation uses the same application service as the CLI."""

from fastapi import APIRouter, Request

from dataset_gate.api.models import CSVInput
from dataset_gate.contracts import parse_contract
from dataset_gate.data import read_text
from dataset_gate.history.save import save_run
from dataset_gate.run import run_validation


class ValidateInput(CSVInput):
    contract: dict
    save: bool = False


router = APIRouter(tags=["Validation"])


@router.post("/validate")
def validate(body: ValidateInput, request: Request):
    result = run_validation(
        read_text(body.csv, delimiter=body.delimiter), parse_contract(body.contract)
    )
    if body.save:
        save_run(request.app.state.store, result)
    return result
