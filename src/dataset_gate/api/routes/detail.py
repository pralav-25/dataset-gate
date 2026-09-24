"""Get a report by id, with explicit 404 handling."""

from fastapi import APIRouter, HTTPException, Request

from dataset_gate.errors import GateError
from dataset_gate.history.detail import get_run
from dataset_gate.history.notes import get_note

router = APIRouter(tags=["History"])


@router.get("/runs/{run_id}")
def detail(run_id: str, request: Request):
    try:
        report = get_run(request.app.state.store, run_id)
    except GateError as exc:
        raise HTTPException(404, "run not found") from exc
    return {"report": report, "note": get_note(request.app.state.store, run_id)}
