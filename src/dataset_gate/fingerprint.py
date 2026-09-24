"""SHA-256 over canonical parsed records, preserving order and cell spelling."""

import hashlib
import json


def dataset_fingerprint(data):
    digest = hashlib.sha256()
    for row in (data.columns, *data.rows):
        digest.update(json.dumps(row, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        digest.update(b"\n")
    return digest.hexdigest()
