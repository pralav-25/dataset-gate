"""Render saved reports with explicit media types and safe generated filenames."""

from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import Response

from dataset_gate.errors import GateError
from dataset_gate.exporters import render
from dataset_gate.history.detail import get_run

router = APIRouter(tags=["Reports"])
MEDIA = {
    "html": "text/html",
    "json": "application/json",
    "markdown": "text/markdown",
    "junit": "application/xml",
    "csv": "text/csv",
}


@router.get("/runs/{run_id}/report")
def export(run_id: str, request: Request, format: str = "html"):
    if format not in MEDIA:
        raise HTTPException(400, "unsupported report format")
    try:
        report = get_run(request.app.state.store, run_id)
    except GateError as exc:
        raise HTTPException(404, "run not found") from exc
    return Response(
        render(report, format),
        media_type=MEDIA[format],
        headers={"X-Content-Type-Options": "nosniff", "Cache-Control": "no-store"},
    )
