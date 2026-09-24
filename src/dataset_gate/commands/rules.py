"""Display the built-in rule catalog."""

from dataset_gate.catalog import rule_catalog
from dataset_gate.commands._common import output, output_options


def configure(subparsers):
    parser = subparsers.add_parser("rules", help="List supported rules and their parameters")
    output_options(parser)
    parser.set_defaults(run=run)


def run(args):
    output(args, rule_catalog())
