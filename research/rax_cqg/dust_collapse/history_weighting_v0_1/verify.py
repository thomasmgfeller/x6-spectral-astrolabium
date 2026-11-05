"""Finite diagnostics for history-weighting foundations. Python 3.10+, stdlib.

These are exact combinatorial checks and floating-point benchmark checks;
they neither determine a physical CST measure nor evaluate a new bounce.
"""
from collections import Counter
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import cmath
import csv
import hashlib
import json
import math

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def relabel(edges, p):
    return tuple(sorted((p[i], p[j]) for i, j in edges))

def quotient_checks(n):
    pairs = list(combinations(range(n), 2))
    perms = list(permutations(range(n)))
    classes = Counter()
    reps = {}
    for mask in range(1 << len(pairs)):
        edges = tuple(e for k, e in enumerate(pairs) if mask >> k & 1)
        es = set(edges)
        if any((i, j) in es and (j, k) in es and (i, k) not in es
               for i, j, k in combinations(range(n), 3)):
            continue
        key = min(relabel(edges, p) for p in perms)
        classes[key] += 1
        reps[key] = edges
    labeled_count = 0
    a_sum, nat_corrected_sum, flat_nat_sum = F(0), F(0), F(0)
    examples = []
    for key, actual_nat in classes.items():
        edges = reps[key]
        aut = sum(relabel(edges, p) == edges for p in perms)
        lin = sum(all(p[i] < p[j] for i, j in edges) for p in perms)
        actual_labeled = len({relabel(edges, p) for p in perms})
        require(actual_labeled * aut == math.factorial(n), 'orbit-stabilizer')
        require(actual_nat * aut == lin, 'natural-label multiplicity')
        labeled_count += actual_labeled
        f = 1 + len(edges)  # Independent invariant test integrand.
        a_sum += F(f, aut)
        nat_corrected_sum += F(actual_nat*f, lin)
        flat_nat_sum += actual_nat*f
        if n == 3:
            examples.append(dict(relations=len(edges), aut=aut, linear_extensions=lin,
                                 natural_copies=actual_nat,
                                 quotient_weight=str(F(1, aut))))
    require(a_sum == nat_corrected_sum, 'natural enumeration corrected by 1/L')
    require(len(classes) == {1:1, 2:2, 3:5, 4:16, 5:63}[n], 'class count')
    require(labeled_count == {1:1, 2:3, 3:19, 4:219, 5:4231}[n], 'labeled count')
    return dict(n=n, unlabeled=len(classes), natural=sum(classes.values()),
                arbitrary_labels=labeled_count, corrected_invariant_sum=str(a_sum),
                naive_natural_sum=str(flat_nat_sum), examples=examples)

def marked_check():
    edges = ((0, 2), (1, 2))
    out = []
    for mark in range(3):
        ps = [p for p in permutations(range(3)) if p[mark] == mark]
        aut = sum(relabel(edges, p) == edges for p in ps)
        orbit = len({relabel(edges, p) for p in ps})
        require(aut*orbit == math.factorial(2), 'marked quotient')
        out.append(dict(mark=mark, boundary_preserving_aut=aut, orbit=orbit))
    require([r['boundary_preserving_aut'] for r in out] == [1,1,2], 'mark dependence')
    return out

def matmul(a, b):
    return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]

def maxdiff(a,b):
    return max(abs(x-y) for ar,br in zip(a,b) for x,y in zip(ar,br))

def kernel_checks(n):
    length = 5.0
    dq = length/(n+1)
    qs = [(j+1)*dq for j in range(n)]
    basis = [[math.sqrt(2/length)*math.sin(k*math.pi*q/length)
              for k in range(1,n+1)] for q in qs]
    def kernel(t):
        return [[sum(x*y*cmath.exp(1j*(k*math.pi/length)**2*t)
                     for k,(x,y) in enumerate(zip(a,b),1)) for b in basis] for a in basis]
    ka,kb,kab = kernel(.13),kernel(.21),kernel(.34)
    comp = matmul(ka,[[dq*z for z in row] for row in kb])
    err = maxdiff(comp,kab)
    u = [[dq*z for z in row] for row in ka]
    adj = [[u[j][i].conjugate() for j in range(n)] for i in range(n)]
    ident = [[float(i==j) for j in range(n)] for i in range(n)]
    unity = maxdiff(matmul(adj,u), ident)
    # Same kernel in V=q^2 must still be integrated against dq.
    wrong = matmul(ka, [[(2*qs[j]*dq)*z for z in row] for j,row in enumerate(kb)])
    wrong_err = maxdiff(wrong,kab)
    require(err < 2e-11 and unity < 2e-11, 'spectral composition or norm')
    require(wrong_err > .1, 'missing-Jacobian negative control')
    return dict(n=n, composition_max_abs_error=err, unitarity_max_abs_error=unity,
                wrong_dV_composition_error=wrong_err,
                model='finite sine subspace on 0<q<5; kappa=hbar=1')

