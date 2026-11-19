"""Full-support certificate using N11 cross-rows and convexity for arbitrary unknown N15 phases."""
from fractions import Fraction as F
from itertools import combinations
import json
import numpy as np
from matrices import ROOT,CACHE,names_and_reach,common,write
from exact import cf,add,scale,mul,conj,modupper,ZERO

def read(path): return json.loads(path.read_text())
def total(zs):
    z=ZERO
    for w in zs:z=add(z,w)
    return z

def inputs(tag):
    g=np.load(ROOT/'gram.npy'); names,reach=names_and_reach()
    old=common.archived()
    extra={**read(CACHE/'study/direct.json'),**read(ROOT/'clocks.json')}
    caps={**read(CACHE/'study/caps.json'),**read(CACHE/'study/extra_cap.json')}
    caps15=read(ROOT/'caps.json');rows=read(ROOT/'anchor_rows.json')
    cat=read(ROOT/'catalog.json')
    offsets={n:i for i,n in enumerate(names)}
    missing=sorted(int(m) for m in rows if 'N15_'+m not in offsets)
    for j,m in enumerate(missing):
        for r,k in enumerate(('chain','one')):
            if str(m) in cat['roots'][k]['ends']:reach[r].append(len(names)+j)
    names=names+['N15_'+str(m) for m in missing]
    base=np.array([g[k,:2,:2] for k in range(3)])
    cols=[]; known=[]; mags=[]; radii=[]
    for j,name in enumerate(names):
        size,mask=common.prior.key(name)
        r=F('1e-7') if name in extra or name=='N14_760' else F(0)
        amps=None
        if name in old:amps=common.coherent(old[name][{'coarse':-2,'fine':-1}[tag]])
        if name in extra:amps=[complex(*z) for z in extra[name]['rows'][tag]]
        if amps is None:
            cap=F(caps15[str(mask)][tag] if size==7 else caps[name][tag])
        else:
            amps=[cf(z) for z in amps];cap=max(map(modupper,amps))+r
        if j<len(g[0]):
            col=g[:,[0,1,j],j]
        else:
            col=np.array([[complex(*z) for z in rr] for rr in rows[str(mask)]]).T
        if j>=len(g[0]):
            assert np.max(abs(col[:,2].imag))<1e-50
            col[:,2]=col[:,2].real  # Hermitian diagonals are real.
        if size==7 and j<len(g[0]):
            stored=np.array([[complex(*z) for z in rr] for rr in rows[str(mask)]]).T
            assert np.max(abs(stored-col))<1e-14
        cols.append([[cf(z) for z in row] for row in col]); mags.append(cap);known.append(amps);radii.append(r)
    assert len(names)==1217 and len(missing)==1025 and max(mags)<F('0.03609')
    return names,reach,base,cols,known,mags,radii

def positive_completion(base,cols):
    # Schur complement of the shared 2x2 block. Each admissible residual
    # can be realized along a separate orthogonal vector (or any PSD completion).
    for k in range(3):
        h,u=cf(base[k,0,0])[0],cf(base[k,1,1])[0]
        v=cf(base[k,0,1]);det=h*u-mul(v,conj(v))[0]
        assert h>0 and det>0
        for row in cols[2:]:
            a,b,s=row[k];assert abs(s[1]) < F('1e-50')
            a2=mul(a,conj(a))[0];b2=mul(b,conj(b))[0]
            cross=mul(mul(conj(a),v),b)[0]
            assert s[0]*det >= u*a2+h*b2-2*cross

