"""Fixed-size DEVELOPMENT screen of the structural C0 fast-path ceiling."""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import sys
from time import perf_counter

import numpy as np
import scipy
from scipy.stats import beta, binomtest
import stim

ROOT = Path(__file__).resolve().parent
REF = ROOT / "reference"
sys.path.insert(0, str(REF))
from measure import PathIndex, classification, incidence, read_sources
from verify import ExhaustiveCheck

FREEZE = "9352d6bd704022d4f36666943df9ee94287203391c425b82523c0a5f0910488b"
PASS_TO_MARGIN = "ALL_CLUSTERS_BOTH"
EMPTY = "EMPTY_SEPARATE"
OVERFLOW = "CLUSTER_OVERFLOW"
STATES = [EMPTY, OVERFLOW, "NO_LOCAL_PAIRING", "SINGLE_CLASS_BLOCKS", PASS_TO_MARGIN]


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, sort_keys=True, indent=2) + "\n")


def cluster_guard(active, near):
    todo = set(active)
    result = []
    while todo:
        head = min(todo)
        todo.remove(head)
        part, queue = {head}, [head]
        while queue:
            fringe = near[queue.pop()] & todo
            todo.difference_update(fringe)
            part.update(fringe)
            queue.extend(fringe)
        result.append(tuple(sorted(part)))
    return tuple(result)


def independent_groups(active, closed):
    # Intersection of closed one-hop detector neighborhoods iff distance <= 2.
    groups = [{d} for d in active]
    for a,b in combinations(active, 2):
        if not closed[a].isdisjoint(closed[b]):
            left = next(g for g in groups if a in g)
            right = next(g for g in groups if b in g)
            if left is not right:
                groups.remove(right)
                left.update(right)
    return tuple(sorted(tuple(sorted(g)) for g in groups))


class Screen:
    def __init__(self, adj):
        self.index = PathIndex(adj)
        self.verifier = ExhaustiveCheck(adj)

    @lru_cache(maxsize=None)
    def classify(self, active):
        groups = cluster_guard(active, self.index.near)
        independently = independent_groups(active, self.verifier.closed_neighbours)
        assert groups == independently
        size = max(map(len, groups), default=0)
        if size > 8:
            return OVERFLOW, size, len(groups), ()
        masks = tuple(self.index.analyse(active))
        assert tuple(g for g,_ in masks) == groups
        return classification(masks)[1], size, len(groups), masks

    @lru_cache(maxsize=None)
    def full_check(self, active):
        state,size,_,masks = self.classify(active)
        if state == OVERFLOW:
            assert size > 8  # The independent partition was already compared; skip search.
        else:
            assert tuple(self.verifier.analyse(active)) == masks
        return True


def controls(screen):
    with (REF/"results/development_syndromes.csv").open() as fp:
        count = 0
        for row in csv.DictReader(fp):
            if row["policy"] != "syntactic":
                continue
            active = tuple(map(int, row["active_detectors"].split()))
            state,_,_,groups = screen.classify(active)
            assert state == row["section17"]
            codes = {0:"-",1:"0",2:"1",3:"01"}
            assert " | ".join(codes[m] for _,m in groups) == row["reachable_per_cluster"]
            count += bool(active)
        assert count == 1679
    # Same nine active detectors form an oversized cluster. Eight remain admissible.
    chain = tuple(tuple((j,0) for j in (i-1,i+1) if 0<=j<9) for i in range(9))
    toy = Screen(chain)
    assert toy.classify(tuple(range(9)))[:3] == (OVERFLOW,9,1)
    assert toy.classify(tuple(range(8)))[1] == 8 and toy.full_check(tuple(range(8)))
    assert toy.classify((0,))[0] == "NO_LOCAL_PAIRING"
    assert toy.classify(())[0] == EMPTY
    # The abstract boundary must not fuse two clusters. One singleton blocks eligibility.
    multi = Screen((((-1,0),(-1,1)), ((-1,0),)))
    assert multi.classify((0,1))[:3] == ("SINGLE_CLASS_BLOCKS",1,2)
    assert multi.full_check((0,1))
    assert multi.classify((0,))[0] == PASS_TO_MARGIN


