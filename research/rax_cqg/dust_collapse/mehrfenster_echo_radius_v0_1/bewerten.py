"""Open the scoring key only after storing and hashing the blind predictions."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

from basis import echos, ltb
from vorwaerts import CASES, as_bytes
from gegenrechnung_ltb import run as independent_light

ROOT = Path(__file__).resolve().parent


def deviation_interval(estimate, ref_low, ref_high):
    a = estimate / ref_low - 1
    b = estimate / ref_high - 1
    return (min(abs(a), abs(b)) if a * b > 0 else F(0), max(abs(a), abs(b)))


def evaluate(predictions, geodesics):
    result = {}
    for tag, mass in CASES:
        record = predictions[tag]
        rough = record['all_early']
        mark = F(13 * rough['marker'], 640)
        a_values = {'material': mark, 'support': F(10)}
        clocks = geodesics[str(mass)]['forward_control']
        numerical = clocks['material_station']['duration'] * 10**6
        assert rough['last_no'] < numerical <= rough['first_yes']
        entries = {}
        for target, a in a_values.items():
            ref = echos.late_radius(a, mass, F(0))
            # Separate time integration on the same mass shell, using the archived ODE.
            ode_ref = ltb.rk_radius(float(a), float(mass * ltb.mass_fraction(a)), ltb.END / 2)
            assert abs(ode_ref - float(sum(ref) / 2)) < 1e-10
            scores = {}
            for key in ('recorded_early', 'all_early'):
                predicted = record[key][target]
                low, high, estimate, guarantee = (F(predicted[k]) for k in (
                    'lower', 'upper', 'estimate', 'max_relative_error'))
                if not low <= ref[0] <= ref[1] <= high:
                    raise ArithmeticError('reference outside certified interval')
                error = deviation_interval(estimate, *ref)
                assert error[1] <= guarantee
                scores[key] = {'interval': [str(low), str(high)], 'estimate': str(estimate),
                               'max_relative_error': str(guarantee),
                               'observed_relative_error_interval': [str(x) for x in error],
                               'at_most_2pct': guarantee <= F(2, 100),
                               'at_most_5pct': guarantee <= F(5, 100)}
            entries[target] = {'reference': [str(x) for x in ref], **scores}
        result[str(mass)] = {'id': tag, 'threshold_millionths': [rough['last_no'], rough['first_yes']],
                             'old_window': record['old_window']['status'], 'targets': entries,
                             'nominal_flight_millionths': numerical}
    return result


def score_replay():
    raw = (ROOT / 'Schaetzungen.json').read_bytes()
    digest, fname = (ROOT / 'Schaetzungen.sha256').read_text().split()
    assert fname == 'Schaetzungen.json' and sha256(raw).hexdigest() == digest
    geo = independent_light(ROOT / 'basis')
    return evaluate(json.loads(raw), geo), geo


if __name__ == '__main__':
    score, geo = score_replay()
    (ROOT / 'Bewertung.json').write_bytes(as_bytes(score))
    (ROOT / 'Strahlkontrolle.json').write_bytes(as_bytes(geo))
    for mass, row in score.items():
        print(mass, row['threshold_millionths'])
        for target, trial in row['targets'].items():
            for method in ('all_early', 'recorded_early'):
                item = trial[method]
                print(target, method, 'ref', float(F(trial['reference'][0])), 'est', float(F(item['estimate'])),
                      'actual %', float(F(item['observed_relative_error_interval'][1]) * 100), 'max %',
                      float(F(item['max_relative_error']) * 100))
