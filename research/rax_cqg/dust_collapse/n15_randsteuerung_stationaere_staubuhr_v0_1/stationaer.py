"""Outward bounds on the interior clock equation over the incoming boxes."""
from basis import EDGES, E, FUTURE, INNER, ORDER, Q, dwells, force, scalar_coefficients
from intervalle import I,S

def box(low,high):return I(I.of(low).lo,I.of(high).hi)
DELTA=I.of(Q(3,722)).sqrt().sqrt()
CENTRE=[Q(k,8) for k in range(1,8)]
FAC=dwells(CENTRE)

def edge_coefficients(probe):
    # Coefficients of sum b_ij (v_j-v_i)(Y_j-Y_i) grouped by target j.
    v=dict.fromkeys(ORDER,0);v.update(dict(zip(INNER,probe)))
    by_target={j:dict.fromkeys(ORDER,0) for j in ORDER}
    for (i,j),b in EDGES.items():
        z=b*(v[j]-v[i]);by_target[j][j]+=z;by_target[j][i]-=z
    return by_target

def bound(probe,mass,off):
    e=off/DELTA;L=4-e;D=4*DELTA-off
    c=edge_coefficients(probe)
    y={j:I.of(j-5) for j in E};y[3]+=e;y.update({j:-2+e+L*centre for j,centre in zip(INNER,CENTRE)})
    z={j:I.of(0) for j in ORDER};weights={j:I.of(Q(1,8)) for j in FUTURE};weights.update({j:mass*D*f for j,f in zip(INNER,FAC)})
    for j,w in weights.items():
        for i,a in c[j].items():
            if a:z[i]+=w*a
    # Nominal-density contribution with common clock jitter for every occurrence of a site.
    central=sum((a*y[i] for i,a in z.items()),I.of(0)); clock_radius=sum(z[i].absmax() for i in INNER)*L.hi
    clock_error=Q(clock_radius,64*S*S)
    errors=I.of(0)
    for j,f in zip(INNER,FAC):
        slope=sum((a*y[i] for i,a in c[j].items() if a),I.of(0))
        rad=L*Q(sum(abs(c[j][i]) for i in INNER),64)
        # |f_actual*(1+jitter)-f_central| on the permitted box.
        werr=mass*D*(Q(1,64)+Q(1,100)*(f+Q(1,64)))
        errors+=werr*(Q(slope.absmax(),S)+Q(rad.hi,S))
    radius=I.of(clock_error).hi+errors.hi
    return I(central.lo-radius,central.hi+radius)


def run():
    result={}
    for M in (Q(1,4),Q(1),Q(4)):
        for side,mid in [('left',Q(-1,16)),('right',Q(1,16))]:
            ans={}
            for k,node in enumerate(INNER):
                probe=[int(i==k) for i in range(7)];bounds=[]
                for t in range(16):
                    a=mid-Q(1,32)+Q(t,256);bounds.append(bound(probe,M,box(a,a+Q(1,256))))
                ans[str(node)]=I(min(x.lo for x in bounds),max(x.hi for x in bounds)).rounded(6)
            witness=12 if M==1 else 11
            low,high=map(Q,ans[str(witness)]);assert high<0 or low>0
            result[f'{M}|{side}']={'minus_19_gradient':ans,'excludes_zero_at':witness}
    # Control on a changed collar: equal positive densities and unit-scaled gaps.
    ys={v:Q(k-5) for k,v in enumerate(ORDER)};ws=dict.fromkeys(ORDER,Q(1,8));g=force(ys,ws);density=scalar_coefficients(ys)
    assert all(g[j]==density[j]==0 for j in INNER)
    return {'box_checks':result,'stationary_control':{'clocks':[ys[v] for v in ORDER],'density':'1/8','duration_over_Delta':ys[7]-ys[3],'interior_equations_satisfied':14}}

if __name__=='__main__':
    import json
    print(json.dumps(run(),default=str,indent=2,sort_keys=True))
