"""Post-campaign endpoint diagnostics, including an explicitly selected witness."""
from fractions import Fraction as Q
from itertools import product
import numpy as np
import sympy as sp
from run import assess


def endpoint_tests(m, names, roots, daughters, split, transfer):
    eye = dict(zip(names, np.eye(len(names))))
    baseline = {r:Q(1,2) for r in roots}
    def vector(weights):
        return np.array([float(weights.get(k,0)) for k in names])
    w0 = vector(baseline)
    p0 = w0 @ m @ w0
    def scores(w):
        return assess({"coherent":w@m@w},{"coherent":p0})
    # The sector-success matrix is PSD as a norm of the summed state. Verify
    # positive definiteness again on the supplied numerical entries.
    rational = np.vectorize(lambda x:Q.from_float(float(x)), otypes=[object])
    mat = rational(m)
    mat = (mat + mat.swapaxes(-1,-2)) / 2
    success = mat[:,:3].sum(axis=1)
    ids = [i for i,k in enumerate(names) if k in daughters]
    pivots=[]
    for s in success:
        block=sp.Matrix(s[np.ix_(ids,ids)].tolist())
        row=[]
        while block.rows:
            pivot=block[0,0]
            assert pivot>0
            row.append(float(pivot))
            block=block[1:,1:]-block[1:,:1]*block[:1,1:]/pivot
        pivots.append(row)
    lower={}
    mids={k for k in names if k[0]==4}
    ref=np.array([baseline.get(k,Q(0)) for k in names])
    for law in ("marked","shapes"):
        weights={k:w for k,w in transfer(baseline,3,Q(1),mids,law).items() if w}
        choices=[sorted(split(k,daughters,law)) for k in weights]
        corners=list(product(*choices))
        results=[]
        for assignment in corners:
            w=np.array([sum((v for child,v in zip(assignment,weights.values()) if child==k),Q(0)) for k in names],dtype=object)
            results.append(w@success@w)
        ratios=np.max(results,axis=0)/(ref@success@ref)
        lower[law]={"deterministic_assignments":len(corners),"max_success_over_N11_success":[float(x) for x in ratios]}
    # Exploratory edge: choose 1/250 on type 22 and 249/250 on type 184
    # after searching the computed edge family. Show its entire passing interval.
    a,b=(5,184),(5,22)
    assert a in split((4,11),daughters,"marked") and b in split((4,14),daughters,"marked")
    assert (4,11) in split(roots[0],mids,"marked") and {(4,11),(4,14)}<=set(split(roots[1],mids,"marked"))
    x=Q(1,250)
    vec=(1-float(x))*eye[a]+float(x)*eye[b]
    middle=(1-float(x))*eye[(4,11)]+float(x)*eye[(4,14)]
    start = eye[a]; change = eye[b]-start
    c0=start@m@start-p0; c1=change@m@start+start@m@change; c2=change@m@change
    gate_roots={0.,1.}
    def add_zeros(coefs):
        for z in np.roots(coefs):
            if abs(z.imag)<1e-10 and 0<z.real<1:
                gate_roots.add(float(z.real))
    for s0 in product((-1,1),repeat=4):
        sign=np.array(s0)
        for j in range(2):
            add_zeros([c2[j]@sign,c1[j]@sign,c0[j]@sign-.2*sum(p0[j,:3])])
        add_zeros([(c2[1]-c2[0])@sign,(c1[1]-c1[0])@sign,
                   (c0[1]-c0[0])@sign-.25*abs(p0[1]-p0[0]).sum()])
    # Sign is constant on the global real vector space, tested separately.
    accepted=[]
    cuts=sorted(gate_roots)
    for lo,hi in zip(cuts,cuts[1:]):
        if hi-lo<1e-12:continue
        if scores(start+(lo+hi)/2*change)['pass']:
            if accepted and abs(accepted[-1][1]-lo)<1e-10:accepted[-1][1]=hi
            else:accepted.append([lo,hi])
    assert scores(vec)['pass'] and not scores(middle)['pass']
    return {"positive_success_matrix_pivots":pivots,"fixed_N12_marginal":lower,
            "selected_endpoint_fraction_on_type_22":str(x),"selected_endpoint":scores(vec),
            "selected_intermediate":scores(middle),"closed_passing_intervals_along_edge":accepted}


