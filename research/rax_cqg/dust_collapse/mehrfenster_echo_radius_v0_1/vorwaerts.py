"""Generate conservative synthetic clock responses on the three LTB histories."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

from basis import echos
from auslesen import WINDOWS, TIME_UNIT, STAMP

ROOT = Path(__file__).resolve().parent
BASIS = ROOT / 'basis'
# The mapping never goes to the reader. Archive order of the labelled source frames.
CASES = (('C7', F(1, 4)), ('A5', F(1)), ('B2', F(4)))


def collar_bounds():
    # Uniform estimates on the whole tested family for T up to 2, a >= 9.99.
    a_min = F(999, 100)
    family_mass_max = 4
    s_max = F(9, 100)
    assert 2 * family_mass_max / a_min**3 < s_max**2
    factor_min = 1 - F(3, 2) * 2 * s_max
    assert a_min * factor_min > 7 + 3 * (max(WINDOWS) * TIME_UNIT + 2 * STAMP)
    assert factor_min > F(1, 2)**3
    # R'=f^(2/3)-a*t*s'*f^(-1/3), 0 <= -a*s' <= 3*s/2.
    assert 1 + F(3, 2) * 2 * s_max * 2 < 2
    assert F(2 * family_mass_max, 7) < 4


def clock_word(mass, a, angle):
    # Worst case over both the initial angle enclosure and all late stamps.
    min_emit_radius = echos.late_radius(a, mass, STAMP)[0]
    max_emit_radius = echos.late_radius(a, mass, -STAMP)[1]
    states = []
    for w in WINDOWS:
        d_min = w * TIME_UNIT - 2 * STAMP
        d_max = w * TIME_UNIT + 2 * STAMP
        radial_lower = min_emit_radius - 3 * d_max
        assert radial_lower > 7 and d_min > 0
        if max_emit_radius * angle[1] <= d_min:
            states.append('Y')
        elif radial_lower * angle[0] > d_max:
            states.append('N')
        else:
            states.append('?')
    return ''.join(states)


def measurements():
    collar_bounds()
    net = json.loads((BASIS / 'Netzaufnahmen.json').read_bytes())
    archive = json.loads((BASIS / 'Echoaufnahmen.json').read_bytes())
    frames = []
    for (tag, mass), old in zip(CASES, archive, strict=True):
        data = net[str(mass)]
        assert dict(old['echo_ticks']) == {
            partner: data['ticks']['|'.join(sorted(('D', partner)))] for partner, _ in old['echo_ticks']}
        j = echos.locate([v == '1' for v in old['initial_positive']])
        assert j == echos.locate([v == '1' for v in old['final_positive']]) == 492
        a = F(13 * j, 640)
        pair = 'B|D'  # physical channel designated by the archived early experiment
        lo, hi = data['bounds'][pair]
        angle = (echos.decode(lo, a / 10, 0)[0], echos.decode(hi, a / 10, 0)[1])
        assert echos.contained(angle)
        word = clock_word(mass, a, angle)
        frames.append({'id': tag, 'initial_positive': old['initial_positive'],
                       'final_positive': old['final_positive'], 'ticks': data['ticks'],
                       'tick_ranges': data['bounds'], 'observed_pair': pair, 'windows': word})
    return sorted(frames, key=lambda x: x['id'])


def as_bytes(obj):
    return (json.dumps(obj, sort_keys=True, indent=2, ensure_ascii=False) + '\n').encode()


if __name__ == '__main__':
    print(as_bytes(measurements()).decode(), end='')
