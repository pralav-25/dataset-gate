"""Strict in-memory CSV ingestion with explicit resource bounds.

Cell values are preserved verbatim. Blank means whitespace-only. Record numbers
start at one after the header, independently of quoted multiline physical lines.
"""

import csv
import io
from dataclasses import dataclass
from pathlib import Path

from dataset_gate.errors import GateError

MAX_BYTES = 5_000_000
MAX_ROWS = 50_000
MAX_COLUMNS = 200


@dataclass(frozen=True)
class Dataset:
    columns: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]

    def column(self, name):
        if name not in self.columns:
            raise KeyError(name)
        position = self.columns.index(name)
        return tuple(row[position] for row in self.rows)

    def __len__(self):
        return len(self.rows)


def read_text(text, *, delimiter=","):
    if not isinstance(text, str) or len(text.encode("utf-8")) > MAX_BYTES:
        raise GateError("CSV exceeds the 5 MB text limit")
    if not isinstance(delimiter, str) or len(delimiter) != 1 or delimiter in '\r\n"':
        raise GateError("delimiter must be one non-newline character")
    if "\x00" in text:
        raise GateError("CSV cannot contain NUL characters")
    try:
        reader = csv.reader(
            io.StringIO(text.lstrip("\ufeff"), newline=""), delimiter=delimiter, strict=True
        )
        header = next(reader, None)
        if not header or any(not name.strip() for name in header):
            raise GateError("CSV requires nonempty column names")
        if len(header) > MAX_COLUMNS or len(header) != len(set(header)):
            raise GateError("CSV has too many columns or duplicate column names")
        rows = []
        for number, row in enumerate(reader, 1):
            if number > MAX_ROWS:
                raise GateError("CSV exceeds 50000 data records")
            if len(row) != len(header):
                raise GateError(f"record {number} has {len(row)} cells; expected {len(header)}")
            rows.append(tuple(row))
        return Dataset(tuple(header), tuple(rows))
    except csv.Error as exc:
        raise GateError(f"invalid CSV: {exc}") from exc


def read_csv(path, *, delimiter=","):
    with Path(path).open("rb") as stream:
        raw = stream.read(MAX_BYTES + 1)
    if len(raw) > MAX_BYTES:
        raise GateError("CSV exceeds the 5 MB file limit")
    try:
        return read_text(raw.decode("utf-8-sig"), delimiter=delimiter)
    except UnicodeDecodeError as exc:
        raise GateError("CSV must use UTF-8 encoding") from exc
