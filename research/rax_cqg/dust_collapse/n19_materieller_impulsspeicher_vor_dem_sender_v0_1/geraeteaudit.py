"""Cross-check reduced dust equations against the unreduced link variations."""
from fractions import Fraction as F
from itertools import product

from geraet import EPSILON, MOMENTUM, TOTAL, full_link_action, trajectory, local_readout, fixed_target_coupling
from vorlage import read_json


def difference(fn, x):
    step = F(1,8192)
    return (fn(x+step)-fn(x-step))/(2*step)


def link_test():
    # Use non-reference, non-stationary dust clocks and non-identical masses.
    y = [F(-49,10), F(-16, 5)]
    w = [0,F(2,9),F(3,10)]
    qzero = (F(3,7),F(-1,3))
    tests = 0
    for gain, p, t in product((-1,0,1),(F(-17,3),F(0),F(1,8)),(F(0),F(2,5))):
        q = trajectory(y,w,p,t,gain,qzero)
        def replace(seq,i,v):
            parts = list(seq)
            parts[i] = v
            return parts
        derived = []
        for i in range(3):
            pair = []
            for j in (0,1):
                def displaced(value):
                    changed = replace(q,i,replace(q[i],j,value))
                    return full_link_action(y,w,changed,gain)
                pair.append(difference(displaced,q[i][j])/2)
            derived.append(pair)
        assert derived == [[-p,-t],[0,0],[p,t]]
        d_y = [difference(lambda v:full_link_action(replace(y,i,v),w,q,gain),y[i])/2
               for i in (0,1)]
        assert d_y == [gain*p,t-gain*p]
        assert local_readout(q,w[2]) == (p,t)
        mirror = trajectory(y,w,-p,t,-gain,(-qzero[0],qzero[1]))
        assert all(x == -xm and u == um for (x,u),(xm,um) in zip(q,mirror))
        tests += 1
    return tests


def run(directory,data):
    from algebra import box, hull
    from gemischt import Action, CLOCK, WEIGHT, Z
    # Rebuild every coefficient from the partial order as in the original action.
    from quelle import DATA
    _,_,order,_,_,_ = DATA
    model = Action(True)
    checked = 0
    change_lower_bounds = {}
    for state in data['states']:
        proof = state['proof']
        radius = F(proof['radius'])
        domain = [hull(F(v)-radius,F(v)+radius) for v in proof['solution_centres']]
        y,w = model.fields(domain)
        current = [box(0) for _ in range(19)]
        density = [box(19) for _ in range(19)]
        for i,j in order:
            between = sum((i,k) in order and (k,j) in order for k in y)
            coef = (1,-9,16,-8)[between] if between < 4 else 0
            gap = y[j]-y[i]
            flow = coef*w[j]*gap
            current[i] += flow
            current[j] -= flow
            density[j] += coef*gap*gap
        source = F(state['source_w'])
        for i in CLOCK:
            assert current[i].contains_zero()
        for i in WEIGHT:
            assert (density[i]-(source if i == Z else 0)).contains_zero()

        # Construct coordinate enclosures from stored positions at 0 and the
        # incoming data; differentiate the two link actions at fixed positions.
        p,t = F(state['P_read_exact']),F(state['T_read_exact'])
        q = trajectory(y,w,box(p),box(t))
        d1_p = w[1]*(q[1][0]-q[0][0]+y[0]-y[1]+1)
        d1_t = w[1]*(q[1][1]-q[0][1]+y[1]+4)
        d2_p,d2_t = local_readout(q,w[2])
        assert all(v.contains_zero() for v in
                   (d1_p-p,d1_t-t,d1_p-d2_p,d1_t-d2_t,d2_p-p,d2_t-t))
        assert (current[0]-d1_p).contains_zero()
        assert (sum(current[:4])-d1_t).contains_zero()
        if source:
            diffs = state['difference_from_zero_arm']
            for label in ('Y0','Y1','Y2','Y15','Yr','wr','X1','U1','X2','U2'):
                lo,hi = map(F,diffs[label])
                assert lo*hi>0
            change_lower_bounds[str(source)] = str(min(abs(F(v)) for v in diffs['Y0']))
        checked += 1

    original = read_json(directory/'Frueher_Zugriff.json')
    separation = list(map(F,original['fixed_clocks_and_sum']['G0_plus_minus_separation']))
    slope_hi = F(original['fixed_clocks_and_sum']['slope_G0'][1])
    risk = F(data['passive_pair']['minimax_absolute_risk_lower_bound'])
    assert risk == -EPSILON*slope_hi
    assert 0 <= 2*risk - separation[0] <= F(1,10**32)
    # Nearest of three prepared values. Each of the two independent positions
    # may have an absolute error up to eta, with no distribution assumption.
    eta_sup = EPSILON/(4*F(1,8))
    assert 2*F(1,8)*eta_sup == EPSILON/2
    return {'fixed_G0_coupling':fixed_target_coupling(), 'exact_variation_cases':link_test(),'checked_coupled_states':checked,
            'free_interior_rows_per_case':20,'boundary_rows_per_case':2,
            'sender_arms_abs_Y0_change_lower_bounds':change_lower_bounds,
            'strict_per_position_error_for_three_settings':str(eta_sup),
            'neighbouring_preparations_coast_travel_gap':str(8*EPSILON)}
