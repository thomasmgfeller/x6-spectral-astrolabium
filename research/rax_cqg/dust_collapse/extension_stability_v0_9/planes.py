"""Rational certificates at 5 percent using the frozen N14 trial directions."""
from fractions import Fraction as F
from itertools import chain

from reference import ROOT, SOURCE, full, save_json
from bounds import inputs, GRIDS
from anchors import SUPPORT
from teiltraeger import names_and_reach
import numpy as np

T = F(1,20)
Z = full.ZERO
add, mul, conj, scale = full.add, full.mul, full.conj, full.scale
def sub(x,y):
    return x[0]-y[0], x[1]-y[1]

def dot(a,b):
    return full.total(mul(conj(x),y) for x,y in zip(a,b,strict=True))

def forward(L,c):
    y = []
    for i,v in enumerate(c):
        y.append(sub(v,full.total(mul(L[i][j],yj) for j,yj in enumerate(y))))
    return y

def ldl(B):
    n = len(B)
    L = [[Z for _ in range(n)] for _ in range(n)]
    D = []
    for i in range(n):
        for j in range(i+1):
            v = sub(B[i][j],full.total(scale(d,mul(L[i][k],conj(L[j][k])))
                                      for k,d in enumerate(D[:j])))
            if i==j:
                if v[1] or v[0]<=0:
                    raise ValueError("Nonpositive anchor block")
                D.append(v[0]); L[i][i]=(F(1),F(0))
            else:
                L[i][j] = scale(1/D[j],v)
    return L,D

def gram_rows():
    names,_,_,original,*_ = inputs("fine")
    pilot,_ = names_and_reach()
    ix = {s:i for i,s in enumerate(pilot)}
    used = pilot[:2]+list(SUPPORT)
    pts = [ix[s] for s in used]
    g = np.load(SOURCE/"gram.npy")
    data = full.read(ROOT/"support_rows.json")
    if set(data)!={s for s in names if s.startswith("N15_")}:
        raise ValueError("Incomplete additional anchor rows")
    total = [[Z]*5 for j in names]
    margins = []
    for k in range(3):
        block = [[full.cf(g[k,i,j]) for j in pts] for i in pts]
        L,D = ldl(block)
        residual = []
        for j,s in enumerate(names):
            if s in ix:
                col = [full.cf(g[k,i,ix[s]]) for i in pts]
            else:
                col = original[j][k][:2]+[full.cf(complex(*r[k])) for r in data[s]]
            if col[:2]!=original[j][k][:2]:
                raise ValueError(("Inconsistent parents",s,k))
            diag = original[j][k][2][0]
            y = forward(L,col)
            slack = diag-sum((v[0]**2+v[1]**2)/d for v,d in zip(y,D))
            if slack<0 or (s in used and slack!=0):
                raise ValueError(("Incompatible Gram data",s,k,slack))
            if s not in used:
                residual.append(slack)
            total[j] = [add(x,v) for x,v in zip(total[j],col)]
        margins.append(str(min(residual)))
    return total,[names.index(s) for s in used],margins

def directions(rows,indices,tag):
    names,reach,_,_,known,mags,radii = inputs(tag)
    out = []
    for d,nums in enumerate(((202741,693388,103871),(201682,691688,106630))):
        if sum(nums)!=10**6:
            raise ValueError("Trial weights")
        amps = [known[j][d] for j in indices]
        b = [scale(F(1,2),a) for a in amps[:2]]+[Z]*3
        q = [scale(1-T,a) for a in b[:2]]+[scale(T*F(k,10**6),a) for k,a in zip(nums,amps[2:])]
        def pair(c,v):
            return sum(mul(dot(c,rows[j]),z)[0] for j,z in zip(indices,v))
        p, qb, qq = pair(b,b), pair(q,b), pair(q,q)
        h = []
        for j,row in enumerate(rows):
            z = dot(q,row)
            h.append(mul(z,known[j][d])[0]-full.modupper(z)*radii[j] if known[j]
                     else -full.modupper(z)*mags[j])
        critical = (F(9,10)*p+qq-2*(1-T)*qb)/(2*T)
        if 2*qb-qq <= F(9,10)*p:
            raise ValueError("Supporting plane at zero transfer")
        out.append(dict(tag=tag,d=d,p=p,qb=qb,qq=qq,h=h,critical=critical,reach=reach,names=names))
    return out

