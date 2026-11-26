"""Run the published N19 calculation offline and regenerate all five local records."""
import hashlib
import json
import subprocess
import sys
from fractions import Fraction as F

from herkunft import ROOT, inputs
from eichen import H_LIMIT, evaluate as calibrate
import eichprobe
import streuung
import zeugen
import zeugenprobe


def check_report(filename, expected):
    serialized = (json.dumps(expected, indent=2, sort_keys=True) + '\n').encode()
    if (ROOT / filename).read_bytes() != serialized:
        raise ValueError('Ergebnis weicht ab: ' + filename)
    print('PASS', filename, flush=True)


def main():
    if not __debug__:
        raise SystemExit('Bitte Python ohne -O starten.')
    for manifest in [ROOT / 'SHA256SUMS', *sorted(ROOT.glob('*.sha256'))]:
        for line in manifest.read_text().splitlines():
            digest, filename = line.split('  ', 1)
            assert hashlib.sha256((ROOT / filename).read_bytes()).hexdigest() == digest, filename
    with inputs() as (baseline, prev, early):
        subprocess.run([sys.executable, '-B', 'pruefen.py'], cwd=baseline, check=True)
        published = json.loads((baseline / 'Praeparation.json').read_text())['canonical']
        assert {F(r['k']): F(r['max_hbar_effective_for_this_gaussian']) for r in published} == {
            F(1): 10**11 * H_LIMIT, streuung.K0: H_LIMIT}
        check_report('Eichkontrollen.json', eichprobe.run(prev, early))
        check_report('Streuungskontrollen.json', streuung.run(prev, early))
        check_report('Zeugenkontrollen.json', zeugenprobe.run(baseline))
        check_report('Synthetische_Rohdaten.json', eichprobe.fixture(F(3000)))
        check_report('Synthetische_Zeugenlaeufe.json', zeugenprobe.fixture_witness())
    empty = json.loads((ROOT / 'Messstand.json').read_text())
    scale = calibrate(empty)
    assert scale['common_S0_Js'] is None and scale['scale_status'] == 'NOT_MEASURED'
    assert zeugen.evaluate(scale, empty)['witness_status'] == 'NOT_MEASURED'
    print('PASS Modell und synthetische Kontrollen. Physische Messungen: 0. P3: 60 NOT_RUN.')


if __name__ == '__main__':
    main()
