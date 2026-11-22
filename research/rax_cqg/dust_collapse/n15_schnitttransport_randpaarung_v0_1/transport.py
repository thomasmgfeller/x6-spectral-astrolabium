"""Transport the six directed phases across the three subsequent N15 cuts."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'quellen'))
from ordnung import ORDER, INNER, PAST, FUTURE, pairs_from_intervals

WEIGHTS = (1, -9, 16, -8)
SLOTS = (4, 5, 6)
CUTS = (11, 12, 13, 14)
TARGETS = (12, 13, 14)
START = ORDER.index(11) + 1
EDGES = pairs_from_intervals()
RANK = {j: k for k, j in enumerate(ORDER)}

def split_pairs(slot, last):
    """Prefix terms must travel with the left state. Read the rest from ordinary memory."""
    done, ahead = [], []
    for rank in range(START, len(ORDER)):
        j = ORDER[rank]
        lag = rank - RANK[slot]
        if lag > len(WEIGHTS):
            break
        entry = (slot, j, WEIGHTS[lag-1])
        (done if rank <= RANK[last] else ahead).append(entry)
    return done, ahead

def polynomial(pairs):
    # Coefficients of 38 times the difference, using t as the actual shift in Y.
    result = Counter()
    for i, j, b in pairs:
        result[j, j, 1] += 2*b    # w_j Y_j t
        result[j, i, 1] -= 2*b    # w_j Y_i t
        result[j, j, 2] -= b      # w_j t^2
    return {k: v for k, v in result.items() if v}

def fine_action(y, density, slot, last, step, carry):
    split = RANK[last] + 1
    result = -F(1, 2) * sum(density.values())
    for region in [ORDER[:split], ORDER[split:]]:
        for j in region:
            for i in ORDER[:RANK[j]]:
                b = EDGES.get((i, j), 0)
                old = y[i]
                if i == slot and j in ORDER[split:] and i in ORDER[split-4:split]:
                    old += step
                result -= F(b, 38)*density[j]*(y[j]-old)**2
    if carry:
        for i, j, b in split_pairs(slot, last)[0]:
            result += F(b, 38)*density[j]*(2*(y[j]-y[i])*step-step**2)
    return result

def exact():
    assert len(EDGES) == 50
    y = {j: F(k*k+7*k-11, 23) for k, j in enumerate(ORDER)}
    units = [{i:F(i==j) for i in ORDER} for j in ORDER]
    rows = {}
    for last in CUTS:
        split = RANK[last] + 1
        details = {}
        for slot in SLOTS:
            past, future = split_pairs(slot, last)
            original = [(i,j,b) for (i,j),b in EDGES.items() if i==slot and RANK[j]>=START]
            assert polynomial(original) == polynomial(past+future)
            assert all(i in ORDER[split-4:split] for i,_,_ in future)
            for unit in units:
                for step in (F(1,8), F(-1,8)):
                    expected = fine_action(y,unit,slot,11,step,False)
                    assert expected == fine_action(y,unit,slot,last,step,True)
            details[str(slot)] = {'links':[j for _,j,_ in past], 'rechts':[j for _,j,_ in future]}
        # Masking all already passed targets retains the later columns of the triangular matrix.
        retained = [j for j in TARGETS if RANK[j] >= split]
        matrix = [[-EDGES.get((i,j),0) if j in retained else 0 for j in TARGETS] for i in SLOTS]
        for j in retained:
            k=TARGETS.index(j)
            assert matrix[k][k]==8 and all(matrix[v][k]==0 for v in range(k))
        rows[str(last)] = {'speicher':list(ORDER[split-4:split]),'arme':details,
                           'rang_ohne_mittransport':len(retained),'matrix_ohne_mittransport':matrix}
    return {'schnitte':rows,'polynomvergleiche':12,'rationale_wirkungsvergleiche':4*3*15*2}
