"""Paired finite-source response to a known model flow. Python standard library."""
from collections import Counter
from fractions import Fraction as F
from pathlib import Path
import json
import sys

HERE=Path(__file__).resolve().parent
UP=HERE/"upstream"
for p in ("variation_v0_1","current_calibration_v0_1","boundary_mass_sector_v0_1"):
    sys.path.insert(0,str(UP/p))
from charge import order, P, I, FUT, row, beta, delta, scale, add, mul
from current import Current
from variation import matter_action,current_and_gradient
from gluing import encode

M0=F(1,4)
M1=F(1)
TOL=F(1,50)
OFF=F(1,16)
nodes=(3,)+I+(7,)
moment2=scale(F(13,3072)*F(19,2),beta)
# theta=clock offset / Delta; the boundary clock law is uniform on the two equal lobes.
def summary(b): return {"exact_bounds":list(map(str,b)),"approx":float(sum(b)/2)}
def avg(poly): return add((poly[0],poly[0]),scale(poly[2],moment2))

def point(poly,offset):
    z=tuple(sorted((offset/delta[0],offset/delta[1])))
    return add((poly[0],poly[0]),mul(z,add((poly[1],poly[1]),scale(poly[2],z))))

def read_catalog():
    cat=json.loads((UP/"prefix_1564_two_event_v0_1/inputs/catalog.json").read_text())
    return sorted(int(k) for k,(a,_,b) in cat["ranks_pure_free_mixed"].items() if a==b==0)

def chains(rel):
    adj={u:[] for u in nodes}
    for u,v in sorted(rel):
        if u in adj and v in adj and not any((u,z) in rel and (z,v) in rel for z in nodes):
            adj[u].append(v)
    def paths(u):
        if u==7:
            yield (u,)
        else:
            for v in adj[u]:
                for tail in paths(v):
                    yield (u,)+tail
    return list(paths(3))

def midpoint_cells(paths,times):
    """Fractions of elapsed proper time on each worldline, closed end cells."""
    frac={v:F(0) for v in I}
    for path in paths:
        samples=path[1:-1]
        div=[F(0)]+[(times[u]+times[v])/2 for u,v in zip(samples,samples[1:])]+[F(1)]
        for v,l,r in zip(samples,div,div[1:]):
            assert l<r
            frac[v]+=(r-l)/len(paths)
    assert sum(frac.values())==1
    return frac

def flow_check(paths,rel,ideals,mass):
    edges=Counter()
    for path in paths:
        for edge in zip(path,path[1:]):edges[edge]+=mass/len(paths)
    flow=Current(range(15),rel,edges,{3:mass,7:-mass})
    assert all(flow.cut_mass(p)==mass for p in ideals)
    return len(ideals)

def polynomial(deg,u,frac):
    # With dimensionless clocks in units Delta, T_v=-2+4u + theta*(1-u).
    # beta*Delta^2/2=1/19, w_v=M*Delta*(4-theta)*frac_v.
    A=B=F(0)
    for v,d in zip(I,deg):
        b=row(d)
        A+=frac[v]*(sum((i-5)*c for i,c in enumerate(b)) - sum(b)*(-2+4*u[v]))
        B+=frac[v]*(b[3]-sum(b)*(1-u[v]))
    return (4*A/19,(4*B-A)/19,-B/19)

def check_source(code,u,frac,poly,t=F(1,4)):
    # Exact dimensionless coefficient test on a rational theta. All clocks and
    # integrated weights held fixed while shifting the past collar only.
    times=[F(0)]*15
    for v in P+FUT: times[v]=F(v-5)
    times[3]+=t
    for v in I:times[v]=-2+t+(4-t)*u[v]
    w=[F(1,8)]*15
    for v in I:w[v]=(4-t)*frac[v]
    tau=F(1,5)
    plus=[a+tau/2 if i in P else a for i,a in enumerate(times)]
    minus=[a-tau/2 if i in P else a for i,a in enumerate(times)]
    value=F(2,19)*(matter_action(code,15,minus,w)-matter_action(code,15,plus,w))/tau
    _,grad=current_and_gradient(code,15,times,w)
    assert value==-F(2,19)*sum(grad[i] for i in P)
    assert value==poly[0]+t*poly[1]+t*t*poly[2]
    for v in I:w[v]=0
    # Any nonzero collar weights remain; all direct past-to-future terms vanish.
    assert matter_action(code,15,minus,w)==matter_action(code,15,plus,w)
    assert matter_action(code,15,minus,[0]*15)==matter_action(code,15,plus,[0]*15)

