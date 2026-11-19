"""Independent low-order checks of each rectangular factorization and the phase moments."""
from itertools import product
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
import sympy as sp
from compare import (ROOT, INNER, MASKS, ORDERS, ward, past_set, axis, times_and_weights,
                     kernel_mean)


def mask_check():
    errors = []
    for cut in (0.,.25):
        boxes = [axis(cut,ward.L,7),axis(-ward.L,cut,7)]
        for mask in MASKS:
            axes = [boxes[int(v)] for v in mask]
            t,weights = times_and_weights(-2*ward.DELTA+1/16,axes)
            for g,d in ((0,0),(1,1),(1,0)):
                c = ORDERS[d][0]
                kept = past_set(mask,ORDERS[g][0])
                full = kernel_mean(True,c,t,axes,weights,set())
                pieces = kernel_mean(False,c,t,axes,weights,kept)
                errors.append(abs(full-pieces))
    assert len(errors)==48 and max(errors)<1e-13
    return max(errors)


def moment_check():
    # The phase and its square are of degree <=4 in every uniform clock and
    # degree <=2 in every mark. Positive three-node Gauss rules integrate them.
    x,w = leggauss(3)
    weights = w/2
    mark_nodes = np.r_[0.,(1+x)/2]
    mark_w = np.r_[.5,w/4]
    axes = np.ix_(x,x,x,mark_nodes,mark_nodes,mark_nodes)
    joint_w = np.prod(np.broadcast_arrays(*np.ix_(weights,weights,weights,mark_w,mark_w,mark_w)),axis=0)
    exact = json.loads((ROOT/"exact.json").read_text())["variance_C1"]
    coeffs = ORDERS[1][0]
    errors = []
    for prep,offsets in (("sharp",[0]),("narrow",[0]),("split",[-1/16,1/16])):
        m1 = m2 = 0.
        for off,k in product(offsets,range(3)):
            t = [(j-5)*ward.DELTA for j in range(11)]
            t[3] += off + (0. if prep=="sharp" else x[k]/32)
            t[4:7] = [v*1.5 for v in axes[:3]]
            rho = [*axes[3:],1/8,1/8,1/8,1/8]
            phase = sum(rho[j-4]*ward.cvalue(j,t,coeffs)/2 for j in range(4,11))
            m1 += weights[k]/len(offsets)*np.sum(joint_w*phase)
            m2 += weights[k]/len(offsets)*np.sum(joint_w*phase**2)
        expected = [float(sp.sympify(exact[prep][key]).subs(sp.Symbol("d"),ward.DELTA))
                    for key in ("mean","variance")]
        errors.extend((abs(m1-expected[0]),abs(m2-m1**2-expected[1])))
    assert max(errors)<1e-13
    return max(errors)


if __name__=="__main__":
    print(json.dumps({"individual_rectangles_checked":48,"rectangle_max_abs_error":mask_check(),
                      "moment_max_abs_error":moment_check()},indent=2))
