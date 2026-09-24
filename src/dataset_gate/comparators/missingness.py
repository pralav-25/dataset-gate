"""Compare common-column blank rates; missing columns are a schema concern."""


def compare(before, after):
    result = []
    for name in before.columns:
        if name not in after.columns:
            continue
        rates = []
        for data in (before, after):
            values = data.column(name)
            rates.append(sum(not v.strip() for v in values) / len(values) if values else 0)
        result.append(
            {"column": name, "before": rates[0], "after": rates[1], "delta": rates[1] - rates[0]}
        )
    return {"missingness": result}
