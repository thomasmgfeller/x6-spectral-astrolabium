"""Independent finite-clock screen and direct tests of the original 15 cases."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations
from felder import OLD, INNER, PAST, FUTURE, P, U, Z, NODES, COLLAR, E, X, SCALE, Box, box, serial


def future_pairs():
    # Each old non-past node is either outside, above u only, or above both.
    # Extend monotonically up the old order, using its transitive closure.
    order = sorted(set(range(15))-P, key=lambda j:(sum(k==j for _, k in OLD),j))
    out = []
    def visit(j, codes):
        if j == len(order):
            out.append((frozenset(i for i,v in codes.items() if v >= 1),
                        frozenset(i for i,v in codes.items() if v == 2)))
            return
        n = order[j]
        minimum = max((v for i,v in codes.items() if (i,n) in OLD),default=0)
        for k in range(minimum,3):
            if k and any((p,n) not in OLD for p in P):
                continue
            visit(j+1, {**codes,n:k})
    visit(0,{})
    return out


def screen(fu, fz):
    past = {j:{i for i,k in OLD if k==j} for j in range(15)}
    for j in fu: past[j].add(U)
    for j in fz: past[j].add(Z)
    past[U],past[Z]=set(P),set(P)|{U}
    e=Box.hull(*E)
    # Both partial derivatives of t=(1-x)e+4x-2 are positive here.
    t=Box.hull((1-X[0])*E[0]+4*X[0]-2,(1-X[1])*E[1]+4*X[1]-2)
    d=(t.square()+6*t+6).sqrt_nonnegative_part()
    clocks={**{i:box(i-5) for i in PAST+FUTURE},3:e-2,U:t-d,Z:t}
    if fu <= COLLAR:
        above=sorted(fz)
        out=sum((b*(box(i-5)-t)/64 for b,i in zip((1,-9,16,-8),above)),box(0))
        wz=out/(d-t-3)
        if wz.hi <= 0 or wz.lo >= SCALE:
            return {'by':'w_z','interval':serial(wz)}
        assert fu==fz==COLLAR
        grad=t*(t+d+9)/192
        assert grad.lo>0
        return {'by':'G_u','interval':serial(grad)}
    states=[clocks]
    for j in sorted(INNER,key=lambda k:(len(past[k]),k)):
        following=[]
        for state in states:
            if any(state[i].lo >= state[k].hi for k in state for i in past[k] if i in state):
                continue
            coeffs=[]
            for i in sorted(past[j]):
                n=sum(i in past[k] for k in past[j])
                if n<4: coeffs.append(((1,-9,16,-8)[n],state[i]))
            a=sum(b for b,_ in coeffs)
            # Local numerical origin anchored on a predecessor's lower bound.
            origin=Box(coeffs[0][1].lo,coeffs[0][1].lo) if coeffs else box(0)
            m=sum((b*(v-origin) for b,v in coeffs),box(0))
            if a:
                disc=-19*a-sum((b*c*(v-w).square() for (b,v),(c,w) in combinations(coeffs,2)),box(0))
                if disc.hi<0: continue
                radical=disc.sqrt_nonnegative_part()
                roots=[origin+(m+radical)/a,origin+(m-radical)/a]
            else:
                c=19+sum((b*(v-origin).square() for b,v in coeffs),box(0))
                if m.lo==m.hi==0 and (c.lo>0 or c.hi<0): continue
                if m.lo<=0<=m.hi: return {'by':'OPEN_LINEAR','node':j}
                roots=[origin+c/(2*m)]
            for v in roots:
                trial={**state,j:v}
                if all(trial[i].lo<trial[k].hi for k in trial for i in past[k] if i in trial):
                    following.append(trial)
        states=following
        if not states: return {'by':'clock_equations_and_order','last_node_checked':j}
    return {'by':'SURVIVES','number':len(states)}


def audit():
    pairs=future_pairs()
    result=[{'u':sorted(u),'z':sorted(z),**screen(u,z)} for u,z in pairs]
    assert len(result)==len(set(pairs))==193
    return {'counts':dict(Counter(row['by'] for row in result)), 'cases':result}


if __name__=='__main__':
    import json
    print(json.dumps(audit(),sort_keys=True,indent=2))
