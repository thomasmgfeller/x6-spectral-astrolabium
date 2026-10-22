"""Held-out simple-vs-simple Poisson testing; no threshold selection on holdout.
SPDX-License-Identifier: Apache-2.0
"""
from pt_common import *
def evaluate(rows):
    c=read(HERE/'contract.json');model=read(HERE/'model.json');coef=np.array(model['coefficients'],dtype=np.int64)
    n=c['validation_trials_per_geometry'];eps=sqrt_bounds(F(c['hoeffding_c'],2*n))[1]
    records=[];uppers=[]
    for g,r in enumerate(rows):
        X=np.array(r['counts'],dtype=np.int64);assert len(X)==n
        assert int(np.max(X))*int(np.sum(abs(coef)))<2**63
        pred=X@coef>model['threshold'];errors=int(np.sum(pred!=g))
        upper=min(F(1),F(errors,n)+eps+setup(g)['coupling_upper']);uppers.append(upper)
        records.append(dict(geometry=g,trials=n,errors=errors,error_fraction=str(F(errors,n)),
                            continuous_error_upper=outward(upper)[1],grid_coupling_upper=r['coupling_upper']))
    # The original helper bounds 2*exp(-c), exactly the two one-sided tails here.
    failure=confidence_bound(1,c['hoeffding_c'])
    return dict(status='COMPLETE',records=records,empirical_equal_prior_accuracy=str(1-sum(F(r['errors'],n) for r in records)/2),
      equal_prior_accuracy_lower=outward(1-sum(uppers)/2)[0],
      full_observation_total_variation_lower=outward(max(F(0),1-sum(uppers)))[0],
      numerical_validation_failure_upper=outward(failure)[1],
      numerical_validation_confidence_lower=outward(1-failure)[0],
      scope='Conditional fixed witness pair and sealed classifier; ideal independent Poisson/grid sampling. Achievable test performance and TV lower bound, not TV upper bound, minimax reconstruction risk, physical data validation or 10% operator accuracy.')
def main():
    frozen();c=read(HERE/'contract.json');seal=read(HERE/'model_seal.json')
    assert hashlib.sha256((HERE/'model.json').read_bytes()).hexdigest()==seal['model_sha256']
    f=kernel();rows=[]
    for g in range(2):
        r=simulate(g,'validation',c['validation_trials_per_geometry'],f);save(HERE/f'validation-{g}.json.gz',r);rows.append(r)
    result=evaluate(rows);save(HERE/'summary.json',result);print(json.dumps(result),flush=True)
if __name__=='__main__':main()
