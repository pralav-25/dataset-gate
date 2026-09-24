"""Run a quality gate, export reports, and optionally save its reproducible history."""

from pathlib import Path

from dataset_gate.commands._common import (
    contract_file,
    history_options,
    inputs,
    output,
    output_options,
    store,
)
from dataset_gate.exporters import formats, render
from dataset_gate.history.save import save_run
from dataset_gate.load import load_dataset
from dataset_gate.policy import gate_passes
from dataset_gate.run import run_validation


def configure(subparsers):
    parser = subparsers.add_parser("validate", help="Validate a dataset against a data contract")
    inputs(parser)
    output_options(parser)
    history_options(parser)
    parser.add_argument("--contract", type=Path, required=True)
    parser.add_argument("--format", choices=formats(), default="json")
    parser.add_argument("--save", action="store_true")
    parser.add_argument("--fail-on-warning", action="store_true")
    parser.add_argument("--min-score", type=float, default=0)
    parser.set_defaults(run=run)


def run(args):
    result = run_validation(
        load_dataset(args.dataset, delimiter=args.delimiter), contract_file(args.contract)
    )
    passed = gate_passes(result, fail_on_warning=args.fail_on_warning, min_score=args.min_score)
    output(
        args,
        render(result, args.format),
        raw=True,
        protected=[args.dataset, args.contract, args.db],
    )
    if args.save:
        save_run(store(args), result)
    return 0 if passed else 1
