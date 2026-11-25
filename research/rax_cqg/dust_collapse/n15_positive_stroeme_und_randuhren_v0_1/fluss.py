"""Positive causal-flow bounds, explicit attaining routes, and past-clock source certificates."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
from zertifikat import MID,WIDTH,I,P,FUT,construct,box,Box,SCALE,lower,upper,mag,saddle_phase,expansion,l1
from paketbreite import variation

ROOT=Path(__file__).resolve().parent
STEP=F(1,64)
PHASE_ERROR=F(1,10000)  # Error on the one relative interferometric phase for a subset.
EARLY=(4,5,6)


def pack(x):
    return [str(lower(x)),str(upper(x))]


def hull(xs):
    return Box(min(x.lo for x in xs),max(x.hi for x in xs))


def masks():
    return [frozenset(xs) for n in range(1,5) for xs in combinations(P,n)]


def key(g):
    return ''.join(map(str,sorted(g)))


def optimum(y,d,rel,edges,restricted):
    # Each R_v is the throughflow arriving at an early node. Every route reaching it is from P.
    first=2 if restricted else 0
    available=set(edges) if restricted else rel
    assert first==min(i for i in P if (i,11) in available)
    m={j:d[j]/(y[j]-y[0]) for j in EARLY}
    inlet_11=(d[11]-sum((y[11]-y[j])*m[j] for j in (4,5)))/(y[11]-y[first])
    m11=m[4]+m[5]+inlet_11
    m12=d[12]/(y[12]-y[6])
    m13=d[13]/(y[13]-y[6])
    m14=d[14]/(y[14]-y[13])
    plan={(0,4):m[4],(0,5):m[5],(0,6):m[6],(first,11):inlet_11,
          (4,11):m[4],(5,11):m[5],(6,12):m12,(6,13):m13,(13,14):m14,
          (6,7):m[6]-m12-m13,(11,7):m11,(12,7):m12,(13,7):m13-m14,(14,7):m14}
    assert set(plan)<=available and all(x.lo>0 for x in plan.values())
    value=sum(m.values())+inlet_11
    # Dual lower bound for arbitrary positive flow using the node-11 moment.
    remaining={j:(y[j]-y[first])/(y[11]-y[first]) for j in (4,5)}
    assert min(v.lo for v in remaining.values())>0
    bound=m[6]+sum(remaining[j]*m[j] for j in (4,5))+d[11]/(y[11]-y[first])
    assert value.intersection(bound) is not None
    # Independent incidence sums for each constructed moment and Kirchhoff equation.
    for j in I:
        arrivals=[(i,x) for (i,v),x in plan.items() if v==j]
        residue=sum(x*(y[j]-y[i]) for i,x in arrivals)-d[j]
        balance=sum(x for i,x in arrivals)-sum(x for (i,v),x in plan.items() if i==j)
        assert residue.lo<=0<=residue.hi and balance.lo<=0<=balance.hi
    return value.intersection(bound),plan


def one(e,level,origin):
    rel,edges,y,w,center=construct(e,True)
    w.update(dict.fromkeys(P,box(F(1,8))))
    hy=(4-e)*F(1,64*2**level)
    hw={j:w[j]*F(1,100*2**level) for j in I}
    dy={j:Box(-hy.hi,hy.hi) for j in I}
    dw={j:Box(-hw[j].hi,hw[j].hi) for j in I}
    yp={j:z+dy.get(j,box(0)) for j,z in y.items()}
    wp={j:z+dw.get(j,box(0)) for j,z in w.items()}
    assert all(yp[i].hi<yp[j].lo for i,j in rel)
    assert all(i not in P or yp[j].lo-yp[i].hi>box(STEP).hi for i,j in rel)
    # The stationary density moments D_v=19w_v are defined separately from off-shell currents.
    d={j:19*wp[j] for j in I}
    ports={}
    k_terms={}
    for group in masks():
        subset={(i,j):b for (i,j),b in edges.items() if i in group and j not in P}
        c0=center if group==frozenset(P) else sum(b*w[j]*(y[i]-y[j]) for (i,j),b in subset.items())
        ports[key(group)]=c0+variation(subset,y,w,dy,dw)
        k_terms[key(group)]=-sum(b*wp[j] for (i,j),b in subset.items())/38
    total=ports['0123']
    assert total.lo>0
    for j in EARLY:
        assert [edges.get((i,j),0) for i in P]==[-8,16,-9,1]
        assert {i for i in I if (i,j) in rel}==set()
    # For minimal nodes Gamma = -sum b*(Yj-Yi)^2 = 19 + 2(1+e) * dy_j, exactly.
    local={j:wp[j]*(19+2*(1+e)*dy[j]) for j in EARLY}
    real_lower=sum(local[j]/(yp[j]-yp[0]) for j in EARLY)
    needed_all,plan_all=optimum(yp,d,rel,edges,False)
    needed_kernel,plan_kernel=optimum(yp,d,rel,edges,True)
    cover_lower=sum(d[j]/(yp[j]-yp[3]) for j in EARLY)
    # 14 is reached by every saturated material path 3 -> 7, directly from 12 or 13.
    immediate={i for i in I if (i,14) in rel and not any((i,k) in rel and (k,14) in rel for k in I)}
    assert immediate=={12,13} and all((j,14) in rel for j in I if j!=14)
    cover_upper=d[14]/(yp[14]-hull([yp[12],yp[13]]))
    assert cover_lower.lo>cover_upper.hi and min(needed_all.lo,real_lower.lo)>total.hi
    phase_spread=mag(saddle_phase(edges,y,w)-box(origin))+l1(expansion(edges,y,w,hy,hw))
    return {'ports':ports,'k':k_terms,'Q':total,'all':needed_all,'kernel':needed_kernel,
            'true_local':real_lower,'cover_required':cover_lower,'cover_max':cover_upper,
            'phase':phase_spread,'plans':[plan_all,plan_kernel]}


def run():
    _,edges,y,w,c=construct(box(MID),True)
    w.update(dict.fromkeys(P,box(F(1,8))))
    ref=saddle_phase(edges,y,w)
    origin=(lower(ref)+upper(ref))/2
    # No width: record the optimal primal construction at the central history.
    amounts={j:19*w[j] for j in I}
    rel=construct(box(MID),True)[0]
    nominal={}
    for label,restriction in [('all',False),('kernel',True)]:
        value,route=optimum(y,amounts,rel,edges,restriction)
        nominal[label]={'minimum':pack(value),'minimum_over_stationary_charge':pack(value/c),
                        'flow':{f'{i}->{j}':pack(n) for (i,j),n in route.items()}}
    ports0={key(g):pack(sum(b*w[j]*(y[i]-y[j]) for (i,j),b in edges.items() if i in g and j not in P))
            for g in masks()}
    levels={}
    for level in range(4):
        cells=[one(Box.hull(MID-WIDTH+2*WIDTH*F(k,16),MID-WIDTH+2*WIDTH*F(k+1,16)),level,origin)
               for k in range(16)]
        stats={n:pack(hull([x[n] for x in cells])) for n in ('Q','all','kernel','true_local','cover_required','cover_max')}
        stats['replacement_to_Q_lower']=str(min(lower(x['all'])/upper(x['Q']) for x in cells))
        stats['action_moment_to_Q_lower']=str(min(lower(x['true_local'])/upper(x['Q']) for x in cells))
        readings={}
        for g in masks():
            k=key(g)
            port=hull([x['ports'][k] for x in cells])
            kg=hull([x['k'][k] for x in cells])
            # A common phase is immaterial. This conservative envelope is valid for either arm
            # and all intermediate t in the argument derivative of Z(t).
            half=max(x['phase'] for x in cells)+STEP**2*mag(kg)+STEP*mag(port)/19
            assert 2*half < F(1,2)
            cosine=1-2*half**2
            assert cosine>0
            err=F(19)*PHASE_ERROR/(2*STEP)
            readings[k]={'range':pack(port),'phase_read_range_with_error':[str(lower(port)-err),str(upper(port)+err)],
                         'relative_phase_worst_abs':str(2*STEP*mag(port)/19),'amplitude_modulus_lower':str(1-half**2/2)}
        margin=[]
        for group in masks():
            if 0 not in group or len(group)==4:continue
            other=frozenset(P)-group
            upper_min=min(F(readings[key(g)]['phase_read_range_with_error'][1]) for g in (group,other))
            assert upper_min<0
            margin.append(-upper_min)
        stats['minimum_negative_channel_margin_with_read_noise']=str(min(margin))
        stats['ports']=readings
        levels[str(level)]=stats
    return {'past_ports_at_midpoint':ports0,'at_midpoint':nominal,'levels':levels,
            'pulse_step':str(STEP),'relative_phase_absolute_error_rad':str(PHASE_ERROR),
            'reference_rotation':str(origin),'tiles_per_level':16}


if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
