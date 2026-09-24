import pytest
from fastapi.testclient import TestClient

from dataset_gate.api.app import create_app


@pytest.fixture
def client(tmp_path):
    with TestClient(create_app(tmp_path / "history.db")) as client:
        yield client
