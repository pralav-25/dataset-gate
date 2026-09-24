"""Profile a CSV/TSV/gzip dataset."""

from dataset_gate.commands._common import inputs, output, output_options
from dataset_gate.load import load_dataset
from dataset_gate.profile import profile


def configure(subparsers):
    parser = subparsers.add_parser("profile", help="Summarize dataset structure and distributions")
    inputs(parser)
    output_options(parser)
    parser.set_defaults(run=run)


def run(args):
    output(
        args,
        profile(load_dataset(args.dataset, delimiter=args.delimiter)),
        protected=[args.dataset],
    )
