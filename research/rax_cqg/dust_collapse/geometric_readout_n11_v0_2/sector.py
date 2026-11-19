"""Largest cross-talk-free input subspace for the fixed pair of non-vacuum tests."""
import sympy as s


def analyze(tests, maps):
    # A pulled-back annihilator is a linear combination of standard vacuum annihilators.
    alpha=[s.Matrix([row["unnormalized_coefficients_q_then_p"]]).applyfunc(s.sympify) for row in tests]
    own=[(alpha[j]*maps[j]).applyfunc(s.simplify) for j in range(2)]
    rows=s.zeros(2,3)
    for j,v in enumerate(own):
        rows[j,:]=v[:,3:]
        assert (v[:,:3]+s.I*v[:,3:]).applyfunc(s.simplify)==s.zeros(1,3)
    assert rows.rank()==2
    e,=rows.nullspace()
    assert (rows*e).applyfunc(s.simplify)==s.zeros(2,1)
    # Canonical coherent displacement by real amplitude 1 in the remaining input mode.
    # The real phase-space mean is sqrt(2 / (e^H e)) * [Re(e); Im(e)].
    e2=s.simplify((e.H*e)[0])
    direction=e.applyfunc(s.re).col_join(e.applyfunc(s.im))
    exponents=[]
    for reject in range(2):
        q=alpha[reject].applyfunc(s.re).col_join(alpha[reject].applyfunc(s.im))
        norm=s.sympify(tests[reject]["commutator_norm"])
        exps=[]
        for branch in range(2):
            h=q*maps[branch]
            cov=h*h.T/norm
            d=h*direction
            exponent=s.cancel(2*(d.T*(cov+s.eye(2)/2).inv()*d)[0]/(norm*e2))
            assert exponent>=0
            if branch==reject: assert exponent==0
            else: assert exponent>0
            exps.append(exponent)
        exponents.append(exps[1-reject])
    return {"rank":2,"free_input_modes":1,
            "spectator_direction_not_normalized":[str(s.simplify(z)) for z in e],
            "wrong_vacuum_probability_exponents_on_opposite_branch":[str(v) for v in exponents]}


def lower_upper_efficiency(det_by_test):
    """Enclose the balanced efficiency with strictly rational 12-place endpoints."""
    from math import isqrt
    scale=10**16
    bounds=[]
    for det in det_by_test:
        q=1/det
        floor_root=isqrt(int(q.p)*scale**2//int(q.q))
        lo,hi=s.Rational(floor_root,scale),s.Rational(floor_root+1,scale)
        assert lo**2<=q<=hi**2<1
        bounds.append((1-hi,1-lo))
    low,high=(a*b/(a+b) for a,b in zip(*bounds,strict=True))
    unit=10**12
    return [str(s.Rational(s.floor(low*unit),unit)),str(s.Rational(s.ceiling(high*unit),unit))]
