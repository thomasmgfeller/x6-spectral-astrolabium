"""Deterministic current bounds and explicit field histories around the new stationary branch."""
from fractions import Fraction as F
from intervall import Box, box, SCALE
from pruefung import I,P,FUT
from randdichte import construct
from gegenprobe import ends


def ideals(rel):
    rows=[]
    for bits in range(1<<7):
        region=set(P)|{j for k,j in enumerate(I) if bits & (1<<k)}
        if all(i in region or j not in region for i,j in rel):
            rows.append(region)
    return rows


def coeffs(edges,region,subtract_start):
    return {(i,j):b*(int(i in region and j not in region)-
                     int(subtract_start and i in P and j not in P))
            for (i,j),b in edges.items() if j not in P}


def slopes(c,y,w):
    aw={i:box(0) for i in I}
    ay={i:box(0) for i in I}
    for (i,j),b in c.items():
        if j in I:
            aw[j]+=b*(y[i]-y[j])
            ay[j]-=b*w[j]
        if i in I:
            ay[i]+=b*w[j]
    return ay,aw


def variation(c,y,w,dy,dw):
    ay,aw=slopes(c,y,w)
    linear=sum(ay[j]*dy[j]+aw[j]*dw[j] for j in I)
    mixed=sum(b*dw[j]*(dy.get(i,box(0))-dy[j]) for (i,j),b in c.items() if j in I)
    return linear+mixed


def tube(e,level,find_witness=False):
    rel,edges,y,w,center=construct(e,True)
    factor=F(1,2**level)
    hy=(4-e)*F(1,64)*factor
    hw={j:w[j]*F(1,100)*factor for j in I}
    dy=dict.fromkeys(I,Box(-hy.hi,hy.hi))
    dw={j:Box(-hw[j].hi,hw[j].hi) for j in I}
    for j in I:
        assert w[j].lo+dw[j].lo>0 and w[j].hi+dw[j].hi<SCALE
    assert all((y[i]+dy.get(i,0)).hi<(y[j]+dy.get(j,0)).lo for i,j in rel)
    inlet=coeffs(edges,set(P),False)
    in_box=center+variation(inlet,y,w,dy,dw)
    if in_box.lo<=0:
        # A broad denominator enclosure gives no guarantee from this bound alone.
        error=None
    else:
        error=0
    largest_witness=None
    for region in ideals(rel):
        c=coeffs(edges,region,True)
        v=variation(c,y,w,dy,dw)
        if error is not None:
            error=max(error,F(max(v.hi,-v.lo),in_box.lo))
        if find_witness:
            ay,aw=slopes(c,y,w)
            # Choose attainable joint endpoints. Check the resulting actual current, not only a bound.
            for orient in (1,-1):
                sy={j:orient*(1 if ay[j].lo+ay[j].hi>=0 else -1) for j in I}
                sw={j:orient*(1 if aw[j].lo+aw[j].hi>=0 else -1) for j in I}
                uy={j:sy[j]*hy for j in I}
                uw={j:sw[j]*hw[j] for j in I}
                init=center+variation(inlet,y,w,uy,uw)
                if init.lo<=0:
                    continue
                # Separate calculation from perturbed edge currents without the stationarity substitution.
                new_y={j:z+uy.get(j,0) for j,z in y.items()}
                new_w={j:z+uw.get(j,0) for j,z in w.items()}
                def cut(r):
                    return sum(b*new_w[j]*(new_y[i]-new_y[j]) for (i,j),b in edges.items()
                               if i in r and j not in r)
                init2=cut(set(P))
                assert init.intersection(init2) is not None and init2.lo>0
                diff=(cut(region)-init2)/init2
                actual=F(max(0,diff.lo,-diff.hi),SCALE)
                if largest_witness is None or actual>F(largest_witness['abs_fraction_lower']):
                    largest_witness={'ideal_inner':sorted(region-set(P)),
                        'clock_signs':[sy[j] for j in I], 'density_signs':[sw[j] for j in I],
                        'relative_change_interval':ends(diff),'abs_fraction_lower':str(actual)}
    return {'level':level,'clock_halfwidth_relative':str(factor/64),
            'density_relative_halfwidth':str(factor/100),'inlet_interval':ends(in_box),
            'cut_deviation_fraction_upper':None if error is None else str(error),
            'witness':largest_witness}


def run():
    mid,width=F(1,6),F(1,2**22)
    e=Box.hull(mid-width,mid+width)
    grid=[tube(e,k) for k in range(9)]
    for row in grid:
        row.pop('witness')
    good=[r['level'] for r in grid if r['cut_deviation_fraction_upper'] is not None
          and F(r['cut_deviation_fraction_upper'])<=F(1,50)]
    assert good
    adverse=tube(box(mid),0,True)['witness']
    assert F(adverse['abs_fraction_lower'])>F(1,50)
    return {'scan':grid,'first_certified_halving':good[0],'full_width_midpoint_witness':adverse}
