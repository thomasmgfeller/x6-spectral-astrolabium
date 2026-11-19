"""Fixed-branch scalar integration-by-parts and geometric first-moment diagnostic."""
from fractions import Fraction as Q
from itertools import combinations,product
import sympy as sp
from prefix import A,B,edges
from scalar import INNER,geometry,layout


def single_field(end,code):
    # Exterior labels and existing five interior labels remain fixed. 13 is the
    # new mark. It need not be last in any compatible topological ordering.
    p,f=geometry.P,geometry.F
    rel=set(combinations(p,2))|set(combinations(f,2))|set(product(p,INNER+f))|set(product(INNER,f))
    rel.update((INNER[i],INNER[j]) for i,j in edges(code))
    weights={}
    for i,j in rel:
        size=sum((i,k) in rel and (k,j) in rel for k in range(14))
        weights[i,j]=(1,-9,16,-8)[size] if size<4 else 0
    assert 14-sum(weights.values())==layout((6,end))[2]
    neigh={j if i==13 else i:b for (i,j),b in weights.items() if 13 in (i,j) and b}
    h=-sp.Rational(sum(neigh.values()),2)
    # Formal Abel-regulated integral I(J) over x=q_13. Differentiate the
    # closed Gaussian formula and verify the integration-by-parts identity.
    eps,beta=sp.symbols('epsilon beta',positive=True)
    J=sp.Symbol('J',real=True)
    a=eps-sp.I*beta*h
    factor=sp.sqrt(2*sp.pi)/sp.sqrt(a)*sp.exp(-beta**2*J**2/(2*a))
    mean=sp.simplify(sp.diff(factor,J)/(sp.I*beta*factor))
    assert sp.simplify(-a*mean+sp.I*beta*J)==0
    assert sp.simplify(sp.limit(mean,eps,0,dir='+')+J/h)==0
    return {'new_scalar_label':13, 'quadratic_hessian_entry':str(h),
            'twice_linear_source_coefficients':{str(k):v for k,v in sorted(neigh.items())},
            'integrated_force_identity_rhs':'0','residual_each_branch':'0'}


def diagnostics(paths,bytype):
    derivatives={str(end):single_field(end,c) for end,c,_ in paths if end in (A,B)}
    F0=sum(q*layout((6,j))[2] for j,q in bytype.items())
    slope=49*(layout((6,B))[2]-layout((6,A))[2])
    bound=Q(1,882)
    parent=layout((5,62))[2]
    required=(parent-F0)/slope
    assert slope==-4116 and required>bound
    return {'fixed_order_ward':derivatives,'unphased_geometric_moment_control':{
        'conditional_moment_at_t0':str(F0),'slope':slope,
        'closed_feasible_range':[str(F0+bound*slope),str(F0-bound*slope)],
        'bare_parent_F4':parent,'t_for_bare_parent_value':str(required)}}
