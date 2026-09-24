"""Extension-based input routing; explicit separators override CSV/TSV defaults."""

from pathlib import Path

from dataset_gate.compressed import read_gzip
from dataset_gate.data import read_csv


def load_dataset(path, *, delimiter=None):
    suffixes = Path(path).suffixes
    chosen = delimiter if delimiter is not None else "\t" if ".tsv" in suffixes else ","
    return (
        read_gzip(path, delimiter=chosen)
        if suffixes and suffixes[-1] == ".gz"
        else read_csv(path, delimiter=chosen)
    )
