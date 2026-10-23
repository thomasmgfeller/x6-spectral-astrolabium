"""Independent exact geometric identities and direct decimal Poisson checks.
SPDX-License-Identifier: Apache-2.0
"""
from cm_run import *
from decimal import Decimal, localcontext
from functools import lru_cache

def direct_q(a,b):
    d=[v-u for u,v in zip(a,b)]
    return d[0]**2-d[1]**2-d[2]**2

@lru_cache(None)
def direct_cdf(mu,k):
    # Independent direct exp/PMF sum starting at zero, no mode normalization.
    with localcontext() as ctx:
        ctx.prec=110
        x=Decimal(mu.numerator)/Decimal(mu.denominator)
        term=(-x).exp();value=term
        for j in range(1,k+1):
            term=term*x/j;value+=term
        return +value

def audit():
    frozen();c=read(HERE/'contract.json');w,z,ends=geometry()
    s=read(HERE/'structure.json');rays=read(HERE/'directions.json');rows=read(HERE/'candidates.json')
    summary=read(HERE/'summary.json');A=[[F(v) for v in row] for row in s['difference_matrix']]
    Q=[[F(v) for v in row] for row in s['inverse']]
    assert all(dot(row,col)==int(i==j) for i,row in enumerate(A) for j,col in enumerate(zip(*Q)))
    identities=rank_blocks=0
    for node in range(5,21):
        gradients=[[2*g*(z[node][k]-z[a][k]) for k,g in enumerate((1,-1,-1))] for a in range(4)]
        diff=[[v-u for u,v in zip(gradients[0],row)] for row in gradients[1:]]
        assert diff==A and determinant(diff)!=0;rank_blocks+=1
        for d in ([F(1,1000),F(-1,700),F(1,900)],[-F(1,13),F(1,17),F(-1,19)]):
            x=[v+t for v,t in zip(z[node],d)]
            changes=[direct_q(z[a],x)-direct_q(z[a],z[node]) for a in range(4)]
            rhs=[v-changes[0] for v in changes[1:]]
            assert rhs==[dot(row,d) for row in A]
            assert [dot(row,rhs) for row in Q]==d
            assert max(map(abs,d))<=2*F(s['inverse_infinity_norm'])*max(map(abs,changes))
            identities+=1
    # A singular anchor frame must fail, rather than reporting spurious rank.
    broken=[row[:] for row in A];broken[2]=broken[1][:]
    assert determinant(broken)==0
    try:inv(broken)
    except (StopIteration,ZeroDivisionError):pass
    else:raise AssertionError('singular landmarks accepted')
    isolation=0
    for ray in rays:
        zz=moved(z,ray,F(1,1000));p,j=ray['nodes']
        alone=deform(z,p,ray['axis'],1,F(1,1000)*F(ray['velocities'][0]))
        for k,(a,b) in enumerate(ends):
            if j not in (a,b):
                assert direct_q(zz[a],zz[b])==direct_q(alone[a],alone[b]);isolation+=1
        # Independent high-precision derivative evaluation in the boost frame.
        with localcontext() as ctx:
            ctx.prec=110
            decimal=lambda x:Decimal(x.numerator)/Decimal(x.denominator)
            boost=boosted(z);terms=[]
            for node,velocity in zip(ray['nodes'],map(F,ray['velocities'])):
                x=boost[0][ray['axis']]-boost[node][ray['axis']]
                terms.append(decimal(x)*decimal(direct_q(z[0],z[node])).sqrt()*decimal(velocity))
            residual=abs(sum(terms))/sum(map(abs,terms))
            assert residual<=Decimal(ray['aggregate_derivative_relative_residual_upper'])
            assert all(t!=0 for t in terms) # The component derivatives did not disappear.
    assert {(r['ray'],r['step']) for r in rows}=={(ray['index'],h) for ray in rays for h in c['steps']}
    assert len(rows)==len({r['index'] for r in rows})==420
    assert Counter(r['status'] for r in rows)==summary['states']
    order_checks=gap_checks=probability_checks=0
    for row in rows:
        zz=moved(z,rays[row['ray']],F(row['step']))
        # Direct pairwise order check, independent of certify_order.
        qs=[];ts=[];same=True
        for i in range(21):
          for j in range(i+1,21):
            q=direct_q(zz[i],zz[j]);dt=zz[j][0]-zz[i][0];qs.append(abs(q))
            same &= ((q>0 and dt>0)==w['full_order'][i][j] and (q>0 and dt<0)==w['full_order'][j][i])
            if q>0:ts.append(abs(dt))
        margin=min(qs)>=F(99,10**10) and min(ts)>=F(99,10**10)
        assert (row['status']=='ORDER_OR_MARGIN_REJECTED') == (not same or not margin)
        order_checks+=1
        if row['status']=='GAP_BELOW_GATE':assert F(row['relative'][1])<=F(1,5);gap_checks+=1
        if 'law' not in row:continue
        assert F(row['relative'][0])>F(1,5)
        law=row['law'];assert (row['status']=='LAW_EXCLUDED')==(F(law['tv_lower'])>F(1,4))
        for event in law.get('event_checks',[]):
            cert=event['certificate'];k=cert['threshold']
            for record in cert['endpoint_cdf_records']:
                answer=direct_cdf(F(record['mean']),k)
                lo,hi=map(Decimal,record['cdf']);assert lo<=answer<=hi
                assert int(record['omitted_weight_upper_grid_units'])>0
                probability_checks+=1
    # Inherited continuous certificate lifts under all other support movements.
    joint=read(HERE.parent/'joint_ray_obstruction'/'certificate.json')
    assert joint['statistics']['X']['interval']==[2,15]
    assert joint['statistics']['Y']['interval']==[15,1]
    assert z[2][0]<z[15][0]<z[1][0]
    assert F(joint['full_law_tv_lower'])>F(1,4)
    # Negative control: preserving a scalar sum does not preserve a labeled law.
    # Two independent Poisson means (1,3) versus (2,2) give identical sum laws,
    # while their first-coordinate P(N=0) differs strictly.
    assert 1+3==2+2
    assert direct_cdf(F(1),0)>direct_cdf(F(2),0)
    assert lower_bound((F(1),F(1)),(F(2),F(2)))[1]>0
    return dict(status='PASS',exact_finite_displacement_identities=identities,
        independent_rank_three_blocks=rank_blocks,total_exact_rank=3*rank_blocks,
        off_partner_interval_isolation_checks=isolation,decimal_derivative_checks=len(rays),
        complete_finite_grid=420,direct_order_margin_checks=order_checks,gap_exclusions_checked=gap_checks,
        direct_110_digit_cdf_checks=probability_checks,inherited_joint_event_lift=True,
        negative_controls=['singular landmark frame rejected','equal scalar sum does not imply equal labeled Poisson law'],
        scope='Independent arithmetic/implementation audit; no sampling experiment or peer-review claim.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
