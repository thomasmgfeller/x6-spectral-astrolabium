"""Replay the common-future experiment from the pinned N22 input package."""
import argparse
import csv
import io
import json
import subprocess
import sys
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction
from hashlib import sha256
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
from zeugenkontrolle import verify as verify_witness
from empfangsordnungen import classify, relation, via_ideals, via_insertion

ROOT = Path(__file__).resolve().parent
ARCHIVE_SHA = '2bfad0955d5325337b5c902c31fc54d25596ba6a23ce42dc1067af6b4c587bf2'


def setup(tmp):
    parent = tmp/'empfangsbasis'
    archive = ROOT/'basis/Einzelanbindung.zip'
    assert sha256(archive.read_bytes()).hexdigest() == ARCHIVE_SHA
    with ZipFile(archive) as source:
        source.extractall(parent)
    sys.path.insert(0, str(parent))
    spec = spec_from_file_location('einzelanbindung_pruefung', parent/'pruefen.py')
    previous = module_from_spec(spec)
    spec.loader.exec_module(previous)
    exe, serial_rows, seeds, old, cfg, certify = previous.prepare(tmp)
    controls = {}
    for cid, seed in seeds.items():
        r = next(r for r in serial_rows if r['cid']==cid and r['distance']==0 and r['weight']=='+')
        cert = certify(cfg, seed)
        assert cert['equations']==25 and any(cert['below_window'][i] or cert['above_window'][i] for i in (0,1))
        assert previous.invoke(exe,r,previous.inputs(r,cfg['collar'],seed),0,1,'control').split()==['1','0','1','0']
        controls[cid] = cert['normalized_clocks']
    # Supply an explicit terminal contractor valid even if c(20,21) vanishes.
    # The old command-line B switch only adds 20<21, already in every input order.
    driver = (parent/'fenster.cpp').read_text()
    include = '#include "endmomente.hpp"'
    assert driver.count(include)==1
    (tmp/'empfang.cpp').write_text(driver.replace(include,'#include "enduhren.hpp"'))
    binary = tmp/'empfang'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=undefined','-fno-sanitize-recover=all',
                    '-I',str(ROOT),'-I',str(tmp),'-I',str(tmp/'base'),str(tmp/'empfang.cpp'),
                    '-o',str(binary)],check=True)
    return previous, binary, seeds, old, cfg, controls


def catalog(seeds, old, cfg):
    from anbindungen import coefficients, floyd
    from klassen import clock21, clock_ranges
    from ordnung22 import structure
    from staubuhren import enclose

    orders = []
    for cid, seed in seeds.items():
        serial, _ = structure(set(map(tuple,cfg['order'])), seed['row'], seed['case'][0])
        base = {(i,j) for i,j in serial if i<21 and j<21}
        pairs = via_ideals(base)
        assert pairs == via_insertion(base)
        for past, future in sorted(pairs):
            edges = relation(base, past, future)
            assert edges == floyd(edges) and all(i!=j for i,j in edges)
            assert (19,20) not in edges and (20,19) not in edges
            coeff = coefficients(edges)
            between = classify(edges)
            for j,n in zip((19,20),between):
                assert coeff.get((j,21),0) == ((1,-9,16,-8)[n] if n<4 else 0)
            bounds = clock_ranges(cfg['collar'],tuple(old['window_ticks']),edges,coeff,enclose)
            for weight in ('0','+'):
                method,span = clock21('B',weight=='+',past,future,edges,coeff,bounds)
                assert past and (not future or method=='order')
                orders.append(dict(id=f'{cid}/{past}/{future}/{weight}',cid=cid,po=past,fo=future,
                                   family='B',weight=weight,edges=edges,coeff=coeff,bounds=bounds,
                                   between=between,method=method,span=span))
    return orders


