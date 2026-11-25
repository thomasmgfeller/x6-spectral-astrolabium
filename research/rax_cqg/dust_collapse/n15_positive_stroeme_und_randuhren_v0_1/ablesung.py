"""A two-port counting control and a bound on a specified time-blurring readout."""
from fractions import Fraction as F
from math import factorial
import json
from pathlib import Path
from fluss import STEP,PHASE_ERROR

ROOT=Path(__file__).resolve().parent


def exp_minus_upper(x):
    # Truncation from below of exp(x) for positive rational x.
    x=F(int(x*10**6),10**6)
    bound=1/sum(x**j/factorial(j) for j in range(50))
    return F(-((-bound.numerator*10**12)//bound.denominator),10**12)


def design(cert):
    levels={}
    for level,v in cert['levels'].items():
        p=v['ports']
        qlo,qhi=map(F,p['0123']['range'])
        nlo,nhi=map(F,p['1']['range'])
        assert nhi<min(F(p[str(k)]['range'][0]) for k in (0,2,3))
        # Uniform four-channel confusion matrix, exact threshold eta=Q/(Q-4q_min).
        eta_low=qlo/(qlo-4*nlo)
        eta_top=qhi/(qhi-4*nhi)
        neg_share=-F(p['13']['range'][1])
        phase=-2*STEP*nhi/19
        visibility=F(p['1']['amplitude_modulus_lower'])
        assert 0<phase<1 and visibility>0
        gap=visibility*(phase-phase**3/6)/2-PHASE_ERROR
        levels[level]={'uniform_blur_threshold_interval':list(map(str,(eta_low,eta_top))),
                       'fixed_total_minimum_L1_change_lower':str(2*neg_share),
                       'noisy_vacuum_minus_signal_probability_lower':str(gap)}
    n=2**18
    threshold=F(1,200)
    gap=F(levels['0']['noisy_vacuum_minus_signal_probability_lower'])
    assert gap>threshold>PHASE_ERROR
    return {'levels':levels,'trials_per_preparation':n,'difference_threshold':str(threshold),
            'false_positive_upper':str(exp_minus_upper(n*(threshold-PHASE_ERROR)**2)),
            'miss_upper':str(exp_minus_upper(n*(gap-threshold)**2))}


def simulate(results,numerical,seed=1767356):
    import numpy as np
    n=results['trials_per_preparation']
    rng=np.random.default_rng(seed)
    p0=numerical['empty_interior']['1']['Y_port_probability']
    p1=numerical['quadrature_by_level_order']['0_4']['1']['Y_port_probability']
    ref=int(rng.binomial(n,p0))
    signal=int(rng.binomial(n,p1))
    diff=F(ref-signal,n)
    return {'seed':seed,'numpy_version':np.__version__,'vacuum_Y_counts':ref,
            'sample_Y_counts':signal,'per_setting':n,'observed_difference':str(diff),
            'crosses_threshold':diff>=F(results['difference_threshold'])}


if __name__=='__main__':
    cert=json.loads((ROOT/'zertifikate.json').read_text())
    q=json.loads((ROOT/'gegenrechnung.json').read_text())
    report=design(cert)
    print(json.dumps({'design':report,'counting_example':simulate(report,q)},sort_keys=True,indent=2))
