"""Show a run with its reviewer note, optionally updating that note."""

from dataset_gate.commands._common import history_options, output, output_options, store
from dataset_gate.history.detail import get_run
from dataset_gate.history.notes import get_note, set_note


def configure(subparsers):
    parser = subparsers.add_parser("show", help="Inspect a saved run")
    parser.add_argument("run_id")
    history_options(parser)
    output_options(parser)
    parser.add_argument("--note")
    parser.set_defaults(run=run)


def run(args):
    repository = store(args)
    result = get_run(repository, args.run_id)
    if args.note is not None:
        set_note(repository, args.run_id, args.note)
    output(args, {"report": result, "note": get_note(repository, args.run_id)}, protected=[args.db])