def simpson(f, a, b, n):
    h=(b-a)/n
    return h/3*(f(a)+f(b)+4*sum(f(a+j*h) for j in range(1,n,2))
                +2*sum(f(a+j*h) for j in range(2,n,2)))

def coordinate_checks():
    exact=math.sqrt(math.pi)/2*(math.erf(2)-math.erf(1))
    rows=[]
    for n in (32,64,128):
        q=simpson(lambda q:math.exp(-q*q),1,2,n)
        v=simpson(lambda v:math.exp(-v)/(2*math.sqrt(v)),1,4,n)
        rows.append(dict(n=n,q_error=abs(q-exact),volume_error=abs(v-exact)))
    require(rows[-1]['q_error'] < 1e-9 and rows[-1]['volume_error'] < 1e-8, 'coordinate integral')
    require(all(rows[i+1]['volume_error'] < rows[i]['volume_error']/10 for i in (0,1)), 'convergence')
    return rows

def classical_check():
    # Units kappa=1 => G=2/(3*pi). qdot=-1/2, M=qdot^2/4=1/16.
    qdot=F(-1,2); mass=qdot*qdot/4
    data=[]
    for t in map(F, (0,1,2,3)):
        q=2+qdot*t
        v=q*q
        expansion=2*qdot/(3*q)
        density=mass/v
        require(expansion**2 == F(16,9)*density, 'Friedmann dust equation')
        data.append(dict(time=str(t),q=str(q),volume=str(v),mass=str(mass)))
    return dict(status='PASS_EXACT', rows=data, singular_time='4',
                continuation_across_q_zero='NOT_DERIVED')

def audit_source():
    manifest=json.loads((ROOT/'inputs/source_hashes.json').read_text())
    for name,h in manifest.items():
        require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==h, 'source hash '+name)
    out={}
    for name in ('development','holdout'):
        rows=list(csv.DictReader((ROOT/'inputs'/f'{name}.csv').open()))
        paths={r['path'] for r in rows}
        require(len(paths)==(27 if name=='development' else 17), 'source carrier count')
        ranges={}
        for level in ('0','1'):
            subset=[r for r in rows if r['level']==level]
            require(len(subset)==len(paths),'two levels')
            for r in subset:
                ns=[int(r[k]) for k in ('events','N0','N1','N2','N3','Q')]
                require(ns[-1] == ns[0]-ns[1]+9*ns[2]-16*ns[3]+8*ns[4], 'BD polynomial')
            ranges[level]=[min(int(r['events']) for r in subset),max(int(r['events']) for r in subset)]
        out[name]=dict(histories=len(paths),rows=len(rows),events_by_level=ranges,
                       automorphism_data_present=any('aut' in k.lower() for k in rows[0]),
                       microhistory_fibres_present=False)
    return out

def weight_vs_state():
    p=[F(1,4),F(3,4)]
    squared=[x*x/sum(y*y for y in p) for x in p]
    require(squared==[F(1,10),F(9,10)], 'classical probabilities are not amplitudes')
    # Coarse cells: coherent sum 1-1=0 versus diagonal sum 1+1=2.
    require(abs(1-1)**2==0 and abs(1)**2+abs(-1)**2==2, 'interference control')
    return dict(p=[str(x) for x in p], normalized_squared_linear_weights=[str(x) for x in squared],
                coherent_opposite_phase_cell=0, incoherent_cell=2,
                equal_amplitude_singleton_bound='1/2',
                weighted_necessary_condition='abs(A_B)^2 >= 4 * sum_singleton abs(A_s)^2',
                condition_is_sufficient=False)

def main():
    result=dict(schema='x6-history-weight-foundation/v0.1',
                scientific_status='CONDITIONAL_REFERENCE_DERIVED_CST_MEASURE_OPEN',
                source_audit=audit_source(),quotients=[quotient_checks(n) for n in range(1,6)],
                marked_quotient=marked_check(),
                spectral_reference=[kernel_checks(n) for n in (16,32)],
                coordinate_quadrature=coordinate_checks(),classical_dust=classical_check(),
                distinctions=weight_vs_state(),
                new_bounce_test='NOT_RUN',cst_measure='HOLD',singularity_resolution='HOLD',
                floating_point_checks_are_rigorous_interval_certificates=False)
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results/verification.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':
    main()
