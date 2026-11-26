"""Ground-truth fixtures and pulsed solutions, kept outside the prediction module."""
from fractions import Fraction as F
import json
from zipfile import ZipFile


def samples(previous,early):
    from zustand import nominal,check
    from gemischt import PAST,FUT,WEIGHT,Action
    from quelle import box,hull
    from algebra import correction,solve_box
    from felder import background_rows
    y,w=nominal(early)[1]
    K0=w[16]*(y[16]-y[15])
    published=json.loads((previous/'Amplituden.json').read_bytes())
    result=[]
    for record,lam in zip(published['scaling'],(box(1),box(F(1,2)),box(F(1,4)),F(1,8)/K0)):
        result.append((record['case'],y,{i:(a if i in PAST else lam*a) for i,a in w.items()}))
    for record in published['same_G0_G1']['members']:
        yy={**y,**{int(i):hull(*v) for i,v in record['far_clocks'].items()}}
        ww={int(i):hull(*v) for i,v in record['weights'].items()}
        result.append(('G_'+record['delta_wz'],yy,ww))
    # Two geometrical controls vary t and h; two more vary the prefix clock u.
    with ZipFile(previous/'basis/Stromvorhersage.zip') as z:
        clocks=json.loads(z.read('Uhrwahl.json'))
        other=json.loads(z.read('Stromzeugen.json'))['results']['all_momenta']['backgrounds']
    for record in other:
        changes={k:hull(*v) for k,v in record['delta_weights_and_far_moments'].items()}
        yy=y.copy();ww=w.copy()
        for j in (17,18):
            yy[j]+=hull(*record['dY'+str(j)])
        for j in WEIGHT+FUT:
            ww[j]+=changes['w'+str(j)]
        for j in FUT:
            yy[j]=(w[j]*y[j]+changes['M'+str(j)])/ww[j]
        yy[7]=y[7];ww[16]=w[16]
        result.append(('t_'+record['parameter'],yy,ww))
    for record in clocks['tests']:
        if record['mode']!='fixed_future_offset' or not record['both_windows']:
            continue
        proof=record['proof']
        radius=F(proof['radius'])
        yy,ww=Action(False).fields([hull(F(p)-radius,F(p)+radius) for p in proof['solution_centres']])
        ww[7]+=hull(*record['delta_w7'])
        result.append(('u_'+str(F(record['delta_w7'][0])),yy,ww))

    # Fixed clocks, fixed receiver weight, variable sender weight. Complete the
    # 11 native clock rows by fixing Y7 and the shifts listed below.
    cols,old=background_rows(y)
    A=old[:11]+[old[-1]]
    pins=[('w',16),('w',18),('w',5),('w',6),('M',10)]
    A += [[box(c==k) for c in cols] for k in pins]
    rhs=[box(0)]*12+[box(1)]+[box(0)]*4
    _,q=correction(A)
    v=dict(zip(cols,solve_box(A,rhs)))
    for alpha in (-F(1,150),F(1,150)):
        yy=y.copy();ww=w.copy()
        for i in WEIGHT+FUT:
            ww[i]+=alpha*v['w',i]
        for j in FUT:
            yy[j]=(w[j]*y[j]+alpha*v['M',j])/ww[j]
        assert (yy[7]-y[7]).contains_zero() and (ww[18]-w[18]).contains_zero()
        yy[7]=y[7];ww[18]=w[18]
        result.append(('local_'+str(alpha),yy,ww))
    for _,yy,ww in result:
        check(yy,ww)
    return result,{'linear_residual_norm_upper':str(q),'per_sender_weight':
                   {k+str(j):v.data() for (k,j),v in v.items()}}


def causal_sites(order):
    nodes=set(range(19))
    needed={0,1,2,3,4,11,12,13,15,17}
    def sites(required):
        all_sites=sorted(j for j in nodes if all(i==j or (i,j) in order for i in required))
        return all_sites,[j for j in all_sites if not any((k,j) in order for k in all_sites)]
    all_sites,first=sites(needed)
    _,meter=sites({4,11,12,13})
    assert first==[7] and meter==[14] and (18,7) in order
    assert not any((16,i) in order or (18,i) in order for i in needed)
    return {'inputs':sorted(needed),'first_for_four_weights':meter,
            'joint_sites':all_sites,'first_joint':first}
