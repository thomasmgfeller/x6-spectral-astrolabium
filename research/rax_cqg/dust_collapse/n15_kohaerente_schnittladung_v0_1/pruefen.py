"""Replay the exact certificates and optional separate quadrature within the archive."""
import argparse
from fractions import Fraction as F
from pathlib import Path
import hashlib
import json
import math
import sys

ROOT=Path(__file__).resolve().parent
import zertifikat
import verweildauer


def archived(name):
    return json.loads((ROOT/name).read_text())


def run(numerical):
    if not __debug__:
        raise ValueError('Ohne -O ausführen, damit alle Gleichungen geprüft werden.')
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        digest,fn=line.split('  ',1)
        if hashlib.sha256((ROOT/fn).read_bytes()).hexdigest()!=digest:
            raise ValueError('Datei weicht ab: '+fn)
    cert=zertifikat.run()
    assert cert==archived('schranken.json')
    material=verweildauer.run(cert['levels'])
    assert json.loads(json.dumps(material))==archived('materialtest.json')
    checkpoints=archived('basis/quellen/inputs/checkpoints.json')
    assert len(checkpoints)==60 and all(c['checkpoint_id']=='P3' and c['execution']=='NOT_RUN' for c in checkpoints)
    q=archived('quadratur.json')
    if numerical:
        import quadratur
        q=quadratur.run()
    ref=archived('quadratur.json')
    for level,rows in q.items():
        bound=cert['levels'][level]
        last='4,5,6,11,12,13,14'
        assert F(bound['cuts'][last]['relative_lower'])>0
        assert len(rows)==2 and {r['order'] for r in rows}=={3,4}
        for row,reference in zip(rows,ref[level]):
            assert row['modulus_Z_per_measure']>=float(F(bound['amplitude_modulus_lower']))-1e-14
            assert row['max_volume_face_gap']<1e-17
            assert math.dist(row['coherent_inlet'],reference['coherent_inlet'])<1e-12
            assert len(row['cuts'])==15
            for cut,vals in row['cuts'].items():
                target=reference['cuts'][cut]
                v=complex(*vals['volume_relative'])
                b=complex(*vals['face_relative'])
                assert abs(v-b)<1e-17 and abs(v-complex(*target['volume_relative']))<1e-17
                exact=bound['cuts'][cut]
                assert float(F(exact['relative_lower']))<=abs(v)<=float(F(exact['relative_upper']))
                if vals['finite_relative'] is not None:
                    h=complex(*vals['finite_relative'])
                    assert abs(h)<=float(F(bound['finite_pulse_ratio_error_max']))
                    assert abs(h-complex(*target['finite_relative']))<1e-11
        for key in rows[0]['cuts']:
            assert abs(complex(*rows[0]['cuts'][key]['volume_relative'])-
                       complex(*rows[1]['cuts'][key]['volume_relative']))<1e-17
    print('PASS · vier Breiten, je 15 Schnitte, Ward-Randterm, endliche Quelle und sechs markierte Pfade.')
    if numerical:
        print('Separate Volumen- und Flächenquadratur auf beiden Auflösungen neu berechnet.')
    print('P3: 60 NOT_RUN.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--quadratur',action='store_true',help='Numerische Gegenrechnung mit NumPy wiederholen')
    run(parser.parse_args().quadratur)
