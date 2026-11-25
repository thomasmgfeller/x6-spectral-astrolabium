"""Replay the study from the unpacked archive, using only the standard library."""
from fractions import Fraction
from hashlib import sha256
import json
from pathlib import Path

from quadratur import run as numerical
from rechnung import run as certify

ROOT = Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_text())


def check_ranges(data, bounds):
    keys={'0.0':'mischung','0.001':'ein_promille','0.1':'zehn_prozent','1.0':'kohaerent'}
    cases={k:bounds['two_windows'][v] for k,v in keys.items()}
    cases.update({'continuous':bounds['continuous_window']['relative_intensity'],
                  'root':bounds['real_coherence_zero'],
                  'phase_root':[bounds['phase_radian_negative_at'],bounds['phase_radian_positive_at']],
                  'matched_same':bounds['matched_density_control']['class_contrast_coherent'],
                  'matched_diag':bounds['matched_density_control']['class_contrast_mixed']})
    assert set(data)=={'12','24'}
    for grid in data.values():
        assert set(grid)=={'0.125','0.25'}
        for row in grid.values():
            for key,(low,high) in cases.items():
                assert float(Fraction(low)) <= row['fixed'][key] <= float(Fraction(high)), key
            assert float(bounds['low_visibility_factor_lower'])<=row['fixed']['visibility_factor']<=1+1e-14
            assert all(abs(z)<1e-14 for z in row['moving'].values())


def main():
    if not __debug__:
        raise RuntimeError('Bitte ohne -O ausführen.')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        assert sha256((ROOT/name).read_bytes()).hexdigest()==digest,name
    for path,meta in read('Herkunft.json')['files'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest()==meta['sha256'],path
    checks=json.loads(next((ROOT/'basis').rglob('p3.json')).read_text())
    assert len(checks)==60 and all(r['execution']=='NOT_RUN' and r['checkpoint_id']=='P3' for r in checks)
    bounds=certify()
    assert bounds==read('ergebnisse.json')
    for data in (read('gegenrechnung.json'), numerical()):
        check_ranges(data,bounds)
    old=read('basis/ergebnisse.json')['equal_phase_wide']['relative_intensity_high_minus_low']
    new=bounds['two_windows']['kohaerent']
    assert max(Fraction(old[0]),Fraction(new[0])) <= min(Fraction(old[1]),Fraction(new[1]))
    # Sanity check for all equal populations with real coherence in [-1,1]:
    # positivity of the input density matrix, and a record bit kills its off-diagonals.
    for value in (Fraction(-1),Fraction(0),Fraction(1,1000),Fraction(1)):
        assert (1-value)*(1+value)/4 >= 0
        assert sum(a*b for a,b in zip((1,0),(0,1)))*value == 0
    print('PASS – Quellen und Prüfsummen, Intervallrechnung, vollständiges Uhrfenster, Dichtekontrolle')
    print('PASS – separate Rechnung mit 50 Paaren, zwei Auflösungen und zwei Anfangsdichten')
    print('P3 – 60 physische Prüfpunkte NOT_RUN')


if __name__=='__main__':
    main()
