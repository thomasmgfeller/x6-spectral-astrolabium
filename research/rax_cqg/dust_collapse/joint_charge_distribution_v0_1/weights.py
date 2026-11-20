"""Project each published positive column witness onto its actual N15 daughters."""
from collections import Counter, defaultdict
from fractions import Fraction as F
from itertools import combinations, permutations
import json
from pathlib import Path
import sys
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE/"inputs/four"))
from extension import load_inputs, marked_three, SEVEN

def run():
    d,res,weights,cat=load_inputs()
    reps,lookup,parents,_=marked_three(d,res,weights)
    columns=defaultdict(lambda: defaultdict(set))
    good=[int(k) for k,(a,_,b) in cat['ranks_pure_free_mixed'].items() if a==b==0]
    for code in sorted(good):
        edges=[e for bit,e in enumerate(SEVEN) if code>>bit & 1]
        for root in permutations(range(7),3):
            rootpos={v:i for i,v in enumerate(root)}
            if {(rootpos[a],rootpos[b]) for a,b in edges if a in rootpos and b in rootpos}!={(0,2)}:
                continue
            extras=tuple(v for v in range(7) if v not in root)
            projections=[]
            for deleted in extras:
                order=root+tuple(v for v in extras if v!=deleted)
                pos={v:i for i,v in enumerate(order)}
                raw=sum(1<<(6*pos[a]+pos[b]) for a,b in edges if deleted not in (a,b))
                if raw not in lookup: break
                projections.append(lookup[raw])
            if len(projections)!=4: continue
            col=tuple(sorted(projections))
            def mark(seq):
                pos={v:i for i,v in enumerate(root+seq)}
                return sum(1<<(7*pos[a]+pos[b]) for a,b in edges)
            columns[col][code].add(min(mark(p) for p in permutations(extras)))
    assert len(columns)==928
    certificates=json.loads((BASE/'inputs/four/local_proof.json').read_text())
    laws={}
    for label,t in [('1:1','0'),('1:3','1/1764')]:
        z=certificates[t]
        residual={tuple(map(int,k.split(','))):F(v) for k,v in z['residual_column_weights'].items()}
        assert set(residual)<=columns.keys()
        law=Counter(); inherited=Counter();local=Counter()
        for col,group in columns.items():
            weight=F(z['common_floor_per_column'])+residual.get(col,0)
            n=sum(map(len,group.values()))
            for code,orbits in group.items(): law[code]+=weight*len(orbits)/n
            for orbit in col:
                end, paths=reps[orbit]
                for raw in paths:
                    from extension import MASK
                    part=weight/(4*len(paths))
                    inherited[raw&MASK]+=part
                    if raw&MASK==1564: local[end]+=part
        assert inherited==parents and local[1790]/local[5374]==(1 if t=='0' else F(1,3))
        assert sum(law.values())==1 and min(law.values())>0
        laws[label]={str(k):str(v) for k,v in sorted(law.items())}
    return {'catalogue_total':len(good),'columns':len(columns),'fine_orbits':sum(len(c) for g in columns.values() for c in g.values()),'types':len(laws['1:1']),'laws':laws}
if __name__=='__main__': print(json.dumps(run(),sort_keys=True,indent=2))
