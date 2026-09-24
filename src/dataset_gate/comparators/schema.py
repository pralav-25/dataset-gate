"""Name-based schema comparison; reordering is reported separately from additions."""


def compare(before, after):
    added = [name for name in after.columns if name not in before.columns]
    removed = [name for name in before.columns if name not in after.columns]
    return {
        "schema": {
            "added": added,
            "removed": removed,
            "reordered": not added and not removed and before.columns != after.columns,
        }
    }
