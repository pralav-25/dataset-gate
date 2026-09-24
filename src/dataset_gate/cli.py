"""Composable command-line entry point with consistent user-error exit codes."""

import argparse
import importlib
import pkgutil
import sqlite3
import sys

from dataset_gate import __version__, commands
from dataset_gate.errors import GateError


def parser():
    result = argparse.ArgumentParser(
        prog="dataset-gate", description="Check data before it enters your pipeline."
    )
    result.add_argument("--version", action="version", version=__version__)
    subparsers = result.add_subparsers(dest="command")
    for module in sorted(pkgutil.iter_modules(commands.__path__), key=lambda item: item.name):
        if not module.name.startswith("_"):
            importlib.import_module(f"dataset_gate.commands.{module.name}").configure(subparsers)
    return result


def main(argv=None):
    root = parser()
    args = root.parse_args(argv)
    if not hasattr(args, "run"):
        root.print_help()
        return 0
    try:
        return args.run(args) or 0
    except sqlite3.Error:
        print("Error: history database is unavailable or invalid", file=sys.stderr)
        return 2
    except (GateError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
