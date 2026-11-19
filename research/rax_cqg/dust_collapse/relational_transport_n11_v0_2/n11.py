"""Compose the N11 dust kernel using released ideals, frontier censoring and nested integrals."""
from functools import lru_cache
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from sources import ward_clock as ward
from ideals import paths

ROOT = Path(__file__).resolve().parent
def read(name):
    return json.loads((ROOT/name).read_bytes())

PLAN = read("contract.json")
GRID = PLAN["grids"]
INNER = tuple(ward.INNER)
BRANCHES = [ward.coeffs(deleted) for deleted in ward.ORDERS.values()]
PREDS = [tuple(sum(1<<i for i,v in enumerate(INNER) if (v,j) in edges) for j in INNER) for edges,_ in BRANCHES]
ETA = np.array(read("sources/readout.json")["one_unknown_pulse"]["reference_charge_efficiencies_C0_C1"]["1"])
PACKET = read("sources/preparation.json")


@lru_cache(None)
def axis(lo,hi):
    n = GRID["full_axis"] if (lo,hi)==(-ward.L,ward.L) else GRID["partial_axis"]
    x,w = leggauss(n)
    return (lo+hi+(hi-lo)*x)/2,w*(hi-lo)/(4*ward.L)


def box_integral(t,cell,chain,action):
    axes = [axis(*bounds) for bounds in cell]
    x = list(np.ix_(*(item[0] for item in axes)))
    w = list(np.ix_(*(item[1] for item in axes)))
    terminal = len(chain)
    stage = {j:next((k for k,D in enumerate(chain) if D&(1<<i)),terminal)
             for i,j in enumerate(INNER)}
    factors = [1.]*(terminal+1)
    times = [(j-5)*ward.DELTA for j in range(11)]
    times[3] = t
    times[4:7] = x
    coeffs = BRANCHES[action][0]
    for j in (*INNER,*ward.FUTURE):
        incoming = [(i,v) for (i,k),v in coeffs.items() if k==j and v]
        kinetic = sum(v*(times[j]-times[i])**2 for i,v in incoming)
        c = 1+ward.BETA*kinetic/2
        if j in INNER:
            ready = max([stage[j]]+[stage[i] for i,v in incoming if i in stage])
            g = (1+np.exp(-.25j*c)*np.sinc(c/(4*np.pi)))/2
        else:
            ready = terminal
            g = np.exp(-1j*c/16)
        factors[ready] = factors[ready]*g
    result = np.ones((1,1,1),complex)
    for k in reversed(range(terminal+1)):
        result = result*factors[k]
        for i,j in enumerate(INNER):
            if stage[j]==k:
                result = np.sum(result*w[i],axis=i,keepdims=True)
    return result.item()


def coefficients(t,cuts):
    values = []
    for geo,action in ((0,0),(1,1),(1,0)):
        sectors = paths(PREDS[geo],cuts,-ward.L,ward.L)
        summed = sum(box_integral(t,cell,chain,action) for chain,cell in sectors)
        values.append(np.exp(1j*BRANCHES[geo][1])*summed/2)
    return np.array(values)


def samples(prep):
    t0 = -2*ward.DELTA
    if prep=="sharp":
        return [(t0,1.)]
    offsets = [0.] if prep=="narrow" else PACKET["clock_offsets_from_affine_T3"]
    nodes,weights = leggauss(GRID["outer_per_lobe"])
    return [(t0+off+PACKET["clock_lobe_half_width"]*x,w/(2*len(offsets)))
            for off in offsets for x,w in zip(nodes,weights)]


def evaluate(prep,cuts):
    c = np.zeros((3,3),complex)
    for t,w in samples(prep):
        a = coefficients(t,cuts)
        c += w*np.outer(a.conj(),a)
    answer = {}
    for arm,idx in (("coupled",[0,1]),("common_C0_dust",[0,2])):
        g = c[np.ix_(idx,idx)]
        assert np.linalg.eigvalsh(g)[0]>-1e-13
        three,one = np.diag(g).real*ETA
        answer[arm] = {"gram":{"diagonal":np.diag(g).real.tolist(),
                            "off_diagonal_re_im":[g[0,1].real,g[0,1].imag]},
                       "P_three_one_other":[three,one,1-three-one]}
    return answer


def vector(row):
    return np.array([*row["gram"]["diagonal"],complex(*row["gram"]["off_diagonal_re_im"]),
                     *row["P_three_one_other"]])


def compute():
    archive = read("sources/v01_numerical.json")["results"]
    data = {}
    max_gap = reference_gap = 0.
    for prep in ("sharp","narrow","split"):
        direct = evaluate(prep,())
        data[prep] = {"direct":direct}
        for arm in direct:
            reference_gap = max(reference_gap,max(abs(vector(direct[arm])-vector(archive[prep]["direct"][arm]))))
        for tag,cuts in (("zero",(0.,)),("quarter",(.25,)),("both",(0.,.25))):
            via = evaluate(prep,cuts)
            for arm in via:
                max_gap = max(max_gap,max(abs(vector(direct[arm])-vector(via[arm]))))
            data[prep][tag] = via
    assert max(max_gap,reference_gap)<PLAN["absolute_tolerance"]
    return {"endpoints":data,"max_composition_error":max_gap,"direct_v01_error":reference_gap}


if __name__=="__main__":
    print(json.dumps(compute(),indent=2,allow_nan=False))
