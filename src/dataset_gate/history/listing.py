"""Stable newest-first run listings, without loading full report bodies."""

from dataset_gate.errors import GateError


def list_runs(store, *, limit=25, offset=0, status=None, contract=None):
    if type(limit) is not int or not 1 <= limit <= 200 or type(offset) is not int or offset < 0:
        raise GateError("invalid pagination")
    if status is not None and status not in ("passed", "warning", "failed"):
        raise GateError("invalid status filter")
    conditions, values = [], []
    for name, value in [("status", status), ("contract", contract)]:
        if value is not None:
            conditions.append(name + " = ?")
            values.append(value)
    where = " WHERE " + " AND ".join(conditions) if conditions else ""
    with store.connect() as connection:
        total = connection.execute("SELECT count(*) FROM runs" + where, values).fetchone()[0]
        rows = connection.execute(
            "SELECT id,created_at,contract,status,score,dataset_hash,contract_hash FROM runs"
            + where
            + " ORDER BY created_at DESC,id DESC LIMIT ? OFFSET ?",
            values + [limit, offset],
        ).fetchall()
    return {"total": total, "limit": limit, "offset": offset, "items": [dict(row) for row in rows]}
