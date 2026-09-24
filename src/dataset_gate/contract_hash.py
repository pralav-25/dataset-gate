"""Contract identity includes rule order, defaults and descriptive names."""

import hashlib
import json


def contract_fingerprint(contract):
    canonical = json.dumps(
        contract.to_dict(),
        sort_keys=True,
        ensure_ascii=False,
        separators=(",", ":"),
        allow_nan=False,
    )
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
