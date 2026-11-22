"""Offline reproduction. Use --nur-exakt if NumPy is unavailable."""
import argparse
import cmath
import hashlib
import json
import math
from fractions import Fraction as Q
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

import ordnung
import schranken

ROOT=Path(__file__).resolve().parent

def load(name):
    return json.loads((ROOT/name).read_bytes())

def data_json(data):
    return json.dumps(data,indent=2,sort_keys=True,default=str,ensure_ascii=False)+'\n'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def compare(a,b,where='root'):
    if isinstance(a,dict):
        assert a.keys()==b.keys(),where
        for k,v in a.items():compare(v,b[k],where+'/'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),where
        for j,v in enumerate(a):compare(v,b[j],where+str(j))
    elif isinstance(a,float):
        # Phases are differenced twice. Rounding scales like 1/h^2.
        assert math.isclose(a,b,abs_tol=1e-8,rel_tol=1e-9),(where,a,b)
    else:assert a==b,(where,a,b)

def certified():
    for p,d in load('herkunft.json')['files'].items():assert digest(ROOT/p)==d['sha256']
    for name in ('pruefplan','ergaenzung'):
        d,p=(ROOT/(name+'.sha256')).read_text().split()
        assert digest(ROOT/p)==d
    ref=load('quellen/referenz.json')
    records=load('quellen/p3.json')
    assert len(records)==60 and all(r['execution']=='NOT_RUN' and r['checkpoint_id']=='P3' for r in records)
    bounds=schranken.phase_bounds(ref)
    rep={r:ref['repaired_chain'][r]['all_relative_lobe_phases']['relative_upper'] for r in bounds}
    assert all(Q(x)<Q(295,10**7) for x in rep.values())
    gain=schranken.phase_gain(Q(1,8))
    return {'geometry':ordnung.exact(),'two_histories':ordnung.discrete_control(),
            'shifted_kernel_bounds':bounds,'insertion_relative_bounds':rep,
            'phase_error_gain_at_h_1_over_8':gain,'mass_error_at_phase_noise_1e-7':gain*Q(1,10**7),
            'physical_P3':{'NOT_RUN':len(records)}}

def numerical():
    import kern
    out={}
    for rho in (.125,.25):
        key=str(Q(rho))
        levels={}
        for n,o in ((3,4),(4,8),(5,10)):
            levels[f'{n}x{o}']=kern.statistics(n,o,rho)
        best=levels['5x10']
        for k in ('all_clock_mass','ordinary_mass','weak_mass_real','finite_pointer'):
            assert abs(best[k]-levels['4x8'][k])<1e-8
        finite={}
        for denom in (8,16,32,64,128):
            finite[str(denom)]=kern.finite_difference(4,8,rho,1/denom,record=(denom==8))
        high=kern.finite_difference(5,10,rho,1/8)
        assert abs(best['all_clock_mass']-finite['128']['all_clock_mass'])<1e-7
        assert abs(best['ordinary_mass']-finite['128']['hybrid_mass'])<1e-7
        assert abs(high['all_clock_mass']-finite['8']['all_clock_mass'])<1e-8
        assert abs(best['all_clock_mass']/4-1)<.02
        # Compare direct total-order contraction and delayed contraction. Shared frozen
        # measure, but separate incidence enumeration and summation order.
        residuals={}
        for tag,shifts in ((0,(0,0)),(.25,(0,0)),(-.25,(0,0)),(0,(.125,-.125)),(0,(0,0,.125,-.125))):
            kw=dict(tag=tag,shifts=shifts)
            left=kern.integrate(4,8,rho,stream=False,**kw)
            right=kern.integrate(4,8,rho,stream=True,**kw)
            diff=float(abs(left-right)/abs(left))
            assert diff<5e-12
            residuals[str((tag,shifts))]=diff
        assert len(finite["8"]["source_phase_and_relative_modulus"])==17
        const_arms=[kern.integrate(4,8,rho,stream=True,constant_phase=x) for x in (1.,-1.)]
        for phase,arm in zip((1.,-1.),const_arms):
            assert abs(arm/cmath.exp(1j*phase)-kern.integrate(4,8,rho))<1e-12
        no_cross=kern.integrate(4,8,rho,stream=True,drop_cross=True)
        base=complex(*best['unshifted_complex'])
        raw=abs(no_cross-base)/abs(base)
        assert raw>1e-3
        out[key]={'quadrature_levels':levels,'finite_steps_reciprocal':finite,'fine_grid_at_h_1_over_8':high,
                  'gluing_residuals':residuals,'dropping_cross_pairs_relative_complex_change':float(raw)}
    return out

def upstream_replay():
    with tempfile.TemporaryDirectory() as dest, zipfile.ZipFile(ROOT/'quellen/pr354.zip') as z:
        assert z.testzip() is None
        z.extractall(dest)
        p=Path(dest)/'Skalar_und_Traeger'
        assert (p/'ergebnis.json').read_bytes()==(ROOT/'quellen/referenz.json').read_bytes()
        subprocess.run([sys.executable,'-B','pruefen.py'],cwd=p,check=True,stdout=subprocess.DEVNULL)

def main():
    if not __debug__:raise RuntimeError('Python ohne -O verwenden.')
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--nur-exakt',action='store_true')
    parser.add_argument('--emit',action='store_true',help='Ergebnisse in diesem Verzeichnis erzeugen')
    args=parser.parse_args()
    if not args.emit:
        for line in (ROOT/'SHA256SUMS').read_text().splitlines():
            d,p=line.split(maxsplit=1);assert digest(ROOT/p)==d,p
    upstream_replay()
    exact=data_json(certified())
    if args.emit:(ROOT/'exakt.json').write_text(exact)
    else:assert exact==(ROOT/'exakt.json').read_text()
    print('PASS: PR 354, Quellen, Schnittwirkungsidentität, Rang 4, Zwei-Historien-Kontrolle, Amplitudenschranken und 15 Phaseneinstellungen.')
    if not args.nur_exakt:
        results=numerical()
        if args.emit:(ROOT/'quadratur.json').write_text(data_json(results))
        else:compare(results,load('quadratur.json'))
        for key,record in results.items():
            print(key,'M(Uhrverschiebungen, h=1/8) =',round(record['fine_grid_at_h_1_over_8']['all_clock_mass'],9))
        print('PASS: Produktquadraturen, verklebte Amplituden und getrennte Auswertung der Wirkungsableitungen.')
    print('Physischer P3-Status: 60 x NOT_RUN.')

if __name__=='__main__':main()
