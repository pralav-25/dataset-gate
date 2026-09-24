import sqlite3

import pytest

from dataset_gate.errors import GateError
from dataset_gate.history.store import Store


def test_idempotent_schema_and_rollback(tmp_path):
    path = tmp_path / "nested/history.db"
    Store(path)
    store = Store(path)
    with pytest.raises(RuntimeError):
        with store.connect() as connection:
            connection.execute("INSERT INTO runs VALUES ('x','now','c','passed',100,'d','c','{}')")
            raise RuntimeError("rollback")
    with store.connect() as connection:
        assert connection.execute("SELECT count(*) FROM runs").fetchone()[0] == 0
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA user_version=99")
    connection.close()
    with pytest.raises(GateError):
        Store(path)
