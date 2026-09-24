"""Promote passing baselines or compare two saved run reports."""

from dataset_gate.commands._common import history_options, output, output_options, store
from dataset_gate.errors import GateError
from dataset_gate.history.baselines import list_baselines, set_baseline
from dataset_gate.history.detail import get_run
from dataset_gate.history.diff import diff_runs


def configure(subparsers):
    parser = subparsers.add_parser("baseline", help="List or promote a named passing baseline")
    history_options(parser)
    output_options(parser)
    parser.add_argument("--name")
    parser.add_argument("--run-id")
    parser.add_argument("--replace", action="store_true")
    parser.set_defaults(run=run)
    diff = subparsers.add_parser("diff-runs", help="Compare outcomes of two saved runs")
    history_options(diff)
    output_options(diff)
    diff.add_argument("before")
    diff.add_argument("after")
    diff.set_defaults(run=diff_command)


def run(args):
    repository = store(args)
    if bool(args.name) != bool(args.run_id):
        raise GateError("--name and --run-id must be supplied together")
    if args.name:
        set_baseline(repository, args.name, args.run_id, replace=args.replace)
    output(args, list_baselines(repository), protected=[args.db])


def diff_command(args):
    repository = store(args)
    output(
        args,
        diff_runs(get_run(repository, args.before), get_run(repository, args.after)),
        protected=[args.db],
    )
