"""Reproduce the past-cone certificates, echo records and blinded material selection."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from itertools import permutations
import json
import sys
import echos
import netz
import vorfahre
ROOT=Path(__file__).resolve().parent
def encode(v):return (json.dumps(v,ensure_ascii=False,sort_keys=True,indent=2)+'\n').encode()
def preflight():
    for name in ('Pruefplan.sha256','Prueffamilie.sha256','Zusatzplan.sha256','Quellen.sha256'):
        for row in (ROOT/name).read_text().splitlines():
            digest,relative=row.split('  ',1)
            assert sha256((ROOT/relative).read_bytes()).hexdigest()==digest
def automorphisms():
    fixed=vorfahre.PAST+vorfahre.FUTURE
    permutations_found=[]
    for seq in permutations(vorfahre.INNER):
        f=dict(zip(vorfahre.INNER,seq));f.update((k,k) for k in fixed)
        if {(f[i],f[j]) for i,j in vorfahre.R}==vorfahre.R:
            permutations_found.append({str(i):f[i] for i in vorfahre.INNER if i!=f[i]})
    return permutations_found
def audit():
    preflight()
    cones=vorfahre.trial()
    assert not cones['singular']
    assert cones['counts']=={'cones_0':23,'cones_1':1656,'with_roots_0':9,'with_roots_1':53}
    assert F(cones['min_gap']['0'])>F('.04070') and F(cones['min_gap']['1'])>F('.03210')
    aut=automorphisms()
    assert aut==[{}, {'4':5,'5':4}]
    verdict,details,raw=echos.run()
    for (m,row),frame in zip(verdict.items(),raw):
        assert echos.reader(frame,0)==row['selected']
        bits=frame['final_positive']
        empty=dict(frame,final_positive='0'*len(bits))
        assert echos.reader(empty,0)=='KEINE_MATERIALKLAMMER'
    graph,edges=netz.run()
    for row in details:
        m=row['M_for_scoring'];emitter,receiver=graph[m]['orientation']
        assert receiver==verdict[m]['selected']
        for name,n in row['readings'].items():
            assert edges[m]['ticks']['|'.join(netz.edge(name,emitter))]==n
    ledger=json.loads((ROOT/'basis/vorversuch.json').read_bytes())['CST']
    assert ledger['P3']=='HOLD_NOT_ELIGIBLE' and ledger['NOT_RUN']==60
    out={'Ergebnisse.json':{'material_echos':verdict,'ungerichtetes_echonetz':graph,'cst_counts':cones['counts'],
         'cst_minimum_gap_x':cones['min_gap'],'automorphism_moved_internal_nodes':aut,
         'P3':ledger['P3'],'NOT_RUN':ledger['NOT_RUN']},'Vergangenheiten.json':cones,
         'Echoaufnahmen.json':raw,'Kontrollschluessel.json':details,'Netzaufnahmen.json':edges}
    for name,data in out.items():
        if sys.argv[1:]==['--erzeugen']:(ROOT/name).write_bytes(encode(data))
        else:assert (ROOT/name).read_bytes()==encode(data),name
    print('PASS: 23 + 1656 Vergangenheiten, beide Uhrenrechnungen, 63 Paar-Echos, drei Massentransfers und Negativkontrollen. P3: 60 NOT_RUN.')
if __name__=='__main__':
    if not __debug__:raise SystemExit('Python ohne -O ausführen.')
    audit()
