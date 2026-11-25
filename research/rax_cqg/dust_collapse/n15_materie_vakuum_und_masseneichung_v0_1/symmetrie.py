"""Exploratory check after the two interchangeable events were identified."""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, product
import n15


def run():
    _, rel = n15.support.geometry(n15.TYPE)
    code = n15.encode(rel,15)
    rows = n15.coefficients(rel)
    orbits = ((4,5),(6,),(11,),(12,),(13,),(14,))
    collar = tuple((i,) for i in n15.COLLAR)
    oracle = {}
    for x,y in combinations_with_replacement(collar+orbits,2):
        column = [sum(rows[tuple(sorted((i,j)))][k] for i in x for j in y) for k in range(15)]
        assert column[4] == column[5]
        oracle[x,y] = column
    columns = [group[-1] for group in orbits]
    ranks = {}
    chosen = None
    for size in range(len(orbits)+1):
        for events in combinations(orbits,size):
            accessible = collar+events
            obs = list(combinations_with_replacement(accessible,2))
            keys = n15.basis_rows((pair,[oracle[pair][k] for k in columns]) for pair in obs)
            ranks[events] = len(keys)
            if events == ((6,),(11,)):
                chosen = keys
    assert chosen and len(chosen)==6
    minimal = min(len(events) for events,rank in ranks.items() if rank==6)
    # Strictly order-respecting rational test clocks; identical clocks on the orbit {4,5}.
    clocks = [0]*15
    for n,i in enumerate(n15.support.PAST): clocks[i] = -6+n
    for n,i in enumerate(n15.support.FUTURE): clocks[i] = 8+n
    for i,val in zip(n15.INNER,(0,0,1,2,3,4,5)): clocks[i] = val
    def original(w,shifts):
        y = [F(v) for v in clocks]
        for orbit,sign in shifts:
            for i in orbit: y[i] += sign*n15.STEP
        assert all(y[i]<y[j] for i,j in rel)
        return n15.variation.matter_action(code,15,y,w)
    weights = [F(i+1,32) for i in range(15)]
    observed = []
    for x,y in chosen:
        if x==y:
            value=-2*(original(weights,[(x,1)])-2*original(weights,[])+original(weights,[(x,-1)]))/n15.STEP**2
        else:
            value=-sum(a*b*original(weights,[(x,a),(y,b)]) for a,b in product((1,-1),repeat=2))/(2*n15.STEP**2)
        observed.append(value-sum(oracle[x,y][k]*weights[k] for k in n15.COLLAR))
    reconstructed = n15.solve([[oracle[key][k] for k in columns] for key in chosen],observed)
    assert list(reconstructed)==[sum(weights[k] for k in group) for group in orbits]
    # Even if every orbit is pulsed, identical clocks on 4 and 5 leave their split invisible.
    one = weights.copy(); two = weights.copy()
    one[4],one[5] = F(1,2),F(0)
    two[4],two[5] = F(1,4),F(1,4)
    shifts = [(group,(-1)**k*(k+1)) for k,group in enumerate(collar+orbits)]
    assert original(one,shifts)==original(two,shifts)
    return {'orbits':orbits,'access_sets':len(ranks),'minimum_extra_orbit_sources':minimal,
            'selected_intrinsic_sites':[6,11],'rank_selected':len(chosen),'selected_responses':chosen,
            'test_orbit_sums':list(map(str,reconstructed)),'unresolved_split_equal_clocks':[['1/2','0'],['1/4','1/4']]}
