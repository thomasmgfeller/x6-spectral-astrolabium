"""Rebuild and verify the independent causal attachments at the three certified N22 references."""
import argparse
import csv
import io
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile

from klassen import S, catalog
from gegenprobe import audit
from serienkontrolle import replay

ROOT=Path(__file__).resolve().parent
PINS=['da6dbc733df51fc52780b13607a3111127bc6fc89447ece04f79bbfa49e75fe3',
      '786feda88a47ebab2a117e06bb0b8b8401f05ad311baa1e84d87d27cee5a4a7b',
      'bde2befb9dd6f306f596126976fcde4379a4449b351fcc6413c6929c555cf042',
      '7b1e8655d3706ab0980d7843d936912a4914473de7c52033c974d1b4ff261100']


def prepare(tmp):
    source=ROOT/'basis/Seriell.zip'
    directories=[]
    for label,child,pin in zip(('final','follower','branch','base'),
                               ('Nachfolger.zip','Vorstudie.zip','N22.zip',None),PINS):
        dst=tmp/label
        assert sha256(source.read_bytes()).hexdigest()==pin
        with ZipFile(source) as z:z.extractall(dst)
        directories.append(dst)
        if child:source=dst/'basis'/child
    final,follower,branch,base=directories
    sys.path[:0]=[str(follower),str(branch),str(base),str(final)]
    from randhulle import collect
    from ordnung22 import structure
    from staubuhren import enclose
    from zeugnis import certify
    cfg=collect(branch/'basis/N22.zip',256)
    collar=cfg['collar']
    left,right=F(31,64),F(33,64)
    a=(1-left)*collar[3][0]+left*collar[7][0]
    b=(1-right)*collar[3][1]+right*collar[7][1]
    window=(a//1,-(-b//1))
    old=json.loads((final/'Ergebnisse.json').read_text())
    assert old['remaining']==0 and list(window)==old['window_ticks']
    named=json.loads((base/'Zeugenzentren.json').read_text())
    seeds={216141:json.loads((final/'Zeugenzentrum_216141.json').read_text()),
           216427:named['Zeuge_Kontrolle'],217269:named['Zeuge_Rand_zz']}
    # Resolve the original order IDs independently from their four masks.
    import gzip
    with gzip.open(base/'Register.tsv.gz','rt') as fp:
        found={int(r['ID']):[int(r[s]) for s in ('P19','F19','P20','F20')]
               for r in csv.DictReader(fp,delimiter='\t') if int(r['ID']) in seeds}
    assert found=={k:v['row'] for k,v in seeds.items()}
    rows=catalog(set(map(tuple,cfg['order'])),seeds,collar,window,structure,enclose)
    kernel=(branch/'zweigtest.cpp').read_text()
    head,rest=kernel.split('void combined(')
    (tmp/'gleichungen.hpp').write_text(head)
    prefix=(final/'fenster.cpp').read_text().split('#include "suche.hpp"')[0]
    (tmp/'reduktion.hpp').write_text(prefix+'\nvoid combined('+rest.split('void search(')[0])
    exe=tmp/'test'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',
                    '-I',str(tmp),'-I',str(base),str(ROOT/'fenster.cpp'),'-o',str(exe)],check=True)
    return exe,rows,seeds,old,cfg,certify


