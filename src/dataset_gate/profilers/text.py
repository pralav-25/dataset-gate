"""Text quality descriptors without raw-value samples."""


def analyze(values):
    lengths = [len(value) for value in values]
    return {
        "text": {
            "min_length": min(lengths, default=None),
            "max_length": max(lengths, default=None),
            "surrounding_whitespace": sum(value != value.strip() for value in values),
        }
    }
