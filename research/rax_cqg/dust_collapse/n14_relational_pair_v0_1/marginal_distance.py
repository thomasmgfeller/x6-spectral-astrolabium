"""Certified minimum variation of an N13 marginal for positive end-type coefficients."""
import numpy as np
from scipy.optimize import linprog
import sympy as sp


def minimum(matrix, target, prefixes, ends):
    # Each column now describes the prefix law of a normalized marked history
    # with a particular end type. Allowed laws form their convex hull.
    rows,cols = matrix.shape
    law = matrix*sp.diag(*(1/sum(matrix[:,j]) for j in range(cols)))
    system = law.row_join(sp.eye(rows)).row_join(-sp.eye(rows))
    system = system.col_join(sp.Matrix([[1]*cols+[0]*(2*rows)]))
    rhs = target.col_join(sp.ones(1,1))
    fit = linprog([0]*cols+[1]*rows+[0]*rows,A_eq=np.array(system,dtype=float),
                  b_eq=np.array(rhs,dtype=float).ravel(),bounds=(0,None),method='highs-ds',
                  options={'primal_feasibility_tolerance':1e-10,'dual_feasibility_tolerance':1e-10})
    if not fit.success:
        raise ArithmeticError(fit.message)
    keep = np.flatnonzero(fit.x>1e-10).tolist()
    values, free = system[:,keep].gauss_jordan_solve(rhs)
    assert free.rows==0 and min(values)>0
    primal = sp.zeros(cols,1)
    for j,value in zip(keep,values):
        if j<cols:
            primal[j]=value
    assert sum(primal)==1
    upper = sum(abs(x) for x in law*primal-target)/2
    dual = sp.Matrix([sp.Rational(float(v)).limit_denominator(1000000)
                      for v in fit.eqlin.marginals[:rows]])
    assert min(dual)>=0 and max(dual)<=1
    lower = (dual.T*target)[0]-max(dual.T*law)
    assert lower == upper > 0
    return {'minimum_normalized_nonnegative_TV':str(upper),
            'attaining_mass_by_endtype':{str(j):str(v) for j,v in zip(ends,primal) if v},
            'dual_test_by_prefix':{str(j):str(v) for j,v in zip(prefixes,dual) if v},
            'dual_target':str((dual.T*target)[0]),'maximum_dual_endtype':str(max(dual.T*law))}
