"""Offline reproduction and comparison against the archived results using Python 3.10+."""
from fractions import Fraction as F
from pathlib import Path
from hashlib import sha256
from io import StringIO
import argparse
import json
import csv
from geometrie import causal, inside_clock, balls, probes, contact_test, extended_order
from ordnung import enumerate_shadows
from stationaritaet import check
from leersonde import scan

ROOT=Path(__file__).resolve().parent
PIN='c75c0c97c1b536d0140d77b4f01d8bfa0a2aab487a1b05a2b58f2ebf23159c2f'
def read_boxes(z): return [tuple(map(F,v)) for v in z]
def tables():
    source=ROOT/'basis/Vergleichspaar.json'
    assert sha256(source.read_bytes()).hexdigest()==PIN
    for name in ('Pruefplan','Ergaenzung_Kugel','Sondenstationaritaet'):
        assert sha256((ROOT/(name+'.md')).read_bytes()).hexdigest()==(ROOT/(name+'.sha256')).read_text().split()[0]
    d=json.loads(source.read_text()); rel=set(map(tuple,d['relation']))
    assert d['physical_radius_heavy'] is None and d['physical_radius_light'] is None
    assert len(rel)==152 and all(i!=j and (j,i) not in rel for i,j in rel)
    assert all((i,k) in rel for i,j in rel for l,k in rel if j==l)
    p=read_boxes(json.loads((ROOT/'Ortskoordinaten.json').read_text()))
    assert len(p)==22 and all(len(v)==3 for v in p)
    topo=enumerate_shadows(set(range(22)),rel,(17,19,20))
    assert topo['proper_families']==1373 and topo['max_betti2']==0
    out=StringIO()
    w=csv.writer(out,delimiter='\t',lineterminator='\n')
    w.writerow(('Praeparation','Start','Durchgang','Kugel_R1','Kugel_R2','Distanzquadrat_R1_unten','Distanzquadrat_R1_oben','Distanzquadrat_R2_unten','Distanzquadrat_R2_oben'))
    records={}
    for state in ('heavy','light'):
        row=d[state];clock=read_boxes(row['normalized_clocks']); weights=read_boxes(row['weight_box'])
        assert all(lo<=hi for lo,hi in clock+weights)
        positive=inside_clock(clock,weights)
        assert positive==set(range(22))-{15,17,20}
        occ={i for i,(lo,hi) in enumerate(clock) if F(15,32)<=lo<=hi<=F(17,32)}
        assert [sorted(occ&positive),sorted(occ-positive)]==[row['positive_in_window'],row['zero_in_window']]
        contacts={(a,b) for a in occ&positive for b in occ-positive if (a,b) not in rel and (b,a) not in rel
                  and any((j,a) in rel and (j,b) in rel for j in positive)
                  and any((a,j) in rel and (b,j) in rel for j in positive)}
        assert sorted(map(list,contacts))==[q['pair'] for q in row['contacts']]
        margin=causal(p,clock,rel)
        sphere=balls(p,clock,positive);probe=probes(p,clock,rel)
        separating=[]; extensions=[]
        for q in probe:
            a,b=q['balls'];i,j=q['von'],q['durch']
            assert 'offen' not in (a['tag'],b['tag'])
            if a['tag']!=b['tag']:
                separating.append((i,j))
                extensions.append(dict(start=i,via=j,order=extended_order(p,clock,rel,q),
                                       predicted=[a['tag'],b['tag']],point_box=q['point_box']))
            w.writerow((state,i,j,a['tag'],b['tag'],*a['d2'],*b['d2']))
            if (i,j) in [(4,11),(5,11)]:
                assert a['d2'][1]<F('0.601')**2 and b['d2'][0]>F('2.0052')**2
        assert separating==[(3,11),(4,11),(5,11)]
        for e in extensions:
            e['discrete']=check(rel,e['order'],read_boxes(row['clock_box']),weights)
        between=probes(p,clock,rel,extend=False)
        assert all(q['balls'][0]['tag']==q['balls'][1]['tag']!='offen' for q in between)
        records[state]=dict(boxes_checked=231,positive=sorted(positive),minimum_squared_causal_margin=margin,
                           sphere=sphere,contact_planes=contact_test(p,clock,rel,positive),probe_count=len(probe),
                           discriminating_probes=separating,interpolated_pairs=between, extensions=extensions,
                           empty_futures=scan(rel,read_boxes(row['clock_box']),weights,clock))
    extensions={k:v['extensions'] for k,v in records.items()}
    report=dict(source_sha256=PIN,order_id=d['order_id'],comparison=records,shadows=topo,
                radius_control=[1,2],area_control_in_pi=[4,16],minimax_radius='1/3',minimax_area='3/5',
                physical_pilot_radii=[None]*8,physical_P3='NOT_RUN',physical_P3_count=60)
    return {'Ergebnisse.json':json.dumps(report,indent=2,sort_keys=True,default=str)+'\n', 'Sondenregister.tsv':out.getvalue(),
            'Sonden_auf_N23.json':json.dumps(extensions,indent=2,sort_keys=True,default=str)+'\n' }

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen')
    parser=argparse.ArgumentParser();parser.add_argument('--ausgabe',action='store_true')
    args=parser.parse_args()
    for name,text in tables().items():
        if args.ausgabe:(ROOT/name).write_text(text,encoding='utf-8')
        else:assert (ROOT/name).read_bytes()==text.encode('utf-8'),name
    print('Zwei Kugelgrenzen auf beiden Feldboxen bestätigt. 1373 Schattenfamilien geprüft.')
