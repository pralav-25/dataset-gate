"""Read-only runtime diagnostics do not initialize a history database."""

import importlib.util
import platform
import sqlite3

from dataset_gate import __version__
from dataset_gate.commands._common import output, output_options
from dataset_gate.data import MAX_BYTES, MAX_COLUMNS, MAX_ROWS


def configure(subparsers):
    parser = subparsers.add_parser("doctor", help="Check runtime and optional API availability")
    output_options(parser)
    parser.set_defaults(run=run)


def run(args):
    output(
        args,
        {
            "version": __version__,
            "python": platform.python_version(),
            "sqlite": sqlite3.sqlite_version,
            "api_available": importlib.util.find_spec("fastapi") is not None,
            "limits": {"bytes": MAX_BYTES, "rows": MAX_ROWS, "columns": MAX_COLUMNS},
        },
    )
