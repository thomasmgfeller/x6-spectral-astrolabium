"""Hypothetical orthogonal binary record of the occupancy-two alternative."""
import numpy as np


def occupancy_record(total, two, scalar):
    # Both branches share the *same* count flag; no endpoint identity is copied.
    weights = np.array([.5,.5])
    yes, other = two*weights, (total-two)*weights
    def pair(a,b):
        return np.einsum('di,ij,dj->d',a.conj(),scalar,b)
    direct = pair(yes+other,yes+other).real
    pinched = (pair(yes,yes)+pair(other,other)).real
    cross = 2*pair(yes,other).real
    assert max(abs(direct-pinched-cross))<1e-17
    return {'equal_pair_direct_success':direct.tolist(),
            'equal_pair_flagged_success':pinched.tolist(),
            'direct_minus_flagged_interference':cross.tolist()}
