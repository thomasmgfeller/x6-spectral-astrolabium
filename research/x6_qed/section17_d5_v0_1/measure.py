"""Enumerate section 17 of the X6-QED development contract. No random sampling."""
from __future__ import annotations

import csv
import hashlib
import itertools
import json
import sys
from collections import Counter, defaultdict
from functools import lru_cache
from pathlib import Path
from time import perf_counter

import stim

ROOT = Path(__file__).resolve().parent
BOUNDARY = -1
ZERO, ONE, BOTH = 1, 2, 3  # bit masks for sets of reachable classes
LABEL = {0: "-", ZERO: "0", ONE: "1", BOTH: "01"}


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def sha(data):
    return hashlib.sha256(data).hexdigest()


def xor_product(a, b):
    return sum(1 << v for v in {i ^ j for i in (0, 1) if a & (1 << i)
                                for j in (0, 1) if b & (1 << j)})


def read_sources(dem):
    rows = []
    for inst in dem.flattened():
        if inst.type != "error":
            continue
        parts, ds, bit = [], set(), 0
        all_ds, all_bit = set(), 0
        for target in inst.targets_copy():
            if target.is_separator():
                parts.append((tuple(sorted(ds)), bit))
                ds, bit = set(), 0
            elif target.is_relative_detector_id():
                ds ^= {target.val}
                all_ds ^= {target.val}
            else:
                assert target.is_logical_observable_id() and target.val == 0
                bit ^= 1
                all_bit ^= 1
        parts.append((tuple(sorted(ds)), bit))
        rows.append({"id": len(rows), "p": inst.args_copy()[0],
                     "syndrome": tuple(sorted(all_ds)), "logical": all_bit, "parts": parts})
    return rows


def incidence(n, sources, policy):
    # Multiple source components with the same (endpoints, mask) are equivalent
    # only for existential path feasibility. Source provenance remains in sources.json.
    adj = [set() for _ in range(n)]
    for src in sources:
        detector_xor, logical_xor = set(), 0
        for i, (detectors, mask) in enumerate(src["parts"]):
            assert len(detectors) in (1, 2) and all(0 <= d < n for d in detectors)
            if policy == "first_component":
                mask = src["logical"] if i == 0 else 0
            detector_xor ^= set(detectors)
            logical_xor ^= mask
            a = detectors[0]
            b = detectors[1] if len(detectors) == 2 else BOUNDARY
            adj[a].add((b, mask))
            if b != BOUNDARY:
                adj[b].add((a, mask))
        assert tuple(sorted(detector_xor)) == src["syndrome"] and logical_xor == src["logical"]
    return tuple(tuple(sorted(row)) for row in adj)


class PathIndex:
    def __init__(self, adj):
        self.paths = defaultdict(set)
        self.near = [set() for _ in adj]
        self.boundary_adjacent = {i for i, row in enumerate(adj) if any(v == BOUNDARY for v, _ in row)}
        for start in range(len(adj)):
            def visit(u, visited, depth, parity):
                for v, mask in adj[u]:
                    bit = parity ^ mask
                    if v == BOUNDARY:
                        if depth + 1 <= 2:
                            self.paths[start, v].add((visited ^ (1 << start), bit))
                        continue
                    if visited & (1 << v):
                        continue
                    if depth + 1 <= 2:
                        self.near[start].add(v)
                    self.paths[start, v].add((visited ^ (1 << start), bit))
                    if depth + 1 < 4:
                        visit(v, visited | (1 << v), depth + 1, bit)
            visit(start, 1 << start, 0, 0)

    def analyse(self, active):
        active_bits = sum(1 << u for u in active)
        remaining = set(active)
        clusters = []
        while remaining:
            seed = min(remaining)
            group, pending = {seed}, [seed]
            while pending:
                more = (self.near[pending.pop()] & remaining) - group
                group.update(more)
                pending.extend(more)
            remaining -= group
            clusters.append(tuple(sorted(group)))

        @lru_cache(None)
        def choices(u, v):
            found = 0
            for internal, flip in self.paths[u, v]:
                if not active_bits & internal:
                    found |= 1 << flip
            return found

        @lru_cache(None)
        def solve(nodes):
            if not nodes:
                return ZERO
            u, *rest = nodes
            result = xor_product(choices(u, BOUNDARY), solve(tuple(rest)))
            for j, v in enumerate(rest):
                result |= xor_product(choices(u, v), solve(tuple(rest[:j] + rest[j+1:])))
            return result

        assert all(len(group) <= 8 for group in clusters), "Unexpected overflow in this source population"
        return [(group, solve(group)) for group in clusters]


def classification(groups):
    shot = ZERO
    for _, mask in groups:
        shot = xor_product(shot, mask)
    if not groups:
        state = "EMPTY_SEPARATE"
    elif any(mask == 0 for _, mask in groups):
        state = "NO_LOCAL_PAIRING"
    elif all(mask == BOTH for _, mask in groups):
        state = "ALL_CLUSTERS_BOTH"
    else:
        state = "SINGLE_CLASS_BLOCKS"
    return shot, state