def path_positions(path,rel,k):
    a,b=path[1:-1]
    # b has precisely one inner predecessor and a->b is a cover; a can have other successors.
    # Build the remaining times in a linear extension respecting the two fixed positions.
    ordered=[v for v in I if v not in (a,b)]
    # All nonselected vertices stay fixed above 1/2 in increasing topological order.
    # No other vertex precedes a or b, and b is maximal.
    times={a:F(1,2)-k,b:k}
    for j,v in enumerate(ordered,1):times[v]=F(1,2)+F(j,2*(len(ordered)+1))
    assert all(times[u]<times[v] for u,v in rel if u in I and v in I)
    return times

def main_audit():
    rows={}
    special=Counter()
    representative=None
    mean_ext={label:[] for label in ["linear","square"]}
    maxW={label:F(0) for label in mean_ext}
    ncuts=0
    disjoint_this_type=0
    for key in read_catalog():
        rel,deg=order(key)
        code=encode(rel,15)
        paths=chains(rel)
        pred=[sum(1<<j for j,u in enumerate(I) if (u,v) in rel) for v in I]
        ideals=[set(P)|{v for j,v in enumerate(I) if bits>>j&1} for bits in range(128)
                if all(not(bits>>j&1) or not(mask & ~bits) for j,mask in enumerate(pred))]
        for m in (F(0),M0,M1):
            flow_check(paths,rel,ideals,m)
        ncuts+=len(ideals)
        pos={}
        for v in I:
            distances=[(p.index(v),len(p)-1-p.index(v)) for p in paths if v in p]
            l=max(a for a,b in distances);r=max(b for a,b in distances)
            pos[v]=F(l,l+r)
        per_type={}
        for label,exponent in [("linear",1),("square",2)]:
            u={v:q**exponent for v,q in pos.items()}
            assert all(u[v]<u[z] for v,z in rel if v in I and z in I)
            frac=midpoint_cells(paths,u)
            wbound=M1*(4*delta[1]+F(3,32))*max(frac.values())
            assert wbound<1
            maxW[label]=max(maxW[label],wbound)
            poly=polynomial(deg,u,frac)
            check_source(code,u,frac,poly)
            expectation=avg(poly)
            mean_ext[label].append((key,expectation))
            per_type[label]={"p_over_M_coefficients_theta":list(map(str,poly)),"mean_p_over_M":summary(expectation)}
        means=[v[-1][1] for v in mean_ext.values()]
        # Nonpositive means have no admissible positive gain. Otherwise test interval separation.
        if any(m[1]<=0 for m in means):
            disjoint_this_type+=1
        elif all(m[0]>0 for m in means):
            if max((1-TOL)/m[1] for m in means)>min((1+TOL)/m[0] for m in means):
                disjoint_this_type+=1
        motifs=[p for p in paths if len(p)==4 and deg[I.index(p[2])]==1]
        if motifs:
            special["types"]+=1
            for path in motifs:
                for k in (F(1,3),F(11,24)):
                    u=path_positions(path,rel,k)
                    frac=midpoint_cells([path],u)
                    assert frac[path[1]]==F(1,4) and frac[path[2]]==F(3,4)
                    poly=polynomial(deg,u,frac)
                    check_source(code,u,frac,poly)
                    f=point(poly,OFF)
                    assert f[1]<0 if k==F(1,3) else f[0]>0
                if representative is None: representative=(key,path)
                special["routes"]+=1
        rows[str(key)]=per_type
    broad={}
    for label,results in mean_ext.items():
        vals=[m for _,m in results]
        lowest=(min(m[0] for m in vals),min(m[1] for m in vals))
        highest=(max(m[0] for m in vals),max(m[1] for m in vals))
        assert all(m[0]>0 or m[1]<0 or m==(0,0) for m in vals)
        broad[label]={"min_mean_p_per_M":summary(lowest),"max_mean_p_per_M":summary(highest),
                      "positive_means":sum(m[0]>0 for m in vals),"negative_means":sum(m[1]<0 for m in vals),
                      "zero_means":sum(m==(0,0) for m in vals),"max_density_weight_upper_at_M1":float(maxW[label])}
    return rows,{"orders":len(rows),"cuts_per_mass":ncuts,"marked_flux_checks":3*ncuts,
                 "known_conditional_masses":["0","1/4","1"],"all_cover_chain_profiles":broad,
                 "types_without_common_positive_gain_across_two_profiles_at_2pct":disjoint_this_type,
                 "two_event_routes":dict(special),"selected_order":representative[0],"selected_route":representative[1]}

