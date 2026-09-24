"""Pruning defaults to dry-run; baseline references are protected when present."""

from dataset_gate.errors import GateError


def prune_runs(store, *, keep=100, dry_run=True):
    if type(keep) is not int or keep < 1:
        raise GateError("keep must be a positive integer")
    with store.connect() as connection:
        tables = {
            row[0]
            for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")
        }
        protected = (
            {row[0] for row in connection.execute("SELECT run_id FROM baselines")}
            if "baselines" in tables
            else set()
        )
        ordered = [
            row[0]
            for row in connection.execute("SELECT id FROM runs ORDER BY created_at DESC,id DESC")
        ]
        candidates = [run_id for run_id in ordered[keep:] if run_id not in protected]
        if not dry_run:
            connection.executemany(
                "DELETE FROM runs WHERE id=?", [(run_id,) for run_id in candidates]
            )
    return {"dry_run": dry_run, "count": len(candidates), "run_ids": candidates}
