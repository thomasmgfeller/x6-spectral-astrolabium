"""Independent exponential-series and direct-PMF checks of tail certificates.
SPDX-License-Identifier: Apache-2.0
"""
from pto_run import *
from decimal import Decimal,localcontext
from math import factorial
from ss_marginal import geometry,means,pi_bounds,deform
from pa_run import void_bounds

def decimal_cdf(mu,k):
    """Independent numerical cross-check, not the rigorous certificate."""
    with localcontext() as ctx:
        ctx.prec=100
        x=Decimal(mu.numerator)/Decimal(mu.denominator)
        term=(-x).exp();total=term
        for j in range(1,k+1):term=term*x/j;total+=term
        return +total

def audit():
    c=read(HERE/'contract.json');rows=read(HERE/'certificates.json');summary=read(HERE/'summary.json')
    args=(c['cdf_grid_digits'],c['cdf_upper_steps'],c['maximum_mean'])
    small=0
    for mu in (F(1,4),F(1,2),F(3,4),F(1)):
        exp=(1-void_bounds(mu)[1],1-void_bounds(mu)[0])
        for k in (0,1,2,5):
            polynomial=sum((mu**j/F(factorial(j)) for j in range(k+1)),F(0))
            exact=(exp[0]*polynomial,exp[1]*polynomial)
            certified,_=cdf(mu,k,*args)
            assert certified[0]<=exact[0]<=exact[1]<=certified[1]
            small+=1
    # A second expression for ln(2): certify its endpoints via exp(-x).
    lo,hi=log_bounds(F(2),c['log_series_terms'])
    assert 1-void_bounds(lo)[1]>=F(1,2)>=1-void_bounds(hi)[0]
    assert log_bounds(F(1),32)==(F(0),F(0))
    assert crossing((F(1),)*2,(F(2),)*2,32)[0:2]==(1,True)
    control=event_certificate((F(1),)*2,(F(2),)*2,c)
    assert control==event_certificate((F(2),)*2,(F(1),)*2,c)
    # A wide mean enclosure must retain the fixed-event interpretation.
    fallback=event_certificate((F(1),F(2)),(F(3),F(4)),c)
    assert not fallback['optimal_single_count_event_certified']
    # If the upward tail were omitted, normalization would falsely raise the CDF.
    rough,meta=cdf(F(10),10,8,1,2048);fine,_=cdf(F(10),10,*args)
    a=sum((F(10)**j/F(factorial(j)) for j in range(11)),F(0))
    z=a+F(10)**11/F(factorial(11))
    assert meta['omitted_weight_upper_grid_units']>0
    assert rough[0]<=fine[0]<=fine[1]<=rough[1] and fine[1]<a/z
    assert cdf(F(0),0,*args)[0]==(F(1),F(1))
    assert cdf(F(10),-1,*args)[0]==(F(0),F(0))
    invalid=0
    for call in [lambda:cdf(F(-1),1,*args),lambda:cdf(F(2049),1,*args),
                 lambda:cdf(F(1),1000,80,1,2048),lambda:cdf(F(1),1,0,768,2048),
                 lambda:crossing((F(1),F(2)),(F(2),F(3)),32),lambda:log_bounds(F(1,2),32)]:
        try:call()
        except AssertionError:invalid+=1;continue
        raise AssertionError('invalid input accepted')
    assert invalid==6
    inherited=read(HERE.parent/'spatial_search'/'marginal_diagnostic.json')
    old={r['index']:r for r in inherited['results']}
    scan=read(HERE.parent/'spatial_search'/'candidates.json.gz')
    strong=[r for r in scan if 'relative' in r and F(r['relative'][0])>F(1,5)]
    assert [r['index'] for r in strong]==[r['index'] for r in rows]
    assert len(scan)==512 and len(strong)==18
    assert all(F(r['relative'][1])<=F(1,5) for r in scan if 'relative' in r and r not in strong)
    w,z,ends=geometry();pi=pi_bounds();base=means(w,z,ends,pi)
    numerical=0;geometry_checks=0
    for row,s in zip(rows,strong):
        p=old[row['index']];k=p['interval_index']
        zz=deform(z,s['node'],s['axis'],s['sign'],F(s['step']))
        alt=means(w,zz,ends,pi)
        assert [[str(x) for x in v] for v in (base[k],alt[k])]==p['mean_intervals'];geometry_checks+=1
        assert row['interval_index']==k and row['endpoints']==p['endpoints']
        assert p['intrinsic_gates']['exact_intrinsic_moments']
        assert all(F(p['intrinsic_gates'][name])<100000 for name in ('landmark_condition_upper','moment_condition_upper'))
        assert row['optimal_single_count_event_certified']
        xlo,xhi=map(F,row['crossing_interval'])
        assert xlo.numerator//xlo.denominator==xhi.numerator//xhi.denominator==row['threshold']
        for r in row['endpoint_cdf_records']:
            value=decimal_cdf(F(r['mean']),row['threshold'])
            assert Decimal(r['cdf'][0])<=value<=Decimal(r['cdf'][1]);numerical+=1
            assert r['omitted_weight_upper_grid_units']>0
        # Reconstruct monotonic-mean event bounds from the rounded CDF records.
        a,b,d,e=[tuple(map(F,r['cdf'])) for r in row['endpoint_cdf_records']]
        vlo,vhi=map(F,row['event_difference'])
        assert abs(vlo-(b[0]-d[1]))<=F(2,10**60)
        assert abs(vhi-(a[1]-e[0]))<=F(2,10**60)
        assert 0<F(row['full_law_tv_lower'])<=vlo<=vhi<1
        assert F(row['full_law_tv_lower'])>F(1,4)
        assert vhi-vlo<=F(c['target_probability_interval_width'])
    assert summary['newly_excluded']==15 and summary['total_excluded']==18 and not summary['unresolved_indices']
    return dict(status='PASS',exact_small_mean_series_cases=small,logarithm_exponential_control=True,
        independent_direct_pmf_decimal_checks=numerical,decimal_precision=100,
        geometric_mean_enclosures_reproduced=geometry_checks,
        finite_grid_coverage=512,strong_gap_rows_checked=18,
        omitted_tail_negative_control=True,ambiguous_threshold_fallback_control=True,
        mean_swap_control=True,invalid_inputs_rejected=invalid,
        scope='Rigorous bounds use directed integer arithmetic and a geometric remainder. Independent exact small-mean series and direct Decimal PMF sums audit the implementation; numerical comparisons do not supply the proof.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
