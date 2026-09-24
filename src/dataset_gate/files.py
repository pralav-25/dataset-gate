"""Atomic UTF-8 output with default no-clobber semantics and input alias checks."""

import os
import tempfile
from pathlib import Path

from dataset_gate.errors import GateError


def write_output(path, content, *, force=False, protected=()):
    target = Path(path)
    for source in protected:
        source = Path(source)
        if target.resolve() == source.resolve() or (
            target.exists() and source.exists() and os.path.samefile(target, source)
        ):
            raise GateError("output must not overwrite an input file")
    if target.exists() and not force:
        raise GateError("output exists; use --force to replace it")
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".gate-", dir=target.parent)
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        if force:
            os.replace(temporary, target)
        else:
            try:
                os.link(temporary, target)
            except FileExistsError as exc:
                raise GateError("output already exists") from exc
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
