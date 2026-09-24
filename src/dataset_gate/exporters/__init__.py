"""Report exporters expose render(report) and EXTENSION constants."""

import importlib
import pkgutil

from dataset_gate.errors import GateError


def formats():
    return sorted(
        item.name for item in pkgutil.iter_modules(__path__) if not item.name.startswith("_")
    )


def render(report, format="json"):
    if format not in formats():
        raise GateError(f"unknown report format: {format}")
    return importlib.import_module(f"{__name__}.{format}").render(report)
