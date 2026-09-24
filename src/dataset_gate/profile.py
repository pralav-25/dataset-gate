"""Dataset overview and extensible per-column profiles."""

import importlib
import pkgutil

from dataset_gate import profilers


def profile(data):
    plugins = [
        importlib.import_module(f"dataset_gate.profilers.{item.name}").analyze
        for item in pkgutil.iter_modules(profilers.__path__)
        if not item.name.startswith("_")
    ]
    columns = []
    for name in data.columns:
        values = data.column(name)
        present = [v for v in values if v.strip()]
        result = {
            "name": name,
            "count": len(values),
            "missing": len(values) - len(present),
            "missing_ratio": (len(values) - len(present)) / len(values) if values else 0,
            "distinct": len(set(present)),
        }
        for analyze in plugins:
            result.update(analyze(present))
        columns.append(result)
    return {
        "schema_version": 1,
        "row_count": len(data),
        "column_count": len(data.columns),
        "duplicate_rows": len(data.rows) - len(set(data.rows)),
        "columns": columns,
    }
