"""Exercise the real action process from a separate consumer checkout."""

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def consumer(tmp_path):
    workspace = tmp_path / "consumer"
    workspace.mkdir()
    runner = tmp_path / "runner"
    runner.mkdir()
    (workspace / "data.csv").write_text("id\na\nb\n")
    (workspace / "contract.json").write_text(
        json.dumps(
            {
                "version": 1,
                "name": "Identifiers",
                "rules": [{"id": "unique", "check": "unique", "column": "id"}],
            }
        )
    )
    return workspace, runner


def run_action(consumer, **inputs):
    workspace, runner = consumer
    output, summary = runner / "output", runner / "summary"
    output.write_text("")
    summary.write_text("")
    result = subprocess.run(
        [sys.executable, "-I", str(ROOT / "scripts/github_action.py")],
        cwd=workspace,
        env={
            **os.environ,
            "GITHUB_WORKSPACE": str(workspace),
            "RUNNER_TEMP": str(runner),
            "GITHUB_OUTPUT": str(output),
            "GITHUB_STEP_SUMMARY": str(summary),
            "DATASET_GATE_DATASET": "data.csv",
            "DATASET_GATE_CONTRACT": "contract.json",
            "DATASET_GATE_FAIL_ON_WARNING": "false",
            **inputs,
        },
        capture_output=True,
        text=True,
    )
    values = dict(line.split("=", 1) for line in output.read_text().splitlines())
    return result, values, summary.read_text()


def test_clean_data_produces_consistent_reports_without_installing(consumer):
    workspace, runner = consumer
    # A consumer package with the same name must not shadow the bundled implementation.
    (workspace / "dataset_gate.py").write_text("raise RuntimeError('shadowed')")
    before = {path.name: path.read_bytes() for path in workspace.iterdir()}
    result, outputs, summary = run_action(consumer)
    assert result.returncode == 0, result.stdout + result.stderr
    assert outputs["status"] == "passed"
    directory = Path(outputs["report-directory"])
    assert directory.parent == runner
    report = json.loads((directory / "report.json").read_text())
    assert report["row_count"] == 2 and report["summary"]["passed"] == 1
    assert {path.name for path in directory.iterdir()} == {
        "report.json",
        "report.html",
        "report.xml",
        "report.md",
    }
    assert "Quality gate: PASSED" in summary
    assert "Identifiers" in (directory / "report.html").read_text()
    assert 'failures="0"' in (directory / "report.xml").read_text()
    assert before == {path.name: path.read_bytes() for path in workspace.iterdir()}


def test_failed_gate_keeps_reports_and_returns_one(consumer):
    (consumer[0] / "data.csv").write_text("id\na\na\n")
    result, outputs, summary = run_action(consumer)
    assert result.returncode == 1
    assert outputs["status"] == "failed" and "Quality gate: FAILED" in summary
    report = json.loads((Path(outputs["report-directory"]) / "report.json").read_text())
    assert report["summary"]["errors"] == 1


@pytest.mark.parametrize("strict,code,status", [("false", 0, "passed"), ("true", 1, "failed")])
def test_warning_policy_is_reflected_in_gate_status(consumer, strict, code, status):
    workspace, _ = consumer
    (workspace / "data.csv").write_text("id\na\na\n")
    path = workspace / "contract.json"
    contract = json.loads(path.read_text())
    contract["rules"][0]["severity"] = "warning"
    path.write_text(json.dumps(contract))
    result, outputs, summary = run_action(consumer, DATASET_GATE_FAIL_ON_WARNING=strict)
    assert result.returncode == code and outputs["status"] == status
    assert f"Quality gate: {status.upper()}" in summary
    assert "Status: **warning**" in summary


@pytest.mark.parametrize(
    "inputs",
    [
        {"DATASET_GATE_DATASET": ""},
        {"DATASET_GATE_CONTRACT": "missing.json"},
        {"DATASET_GATE_FAIL_ON_WARNING": "yes"},
    ],
)
def test_invalid_inputs_return_two_without_reports(consumer, inputs):
    result, outputs, _ = run_action(consumer, **inputs)
    assert result.returncode == 2 and outputs == {"status": "error"}
    assert "::error::" in result.stdout


def test_malformed_contract_is_an_error(consumer):
    (consumer[0] / "contract.json").write_text("{broken")
    result, outputs, _ = run_action(consumer)
    assert result.returncode == 2 and outputs == {"status": "error"}


def test_repeated_runs_keep_separate_reports(consumer):
    first, one, _ = run_action(consumer)
    (consumer[0] / "data.csv").write_text("id\na\na\n")
    second, two, _ = run_action(consumer)
    assert first.returncode == 0 and second.returncode == 1
    assert one["report-directory"] != two["report-directory"]
    assert (
        json.loads((Path(one["report-directory"]) / "report.json").read_text())["status"]
        == "passed"
    )


def test_shell_metacharacters_in_paths_are_literal(consumer):
    name = "data $(touch injected); with spaces.csv"
    (consumer[0] / "data.csv").rename(consumer[0] / name)
    result, outputs, _ = run_action(consumer, DATASET_GATE_DATASET=name)
    assert result.returncode == 0 and outputs["status"] == "passed"
    assert not (consumer[0] / "injected").exists()


def test_error_text_cannot_inject_workflow_commands(consumer):
    path = consumer[0] / "contract.json"
    contract = json.loads(path.read_text())
    contract["rules"][0]["check"] = "unknown\n::warning::injected"
    path.write_text(json.dumps(contract))
    result, outputs, _ = run_action(consumer)
    assert result.returncode == 2 and outputs["status"] == "error"
    assert "\n::warning::" not in result.stdout and "%0A" in result.stdout
