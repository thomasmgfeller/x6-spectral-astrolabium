"""Five validated dust states and an explicit causal precursor register."""
from fractions import Fraction as F
import json

from geraet import TOTAL, MOMENTUM, EPSILON, trajectory, local_readout
from vorlage import read_json, reference


def run(directory):
    from algebra import box, hull, mid
    from frueh import Z, R
    from gemischt import Action, CLOCK, WEIGHT, N, ORDER, SCALE, certify, propose, validate_state
    earlier = read_json(directory/'Frueher_Zugriff.json')
    base = read_json(directory/'Randpraeparation.json')['reference']
    prefix = set(earlier['strict_past_sender'])
    assert prefix == {0,1,2,15} and {0,1,2} <= prefix
    assert {(0,1),(1,2),(2,Z),(Z,R)} <= ORDER
    initial = list(map(F, base['solution_centres'])) + [F(0),F(0)]
    start = list(map(mid,initial))
    mixed = Action(True)
    z_axis = len(CLOCK)+WEIGHT.index(Z)

    class Source:
        def __init__(self, strength):
            self.strength = strength
            self.fields = mixed.fields

        def evaluate(self, x, targets):
            g,H = mixed.evaluate(x,targets)
            g[z_axis] -= box(self.strength) if hasattr(x[0], 'lo') else mid(self.strength)
            return g,H

    cases = []
    anchor = None
    for dp,source in [(0,0),(-EPSILON,0),(EPSILON,0),(0,-EPSILON),(0,EPSILON)]:
        p = MOMENTUM + dp
        targets = [TOTAL,p]
        model = Source(source)
        proposal = propose(model,start,list(map(mid,targets)))
        domain,proof = certify(model,proposal,list(map(box,targets)),F(1,10**18))
        windows = validate_state(model,domain)
        y,w = model.fields(domain)
        assert all(w[i].lo == w[i].hi == SCALE//8 for i in (0,1,2))
        positions = trajectory(y,w,box(p),box(TOTAL), initial=(box(0),box(0)))
        read = local_readout(positions,w[2])
        assert all((v-exact).contains_zero() for v,exact in zip(read,(p,TOTAL)))
        # Compare the same physical inputs / same calibrated apparatus in all arms.
        readings = {'Y0':y[0], 'Y1':y[1], 'Y2':y[2], 'Y15':y[15],
                    'Yz':y[Z], 'Yr':y[R], 'wr':w[R], 'X1':positions[1][0],
                    'U1':positions[1][1], 'X2':positions[2][0], 'U2':positions[2][1]}
        if anchor is None:
            anchor = readings
        difference = {k:(v-anchor[k]) for k,v in readings.items()}
        cases.append({'delta_P':str(dp),'source_w':str(source),'proof':proof,
                      'window_times':windows,'P_read_exact':str(p),'T_read_exact':str(TOTAL),
                      'coast_travel_exact':[str(8*p),str(8*TOTAL)],
                      'difference_from_zero_arm':{k:v.data() for k,v in difference.items()}})
    # Callback-independent certificate over the complete predeclared region, also
    # covering the width of the archived exact nominal centre.
    half = F(1,10**4)
    old_radius = F(base['radius'])
    neighbourhood = [hull(v-half-old_radius,v+half+old_radius) for v in initial[:N]]
    neighbourhood += [hull(-half,half),hull(-half,half)]
    grad,_ = mixed.evaluate(neighbourhood)
    sum_region,g0_region = [-v/2 for v in grad[-2:]]
    assert not g0_region.contains_zero() and not (g0_region-F(1,8)).contains_zero()
    calibrated_reverse = (-1)*(-MOMENTUM)
    assert calibrated_reverse == MOMENTUM
    bound = earlier['fixed_clocks_and_sum']['minimax_absolute_error_lower_bound']
    return {'causal_prefix':sorted(prefix),'passive_pair':{'equal_prior_success':'1/2',
            'minimax_absolute_risk_lower_bound':bound},
            'control_region':{'radius':str(half),'G0':g0_region.data(),'sum_G':sum_region.data(),
                              'incompatible_G0':['0','1/8'],'reversed_gP':str(calibrated_reverse)},
            'model':'two cyclic registers; 0->1 coupled, 1->2 free',
            'targets':{'P':str(MOMENTUM),'T':str(TOTAL)},'states':cases,
            'physical_P3':{'NOT_RUN':60}}


if __name__ == '__main__':
    with reference() as root:
        print(json.dumps(run(root),indent=2,sort_keys=True))