def inputs(row, collar, witness=None):
    out=[]
    for j in range(22):
        y = row['span'] if j==21 else row['bounds'][j]
        if y is None:y=(0,0)
        w=collar[j][2:] if j in collar else ((0,0) if j in (15,17,20) or j==21 and row['weight']=='0' else (0,S))
        if witness and j not in collar:
            rad=F(1,10**7); val=F(witness['y'][j]);y=((val-rad)*S//1,-(-(val+rad)*S//1))
            if w!=(0,0):
                rad=F(1,10**8);val=F(witness['w'][j]);w=((val-rad)*S//1,-(-(val+rad)*S//1))
        out.append([*y,*w])
    return out


def invoke(exe,row,fields,small,cap,mode):
    raw=[str(len(row['edges'])),*(f'{a} {b}' for a,b in sorted(row['edges']))]
    raw.extend(' '.join(map(str,v)) for v in fields)
    run=subprocess.run([str(exe),row['family']+row['weight'],str(small),str(cap),mode],
                       input='\n'.join(raw)+'\n',capture_output=True,text=True)
    if run.returncode:raise RuntimeError(f"{row['id']} {small} {mode} {run.stderr}")
    return run.stdout


def compute(tmp,jobs,budget,profile):
    exe,rows,seeds,old,cfg,certify=prepare(tmp)
    collar=cfg['collar']
    checks=audit(rows,collar,exe,inputs,invoke)
    trees={}
    controls={}
    for cid,seed in seeds.items():
        row=next(v for v in rows if v['cid']==cid and v['distance']==0 and v['weight']=='+')
        cert=certify(cfg,seed)
        assert list(map(int,invoke(exe,row,inputs(row,collar,seed),0,1,'control').split()))==[1,0,1,0]
        assert cert['equations']==25
        assert any(cert['below_window'][j] or cert['above_window'][j] for j in (0,1))
        controls[cid]=cert['normalized_clocks']
    def solve(item):
        row,small,cap=item
        mode='moments' if row['method']=='projected_moments' else 'tree'
        val=invoke(exe,row,inputs(row,collar),small,cap,mode)
        n,c,o,d=map(int,val.split())
        assert n==2*(c+o)-1
        return row['id'],str(small),dict(nodes=n,closed=c,open=o,depth=d,budget=cap)
    todo=[]
    for r in rows:
        if r['span'] is None or r['span'][0]>r['span'][1]:
            continue
        for s in range(4):
            b=profile.get(r['id'],{}).get(str(s),budget)
            todo.append((r,s,b))
    # Solve the preselected single-relation neighbours first.
    todo.sort(key=lambda z:(z[0]['distance']!=1,z[0]['distance']!=0,z[0]['distance'],z[0]['id']))
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for k,s,res in pool.map(solve,todo):
            trees.setdefault(k,{})[s]=res
    serial_trees=replay(tmp,cfg,seeds,jobs)
    output=io.StringIO()
    writer=csv.writer(output,delimiter='\t',lineterminator='\n')
    writer.writerow(['Referenz','Lage','P21','F21','Abstand','Gewicht21','Uhrgrenze','Ergebnis','Nachweis','Offene_Gewichtsbereiche_im_Wiederholungslauf'])
    counts=Counter()
    for r in rows:
        if r['id'] not in trees:state='AUSGESCHLOSSEN';missing=0
        else:
            assert len(trees[r['id']])==4
            missing=sum(x['open']>0 for x in trees[r['id']].values())
            state='OFFEN' if missing else 'AUSGESCHLOSSEN'
        proof='Intervallbaum' if r['id'] in trees else 'Uhrgrenze'
        if missing and r['distance']==0 and r['weight']=='+' and str(r['cid']) in serial_trees:
            assert old['cases']==old['now_excluded']==1624568 and old['remaining']==0
            assert all(t['open']==0 for t in serial_trees[str(r['cid'])].values()) and r['weight']=='+'
            state='AUSGESCHLOSSEN'
            proof='Wiederholter serieller Pruefer'
        counts[state]+=1
        writer.writerow([r['cid'],r['family'],r['po'],r['fo'],r['distance'],r['weight'],r['method'],state,proof,missing])
    return dict(sectors=len(rows),serial_trees=serial_trees,audit=checks,counts=dict(counts),trees=trees,controls=controls,P3=old['P3']),output.getvalue()


def main():
    p=argparse.ArgumentParser()
    p.add_argument('--jobs',type=int,default=2)
    p.add_argument('--budget',type=int,default=128)
    p.add_argument('--ausgabe',type=Path)
    p.add_argument('--stufe',type=Path)
    args=p.parse_args()
    if not __debug__ or args.jobs<1 or args.budget<1:raise RuntimeError('Python ohne -O und positive Parameter erforderlich.')
    for tag in ('Pruefplan','Einseitige_Faelle'):
        assert sha256((ROOT/(tag+'.md')).read_bytes()).hexdigest()==(ROOT/(tag+'.sha256')).read_text().split()[0]
    reference=json.loads((ROOT/'Ergebnisse.json').read_text()) if not args.ausgabe else None
    stage=json.loads(args.stufe.read_text()) if args.stufe else reference
    profile={k:{s:(args.budget if args.stufe and t['open'] else t['budget']) for s,t in sec.items()}
             for k,sec in stage['trees'].items()} if stage else {}
    with TemporaryDirectory() as d:r,tsv=compute(Path(d),args.jobs,args.budget,profile)
    if args.ausgabe:
        args.ausgabe.mkdir(exist_ok=True,parents=True)
        (args.ausgabe/'Ergebnisse.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
        (args.ausgabe/'Fallregister.tsv').write_text(tsv)
    else:
        assert tsv==(ROOT/'Fallregister.tsv').read_text()
        got=json.loads(json.dumps(r))
        assert {k:v for k,v in got.items() if k not in ('trees','serial_trees')}=={k:v for k,v in reference.items() if k not in ('trees','serial_trees')}
        for name in ('trees','serial_trees'):
            assert r[name].keys()==reference[name].keys()
            for k,sec in r[name].items():
                assert sec.keys()==reference[name][k].keys()
                for s,t in sec.items():assert (t['open']==0)==(reference[name][k][s]['open']==0)
    print('Prüfergebnis',r['counts'],flush=True)

if __name__=='__main__':main()
