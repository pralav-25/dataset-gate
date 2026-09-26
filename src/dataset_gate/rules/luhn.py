"""Validate ASCII digit identifiers using the Luhn checksum."""

from dataset_gate.rules._base import Spec, row_check


def valid(value):
    if len(value) < 2 or any(char < "0" or char > "9" for char in value):
        return False
    total = 0
    for index, char in enumerate(reversed(value)):
        digit = ord(char) - ord("0")
        if index % 2:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def evaluate(data, rule):
    return row_check(data, rule.column, valid, message="Invalid Luhn identifier")


SPEC = Spec("luhn", "Validate ASCII digit identifiers using the Luhn checksum.", evaluate, {})
