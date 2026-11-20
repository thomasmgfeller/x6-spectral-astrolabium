"""Re-enumerate the marked prefixes from the published incidence data only."""
from collections import Counter, defaultdict
from itertools import permutations
import argparse
import json
from pathlib import Path
from study import source, write_fresh, TYPES


def enumerate_family(check, data):
    prefixes=set()
    for key in data['target_pair_marginal']:
        code=int(key)
        prefixes.add(code)
        prefixes.add(check.relabel(check.decode(code),(0,1,2,4,3,5)))
    rows=defaultdict(Counter)
    orbit_count=0
    for end in data['fully_admissible_end_types']:
        edges=[e for i,e in enumerate(check.EDGES) if end & (1<<i)]
        for code in {check.relabel(edges,p) for p in check.LABELS}:
            if (code&check.MASK) not in prefixes:
                continue
            orbit={check.relabel(check.decode(code),p) for p in check.MARKS}
            if min(orbit)!=code or any((c&check.MASK) not in prefixes for c in orbit):
                continue
            orbit_count+=1
            for c in orbit:rows[c&check.MASK][end]+=1
    assert orbit_count==data['fully_admissible_orbits']
    assert sum(sum(r.values()) for r in rows.values())==data['paths_valid_in_all_six_orders']
    return rows


def select():
    with source() as upstream:
        import check
        exchange=json.loads((upstream/'inputs/exchange.json').read_text())
        old=enumerate_family(check,exchange['one'])[1564]
        candidates=enumerate_family(check,exchange['chain'])
        def canon(code):
            return min(check.relabel(check.decode(code),p) for p in permutations(range(5)))
        allowed=[p for p,x in sorted(candidates.items())
                 if canon(p)!=canon(1564) and len(x)>=2 and set(x).isdisjoint(old)]
        chosen=allowed[0]
        counts=candidates[chosen]
        assert chosen==270 and tuple(sorted(counts))==TYPES and sum(counts.values())==15
        return {'selection':'Smallest eligible marked code in the chain family; at least two end types, disjoint old end support, nonisomorphic five-inner-event prefix.',
                'candidate':chosen,'eligible_prefixes':len(allowed),'canonical_inner_prefix':canon(chosen),
                'canonical_old_inner_prefix':canon(1564),'end_types':list(TYPES),
                'paths_by_end_type':dict(sorted(counts.items())),'marked_paths':sum(counts.values()),
                'reference_target_amplitudes_used_for_selection':0}

if __name__=='__main__':
    if not __debug__:raise SystemExit('Keep assertions enabled.')
    ap=argparse.ArgumentParser()
    ap.add_argument('output',type=Path)
    write_fresh(ap.parse_args().output,select())
