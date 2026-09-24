"""Read gzip data without allowing compressed inputs to bypass the CSV size cap."""

import gzip
import zlib

from dataset_gate.data import MAX_BYTES, read_text
from dataset_gate.errors import GateError


def read_gzip(path, *, delimiter=","):
    try:
        with gzip.open(path, "rb") as stream:
            raw = stream.read(MAX_BYTES + 1)
        if len(raw) > MAX_BYTES:
            raise GateError("decompressed CSV exceeds 5 MB")
        return read_text(raw.decode("utf-8-sig"), delimiter=delimiter)
    except (gzip.BadGzipFile, EOFError, UnicodeDecodeError, zlib.error) as exc:
        raise GateError("invalid gzip or UTF-8 data") from exc
