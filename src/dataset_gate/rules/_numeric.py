"""Exact sums across the numeric domain accepted by the bounded CSV loader."""

from decimal import Decimal, localcontext


def exact_sum(values):
    with localcontext() as context:
        # Accepted cells have at most 128 characters and adjusted exponents in
        # +/-100. 512 digits cover their full span plus the 50,000-row carry.
        context.prec = 512
        return sum(values, Decimal(0))
