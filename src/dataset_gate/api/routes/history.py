"""Report index endpoints expose metadata without raw dataset data."""

from fastapi import APIRouter, Query, Request

from dataset_gate.history.listing import list_runs

router = APIRouter(tags=["History"])


@router.get("/runs")
def history(
    request: Request,
    limit: int = Query(default=25, ge=1, le=200),
    offset: int = Query(default=0, ge=0),
    status: str | None = None,
    contract: str | None = None,
):
    return list_runs(
        request.app.state.store, limit=limit, offset=offset, status=status, contract=contract
    )
