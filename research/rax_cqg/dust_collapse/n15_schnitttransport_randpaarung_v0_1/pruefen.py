"""Offline replay of the cut transport, its conditional information loss and the two placements."""
import argparse
import hashlib
import json
import math
from fractions import Fraction as F
from transport import ROOT, exact
from paarung import run as prove

def load(name):
    return json.loads((ROOT/name).read_bytes())

def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def verify_exact():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,name=line.split('  ',1)
        assert digest(name)==expected,name
    for stem in ('pruefplan','massplan','quadraturplan','rangplan'):
        expected,name=(ROOT/(stem+'.sha256')).read_text().split()
        assert name==stem+'.txt' and digest(name)==expected
    for name,source in load('herkunft.json')['dateien'].items():
        assert digest('quellen/'+name)==source['sha256'],name
    assert exact()==load('transport.json')
    assert prove()==load('paarung.json')
    gates=load('quellen/p3.json')
    assert len(gates)==60 and all(x['execution']=='NOT_RUN' for x in gates)
    print('PASS  12 Polynomidentitaeten, 360 Wirkungsvergleiche, Dichteintervalle, Rang und Nullrichtung. P3: 60 NOT_RUN.',flush=True)

def numerical():
    from integration import run
    rows=run()
    stored=load('integration.json')
    reference=load('quellen/rechnung.json')
    assert set(rows)==set(stored)
    for key, centres in rows.items():
        assert set(centres)=={'1/4','1/8'}
        cut,mode,rule=key.split('|')
        for rho,row in centres.items():
            target=stored[key][rho]
            assert set(target)==set(row)
            for field in set(row)-{'amplituden'}:
                assert math.isclose(row[field],target[field],abs_tol=2e-9,rel_tol=1e-10),(key,rho,field)
            expected=reference[rho+'|positive|1']['gauss5x10']
            assert len(row['amplituden'])==11
            for arm,parts in row['amplituden'].items():
                z=complex(*parts)
                assert abs(z-complex(*target['amplituden'][arm]))<1e-11,(key,rho,arm)
                if mode=='transport' and rule=='gauss5x10':
                    assert abs(z-complex(*expected['eleven_amplitudes'][arm]))<1e-13
            if mode=='transport':
                assert abs(row['masse']-expected['calibrated'])<2e-9
            if mode=='gemeinsam':
                diff=row['masse']-expected['calibrated']
                assert .003<diff<.017
                unchanged=[a for a in row['amplituden'] if not a.startswith('6')]
                standard=rows['11|transport|'+rule][rho]['amplituden']
                for arm in unchanged:
                    assert abs(complex(*row['amplituden'][arm])-complex(*standard[arm]))<1e-13
            if mode=='vergessen':
                assert abs(row['masse']-expected['calibrated'])>.12
            if rule=='gauss5x10':
                cc=rows[cut+'|'+mode+'|cc5x9'][rho]
                assert abs(cc['masse']-row['masse'])<2e-9
    # Independent null-packet integral using one-dimensional Gauss-Legendre on q12.
    import numpy as np
    from numpy.polynomial.legendre import leggauss
    q=load('paarung.json')
    x,w=leggauss(32)
    lam=sum(float(F(p)) for p in q['frequenzen_pro_v']['4+'])/2
    wave=np.sqrt(3.)*x
    assert abs(w @ wave/2)<1e-15 and abs(w @ (wave*wave)/2-1)<1e-14
    amplitude=abs(w @ (wave*np.exp(1j*lam*x))/2)
    a,b=map(F,q['normierte_nullrichtung_betrag_4plus'])
    assert float(a)<amplitude<float(b)
    print('PASS  Zwei Quadraturen, 32 Schnitt-/Dichte-/Modusvergleiche mit je elf komplexen Amplituden; konditionierte Nullwelle.',flush=True)

if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Bitte ohne -O ausführen.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--nur-exakt',action='store_true')
    args=parser.parse_args()
    verify_exact()
    if not args.nur_exakt:numerical()
