"""Create an independent replay copy with all frozen dependencies.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,shutil
from pathlib import Path
HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);a=ap.parse_args();dest=a.destination.resolve()
if dest.exists():raise SystemExit('Destination must not already exist.')
dest.mkdir(parents=True)
for name in ['causal_count_fit','four_landmark_count_covariance/evidence']:
    shutil.copytree(HERE.parent/name,dest/name,ignore=shutil.ignore_patterns('__pycache__'))
run=dest/'stability_followup';run.mkdir()
for name in ['models.py','selection_audit.py','runner.py','analyze.py','controls.py','controls.json','contract.json','PROTOCOL.md','freeze.json','verify_followup.py','requirements.txt']:
    shutil.copy2(HERE/name,run/name)
print(run)
