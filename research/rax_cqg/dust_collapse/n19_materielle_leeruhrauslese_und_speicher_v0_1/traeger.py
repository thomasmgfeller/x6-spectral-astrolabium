"""Native positive-density test and three indistinguishable positive cones."""
from fractions import Fraction as F
from itertools import combinations
import json


def native_cases(early):
    from gemischt import ORDER,COEFF,FUT,WEIGHT
    from quelle import box
    from zustand import nominal,check
    from felder import background_rows
    from algebra import correction,solve_box
    from uhrauslese import LABELS,decode
    y,w=nominal(early)[1]
    cone=sorted([18]+[i for i,j in ORDER if j==18])
    positive=[i for i in cone if w[i].lo>0]
    assert positive==[0,1,2,16,18]
    assert sorted((i,c) for (i,j),c in COEFF.items() if j==15 and c)==[(0,16),(1,-9),(2,1)]
    assert sorted((i,c) for (i,j),c in COEFF.items() if j==17 and c)==[(0,1)]
    s,t=y[16],y[18]
    result=[]
    for label in LABELS:
        if not label:
            result.append((label,y,w,box(0)))
            continue
        u=s-(s*s+6*s+6+label).sqrt()
        h=t-(8*(t+4)*(t+4)-16*(t+3)*(t+3)+9*(t-u)*(t-u)-(t-s)*(t-s)-19).sqrt()
        yy={**y,15:u,17:h}
        keys,rows=background_rows(yy)
        pins=[('w',16),('w',18),('w',5),('w',6),('M',10)]
        matrix=rows[:11]+[rows[-1]]+[[box(k==pin) for k in keys] for pin in pins]
        def value(key):
            kind,j=key
            return w[j] if kind=='w' else w[j]*y[j]
        rhs=[box(0)]*12+[value(pin) for pin in pins]
        _,contraction=correction(matrix)
        state=dict(zip(keys,solve_box(matrix,rhs)))
        ww={**w,**{i:state['w',i] for i in WEIGHT+FUT}}
        yy.update({j:state['M',j]/ww[j] for j in FUT})
        for j in (5,6,16,18):
            assert (ww[j]-w[j]).contains_zero()
            ww[j]=w[j]
        assert (yy[7]-y[7]).contains_zero()
        yy[7]=y[7]
        check(yy,ww,label)
        assert all(yy[i] is y[i] and ww[i] is w[i] for i in positive)
        assert decode(yy[15],yy[17],yy[18])==label
        result.append((label,yy,ww,box(contraction)))
    for a,b in combinations(result,2):
        assert all(not (a[1][i]-b[1][i]).contains_zero() for i in (15,17))
    return result,positive


def run(early):
    from quelle import box
    from speichermodell import coupled
    cases,positive=native_cases(early)
    rows=[]
    for j,y,w,q in cases:
        # Use the same early fields; reverse the source by its signed change.
        # The unloaded general solver uses the actual starting density J here.
        base=coupled(y,w,j,F(0),box(0),box(0))
        forward=coupled(base['y'],base['w'],F(0),j,box(0),box(0))
        assert all((forward['y'][i]-y[i]).contains_zero() and
                   (forward['w'][i]-w[i]).contains_zero() for i in y)
        rows.append({'J':str(j),'empty_clocks':[y[i].data() for i in (15,17)],
                     'constraint_contraction':q.data(),'null_background_and_forward_verified':True})
    return {'positive_cone':positive,'same_native_observations':['Y','w'],
            'D15_polynomial':[8,94,284],'D15_global_minimum':'63/8',
            'D15_strict_causal_lower_bound':'74','D17_lower_bound':'19','cases':rows}
