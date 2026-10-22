"""Copy frozen inputs to a new, empty destination without touching evidence.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,shutil
from pathlib import Path

HERE=Path(__file__).resolve().parent
ap=argparse.ArgumentParser();ap.add_argument('destination',type=Path);args=ap.parse_args()
dest=args.destination.resolve()
if dest.exists():raise SystemExit('Destination must not exist; archived runs are never overwritten.')
dest.mkdir(parents=True)
shutil.copytree(HERE.parent/'four_landmark_count_covariance/evidence',dest/'four_landmark_count_covariance/evidence',ignore=shutil.ignore_patterns('__pycache__'))
run=dest/'causal_count_fit';run.mkdir()
for name in ['fit.py','controls.py','controls.json','contract.json','run.py','analyze.py','verify.py','freeze.json','PROTOCOL.md','requirements.txt']:
    shutil.copy2(HERE/name,run/name)
print(run)
