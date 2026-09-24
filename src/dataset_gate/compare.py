"""Combine descriptive comparisons with content identities and dataset sizes."""

import importlib
import pkgutil

from dataset_gate import comparators
from dataset_gate.fingerprint import dataset_fingerprint


def compare_datasets(before, after):
    result = {
        "schema_version": 1,
        "before_hash": dataset_fingerprint(before),
        "after_hash": dataset_fingerprint(after),
        "rows": {"before": len(before), "after": len(after), "delta": len(after) - len(before)},
    }
    for item in pkgutil.iter_modules(comparators.__path__):
        if not item.name.startswith("_"):
            result.update(
                importlib.import_module(f"dataset_gate.comparators.{item.name}").compare(
                    before, after
                )
            )
    return result
