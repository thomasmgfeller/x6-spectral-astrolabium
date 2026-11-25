"""Compare the stationary densities with any positive routing of the existing material marks."""
from fractions import Fraction as F
from zertifikat import I,MID,WIDTH,construct,Box,lower,upper
from pruefung import support


def run(contrast):
    e=Box.hull(MID-WIDTH,MID+WIDTH)
    rel,_,y,w,_=construct(e,True)
    routes,_=support.paths_and_edges(rel)
    terminals={p[-1] for p in routes}
    assert terminals=={14} and len(routes)==6
    out={}
    for k in range(4):
        hy=(4-e)/int(64*2**k)
        eps=F(1,100*2**k)
        pert={j:y[j]+Box(-hy.hi,hy.hi) for j in I}
        weights={j:w[j]*Box.hull(1-eps,1+eps) for j in I}
        fraction=weights[14]/sum(weights.values())
        # A last midpoint, or any last interface between the last two sampled clocks.
        midpoint_ranges=[(2-(pert[p[-1]]+pert[p[-2]])/2)/(4-e) for p in routes]
        midpoint_min=min(map(lower,midpoint_ranges))
        tail_min=lower((2-pert[14])/(4-e))
        # Even allow independent 1% multiplicative errors on the reference path doses.
        def relax(a):
            return (1-F(1,100))*a/((1-F(1,100))*a+(1+F(1,100))*(1-a))
        phase_floor=F(contrast[str(k)]['amplitude_modulus_lower'])
        # Rotated integrands are in the cone Re exp[i(S-origin)] >= phase_floor.
        coh_obs_upper=upper(fraction)/phase_floor
        assert coh_obs_upper<relax(tail_min)*phase_floor
        out[str(k)]={'actual_fraction':[str(lower(fraction)),str(upper(fraction))],
            'midpoint_min':str(midpoint_min),'any_between_event_interface_min':str(tail_min),
            'midpoint_min_after_one_percent':str(relax(midpoint_min)),
            'any_interface_min_after_one_percent':str(relax(tail_min)),
            'same_pairing_abs_fraction_upper':str(coh_obs_upper)}
    return {'paths':routes,'terminal':14,'tested_levels':out}
