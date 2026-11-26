"""Rebuild the complete targeted test and the graph-selected supplementary register."""
from concurrent.futures import ThreadPoolExecutor
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
from pathlib import Path
from tempfile import TemporaryDirectory
from zipfile import ZipFile
import argparse,csv,json,subprocess,sys
from randhulle import collect
from wirkungstest import check as action_check

ROOT=Path(__file__).resolve().parent
PIN='7b1e8655d3706ab0980d7843d936912a4914473de7c52033c974d1b4ff261100'
CLOCKS=tuple(range(15,22))
WEIGHTS=(16,18,19,21)
PRIMARY={216427,217269}
TICKS=10**9

def serialize(val):return json.dumps(val,indent=2,ensure_ascii=False,sort_keys=True)+'\n'

def input_text(bounds,row,control=None):
    # Dust bounds are unused by the reduced system; the reference frame is exact.
    order=bounds['order'];lines=[str(len(order)),*['%d %d'%tuple(e) for e in order]]
    lines.extend(' '.join(map(str,(k,*v))) for k,v in bounds['collar'].items())
    lines.extend('%d 0 0'%k for k in (4,5,6,11,12,13,14))
    a,b=F(31,64),F(33,64)
    y3,y7=bounds['collar'][3],bounds['collar'][7]
    left=(1-a)*y3[0]+a*y7[0];right=(1-b)*y3[1]+b*y7[1]
    window=(left//1,-(-right//1))
    assert window==(23437499,143229167)
    lines.extend(('%d %d'%window,'1',' '.join(map(str,row))))
    if control is not None:
        for key,ids,radius in [('y',CLOCKS,F(1,10**7)),('w',WEIGHTS,F(1,10**8))]:
            for j in ids:
                x=F(control[key][j])
                lines.append('%d %d'%((x-radius)*TICKS//1,-(-(x+radius)*TICKS//1)))
    return '\n'.join(lines)+'\n'

def compute(tmp,workers):
    archive=ROOT/'basis/N22.zip';assert sha256(archive.read_bytes()).hexdigest()==PIN
    for name in ['Pruefplan','Ergaenzung']:
        assert sha256((ROOT/(name+'.md')).read_bytes()).hexdigest()==(ROOT/(name+'.sha256')).read_text().split()[0]
    parent=tmp/'n22'
    with ZipFile(archive) as z:z.extractall(parent)
    sys.path.insert(0,str(parent))
    from ordnung22 import structure
    from zeugnis import certify
    cfg=collect(archive,256);order=set(map(tuple,cfg['order']))
    table=(parent/'Offene_Faelle.tsv').read_text().splitlines()
    rows=list(csv.DictReader(table,delimiter='\t'));assert len(rows)==73
    eligible={};separate={}
    for v in rows:
        if v['Sektor']!='B+':continue
        case=int(v['ID']);row=tuple(int(v[n]) for n in ('P19','F19','P20','F20'))
        rel,c=structure(order,row,'B')
        dust={4,5,6,11,12,13,14}
        coupled=any((a in dust and b in CLOCKS) or (b in dust and a in CLOCKS) for a,b in c)
        if not coupled:
            missing=[(i,k) for j in CLOCKS for i,k in [(0,j),(j,7)] if (i,k) not in rel]
            separate[case]=missing
            if not missing:eligible[case]=row
    assert len(eligible)==12 and PRIMARY<=eligible.keys()
    binary=tmp/'test'
    subprocess.run(['g++','-std=c++17','-O2','-fsanitize=signed-integer-overflow','-fno-sanitize-recover=all',
                    '-I',str(parent),str(ROOT/'zweigtest.cpp'),'-o',str(binary)],check=True)
    action_entries=0
    for case,row in eligible.items():
        _,coefficients=structure(order,row,'B')
        action_entries+=action_check(binary,input_text(cfg,row),coefficients,cfg['collar'])
    def run(binary,case,sector,budget,depth,control=None):
        args=[str(binary),str(depth),str(budget),str(sector)]
        if control is not None:args.append('control')
        proc=subprocess.run(args,input=input_text(cfg,eligible[case],control),text=True,capture_output=True,check=True)
        mask,sec,nodes,closed,opened,deep=map(int,proc.stdout.split())
        assert mask==eligible[case][1] and sec==sector and nodes==2*(closed+opened)-1
        return dict(nodes=nodes,closed=closed,open=opened,depth=deep)
    def sector_run(item):
        case,sector=item
        return case,sector,run(binary,case,sector,3000000 if case in PRIMARY else 100000,76)
    results={k:{} for k in eligible}
    with ThreadPoolExecutor(max_workers=workers) as pool:
        for case,sector,out in pool.map(sector_run,[(k,s) for k in eligible for s in range(4)]):
            results[case][sector]=out
    witness=json.loads((parent/'Zeugenzentren.json').read_text())
    controls={}
    for case,name in [(216427,'Zeuge_Kontrolle'),(217269,'Zeuge_Rand_zz')]:
        v=witness[name];assert tuple(v['row'])==eligible[case]
        cert=certify({'order':list(order)},v)
        assert not any(cert['inside_window'][:2])
        trial=run(binary,case,0,1,0,v);assert trial['open']==1
        controls[case]={k:cert[k] for k in ('normalized_clocks','upper_sum','equations','strict_relations')}
    removed=sorted(k for k in eligible if all(v['open']==0 for v in results[k].values()))
    next_group={k:v for k,v in separate.items() if k not in removed}
    old=json.loads((parent/'Ergebnisse.json').read_text())
    counted=sum(v['open'] for v in old['sectors'].values());assert counted==len(rows)
    keep=[v for v in rows if v['Sektor']!='B+' or int(v['ID']) not in removed]
    buf=StringIO();writer=csv.DictWriter(buf,fieldnames=list(rows[0]),delimiter='\t',lineterminator='\n')
    writer.writeheader();writer.writerows(keep)
    assert len(keep)==len(rows)-len(removed)
    res=dict(next_decoupled_B_plus=next_group,primary=sorted(PRIMARY),eligible=sorted(eligible),excluded=removed,remaining=len(keep),
             cases=old['cases'],now_excluded=old['cases']-len(keep),positive_follower_remaining=old['sectors']['B+']['open']-len(removed),
             P3=old['P3'],action_entries=action_entries,partitions=cfg['pieces'],sources=cfg['sources'],collar=cfg['collar'],controls=controls,trees=results)
    return res,buf.getvalue()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--ausgabe',type=Path);parser.add_argument('--jobs',type=int,default=2);args=parser.parse_args()
    assert 1<=args.jobs<=16
    with TemporaryDirectory() as td:res,reg=compute(Path(td),args.jobs)
    outputs={'Ergebnisse.json':serialize(res),'Offene_Faelle.tsv':reg}
    if args.ausgabe:
        for name,val in outputs.items():(args.ausgabe/name).write_text(val)
    else:
        ref=json.loads((ROOT/'Ergebnisse.json').read_bytes())
        actual=json.loads(serialize(res))
        # Different admissible pivot choices may produce differently sized covering trees.
        assert {k:v for k,v in actual.items() if k!='trees'}=={k:v for k,v in ref.items() if k!='trees'}
        assert all((v['open']==0)==(ref['trees'][case][s]['open']==0) for case,c in actual['trees'].items() for s,v in c.items())
        assert (ROOT/'Offene_Faelle.tsv').read_text()==reg
    print('Ausgeschlossen:',res['excluded'],'; offene N22-Fälle:',res['remaining'],flush=True)
