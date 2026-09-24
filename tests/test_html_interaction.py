import base64
import hashlib

from dataset_gate.exporters.html import CSP, FILTERS, SCRIPT


def test_script_integrity_and_accessible_controls():
    digest = base64.b64encode(hashlib.sha256(SCRIPT.encode()).digest()).decode()
    assert "sha256-" + digest in CSP
    assert "innerHTML" not in SCRIPT and "eval(" not in SCRIPT
    assert 'for="rule-search"' in FILTERS and 'aria-live="polite"' in FILTERS
