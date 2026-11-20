"""An independent density insertion on the original, unconstrained field support."""
from fractions import Fraction as F
from calibrate import I,order,row,point,summary,OFF,read_catalog

def run():
    limits={s:[] for s in (OFF,-OFF)}
    for key in read_catalog():
        _,deg=order(key)
        # At fixed W=sum w each visible or invisible site has E[w_v|W]=W/7.
        # The base clock measure is uniform in [-3/2,3/2], hence E[T_v]=0.
        a=F(sum(sum((i-5)*x for i,x in enumerate(row(d))) for d in deg),7)
        b=F(sum(row(d)[3] for d in deg),7)
        poly=(4*a/19,(4*b-a)/19,-b/19)
        for off in limits:limits[off].append(point(poly,off))
    out={}
    for off,vals in limits.items():
        assert all(v[0]>0 or v[1]<0 or v==(0,0) for v in vals)
        out[str(off)]={"positive_conditional_means":sum(v[0]>0 for v in vals),
             "negative_conditional_means":sum(v[1]<0 for v in vals),
             "zero_conditional_means":sum(v==(0,0) for v in vals),
             "min_mean_p_over_m_occ":summary(tuple(min(v[i] for v in vals) for i in range(2))),
             "max_mean_p_over_m_occ":summary(tuple(max(v[i] for v in vals) for i in range(2)))}
    return {"readout":"W=sum of seven inner integrated density weights; local unit-term source gives W=-2*dS/dzeta.",
            "conditional_variable":"m_occ=W/(T7-T3), dimensionless probe only",
            "scope":"symmetric auxiliary field measure at fixed outer clock; no imposed marks, no coherent Born pairing",
            "lobe_centres":out}

