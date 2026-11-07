#!/usr/bin/env python3
"""Independent floating-point quadrature check; not an interval certificate."""
from pathlib import Path
from fractions import Fraction
import json, math
from scipy.integrate import quad
ROOT=Path(__file__).resolve().parent
rows=[]
def center(c):
    return complex(sum(float(Fraction(x)) for x in c['real'])/2,
                   sum(float(Fraction(x)) for x in c['imag'])/2)
def integrate(fun,a,b):
    real,er=quad(lambda x:fun(x).real,a,b,epsabs=1e-12,epsrel=1e-12)
    imag,ei=quad(lambda x:fun(x).imag,a,b,epsabs=1e-12,epsrel=1e-12)
    return complex(real,imag),er+ei
def phase(x):return complex(math.cos(x),-math.sin(x))
def check(kind,val,err,target,**metadata):
    discrepancy=abs(val-center(target))
    if discrepancy>1e-11:raise RuntimeError('Supplementary quadrature mismatch')
    rows.append({'kind':kind,**metadata,'absolute_difference':discrepancy,'reported_quad_error':err})
for filename in ['amplitude_certificates.json','amplitude_certificates_interior.json']:
    data=json.loads((ROOT/'results'/filename).read_text());w=float(Fraction(data['w']))
    for record in data['records']:
        if 'shift' not in record:continue
        b=float(Fraction(record['b']));c=float(Fraction(record['shift']))
        for name,bvalue,mu in [('baseline',b,0),('fixed_box',b+c,0)]:
            v,e=integrate(lambda t:phase(w*(t-bvalue)**2/4)/2,mu-1,mu+1)
            check(name,v,e,record[name],w=w,b=bvalue)
        v,e=integrate(lambda t:phase(w*(t-(b+c))**2/4)/2,c-1,c+1)
        check('cotransformed',v,e,record['baseline'],w=w,b=b+c,mu=c)
    for record in data['relative_measure_amplitudes']:
        L=float(Fraction(record['L']))
        v,e=integrate(lambda r:(2*L-r)/(2*L*L)*phase(w*r*r/4),0,2*L)
        check('relative_pushforward',v,e,record['correct_pushforward'],w=w,L=L)
        v,e=integrate(lambda r:phase(w*r*r/4)/(2*L),-L,L)
        check('naive_box',v,e,record['naive_box'],w=w,L=L)
result={'checks':len(rows),'max_absolute_difference':max(r['absolute_difference'] for r in rows),
        'max_reported_quadrature_error':max(r['reported_quad_error'] for r in rows),
        'acceptance_tolerance':1e-11,'certification':False,
        'role':'Supplementary independent integration, not used for the rational decisions.','rows':rows}
(ROOT/'results'/'quadrature_check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='rows'},indent=2))
