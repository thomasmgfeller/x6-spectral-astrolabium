"""Independent distribution controls; the certificate itself uses exact bounds.
SPDX-License-Identifier: Apache-2.0
"""
from fl_run import *
import math
import numpy as np

def controls():
    # Direct enumeration of independent Poisson pairs, independent of geometry.
    # Floating checks are controls only; analytic proofs support the certificate.
    cases=[]
    for U,L,s in [(F(2),F(5),F(101,100)),(F(2),F(5),F(11,10)),(F(1),F(9),F(6,5))]:
        a=s**3;means0=[U,L-U];means1=[a*U,L-a*U]
        def pmf(mu):
            p=[math.exp(-float(mu))]
            for k in range(1,80):p.append(p[-1]*float(mu)/k)
            return np.array(p)
        p=np.outer(pmf(means0[0]),pmf(means0[1]));q=np.outer(pmf(means1[0]),pmf(means1[1]))
        tv=float(np.sum(abs(p-q))/2);aff=float(np.sum(np.sqrt(p*q)))
        J=sum((math.sqrt(float(x))-math.sqrt(float(y)))**2 for x,y in zip(means0,means1))
        assert abs(aff-math.exp(-J/2))<1e-13
        upper,j=tv_bound(s,(U,U),(L,L))
        # Exact factorial-moment bound on omitted Poisson tails.
        tail=sum(mu**80/F(math.factorial(80)) for mu in means0+means1)
        assert tail<F(1,10**40)
        assert tv+float(tail)<=float(upper)+1e-13
        cases.append(dict(U=str(U),L=str(L),s=str(s),tv_upper_verified=True,affinity_checked=True))
    # Splitting the occupied region into more membership atoms preserves J.
    atoms=[F(1),F(2),F(3),F(5)];a=F(121,100)
    direct=sum((math.sqrt(float(a*v))-math.sqrt(float(v)))**2 for v in atoms)
    aggregate=float(sum(atoms))*(math.sqrt(float(a))-1)**2
    assert abs(direct-aggregate)<1e-13
    assert tv_bound(F(1),(F(2),F(2)),(F(5),F(5)))[0]<F(1,10**60)
    return dict(poisson_enumeration_cases=cases,atom_partition_affinity=True,identical_law_control=True)

if __name__=='__main__':
    result=main_result();assert result==read(HERE/'certificate.json')
    rows=result['grid'];gate=F(read(HERE/'contract.json')['tv_upper_gate'])
    assert all(F(a['tv_upper'])<F(b['tv_upper']) for a,b in zip(rows,rows[1:]))
    assert rows[591]['accepted'] and not rows[592]['accepted']
    audit=dict(status='PASS',exact_certificate_replayed=True,controls=controls())
    if '--verify' in sys.argv:assert audit==read(HERE/'audit.json')
    else:save(HERE/'audit.json',audit)
    print(json.dumps(audit))
