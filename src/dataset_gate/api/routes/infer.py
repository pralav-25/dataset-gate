"""Draft contracts from posted data without writing server files."""

from fastapi import APIRouter
from pydantic import Field

from dataset_gate.api.models import CSVInput
from dataset_gate.data import read_text
from dataset_gate.infer import infer_contract


class InferInput(CSVInput):
    name: str = Field(default="Inferred dataset contract", min_length=1, max_length=120)


router = APIRouter(tags=["Contracts"])


@router.post("/infer")
def infer(body: InferInput):
    return infer_contract(read_text(body.csv, delimiter=body.delimiter), name=body.name).to_dict()
