"""Blind mixed clock probes of the finite action and conservative box enclosures."""
from fractions import Fraction as Q
from itertools import product
import json
import katalog
from katalog import n15,INNER
import sattel

PAST=n15.support.PAST
FUT=n15.support.FUTURE
D=Q(23,6)
PULSE=Q(1,1024)
ARM_ERROR=Q(1,10**11)
R=sattel.R


def group_geometry(rel,edge,y):
    minima=[j for j in INNER if not any((i,j) in rel for i in INNER)]
    first=min(y[j] for j in minima)
    group=sorted(j for j in minima if y[j]<=first+D/64)
    bins={1:[], -1:[]}
    for j in range(15):
        signs={1 if edge[i,j]>0 else -1 for i in group if (i,j) in edge}
        if len(signs)>1:
            raise ValueError('mixed signs at a receiver: grouped readout ambiguous')
        if signs:bins[signs.pop()].append(j)
    assert all(edge[3,j]==1 for j in group)
    return minima,group,bins


def observable(rel,edge,y,w,group,bins):
    code=n15.encode(rel,15)
    def normalized_action(clock):
        # Project units, including the constant density term.
        return Q(2,19)*n15.variation.matter_action(code,15,clock,[w[j] for j in range(15)])-Q(17,38)*sum(w.values())
    def mixed(left,right):
        total=Q(0)
        for a,b in product((-1,1),repeat=2):
            clock=[y[j]+PULSE*(a*left.get(j,0)+b*right.get(j,0)) for j in range(15)]
            assert all(clock[i]<clock[j] for i,j in rel)
            total+=a*b*normalized_action(clock)
        return 19*total/(4*PULSE**2)
    def direction(nodes,drift=False):
        return {j:(y[j]-y[3])/D if drift else 1 for j in nodes}
    source=direction(group)
    density=mixed({3:1},source)
    answers={}
    for s,target in bins.items():
        # Positive for a positive coefficient and an increasing clock; orientation is outgoing.
        answers[s]=D*(mixed(source,direction(target,True))-mixed(direction(group,True),direction(target)))
    clocks=[y[j] for j in range(15)]
    arm_clock=lambda h:[clocks[j]+h*source.get(j,0) for j in range(15)]
    net=19*(normalized_action(arm_clock(PULSE))-normalized_action(arm_clock(-PULSE)))/(2*PULSE)
    # The uniform clock derivative is incoming negative, outgoing positive in this orientation.
    plain={s:sum(edge[i,j]*w[j]*(y[j]-y[i]) for i in group for j in bins[s] if (i,j) in edge) for s in bins}
    assert answers==plain and density==sum(w[j] for j in group)
    return density,answers,net


def enclosure(case,wide):
    _,rel=n15.support.geometry(n15.TYPE)
    _,edge,_=katalog.structure(n15.TYPE)
    x=list(map(Q,case['center']));active=case['active']; y,w=sattel.fields(x,active)
    minima,U,V=group_geometry(rel,edge,y)
    assert set(U)==set(INNER)-set(active)
    yr={j:(R+(D/512 if wide else 0)) if j in INNER else Q(0) for j in y}
    wr={j:(R+(w[j]+R)/100 if wide else R) if j in active else Q(0) for j in w}
    # Freeze the source selection before each pulse; certify selection and order at every field value.
    max_first=min(y[i]+yr[i] for i in minima)
    min_first=min(y[i]-yr[i] for i in minima)
    assert all(y[i]+yr[i]<=min_first+D/64 for i in U)
    assert all(y[i]-yr[i]>max_first+D/64 for i in set(minima)-set(U))
    assert all(y[3]<y[j]-yr[j] and y[j]+yr[j]<y[7] for j in set(U).union(*V.values()))
    gap=min(y[j]-yr[j]-y[i]-yr[i] for i,j in rel)
    assert gap>2*PULSE
    for j in active:assert 0<w[j]-wr[j]<=w[j]+wr[j]<1
    bounds={}
    for s in V:
        lo=hi=Q(0)
        for i in U:
            for j in V[s]:
                if (i,j) not in edge:continue
                b=abs(edge[i,j]); dy=y[j]-y[i];spread=yr[i]+yr[j]
                lo+=b*(w[j]-wr[j])*(dy-spread)
                hi+=b*(w[j]+wr[j])*(dy+spread)
        bounds[str(s)]=[str(lo/len(U)),str(hi/len(U))]
    abs_error=38*D*ARM_ERROR/PULSE**2
    assert all(Q(v[0])>2*abs_error for v in bounds.values())
    center_density,center_arms,net=observable(rel,edge,y,w,U,V)
    # A vacuum control uses identical clocks with the interior and future empty.
    vacuum={j:w[j] if j in PAST else Q(0) for j in range(15)}
    control=observable(rel,edge,y,vacuum,U,V)
    assert control==(0,{1:0,-1:0},0)
    assert all(value==0 for j,value in enumerate(n15.variation.current_and_gradient(n15.encode(rel,15),15,
               [y[i] for i in range(15)],[vacuum[i] for i in range(15)])[1]) if j in INNER)
    # Exercise the full finite-pulse implementation at field-box corners with independently varying signs.
    for k in range(8):
        yc={j:v+(-1 if (j+k).bit_count()%2 else 1)*yr[j] for j,v in y.items()}
        wc={j:v+(-1 if (2*j+k).bit_count()%2 else 1)*wr[j] for j,v in w.items()}
        _,g,bins=group_geometry(rel,edge,yc)
        assert g==U and bins==V
        dens,r,_=observable(rel,edge,yc,wc,U,V)
        assert dens==0 and all(Q(bounds[str(s)][0])<=s*r[s]/len(U)<=Q(bounds[str(s)][1]) for s in V)
    return {'group':U,'positive_receivers':V[1],'negative_receivers':V[-1],'wide':wide,
            'unsigned_bounds_per_event':bounds,'density_center':str(center_density),
            'signed_channels_at_rational_center':{str(k):str(v) for k,v in center_arms.items()},
            'clock_gradient_at_approximate_center':str(net),'min_unpulsed_clock_gap_lower':str(gap),
            'hypothetical_channel_error_whole_group':str(abs_error),'matched_clock_vacuum':[0,0,0]}


def original_type():
    _,edges,maximal=katalog.structure(n15.TYPE)
    assert maximal=={14}
    inflow={i:b for (i,j),b in edges.items() if j==14}
    assert set(inflow)==set(INNER)-{14}
    capacity=sum(-b for b in inflow.values() if b<0)*D
    return {'terminal':14,'incident_coefficients':inflow,'terminal_density_strict_lower':str(Q(1,64)/capacity),
            'quiet_inner_sites_possible':False}


def run():
    # Recheck existence and local stationarity of the published roots.
    cert=sattel.run()
    assert cert['inequivalent_supports_shown']==2
    cases=json.loads((n15.ROOT/'Sattelpunkte.json').read_text())
    return {'stationary_type':original_type(),'arms_absolute_error_assumed':str(ARM_ERROR),
            'pulse_size':str(PULSE),'box_checks':[enclosure(c,wide) for c in cases for wide in (False,True)]}
