"""Certify positivity of the binary Gram tables with integer congruences."""
from common import HERE
import json
import numpy as np

def verify():
    matrices=np.load(HERE/'gram.npy')
    assert np.array_equal(matrices[0],matrices[2])
    out=[]
    for g in matrices[:2]:
        assert np.array_equal(g,g.conj().T)
        # Integer-scaled dyadics. Use the inverse Cholesky only as a witness.
        dyads=[float(x).as_integer_ratio() for a in (g.real,g.imag) for x in a.flat]
        d=max(v for _,v in dyads)
        integer=[u*(d//v) for u,v in dyads]
        ar,ai=np.array(integer,dtype=object).reshape(2,*g.shape)
        y=np.linalg.inv(np.linalg.cholesky(g));den=2**35
        yr=np.rint(y.real*den).astype(np.int64).astype(object)
        yi=np.rint(y.imag*den).astype(np.int64).astype(object)
        left=yr@ar-yi@ai; other=yr@ai+yi@ar
        c=left@yr.T+other@yi.T; s=other@yr.T-left@yi.T
        unit=d*den**2
        residual=abs(c-np.eye(len(g),dtype=object)*unit)+abs(s)
        radius=max(residual.sum(axis=1))
        assert 2*radius<unit
        out.append(float(radius/unit))
    print('Upper bounds for the two congruence residuals',out)
    return out
if __name__=='__main__': verify()
