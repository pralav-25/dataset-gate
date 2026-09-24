"""Persist one generated report atomically. Reusing an id cannot replace history."""

import json
import sqlite3

from dataset_gate.errors import GateError


def save_run(store, report):
    try:
        with store.connect() as connection:
            connection.execute(
                "INSERT INTO runs VALUES (?,?,?,?,?,?,?,?)",
                (
                    report["run_id"],
                    report["created_at"],
                    report["contract"],
                    report["status"],
                    report["quality_score"],
                    report["dataset_hash"],
                    report["contract_hash"],
                    json.dumps(report, allow_nan=False),
                ),
            )
    except sqlite3.IntegrityError as exc:
        raise GateError("run id already exists") from exc
    return report["run_id"]
