"""Compare report outcomes by stable rule id; changed contracts are explicitly flagged."""


def diff_runs(before, after):
    a = {row["id"]: row for row in before["results"]}
    b = {row["id"]: row for row in after["results"]}
    return {
        "before": before["run_id"],
        "after": after["run_id"],
        "contract_changed": before["contract_hash"] != after["contract_hash"],
        "score_delta": after["quality_score"] - before["quality_score"],
        "added_rules": sorted(b.keys() - a.keys()),
        "removed_rules": sorted(a.keys() - b.keys()),
        "changes": [
            {
                "id": key,
                "before_failed": a[key]["failed"],
                "after_failed": b[key]["failed"],
                "regressed": a[key]["passed"] and not b[key]["passed"],
                "resolved": not a[key]["passed"] and b[key]["passed"],
            }
            for key in sorted(a.keys() & b.keys())
            if a[key]["failed"] != b[key]["failed"] or a[key]["passed"] != b[key]["passed"]
        ],
    }
