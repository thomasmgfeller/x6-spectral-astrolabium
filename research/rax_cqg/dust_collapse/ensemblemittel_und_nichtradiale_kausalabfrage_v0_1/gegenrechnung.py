"""Independent double-precision root and action calculation for the same finite test."""
from pathlib import Path
import json
import cmath
from math import sqrt
from itertools import product

root=Path(__file__).resolve().parent/'quelle'
initial=json.loads((root/'basis/zweig.json').read_text())
old=frozenset(map(tuple,initial['order']))
past=tuple(initial['past']);future=tuple(initial['future'])
zero=15
masks=[]
for i in range(1,1<<15):
    s=frozenset(j for j in range(15) if (i>>j)&1)
    masks.append(s)
pools=[[s for s in masks if all(v not in s or u in s for u,v in r)] for r in (old,[(v,u) for u,v in old])]
ext=[(p,f) for p,f in product(*pools) if all((i,j) in old for i,j in product(p,f))]
def expand(p,f,i):return {(j,i) for j in p}|{(i,j) for j in f}
def solve(r,n,x=0.5):
    V=range(n)
    order=sorted(V,key=lambda k:sum((i,k) in r for i in V))
    up=[{b for a,b in r if a==i} for i in V]
    dn=[{a for a,b in r if b==i} for i in V]
    C={(i,j):[1,-9,16,-8][k] for i,j in r if (k:=len(up[i]&dn[j]))<4}
    weights=[(i,j,b) for (i,j),b in C.items()]
    active=[i for i in order if i not in (*past,*future,zero)]
    fixed={j:j-5 for j in (*past,*future)};fixed[3]=-11/6
    fixed[zero]=fixed[3]+x*(fixed[7]-fixed[3])
    val=[fixed]
    for j in active:
        out=[]
        incoming=[(i,b) for i,v,b in weights if j==v]
        for Y in val:
            A=sum(b for _,b in incoming)
            B=sum(b*Y[i] for i,b in incoming)
            D=sum(b*Y[i]**2 for i,b in incoming)+19
            disc=B*B-A*D
            if A==0:roots=[D/(2*B)] if abs(B)>1e-12 else []
            elif disc<0:roots=[]
            else:roots=[(B-sqrt(disc))/A,(B+sqrt(disc))/A]
            for t in roots:
                if all(t>Y[i] for i in dn[j] if i in Y) and all(t<Y[i] for i in up[j] if i in Y):
                    out.append({**Y,j:t})
        val=out
        if not val:break
    rows=[]
    for Y in val:
        if any(Y[i]>=Y[j] for i,j in r):continue
        w={**dict.fromkeys(past,1/8),**dict.fromkeys(future,1/64),zero:0}
        for j in reversed(active):
            factor=sum(b*(Y[j]-Y[i]) for i,v,b in weights if j==v)
            if abs(factor)<1e-12:break
            w[j]=sum(b*w[k]*(Y[k]-Y[j]) for i,k,b in weights if i==j)/factor
            if not 0<w[j]<1:break
        else:
            G=sum(b*w[k]*(Y[k]-Y[zero]) for i,k,b in weights if i==zero)
            F=n-sum(C.values())
            S=F-(19*sum(w.values())+sum(b*w[j]*(Y[j]-Y[i])**2 for i,j,b in weights))/38
            Sb=F-sum(w[j]*(19+sum(b*(Y[j]-Y[i])**2 for i,k,b in weights if k==j)) for j in (*past,*future))/38
            assert abs(Sb-S)<1e-10
            rows.append((G,S,F))
    return rows
print('two sided',len(ext),flush=True)
N16=[];N17=[];n17=0
for p,f in ext:
    N16.extend(solve(old|expand(p,f,15),16))
    for pv,fv in ext:
        if not(p<=pv and fv<=f):continue
        n17+=1
        N17.extend(solve(old|expand(p,f,16)|expand(pv,fv,15)|{(16,15)},17))
for n,entries in [(16,N16),(17,N17)]:
    print('n',n,len(entries),'n17',n17)
    phases=[cmath.exp(1j*s) for g,s,f4 in entries]
    q=sum(g*p for (g,s,f4),p in zip(entries,phases))/sum(phases)
    target=json.loads((root.parent/'Intervalle.json').read_bytes())
    unit=target['endpoint_denominator']
    for v,k in ((q.real,'Re_ratio'),(q.imag,'Im_ratio')):
        lo,hi=target['N'+str(n)][k]
        assert lo/unit <= v <= hi/unit
    print('G-Mittel mit Phase', q)
