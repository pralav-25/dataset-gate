"""Named baselines are promoted explicitly and never replace silently."""

from fastapi import APIRouter, Request
from pydantic import BaseModel, ConfigDict, Field

from dataset_gate.history.baselines import list_baselines, set_baseline


class BaselineInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    name: str = Field(min_length=1, max_length=64)
    run_id: str = Field(min_length=1, max_length=64)
    replace: bool = False


router = APIRouter(tags=["Baselines"])


@router.get("/baselines")
def listing(request: Request):
    return list_baselines(request.app.state.store)


@router.post("/baselines")
def promote(body: BaselineInput, request: Request):
    set_baseline(request.app.state.store, body.name, body.run_id, replace=body.replace)
    return {"name": body.name, "run_id": body.run_id}
