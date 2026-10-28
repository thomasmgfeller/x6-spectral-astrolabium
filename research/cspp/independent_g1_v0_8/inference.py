"""One-sided exact binomial inference using rational arithmetic, no normal approximation."""
from fractions import Fraction as F
from functools import lru_cache
from math import comb
from flint import arb
from support import check,pack,plan,unpack

def tail(k,n,p):
    p=F(p)
    a,b=p.numerator,p.denominator
    return F(sum(comb(n,j)*a**j*(b-a)**(n-j) for j in range(k,n+1)),b**n)

@lru_cache(None)
def cp_lower(k,n,alpha):
    check(0<=k<=n and 0<F(alpha)<1,'binomial inputs')
    if k==0:return F(0),F(0)
    lo,hi=F(0),F(1)
    for _ in range(72):
        mid=(lo+hi)/2
        if tail(k,n,mid)<=F(alpha):lo=mid
        else:hi=mid
    check(tail(k,n,lo)<=F(alpha)<=tail(k,n,hi),'exact CP enclosure')
    return lo,hi

def summarize(rows):
    p=plan();M=p['realizations_per_density'];alpha=F(p['statistics']['one_sided_alpha_per_field_cell'])
    out=[]
    for d,nu in enumerate(p['nu']):
        for e in p['epsilon']:
            tests=[]
            subset=[r for r in rows if r['density_index']==d and r['epsilon']==e]
            check(len(subset)==M,'all planned trial identities retained')
            check({r['realization_index'] for r in subset}==set(range(M)),'unique complete realization slots')
            for j,name in enumerate(p['fields']):
                k=sum(bool(r['fields'][j]['certified_exceedance']) for r in subset if r['status']=='COMPLETE')
                lo,hi=cp_lower(k,M,alpha)
                lb=arb(str(lo))/25
                reject=tail(k,M,F(1,4))<=alpha
                check(reject==(lo>F(1,4)),'binomial test and CP lower bound agree')
                tests.append({'field':name,'certified_exceedances':k,'planned_M':M,
                    'pvalue_at_null_probability_quarter':str(tail(k,M,F(1,4))),
                    'exceedance_probability_lower_endpoint_bracket':[str(lo),str(hi)],
                    'population_RMS_lower':pack(lb.sqrt().lower()),
                    'status':'REJECT_RMS_LE_0.1' if reject else 'INCONCLUSIVE'})
            out.append({'density_index':d,'nu':nu,'epsilon':e,'tests':tests,
                        'status':'REJECTED' if any(t['status']=='REJECT_RMS_LE_0.1' for t in tests) else 'INCONCLUSIVE'})
    rejected=sum(c['status']=='REJECTED' for c in out)
    return {'status':'ALL_TESTED_CELLS_REJECTED' if rejected==len(out) else 'INCONCLUSIVE_FOR_SURVIVORS',
            'cells':out,'rejected_cells':rejected,'familywise_false_rejection_risk_max':'1/40',
            'model':'independent identically distributed realizations within each density; declared sampler model',
            'scientific_status':{'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'},
            'Dirac_decision':'DO_NOT_START','Flavor_and_coherence':'BLOCKED_BY_G1_G2_G3',
            'E4_confirmation_seed_used':False}
