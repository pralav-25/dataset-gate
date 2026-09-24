from dataset_gate.data import read_text
from dataset_gate.demo import sample_csv


def test_synthetic_reproducibility_and_defects():
    assert sample_csv() == sample_csv()
    clean, dirty = read_text(sample_csv()), read_text(sample_csv(dirty=True))
    assert len(clean) == len(dirty) == 300 and clean.columns == dirty.columns
    assert dirty.rows[1][0] == dirty.rows[0][0] and clean.rows[1][0] != clean.rows[0][0]
