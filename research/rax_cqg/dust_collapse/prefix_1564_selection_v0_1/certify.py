"""Rational projection bound for normalized three-dimensional complex Gaussians."""
import sympy as sp

SCALE=10**7


def overlap_fourth(left,right):
    inner=(left.conjugate()+right).det()
    value=sp.cancel(64*left.applyfunc(sp.re).det()*right.applyfunc(sp.re).det()
                    /(inner*sp.conjugate(inner)))
    assert value.is_Rational and 0<value<=1
    return value


def upper_fourth_root(q):
    floor,exact=sp.integer_nthroot(int(q.p)*SCALE**4//int(q.q),4)
    upper=sp.Rational(floor,SCALE)
    if upper**4!=q:
        upper+=sp.Rational(1,SCALE)
    assert (upper-1/sp.Integer(SCALE))**4<q<=upper**4
    return upper


def projection_certificate(shapes):
    parent,*daughters=shapes
    sums=[sp.Integer(0) for _ in daughters]
    for i,a in enumerate(daughters):
        for j in range(i):
            bound=upper_fourth_root(overlap_fourth(a,daughters[j]))
            sums[i]+=bound
            sums[j]+=bound
    eigen_lower=1-max(sums)
    parent_sq_upper=sum(upper_fourth_root(overlap_fourth(parent,w))**2 for w in daughters)
    assert eigen_lower>0
    missing_lower=1-parent_sq_upper/eigen_lower
    assert missing_lower>sp.Rational(975,1000)
    return {'lower_eigenvalue_daughter_gram':str(eigen_lower),
            'upper_squared_ordinary_norm_overlap_vector':str(parent_sq_upper),
            'lower_relative_squared_parent_norm_outside_span':str(missing_lower),
            'decimal_lower_rounded_down_to_1e-7':int(missing_lower*SCALE)/SCALE}
