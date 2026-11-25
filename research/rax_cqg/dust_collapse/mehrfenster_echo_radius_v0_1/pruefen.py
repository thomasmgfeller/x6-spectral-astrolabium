"""Verify source bytes, run the isolated reader and reproduce the two controls."""
from copy import deepcopy
from fractions import Fraction as F
from hashlib import sha256
from math import isclose
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import shutil
import subprocess
import sys

from auslesen import WINDOWS, TIME_UNIT, predict, read
from bewerten import score_replay
from vorwaerts import ROOT, as_bytes, measurements


def negative_controls(frame):
    mask = '0' * 641
    assert read({**frame, 'initial_positive': mask, 'final_positive': mask})['status'] == 'VACUUM'
    assert read({**frame, 'final_positive': mask})['status'] == 'OPEN_MATERIAL'
    assert read({**frame, 'windows': '?' * len(WINDOWS)})['status'] == 'OPEN'
    assert read({**frame, 'windows': 'N' * len(WINDOWS)})['status'] == 'ONE_SIDED'
    assert read({**frame, 'windows': 'Y' + '?' * (len(WINDOWS) - 2) + 'N'})['status'] == 'INCONSISTENT'
    assert read({**frame, 'observed_pair': 'B|K'})['status'] == 'OPEN_PAIR'
    ambiguous = deepcopy(frame)
    ambiguous['tick_ranges']['B|K'] = ambiguous['tick_ranges']['B|D']
    assert read(ambiguous)['status'] == 'OPEN_PAIR'
    try:
        read({**frame, 'reference_radius': '9.0'})
    except ValueError:
        pass
    else:
        raise AssertionError('hidden key accepted')


def compare_data(actual, expected):
    if isinstance(actual, dict):
        assert set(actual) == set(expected)
        for key, value in actual.items():
            compare_data(value, expected[key])
    elif isinstance(actual, float):
        assert isclose(actual, expected, rel_tol=1e-12, abs_tol=2e-14)
    else:
        assert actual == expected


def verify():
    for line in (ROOT / 'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ', 1)
        assert sha256((ROOT / name).read_bytes()).hexdigest() == digest, name
    for name in ('Pruefplan', 'Fensterkonvention'):
        saved_hash, file_name = (ROOT / (name + '.sha256')).read_text().split()
        assert sha256((ROOT / file_name).read_bytes()).hexdigest() == saved_hash
    data = measurements()
    assert (ROOT / 'Fensteraufnahmen.json').read_bytes() == as_bytes(data)
    with TemporaryDirectory() as tmp:
        for filename in ('auslesen.py', 'Fensteraufnahmen.json'):
            shutil.copyfile(ROOT / filename, Path(tmp) / filename)
        code = ("import json,runpy; r=runpy.run_path('auslesen.py');"
                "print(json.dumps(r['predict'](json.load(open('Fensteraufnahmen.json'))),"
                "sort_keys=True,indent=2,ensure_ascii=False))")
        prediction = subprocess.check_output([sys.executable, '-I', '-B', '-c', code], cwd=tmp)
        assert prediction == (ROOT / 'Schaetzungen.json').read_bytes()
    negative_controls(data[0])
    scores, geo = score_replay()
    compare_data(scores, json.loads((ROOT / 'Bewertung.json').read_bytes()))
    compare_data(geo, json.loads((ROOT / 'Strahlkontrolle.json').read_bytes()))
    # Old single window reproduces PR 382's conservative late channel.
    assert [scores[m]['old_window'] for m in ('1/4', '1', '4')] == ['ONE_SIDED', 'OPEN', 'ONE_SIDED']
    by_id = {f['id']: f for f in data}
    assert [by_id[scores[m]['id']]['windows'][WINDOWS.index(1000)] for m in ('1/4', '1', '4')] == ['N','?','Y']
    for m, result in scores.items():
        frame = by_id[result['id']]
        assert len(frame['windows']) == 501
        for target in result['targets'].values():
            for mode in ('all_early', 'recorded_early'):
                assert target[mode]['at_most_2pct'] and target[mode]['at_most_5pct']
        # Any individual admissible early reading at either endpoint yields
        # tighter bounds. Monotonicity of the two calibration endpoints covers the interior.
        all_errors = read(frame)
        for index in (0, 1):
            worst_ticks = {pair: bounds[index] for pair, bounds in frame['tick_ranges'].items()}
            actual = read({**frame, 'ticks': worst_ticks}, all_early=False)
            for target in ('material', 'support'):
                assert F(all_errors[target]['lower']) <= F(actual[target]['lower'])
                assert F(actual[target]['upper']) <= F(all_errors[target]['upper'])
    print('PASS: 3 LTB histories, 1503 windows, isolated reader, two target surfaces, independent light propagation.')
    print('Physical P3: 60 NOT_RUN.')


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Run Python without optimisation (-O).')
    verify()
