"""Built-in rule discovery; modules are shipped package code, never user plugins."""

import importlib
import pkgutil


def catalog():
    result = {}
    for module in pkgutil.iter_modules(__path__):
        if not module.name.startswith("_"):
            item = importlib.import_module(f"{__name__}.{module.name}").SPEC
            result[item.name] = item
    return result
