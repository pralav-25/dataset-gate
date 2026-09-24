"""Total variation in [0,1] over nonblank exact strings; no category labels exported."""

from collections import Counter


def compare(before, after):
    result = []
    for name in before.columns:
        if name not in after.columns:
            continue
        a, b = (Counter(v for v in data.column(name) if v.strip()) for data in (before, after))
        na, nb = sum(a.values()), sum(b.values())
        distance = (
            sum(abs(a[k] / na - b[k] / nb) for k in a.keys() | b.keys()) / 2 if na and nb else None
        )
        result.append(
            {
                "column": name,
                "new_categories": len(b.keys() - a.keys()),
                "removed_categories": len(a.keys() - b.keys()),
                "total_variation": distance,
            }
        )
    return {"categories": result}
