"""Routes, carrier inertia and the discrete Legendre update of each pointer."""
from fractions import Fraction as F

# Each entry gives target node, node supplying inertia, and optional sampled clock pair.
UP=((1,1,None),(2,2,None),(16,16,(15,16)),(18,18,(16,18)),(7,7,None))
COMMON=((1,1,None),(2,2,None),(16,16,None))
H_END=((18,18,(17,18)),(7,7,None))
T_END=((18,18,None),(7,7,(18,7)))
ROUTES={
    'positive_bridge':(UP,COMMON+H_END,COMMON+T_END),
    'cover_probes':(UP[:2]+((15,2,None),)+UP[2:],((17,0,None),)+H_END,((17,0,None),)+T_END),
}


def topology():
    from gemischt import ORDER,COEFF
    covers={(i,j) for i,j in ORDER if not any((i,k) in ORDER and (k,j) in ORDER for k in range(19))}
    def paths(end,p):
        if p[-1]==end:return [p]
        return [leaf for i,j in sorted(covers) if i==p[-1] and (j==end or (j,end) in ORDER)
                for leaf in paths(end,p+[j])]
    to_sender=paths(16,[0]);to_receiver=paths(18,[0])
    assert to_sender==[[0,1,2,15,16]]
    assert to_receiver==[[0,1,2,15,16,18],[0,17,18]]
    for route,tracks in ROUTES.items():
        for track in tracks:
            last=0
            for j,inertia,probe in track:
                assert (last,j) in ORDER and inertia not in (15,17)
                assert (last,j) in covers or (route=='positive_bridge' and (last,j)==(2,16))
                if probe: assert COEFF[probe]==1 and probe in covers
                last=j
    intermediate=[k for k in range(19) if (2,k) in ORDER and (k,16) in ORDER]
    assert intermediate==[15] and COEFF[2,16]==-9
    return {'from_0_to_sender':to_sender,'from_0_to_receiver':to_receiver,
            'bridge':{'link':[2,16],'intermediate':intermediate,'native_coefficient':-9},
            'extra_probe_nodes':[15,17],'free_inertia_sources_at_empty':[2,0]}


def forward(fields,route,q,velocity):
    from quelle import box
    y,w=fields['y'],fields['w']
    histories=[];factors=[]
    for track,initial,v in zip(ROUTES[route],q,velocity):
        hist={0:initial};coef={0:box(0)}
        last=0
        for j,inertia,probe in track:
            drift=v/w[inertia]
            sample=(y[probe[1]]-y[probe[0]]) if probe else box(0)
            hist[j]=hist[last]+sample+drift
            coef[j]=coef[last]+1/w[inertia]
            last=j
        histories.append(hist);factors.append(coef)
    return histories,factors
