"""Uniform cut-charge sign on the same fixed finite-width rule for every carrier."""
from collections import Counter
from fractions import Fraction as Q
from functools import lru_cache
import json
from coherence import add, bounds, mul, sub
import support
from tube import template


@lru_cache(maxsize=None)
def charge_on_tiles(degree, center, halfwidth, epsilon):
    coeffs = [((1,-9,16,-8)[j] if j<4 else 0) for j in (degree+3-i for i in range(4))]
    u = (center-halfwidth,center+halfwidth)
    result = []
    for left,right in support.WINDOWS:
        for j in range(32):
            h=(right-left)/32
            e=mul((left+j*h,left+(j+1)*h),(1/support.DELTA[1],1/support.DELTA[0]))
            z=(-2+4*u[0]+(1-u[0])*e[0],-2+4*u[1]+(1-u[1])*e[1])
            past=add(bounds(sum(b*(i-5) for i,b in enumerate(coeffs))),mul(bounds(coeffs[3]),e))
            response=sub(past,mul(bounds(sum(coeffs)),z))
            result.append(mul(mul((1-epsilon,1+epsilon),response),
                              mul(bounds(Q(1,19)),sub(bounds(4),e))))
    return result


@lru_cache(maxsize=None)
def per_node(degree, center, halfwidth, epsilon, low, high):
    # Outward fixed-point rounding after each complete one-node enclosure.
    # Subsequent sums and sign checks use exact integers.
    scale = 10**9
    result=[]
    for interval in charge_on_tiles(degree,center,halfwidth,epsilon):
        a,b = mul((low,high),interval)
        result.append((a*scale//1,-((-b*scale)//1)))
    return result


def run():
    totals=Counter()
    patterns=Counter()
    by_type={}
    d_max=4*support.DELTA[1]-support.WINDOWS[0][0]
    d_max_lower=4*support.DELTA[0]-support.WINDOWS[0][0]
    for code in support.catalogue():
        _, centers, r, eps, low, high = template(code)
        if (1+eps)*4*d_max*max(high)>=1:
            assert (1+eps)*4*d_max_lower*max(high)>1
            totals["full_box_crosses_density_cap"]+=1
            by_type[str(code)]={"full_box":False}
            continue
        _,rel=support.geometry(code)
        deg=[sum((u,v) in rel for u in support.I) for v in support.I]
        pieces=[per_node(deg[j],centers[v],r,eps,low[j],high[j]) for j,v in enumerate(support.I)]
        intervals=[(sum(pair[0] for pair in tile),sum(pair[1] for pair in tile))
                   for tile in zip(*pieces)]
        lobes=[(min(x[0] for x in side),max(x[1] for x in side))
               for side in (intervals[:32],intervals[32:])]
        signs=["+" if a>0 else "-" if b<0 else "?" for a,b in lobes]
        pattern="".join(signs)
        patterns[pattern]+=1
        totals["full_box_inside_for_both_masses"]+=1
        by_type[str(code)]={"full_box":True,"p_over_M_lobe_bounds_nanounits":lobes,"signs":pattern}
    assert len(by_type)==1048 and sum(totals.values())==1048
    return {"counts":dict(totals),"sign_patterns_left_right":dict(patterns),
            "nanounits_per_unit":10**9,"by_type":by_type}


if __name__=="__main__":
    print(json.dumps(run(),sort_keys=True))
