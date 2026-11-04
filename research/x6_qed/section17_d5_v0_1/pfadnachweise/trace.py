"""Construct provenance-bearing witnesses for the graph and populations of X6 PR 222."""
import csv
import json
from collections import Counter, defaultdict
from functools import lru_cache
from itertools import product
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent


def dump(path, obj):
    path.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def edge(u, v):
    return (u, v) if v == -1 else tuple(sorted((u, v)))


def ids(s):
    return tuple(map(int, s.split()))


def build_graph(sources):
    provenance = defaultdict(lambda: [defaultdict(list), defaultdict(list)])
    for row in sources:
        totals = set()
        parity = 0
        for i, (ends, mask) in enumerate(row["parts"]):
            assert 1 <= len(ends) <= 2
            key = edge(ends[0], ends[-1] if len(ends) == 2 else -1)
            provenance[key][0][mask].append((row["id"], i))
            moved = row["logical"] if i == 0 else 0
            provenance[key][1][moved].append((row["id"], i))
            totals.symmetric_difference_update(ends)
            parity ^= mask
        assert sorted(totals) == row["syndrome"] and parity == row["logical"]
    sites = sorted(provenance)
    graph = []
    for u,v in sites:
        maps = provenance[u,v]
        assert len(maps[0]) == 1 and maps[0].keys() <= maps[1].keys()
        graph.append({"ends": [u,v], "primary_bit": next(iter(maps[0])),
                      "sources": [{str(k): sorted(cites) for k,cites in pol.items()} for pol in maps]})
    return graph


class Routes:
    def __init__(self, graph):
        self.graph = graph
        self.site_id = {tuple(d["ends"]): i for i,d in enumerate(graph)}
        adj = defaultdict(set)
        for u,v in self.site_id:
            adj[u].add(v)
            if v != -1:
                adj[v].add(u)
        self.paths = defaultdict(list)
        for start in sorted(adj):
            def dfs(path):
                for v in sorted(adj[path[-1]]):
                    if v == -1:
                        if len(path) <= 2:
                            self.paths[start, -1].append(path + (v,))
                    elif v not in path:
                        nxt = path + (v,)
                        self.paths[start,v].append(nxt)
                        if len(nxt)-1 < 4:
                            dfs(nxt)
            dfs((start,))

    @lru_cache(None)
    def describe(self, geom):
        sites = tuple(self.site_id[edge(u,v)] for path in geom for u,v in zip(path,path[1:]))
        bit = sum(self.graph[e]["primary_bit"] for e in sites) % 2
        amb = {e for e in sites if len(self.graph[e]["sources"][1]) == 2}
        return sites, bit, amb

    def geometries(self, g, active):
        def paths(u,v):
            return [p for p in self.paths[u,v] if active.isdisjoint(p[1:-1])]
        if len(g) == 1:
            options = [(p,) for p in paths(g[0],-1)]
        else:
            assert len(g) == 2  # verified for every cluster of this finite dataset
            u,v = g
            options = [(p,) for p in paths(u,v)] + list(product(paths(u,-1),paths(v,-1)))
        return sorted(options, key=lambda x:(sum(len(p)-1 for p in x), x))

    def realization(self, geom, policy, flipped=None):
        sites, primary, _ = self.describe(geom)
        chosen = []
        for i,e in enumerate(sites):
            bit = self.graph[e]["primary_bit"] ^ int(i == flipped)
            ref = self.graph[e]["sources"][policy][str(bit)][0]
            chosen.append([e,bit,*ref])  # site ID, logical bit, source ID, component index
        return {"paths": geom, "steps":chosen, "parity":primary ^ int(flipped is not None)}

    def cluster(self, g, active, emit):
        options = self.geometries(g,active)
        by_bit = {}
        allowed = set()
        by_type = defaultdict(dict)
        for geom in options:
            sites,bit,amb = self.describe(geom)
            by_bit.setdefault(bit,geom)
            by_type[tuple(p[-1] == -1 for p in geom)].setdefault(bit,geom)
            allowed.update(amb)
        classes = set(by_bit)
        alternate = {0,1} if allowed else classes
        summary = (classes, alternate, allowed)
        if not emit:
            return summary, None

        # If possible, preserve the pairing type even for two distinct primary routes.
        same_type = next((pairs for pairs in by_type.values() if len(pairs)==2),None)
        primary_witnesses = same_type if same_type is not None else by_bit
        audit = {"cluster":g, "primary":[self.realization(geom,0) for _,geom in sorted(primary_witnesses.items())],
                 "same_pairing_type_primary":(same_type is not None), "flippable_sites":sorted(allowed)}
        audit["alternative"] = self.alt_witnesses(options,allowed,None) if allowed else [
            self.realization(geom,1) for _,geom in sorted(primary_witnesses.items())]
        return summary,(audit,options)

    def alt_witnesses(self, options, allowed, permitted):
        choices = allowed if permitted is None else allowed.intersection(permitted)
        for geom in options:
            sites,bit,amb = self.describe(geom)
            if choices & amb:
                j = min((i for i,e in enumerate(sites) if e in choices),
                        key=lambda i:(sites.count(sites[i]) != 1,i))
                pair = [self.realization(geom,1),self.realization(geom,1,j)]
                return sorted(pair,key=lambda w:w["parity"])
        raise ValueError("No eligible same-geometry flip")


