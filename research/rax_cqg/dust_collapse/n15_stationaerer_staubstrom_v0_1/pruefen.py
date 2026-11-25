"""Run the certificates and compare with the archived finite experiment."""
import argparse
from collections import Counter
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path

import gegenprobe
import paketbreite
import pruefung
import randdichte
import rohform

ROOT=Path(__file__).resolve().parent


def load(name):
    return json.loads((ROOT/name).read_text())


def check(value,name):
    actual=json.loads(json.dumps(value))
    if actual != load(name):
        raise ValueError(f'Abweichende Nachrechnung in {name}')


def summary(rows):
    out={}
    for side in ('links','rechts'):
        counts=Counter()
        for case in rows.values():
            result=case[side]
            counts[result.get('motif','dyadic_cover')]+=1
            if 'dyadic_leaf_depths' in result:
                assert sum(F(n,2**int(d)) for d,n in result['dyadic_leaf_depths'].items())==1
        assert sum(counts.values())==1048
        out[side]=dict(sorted(counts.items()))
    return out


def main():
    if not __debug__:
        raise RuntimeError('Prüfer erfordert aktivierte Assertions, bitte ohne -O ausführen.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--rohform',action='store_true',help='Zusätzlicher Rechenweg für 66 Typen')
    args=parser.parse_args()
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Prüfsumme stimmt nicht für {name}')
    rows=pruefung.census()
    check(rows,'katalog.json')
    check(summary(rows),'gruppen.json')
    check(gegenprobe.run(),'kontrollen.json')
    check(randdichte.run(),'randdichte.json')
    check(paketbreite.run(),'paketbreite.json')
    checkpoints=load('quellen/inputs/checkpoints.json')
    assert len(checkpoints)==60 and all((a['execution'],a['checkpoint_id'])==('NOT_RUN','P3') for a in checkpoints)
    if args.rohform:
        data=rohform.run()
        check(data,'rohform.json')
        print('Rohform reproduziert:', sum(sum(r.values()) for r in data.values()), 'Teilintervalle.')
    print('Beide Uhrfenster, 1048 Typen, Nullatom-Motive, Kontrollhistorien und 15 Schnitte reproduziert. P3: 60 NOT_RUN.')


if __name__=='__main__':
    main()