def constants(tag):
    names,reach,base,cols,known,mags,radii=inputs(tag)
    positive_completion(base,cols)
    A=F('0.03609');eta=F('0.001813')
    anchors=[[scale(F(1,2),known[i][d]) for i in (0,1)] for d in (0,1)]
    effects=[]
    for size in (1,2,3):
        for sub in combinations(range(3),size):
            entries=[[total(col[k][i] for k in sub) for i in range(3)] for col in cols]
            proj=[[total(mul(conj(b[i]),v[i]) for i in (0,1)) for v in entries] for b in anchors]
            p=[sum(mul(proj[d][j],a)[0] for j,a in enumerate(anchors[d])) for d in (0,1)]
            D=p[1]-p[0]
            lower=[];upper=[]
            def extremum(values,fn):
                return sum(fn(values[j] for j in r) for r in reach)/2
            for d in (0,1):
                lo=[];hi=[]
                for j,z in enumerate(proj[d]):
                    center=mul(z,known[j][d])[0] if known[j] else F(0)
                    rad=modupper(z)*(radii[j] if known[j] else mags[j])
                    lo.append(center-rad);hi.append(center+rad)
                lower.append(extremum(lo,min));upper.append(extremum(hi,max))
            M=max(row[2][0]*a*a for row,a in zip(entries,mags))
            # Bound the change in the real cross term between densities.
            change=[]
            for j,v in enumerate(entries):
                lo,hi=proj[0][j],proj[1][j]
                if known[j]:
                    z=mul(hi,known[j][1])[0]-mul(lo,known[j][0])[0]-D
                    bound=abs(z)+(modupper(lo)+modupper(hi))*radii[j]
                else:
                    anchor_shift=(F('0.000166')*modupper(v[0])+F('0.000316')*modupper(v[1]))/2
                    bound=abs(D)+anchor_shift*mags[j]+modupper(hi)*eta
                change.append(bound)
            K=extremum(change,max)
            R=2*A*eta*max(row[2][0] for row in entries)+abs(D)
            effects.append((sub,p,lower,upper,M,K,R))
    return effects

def metrics(effects,T):
    # Bernstein control coefficients of each degree-2 polynomial on [0,T].
    ptotal=effects[-1][1]
    ref_tv=max(abs(p[1]-p[0]) for _,p,*_ in effects)
    signal=ptotal[1]-ptotal[0]; assert signal<0
    level=[F(0),F(0)];contrast=F(0);sig=None
    for sub,p,lo,hi,M,K,R in effects:
        for d in (0,1):
            a=2*(lo[d]-p[d]);b=p[d]-2*lo[d]
            bottom=min(0,T*a/2,T*(a+T*b))
            a=2*(hi[d]-p[d]);b=p[d]-2*hi[d]+M
            top=max(0,T*a/2,T*(a+T*b))
            level[d]=max(level[d],max(-bottom,top)/ptotal[d])
        delta=2*T*(1-T)*K+T*T*R
        contrast=max(contrast,delta/ref_tv)
        if len(sub)==3:sig=delta/abs(signal)
    return (*level,contrast,sig)

def calculate():
    effects={tag:constants(tag) for tag in ('coarse','fine')}
    def passes(k):
        T=F(k,10**6)
        return all(u<=F(1,10) and v<=F(1,10) and w<=F(1,4) and s<1
                   for u,v,w,s in (metrics(es,T) for es in effects.values()))
    lo,hi=0,50211
    assert passes(lo)
    while hi-lo>1:
        mid=(lo+hi)//2
        if passes(mid):lo=mid
        else:hi=mid
    assert not passes(hi)
    result={'bound_fraction':str(F(lo,10**6)),'next_fraction_not_certified_by_this_bound':str(F(hi,10**6)),
            'known_and_bounded_states':1217,'metrics':{},'proof_constants':{}}
    for tag,es in effects.items():
        result['proof_constants'][tag]=[{'bins':s,'p':list(map(str,p)),'lo':list(map(str,l)),
            'hi':list(map(str,h)),'M':str(m),'K':str(k),'R':str(r)} for s,p,l,h,m,k,r in es]
        result['metrics'][tag]={str(t):[str(v) for v in metrics(es,t)]
                                for t in [F(16,1000),F(lo,10**6),F(hi,10**6),F(1,20)]}
    return result

if __name__=='__main__':
    if not __debug__: raise RuntimeError('Run without -O')
    obj=calculate();write('full.json',obj);print(obj['bound_fraction'])
