"""Write a deterministic synthetic dataset, protected against accidental replacement."""

from dataset_gate.commands._common import output, output_options
from dataset_gate.demo import sample_csv


def configure(subparsers):
    parser = subparsers.add_parser("demo", help="Generate synthetic support-ticket CSV data")
    output_options(parser)
    parser.add_argument("--rows", type=int, default=300)
    parser.add_argument("--dirty", action="store_true")
    parser.set_defaults(run=run)


def run(args):
    output(args, sample_csv(args.rows, dirty=args.dirty), raw=True)
