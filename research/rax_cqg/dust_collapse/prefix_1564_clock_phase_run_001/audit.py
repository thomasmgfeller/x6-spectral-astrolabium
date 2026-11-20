"""Independent consistency checks for the first target run (Python standard library)."""
import hashlib
import json
import math
import sys
from fractions import Fraction as F
from pathlib import Path
from zipfile import ZipFile
from io import BytesIO

HERE = Path(__file__).resolve().parent
LOCK = '8665610801ec890ead3da7659fd55d79a2ed56efd3fe3635b7baf283afbd619a'
BUNDLE = '533bf8bdf41faae749aead7dc1ad2b815ff4cdcdd47d884fa9c604d7b102651b'
def digest(data):
    return hashlib.sha256(data).hexdigest()

def audit():
    archive = next(HERE.glob('*Vorhersage*Pruefpaket.zip'))
    assert digest(archive.read_bytes()) == BUNDLE
    with ZipFile(archive) as package:
        manifest = package.read('registration.json')
        assert digest(manifest) == LOCK
        registered = json.loads(manifest)
        for name, expected in registered['frozen_files_sha256'].items():
            assert digest(package.read(name)) == expected
        with ZipFile(BytesIO(package.read('reference.zip'))) as old:
            baseline = json.loads(old.read('result.json'))
    target = json.loads((HERE/'target_run_001.json').read_text())
    score = json.loads((HERE/'score_001.json').read_text())
    assert target['registration_sha256'] == LOCK == score['registration_sha256']
    assert target['reference_sha256'] == registered['reference_bundle_sha256']
    assert set(target['densities']) == set(score['ratio_intervals']) == set(registered['densities'])
    gram = F(baseline['lower_scalar_gram_eigenvalue'])
    threshold = F(registered['decision']['threshold_ratio'])
    rad_max = F(registered['decision']['new_amplitude_radius_max'])
    old_rad = F(baseline['clock_disk_radius'])
    # Conservative rational majorant for the registered seven-cell error budget.
    full_budget = F(37,1000)*(F(8,32768)+F(1,5000)+6*F(1,2**51)+F(1,10**8))
    assert full_budget < rad_max
    summary = {}
    for i,density in enumerate(registered['densities']):
        rows = target['densities'][density]
        assert set(rows) == set(map(str,registered['end_types']))
        lower,upper = map(F,score['ratio_intervals'][density])
        assert 0 <= lower <= upper
        max_dist_sq = F(0)
        # Recover the scorer's square-root enclosures by exact integer comparisons.
        lows, highs = [], []
        for j,row in rows.items():
            oldrow = baseline['clock_packets_by_end'][j]
            m, M = map(F,oldrow['modulus_bounds'][i])
            assert 0 < m <= M
            rad = F(row['complex_disk_radius'])
            assert full_budget <= rad <= rad_max
            ctrl = list(map(F,row['unmodulated_split_center']))
            src = [F.from_float(float(v)) for v in oldrow['complex_values'][i]]
            assert len(ctrl) == len(src) == 2
            dist_sq = sum((x-y)**2 for x,y in zip(ctrl,src))
            assert dist_sq <= (rad + old_rad)**2
            max_dist_sq = max(max_dist_sq,dist_sq)
            re,im = map(F,row['complex_center'])
            nsq = re*re + im*im
            scale = 10**15
            t = math.isqrt(int(nsq * scale**2))
            lo = F(t,scale)
            hi = lo if lo**2 == nsq else F(t+1,scale)
            assert lo**2 <= nsq <= hi**2
            lows.append((max(0,lo-rad)/M)**2)
            highs.append(((hi+rad)/m)**2)
        assert (lower, upper) == (max(lows),max(highs)*(2-gram)/gram)
        summary[density] = dict(reference_controls_passed=len(rows),
                                max_control_center_distance_approx=math.sqrt(float(max_dist_sq)),
                                lower_ratio=str(lower), upper_ratio=str(upper))
    intervals = [list(map(F,score['ratio_intervals'][d])) for d in registered['densities']]
    expected = 'FAIL' if any(lo>threshold for lo,hi in intervals) else ('PASS' if all(hi<=threshold for lo,hi in intervals) else 'HOLD')
    assert score['status'] == expected
    return dict(verdict=expected, threshold_ratio=str(threshold), amplitude_error_budget_upper_ratio=str(full_budget),
                control_overlap_distance_limit=str(old_rad+rad_max), by_density=summary)

if __name__ == '__main__':
    if not __debug__:
        sys.exit('Run without -O to keep checks enabled.')
    print(json.dumps(audit(),indent=2))
