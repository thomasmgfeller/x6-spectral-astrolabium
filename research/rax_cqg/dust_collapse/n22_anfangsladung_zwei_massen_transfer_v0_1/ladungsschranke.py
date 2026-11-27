"""Derive charge from the terminal collar and verify linear inequality certificates."""
from fractions import Fraction as F
from anfangsbasis import LATE,QSTAR

GROUND=22


def affine_charge(y,w,order,edges):
    # -sum G_past = sum G_late when the fourteen free clock gradients vanish.
    assert all(j in LATE for i,j in order if i in LATE)
    assert all(i in (0,1,2,3) for i,j in order if j in (0,1,2,3))
    coeff=[F(0)]*22
    constant=F(0)
    for (i,j),k in edges.items():
        if i not in LATE and j in LATE:
            t=F(k)*w[j]
            coeff[i]+=t
            constant-=t*y[j]
    return constant,coeff


def inequalities(y,order,side):
    # Each tuple encodes Y_i - Y_j <= b, with Y_ground=0.
    rows=[(i,j,F(0)) for i,j in sorted(order)]
    rows += [(j,i,F(8)) for i,j in ((15,16),(15,18),(17,18),(18,7))]
    for j in (3,*LATE):
        rows.extend(((j,GROUND,y[j]),(GROUND,j,-y[j])))
    if side is not None:
        rows.append((side,GROUND,(y[3]+y[7])/2))
    return rows


def verify_linear(y,w,order,edges,certs):
    C,u=affine_charge(y,w,order,edges)
    L=sum(map(abs,u))
    assert L>0
    out={}
    for key,terms in certs.items():
        side=None if key=='order' else int(key)
        rows=inequalities(y,order,side)
        total=[F(0)]*23
        offset=F(0)
        for idx,value in terms.items():
            mult=F(value)
            assert mult>0
            i,j,d=rows[int(idx)]
            total[i]+=mult
            total[j]-=mult
            offset+=mult*d
        assert total[:22]==[-v for v in u]
        bound=C-offset
        info=dict(lower_Q_if_x_at_most_half=str(bound))
        if side is not None:
            mu=F(terms[str(len(rows)-1)])
            assert mu>0
            # Remove the assumed side condition to obtain a global inequality.
            # Q >= bound - mu*(Y_side-(Y3+Y7)/2).
            info['clock_slope']=str(mu*(y[7]-y[3]))
            info['x_min_for_Qstar_over_16']=str(F(1,2)+(bound-QSTAR/16)/(mu*(y[7]-y[3])))
            info['x_min_for_zero']=str(F(1,2)+bound/(mu*(y[7]-y[3])))
        out[key]=info
    return dict(constant=str(C),clock_coefficients=list(map(str,u)),L_in_raw_clock_units=str(L),
                required_max_raw_displacement=str(QSTAR*15/(16*L)),
                required_max_normalized_displacement=str(QSTAR*15/(16*L*(y[7]-y[3]))),
                inequalities=out)


def density_at_13(y,order,edges,linear):
    from math import isqrt
    incoming={i:F(k) for (i,j),k in edges.items() if j==13 and k}
    assert incoming=={3:-8,4:1,5:1,6:1}
    assert all((3,i) in order and (i,13) in order for i in (4,5,6))
    # At w13>0: 19 = 8*t^2 - sum(gap_i^2), with 0 < gap_i < t = Y13-Y3.
    # Thus 19 > 5*t^2. The upper endpoint for sqrt(19/5) is rounded outward.
    denominator=10**20
    s=F(isqrt(19*denominator**2//5)+1,denominator)
    assert (s-F(1,denominator))**2<=F(19,5)<s*s
    duration=y[7]-y[3]
    xhi=s/duration
    dual=linear['inequalities']['13']
    qlo=F(dual['lower_Q_if_x_at_most_half'])-F(dual['clock_slope'])*(xhi-F(1,2))
    assert qlo>QSTAR/16 and xhi<F(dual['x_min_for_Qstar_over_16'])
    return dict(positive_node=13,incoming={str(i):str(k) for i,k in incoming.items()},
                x13_upper=str(xhi),Q_strict_lower=str(qlo),
                target_light=str(QSTAR/16),margin_over_light=str(qlo-QSTAR/16),
                ratio_ceiling_with_fixed_reference=str(QSTAR/qlo),
                largest_possible_common_late_scale_for_light=str((QSTAR/16)/qlo),
                mass_lower_if_reference_is_four=str(4*qlo/QSTAR))
