"""Check every certificate against sources, then intervene using the PR 222 independent solver."""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/"in"))
from verify import ExhaustiveCheck


def read(p):
    return json.loads(p.read_text())


def check_path_certificate(w, group, active, policy, sites, src):
    endpoints=[]
    expected=[]
    parity=0
    for p in w['paths']:
        assert p[0] in group and len(p)>=2 and len(set(p))==len(p)
        assert not set(p[1:-1]) & (set(active)|{-1})
        if p[-1]==-1:
            assert len(p)-1<=2
            endpoints += [p[0]]
        else:
            assert len(p)-1<=4 and p[-1] in group
            endpoints += [p[0],p[-1]]
        expected.extend([u,v] if v==-1 else sorted((u,v)) for u,v in zip(p,p[1:]))
    assert sorted(endpoints)==sorted(group) and len(expected)==len(w['steps'])
    for target,(eid,b,sid,comp) in zip(expected,w['steps']):
        assert 0<=eid<len(sites) and sites[eid]['ends']==target and b in (0,1)
        source=src[sid]
        assert source['id']==sid and 0<=comp<len(source['parts'])
        ends,mask=source['parts'][comp]
        assert (sorted(ends) if len(ends)==2 else ends+[-1])==target
        assert b==(mask if policy==0 else source['logical']*int(comp==0))
        parity^=b
    assert parity==w['parity']


def graph(sites,enabled):
    adj=[set() for _ in range(120)]
    for i,s in enumerate(sites):
        u,v=s["ends"]
        bits=(0,1) if i in enabled else (s["primary_bit"],)
        for b in bits:
            adj[u].add((v,b))
            if v!=-1:
                adj[v].add((u,b))
    return tuple(tuple(sorted(nodes)) for nodes in adj)


def main(out):
    sites=read(out/"sites.json")
    sources=read(ROOT/"in/results/development_sources.json")
    whole=defaultdict(lambda:defaultdict(list))
    for source in sources:
        whole[tuple(source['syndrome'])][str(source['logical'])].append(source['id'])
    by=defaultdict(dict)
    for row in csv.DictReader((ROOT/"in/results/development_syndromes.csv").open()):
        s=tuple(map(int,row['active_detectors'].split()))
        if s:
            by[s][row['policy']]=row
    recs={tuple(r['active']):r for r in map(json.loads,(out/'witnesses.jsonl').read_text().splitlines())}
    selected={s for s,r in by.items() if r['first_component']['section17']=='ALL_CLUSTERS_BOTH'}
    assert recs.keys()==selected and len(recs)==979 and len(by)==1679
    certs=0
    for active,rec in recs.items():
        old=by[active]['syntactic']
        assert rec['group']==('shared' if old['section17']=='ALL_CLUSTERS_BOTH' else 'gained')
        assert rec['single_whole_event_ids_by_bit']==whole[active]
        assert [c['cluster'] for c in rec['clusters']]==[list(map(int,v.split())) for v in old['clusters'].split(' | ')]
        for i,c in enumerate(rec['clusters']):
            assert sorted(w['parity'] for w in c['primary'])==list(map(int,old['reachable_per_cluster'].split(' | ')[i]))
            assert [w['parity'] for w in c['alternative']]==[0,1]
            for pol,key in [(0,'primary'),(1,'alternative')]:
                for w in c[key]:
                    check_path_certificate(w,c['cluster'],active,pol,sites,sources)
                    certs+=1
            a,b=c['alternative']
            assert a['paths']==b['paths']
            changed=[x[0] for x,y in zip(a['steps'],b['steps']) if x[1]!=y[1]]
            assert len(changed)==1
            if len(c['primary'])==1:
                assert changed[0] in rec['sufficient_sites']

    ambiguous=[i for i,s in enumerate(sites) if len(s['sources'][1])==2]
    assert len(ambiguous)==61
    def eligibles(enabled, samples):
        solver=ExhaustiveCheck(graph(sites,enabled))
        try:
            return {s for s in samples if all(mask==3 for _,mask in solver.analyse(s))}
        finally:
            solver.pair_paths.cache_clear()
    shared={s for s,r in recs.items() if r['group']=='shared'}
    assert eligibles(set(),by)==shared and eligibles(set(ambiguous),by)==selected
    one_site=defaultdict(set)
    for i in ambiguous:
        for s in eligibles({i},by):
            one_site[s].add(i)
    pairs=defaultdict(list)
    for s,r in recs.items():
        selected_sites=r['sufficient_sites']
        assert len(selected_sites)==r['min_sites_to_enable']
        if s in shared:
            assert r['min_sites_to_enable']==0
        elif s in one_site:
            assert r['min_sites_to_enable']==1 and selected_sites[0] in one_site[s]
        else:
            assert len(set(selected_sites))==2
            pairs[tuple(selected_sites)].append(s)
    assert set(one_site)<=selected
    for enabled,cases in pairs.items():
        assert eligibles(set(enabled),cases)==set(cases)

    # Independently separate the two pairing types for all primary shared controls.
    solver=ExhaustiveCheck(graph(sites,set()))
    signatures=Counter()
    for s in shared:
        a,b=s
        def path_bits(x,y):
            return {parity for internal,parity in solver.pair_paths(x,y) if set(s).isdisjoint(internal)}
        direct=path_bits(a,b)
        separate={x^y for x in path_bits(a,-1) for y in path_bits(b,-1)}
        assert len(direct)==len(separate)==1 and direct!=separate
        signatures[f'DD={min(direct)},BB={min(separate)}']+=1
    solver.pair_paths.cache_clear()
    answer={'syndromes_per_single_site_intervention':len(by),'single_site_interventions':len(ambiguous),
            'syndrome_site_decisions':len(by)*len(ambiguous),'concrete_certificates_checked':certs,
            'distinct_two_site_interventions_for_selected_pairs':len(pairs),
            'two_site_cases_checked':sum(map(len,pairs.values())),'primary_controls':signatures,
            'one_site_gained':len(set(one_site)-shared),'unaffected_cases':len(by)-len(selected)}
    (out/'verification.json').write_text(json.dumps(answer,sort_keys=True,indent=2)+'\n')
    print(answer)


if __name__=='__main__':
    main(Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results')