def run(tmp, jobs, budgets, default, width):
    previous, exe, seeds, old, cfg, controls = setup(tmp)
    from schranken import NORMALIZERS
    assert tuple(cfg['collar'][j][:2] for j in (3,7)) == NORMALIZERS
    if width != Fraction(1,64):
        low, high = Fraction(1,2)-width, Fraction(1,2)+width
        collar = cfg['collar']
        left = (1-low)*collar[3][0]+low*collar[7][0]
        right = (1-high)*collar[3][1]+high*collar[7][1]
        old = dict(old,window_ticks=[left//1,-(-right//1)])
    rows = catalog(seeds,old,cfg)
    from endpolynom import certify_terminal
    moments = certify_terminal(rows)
    witness = verify_witness(tmp,cfg,rows,seeds,previous,exe)
    # The old algebra verifier uses distance only for sample selection.
    # Check every encountered combination of reference, two layer counts, clock bound and weight.
    samples=set()
    for r in rows:
        key=(r['cid'],*r['between'],r['method'],r['weight'])
        r['distance']=int(key not in samples)
        samples.add(key)
    audit = previous.audit(rows,cfg['collar'],exe,previous.inputs,previous.invoke)
    enhanced=None
    extra_audit=None
    if width>=Fraction(27,1024):
        from terminaltest import compile_solver,check_derivatives
        from dichtevergleich import intersect_fields
        enhanced=compile_solver(tmp)
        witness_row=next(r for r in rows if r['id']==witness['case_id'])
        fields=previous.inputs(witness_row,cfg['collar'])
        snapshot=json.loads((ROOT/'Zeugenzentrum.json').read_text())
        control=previous.inputs(witness_row,cfg['collar'],snapshot)
        assert previous.invoke(enhanced,witness_row,control,0,1,'control').split()==['1','0','1','0']
        extra_audit=dict(linear_entries=check_derivatives(enhanced,witness_row,fields,previous),
                         regular_ticks=intersect_fields(witness_row,fields,0)[1])
    trees = {}
    jobs_to_run=[]
    for r in rows:
        if r['span'] is None or r['span'][0]>r['span'][1]:
            continue
        for s in range(4):
            cap=budgets.get(r['id'],{}).get(str(s),default)
            jobs_to_run.append((r,s,cap))
    def solve(item):
        r,s,cap=item
        mode='moments' if r['method']=='projected_moments' else 'tree'
        current=exe
        fields=previous.inputs(r,cfg['collar'])
        if enhanced is not None and r['id']==witness['case_id']:
            current=enhanced
            if s==0:
                from uhrteilung import cover
                return r['id'],str(s),cover(previous,current,r,fields,320)
            fields,_=intersect_fields(r,fields,s)
        raw=previous.invoke(current,r,fields,s,cap,mode)
        n,c,o,d=map(int,raw.split())
        assert n==2*(c+o)-1
        return r['id'],str(s),dict(nodes=n,closed=c,open=o,depth=d,budget=cap)
    with ThreadPoolExecutor(max_workers=jobs) as pool:
        for key,sector,result in pool.map(solve,jobs_to_run):
            trees.setdefault(key,{})[sector]=result

    buffer=io.StringIO()
    writer=csv.writer(buffer,delimiter='\t',lineterminator='\n')
    writer.writerow(('Referenz','P21','F21','Zwischen_19_21','Zwischen_20_21','Direkte_Verbindungen',
                     'Gewicht21','Uhrgrenze','Ergebnis','Offene_Gewichtsbereiche'))
    tally=Counter()
    for r in rows:
        branch=trees.get(r['id'])
        if branch:
            assert len(branch)==4
        missing=sum(x['open']>0 for x in branch.values()) if branch else 0
        status='OFFEN' if missing else 'AUSGESCHLOSSEN'
        tally[status]+=1
        writer.writerow((r['cid'],r['po'],r['fo'],*r['between'],r['between'].count(0),
                         r['weight'],r['method'],status,missing))
    output = dict(halfwidth=str(width),terminal_polynomial=moments,witness=witness,counts=dict(tally),controls=controls,trees=trees,checks=audit,P3=old['P3'],
                window_ticks=old['window_ticks'],case_count=len(rows))
    if extra_audit is not None:
        output['terminal_audit']=extra_audit
    return output, buffer.getvalue()


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--halbbreite',type=Fraction,default=Fraction(1,64))
    parser.add_argument('--jobs',type=int,default=4)
    parser.add_argument('--budget',type=int,default=128)
    parser.add_argument('--vorlauf',type=Path)
    parser.add_argument('--ausgabe',type=Path)
    args=parser.parse_args()
    if not __debug__ or args.jobs<1 or args.budget<1:
        raise ValueError('Python ohne -O und positive Parameter erforderlich.')
    assert sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest()==(ROOT/'Pruefplan.sha256').read_text().split()[0]
    allowed = [Fraction(1,64),Fraction(3,128),Fraction(13,512),Fraction(27,1024),Fraction(55,2048)]
    if args.halbbreite not in allowed: raise ValueError('Ungeplante Halbbreite')
    for line in (ROOT/'Fenstervergleich.sha256').read_text().splitlines():
        pin,name=line.split()
        assert sha256((ROOT/name).read_bytes()).hexdigest()==pin
    dest=ROOT if args.halbbreite==allowed[0] else ROOT/'Fenstervergleich'/str(args.halbbreite).replace('/','_')
    reference = None
    if not args.ausgabe:
        reference = json.loads((dest/'Ergebnisse.json').read_text())
    stage = json.loads(args.vorlauf.read_text()) if args.vorlauf else reference
    budgets = {k:{s:(args.budget if args.vorlauf and t['open'] else t['budget']) for s,t in ss.items()}
               for k,ss in stage['trees'].items()} if stage else {}
    with TemporaryDirectory() as folder:
        result, table = run(Path(folder),args.jobs,budgets,args.budget,args.halbbreite)
    if args.ausgabe:
        args.ausgabe.mkdir(parents=True,exist_ok=True)
        (args.ausgabe/'Ergebnisse.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
        (args.ausgabe/'Fallregister.tsv').write_text(table)
    else:
        assert table==(dest/'Fallregister.tsv').read_text()
        got=json.loads(json.dumps(result))
        assert {k:v for k,v in got.items() if k!='trees'} == {k:v for k,v in reference.items() if k!='trees'}
        assert got['trees'].keys()==reference['trees'].keys()
        if got['counts'].get('OFFEN') and args.halbbreite>=Fraction(27,1024):
            from schranken import first_possible_y19
            assert first_possible_y19(got)>=first_possible_y19(reference)
        for k,ss in got['trees'].items():
            assert ss.keys()==reference['trees'][k].keys()
            for s,t in ss.items():
                assert (t['open']==0)==(reference['trees'][k][s]['open']==0)
    print(result['counts'],flush=True)

if __name__=='__main__':
    main()
