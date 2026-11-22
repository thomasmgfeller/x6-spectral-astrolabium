"""Reproduce the model checks, the contrast enclosure and the optional numerical transfers."""
import argparse
from fractions import Fraction
import hashlib
import json
import math

from modell import ROOT, EDGES, PAST, FUTURE, INNER, ORDER, CUT, H, exact_checks
from schranken import DELTA, I, S, certify
from stencil import run as stencil_checks


def load(name):
    return json.loads((ROOT / name).read_bytes())


def digest(name):
    return hashlib.sha256((ROOT / name).read_bytes()).hexdigest()


def close_rows(new, stored, key=''):
    if isinstance(stored, dict):
        assert set(new) == set(stored), key
        for k, val in stored.items():
            close_rows(new[k], val, k)
    elif isinstance(stored, list):
        assert len(new) == len(stored), key
        for a, b in zip(new, stored):
            close_rows(a, b, key)
    elif isinstance(stored, (int, float)):
        # Near 2^-20, double rounding of phase differences is amplified in relative units.
        tol = 2e-6 if key == 'relative_error' else 1e-9
        assert math.isclose(new, stored, rel_tol=1e-10, abs_tol=tol), (key, new, stored)
    else:
        assert new == stored, (key, new, stored)


def verify_exact():
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        sha, path = line.split('  ', 1)
        assert digest(path) == sha, path
    for prefix in ('pruefplan', 'ergaenzung', 'kleinplan', 'eichung'):
        sha, name = (ROOT / (prefix + '.sha256')).read_text().split()
        assert sha == digest(name)
    for name, source in load('herkunft.json')['files'].items():
        assert digest('quellen/' + name) == source['sha256'], name
    checkpoints = load('quellen/p3.json')
    assert len(checkpoints) == 60 and all(c['execution'] == 'NOT_RUN' for c in checkpoints)
    algebra = {'schnitt': exact_checks(), 'dichten': stencil_checks()}
    assert json.loads(json.dumps(algebra, default=str)) == load('exakt.json')
    old = load('quellen/gegenpaar.json')['point']
    witness = algebra['schnitt']['witnesses']['original']
    assert witness['difference_sum_w_over_D'] == Fraction(old['delta_sum'])
    assert witness['difference_9w13_over_D'] == Fraction(old['delta_mixed_marker'])
    bounds = certify()
    assert bounds == load('schranken.json')
    # Every translated crossing lands in the inner sector. A shared past shift at
    # zero inner mass only adds the same constant to both ends of a past pair.
    assert all(j in INNER for i, j in EDGES if i in (4, 5, 6) and j in ORDER[CUT:])
    assert not any(i in PAST and j in FUTURE for i, j in EDGES)
    duration_lower = 4 * DELTA - I.of(Fraction(3, 32))
    excursion = DELTA * I.of(H) / (duration_lower * duration_lower.sqrt())
    assert Fraction(excursion.hi, S) + Fraction(1, 64) < Fraction(7, 128)
    for rho in ('1/8', '1/4'):
        for sector in ('limit', 'empty'):
            ref = load('quellen/nullgrenze.json')[rho + '|' + sector]
            assert Fraction(ref['unnormalized_modulus_floor']) > 0
            for sign in '+-':
                phases = ref['phase_intervals']
                assert phases['U+V'+sign] == phases['U-V'+sign]
        for sign in '+-':
            lo, hi = map(Fraction, bounds[rho]['directions'][sign]['delta_R_minus_pi_over_2'])
            assert lo*hi > 0 and (lo > 0) == (sign == '+')
    print('PASS  Schnittidentitaeten, 15 Dichtebasisvektoren, Intervalle, Quellen und 60 P3 NOT_RUN', flush=True)
    return bounds


def verify_numerical(bounds):
    from eichung import run as calibrate
    from kleinmassen import run as small_masses
    from rechnung import run as run_main
    calibration = calibrate()
    frozen = load('eichung.json')
    assert calibration['plan_sha256'] == frozen['plan_sha256'] == digest('ergaenzung.txt')
    close_rows(calibration['levels'], frozen['levels'])
    assert abs(float(calibration['offset'])-float(frozen['offset'])) < 1e-9
    assert 0 < float(frozen['gain']) and abs(float(calibration['gain'])-float(frozen['gain'])) < 1e-8
    rows = run_main()
    close_rows(rows, load('rechnung.json'))
    archive = load('quellen/volles_raster.json')
    for key, levels in rows.items():
        if key.startswith('witness|'):
            rho = key.split('|')[1]
            for tag, sign in [('4+', '+'), ('4-', '-')]:
                lo, hi = map(Fraction, bounds[rho]['directions'][sign]['delta_R_minus_pi_over_2'])
                for name in ('gauss5x10', 'cc5x9'):
                    values = levels[name]['shifted'][tag]
                    assert lo < values['delta_balance']['minus_pi_over_2'] < hi
                    assert values['plus']['minus_pi_over_2']['orthogonal_record_balance'] == 0
            continue
        fine = levels['gauss5x10']
        reference = archive[key]['levels']['5x10']['complex_kernels']['0']
        assert abs(complex(*reference)-complex(*fine['eleven_amplitudes']['0'])) < 1e-12
        assert abs(levels['cc5x9']['raw']-fine['raw']) < 1e-9
        if 'relative_error' in fine:
            assert abs(fine['relative_error']) < .02
        else:
            assert abs(fine['calibrated']) < 1e-10
    print('PASS  Eichung, Zweiarmauslese und 11 Einstellungen auf zwei Dichtezentren', flush=True)
    small = small_masses()
    close_rows(small, load('kleinmassen.json'))
    for levels in small.values():
        assert abs(levels['cc5x9']['relative_error']-levels['gauss5x10']['relative_error']) < 2e-6
        assert max(abs(levels[k]['relative_error']) for k in ('cc5x9', 'gauss5x10')) < .00014
    print('PASS  Sechs nachgelagerte Kleinmassentests', flush=True)


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Python bitte ohne -O aufrufen.')
    parser = argparse.ArgumentParser()
    parser.add_argument('--nur-exakt', action='store_true', help='Nur Algebra, Intervallbeweise und Archivprüfung')
    args = parser.parse_args()
    bounds = verify_exact()
    if not args.nur_exakt:
        verify_numerical(bounds)
