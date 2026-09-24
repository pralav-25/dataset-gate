"""Compare two datasets descriptively without a quality-gate threshold."""

from pathlib import Path

from dataset_gate.commands._common import output, output_options
from dataset_gate.compare import compare_datasets
from dataset_gate.load import load_dataset


def configure(subparsers):
    parser = subparsers.add_parser("compare", help="Compare two dataset revisions")
    parser.add_argument("before", type=Path)
    parser.add_argument("after", type=Path)
    parser.add_argument("--delimiter")
    output_options(parser)
    parser.set_defaults(run=run)


def run(args):
    output(
        args,
        compare_datasets(
            load_dataset(args.before, delimiter=args.delimiter),
            load_dataset(args.after, delimiter=args.delimiter),
        ),
        protected=[args.before, args.after],
    )
