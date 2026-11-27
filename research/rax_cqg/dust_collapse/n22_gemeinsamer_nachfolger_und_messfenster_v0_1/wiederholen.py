"""Reproduce every published window and the resulting infimum interval offline."""
import argparse
import json
from pathlib import Path
import subprocess
import sys

from schranken import ROOT, derive

parser=argparse.ArgumentParser()
parser.add_argument('--jobs',type=int,default=4)
args=parser.parse_args()
if not __debug__ or args.jobs<1:
    raise ValueError('Python ohne -O und positive Parallelität erforderlich.')
summary,table=derive()
assert summary==json.loads((ROOT/'Schranken.json').read_text())
assert table==(ROOT/'Fenstervergleich.tsv').read_text()
for h in summary['halfwidths']:
    subprocess.run([sys.executable,'-B',str(ROOT/'pruefen.py'),'--jobs',str(args.jobs),'--halbbreite',h],
                   check=True)
print('Halbbreiten und Zeugenintervalle reproduziert.')
