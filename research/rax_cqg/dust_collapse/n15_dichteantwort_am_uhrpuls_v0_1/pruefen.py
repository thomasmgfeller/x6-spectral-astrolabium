"""Offline repeat of the finite identities, probability enclosures and source quadratures."""
import argparse
import cmath
from fractions import Fraction as F
import hashlib
import json
import math
from randquelle import ROOT,run as algebra
from intensitaet import run as certify
from vorrecord import run as past_record,at_q
from zellkontrolle import exact as cell_identity

def load(name):
    return json.loads((ROOT/name).read_bytes())

def digest(path):
    return hashlib.sha256((ROOT/path).read_bytes()).hexdigest()

def check_exact():
    for line in (ROOT/'SHA256SUMS').read_text().splitlines():
        expected,path=line.split('  ',1)
        assert digest(path)==expected,path
    for prefix in ('pruefplan','ergaenzung','kontrollplan','zellplan'):
        expected,p=(ROOT/(prefix+'.sha256')).read_text().split()
        assert p==prefix+'.txt' and digest(p)==expected
    for name,rec in load('herkunft.json')['quellen'].items():
        assert digest('quellen/'+name)==rec['sha256']
    rows=load('quellen/p3.json')
    assert len(rows)==60 and all(r['execution']=='NOT_RUN' for r in rows)
    assert algebra()==load('quelle.json') and cell_identity()==load('zellkontrolle.json')['algebra']
    # The Leibniz boundary response agrees with direct differentiation of every tested polynomial moment.
    for f in (F(7,64),F(1,8),F(9,64)):
        for scale in (F(1,4),F(1),F(7,2)):
            a,b=scale*F(99,100),scale*F(101,100)
            for n in range(13):
                derivative=f**n*(b**(n+1)-a**(n+1))
                assert derivative==b*(b*f)**n-a*(a*f)**n
    assert certify()==load('intensitaet.json')
    assert past_record()==load('vorrecord.json')
    for sign in (1,-1):
        a,b,den=at_q(F(0),sign)
        assert a-b==0 and den>0
    print('PASS  Eingangsprofile, mitbewegte Grenzen, zwei Intensitaetseinschluesse je Zentrum, vergangener Traeger und 60 P3 NOT_RUN.',flush=True)

def close(a,b,eps=2e-10):
    if isinstance(b,dict):
        assert a.keys()==b.keys()
        for k in b:close(a[k],b[k],eps)
    elif isinstance(b,list):
        assert len(a)==len(b)
        for x,y in zip(a,b):close(x,y,eps)
    elif isinstance(b,(float,int)):
        assert math.isclose(a,b,abs_tol=eps,rel_tol=eps),(a,b)
    else:assert a==b

def check_numerical():
    from auslese import run as sources
    from kontrollen import run as independent
    from zellkontrolle import run as control
    rows=sources()
    close(rows,load('auslese.json'))
    base=load('quellen/integration360.json')
    for mass in ('0','1/4','1','4'):
        for rho in ('1/8','1/4'):
            for alpha,old in [('0','transport'),('1','gemeinsam')]:
                k=rho+'|'+alpha
                fine=rows[mass+'|gauss5x10'][k]
                cc=rows[mass+'|cc5x9'][k]
                assert abs(fine['dichtedifferenz']-cc['dichtedifferenz'])<2e-10
                if mass=='0':
                    assert max(abs(fine['asymmetrie']),abs(fine['dichtedifferenz']))<1e-12
                if mass=='1':
                    for rule in ('gauss5x10','cc5x9'):
                        prior=base['11|'+old+'|'+rule][rho]['amplituden']
                        sub=rows['1|'+rule][k]['amplituden']
                        for arm,name in [('null','0'),('plus','6+'),('minus','6-')]:
                            assert abs(complex(*sub[arm]['ref'])-complex(*prior[name]))<1e-12
                    lo,hi=map(F,load('intensitaet.json')[k]['asymmetrie'])
                    assert lo<fine['asymmetrie']<hi
    print('PASS  Zwei Quadraturen, 32 Dosis-/Dichte-/Vorschrift-/Gitterfaelle; PR-360-Referenzarme.',flush=True)
    extra=control()
    close(extra,load('zellkontrolle.json'))
    for k,z in extra['numerik'].items():
        _,rule,site=k.split('|')
        for pair,v in z.items():
            assert abs(v['dichtedifferenz']-extra['numerik']['1|cc5x9|'+site][pair]['dichtedifferenz'])<2e-10
            if site=='11' and not pair.endswith('|2'):close(v,rows['1|'+rule][pair])
    checks=independent(rows);close(checks,load('kontrollen.json'))
    for arm in ('plus','minus'):
        lo,hi=map(F,load('vorrecord.json')[arm])
        assert all(lo<grid[arm]['verbotener_anteil']<hi for grid in checks['direkt'].values())
    # Direct numerical check of the moving-boundary term for the exponential integrand.
    for c in (.0,-.67,1.72):
        def integral(f):
            a,b=.99*f,1.01*f
            return b-a if c==0 else (cmath.exp(1j*c*b)-cmath.exp(1j*c*a))/(1j*c)
        f=.13;step=.0001
        boundary=1.01*cmath.exp(1j*c*1.01*f)-.99*cmath.exp(1j*c*.99*f)
        assert abs((integral(f+step)-integral(f-step))/(2*step)-boundary)<1e-9
    print('PASS  Zweite Eingangsquelle, kompensierte Zellen, separate Armnormierung und direkte Traegerintegration.',flush=True)

if __name__=='__main__':
    if not __debug__:raise SystemExit('Bitte ohne -O aufrufen.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--nur-exakt',action='store_true')
    args=parser.parse_args()
    check_exact()
    if not args.nur_exakt:check_numerical()
