"""Convert a saved report into a portable report format."""

from dataset_gate.commands._common import history_options, output, output_options, store
from dataset_gate.exporters import formats, render
from dataset_gate.history.detail import get_run


def configure(subparsers):
    parser = subparsers.add_parser(
        "export", help="Export a saved run as JSON HTML Markdown JUnit or CSV"
    )
    parser.add_argument("run_id")
    history_options(parser)
    output_options(parser)
    parser.add_argument("--format", choices=formats(), default="html")
    parser.set_defaults(run=run)


def run(args):
    output(
        args, render(get_run(store(args), args.run_id), args.format), raw=True, protected=[args.db]
    )
