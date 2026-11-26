from fractions import Fraction as F
from itertools import product
from freigabefenster import code_range
from uhrvergleich import TINY, corner_band,decision


def stability(state,step,biases,ref,geo,cert):
    ranges=[code_range(state[i],step,b) for i,b in zip((15,17),biases)]
    rows=[]
    for codes in product(*ranges):
        band=corner_band(codes,step,biases,geo,cert)
        # Stable true zero is in both references. Only the outer budget can bind.
        assert band[0]<=42180625621<=band[1]
        rows.append({'codes':list(codes),'band':list(band),'status':decision(ref,band)})
    return rows


def quantizer_edge(state,step,lo,hi,ref,geo,cert):
    from quelle import box
    clocks=(15,17)
    before=[set(code_range(state[i],step,lo)) for i in clocks]
    after=[set(code_range(state[i],step,hi)) for i in clocks]
    changed=[k for k in (0,1) if before[k]!=after[k]]
    assert len(changed)==1
    k=changed[0]
    added=after[k]-before[k]
    assert len(added)==1
    new=added.pop()
    upper=new>max(before[k])
    boundary=(new+(-F(1,2) if upper else F(1,2)))*step
    dist=box(boundary)-state[clocks[k]] if upper else state[clocks[k]]-box(boundary)
    a,b=map(F,dist.data())
    assert lo<a<=b<hi
    # Old pairs pass even with the wide uncertainty. Every new pair already
    # exceeds the budget when evaluated with the narrow uncertainty.
    for pair in product(*before):
        assert decision(ref,corner_band(pair,step,(hi,hi),geo,cert))=='ACCEPT'
    for pair in set(product(*after))-set(product(*before)):
        assert decision(ref,corner_band(pair,step,(lo,lo),geo,cert))=='GEOMETRY_OUTSIDE_ERROR_BUDGET'
    return {'clock':clocks[k],'entering_code':new,'threshold_band':dist.data(),
            'all_pairs_pass_at_equality':not upper}


def stable_limits(state,ref,geo,cert):
    rows=[]
    for step,axes in product((TINY,2*TINY),((1,1),(1,0),(0,1))):
        def evaluate(b):
            return stability(state,step,tuple(b*x for x in axes),ref,geo,cert)
        def passes(rows):
            return all(r['status']=='ACCEPT' for r in rows)
        lo,hi=F(0),TINY
        assert passes(evaluate(lo))
        end=evaluate(hi)
        basic={'step':str(step),'varied_clocks':[i for i,x in zip((15,17),axes) if x],
               'at_1e_minus_12':end}
        if passes(end):
            rows.append({**basic,'all_pass_up_to':str(hi)})
            continue
        for _ in range(24):
            mid=(lo+hi)/2
            if passes(evaluate(mid)):
                lo=mid
            else:
                hi=mid
        assert passes(evaluate(lo)) and not passes(evaluate(hi)) and hi-lo<F(1,10**18)
        if axes==(1,1):
            basic['analytic_edge']=quantizer_edge(state,step,lo,hi,ref,geo,cert)
        rows.append({**basic,'bracket':[str(lo),str(hi)],'rejected_witness_at_upper':
                        next(r for r in evaluate(hi) if r['status']!='ACCEPT')})
    return rows
