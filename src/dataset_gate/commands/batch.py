"""Validate up to 50 datasets sequentially against one contract without losing file errors."""

from pathlib import Path

from dataset_gate.commands._common import (
    contract_file,
    history_options,
    output,
    output_options,
    store,
)
from dataset_gate.errors import GateError
from dataset_gate.history.save import save_run
from dataset_gate.load import load_dataset
from dataset_gate.policy import gate_passes
from dataset_gate.run import run_validation


def configure(subparsers):
    parser = subparsers.add_parser("batch", help="Validate multiple datasets against one contract")
    parser.add_argument("datasets", nargs="+", type=Path)
    parser.add_argument("--contract", required=True, type=Path)
    parser.add_argument("--delimiter")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true")
    output_options(parser)
    history_options(parser)
    parser.set_defaults(run=run)


def run(args):
    if len(args.datasets) > 50:
        raise GateError("batch accepts at most 50 datasets")
    contract = contract_file(args.contract)
    results = []
    code = 0
    for path in args.datasets:
        try:
            report = run_validation(load_dataset(path, delimiter=args.delimiter), contract)
            passed = gate_passes(report, fail_on_warning=args.fail_on_warning)
            results.append({"file": str(path), "gate_passed": passed, "report": report})
            if not passed:
                code = max(code, 1)
        except (GateError, OSError) as exc:
            results.append({"file": str(path), "input_error": str(exc)})
            code = 2
    output(
        args,
        {"files": len(results), "exit_code": code, "results": results},
        protected=[*args.datasets, args.contract, args.db],
    )
    if args.save:
        repository = store(args)
        for result in results:
            if "report" in result:
                save_run(repository, result["report"])
    return code
