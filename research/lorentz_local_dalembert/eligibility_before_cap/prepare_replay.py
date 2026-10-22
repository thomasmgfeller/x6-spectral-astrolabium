"""Make a fresh replay directory; never overwrite published evidence.
SPDX-License-Identifier: Apache-2.0
"""
import argparse
import shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser(); ap.add_argument('destination',type=Path); a=ap.parse_args()
dest=a.destination.resolve()
if dest.exists(): raise SystemExit('Destination must not exist.')
dest.mkdir(parents=True)
source=HERE.parent/'four_landmark_count_covariance/evidence'
shutil.copytree(source,dest/'four_landmark_count_covariance/evidence',ignore=shutil.ignore_patterns('__pycache__'))
# Historical data allow duplicate-hash exclusion in the post-run audit.
for name in ['causal_count_fit/results','stability_followup/conditional']:
    shutil.copytree(HERE.parent/name,dest/name,ignore=shutil.ignore_patterns('__pycache__'))
run=dest/'eligibility_before_cap'; run.mkdir()
for name in ['eb_common.py','selector.py','simulation_pair.py','runner.py','analyze.py',
             'controls.py','controls.json','contract.json','requirements.txt','PROTOCOL.md',
             'freeze.json','preflight-import-abort.zip','preflight-import-abort.log',
             'PRE_DATA_CORRECTION.json','verify.py']:
    shutil.copy2(HERE/name,run/name)
print(run)
