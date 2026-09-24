"""Profile posted CSV text; server filesystem paths are never accepted."""

from fastapi import APIRouter

from dataset_gate.api.models import CSVInput
from dataset_gate.data import read_text
from dataset_gate.profile import profile

router = APIRouter(tags=["Datasets"])


@router.post("/profile")
def profile_dataset(body: CSVInput):
    return profile(read_text(body.csv, delimiter=body.delimiter))
