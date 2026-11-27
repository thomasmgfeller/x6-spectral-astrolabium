"""Standardbibliotheks-Reproduktion des N22-Quantenpixeltests. Python >= 3.10."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT=Path(__file__).resolve().parent


def run(script, expected=None, args=()):
    out=subprocess.check_output([sys.executable,'-B',str(ROOT/script),*map(str,args)],cwd=ROOT)
    if expected is not None and out != (ROOT/expected).read_bytes():
        raise ValueError(f'Abweichende Ausgabe für {script}')
    print('PASS',script)


def main(sympy):
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest, name=line.split('  ',1)
        if hashlib.sha256((ROOT/name).read_bytes()).hexdigest()!=digest:
            raise ValueError(f'Prüfsummenfehler in {name}')
    data=ROOT/'eingaben'
    assert (ROOT/'vergleich/Vergleichspaar.json').read_bytes()==(data/'Vergleichspaar.json').read_bytes()
    assert (ROOT/'gewichte/quellen/weight_certificates.json').read_bytes()==(data/'weight_certificates.json').read_bytes()
    vac=json.loads((data/'Nullkontrolle.json').read_bytes())
    assert vac['signed_flux_Q']==vac['residence_proxy_B']=='0'
    assert vac['physical_P3']=={'count':60,'status':'NOT_RUN'} and vac['independent_positive_mass_standard'] is None
    run('gewichte/pruefen.py','gewichte/Ergebnisse.json')
    run('wirkung/wirkungszeuge.py','wirkung/Ergebnisse.json',
        [data/n for n in ('Vergleichspaar.json','Kugelzeuge.json','Ortskoordinaten.json')])
    run('vergleich/fensterkontrolle.py','vergleich/Ergebnis.json')
    run('info/pruefen.py')
    run('radiustest.py','Radiuspruefung.json')
    run('zeigerprobe.py','Zeigerkontrolle.json')
    if sympy:
        run('entropie.py')
    print('Acht physische Pilotradien und 60 P3-Punkte NOT_RUN.')


if __name__=='__main__':
    if not __debug__: raise RuntimeError('Ohne -O ausführen.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mit-sympy',action='store_true',help='zusätzlich komplexe Produkt-Gram-Matrizen prüfen')
    main(parser.parse_args().mit_sympy)
