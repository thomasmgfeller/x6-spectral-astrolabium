"""Independent controls for paired transfer and rational exponential bounds.
SPDX-License-Identifier: Apache-2.0
"""
from pa_run import *
from decimal import Decimal, localcontext

def audit():
    checks=0
    with localcontext() as ctx:
        ctx.prec=100
        for x in [F(0),F(1,10**8),F(1,20),F(1,4),F(1,2),F(1)]:
            lo,hi=void_bounds(x)
            y=1-(-Decimal(x.numerator)/Decimal(x.denominator)).exp()
            assert Decimal(lo.numerator)/Decimal(lo.denominator)-Decimal("1e-90")<=y<=Decimal(hi.numerator)/Decimal(hi.denominator)+Decimal("1e-90")
            checks+=1
    # Both marginals (100,100) vs (99,101); transfer 1 from a to b.
    toy=paired_bound({'a':F(99),'b':F(100)},{('a','b'):F(1)})
    assert F(toy['tv_upper'])<F(72,1000)
    # A bidirectional transfer changes individual memberships but cancels in the law.
    cycle=paired_bound({'a':F(10),'b':F(10)},{('a','b'):F(1),('b','a'):F(1)})
    assert F(cycle['tv_upper'])==0 and cycle['uncancelled_transfer_mean']=='0'
    # An unbacked rare label cannot be deleted or divided by zero.
    rare=paired_bound({}, {('a','b'):F(1,4)})
    assert F(rare['tv_upper'])>F(22,100)
    assert rare['zero_background_nonzero_difference_labels']==2
    assert paired_bound({'a':F(0)}, {})['tv_upper']=='0.00000000000000000000'
    bad=0
    for a,b in [({'a':F(-1)},{}),({}, {('a','b'):F(-1)}),({}, {('a','a'):F(1)})]:
        try:paired_bound(a,b)
        except AssertionError:bad+=1;continue
        raise AssertionError('invalid transfer accepted')
    # Independent exact J expression for toy; the paired bound must dominate it.
    r=[sqrt_bounds(F(v)) for v in [9900,10100]]
    actual_J_upper=400-2*sum(x[0] for x in r)
    assert actual_J_upper<F(toy['squared_root_distance_upper'])
    s=run();assert F(s['tv_upper'])<F(222,1000)
    return dict(status='PASS',exponential_cross_checks=checks,invalid_inputs_rejected=bad,
        toy=toy,balanced_cycle=cycle,unbacked_label=rare,actual_pair_tv_upper=s['tv_upper'],
        scope='Decimal is an independent numerical cross-check; alternating rational series supplies the enclosure proof. Exact transfer controls are not actual-pair transfer measurements.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(__import__('json').dumps(result))
