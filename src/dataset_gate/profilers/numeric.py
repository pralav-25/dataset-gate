"""Finite numeric summary with linear-interpolated quantiles and population variance."""

import math

from dataset_gate.rules._base import number


def quantile(ordered, fraction):
    position = (len(ordered) - 1) * fraction
    low, high = math.floor(position), math.ceil(position)
    return (
        ordered[low] * (high - position) + ordered[high] * (position - low)
        if low != high
        else ordered[low]
    )


def analyze(values):
    parsed = [number(value) for value in values]
    numbers = sorted(float(value) for value in parsed if value is not None)
    result = {"parsed": len(numbers), "invalid": len(values) - len(numbers)}
    if numbers:
        mean = math.fsum(numbers) / len(numbers)
        result.update(
            min=min(numbers),
            max=max(numbers),
            mean=mean,
            stddev=math.sqrt(math.fsum((v - mean) ** 2 for v in numbers) / len(numbers)),
            p25=quantile(numbers, 0.25),
            median=quantile(numbers, 0.5),
            p75=quantile(numbers, 0.75),
        )
    return {"numeric": result}
