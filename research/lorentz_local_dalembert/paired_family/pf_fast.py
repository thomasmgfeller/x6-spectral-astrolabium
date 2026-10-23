"""Exactly equivalent integer evaluation of the frozen rational exponential sum.
SPDX-License-Identifier: Apache-2.0
"""
from pf_run import *
import math
import ss_marginal

def integer_void_bounds(x):
    assert 0<=x<=1
    p,q=x.numerator,x.denominator
    # Exact common-denominator form of sum_{k=0}^{80} (-x)^k/k!.
    numerator=1;qpower=1;coefficient=1
    for k in range(79,-1,-1):
        qpower*=q;coefficient*=k+1
        numerator=-p*numerator+coefficient*qpower
    even=F(numerator,qpower*coefficient)
    odd=even-F(p**81,q**81*math.factorial(81))
    return 1-even,1-odd

def install():
    ss_marginal.void_bounds=integer_void_bounds

if __name__=='__main__':
    original=ss_marginal.void_bounds
    controls=[F(0),F(1),F(1,2),F(1,10**130),F(10**130-1,10**130)]
    controls += [F(k,97) for k in range(1,97)]
    for x in controls:assert integer_void_bounds(x)==original(x)
    print('EXACT_EXPONENTIAL_EQUIVALENCE_PASS',len(controls),flush=True)
    install()
    for name,result in zip(('cells.json.gz','summary.json'),run()):
        # JSON object keys are strings; the runtime anchor lookup uses integers.
        result=json.loads(json.dumps(result))
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print('PAIRED_FAMILY_REPLAY_COMPLETE',flush=True)
