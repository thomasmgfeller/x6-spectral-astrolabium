"""Window exclusions on the same three N21 projections with the revised collar enclosure."""
import csv
import io
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from hashlib import sha256
from importlib.util import spec_from_file_location,module_from_spec
from pathlib import Path
from zipfile import ZipFile

ROOT=Path(__file__).resolve().parent
PIN='befab2c92a744c2f45ee584baada581a309f449466d6f8059c889173c1d50dd9'
KEY='216141/229383/0/+'
H1,H2=F(27,1024),F(55,2048)


def module(name,path):
    spec=spec_from_file_location(name,path)
    obj=module_from_spec(spec)
    spec.loader.exec_module(obj)
    return obj


def setup(tmp,partitions):
    archive=ROOT/'basis/Gemeinsamer_Nachfolger.zip'
    assert sha256(archive.read_bytes()).hexdigest()==PIN
    parent=tmp/'nachfolger'
    with ZipFile(archive) as z:z.extractall(parent)
    sys.path.insert(0,str(parent))
    study=module('publizierter_empfang',parent/'pruefen.py')
    prev,exe,seeds,old,cfg,controls=study.setup(tmp)
    from terminaltest import compile_solver
    special=compile_solver(tmp)
    out=tmp/'rand.json'
    subprocess.run([sys.executable,'-B',str(ROOT/'praeparieren.py'),str(tmp/'base/basis/N21.zip'),
                    str(partitions),str(out)],check=True)
    prepared=json.loads(out.read_text())
    collar={int(k):v for k,v in prepared['collar'].items()}
    original=cfg['collar']
    for j,z in collar.items():
        a=original[j]
        for k in (0,2):
            assert a[k]<=z[k]<=z[k+1]<=a[k+1]
    return study,prev,exe,special,seeds,old,dict(cfg,collar=collar),prepared,original


