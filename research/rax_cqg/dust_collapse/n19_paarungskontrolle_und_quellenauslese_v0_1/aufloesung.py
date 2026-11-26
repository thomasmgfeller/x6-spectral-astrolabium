"""Conservative error propagation; input uncertainties are test assumptions."""
from fractions import Fraction as F
from leser import old_clocks,read,PROBES
from proben import samples
import json


def run(previous,early):
    from quelle import hull,box,SCALE
    from gemischt import COEFF,ORDER,WINDOWS
    qlo,qhi=map(F,json.loads((previous/'Fenster.json').read_bytes())['positive_weight_reversal']['Q'])
    fixtures,_=samples(previous,early)
    ew=F(1,10**6)
    ec=F(1,10**8)
    signal_err=F(1,4000)
    results=[]
    for label,y,w in fixtures:
        cl=old_clocks({i:y[i] for i in range(4)},COEFF,ORDER)
        def value(weights,du,dh):
            return read(cl,weights,y[15]+du,y[17]+dh,COEFF,ORDER,WINDOWS)
        weights={i:w[i] for i in PROBES}
        exact=value(weights,box(0),box(0))
        ewbox=hull(1-ew,1+ew)
        ecbox=hull(-ec,ec)
        noisy=value({i:v*ewbox for i,v in weights.items()},ecbox,ecbox)
        T=exact['arms'][0]['delta']
        relative=noisy['arms'][0]['delta']/T-1
        eta=F(max(abs(relative.lo),abs(relative.hi)),SCALE)
        max_relative=[]; max_absolute=[]
        for arm in exact['arms']:
            magnitude=F(min(abs(arm['delta'].lo),abs(arm['delta'].hi)),SCALE)
            abs_sum=F(arm['absolute'].hi+exact['K0'].hi,SCALE)
            max_absolute.append(str(signal_err*magnitude/2))
            max_relative.append(str(signal_err*magnitude/abs_sum))
        # A single common gain error in all four reference channels is
        # admissible and biases a subtracted blind K0 by ew*K0 exactly.
        bias=ew*exact['K0']/T
        assert bias.lo>SCALE
        results.append({'name':label,'T_relative_error_bound':str(eta),
                        'equal_absolute_K_error_budget':max_absolute,
                        'equal_relative_K_error_budget':max_relative,
                        'unit_gain_error_in_null_in_units_of_negative_pulse':bias.data()})
    tag_err=max(F(row['T_relative_error_bound']) for row in results)
    expansion=(1+tag_err)*(1+signal_err)/((1-tag_err)*(1-signal_err))
    low=qlo/expansion; high=qhi*expansion
    assert F(998,1000)<low<high<F(1002,1000)
    return {'relative_weight_error':str(ew),'absolute_vacuum_clock_error':str(ec),
            'exact_initial_collar':True,'worst_T_relative_error':str(tag_err),
            'assumed_relative_differential_current_error':str(signal_err),
            'joint_reported_Q_bounds':list(map(str,(low,high))),
            'safe_equal_absolute_current_error_both_readings':str(min(F(v) for r in results for v in r['equal_absolute_K_error_budget'])),
            'safe_equal_relative_current_error_both_readings':str(min(F(v) for r in results for v in r['equal_relative_K_error_budget'])),
            'cases':results}


if __name__=='__main__':
    from vorgaenger import inputs
    with inputs() as a:print(json.dumps(run(*a),indent=2,sort_keys=True))
