"""Einheitlicher Offline-Lauf für das CST-DUST-Prüfpaket. Python 3.10+."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def check_hashes():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest, name = line.split('  ',1)
        actual = hashlib.sha256((ROOT/name).read_bytes()).hexdigest()
        if actual != digest:
            raise ValueError(f'Abweichende Prüfsumme in {name}')
    for name,digest in [('Vergleichspaar.json','c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f'),
                        ('Ortskoordinaten.json','a8bdf817687174d3c47d6ebf105974b41008a9037555e66da62a581c9f9601f4')]:
        for src in ROOT.rglob(name):
            assert hashlib.sha256(src.read_bytes()).hexdigest() == digest, src


def execute(folder,script,*args,snapshot=None):
    out=subprocess.check_output([sys.executable,'-B',script,*args],cwd=ROOT/folder)
    if snapshot is not None and out != (ROOT/folder/snapshot).read_bytes():
        raise ValueError(f'{folder}/{script} reproduziert {snapshot} nicht')
    print(f'PASS {folder}/{script}',flush=True)


def main():
    if not __debug__:
        raise RuntimeError('Ohne -O ausführen')
    check_hashes()
    plan = json.loads((ROOT/'eingaben/P3_Zulassung.json').read_bytes())
    assert plan['execution']=='NOT_RUN' and plan['decision']=='HOLD_NOT_ELIGIBLE'
    for path,file,ref in [('schalen','kontrolle.py','Ergebnisse.json'),
                          ('schalen','gleiche_seiten.py','Gegenzeuge.json'),
                          ('schalen','weitere_kontrolle.py','Vierte_Kugel.json')]:
        execute(path,file,snapshot=ref)
    for path in ['messfenster','leere_sonden','massenkontrolle','positive_probe_next']:
        execute(path,'pruefen.py')
    execute('helper_audit_next','gegenpruefen.py','../positive_probe_next',snapshot='Kontrollregister.json')
    execute('positive_probe_next','gegenprobe.py')
    execute('geom_terminal_next','pruefen_zweit.py')
    summary=json.loads((ROOT/'positive_probe_next/Ergebnisse.json').read_text())
    assert {key:value['cases'] for key,value in summary.items()} == {
        'heavy_3':{'AUSGESCHLOSSEN':474},
        'heavy_4,5':{'AUSGESCHLOSSEN':566},
        'light_3,4,5':{'AUSGESCHLOSSEN':474}}
    print('1 514 Helferfälle ausgeschlossen. Acht physische Pilotradien und 60 P3-Punkte NOT_RUN.')


if __name__=='__main__':
    main()