def main(out):
    out.mkdir(parents=True,exist_ok=True)
    src=BASE / "in/results"
    sources=json.loads((src/"development_sources.json").read_text())
    whole=defaultdict(lambda:defaultdict(list))
    for row in sources:
        whole[tuple(row["syndrome"])][row["logical"]].append(row["id"])
    graph=build_graph(sources)
    for i,name in enumerate(("syntactic","first_component")):
        original=json.loads((src/f"development_{name}_edges.json").read_text())
        calculated={(u,v,int(b)) for s in graph for u,v in [s["ends"]] for b in s["sources"][i]}
        assert calculated==set(map(tuple,original))
    dump(out/"sites.json",graph)
    routes=Routes(graph)
    records=defaultdict(dict)
    with (src/"development_syndromes.csv").open() as f:
        for row in csv.DictReader(f):
            active=ids(row["active_detectors"])
            if active:
                records[active][row["policy"]]=row
    counts=Counter()
    report=[]
    with (out/"witnesses.jsonl").open("w") as log:
        for active,pair in sorted(records.items()):
            old=pair["syntactic"]; new=pair["first_component"]
            gained=old["section17"]!=new["section17"]
            keep=new["section17"]=="ALL_CLUSTERS_BOTH"
            kind="gained" if gained else ("shared" if keep else "other")
            groups=[ids(g) for g in old["clusters"].split(" | ")]
            assert old["clusters"]==new["clusters"]
            infos=[]; supports=[]; bits_primary=[]; bits_alt=[]
            for g in groups:
                (classes,alt,allowed),info=routes.cluster(g,set(active),keep)
                bits_primary.append(''.join(map(str,sorted(classes))) or '-')
                bits_alt.append(''.join(map(str,sorted(alt))) or '-')
                if keep:
                    infos.append(info)
                    if len(classes)==1:
                        supports.append(allowed)
            assert " | ".join(bits_primary)==old["reachable_per_cluster"]
            assert " | ".join(bits_alt)==new["reachable_per_cluster"]
            counts[kind]+=1
            if not keep:
                continue
            assert len(supports)<=2
            if not supports:
                minimum,chosen=0,()
            else:
                common=set.intersection(*supports)
                if common:
                    minimum,chosen=1,(min(common),)
                else:
                    assert len(supports)==2 and all(supports)
                    minimum,chosen=2,tuple(min(s) for s in supports)
            audit=[]
            for rec,options in infos:
                if len(rec["primary"])==1:
                    rec["alternative"]=routes.alt_witnesses(options,set(rec["flippable_sites"]),set(chosen))
                audit.append(rec)
            same_all=all(len(cl["alternative"])==2 and
                         cl["alternative"][0]["paths"]==cl["alternative"][1]["paths"] for cl in audit)
            counts[f'{kind}_same_geometry_in_all_clusters_{same_all}']+=1
            counts[f'{kind}_min_sites_{minimum}']+=1
            counts[f'{kind}_originally_blocked_clusters_{len(supports)}']+=1
            counts[f'{kind}_whole_source_class_count_{len(whole[active])}']+=1
            counts[f'{kind}_primary_shot_class_count_{len(old["reachable_shot_xor"])}']+=1
            if kind=='shared':
                counts[f'shared_same_pairing_in_primary_{audit[0]["same_pairing_type_primary"]}']+=1
                first=audit[0]["primary"]
                counts['shared_primary_witness_types_'+'_'.join("B" if w["paths"][0][-1]==-1 else "D" for w in first)]+=1
            rec={"active":active,"group":kind,"clusters":audit,"min_sites_to_enable":minimum,
                 "sufficient_sites":chosen,"single_whole_event_ids_by_bit":whole[active]}
            log.write(json.dumps(rec,separators=(',',':'))+'\n')
            report.append([kind,' '.join(map(str,active)),len(groups),' | '.join(bits_primary),
                           ' | '.join(bits_alt),len(supports),minimum,' '.join(map(str,chosen)),
                           int(same_all),' '.join(map(str,whole[active]))])
    with (out/'cases.csv').open('w',newline='') as f:
        w=csv.writer(f);w.writerow(['group','active_detectors','n_clusters','primary_per_cluster','alternative_per_cluster',
                                    'previously_blocked_clusters','min_distinct_sites','sufficient_site_ids',
                                    'same_geometry_in_all_alt_clusters','single_whole_event_bits'])
        w.writerows(report)
    counts['endpoint_pairs']=len(graph)
    counts['unchanged_single_mask']=sum(len(e['sources'][1])==1 for e in graph)
    counts['ambiguous_alt']=sum(len(e['sources'][1])==2 for e in graph)
    counts['primary_zero_to_both']=sum(e['primary_bit']==0 and len(e['sources'][1])==2 for e in graph)
    counts['primary_one_to_both']=sum(e['primary_bit']==1 and len(e['sources'][1])==2 for e in graph)
    counts['population_checked']=len(records)
    dump(out/'summary.json',counts)


if __name__=='__main__':
    main(Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'results')
