"""Homogeneity and absolute-flux ambiguity, including a pair at fixed G0 and G1."""
from fractions import Fraction as F
from felder import background_rows,pulses,SOURCES


def run(early):
    from zustand import nominal,gradients,check
    from gemischt import ORDER,COEFF,FUT,WEIGHT,CLOCK,PAST
    from quelle import box
    from algebra import solve_box,correction
    y,w=nominal(early)[1]
    assert not any(j in PAST and i not in PAST for i,j in ORDER)
    prior=gradients(y,w)[0]
    K0=w[16]*(y[16]-y[15])
    edge=COEFF[0,1]*w[1]*(y[1]-y[0])
    assert edge.lo==edge.hi==box(F(1,8)).lo
    assert all((COEFF.get((j,15),0)*w[15]*(y[15]-y[j])).lo==0 for j in (0,1,2))
    ref=pulses(y,w)
    scaling=[]
    for label,lam in [('reference',box(1)),('half',box(F(1,2))),('quarter',box(F(1,4))),
                      ('prefix_setpoint',edge/K0)]:
        ws={j:(v if j in PAST else lam*v) for j,v in w.items()}
        K=ws[16]*(y[16]-y[15])
        if label=='prefix_setpoint':
            assert (K-edge).contains_zero() and not (lam-1).contains_zero()
        records=pulses(y,ws)
        for (delta,yp,wp),(old,yo,wo),J in zip(records,ref,SOURCES):
            assert (delta-lam*old).contains_zero()
            for i in y:
                assert (yp[i]-yo[i]).contains_zero()
                assert (wp[i]-(wo[i] if i in PAST else lam*wo[i])).contains_zero()
            # Independent finite construction by directly scaling the solved fields.
            check(yo,{j:(v if j in PAST else lam*v) for j,v in wo.items()},J)
        scaling.append({'case':label,'lambda':lam.data(),'K0':K.data(),
                        'delta_K':[v.data() for v,_,_ in records],
                        'Q':(-records[1][0]/records[0][0]).data()})
    keys,A=background_rows(y)
    # Two remaining far-boundary choices select a well-conditioned one-dimensional family.
    for field in [('w',16),('w',6),('M',10)]:
        A.append([box(col==field) for col in keys])
    rhs=[box(0)]*14+[box(1),box(-F(5,6)),box(-F(2,3))]
    _,q=correction(A)
    direction=dict(zip(keys,solve_box(A,rhs)))
    members=[]
    magnitudes=[[],[]]
    for alpha in (-F(1,30),F(1,30)):
        ww,yy=w.copy(),y.copy()
        for i in WEIGHT+FUT:
            ww[i]+=alpha*direction['w',i]
        for j in FUT:
            yy[j]=(w[j]*y[j]+alpha*direction['M',j])/ww[j]
        assert (yy[7]-y[7]).contains_zero()
        yy[7]=y[7]
        testG=gradients(yy,ww)[0]
        assert all((testG[j]-prior[j]).contains_zero() for j in (0,1))
        records=pulses(yy,ww)
        for k,((delta,_,_),J) in enumerate(zip(records,SOURCES)):
            magnitudes[k].append(delta if J<0 else -delta)
        members.append({'delta_wz':str(alpha),'K0':(ww[16]*(yy[16]-yy[15])).data(),
                        'weights':{str(j):v.data() for j,v in ww.items()},
                        'far_clocks':{str(j):yy[j].data() for j in FUT},
                        'delta_K':[v.data() for v,_,_ in records],
                        'Q':(-records[1][0]/records[0][0]).data()})
    risk=[]
    for a,b in magnitudes:
        assert 0<a.lo<=a.hi<b.lo
        risk.append(str(F(b.lo-a.hi,b.lo+a.hi)))
    return {'reference_G0':prior[0].data(),'reference_G1':prior[1].data(),
            'earliest_link_current':edge.data(),'scaling':scaling,
            'same_G0_G1':{'inverse_infinity_residual_bound':str(q),
                           'per_unit_dw16':{k+str(j):v.data() for (k,j),v in direction.items()},
                           'members':members,'minimax_relative_error_lower_bounds':risk},
            'source_order':list(map(str,SOURCES))}
