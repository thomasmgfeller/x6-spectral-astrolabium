"""Deterministic replay of PR 380, plus an interval audit of the equal-prefactor phase sum."""
import csv
import hashlib
import io
import json
import sys
from fractions import Fraction as F
from math import factorial
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = ROOT / 'quelle'
sys.path.insert(0, str(BASE))
from basis.intervall import Box, SCALE, box

def snapshot(clock, w, coefficients, gradient, geom):
    full = box(geom) - (19*sum(w.values(),box(0)) + sum(
        (b*w[j]*(clock[j]-clock[i]).square() for (i,j),b in coefficients.items()),box(0)))/38
    # Positive free interior events solve their density equations on these partial saddles.
    collar_sum = sum((w[j]*(19+sum((b*(clock[j]-clock[i]).square()
                     for (i,k),b in coefficients.items() if k==j),box(0)))
                     for j in (0,1,2,3,7,8,9,10)),box(0))
    action = full.intersection(box(geom)-collar_sum/38)
    assert action is not None
    return action, gradient

def replay():
    pinned = {'erweiterung.py':'83e6cbbf7d291ab3ec3164f94dfea9c3f8a7e9af73619ba0da22920032b19258',
              'basis/zweig.json':'40690421da499fc1f0d5439bcb11d8085fbb174e6fbf13336220daf8975a013f',
              'basis/intervall.py':'606ab1cc97f85728e46e8ca95294c148237e1bb3d925b7a8dcde686b84706772'}
    for name,sha in pinned.items():
        assert hashlib.sha256((BASE/name).read_bytes()).hexdigest()==sha
    # Add one read-only callback at the accepted-branch point of the original solver.
    source = (BASE/'erweiterung.py').read_text()
    anchor = "        rows.append({'flux':serial(flux)"
    assert source.count(anchor)==1
    callback = "        observe(clock, w, h, flux, gravity)\n"
    cases = []
    def observe(*args):
        cases.append(snapshot(*args))
    ns = {'__file__':str(BASE/'erweiterung.py'), 'observe':observe}
    exec(compile(source.replace(anchor,callback+anchor),str(BASE/'erweiterung.py'),'exec'),ns)
    extensions = [(p,f,r) for p,f,r in ns['extensions']() if p and f]
    assert len(extensions)==182
    rows, totals = [], {16:0,17:0}
    def test(size, keys, r):
        cases.clear()
        totals[size]+=1
        branches, unknown = ns['solve'](r,box(F(1,6)),box(F(1,2)),False,size==17)
        assert not unknown and len(branches)==len(cases)
        for branch,(s,g) in zip(branches,cases):
            assert not branch['bounds_only'] and not (g.lo<=0<=g.hi)
            rows.append((size,*(sum(1<<j for j in k) for k in keys),s.lo,s.hi,g.lo,g.hi))
    z,u = 15,16
    for p,f,r in extensions:
        test(16,[(),(),p,f],r)
    for p,f,_ in extensions:
        for pv,fv,rz in extensions:
            if p<=pv and fv<=f:
                r = rz|{(v,u) for v in p}|{(u,v) for v in f}|{(u,z)}
                test(17,[p,f,pv,fv],r)
    assert totals=={16:182,17:11943}
    assert sorted((n,sum(row[0]==n for row in rows),sum(row[0]==n and row[-2]>0 for row in rows))
                  for n in totals)==[(16,54,30),(17,131,109)]
    return rows

def sin_cos(angle):
    # Range reduction by powers of two. Use Taylor polynomials through order 18.
    s = angle
    steps = 0
    while max(abs(s.lo),abs(s.hi))>SCALE//4:
        s=s/2
        steps+=1
    power=box(1)
    sine,cosine=box(0),box(1)
    for k in range(1,19):
        power=power*s
        term=power*F((-1)**(k//2),factorial(k))
        if k%2:sine=sine+term
        else:cosine=cosine+term
    remainder=F(1,4**19*factorial(19))
    err=Box.hull(-remainder,remainder)
    sine,cosine=sine+err,cosine+err
    for _ in range(steps):
        sine,cosine=2*sine*cosine,cosine.square()-sine.square()
    return sine,cosine

def endpoints(v):
    return [v.lo,v.hi]

def sums(records, phase_scale=1):
    zr,zi,nr,ni,total=[box(0) for _ in range(5)]
    for *_,sl,sh,gl,gh in records:
        s,g=Box(sl,sh),Box(gl,gh)
        si,co=sin_cos(s*phase_scale)
        zr,zi,nr,ni,total=zr+co,zi+si,nr+g*co,ni+g*si,total+g
    denominator=zr.square()+zi.square()
    assert denominator.lo>0
    real=(nr*zr+ni*zi)/denominator
    imag=(ni*zr-nr*zi)/denominator
    return {k:endpoints(v) for k,v in {'Re_Z':zr,'Im_Z':zi,'Re_numerator':nr,'Im_numerator':ni,
        'Re_ratio':real,'Im_ratio':imag,'uniform_mean_G':total/len(records)}.items()}

def angular_certificate():
    dt,theta=F(1,1000),F(1,9200)
    dmax=F(199,5000)+F(161,625)*10*(64*dt/3)**3
    assert dmax<F(1,25) and (10-dt)**2*(1-dmax)>F(979,100)**2
    assert F(17,2)<dt/theta<F(979,100)
    return {'dt':str(dt),'theta':str(theta),'upper_d_B':str(dmax),'R_A_upper':'17/2','R_B_lower_strict':'979/100'}

def main():
    rows=replay()
    buf=io.StringIO()
    w=csv.writer(buf,lineterminator='\n')
    w.writerow(['N','past_u_mask','future_u_mask','past_z_mask','future_z_mask','S_lo','S_hi','G_lo','G_hi'])
    w.writerows(rows)
    result={'endpoint_denominator':SCALE,'phase_scale':1,'N16':sums([r for r in rows if r[0]==16]),
            'N17':sums([r for r in rows if r[0]==17]),'angular_fixture':angular_certificate()}
    outputs={'Kandidaten.csv':buf.getvalue(),'Intervalle.json':json.dumps(result,sort_keys=True,indent=2)+'\n'}
    for name,data in outputs.items():
        path=ROOT/name
        if sys.argv[1:]==['--erzeugen']:path.write_bytes(data.encode())
        else:assert path.read_bytes()==data.encode(),name
    for n in (16,17):
        print(n,{k:[i/SCALE for i in v] for k,v in result['N'+str(n)].items() if 'ratio' in k})
    print('PASS')
if __name__=='__main__':
    if not __debug__:raise SystemExit('Python ohne -O starten.')
    main()
