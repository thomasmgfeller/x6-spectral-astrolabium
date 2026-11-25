"""Reproduce the packaged calculations using only Python's standard library."""
import hashlib
import json
import math
from pathlib import Path

from kontrollrechnung import check
from pruefung import run

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(actual, reference):
    if isinstance(reference, dict):
        assert actual.keys() == reference.keys()
        for key in reference:
            compare(actual[key], reference[key])
    elif isinstance(reference, list):
        assert len(actual) == len(reference)
        for value, expected in zip(actual, reference):
            compare(value, expected)
    else:
        assert math.isclose(actual, reference, rel_tol=1e-9, abs_tol=2e-14), (actual, reference)


def main():
    if not __debug__:
        raise RuntimeError('Bitte Python ohne -O ausführen.')
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        checksum, member = line.split('  ', 1)
        assert digest(ROOT / member) == checksum, member
    provenance = json.loads((ROOT / 'Herkunft.json').read_text())
    for member, data in provenance['files'].items():
        assert digest(ROOT / member) == data['sha256'], member
    checkpoints = json.loads(next((ROOT / 'basis').rglob('p3.json')).read_text())
    assert len(checkpoints) == 60
    assert all(row['checkpoint_id'] == 'P3' and row['execution'] == 'NOT_RUN' for row in checkpoints)
    result = run()
    assert result == json.loads((ROOT / 'ergebnisse.json').read_text())
    compare(check(result), json.loads((ROOT / 'quadratur.json').read_text()))
    print('PASS | SHA-256, Quellen, 63 rationale Kontrollen, Intervallgrenzen, zwei numerische Auflösungen')
    print('P3 | 60 von 60 NOT_RUN')


if __name__ == '__main__':
    main()
