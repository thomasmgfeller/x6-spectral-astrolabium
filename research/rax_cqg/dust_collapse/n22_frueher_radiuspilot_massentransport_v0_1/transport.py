"""Exact packing certificates for the mass fraction bracketed at x=1/2."""
from fractions import Fraction as F
from itertools import combinations
from pilotfelder import shares, HALF, H, PAST, FUTURE


def packing(chains, nodes, x, w, proposal):
    crossing=[p for p in chains if x[p[0]][1]<HALF<x[p[-1]][0]]
    columns={p:shares(p,x) for p in crossing}
    mass_lo,mass_hi=(sum(w[j][k] for j in nodes) for k in (0,1))
    # Variables are path masses times the full clock duration. Their sum has
    # the same units as the integral weights. Singletons absorb each residual.
    prim={tuple(map(int,k.split(','))):F(v,10**12) for k,v in proposal["primal"].items()}
    assert prim.keys() <= columns.keys() and all(v>=0 for v in prim.values())
    used={j:sum(v*columns[p].get(j,(0,0))[1] for p,v in prim.items()) for j in nodes}
    scale=min([F(1)]+[w[j][0]/v for j,v in used.items() if v>0])
    assert all(scale*used[j]<=w[j][0] for j in nodes)
    lower=scale*sum(prim.values())/mass_hi
    dual={int(k):F(v,10**12) for k,v in proposal["dual"].items()}
    assert dual.keys() <= set(nodes) and all(v>=0 for v in dual.values())
    values=[sum(dual.get(j,0)*v[0] for j,v in col.items()) for col in columns.values()]
    floor=min(values)
    assert floor>0
    # For each crossing path p the scaled dual covers one objective unit.
    assert all(v/floor>=1 for v in values)
    upper=sum(w[j][1]*v for j,v in dual.items())/(floor*mass_lo)
    after={j for j in nodes if x[j][0]>HALF}
    before=set(nodes)-after
    # The first late residence cell starts at the midpoint of the last
    # earlier and first later marks. This second bound uses no LP witness.
    min_late_share=1-(max(x[j][1] for j in before)+max(x[j][1] for j in after))/2
    simple_upper=sum(w[j][1] for j in after)/(mass_lo*min_late_share)
    assert 0<min_late_share and 0<lower<=upper<=simple_upper<1
    def round_out(value, up):
        n=10**13
        return str(F(-(-value*n//1) if up else value*n//1,n))
    return dict(crossing=len(crossing),fraction=[round_out(lower,False),round_out(upper,True)],
                primal_scale=str(scale),dual_floor=str(floor),late_weight_upper=round_out(simple_upper,True))


def geometry(order, nodes, positive, x, w):
    inside={i for i,(l,r) in enumerate(x) if HALF-H<=l<=r<=HALF+H}
    possible={i for i,(l,r) in enumerate(x) if l<=HALF+H and r>=HALF-H}
    assert inside==possible
    occupied=sorted(inside & positive)
    zeros=sorted(inside-positive)
    def unrelated(i,j): return (i,j) not in order and (j,i) not in order
    contacts=[]
    for i in occupied:
        for j in zeros:
            if unrelated(i,j):
                past=sorted(k for k in positive if (k,i) in order and (k,j) in order)
                future=sorted(k for k in positive if (i,k) in order and (j,k) in order)
                if past and future:
                    contacts.append(dict(nodes=[i,j],past=past,future=future))
    width=max((n for n in range(1,len(occupied)+1) if any(all(unrelated(i,j) for i,j in combinations(p,2))
              for p in combinations(occupied,n))),default=0)
    masses={}
    for label,initial,final in (("3_to_7",[3],[7]),("all_collar",PAST,FUTURE)):
        missing=[j for j in nodes if not any((s,j) in order for s in initial)
                 or not any((j,t) in order for t in final)]
        total_l,total_h=(sum(w[j][k] for j in nodes) for k in (0,1))
        masses[label]=dict(inaccessible=missing,
            fractional_weight=[str(sum(w[j][0] for j in missing)/total_h),str(sum(w[j][1] for j in missing)/total_l)])
    return dict(positive=occupied,zero=zeros,material_antichain_width=width,contacts=contacts,paths=masses)
