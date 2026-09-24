"""Named reference runs must have passed. Replacement is an explicit caller choice."""

import re

from dataset_gate.errors import GateError


def ensure(connection):
    connection.execute(
        "CREATE TABLE IF NOT EXISTS baselines (name TEXT PRIMARY KEY,run_id TEXT NOT NULL REFERENCES runs(id) ON DELETE RESTRICT)"
    )


def set_baseline(store, name, run_id, *, replace=False):
    if not isinstance(name, str) or not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,63}", name):
        raise GateError("invalid baseline name")
    with store.connect() as connection:
        ensure(connection)
        run = connection.execute("SELECT status FROM runs WHERE id=?", (run_id,)).fetchone()
        if run is None or run[0] != "passed":
            raise GateError("baseline must reference a passing run")
        if (
            connection.execute("SELECT 1 FROM baselines WHERE name=?", (name,)).fetchone()
            and not replace
        ):
            raise GateError("baseline exists; use explicit replacement")
        connection.execute(
            "INSERT INTO baselines VALUES (?,?) ON CONFLICT(name) DO UPDATE SET run_id=excluded.run_id",
            (name, run_id),
        )


def list_baselines(store):
    with store.connect() as connection:
        ensure(connection)
        return [
            dict(row)
            for row in connection.execute("SELECT name,run_id FROM baselines ORDER BY name")
        ]
