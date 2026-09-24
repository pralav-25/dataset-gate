# Dataset Gate

Data contracts and reproducible quality gates for CSV-based ML pipelines.
Python 3.11+. The validation engine and command-line application use only the
standard library. The optional local API uses FastAPI.

```bash
python -m pip install -e '.[api,dev]'
dataset-gate --help
pytest
```
