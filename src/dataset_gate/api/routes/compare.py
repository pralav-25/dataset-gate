"""Descriptive comparison endpoint for bounded before/after CSV text."""

from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict, Field

from dataset_gate.compare import compare_datasets
from dataset_gate.data import read_text


class CompareInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    before: str = Field(max_length=2_500_000)
    after: str = Field(max_length=2_500_000)
    delimiter: str = Field(default=",", min_length=1, max_length=1)


router = APIRouter(tags=["Datasets"])


@router.post("/compare")
def compare(body: CompareInput):
    return compare_datasets(
        read_text(body.before, delimiter=body.delimiter),
        read_text(body.after, delimiter=body.delimiter),
    )
