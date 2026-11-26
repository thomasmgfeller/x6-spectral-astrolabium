"""Independent antichain enumeration and exact rational action and flux checks."""
from fractions import Fraction as F
from itertools import combinations


def run(report, runs, connection):
    from quelle import DATA
    _,_,order,_,_,_ = DATA
    nodes = tuple(range(19))
    u,h,z = 15,17,16
    past = {j:{i for i,k in order if k==j} for j in nodes}
    edges = {}
    for i,j in order:
        k = len(past[j] & {l for a,l in order if a==i})
        if k<4:
            edges[i,j] = (1,-9,16,-8)[k]

    def antichains(remaining, selected):
        yield selected
        for idx,j in enumerate(remaining):
            allowed = [k for k in remaining[idx+1:] if (j,k) not in order and (k,j) not in order]
            yield from antichains(allowed,selected|{j})

    ideals = {frozenset(a.union(*(past[i] for i in a))) for a in antichains(nodes,set())}
    assert len(ideals) == report['ideal_count']
    assert frozenset(past[z])==frozenset(report['D'])
    classes = [sum(z not in s for s in ideals),sum(z in s and 18 not in s for s in ideals),
               sum(18 in s and 7 not in s for s in ideals),sum(7 in s for s in ideals)]
    assert classes == [report['ideal_groups'][k] for k in
                       ('before_z','with_z_without_r','with_r_without_7','with_7')]
    # An independent, ordered rational test field; no stationarity assumed.
    y = {i:F(2*len(past[i]),7)+F(i,200) for i in nodes}
    w = {i:F(i+1,39) if i not in (u,h) else F(0) for i in nodes}
    assert all(y[i]<y[j] for i,j in order)

    def action(yy,ww,domain):
        return 19*sum(ww[j] for j in domain)+sum(c*ww[j]*(yy[j]-yy[i])**2
                         for (i,j),c in edges.items() if i in domain and j in domain)

    def current(s,i):
        return sum(c*w[j]*(y[j]-y[i]) for (k,j),c in edges.items() if k==i and j in s)

    # Check the second, aggregated formulation for every ideal.
    checks = diamonds = 0
    all_nodes = set(nodes)
    native = action(y,w,all_nodes)
    for domain in ideals:
        other = all_nodes-domain
        cross = 0
        for j in other:
            row = [(i,edges.get((i,j),0)) for i in domain]
            n = sum(c for _,c in row)
            t = sum(c*y[i] for i,c in row)
            v = sum(c*y[i]**2 for i,c in row)
            cross += w[j]*(n*y[j]**2-2*t*y[j]+v)
        assert action(y,w,domain)+action(y,w,other)+cross == native
        available = [j for j in other if past[j]<=domain]
        for j in available:
            next_set = domain|{j}
            assert next_set in ideals
            for i in (u,h):
                if i in domain:
                    assert current(next_set,i)==current(domain,i)+edges.get((i,j),0)*w[j]*(y[j]-y[i])
                if i==j:
                    assert current(next_set,i)==0
            checks += 1
        for j,k in combinations(available,2):
            for i in {u,h} & domain:
                start = current(domain,i)
                a = edges.get((i,j),0)*w[j]*(y[j]-y[i])
                b = edges.get((i,k),0)*w[k]*(y[k]-y[i])
                assert (start+a)+b == (start+b)+a == current(domain|{j,k},i)
            diamonds += 1

    step = F(1,1024)
    for i in (u,h):
        C = sum(c*w[j] for (k,j),c in edges.items() if k==i)
        L = sum(c*w[j]*y[j] for (k,j),c in edges.items() if k==i)
        assert C
        root = L/C
        optimum = dict(y); optimum[i] = root
        shifted = dict(optimum); shifted[i] += step
        assert action(shifted,w,all_nodes)-action(optimum,w,all_nodes) == C*step**2
    prefix = past[z]
    shifted = dict(y); shifted[u] += step
    assert action(shifted,w,prefix) == action(y,w,prefix)
    # Direct mixed central difference of the full unreduced action.
    mixed = F(0)
    for a in (-1,1):
        for b in (-1,1):
            yy = dict(y); yy[u] += a*step
            ww = dict(w); ww[z] += b*step
            mixed += a*b*action(yy,ww,all_nodes)
    assert mixed/(4*step**2) == -2*(y[z]-y[u])
    for case, general in zip(runs['arms'][1:],connection['pure_source_controls']):
        assert case['Jw']==general['source_w']
        lo,hi=map(F,general['required_delta_G15_inside'])
        l,h1=map(F,case['fixed_prefix']['delta_internal_flux_at_15'])
        assert lo<=l<=h1<=hi
    return {'ideals_from_antichains':len(ideals),'exact_action_splits':len(ideals),
            'one_birth_transitions':checks,'two_order_diamonds':diamonds,
            'vacuum_eliminations':2,'mixed_derivative_matches_action':True,
            'nominal_flux_in_uniform_bound':2}
