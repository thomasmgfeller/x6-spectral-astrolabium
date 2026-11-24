"""Reproduce source audit, finite-order inventory and exterior controls."""
import argparse
import hashlib
import json
from pathlib import Path

import anschluss
import ordnungen
import volumenfenster

ROOT=Path(__file__).resolve().parent

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--out',type=Path,default=ROOT/'resultate')
    args=p.parse_args()
    src=ROOT/'quellen'
    origin=json.loads((src/'herkunft.json').read_text())
    for entry in origin['files']:
        data=(src/entry['file']).read_bytes()
        obj=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        if hashlib.sha256(data).hexdigest()!=entry['sha256'] or obj!=entry['git_blob']:
            raise ValueError('Quelldatei '+entry['file'])
    planhash=(ROOT/'pruefplan.sha256').read_text().split()[0]
    if hashlib.sha256((ROOT/'pruefplan.txt').read_bytes()).hexdigest()!=planhash:
        raise ValueError('Prüfplan geändert')
    args.out.mkdir(parents=True,exist_ok=True)
    ordnungen.run(args.out)
    anschluss.run(args.out)
    volumenfenster.run(args.out)
    print('N15-Katalog, klassische Anschlüsse und externe Volumenkontrolle vollständig geprüft.')

if __name__=='__main__':
    main()
