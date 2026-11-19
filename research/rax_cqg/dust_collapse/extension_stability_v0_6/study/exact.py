"""Rational verification of all mixture inequalities for the published finite tables."""
from fractions import Fraction as F
from math import isqrt
import json
import numpy as np
from common import HERE, setup, archived, coherent
from analytic import run as check_original_bounds

ZERO=(F(0),F(0))
def cf(z):return (F(float(z.real)),F(float(z.imag)))
def add(z,y):return(z[0]+y[0],z[1]+y[1])
def mul(z,y):return(z[0]*y[0]-z[1]*y[1],z[0]*y[1]+z[1]*y[0])
def conj(z):return(z[0],-z[1])
def scale(k,z):return(k*z[0],k*z[1])
def modupper(z):
    denom=10**18
    sq=(z[0]*z[0]+z[1]*z[1])*denom**2
    return F(isqrt(sq.numerator//sq.denominator)+1,denom)
def proj(c,mat,j):
    z=ZERO
    for i,zi in c.items():z=add(z,mul(conj(zi),mat[i][j]))
    return z
def pair(c,mat,d):
    return sum(mul(proj(c,mat,j),z)[0] for j,z in d.items())
def jsonread(name):return json.loads((HERE/name).read_text())

def verify(tag,T,witness_fraction=F(50211,1000000)):
    names,reach=setup(); ix=[names.index(f'N14_{m}') for m in (734,760,8191)]
    assert all(set(ix)<=set(r) for r in reach)
    cap=jsonread('caps.json');cap.update(jsonread('extra_cap.json'))
    extra=jsonread('direct.json');old=archived()
    A=F('0.03609');eta=F('0.001813')
    n=len(names); mag=[]; radii=[F('0.0000001') if nm in extra or nm=='N14_760' else F(0) for nm in names]; states=[{},{}]
    for i,name in enumerate(names):
        if name in old:
            a=coherent(old[name][{'coarse':-2,'fine':-1}[tag]])
        elif name in extra:a=[complex(*t) for t in extra[name]['rows'][tag]]
        else:
            mag.append(F(cap[name][tag]));continue
        for d in range(2):states[d][i]=cf(a[d])
        mag.append(max(modupper(cf(t)) for t in a)+radii[i])
    assert max(mag)<A
    g=np.load(HERE/'gram.npy')
    # Sum of bins as exact rational dyadics, including the fourth sign.
    bins=[[[cf(v) for v in row] for row in k] for k in g]
    S=[[add(add(bins[0][i][j],bins[1][i][j]),bins[2][i][j]) for j in range(n)] for i in range(n)]
    # Input positivity of the three accepted effects verified by positive.py.
    bs=[{i:scale(F(1,2),st[i]) for i in (0,1)} for st in states]
    base=[];lower=[];witness=[];loss=[];derivatives=[]
    # Rational trial mixture weights. A trial vector need not minimize the objective.
    numerators=([[202741,693388],[201682,691688]] if T==F(1,20)
                else [[202267,690752],[201215,689062]])
    for d,st in enumerate(states):
        b=bs[d];s0=pair(b,S,b)
        p=[pair(b,h,b) for h in bins];p.append(1-sum(p));base.append(p)
        q={i:scale(1-T,z) for i,z in b.items()}
        ws=numerators[d]+[10**6-sum(numerators[d])]
        q.update({i:scale(T*F(w,10**6),st[i]) for i,w in zip(ix,ws)})
        # A supporting plane on each reachable daughter simplex.
        h=[proj(q,S,j) for j in range(n)]
        v=[mul(h[j],st[j])[0]-modupper(h[j])*radii[j] if j in st else -modupper(h[j])*mag[j] for j in range(n)]
        least=sum(min(v[j] for j in r) for r in reach)/2
        z=pair(q,S,b);floor=2*min(z,(1-T)*z+T*least)-pair(q,S,q)
        lower.append(floor/s0)
        slopes=[]
        for k,G in enumerate(bins):
            h=[proj(b,G,j) for j in range(n)]
            v=[mul(h[j],st[j])[0]+modupper(h[j])*radii[j] if j in st else modupper(h[j])*mag[j] for j in range(n)]
            cross=sum(max(v[j] for j in r) for r in reach)/2
            vmax=max(G[j][j][0]*mag[j]**2 for r in reach for j in r)
            slopes.append(max(2*(cross-p[k]),(T-2)*p[k]+2*(1-T)*cross+T*vmax))
        derivatives.append(slopes)
        w={i:scale(1-witness_fraction,z) for i,z in b.items()}
        w.update({i:scale(witness_fraction*F(k,100),st[i]) for i,k in zip(ix,[21,70,9])})
        pp=[pair(w,h,w) for h in bins];pp.append(1-sum(pp))
        witness.append(sum(pp[:3])/s0)
        loss.append(sum(abs(x-y) for x,y in zip(p,pp))/(2*s0))
    # Density contrast. For unknown clocks bound <b_H,F H_j> - <b_L,F L_j>
    # after common rephasing; the first two branch differences are the v0.5 bounds.
    d0=[h-l for l,h in zip(*base)]
    cap_delta=[F('0.000166'),F('0.000316')]
    contrast=F(0)
    for k,G in enumerate(bins+[S]):
        sign=1 if k<3 else -1
        rowbounds=[]
        for j in range(n):
            h=[proj(b,G,j) for b in bs]
            if j in states[0]:
                value=mul(h[1],states[1][j])[0]-mul(h[0],states[0][j])[0]
                rowbounds.append(abs(sign*value-d0[k])+radii[j]*sum(modupper(z) for z in h))
            else:
                ed=sum(cap_delta[i]*modupper(G[i][j]) for i in (0,1))/2
                rowbounds.append(ed*mag[j]+modupper(h[1])*eta+abs(d0[k]))
        # PSD grants |Gij|<=max diag. For full-success use G=S for the failure difference.
        vmax=max(G[i][i][0] for i in range(n))
        sec=2*A*eta*vmax+abs(d0[k])
        contrast+=2*T*(1-T)*max(rowbounds)+T*T*sec
    contrast/=2
    relative=contrast/(sum(map(abs,d0))/2)
    signal=sum(d0[:3])
    assert min(lower)>F(9,10) and max(max(a) for a in derivatives)<0
    assert relative<F(1,4) and signal<0 and contrast<abs(signal)
    assert max(S[i][i][0] for i in range(n))<F('1.00001')**2
    delta=witness_fraction*F('1.00001')*max(radii[i] for i in ix)
    upper_witness=witness[1]+(2*F('0.03610')*delta+delta**2)/sum(base[1][:3])
    assert loss[1]>F(1,10) and upper_witness<F(9,10)
    return {'T':str(T),'witness_transfer':str(witness_fraction),'basis_count':n,
            'evaluated_N14':len(extra)+10,'abs_bounded_N14':139-10-len(extra),
            'support_success_lower':list(map(float,lower)),
            'support_success_floor_fraction_exact':[str(q) for q in lower],
            'bin_change_over_transfer_upper':[list(map(float,v)) for v in derivatives],
            'contrast_change_relative_upper':float(relative),'negative_density_signal':float(signal),
            'signal_change_absolute_upper':float(contrast),'threshold_witness_success_ratio':list(map(float,witness)),
            'threshold_witness_level_TV_relative':list(map(float,loss)),
            'witness_high_density_success_ratio_upper_with_clock_radii':float(upper_witness),
            'direct_clock_radius':1e-7}
if __name__=='__main__':
    check_original_bounds()
    results={tag:{str(t):verify(tag,t) for t in [F(1,20),F(5021,100000)]} for tag in ['coarse','fine']}
    (HERE/'result.json').write_text(json.dumps(results,indent=2)+'\n')
    for tag,rs in results.items():
        for t,r in rs.items():print(tag,t,r['support_success_lower'],r['contrast_change_relative_upper'],r['threshold_witness_success_ratio'])