def window(collar,h):
    l,r=F(1,2)-h,F(1,2)+h
    y3,y7=collar[3],collar[7]
    return [((1-l)*y3[0]+l*y7[0])//1,-(-((1-r)*y3[1]+r*y7[1])//1)]


def run_cut(prev,exe,r,initial,lo,hi,sec,cap):
    from dichtevergleich import intersect_fields
    fields=[a.copy() for a in initial]
    fields[19][:2]=[lo,hi]
    fields,_=intersect_fields(r,fields,sec)
    n,c,o,d=map(int,prev.invoke(exe,r,fields,sec,cap,'tree').split())
    assert n==2*(c+o)-1
    return dict(ticks=[lo,hi],closed=c,open=o,nodes=n,depth=d,budget=cap)


def primary(parent,prev,special,rows,cfg,jobs,cap):
    register=list(csv.DictReader((parent/'Fenstervergleich/27_1024/Fallregister.tsv').open(),delimiter='\t'))
    data=json.loads((parent/'Fenstervergleich/27_1024/Ergebnisse.json').read_text())
    assert len(rows)==len(register)==1342
    for r,z in zip(rows,register,strict=True):
        assert r['id']=='/'.join(z[k] for k in ('Referenz','P21','F21','Gewicht21'))
        assert (z['Ergebnis']=='OFFEN')==(r['id']==KEY)
    assert data['counts']=={'AUSGESCHLOSSEN':1341,'OFFEN':1}
    live=[(k,s) for k,sectors in data['trees'].items() for s,t in sectors.items() if t['open']]
    assert live==[(KEY,'0')]
    slabs=data['trees'][KEY]['0']['slabs']
    assert slabs[0]['ticks'][0]==data['window_ticks'][0] and slabs[-1]['ticks'][1]==data['window_ticks'][1]
    assert all(a['ticks'][1]==b['ticks'][0] for a,b in zip(slabs,slabs[1:]))
    inherited=[s['ticks'] for s in slabs if s['open']]
    lo=min(s[0] for s in inherited);hi=max(s[1] for s in inherited)
    row=next(r for r in rows if r['id']==KEY)
    fields=prev.inputs(row,cfg['collar'])
    count=16
    cut=[lo+(hi-lo)*i//count for i in range(count+1)]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        leaves=list(pool.map(lambda i:run_cut(prev,special,row,fields,cut[i],cut[i+1],0,cap),range(count)))
    assert leaves[0]['ticks'][0]==lo and leaves[-1]['ticks'][1]==hi
    assert all(a['ticks'][1]==b['ticks'][0] for a,b in zip(leaves,leaves[1:]))
    return dict(previous_case_count=len(register),previously_excluded=1341,inherited_open_slabs=len(inherited),
                target=KEY,sector=0,slabs=leaves,excluded=all(v['open']==0 for v in leaves))


def secondary(study,prev,exe,special,rows,cfg,parent,jobs):
    record=json.loads((parent/'Fenstervergleich/27_1024/Ergebnisse.json').read_text())
    # Budgets from the smaller window only choose effort. All wider-window boxes are rebuilt.
    audit_samples=set()
    for row in rows:
        key=(row['cid'],*row['between'],row['method'],row['weight'])
        row['distance']=int(key not in audit_samples)
        audit_samples.add(key)
    audit=prev.audit(rows,cfg['collar'],exe,prev.inputs,prev.invoke)
    need=[]
    for r in rows:
        if r['span'] is None or r['span'][0]>r['span'][1]:
            continue
        for sector in range(4):
            if r['id']==KEY and sector==0:continue
            budget=record['trees'].get(r['id'],{}).get(str(sector),{}).get('budget',512)
            need.append((r,sector,max(512,budget)))
    def test(item):
        r,sector,cap=item
        fields=prev.inputs(r,cfg['collar'])
        binary=exe
        mode='moments' if r['method']=='projected_moments' else 'tree'
        if r['id']==KEY:
            from dichtevergleich import intersect_fields
            binary=special
            fields,_=intersect_fields(r,fields,sector)
        for cap in dict.fromkeys([cap,max(60000,cap)]):
            n,c,o,d=map(int,prev.invoke(binary,r,fields,sector,cap,mode).split())
            assert n==2*(c+o)-1
            if o==0:break
        return r['id'],str(sector),dict(nodes=n,closed=c,open=o,depth=d,budget=cap)
    trees={}
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for k,s,v in pool.map(test,need):trees.setdefault(k,{})[s]=v
    row=next(r for r in rows if r['id']==KEY)
    initial=prev.inputs(row,cfg['collar'])
    lo,hi=initial[19][:2]
    count=96
    ticks=[lo+(hi-lo)*i//count for i in range(count+1)]
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        cuts=list(pool.map(lambda i:run_cut(prev,special,row,initial,ticks[i],ticks[i+1],0,800),range(count)))
    return trees,audit,cuts


def header_and_rows(tmp,parts=16):
    study,prev,exe,special,seeds,old,cfg,prep,orig=setup(tmp,parts)
    rows1=study.catalog(seeds,dict(old,window_ticks=window(cfg['collar'],H1)),cfg)
    rows2=study.catalog(seeds,dict(old,window_ticks=window(cfg['collar'],H2)),cfg)
    assert [r['id'] for r in rows1]==[r['id'] for r in rows2]
    return (study,prev,exe,special,seeds,old,cfg,prep,orig),rows1,rows2


def witnesses(tmp,study,prev,exe,special,seeds,cfg,rows,prepared):
    from terminaltest import check_derivatives
    r=next(r for r in rows if r['id']==KEY)
    primary_control=study.verify_witness(tmp,cfg,rows,seeds,prev,exe)
    data=json.loads((ROOT/'Randzeuge.json').read_text())
    assert data['case']=='B+' and data['cid']==r['cid'] and data['past']==r['po'] and data['future']==r['fo']
    assert data['row']==seeds[r['cid']]['row'] and F(data['drift'])==-F(1,10**6) and F(data['source'])==F(1,10**6)
    checker=module('randzeugnis',tmp/'base/empfangszeugnis.py')
    edge=checker.certify(cfg,data,r['edges'],r['coeff'])
    assert edge['equations']==25 and edge['strict_relations']==len(r['edges'])==152 and edge['positive_weights']==11
    assert F(edge['upper_sum'])<1 and F(edge['normalized_clocks'][0][1])<F(primary_control['normalized_clocks'][0][0])
    groups=[x for x in prepared['cells'] if x['drift'][0]==data['drift'] and x['source']==data['source']]
    assert len(groups)==1
    for j,v in edge['collar'].items():
        for offset,ab in enumerate(v):
            l,h=groups[0]['collar'][j][2*offset:2*offset+2]
            assert l<=F(ab[0])*10**9<=F(ab[1])*10**9<=h
    assert prev.invoke(special,r,prev.inputs(r,cfg['collar'],data),0,1,'control').split()==['1','0','1','0']
    check=check_derivatives(special,r,prev.inputs(r,cfg['collar']),prev)
    def required(p):
        return max(abs(F(x)-F(1,2)) for bounds in p['normalized_clocks'][:2] for x in bounds)
    return dict(central=primary_control,endpoint=edge,tighter_upper_bound=str(required(edge)),
                central_upper_bound=str(required(primary_control)),linear_checks=check)


def fine_cover(tmp,prev,special,rows,cfg,coarse,cuts,jobs):
    path=tmp/'fein.json'
    subprocess.run([sys.executable,'-B',str(ROOT/'praeparieren.py'),str(tmp/'base/basis/N21.zip'),
                    '256',str(path)],check=True)
    finer=json.loads(path.read_text())
    fine={int(k):v for k,v in finer['collar'].items()}
    # Each fine preparation cell has the same source as its enclosing coarse cell.
    assert finer['partitions']==16*coarse['partitions']
    index={(r['source'],F(r['drift'][0])):r for r in coarse['cells']}
    left0=F(-1,10**6)
    step=-2*left0/coarse['partitions']
    for item in finer['cells']:
        a,b=map(F,item['drift'])
        group=index[item['source'],left0+((a-left0)//step)*step]
        assert F(group['drift'][0])<=a<b<=F(group['drift'][1])
    row=next(r for r in rows if r['id']==KEY)
    fields=prev.inputs(row,cfg['collar'])
    for j,b in fine.items():
        c=fields[j]
        assert all(c[i]<=b[i]<=b[i+1]<=c[i+1] for i in (0,2))
        fields[j]=b.copy()
    # Non-collar fields retain their valid coarse enclosures (including the terminal clock).
    fine_slabs=[]
    for block in cuts:
        if block['open']==0:continue
        lo,hi=block['ticks']
        ticks=[lo+(hi-lo)*n//32 for n in range(33)]
        with ThreadPoolExecutor(max_workers=jobs) as pool:
            pieces=list(pool.map(lambda i:run_cut(prev,special,row,fields,ticks[i],ticks[i+1],0,1200),
                                 range(32)))
        assert pieces[0]['ticks'][0]==lo and pieces[-1]['ticks'][1]==hi
        assert all(l['ticks'][1]==r['ticks'][0] for l,r in zip(pieces,pieces[1:]))
        fine_slabs.append(dict(parent=block['ticks'],pieces=pieces))
    return finer,fine_slabs


def assemble(rows,trees,cuts,fine):
    header=('Referenz','P21','F21','Zwischen_19_21','Zwischen_20_21','Gewicht21','Methode',
            'Ergebnis','Endbaeume','Geschlossene_Blaetter','Offene_Blaetter')
    buf=io.StringIO()
    writer=csv.writer(buf,delimiter='\t',lineterminator='\n')
    writer.writerow(header)
    assert all(a['ticks'][1]==b['ticks'][0] for a,b in zip(cuts,cuts[1:]))
    details={tuple(x['parent']):x['pieces'] for x in fine}
    assert set(details)=={tuple(x['ticks']) for x in cuts if x['open']}
    live_slabs=[p for c in cuts for p in details.get(tuple(c['ticks']),[c])]
    control=next(r for r in rows if r['id']==KEY)
    window=control['bounds'][19]
    assert live_slabs[0]['ticks'][0]==window[0] and live_slabs[-1]['ticks'][1]==window[1]
    assert all(a['ticks'][1]==b['ticks'][0] for a,b in zip(live_slabs,live_slabs[1:]))
    total=dict(cases=0,excluded=0,open=0,trees=0,closed_leaves=0,open_leaves=0,initial_exclusions=0)
    for r in rows:
        sub=trees.get(r['id'],{})
        if r['id']==KEY:
            assert set(sub)=={'1','2','3'}
            term=list(sub.values())+live_slabs
        elif r['span'] is None or r['span'][0]>r['span'][1]:
            assert not sub
            term=[]
            total['initial_exclusions']+=1
        else:
            assert set(sub)=={'0','1','2','3'}
            term=list(sub.values())
        closed=sum(t['closed'] for t in term)
        opened=sum(t['open'] for t in term)
        total['cases']+=1
        total['open']+=int(opened>0)
        total['excluded']+=int(opened==0)
        total['trees']+=len(term)
        total['closed_leaves']+=closed
        total['open_leaves']+=opened
        status='OFFEN' if opened else 'AUSGESCHLOSSEN'
        writer.writerow((r['cid'],r['po'],r['fo'],*r['between'],r['weight'],r['method'],status,
                         len(term),closed,opened))
    return total,buf.getvalue()
