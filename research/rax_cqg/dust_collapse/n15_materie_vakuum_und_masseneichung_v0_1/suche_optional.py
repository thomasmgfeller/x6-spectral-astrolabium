"""Exploratory seeds only. The existence proof in sattel.py uses exact arithmetic."""
import json
from fractions import Fraction
import numpy as np
from scipy.optimize import root

import n15


def midpoint(bounds):
    return float(sum(map(Fraction,bounds))/2)


def search():
    inner = list(n15.INNER)
    _, relations = n15.support.geometry(n15.TYPE)
    edge_matrix = np.zeros((15,15))
    for i,j,b in n15.variation.edges(n15.encode(relations,15),15):
        edge_matrix[i,j] = b
    source = json.loads((n15.ROOT/'basis/randdichte.json').read_text())
    fields = source['changed_future_case']['at_midpoint']
    time = np.array([-5,-4,-3,-2+1/6,0,0,0,2,3,4,5,0,0,0,0])
    density = np.full(15,1/64)
    density[:4] = 1/8
    for j in inner:
        time[j] = midpoint(fields['Y_inner'][str(j)])
        density[j] = midpoint(fields['w_inner_new'][str(j)])

    rng = np.random.default_rng(18206)
    for mask in sorted(range(127),key=int.bit_count,reverse=True):
        if not mask & 64:  # At the terminal event, the nonempty future collar forces w14 > 0.
            continue
        active = [j for k,j in enumerate(inner) if mask & (1<<k)]
        y, w = time.copy(), density.copy()
        w[inner] = 0
        def equations(x,derivative=False):
            y[inner], w[active] = x[:7],x[7:]
            diff = y[None,:]-y[:,None]
            signed = edge_matrix*diff
            incoming = -signed.sum(axis=0)
            if not derivative:
                moments = 19+(signed*diff).sum(axis=0)
                balance = w*incoming+signed@w
                return np.r_[moments[active],balance[inner]]
            coupling = edge_matrix*w[None,:]
            gradient = coupling+coupling.T
            gradient -= np.diag(gradient.sum(axis=1))
            mixed = signed+np.diag(incoming)
            return np.block([
                [-2*mixed.T[np.ix_(active,inner)],np.zeros((len(active),len(active)))],
                [gradient[np.ix_(inner,inner)],mixed[np.ix_(inner,active)]]])

        for attempt in range(4):
            initial = np.r_[time[inner],density[active]]
            if attempt:
                initial[:7] += rng.normal(0,.2,size=7)
                initial[7:] *= rng.uniform(.7,1.3,size=len(active))
            result = root(equations,initial,jac=lambda x:equations(x,True),
                          options={'xtol':1.e-11,'maxfev':500})
            if max(abs(equations(result.x))) > 1.e-9:
                continue
            if not all(y[j]>y[i]+1.e-7 for i,j in relations) or not all(0<w[j]<1 for j in active):
                continue
            yield {'active':active,'center':result.x.tolist()}
            break


if __name__=='__main__':
    print(json.dumps(list(search()),indent=2))
