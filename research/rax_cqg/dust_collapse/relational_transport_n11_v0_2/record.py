"""Binary cut record and its loss of interference in the final one-pair outcome."""
from fractions import Fraction as Q
import json
import numpy as np
from ideals import paths
from n11 import PREDS, ETA, box_integral, samples, read, ward


def lower_bound(cut,prep):
    # Reuse the published exact moment enclosure, independently replayed in verify.py.
    prior = read("sources/v01_exact.json")["variance_C1"][prep]
    vmax = Q(prior["variance_exact_enclosure"][1])
    assert vmax<Q(1,5)
    floor = Q(read("sources/readout.json")["one_unknown_pulse"]["uniform_branch_floor_enclosure"][0])
    p = (cut+Q(3,2))/3
    v = (1-p)**2
    return floor*(2*v*(1-v)-vmax)/4


def run(prep,cut,action):
    # No false one-pair hit from C0. A common pure gravity/past phase drops out.
    bins = list(paths(PREDS[1],(float(cut),),-ward.L,ward.L))
    g = np.zeros((2,2),complex)
    for t,w in samples(prep):
        pair = np.zeros(2,complex)
        for chain,cell in bins:
            label = int(chain[0]!=0)
            pair[label] += box_integral(t,cell,chain,action)
        g += w*ETA[1]*np.outer(pair.conj(),pair)/4
    diagonal = g.trace().real
    loss = 2*g[0,1].real
    return {"untagged":diagonal+loss,"tagged_unread":diagonal,
            "P_empty_hit":g[0,0].real,"P_nonempty_hit":g[1,1].real,
            "complex_empty_nonempty_pairing":[g[0,1].real,g[0,1].imag],"lost_hit_probability":loss}


def compute():
    numerical = read("n11.json")["endpoints"]
    data = {}
    for cut in (Q(0),Q(1,4)):
        data[str(cut)] = {}
        for prep in ("sharp","narrow","split"):
            row = {arm:run(prep,cut,action) for arm,action in (("coupled",1),("common_C0_dust",0))}
            for arm,r in row.items():
                assert abs(r["untagged"]-numerical[prep]["direct"][arm]["P_three_one_other"][1])<5e-9
            bound = lower_bound(cut,prep)
            assert 0 < bound < row["coupled"]["lost_hit_probability"]
            row["exact_coupled_loss_lower"] = str(bound)
            data[str(cut)][prep] = row
    return data


if __name__=="__main__":
    print(json.dumps(compute(),indent=2))
