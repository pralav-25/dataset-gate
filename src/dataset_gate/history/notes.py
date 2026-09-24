"""Review notes are separate from immutable reports and cascade on run deletion."""

from dataset_gate.errors import GateError


def ensure(connection):
    connection.execute(
        "CREATE TABLE IF NOT EXISTS notes (run_id TEXT PRIMARY KEY REFERENCES runs(id) ON DELETE CASCADE, body TEXT NOT NULL)"
    )


def set_note(store, run_id, body):
    if not isinstance(body, str) or len(body) > 2000:
        raise GateError("note must be at most 2000 characters")
    with store.connect() as connection:
        ensure(connection)
        if not connection.execute("SELECT 1 FROM runs WHERE id=?", (run_id,)).fetchone():
            raise GateError("run not found")
        connection.execute(
            "INSERT INTO notes VALUES (?,?) ON CONFLICT(run_id) DO UPDATE SET body=excluded.body",
            (run_id, body),
        )


def get_note(store, run_id):
    with store.connect() as connection:
        ensure(connection)
        row = connection.execute("SELECT body FROM notes WHERE run_id=?", (run_id,)).fetchone()
    return row[0] if row else ""
