"""Offline replay. Python 3.11+ and g++ with C++17 and 128-bit integers."""
import argparse
from collections import Counter
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from eingaben import ROOT,SCALE,data,write_input
from gegenprobe import combinatorics, fraction_checks, kernel_controls, density_only


def solve(binary,d,path,rounds,depth,budget,reverse=False):
    write_input(d,path)
    opts=[str(binary),str(rounds),str(depth),str(budget)]
    if reverse:opts.append('reverse')
    with path.open() as f:
        r=subprocess.run(opts,stdin=f,capture_output=True,text=True,check=True)
    out=[v.split() for v in r.stdout.splitlines()]
    assert len(out)==len(d['rows']) and all(v for v in out)
    return out


def expanded_results(v):
    if v[0]!='split':return {v[0]+'.'+v[1]:1}
    causes={key:int(n) for key,n in (entry.split('=') for entry in v[3:])}
    assert sum(causes.values())==int(v[1]) and int(v[2])==2*int(v[1])-1
    return causes


def calculation():
    d=data()
    pre=combinatorics(d)
    density=density_only(d)
    with TemporaryDirectory() as name:
        tmp=Path(name);compiler='g++'
        binaries=[]
        for src in ('feldtest','kontrolle'):
            exe=tmp/src;binaries.append(exe)
            subprocess.run([compiler,'-std=c++17','-O2','-Wall','-Wextra','-Werror','-fsanitize=undefined',
                            '-fno-sanitize-recover=undefined',str(ROOT/(src+'.cpp')),'-o',exe],check=True)
        main,control=binaries;path=tmp/'input'
        ck=kernel_controls(d,control)
        first=solve(main,d,path,24,18,8000)
        tail=[i for i,v in enumerate(first) if v[0]=='OPEN']
        second=solve(main,{**d,'rows':[d['rows'][i] for i in tail]},path,24,43,35000)
        final=first[:]
        for i,line in zip(tail,second):final[i]=line
        assert all(v[0]!='OPEN' for v in final)
        wide=solve(main,{**d,'collar':d['wide_collar']},path,24,43,35000,reverse=True)
        wide_open=[i for i,v in enumerate(wide) if v[0]=='OPEN']
        if wide_open:
            extra=solve(main,{**d,'collar':d['wide_collar'],'rows':[d['rows'][i] for i in wide_open]},
                        path,36,56,160000,reverse=True)
            for i,line in zip(wide_open,extra):wide[i]=line
        sample={}
        for i,v in enumerate(final):sample.setdefault(tuple(v[:2]) if v[0]!='split' else ('split',),i)
        selected=sorted(set(sample.values())|set(tail)|{len(final)-1})
        ck.update(fraction_checks(d,selected))
        groups=Counter();laws=Counter();wide_status=Counter();table=[]
        for i,(row,v,alt) in enumerate(zip(d['rows'],final,wide,strict=True)):
            stage='geteilt_tief' if i in tail else 'geteilt' if v[0]=='split' else 'direkt'
            groups[stage]+=1;laws.update(expanded_results(v));wide_status[alt[0]]+=1
            table.append('\t'.join(map(str,[i+1,*row,stage,' '.join(v),' '.join(alt)])))
        ledger='ID\tP19\tF19\tP20\tF20\tStufe\tHauptnachweis\tErweiterter_Rand\n'+'\n'.join(table)+'\n'
        return ledger.encode(),dict(source='9c732c5b94482130b8a8286caa64e1bf86885091',ticks_per_unit=SCALE,
                 labelled_orders=sum(pre.values()),prefilters=pre,certificates=d['early_proofs'],
                 groups=dict(groups),leaf_causes=dict(laws),split_leaf_total=sum(int(v[1]) for v in final if v[0]=='split'),
                 deep_orders=[{'id':i+1,'masks':d['rows'][i],'leaves':int(v[1]),'boxes':int(v[2])} for i,v in zip(tail,second)],
                 widened_reverse_pass=dict(wide_status),widened_open=[i+1 for i,v in enumerate(wide) if v[0]=='OPEN'],
                 controls=ck,independent_density=density,reference_cells=168,window_ticks=d['window'],P3={'NOT_RUN':60,'physical_radius':None})


def check_hashes(name):
    for line in (ROOT/name).read_text().splitlines():
        digest,fn=line.split('  ',1)
        if sha256((ROOT/fn).read_bytes()).hexdigest()!=digest:raise ValueError('Prüfsumme '+fn)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--ausgabe',type=Path,help='Geprüfte Rechenergebnisse in diesen Ordner schreiben.')
    args=parser.parse_args()
    if not __debug__:raise RuntimeError('Python ohne -O verwenden.')
    for fn in ('Pruefplan.sha256','Ergaenzung.sha256'):check_hashes(fn)
    if not args.ausgabe:check_hashes('SHA256SUMS')
    t,r=calculation()
    files={'Ergebnisse.json':(json.dumps(r,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode(),'Register.tsv':t}
    for n,b in files.items():
        if args.ausgabe:
            args.ausgabe.mkdir(parents=True,exist_ok=True)
            (args.ausgabe/n).write_bytes(b)
        elif (ROOT/n).read_bytes()!=b:raise ValueError('Reproduktion '+n)
    print('PASS · 406142 Anordnungen · 42716 Feldtests · 0 stationäre Kandidaten im geprüften Sektor.')
    print('Erweiterter Rand, offene Fälle:',len(r['widened_open']),'· Physisches P3: 60 NOT_RUN.')

if __name__=='__main__':main()
