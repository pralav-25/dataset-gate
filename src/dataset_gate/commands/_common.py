"""Shared CLI file, JSON and history helpers."""

import json
from pathlib import Path

from dataset_gate.contracts import loads_contract
from dataset_gate.files import write_output
from dataset_gate.history.store import Store


def inputs(parser):
    parser.add_argument("dataset", type=Path)
    parser.add_argument("--delimiter")


def output_options(parser):
    parser.add_argument("-o", "--output", type=Path)
    parser.add_argument("--force", action="store_true")


def output(args, value, *, protected=(), raw=False):
    text = value if raw else json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    if args.output:
        write_output(args.output, text, force=args.force, protected=protected)
    else:
        print(text, end="")


def contract_file(path):
    return loads_contract(Path(path).read_text(encoding="utf-8"))


def history_options(parser):
    parser.add_argument("--db", type=Path, default=Path(".dataset-gate/history.db"))


def store(args):
    return Store(args.db)
