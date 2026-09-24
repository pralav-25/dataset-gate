"""Strict request models reject misspelled fields and implicit scalar coercion."""

from pydantic import BaseModel, ConfigDict, Field


class CSVInput(BaseModel):
    model_config = ConfigDict(extra="forbid", strict=True)
    csv: str = Field(max_length=5_000_000)
    delimiter: str = Field(default=",", min_length=1, max_length=1)
