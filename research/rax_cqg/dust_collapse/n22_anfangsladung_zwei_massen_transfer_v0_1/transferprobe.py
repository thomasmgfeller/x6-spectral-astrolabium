"""Verify fixed-scale transmission using the same two normalized outputs on every state."""
from fractions import Fraction as F
from anfangsbasis import PAST,LATE,QSTAR
from feldroehre import POS
from impulsfelder import fields
from quelle import box,hull


def test_transfer(row,scale,yref,b_star,edges,free,order):
    assert all(i in PAST for i,j in order if j in PAST)
    assert 0<scale<=1
    Y=[hull(*map(F,b)) for b in row['y']]
    W=[hull(*(F(v)*(1 if j in PAST else scale) for v in bounds)) for j,bounds in enumerate(row['w'])]
    # Every edge incident on a free node has a non-past receiving node.
    # Consequently all free clock residuals scale exactly; D is independent of w.
    assert all(j not in PAST for (i,j),k in edges.items() if k and (i in free or j in free))
    ce=[(i,j,box(F(k))) for (i,j),k in sorted(edges.items())]
    vals,_,G=fields(Y,W,box(0),ce,free,[],[box(0)]*5,box)
    assert all(v.contains_zero() for v in vals[:-5])
    q=-sum((G[i] for i in PAST),box(0))
    b=sum((W[i] for i in POS),box(0))*box(1/(yref[7]-yref[3]))
    if row['target_Q']:assert (q-box(F(row['target_Q'])*scale)).contains_zero()
    if row['target_B']:assert (b-box(F(row['target_B'])*scale)).contains_zero()
    assert (q-hull(*(F(v)*scale for v in row['Q']))).contains_zero()
    assert (b-hull(*(F(v)*scale for v in row['B']))).contains_zero()
    def bounds(value,reference):
        calc=[4*F(v)/reference for v in value.data()]
        err=[4*v-1 for v in calc]  # target is 1/4
        return list(map(str,calc)),list(map(str,err)),max(map(abs,err))<=F(1,50)
    m_q,err_q,pass_q=bounds(q,QSTAR)
    m_b,err_b,pass_b=bounds(b,b_star)
    if not pass_b:
        assert min(map(F,err_b))>F(1,50) or max(map(F,err_b))<-F(1,50)
    return dict(case=row['name'],weight_scale=str(scale),mass_Q=m_q,mass_B=m_b,
                relative_error_Q=err_q,relative_error_B=err_b,Q_within_two_percent=pass_q,
                B_within_two_percent=pass_b,positive_zero_pairs=[v['pair'] for v in row['contacts']],
                positive=row['positive'],empty=row['empty'],x19=row['normalized'][19])
