"""Fine-history density readout of the published finite dust action."""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement, permutations, product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "basis"))
import support
import variation
from gluing import encode, valid

INNER = support.I
COLLAR = support.PAST + support.FUTURE
TYPE = 1767356
STEP = F(1, 1024)


def reduce_row(row, pivots):
    row = list(map(F, row))
    for lead, pivot in sorted(pivots.items()):
        if row[lead]:
            scale = row[lead]
            row = [a-scale*b for a,b in zip(row, pivot)]
    return row


def basis_rows(rows):
    pivots, selected = {}, []
    for key, row in rows:
        residual = reduce_row(row, pivots)
        lead = next((i for i,v in enumerate(residual) if v), None)
        if lead is not None:
            scale = residual[lead]
            pivots[lead] = [v/scale for v in residual]
            selected.append(key)
    return selected


def solve(rows, values):
    # Pivoted rational elimination on the detector response matrix.
    aug = [list(map(F,row)) + [v] for row,v in zip(rows,values)]
    for i in range(len(aug)):
        j = next(j for j in range(i,len(aug)) if aug[j][i])
        aug[i], aug[j] = aug[j], aug[i]
        scale = aug[i][i]
        aug[i] = [v/scale for v in aug[i]]
        for j in range(len(aug)):
            if j != i:
                factor = aug[j][i]
                aug[j] = [x-factor*y for x,y in zip(aug[j],aug[i])]
    return tuple(row[-1] for row in aug)


def coefficients(relations):
    # Each ordered edge contributes b * w_receiver * (e_i-e_j)(e_i-e_j)^t.
    rows = {key:[0]*15 for key in combinations_with_replacement(range(15),2)}
    for i,j in relations:
        inside = sum((i,k) in relations and (k,j) in relations for k in range(15))
        b = (1,-9,16,-8)[inside] if inside < 4 else 0
        rows[i,i][j] += b
        rows[j,j][j] += b
        rows[tuple(sorted((i,j)))][j] -= b
    return rows


def pulse_reader(code, clocks, pairs):
    # The independent archive implements S_raw=-sum(w*(gamma+1))/2.
    # For fixed clocks it is linear in w. Compute its gamma once per arm.
    def arm(shifts):
        y = list(clocks)
        for j,sign in shifts:
            y[j] += sign*STEP
        assert all(y[i] < y[j] for i,j,_ in variation.edges(code,15))
        gamma = variation.gamma(code, 15, y)
        return tuple(-(v+1)/2 for v in gamma)

    center = arm([])
    pulse_rows = []
    for i,j in pairs:
        if i == j:
            arms = [arm([(i,1)]),center,arm([(i,-1)])]
            weights = [1,-2,1]
            denom = STEP**2
        else:
            arms = [arm([(i,a),(j,b)]) for a,b in product((1,-1),repeat=2)]
            weights = [1,-1,-1,1]
            denom = 4*STEP**2
        pulse_rows.append(tuple(-2*sum(k*v for k,v in zip(weights,col))/denom for col in zip(*arms)))
    return pulse_rows


def null_witness(rows):
    # Homogeneous system: put one free variable at 1, solve rows backwards.
    pivots = {}
    for row in rows:
        r = reduce_row(row,pivots)
        lead = next((j for j,v in enumerate(r) if v),None)
        if lead is not None:
            pivots[lead] = [v/r[lead] for v in r]
    free = next(j for j in range(7) if j not in pivots)
    v = [F(0)]*7
    v[free] = 1
    for j,r in sorted(pivots.items(),reverse=True):
        v[j] = -sum(a*b for a,b in zip(r[j+1:],v[j+1:]))
    assert all(sum(a*b for a,b in zip(row,v)) == 0 for row in rows)
    return v


