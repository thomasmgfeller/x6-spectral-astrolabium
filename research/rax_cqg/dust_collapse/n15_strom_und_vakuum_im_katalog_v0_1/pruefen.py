"""Run both rational verifications with Python 3.10 or later."""
import hashlib
import json
from pathlib import Path
import sys

import katalog
import gegenprobe
import trennnachweis
import uhrpulse

ROOT=Path(__file__).resolve().parent


def run():
    assert (ROOT/'Pruefplan.sha256').read_text().split()[0]==hashlib.sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest()
    for name,item in json.loads((ROOT/'Herkunft.json').read_text())['inputs'].items():
        data=(ROOT/name).read_bytes()
        assert hashlib.sha256(data).hexdigest()==item['sha256']
        assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['blob']
    screening=katalog.run()
    gegenprobe.check_masks(screening['candidates'])
    prefixes=katalog.sharper_screen(screening['candidates'])
    ratios=katalog.ratio_screen(prefixes['remaining'])
    certificates=trennnachweis.run(ratios['remaining'])
    count=sum(certificates.values())
    assert gegenprobe.check_tree()==count==136
    assert sum(map(len,screening['candidates'].values()))==len(prefixes['excluded'])+len(ratios['excluded'])+sum(map(len,ratios['remaining'].values()))
    return {'readout':uhrpulse.run(),'catalogue_counts':screening['counts'],'first_screen_candidates':screening['candidates'],
            'density_moment_exclusions':prefixes['excluded'],'clock_ratio_exclusions':ratios['excluded'],
            'final_masks':ratios['remaining'],'exact_simplex_leaves':certificates,
            'remaining_quiet_masks_under_contract':0,'physical_status':katalog.n15.physical_status()}


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Bitte Python ohne -O starten.')
    actual=json.dumps(run(),ensure_ascii=False,indent=2,sort_keys=True,allow_nan=False)+'\n'
    if sys.argv[1:]==['--json']:
        print(actual,end='')
    elif not sys.argv[1:]:
        assert actual==(ROOT/'Ergebnisse.json').read_text()
        print('PASS: Uhrpulse, stationäre Zertifikate und vollständiger bedingter Katalogausschluss.')
        print('1048 Typen, 134144 Belegungsmuster, 136 zweifach geprüfte Trennzellen. Physische P3-Prüfpunkte: 60 x NOT_RUN.')
    else:
        raise SystemExit('Aufruf: python -B pruefen.py [--json]')
