"""Independent completeness check and direct rational tests of the elimination identities."""
import csv
import json
from collections import Counter
from fractions import Fraction as Q
from pathlib import Path

ROOT=Path(__file__).resolve().parent
P=ROOT/'basis'
base=json.loads((P/'Vergleichspaar.json').read_text())
probes=json.loads((P/'Sonden_auf_N23.json').read_text())
records=list(csv.DictReader((ROOT/'Fallregister.tsv').open(),delimiter='\t'))
summary=json.loads((ROOT/'Ergebnisse.json').read_text())

def generate(rel):
    chains={frozenset()}
    for j in range(23):
        chains |= {a|{j} for a in chains if all((i,j) not in rel and (j,i) not in rel for i in a)}
    pasts={frozenset(a|{i for i,j in rel if j in a}) for a in chains}
    futures={frozenset(a|{j for i,j in rel if i in a}) for a in chains}
    return {(p,f) for p in pasts if 22 in p for f in futures if all((i,j) in rel for i in p for j in f)}

def decode(x):
    return frozenset(int(i) for i in x.split(',') if i)

def coeff(rel,i,j):
    if (i,j) not in rel:
        return 0
    inside={n for n,k in rel if k==j}&{n for k,n in rel if k==i}
    return (1,-9,16,-8,0)[min(len(inside),4)]-Q((i,j) in ((15,16),(16,18),(17,18),(18,7)),10**11)

def identities(rel,p):
    parents={i:coeff(rel,i,23) for i in p}
    y={i:Q((i+2)**2-7*i+3,13) for i in range(24)}
    a=sum(parents.values())
    even=sum(k*y[i]**2 for i,k in parents.items())
    b=sum(k*y[i] for i,k in parents.items())
    d=19+sum(k*(y[23]-y[i])**2 for i,k in parents.items())
    h=sum(k*(y[23]-y[i]) for i,k in parents.items())
    variance=sum(parents[i]*parents[j]*(y[i]-y[j])**2 for i in parents for j in parents if i<j)
    assert a*d-h*h==19*a+variance
    assert a or d==19+even-2*y[23]*b
    k=coeff(rel,22,23)
    if not k:
        return
    w={j:Q((j+1)**2,2653) for j in range(24)}
    force=sum(coeff(rel,22,j)*w[j]*(y[j]-y[22]) for j in range(22))
    g=force+k*w[23]*(y[23]-y[22])
    for i in parents:
        direct=w[23]*(y[23]-y[i])
        eliminated=-force/k+w[23]*(y[22]-y[i])
        assert direct-eliminated==g/k

for name,row in summary.items():
    side,starts=name.split('_')
    start=set(map(int,starts.split(',')))
    given=[p for p in probes[side] if p['start'] in start]
    assert len(given)==len(start) and all(p['order']==given[0]['order'] for p in given)
    rel=set(map(tuple,base['relation']))|{(i,22) for i in given[0]['order']['past']}|{(22,j) for j in given[0]['order']['future']}
    available=generate(rel)
    relevant=[r for r in records if (r['praeparation'],r['bahnen_von'])==(side,starts)]
    enumerated={(decode(r['alte_vergangenheit_23_mit_22']),decode(r['alte_zukunft_23'])) for r in relevant}
    assert available==enumerated and len(relevant)==len(enumerated)
    assert row['cases']=={'AUSGESCHLOSSEN':len(available)} and all(r['status']=='AUSGESCHLOSSEN' for r in relevant)
    assert row['rules']==dict(Counter(r['grund'] for r in relevant))
    assert Q(row['positive_probe_D22'][1])<0 and Q(row['minimum_certificate_margin'])>0
    for p,f in available:
        if not f:
            identities(rel|{(i,23) for i in p},p)
assert len(records)==1514
print('1514 Zustands-/Ordnungsfälle über Antiketten bestätigt. Terminalidentitäten direkt geprüft.')
