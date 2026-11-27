"""Replay the original N22 enumeration and the two archived rounds of B+ exclusions."""
import argparse
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from pruefen import ROOT, PINS, unpack


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--jobs',type=int,default=2,help='Anzahl Bäume für die beiden B+-Prüfungen.')
    args = parser.parse_args()
    if not __debug__ or not 1<=args.jobs<=16:
        raise RuntimeError('Python ohne -O mit 1 bis 16 Jobs verwenden.')
    with TemporaryDirectory() as directory:
        first,second,third = (Path(directory)/s for s in ('n22','zweige','nachfolger'))
        unpack(ROOT/'basis/Nachfolger.zip',PINS[0],third)
        unpack(third/'basis/Vorstudie.zip',PINS[1],second)
        unpack(second/'basis/N22.zip',PINS[2],first)
        for stage,options in [(first,[]),(second,['--jobs',str(args.jobs)]),(third,['--jobs',str(args.jobs)])]:
            subprocess.run(['sha256sum','-c','--quiet','SHA256SUMS'],cwd=stage,check=True)
            print(stage.name,flush=True)
            subprocess.run([sys.executable,'-B','pruefen.py',*options],cwd=stage,check=True)
    print('PASS: alle drei Vorläufe aus den festgelegten Archiven reproduziert.')

if __name__=='__main__':
    main()
