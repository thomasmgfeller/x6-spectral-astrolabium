"""Post-run import-order repair; preserve every frozen source byte.

The frozen run.py prepends the older curvature directory to sys.path when
imported. Thus verify.py's subsequent `import selftest` selects the old module.
Preload this package's selftest, restore this directory's import precedence,
then execute the unchanged verifier. No data or tolerances are modified.
"""
import os
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['OMP_NUM_THREADS']='1'
import argparse
from pathlib import Path
import sys
import selftest

HERE=Path(__file__).resolve().parent
assert Path(selftest.__file__).resolve()==HERE/'selftest.py'
sys.path.insert(0,str(HERE))
import verify
assert Path(verify.__file__).resolve()==HERE/'verify.py'


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--archive-only',action='store_true')
    args=parser.parse_args()
    verify.execute(replay=not args.archive_only)
