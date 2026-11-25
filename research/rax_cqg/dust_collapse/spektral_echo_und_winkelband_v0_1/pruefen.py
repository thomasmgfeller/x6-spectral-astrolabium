"""Replay the analytic, archival and independent checks from the published bundle."""
import json
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import subprocess
import sys

from gegenrechnung_kappen import ratio
from gegenrechnung_exposition import exposure_details
ROOT = Path(__file__).resolve().parent

def verify():
    for row in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest, path = row.split('  ', 1)
        assert sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    got = subprocess.check_output([sys.executable, '-B', 'etappe2a_spektral_echo.py', '--json'], cwd=ROOT)
    assert got == (ROOT / 'Ergebnisse.json').read_bytes()
    main = json.loads(got)
    _, _, band = ratio()
    expo = exposure_details()
    expected = json.loads((ROOT / 'Gegenrechnung.json').read_bytes())
    assert list(map(str, band)) == expected['kinematischer_Quotient']
    assert json.loads(json.dumps(expo)) == expected['band_exposition']
    first = main['published_kinematic_pair']['degree1_ratio']
    assert F(first['lower']) <= band[0] <= band[1] <= F(first['upper'])
    assert main['uniform_exposure']['95_percent_first_exposure_threshold'] == expo['min_probes_interval']
    print('PASS: analytische Tests, PR-382-Echos, endliche Spektren, dynamische Kappen und Stichprobenexposition.')
if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    verify()
