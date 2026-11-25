"""Independent look-up of order signatures against the published two-percent test."""
import csv
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from hashlib import sha256

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'quellen'))
from diamanten import build, profile, SECTORS, NODES, P, F, I, CATALOG_HASH


def main():
    data = (ROOT/'quellen/gesamtkatalog.json').read_bytes()
    assert sha256(data).hexdigest() == CATALOG_HASH
    catalog = json.loads(data)['ranks_pure_free_mixed']
    rows = list(csv.DictReader((ROOT/'quellen/entscheidungen.csv').read_text().splitlines()))
    judgments = {(int(r['type']),r['inlet_density_center']):r['status'] for r in rows}
    eligible = {k for k,d in judgments}
    assert len(rows)==len(judgments)==122 and len(eligible)==61 and {r['mass'] for r in rows}=={'4'}
    centers = ('1/8','1/4')
    groups = {name:defaultdict(list) for name in ('fest','alle','sektoren')}
    response = {}
    for code, (pure, _, mixed) in catalog.items():
        if pure or mixed:
            continue
        code = int(code)
        relation = build(code)
        pairs,plain,tagged = profile(relation,NODES,SECTORS)
        keys = (pairs[P[-1],F[0]], plain, tagged)
        for group,key in zip(groups.values(),keys):
            group[key].append(code)
        # -19 * partial_(w_j) partial^2_(Y_j) S for each j in the interior.
        response[code] = sorted(sum((1,-9,16,-8)[k] for (i,target),(k,_) in pairs.items()
                                     if target==j and k<4) for j in I)
    summary = {}
    for name, group in groups.items():
        assert sum(map(len,group.values()))==1048
        chain_classes = [members for members in group.values() if 2097151 in members]
        assert len(chain_classes)==1
        comparison = {}
        for center in centers:
            conflict, comparable = [], 0
            occupied = 0
            for members in group.values():
                known = sorted(set(members) & eligible)
                if known:
                    occupied += 1
                if len(known)>=2:
                    comparable += 1
                statuses = {judgments[c,center] for c in known}
                if len(statuses)>1:
                    reps = {s:min(c for c in known if judgments[c,center]==s) for s in sorted(statuses)}
                    conflict.append(reps)
            comparison[center] = {'occupied_classes_in_61':occupied,'classes_with_two_or_more_known':comparable,
                                  'classes_with_different_decisions':len(conflict),'witnesses':conflict}
        varying = [sorted(m) for m in group.values() if len({tuple(response[c]) for c in m})>1]
        summary[name]={'classes':len(group),'multi':sum(len(m)>1 for m in group.values()),
                       'unique_chain_class':sorted(chain_classes[0]),'decisions_M4':comparison,
                       'classes_with_different_local_action_spectra':len(varying)}
        refined = {(key,tuple(response[c])) for key,members in group.items() for c in members}
        summary[name]['classes_after_adding_local_action_spectrum'] = len(refined)
        if varying:
            members = min(varying)
            first = members[0]
            second = next(c for c in members if response[first] != response[c])
            summary[name]['action_witness']={str(c): response[c] for c in (first, second)}
    chain_pairs, _, _ = profile(build(2097151),NODES,SECTORS)
    assert len(chain_pairs)==105 and chain_pairs[3,7]==(7,8)
    return {'signatures':summary,'chain_in_M4_sample':2097151 in eligible,
            'chain_comparable_pairs_each_half':len(chain_pairs),
            'chain_fixed_diamond_each_half':chain_pairs[3,7],
            'witness_37724_37738':{str(c):response[c] for c in (37724,37738)},
            'M4_counts':dict(Counter(judgments.values()))}


if __name__=='__main__':
    print(json.dumps(main(),indent=2))
