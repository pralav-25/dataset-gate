"""Serve locally; external binding requires an explicit host choice."""

from dataset_gate.commands._common import history_options
from dataset_gate.errors import GateError


def configure(subparsers):
    parser = subparsers.add_parser("serve", help="Start the optional local HTTP API")
    history_options(parser)
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8765)
    parser.set_defaults(run=run)


def run(args):
    if not 1 <= args.port <= 65535:
        raise GateError("port must be 1..65535")
    try:
        import uvicorn

        from dataset_gate.api.app import create_app
    except ImportError as exc:
        raise GateError('install the api extra: pip install "dataset-gate[api]"') from exc
    uvicorn.run(create_app(args.db), host=args.host, port=args.port)