def run_case(name, n, sources, out, alternative=False):
    from verify import ExhaustiveCheck
    syn = Counter(row["syndrome"] for row in sources)
    variants = ["syntactic", "first_component"] if alternative else ["syntactic"]
    data, summary = {}, {}
    for policy in variants:
        adj = incidence(n, sources, policy)
        index = PathIndex(adj)
        verify = ExhaustiveCheck(adj)
        graph_data = [(u, v, b) for u, row in enumerate(adj) for v, b in row if v == BOUNDARY or u < v]
        write_json(out / f"{name}_{policy}_edges.json", graph_data)
        rows = {}
        counts, global_classes, stratum, stratum_total, clusters, sizes = (Counter() for _ in range(6))
        for active in sorted(set(syn) | {()}):
            groups = index.analyse(active)
            checked = verify.analyse(active)
            assert groups == checked, (name, policy, active, groups, checked)
            mask, state = classification(groups)
            loc = "boundary_adjacent" if set(active) & index.boundary_adjacent else "interior"
            rows[active] = (groups, mask, state, loc)
            if not active:
                continue
            counts[state] += 1
            global_classes[str(mask.bit_count())] += 1
            stratum_total[loc] += 1
            if state == "ALL_CLUSTERS_BOTH":
                stratum[loc] += 1
            clusters.update(str(b.bit_count()) for _, b in groups)
            sizes.update(len(g) for g, _ in groups)
        summary[policy] = dict(distinct_nonempty=len(rows)-1, deduplicated_edges=len(graph_data),
                               shot_status=counts, shot_reachable_class_counts=global_classes,
                               cluster_class_counts=clusters, cluster_sizes=sizes,
                               nonempty_by_stratum=stratum_total, all_clusters_both_by_stratum=stratum)
        data[policy] = rows
    if alternative:
        transition = Counter((data["syntactic"][s][2], data["first_component"][s][2]) for s in syn if s)
        summary["shot_status_transitions"] = {a+" -> "+b:c for (a,b),c in sorted(transition.items())}
    with (out / f"{name}_syndromes.csv").open("w", newline="") as fp:
        w = csv.writer(fp)
        w.writerow(["policy","active_detectors","n_active","whole_source_count","boundary_stratum",
                    "clusters","reachable_per_cluster","reachable_shot_xor","section17"])
        for policy in variants:
            for active,(groups, mask,state,loc) in data[policy].items():
                w.writerow([policy," ".join(map(str,active)),len(active),syn[active],loc if active else "",
                            " | ".join(" ".join(map(str,g)) for g,_ in groups),
                            " | ".join(LABEL[b] for _,b in groups),LABEL[mask],state])
    return summary


def controls():
    # Same whole-source syndrome and flip, two different separator assignments.
    for mask, target in [(0,ZERO), (1,BOTH)]:
        adj = (((1,mask),(3,0)),((0,mask),(3,0)),((BOUNDARY,1^mask),),((0,0),(1,0)))
        assert PathIndex(adj).analyse((0,1)) == [((0,1),target)]
    adj = (((BOUNDARY,1),),((BOUNDARY,1),))
    checked = PathIndex(adj).analyse((0,1))
    assert checked == [((0,),ONE),((1,),ONE)] and classification(checked) == (ZERO,"SINGLE_CLASS_BLOCKS")
    assert PathIndex(((),)).analyse((0,)) == [((0,),0)]


def main():
    protocol = json.loads((ROOT / "protocol.json").read_text())
    assert stim.__version__ == protocol["stim_version"]
    out = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT / "results"
    out.mkdir(parents=True, exist_ok=True)
    t0 = perf_counter()
    controls()
    fixture = json.loads((ROOT / "main_fixture.json").read_text())
    graph = fixture["graph"]
    assert sha(json.dumps(graph,sort_keys=True,separators=(",",":")).encode()) == fixture["shot"]["frozen_graph_sha256"]
    edge, = graph["edges"]
    assert edge["endpoints"] == [108,"boundary"] and edge["observable_mask"] == 1
    src_fixture = [{"id":0,"p":edge["error_probability"],"syndrome":(108,),"logical":1,"parts":[((108,),1)]}]
    summary = {"main_fixture": run_case("main_fixture",graph["detector_count"],src_fixture,out)}
    start_graph = perf_counter()
    args = protocol["circuit"].copy()
    task = args.pop("task")
    circuit = stim.Circuit.generated(task,**args)
    dem = circuit.detector_error_model(decompose_errors=True)
    assert (circuit.num_detectors,circuit.num_observables)==(120,1)
    (out / "development.stim").write_text(str(circuit))
    (out / "development.dem").write_text(str(dem))
    sources = read_sources(dem)
    write_json(out / "development_sources.json", sources)
    start_enum = perf_counter()
    summary["development"] = run_case("development",120,sources,out,True)
    summary["model"] = {"detectors":120,"observables":1,"source_events":len(sources),
                         "graph_components_with_multiplicity":sum(len(x["parts"]) for x in sources),
                         "separator_events":sum(len(x["parts"])>1 for x in sources),
                         "source_events_with_no_syndrome":sum(not x["syndrome"] for x in sources),
                         "protocol_sha256":sha((ROOT/"protocol.json").read_bytes()),
                         "circuit_sha256":sha(str(circuit).encode()), "dem_sha256":sha(str(dem).encode())}
    write_json(out / "summary.json",summary)
    end = perf_counter()
    write_json(out / "timing.json",{"elapsed_seconds":end-t0, "fixture_and_controls_s":start_graph-t0,
                                    "build_model_s":start_enum-start_graph,"development_enum_and_crosscheck_s":end-start_enum})
    print(json.dumps(summary));print("total_seconds",end-t0)


if __name__ == "__main__":
    main()