def load_model():
    p = (ROOT/"shot_protocol.json").read_bytes()
    assert sha(p) == FREEZE and stim.__version__ == "1.16.0"
    spec = json.loads(p)
    for path, digest in spec["input_sha256"].items():
        assert sha((REF/path).read_bytes()) == digest, path
    circuit = stim.Circuit.from_file(REF/"results/development.stim")
    assert circuit.num_detectors == 120 and circuit.num_observables == 1
    dem = circuit.detector_error_model(decompose_errors=True)
    assert str(dem).encode() == (REF/"results/development.dem").read_bytes()
    adj = incidence(120, read_sources(dem), "syntactic")
    edge_rows = [[u,v,b] for u,row in enumerate(adj) for v,b in row if v == -1 or u < v]
    assert edge_rows == json.loads((REF/"results/development_syntactic_edges.json").read_text())
    return spec, circuit, Screen(adj)


def count_shots(packed, screen, out, target):
    n = len(packed)
    bits = np.unpackbits(packed, axis=1, bitorder="little")
    statuses = Counter()
    strata = defaultdict(Counter)
    verified = set()
    n_check = n_eligible = n_fixed = 0
    with (out/"shot_status.csv").open("w",newline="") as fp:
        w=csv.writer(fp)
        w.writerow(["shot_id","n_active","n_clusters","max_cluster","status","independent_status_check"])
        for i,row in enumerate(bits):
            active=tuple(row.nonzero()[0].tolist())
            state,size,clusters,_=screen.classify(active)
            check = (i % 199 == 0 or state == PASS_TO_MARGIN)
            if check:
                assert screen.full_check(active)
                n_check+=1
                n_eligible+=int(state==PASS_TO_MARGIN)
                n_fixed+=int(i%199==0)
                verified.add(active)
            statuses[state]+=1
            strata[len(active)][state]+=1
            w.writerow([i,len(active),clusters,size,state,int(check)])
    k=statuses[PASS_TO_MARGIN]
    m=n-statuses[EMPTY]
    assert sum(statuses.values())==n and n_eligible==k and m>0
    ci=binomtest(k,m).proportion_ci(confidence_level=0.99,method="exact")
    check_ci=[0.0 if k==0 else beta.ppf(.005,k,m-k+1),1.0 if k==m else beta.ppf(.995,k+1,m-k)]
    assert np.allclose([ci.low,ci.high],check_ci,rtol=0,atol=1e-11)
    decision=("NO_GO_5PCT" if ci.high<target else
              "REACHABILITY_FEASIBLE_5PCT" if ci.low>=target else "INCONCLUSIVE")
    with (out/"by_detector_count.csv").open("w",newline="") as fp:
        w=csv.writer(fp);w.writerow(["n_active","shots"]+STATES)
        for v,counts in sorted(strata.items()):
            w.writerow([v,sum(counts.values())]+[counts[s] for s in STATES])
    return {"n_all":n,"n_nonempty":m,"eligible_nonempty":k,"statuses":{s:statuses[s] for s in STATES},
            "eligible_fraction_nonempty":k/m,"ci_99_nonempty":[ci.low,ci.high],"target":target,
            "eligible_nonempty_fraction_of_all":k/n,"empty_fraction_of_all":statuses[EMPTY]/n,
            "decision":decision,"source_patterns_controls":1679,"sample_distinct_patterns":len(set(map(bytes,packed))),
            "independent_cluster_guard_all_shots":n,"independent_status_checks_shots":n_check,
            "independent_status_checks_distinct_patterns":len(verified),"eligible_shots_checked":n_eligible,
            "systematic_shots_checked":n_fixed}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out",type=Path)
    parser.add_argument("--shots",type=Path,help="Replay the archived raw b8 input instead of sampling.")
    args=parser.parse_args()
    if not __debug__:
        raise SystemExit("Use Python without -O")
    args.out.mkdir(parents=True,exist_ok=False)
    t0=perf_counter()
    spec,circuit,screen=load_model()
    controls(screen)
    t1=perf_counter()
    if args.shots is None:
        packed=circuit.compile_detector_sampler(seed=spec["seed"]).sample(shots=spec["fixed_shots"],bit_packed=True)
        (args.out/"detectors.b8").write_bytes(packed.tobytes())
    else:
        packed=np.fromfile(args.shots,dtype=np.uint8).reshape(-1,15)
    assert packed.shape==(spec["fixed_shots"],15)
    t2=perf_counter()
    report=count_shots(packed,screen,args.out,spec["minimum_nonempty_coverage"])
    report.update(protocol_sha256=FREEZE,raw_b8_sha256=sha(packed.tobytes()),
                  scipy=scipy.__version__,numpy=np.__version__,stim=stim.__version__)
    save(args.out/"summary.json",report)
    times={"controls_s":t1-t0,"sample_or_read_s":t2-t1,"classify_and_check_s":perf_counter()-t2}
    save(args.out/"timing.json",times)
    print(json.dumps(report),flush=True)


if __name__=="__main__":
    main()
