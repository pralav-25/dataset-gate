"""GitHub Actions adapter: one validation, portable reports, explicit gate result."""

import os
import tempfile
from pathlib import Path

from dataset_gate.commands._common import contract_file
from dataset_gate.errors import GateError
from dataset_gate.exporters import render
from dataset_gate.files import write_output
from dataset_gate.load import load_dataset
from dataset_gate.policy import gate_passes
from dataset_gate.run import run_validation


def append_file(path, content):
    with Path(path).open("a", encoding="utf-8") as stream:
        stream.write(content)


def annotation(message):
    # Error messages may contain untrusted filenames or contract fields.
    return str(message).replace("%", "%25").replace("\r", "%0D").replace("\n", "%0A")


def workspace_file(workspace, relative_path, label):
    """Resolve an action input to a file contained in the checked-out repository."""
    path = Path(relative_path)
    if path.is_absolute():
        raise GateError(f"{label} path must be relative to the checked-out repository")
    root = workspace.resolve()
    try:
        resolved = (root / path).resolve(strict=True)
    except (OSError, RuntimeError) as exc:
        raise GateError(f"{label} file does not exist or cannot be resolved") from exc
    if not resolved.is_relative_to(root):
        raise GateError(f"{label} path must stay within the checked-out repository")
    if not resolved.is_file():
        raise GateError(f"{label} path must name a file")
    return resolved


def main():
    output = os.environ["GITHUB_OUTPUT"]
    try:
        dataset = os.environ.get("DATASET_GATE_DATASET", "")
        contract = os.environ.get("DATASET_GATE_CONTRACT", "")
        warning = os.environ.get("DATASET_GATE_FAIL_ON_WARNING", "false")
        if not dataset or not contract:
            raise GateError("dataset and contract inputs are required")
        if warning not in {"true", "false"}:
            raise GateError("fail-on-warning must be 'true' or 'false'")
        workspace = Path(os.environ["GITHUB_WORKSPACE"])
        data_path = workspace_file(workspace, dataset, "dataset")
        contract_path = workspace_file(workspace, contract, "contract")
        result = run_validation(load_dataset(data_path), contract_file(contract_path))
        passed = gate_passes(result, fail_on_warning=warning == "true")
        status = "passed" if passed else "failed"
        directory = Path(tempfile.mkdtemp(prefix="dataset-gate-", dir=os.environ["RUNNER_TEMP"]))
        # Render once from the same run, without storing a database or writing to the checkout.
        for format_name, extension in [("json", "json"), ("html", "html"), ("junit", "xml")]:
            write_output(directory / f"report.{extension}", render(result, format_name))
        summary = f"**Quality gate: {status.upper()}**\n\n" + render(result, "markdown")
        write_output(directory / "report.md", summary)
        append_file(os.environ["GITHUB_STEP_SUMMARY"], summary + "\n")
        append_file(output, f"report-directory={directory}\nstatus={status}\n")
        print(
            f"Dataset Gate: {status}; {result['row_count']} records; "
            f"{result['summary']['errors']} errors; {result['summary']['warnings']} warnings."
        )
        if not passed:
            print("::error::Dataset quality gate failed. See the job summary and reports.")
        return 0 if passed else 1
    except (GateError, OSError) as exc:
        append_file(output, "status=error\n")
        print(f"::error::{annotation(exc)}")
        return 2
