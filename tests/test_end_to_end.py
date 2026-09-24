import json
from pathlib import Path

from fastapi.testclient import TestClient

from dataset_gate.api.app import create_app
from dataset_gate.cli import main
from dataset_gate.history.detail import get_run
from dataset_gate.history.store import Store


def test_complete_workflow(tmp_path, capsys):
    db = tmp_path / "history.db"
    good = tmp_path / "good.json"
    bad = tmp_path / "bad.html"
    contract = "examples/tickets.contract.json"
    assert (
        main(
            [
                "validate",
                "examples/tickets.clean.csv",
                "--contract",
                contract,
                "--save",
                "--db",
                str(db),
                "-o",
                str(good),
            ]
        )
        == 0
    )
    good_report = json.loads(good.read_text())
    assert (
        main(["baseline", "--db", str(db), "--name", "release", "--run-id", good_report["run_id"]])
        == 0
    )
    capsys.readouterr()
    assert (
        main(
            [
                "validate",
                "examples/tickets.dirty.csv",
                "--contract",
                contract,
                "--save",
                "--db",
                str(db),
                "--format",
                "html",
                "-o",
                str(bad),
            ]
        )
        == 1
    )
    assert "Validation results" in bad.read_text()
    with TestClient(create_app(db)) as client:
        listing = client.get("/api/v1/runs").json()
        assert listing["total"] == 2
        bad_id = next(row["id"] for row in listing["items"] if row["status"] == "failed")
        assert client.get("/api/v1/runs/" + bad_id + "/report?format=junit").status_code == 200
        report = client.post(
            "/api/v1/validate",
            json={
                "csv": Path("examples/tickets.dirty.csv").read_text(),
                "contract": json.loads(Path(contract).read_text()),
            },
        ).json()
        assert report["results"] == get_run(Store(db), bad_id)["results"]
    assert main(["diff-runs", good_report["run_id"], bad_id, "--db", str(db)]) == 0
    diff = json.loads(capsys.readouterr().out)
    assert not diff["contract_changed"] and diff["score_delta"] < 0
