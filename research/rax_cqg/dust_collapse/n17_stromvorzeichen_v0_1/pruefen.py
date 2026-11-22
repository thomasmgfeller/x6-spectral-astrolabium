"""Replay the certified outputs from the distributed data. No network use."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--gegenprobe',action='store_true')
    args=parser.parse_args()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError('Prüfsummenfehler: '+name)
    for src,out in [('nachrechnen.py','ergebnis.json'),('uhrfenster.py','uhrfenster.json')]:
        actual=json.loads(subprocess.check_output([sys.executable,'-B',str(ROOT/src)],cwd=ROOT))
        if actual!=json.loads((ROOT/out).read_text()):
            raise ValueError('Abweichung: '+out)
        print('PASS',out,flush=True)
    movable=actual['stromerhaltend']
    for s,num in [('original',64321536),('transfer',128643072)]:
        assert Q(movable[s]['leading_log_slope_per_clock_halfwidth_squared'])==-Q(1,num)
        assert Q(movable[s]['whole_gap'][1])<0
        assert Q(actual['minimal'][s]['whole_gap'][0])>0
        assert max(map(lambda x:abs(Q(x)),actual['abgeschirmt'][s]['whole_gap']))<Q(4428,10**32)
    if args.gegenprobe:
        for cmd in ('gegenprobe.py','fenster_gegenprobe.py'):
            subprocess.run([sys.executable,'-B',str(ROOT/cmd)],cwd=ROOT,check=True)


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    main()