def run():
    archive = json.loads((ROOT/'basis/randdichte.json').read_text())['changed_future_case']
    central = archive['at_midpoint']
    _,rel = support.geometry(TYPE)
    code = encode(rel,15)
    assert archive['code'] == TYPE and valid(code,15)
    rows = coefficients(rel)
    ranks = {}
    full = []
    for n in range(8):
        for subset in combinations(INNER,n):
            access = sorted(COLLAR + subset)
            allowed = combinations_with_replacement(access,2)
            keys = basis_rows((key,[rows[key][i] for i in INNER]) for key in allowed)
            ranks[subset] = len(keys)
            if len(keys) == 7:
                full.append((subset,keys))
    subset,pairs = full[0]
    density = [F(1,8) if i in support.PAST else F(1,64) for i in range(15)]
    clocks = {0:-5,1:-4,2:-3,3:-2+F(1,6),**{j:j-5 for j in support.FUTURE}}
    for j in INNER:
        clocks[j] = sum(map(F,central['Y_inner'][str(j)]))/2
    clocks = tuple(clocks[j] for j in range(15))
    matrix = [[rows[key][j] for j in INNER] for key in pairs]
    pulses = pulse_reader(code,clocks,pairs)
    assert all(tuple(rows[key]) == measured for key,measured in zip(pairs,pulses))
    offsets = [sum(row[j]*density[j] for j in COLLAR) for row in pulses]
    def read(values):
        return solve(matrix,[v-c for v,c in zip(values,offsets)])

    def acquire(weights):
        return [sum(v*w for v,w in zip(row,weights)) for row in pulses]

    verified = 0
    for mask in range(128):
        for k,j in enumerate(INNER):
            density[j] = F(2*k+1,64) if mask & (1<<k) else F(0)
        reconstructed = read(acquire(density))
        assert reconstructed == tuple(density[j] for j in INNER)
        verified += sum((v > 0) == bool(mask & (1<<k)) for k,v in enumerate(reconstructed))
    # Direct original-action check of every selected pulse on the last history.
    def original(shifts):
        y = list(clocks)
        for j,sign in shifts:
            y[j] += sign * STEP
        return variation.matter_action(code,15,y,density)
    for key,expected in zip(pairs,acquire(density)):
        i,j = key
        if i == j:
            measured = -2*(original([(i,1)])-2*original([])+original([(i,-1)]))/STEP**2
        else:
            measured = -sum(a*b*original([(i,a),(j,b)]) for a,b in product((1,-1),repeat=2))/(2*STEP**2)
        assert measured == expected
    witness = null_witness([[rows[key][j] for j in INNER] for key in combinations_with_replacement(sorted(COLLAR),2)])
    # Split the signed invisible change into two distinct nonnegative support masks.
    scale = 2*max(map(abs,witness))
    lhs = [max(F(0),v)/scale for v in witness]
    rhs = [max(F(0),-v)/scale for v in witness]
    assert lhs != rhs and all(sum(rows[key][j]*(x-y) for j,x,y in zip(INNER,lhs,rhs))==0
                               for key in combinations_with_replacement(sorted(COLLAR),2))
    # The three minimal events have identical predecessors and central clocks.
    # Their columns in the unpulsed dust action remain identical at arbitrary collar clocks.
    minimal = [j for j in INNER if not any((i,j) in rel for i in INNER)]
    assert minimal == [4,5,6] and len({clocks[j] for j in minimal}) == 1
    predecessors = [{i for i in range(15) if (i,j) in rel} for j in minimal]
    assert all(ps == set(support.PAST) for ps in predecessors)
    graded = [[b for i0,j,b in variation.edges(code,15) if i0 == i and j in minimal] for i in support.PAST]
    assert all(len(values)==3 and len(set(values))==1 for values in graded)
    one,three = density.copy(),density.copy()
    for j in INNER:
        one[j] = F(1,2) if j==4 else F(0)
        three[j] = F(1,6) if j in minimal else F(0)
    for step in range(9):
        shifted = [y + (F((i+1)*step,4096) if i in COLLAR else 0) for i,y in enumerate(clocks)]
        assert variation.matter_action(code,15,shifted,one) == variation.matter_action(code,15,shifted,three)
    ir = {(i,j) for i,j in rel if i in INNER and j in INNER}
    autos=[]
    for perm in permutations(INNER):
        renaming=dict(zip(INNER,perm))
        if {(renaming[i],renaming[j]) for i,j in ir} == ir:
            autos.append([renaming[i] for i in INNER])
    assert len(autos)==2
    bounds = archive['over_subinterval']['w_inner_new']
    least = min(F(v[0])*F(99,100) for v in bounds.values())
    assert least > 0
    min_size = len(subset)
    return {'type':TYPE, 'rank_boundary':ranks[()], 'tested_access_sets':len(ranks),
            'min_extra_clocks':min_size, 'all_minimal_full_sets':[list(s) for s,_ in full if len(s)==min_size],
            'selected':subset, 'selected_responses':pairs, 'invisible_boundary_support_pair':
            [[str(v) for v in arr] for arr in (lhs,rhs)], 'element_order':INNER,'automorphisms_fixing_collars':autos,
            'same_outer_action_supports':[[str(one[j]) for j in INNER],[str(three[j]) for j in INNER]],
            'support_masks':128,'correct_local_decisions':verified,'min_stationary_w_full_packet':str(least),
            'vacuum_events_in_stationary_packet':0, 'physical_surface':'MISSING_EXTERIOR_OBSERVATION'}


def physical_status():
    records = json.loads((ROOT/'basis/checkpoints.json').read_text())
    calibration = json.loads((ROOT/'basis/massentest.json').read_text())['physical']
    counts = Counter(r['execution'] for r in records)
    assert counts == {'NOT_RUN':60} and calibration['physical_vacuum_reading'] is None
    assert calibration['independent_physical_calibration_pair'] is None and calibration['physical_gain'] is None
    return {'register':dict(counts),'initial_records':sum(r['checkpoint_context']['x']=='0' for r in records),
            'physical_vacuum':None,'independent_mass_pair':None,'gain':None,
            'M1_transfer':'NOT_RUN','M4_transfer':'NOT_RUN','P3':calibration['P3']}
