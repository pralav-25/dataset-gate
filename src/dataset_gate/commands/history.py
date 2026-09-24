"""List runs or explicitly apply a previewed retention plan."""

from dataset_gate.commands._common import history_options, output, output_options, store
from dataset_gate.history.listing import list_runs
from dataset_gate.history.retention import prune_runs


def configure(subparsers):
    parser = subparsers.add_parser("history", help="List saved runs or preview retention")
    history_options(parser)
    output_options(parser)
    parser.add_argument("--limit", type=int, default=25)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--status", choices=["passed", "warning", "failed"])
    parser.add_argument("--contract-name")
    parser.add_argument("--prune-keep", type=int)
    parser.add_argument("--apply", action="store_true")
    parser.set_defaults(run=run)


def run(args):
    result = (
        prune_runs(store(args), keep=args.prune_keep, dry_run=not args.apply)
        if args.prune_keep is not None
        else list_runs(
            store(args),
            limit=args.limit,
            offset=args.offset,
            status=args.status,
            contract=args.contract_name,
        )
    )
    output(args, result, protected=[args.db])
