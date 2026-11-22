"""A finite-width Hilbert-measure control on the archived witness carrier."""
from fractions import Fraction as Q
import support


def template(code):
    nodes, rel = support.geometry(code)
    paths, rows, rhs = support.system(code)
    height = max(map(len,paths))
    center = {v:Q(max(p.index(v)+1 for p in paths if v in p),height+1)
              for v in nodes}
    for v in nodes:
        if all((u,v) not in rel and (v,u) not in rel for u in nodes):
            center[v] = Q(1,2)
    radius = Q(1,64)
    epsilon = Q(1,100)
    assert all(radius < c < 1-radius for c in center.values())
    assert all(center[b]-center[a] > 2*radius for a,b in rel if a in nodes and b in nodes)
    middle = support.fractions_on_paths(paths,center)
    deviation = [radius*sum(map(abs,row[:7])) for row in rows[-7:]]
    lower = [f-e for f,e in zip(middle,deviation)]
    upper = [f+e for f,e in zip(middle,deviation)]
    assert min(lower)>0 and sum(middle)==1
    return paths, center, radius, epsilon, lower, upper

def run():
    code = 2324
    nodes = support.I
    paths, center, radius, epsilon, lower, upper = template(code)
    d_min = 4*support.DELTA[0]-support.WINDOWS[-1][-1]
    d_max = 4*support.DELTA[1]-support.WINDOWS[0][0]
    assert -2*support.DELTA[1]+support.WINDOWS[0][0] > Q(-3,2)
    assert 2*support.DELTA[1] < Q(3,2)
    assert (1+epsilon)*4*d_max*max(upper)<1
    # Conditional on any fixed outer offset: the 7 clock intervals have raw
    # measure (2*r*D/3)^7. At fixed u, each density window contributes eps*w.
    # Multiplying componentwise lower bounds only underestimates the integral.
    clock_lower = (2*radius*d_min/3)**7
    masses = {}
    for m in support.MASSES:
        volume = clock_lower
        for f in lower:
            volume *= epsilon*m*d_min*f
        masses[str(m)] = {
            "W_over_D_interval": list(map(str,(m*(1-epsilon),m*(1+epsilon)))),
            "raw_inner_product_measure_lower_bound":str(volume),
            "approx_lower_bound":float(volume),
            "max_w_upper_including_width":float((1+epsilon)*m*d_max*max(upper))}
    for a,b in zip(support.MASSES,support.MASSES[1:]):
        assert (1+epsilon)*a < (1-epsilon)*b
    return {"carrier":code, "chains_excluding_inlet_and_exit":paths,
            "clock_center":{str(v):str(c) for v,c in center.items()},
            "clock_halfwidth":str(radius), "density_relative_halfwidth":str(epsilon),
            "dwell_affine_ranges_per_vertex":{str(v):list(map(str,p))
                 for v,p in zip(nodes,zip(lower,upper))}, "masses":masses,
            "exact_marked_density_graph_measure_under_raw_product":0,
            "unit":"raw conditional inner field measure given fixed outer offset; no physical Born normalization"}


if __name__=="__main__":
    import json
    print(json.dumps(run(),indent=2))
