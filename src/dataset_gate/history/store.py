"""Small SQLite repository with WAL, foreign keys, and per-operation connections."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

from dataset_gate.errors import GateError


class Store:
    def __init__(self, path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as connection:
            version = connection.execute("PRAGMA user_version").fetchone()[0]
            if version not in (0, 1):
                raise GateError("unsupported history database version")
            connection.execute("PRAGMA journal_mode=WAL")
            connection.execute(
                "CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, created_at TEXT NOT NULL, contract TEXT NOT NULL, status TEXT NOT NULL, score REAL NOT NULL, dataset_hash TEXT NOT NULL, contract_hash TEXT NOT NULL, report TEXT NOT NULL)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS run_time ON runs(created_at DESC,id DESC)"
            )
            connection.execute(
                "CREATE INDEX IF NOT EXISTS run_contract ON runs(contract,created_at DESC)"
            )
            connection.execute("PRAGMA user_version=1")

    @contextmanager
    def connect(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys=ON")
        try:
            with connection:
                yield connection
        finally:
            connection.close()
