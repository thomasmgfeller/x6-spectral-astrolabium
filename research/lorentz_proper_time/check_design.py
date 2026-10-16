"""Exact deterministic design checks; never generates target samples."""
from fractions import Fraction as F
from itertools import permutations
from math import comb
from pathlib import Path
import json

HERE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def points(record):
    return [tuple(F(x) for x in p) for p in record["points"]]

def relation(xy):
    return [[int(i != j and u <= x and v <= y)
             for j, (x, y) in enumerate(xy)]
            for i, (u, v) in enumerate(xy)]

def height(c, ids):
    # Exhaustive oracle for tiny deterministic examples.
    return max((len(p) for k in range(len(ids)+1)
                for p in permutations(ids, k)
                if all(c[p[i]][p[j]] for i in range(k) for j in range(i+1,k))),
               default=0)

def profile(c, p, q):
    require(c[p][q] == 1, "strictly ordered marks")
    inner = [i for i in range(len(c)) if c[p][i] and c[i][q]]
    return dict(N=len(c), R=sum(map(sum,c)), H=height(c,range(len(c))),
                K=len(inner), ell=height(c,inner))

def theta2(xy, p, q, T=F(1)):
    return (xy[q][0]-xy[p][0])*(xy[q][1]-xy[p][1])/(T*T)

def moment_delta(power):
    return F(2)/((power+1)*(power+2))

def run():
    cfg=json.loads((HERE/"contract.json").read_text())
    ex=json.loads((HERE/"design_examples.json").read_text())
    require(cfg["status"] == "DESIGN_FIXED_IMPLEMENTATION_PENDING_NO_TARGET_DATA", "design status")
    require(cfg["publication"]["new_target_samples_generated"] is False
            and cfg["publication"]["large_run_executed"] is False
            and cfg["publication"]["source_freeze_exists"] is False, "no claimed target run")
    sizes=cfg["sampling"]["m_values"]
    require(sizes == [64,144,256], "fixed sizes")
    count=len(sizes)*(cfg["sampling"]["calibration"]["uniform_per_m"]
                     +2*cfg["sampling"]["test_per_family_m"])
    require(count == cfg["sampling"]["total_orders"] == 6912, "cohort accounting")
    require(cfg["matched_transfer"]["key"] == ["N","R","H"]
            and cfg["matched_transfer"]["minimum_pairs"] == 128, "matching contract")
    require(cfg["evaluation"]["primary"]["m"] == 256
            and cfg["evaluation"]["primary"]["family"] == "uniform"
            and cfg["evaluation"]["primary"]["count"] == 1024
            and cfg["evaluation"]["primary"]["method"] == "V", "primary contract")
    require(cfg["evaluation"]["bootstrap"]["replicates"] == 5000, "bootstrap contract")

    shared=ex["shared"]
    relabelings=0
    for key in ["A","B"]:
        r=ex[key]; xy=points(r); c=relation(xy); p,q=r["marks"]
        require(["".join(map(str,row)) for row in c] == shared["relation_rows"], "shared full order")
        expected={k:shared[k] for k in ["N","R","H","K","ell"]}
        require(profile(c,p,q) == expected, "counterexample integer observables")
        require(theta2(xy,p,q) == F(r["theta_squared"]), "exact squared target")
        for perm in permutations(range(len(xy))):
            newxy=[xy[i] for i in perm]; np,nq=perm.index(p),perm.index(q)
            require(profile(relation(newxy),np,nq) == expected, "transported mark invariance")
            require(theta2(newxy,np,nq) == F(r["theta_squared"]), "target relabel invariance")
            relabelings+=1
        boosted=[(2*u,v/2) for u,v in xy]
        require(relation(boosted) == c and theta2(boosted,p,q) == theta2(xy,p,q), "rational boost")
        scaled=[(3*u,3*v) for u,v in xy]
        require(relation(scaled) == c and theta2(scaled,p,q,F(3)) == theta2(xy,p,q), "normalized scale")
        require(theta2(scaled,p,q) == 9*theta2(xy,p,q), "absolute scale ambiguity")
    require(relation(points(ex["A"])) == relation(points(ex["B"]))
            and ex["A"]["theta_squared"] != ex["B"]["theta_squared"], "finite nonidentifiability")

    for key in ["empty","antichain"]:
        r=ex[key]; c=relation(points(r)); v=profile(c,*r["marks"])
        require(v["K"] == r["K"] and v["ell"] == r["ell"], "interval counting convention")
        require(height(c,range(len(c))) == v["ell"]+2, "endpoint count convention")
    xy=points(ex["antichain"]); p,q=ex["antichain"]["marks"]
    normalized=[((u-xy[p][0])/(xy[q][0]-xy[p][0]),
                 (v-xy[p][1])/(xy[q][1]-xy[p][1])) for u,v in xy]
    require(relation(normalized) == relation(xy), "rectangle normalization preserves order")

    cases=0
    for m in range(1,9):
        for a in [F(1,9),F(1,4),F(3,4)]:
            prob=[comb(m,k)*a**k*(1-a)**(m-k) for k in range(m+1)]
            require(sum(prob)==1, "binomial mass")
            mean=sum(F(k,m)*pr for k,pr in enumerate(prob))
            mse=sum((F(k,m)-a)**2*pr for k,pr in enumerate(prob))
            require(mean==a and mse==a*(1-a)/m, "binomial moments")
            cases+=1
    expected={"E_a":moment_delta(F(1))**2,
              "E_a_squared":moment_delta(F(2))**2,
              "E_theta":moment_delta(F(1,2))**2}
    expected["MSE_a_hat_times_m"]=expected["E_a"]-expected["E_a_squared"]
    require(expected == {k:F(v) for k,v in ex["endpoint_moments"].items()}, "endpoint moments")
    return dict(status="PASS_DESIGN_ONLY", target_samples_generated=0,
                relabelings=relabelings, exact_binomial_cases=cases,
                target_values={"A":"3/10","B":"7/10"},
                full_source_freeze=False, monte_carlo_run=False,
                note="Finite checks support arithmetic and examples, not an independent proof of the general argument.")

if __name__ == "__main__":
    print(json.dumps(run(),indent=2))
