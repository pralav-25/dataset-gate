"""Retrieve stored reports using bound identifiers."""

import json

from dataset_gate.errors import GateError


def get_run(store, run_id):
    with store.connect() as connection:
        row = connection.execute("SELECT report FROM runs WHERE id=?", (run_id,)).fetchone()
    if row is None:
        raise GateError("run not found")
    return json.loads(row["report"])