def extra_gates():
    # Certify the six proper subsets on both sides and the positive change
    # of the total. Only a negative total-success change needs the plane.
    result={}
    for tag,rows in full.read(ROOT/"bounds.json")["proof_constants"].items():
        ptotal = list(map(F,rows[-1]["p"]))
        level = F(0)
        for i,row in enumerate(rows):
            for d in (0,1):
                p,lo,hi,M = map(F,(row["p"][d],row["lo"][d],row["hi"][d],row["M"]))
                def ctrl(c,m):
                    return (F(0),T*(c-p),T*(2*(c-p)+T*(p-2*c+m)))
                up = max(ctrl(hi,M))
                down = -min(ctrl(lo,F(0))) if i<len(rows)-1 else F(0)
                level = max(level,up/ptotal[d],down/ptotal[d])
        if level>F(1,10):
            raise ValueError("An additional level gate is active")
        result[tag]=str(level)
    return result

def calculate():
    gates = extra_gates()
    rows,indices,margins = gram_rows()
    directs = list(chain.from_iterable(directions(rows,indices,tag) for tag in GRIDS))
    names = directs[0]["names"]
    pilot = set(names_and_reach()[0])
    # Fixed support: retain every reachable vertex separately above the
    # exact 90% tangent threshold for every grid and density.
    bad={j for v in directs for j,h in enumerate(v["h"])
         if j>=2 and h<v["critical"]}
    if bad & {names.index(s) for s in pilot}:
        raise ValueError("The original pilot includes individually failing vertices")
    pilot_indices={names.index(s) for s in pilot}
    reserve_bad=set()
    for v in directs:
        for r in v["reach"]:
            threshold=min(v["h"][j] for j in r if j in pilot_indices)
            reserve_bad.update(j for j in r if v["h"][j]<threshold)
    cases={}
    reserve_max=F(1)
    unrestricted = T
    outside_max = F(1)
    for v in directs:
        tag,d,p,qb,qq,h,critical,reach = (v[k] for k in
            ("tag","d","p","qb","qq","h","critical","reach"))
        least=sum(min(h[j] for j in r) for r in reach)/2
        safe=[min(h[j] for j in r if j not in bad) for r in reach]
        rest=[min(h[j] for j in r if j in bad) for r in reach]
        h_safe=sum(safe)/2
        # With (alpha_0+alpha_1)/2 <= delta, the common lower bound
        # is h_safe - delta * max_r(safe_r - rest_r,0).
        loss=max([F(0)]+[a-b for a,b in zip(safe,rest)])
        outside=min(F(1),(h_safe-critical)/loss) if loss else F(1)
        outside_max=min(outside_max,outside)
        core=[min(h[j] for j in r if j not in reserve_bad) for r in reach]
        tail=[min(h[j] for j in r if j in reserve_bad) for r in reach]
        slope=max([F(0)]+[a-b for a,b in zip(core,tail)])
        reserve_share=min(F(1),(sum(core)/2-critical)/slope) if slope else F(1)
        reserve_max=min(reserve_max,reserve_share)
        full_limit = min(T,(2*qb-qq-F(9,10)*p)/(2*(qb-least))) if least<qb else T
        unrestricted=min(unrestricted,full_limit)
        def floor(t,hmin):
            return (2*min(qb,(1-t)*qb+t*hmin)-qq)/p
        cases[f"{tag}_{d}"]={"p":str(p),"qb":str(qb),"qq":str(qq),"critical":str(critical),
            "full_minimum":str(least),"safe_parent_minima":list(map(str,safe)),
            "reserve_parent_minima":list(map(str,core)), "reserve_outside_parent_minima":list(map(str,tail)),
            "reserve_outside_limit":str(reserve_share),"outside_parent_minima":list(map(str,rest)),"full_transfer_limit":str(full_limit),
            "safe_success_floor_at_five":str(floor(T,h_safe)),
            "all_success_floor_at_five":str(floor(T,least)),"outside_share_limit":str(outside),
            "limiting_type_by_parent":[names[min(r,key=lambda j:h[j])] for r in reach]}
    other = F(full.read(ROOT/"bounds.json")["bound_fraction"])
    net = max(unrestricted,other)
    return {"state_count":len(names),"safe_state_count":len(names)-len(bad),
        "reserve_state_count":len(names)-len(reserve_bad),"reserve_outside_types":sorted(names[j] for j in reserve_bad),
        "reserve_outside_share_per_million_at_five":int(reserve_max*10**6),
        "outside_types":sorted(names[j] for j in bad),"grid_cases":cases,
        "support_plane_full_transfer":str(unrestricted),"old_method_full_transfer":str(other),
        "joint_full_transfer_per_million":int(net*10**6),
        "outside_transfer_share_per_million_at_five":int(outside_max*10**6),
        "other_level_tests_at_five":gates,"min_schur_residual_nonanchors":margins}
if __name__=="__main__":
    save_json(ROOT/"planes.json",calculate())
