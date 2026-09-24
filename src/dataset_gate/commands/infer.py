"""Draft a contract from observed data; users review it before enforcing it."""

from dataset_gate.commands._common import inputs, output, output_options
from dataset_gate.infer import infer_contract
from dataset_gate.load import load_dataset


def configure(subparsers):
    parser = subparsers.add_parser("infer", help="Draft a contract for review")
    inputs(parser)
    output_options(parser)
    parser.add_argument("--name", default="Inferred dataset contract")
    parser.set_defaults(run=run)


def run(args):
    output(
        args,
        infer_contract(
            load_dataset(args.dataset, delimiter=args.delimiter), name=args.name
        ).to_dict(),
        protected=[args.dataset],
    )
