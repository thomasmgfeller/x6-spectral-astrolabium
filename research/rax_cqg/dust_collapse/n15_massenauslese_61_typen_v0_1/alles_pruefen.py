"""Verify checksums, recompute all decisions, and replay the witness amplitudes offline."""
from hashlib import sha256
from pathlib import Path
import argparse
import subprocess
import sys

from auswertung import table
ROOT=Path(__file__).resolve().parent

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Use Python without -O.')
    cli=argparse.ArgumentParser()
    cli.add_argument('--suche',action='store_true',help='also rerun the exploratory witness search')
    args=cli.parse_args()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split(maxsplit=1)
        assert sha256((ROOT/name).read_bytes()).hexdigest()==expected,name
    for script in ('pruefen.py','zeugen.py','teilung.py','restzeilen.py'):
        flags=['--search'] if script=='zeugen.py' and args.suche else []
        subprocess.run([sys.executable,'-B',script,*flags],cwd=ROOT,check=True)
    assert table()==(ROOT/'entscheidungen.csv').read_text()
    print('PASS 122/122 rows. Of 61 types, 46 satisfy both uniform bounds and 15 admit counterexamples.')
