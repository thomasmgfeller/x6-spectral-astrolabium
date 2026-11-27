"""Reproduce the full two-coordinate scan and the three-coordinate obstructions."""
import argparse,csv,io,json
from fractions import Fraction as F
from hashlib import sha256
from itertools import combinations
from math import ceil
from zukunftsbasis import inputs,ROOT,FUTURE,name

def verify_plan():
    for plan in ('Pruefplan','Uhrenaufloesung'):
        assert sha256((ROOT/(plan+'.md')).read_bytes()).hexdigest()==(ROOT/(plan+'.sha256')).read_text().split()[0]

def run():
    verify_plan()
    with inputs() as (seed,collar,coeff,free,rel,goals,old):
        from paarstudie import certify
        from sekanten import domain,solve_triple,audit_identity,UNIT,ALL
        from randversuch import SOURCES
        from leseregel import STEP,ERROR
        rows=[];checks=0
        assert len(rel)==152 and tuple(sorted(a for a,b in rel if b==16))==(0,1,2,15)
        assert tuple(map(str,goals))==tuple(old['matched_currents'][0]['goals'])
        for fixed in combinations(FUTURE,2):
            cases=[certify(seed,collar,s,coeff,free,rel,goals,fixed) for s in SOURCES]
            assert all(r['labels']==[int(s*10**6)] for s,r in zip(SOURCES,cases))
            for k,j in fixed:
                assert all(r[k][j]==collar[str(j)][0 if k=='y' else 1] for r in cases)
            # Every free future field must differ between sources in the actual pair.
            for a,b in combinations(cases,2):
                for k,j in set(FUTURE)-set(fixed):
                    l,h=map(F,a[k][j]);u,v=map(F,b[k][j])
                    assert h<u or v<l
                checks+=audit_identity(a,b,coeff,free)
            if tuple(map(name,fixed))==('y10','w10'):
                for a,b in zip(cases,old['matched_currents']):
                    assert a['source']==b['J'] and a['codes']==b['receiver_codes']
                    l,h=map(F,a['y'][21]);u,v=map(F,b['receiver'])
                    assert max(l,u)<=min(h,v)
            rows+=cases
        assert len(rows)==63
        bounds=domain(rows,free)
        for s in rows:
            for k,j in ALL:
                l,h=bounds[k,j]
                assert F(l,UNIT)<=F(s[k][j][0])<=F(s[k][j][1])<=F(h,UNIT)
        negatives=[]
        for triple in combinations(FUTURE,3):
            proof=solve_triple(bounds,free,coeff,triple,clock_bound=triple==FUTURE[:3])
            assert proof['certified'] and F(proof['upper_norm'])<1
            negatives.append(proof)
        assert len(negatives)==35
        clock=negatives[0]['clock_bound']
        lower=F(clock['minimum_adjacent_gap'])
        assert lower>F(4276,10**9)
        ticks=ceil((lower-2*ERROR)/STEP-1)
        assert ticks==20
        groups=[]
        for s in SOURCES:
            group=[r for r in rows if F(r['source'])==s]
            l=min(F(r['y'][21][0]) for r in group);h=max(F(r['y'][21][1]) for r in group)
            codes=[min(r['codes'][0] for r in group),max(r['codes'][1] for r in group)]
            groups.append(dict(source=str(s),cases=len(group),analog=[str(l),str(h)],spread=str(h-l),codes=codes))
        return dict(fixed_early_goals=list(map(str,goals)),future=[name(t) for t in FUTURE],witnesses=rows,
                    triples=negatives,domain_grid=str(UNIT),domain={name(a):list(map(str,v)) for a,v in bounds.items()},
                    receiver=groups,independent_secant_components=checks,
                    minimum_future_code_distance=ticks,P3_NOT_RUN=old['P3_NOT_RUN'],physical_readings=0)

def tables(result):
    def make(header,rows):
        stream=io.StringIO();out=csv.writer(stream,delimiter='\t',lineterminator='\n')
        out.writerow(header);out.writerows(rows)
        return stream.getvalue()
    positive=make(['Fest_1','Fest_2','Quelle','Y21_unten','Y21_oben','Code_min','Code_max','Leserlabels','Bildnorm_max'],
        [[*v['fixed'],v['source'],*v['y'][21],*v['codes'],','.join(map(str,v['labels'])),v['upper_image']] for v in result['witnesses']])
    negative=make(['Fest_1','Fest_2','Fest_3','Matrixdimension','Norm_oben','Verschiedene_Quellen_im_Pruefgebiet'],
        [[*v['fixed'],30,v['upper_norm'],'AUSGESCHLOSSEN'] for v in result['triples']])
    return {'Paarregister.tsv':positive,'Dreierregister.tsv':negative}

if __name__=='__main__':
    ap=argparse.ArgumentParser()
    ap.add_argument('--ausgabe',action='store_true',help='Ergebnisdateien erzeugen')
    args=ap.parse_args()
    if not __debug__:raise RuntimeError('Python ohne -O erforderlich')
    r=run()
    files=tables(r)
    files['Ergebnisse.json']=json.dumps(r,sort_keys=True,indent=2)+'\n'
    for n,s in files.items():
        p=ROOT/n
        if args.ausgabe:p.write_text(s)
        else:assert p.read_text()==s
    print('63 Lösungen, 35 Dreiergruppen ausgeschlossen,',r['independent_secant_components'],'exakte Sekantenkontrollen.')
    print('Garantierter Anzeigeabstand bei gleichem hypothetischem Raster:',r['minimum_future_code_distance'])
