#!/usr/bin/env python3
"""Independent rational-interval propagation of the inherited amplitude boxes.

No quadrature is rerun. Every endpoint calculation is exact Fraction arithmetic;
only display conversion is rounded (outward). Scientific validity remains
conditional on the supplied amplitude enclosures and the declared instrument.
"""
from fractions import Fraction as F
from decimal import Decimal, localcontext, ROUND_FLOOR, ROUND_CEILING
from pathlib import Path
import hashlib
import json

BASE = Path(__file__).resolve().parents[1]

class I:
    def __init__(self, a, b=None):
        self.a, self.b = F(a), F(a if b is None else b)
        assert self.a <= self.b
    def __add__(self, v):
        v = box(v)
        return I(self.a + v.a, self.b + v.b)
    __radd__ = __add__
    def __neg__(self):
        return I(-self.b, -self.a)
    def __sub__(self, v): return self + (-box(v))
    def __rsub__(self, v): return box(v) + (-self)
    def __mul__(self, v):
        v = box(v)
        q = [self.a*v.a, self.a*v.b, self.b*v.a, self.b*v.b]
        return I(min(q), max(q))
    __rmul__ = __mul__
    def __truediv__(self, v):
        v = box(v)
        assert v.a > 0 or v.b < 0
        return self * I(1/v.b, 1/v.a)
    def square(self):
        return I(0 if self.a <= 0 <= self.b else min(self.a*self.a,self.b*self.b), max(self.a*self.a,self.b*self.b))
    def out(self):
        result=[]
        for x, mode in [(self.a, ROUND_FLOOR),(self.b, ROUND_CEILING)]:
            with localcontext() as ctx:
                ctx.prec=30
                ctx.rounding=mode
                result.append(str(Decimal(x.numerator)/Decimal(x.denominator)))
        return result
    def nonzero(self): return self.a > 0 or self.b < 0

def box(v): return v if isinstance(v,I) else I(v)
def cadd(u,v): return (u[0]+v[0],u[1]+v[1])
def cconj(u): return (u[0],-u[1])
def cmul(u,v): return (u[0]*v[0]-u[1]*v[1],u[0]*v[1]+u[1]*v[0])
def cabs2(u): return u[0].square()+u[1].square()
def midpoint(z): return ((z[0].a+z[0].b)/2,(z[1].a+z[1].b)/2)
def exact_abs2(z): return z[0]*z[0]+z[1]*z[1]
def exact_add(x,y): return (x[0]+y[0],x[1]+y[1])
def exact_mul(x,y): return (x[0]*y[0]-x[1]*y[1],x[0]*y[1]+x[1]*y[0])

def main():
    file=BASE/'sources/result_64.json'
    digest=hashlib.sha256(file.read_bytes()).hexdigest()
    assert digest=='5085b0f3d5bf2d9a70a184853c9d236fc2d41d7d2f7003b9c57ad980bdb34eae'
    data=json.loads(file.read_text())
    A=[[(I(*z['real']),I(*z['imag'])) for z in row] for row in data['analysis']['amplitudes']]
    gain2=F(1,256**2)
    results=[]
    checks={}
    plus_intervals=[]
    for k,row in enumerate(A):
        Z=sum((cabs2(z) for z in row),I(0))
        cross=(I(0),I(0))
        plus_raw=I(0)
        direct_raw=I(0)
        port_records=[]
        for s in range(2):
            x,y=row[s],row[s+2]
            cross=cadd(cross,cmul(x,cconj(y)))
            add=cadd(x,y)
            sub=cadd(x,(-y[0],-y[1]))
            qp=cabs2(add)/2
            qm=cabs2(sub)/2
            plus_raw+=qp
            direct_raw+=cabs2(add)
            port_records.append({'stratum':['atom','positive'][s], 'plus_unconditional':(gain2*qp).out(), 'minus_unconditional':(gain2*qm).out(), 'plus_conditional':(qp/Z).out(),'minus_conditional':(qm/Z).out()})
            xp,yp=midpoint(x),midpoint(y)
            addp=exact_add(xp,yp)
            subp=exact_add(xp,(-yp[0],-yp[1]))
            checks[f'input{k}_stratum{s}_two_port_identity_exact']=exact_abs2(addp)+exact_abs2(subp)==2*(exact_abs2(xp)+exact_abs2(yp))
            # Rephase class1 by i and transform the reference coefficient by i.
            ip=(F(0),F(1))
            rephased=exact_add(exact_mul(ip,xp),exact_mul(ip,yp))
            checks[f'input{k}_stratum{s}_phase_covariance_exact']=exact_abs2(rephased)==exact_abs2(addp)
        pplus=plus_raw/Z
        plus_intervals.append(pplus)
        checks[f'input{k}_cross_real_excludes_zero']=cross[0].nonzero()
        checks[f'input{k}_normalizer_positive']=Z.a>0
        partial={}
        for g in [F(0),F(1,2),F(1)]:
            p=I(F(1,2)) + g*cross[0]/Z
            partial[str(g)]={'plus_given_success':p.out(),'minus_given_success':(1-p).out()}
            checks[f'input{k}_gamma{g}_probability_in_unit_interval']=p.a>=0 and p.b<=1
        results.append({'input':['g0','gplus'][k], 'Z':Z.out(), 'cross':{'real':cross[0].out(),'imag':cross[1].out()},'ports':port_records,'plus_given_success':pplus.out(),'success':(gain2*Z).out(),'failure':(1-gain2*Z).out(),'direct_classblind_success':(gain2*direct_raw).out(),'direct_classblind_failure':(1-gain2*direct_raw).out(),'partial_coherence':partial})
    delta=plus_intervals[1]-plus_intervals[0]
    checks['source_contrast_excludes_zero']=delta.nonzero()
    checks['source_contrast_negative']=delta.b<0
    old_bound=F(264069,1310720)
    checks['old_effect_bound_below_one']=old_bound<1
    checks['direct_effect_bound_below_one']=2*old_bound<1
    # Recompute completeness for a coherent non-basis input as exact point algebra.
    weights=[(F(1,3),F(2,5)),(F(-2,7),F(1,11))]
    mixed=[]
    for j in range(4):
        mixed.append(exact_add(exact_mul(weights[0],midpoint(A[0][j])),exact_mul(weights[1],midpoint(A[1][j]))))
    old=sum(exact_abs2(z) for z in mixed)
    new=sum((exact_abs2(exact_add(mixed[s],mixed[s+2]))+exact_abs2(exact_add(mixed[s],(-mixed[s+2][0],-mixed[s+2][1]))))/2 for s in range(2))
    checks['coherent_input_completeness_exact']=old==new
    output={'id':'BOUNDARY-COHERENCE-EXACT-RATIONAL-AUDIT-0.1','inherited_input_sha256':digest,'scope':'Independent propagation of inherited boxes, not independent reintegration or physical detector derivation. theta=0; gamma specified as auxiliary assumption.','arithmetic':'Exact rational interval endpoints, decimal display rounded outwards to 30 significant digits.','results':results,'delta_plus_gplus_minus_g0':delta.out(),'delta_plus_percentage_points':(100*delta).out(),'uniform_bounds':{'old':str(old_bound),'direct':str(2*old_bound)},'checks':checks,'all_checks_pass':all(checks.values())}
    assert output['all_checks_pass'],checks
    path=BASE/'checks/root_exact_audit.json'
    path.write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'checks':len(checks),'delta_probability':delta.out(),'plus':[p.out() for p in plus_intervals]},indent=2))

if __name__=='__main__': main()
