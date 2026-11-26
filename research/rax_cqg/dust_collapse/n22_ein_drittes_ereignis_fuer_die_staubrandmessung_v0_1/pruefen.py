"""Offline verification of the two N22 serial attachments. See README.md."""
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from pathlib import Path
from tempfile import TemporaryDirectory
from io import BytesIO
import argparse,gzip,json,subprocess,sys
from seriendaten import ROOT,source,projections,prefilter,write_input
from kontrollen22 import reconstruct,variations,example,binary_control
from zeugnis import certify

KEYS=('A0','A+','B0','B+')
STEPS=('direct','part','deep','joint')
OPTIONS={
    'direct':(0,0,0), 'part':(12,300,0), 'deep':(36,12000,1),
    'joint':(36,4000,0),'reg':(34,5000,0)
}


def compile_tests(tmp):
    for phase,flags in [('normal',[]),('joint',['-DN22_JOINT']),('reg',['-DN22_BOUNDED_LOAD'])]:
        subprocess.run(['g++','-std=c++17','-O3','-Wall','-Wextra','-Werror','-fsanitize=undefined',
                        '-fno-sanitize-recover=undefined',*flags,str(ROOT/'feldtest.cpp'),'-o',tmp/phase],check=True)


def classifications(key,d,rows,tmp,cache=None):
    status=[prefilter(row,key[0]) for row in rows]
    pool=[i for i,v in enumerate(status) if not v]
    phases={};seeds=[];supp={};details=[];sample=set()
    for phase in (*STEPS,'reg'):
        if phase=='joint':seeds=list(pool)
        if phase=='reg':pool=seeds
        if not pool:phases[phase]={'input':0,'excluded':0,'open':0};continue
        opts=OPTIONS[phase] if phase!='deep' or key!='B+' else (24,1700,1)
        if cache:
            out=(cache/(key.replace('+','p')+'.'+phase)).read_text().splitlines()
        else:
            inp=tmp/(key+'.dat')
            write_input(d,[rows[i] for i in pool],inp)
            name=phase if phase in ('reg','joint') else 'normal'
            with inp.open() as f:
                p=subprocess.run([tmp/name,key[0],key[1],*map(str,opts)],stdin=f,capture_output=True,text=True,check=True)
            out=p.stdout.splitlines()
        assert len(out)==len(pool)
        pending=[]
        for i,v in zip(pool,out):
            bits=v.split()
            if bits[0]=='split':
                assert int(bits[2])==2*int(bits[1])-1
                assert sum(int(x.split('=')[1]) for x in bits[3:])==int(bits[1])
            if bits[0]=='OPEN':pending.append(i)
            if phase=='reg':
                supp[i]='OPEN' if bits[0]=='OPEN' else 'EXCLUDED'
            else:
                status[i]=phase+'/'+('OPEN' if bits[0]=='OPEN' else ':'.join(bits[:2]))
            if phase!='direct' and (phase!='part' or bits[0]!='OPEN'):
                details.append(f'{key}\t{i+1}\t{phase}\t{v}')
        phases[phase]={'input':len(pool),'excluded':len(pool)-len(pending),'open':len(pending)}
        if pool:sample.update((pool[0],pool[len(pool)//2],pool[-1]))
        pool=pending
    unresolved=[i for i,s in enumerate(status) if s.endswith('/OPEN')]
    assert all(i in supp for i in unresolved)
    counts=Counter(status)
    return dict(status=status,phases=phases,details=details,sample=sample,
                open=unresolved,supp=supp,early={s:counts[s] for s in ('T','G20','D19') if counts[s]})


def compute(cache=None):
    with source() as (d,archived),TemporaryDirectory() as td:
        tmp=Path(td);rows=projections(d['order']);ct=reconstruct(d,rows)
        assert (ROOT/'intervall.hpp').read_bytes()==(archived/'intervall.hpp').read_bytes()
        common=[row for row in rows if not prefilter(row,'A') and not prefilter(row,'B')]
        assert common==d['rows']
        if not cache:compile_tests(tmp)
        with ThreadPoolExecutor(max_workers=2) as ex:
            fut={k:ex.submit(classifications,k,d,rows,tmp,cache) for k in KEYS}
            out={k:fut[k].result() for k in KEYS}
        samples=[(k,rows[i]) for k in KEYS for i in sorted(out[k]['sample'])]
        count=variations(d,samples)
        centers=json.loads((ROOT/'Zeugenzentren.json').read_bytes())
        proofs={name:certify(d,seed) for name,seed in centers.items()}
        count.update(binary_control(d,samples,centers,proofs,tmp))
        src=BytesIO()
        with gzip.GzipFile(filename='',fileobj=src,mode='wb',mtime=0,compresslevel=6) as f:
            f.write(b'ID\tP19\tF19\tP20\tF20\tA0\tA+\tB0\tB+\n')
            for i,row in enumerate(rows):
                f.write(('\t'.join(map(str,[i+1,*row,*(out[k]['status'][i] for k in KEYS)]))+'\n').encode())
        detail='Sektor\tID\tStufe\tNachweis\n'+'\n'.join(v for k in KEYS for v in out[k]['details'])+'\n'
        open_rows='Sektor\tID\tP19\tF19\tP20\tF20\tNullimpuls_oder_beide_Gewichte_ab_1e-8\n'
        for k in KEYS:
            for i in out[k]['open']:
                open_rows+='\t'.join(map(str,[k,i+1,*rows[i],out[k]['supp'][i]]))+'\n'
        results={'source_commit':'95ca8505f8b679f1ae484fb8ea08b5f97fc4ba6c','projections':ct,
                 'orders':2*ct,'cases':4*ct,'sectors':{},'control':count,'analytic_example':example(d,rows),
                 'witnesses':proofs,'reference_cells':168,'P3':{'NOT_RUN':60,'radius':None}}
        for k in KEYS:
            st=out[k];n=len(st['open']);rigid=sum(st['supp'][i]=='EXCLUDED' for i in st['open'])
            results['sectors'][k]={'prefilters':st['early'],'stages':st['phases'],'excluded':ct-n,
                                   'open':n,'open_also_in_bounded_load_screen':n-rigid,
                                   'open_requiring_nonzero_impulse_and_a_small_weight':rigid}
        return {'Register.tsv.gz':src.getvalue(),'Teilungen.tsv.gz':gzip.compress(detail.encode(),compresslevel=6,mtime=0),
                'Offene_Faelle.tsv':open_rows.encode(),'Ergebnisse.json':(json.dumps(results,indent=2,sort_keys=True)+'\n').encode()}


def hashes(name):
    for line in (ROOT/name).read_text().splitlines():
        h,p=line.split('  ',1)
        if sha256((ROOT/p).read_bytes()).hexdigest()!=h:raise ValueError(p)


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--ausgabe',type=Path,help='Ergebnisse in diesen Ordner kopieren.')
    opt=ap.parse_args()
    if not __debug__:raise RuntimeError('Python ohne -O verwenden.')
    for n in ('Pruefplan','Ergaenzung','Ergaenzung_Gewichte','Ergaenzung_Randfortsetzung'):hashes(n+'.sha256')
    if not opt.ausgabe:hashes('SHA256SUMS')
    files=compute()
    for n,b in files.items():
        if opt.ausgabe:
            opt.ausgabe.mkdir(parents=True,exist_ok=True);(opt.ausgabe/n).write_bytes(b)
        else:
            old=(ROOT/n).read_bytes()
            if n.endswith('.gz'):old,b=gzip.decompress(old),gzip.decompress(b)
            if old!=b:raise ValueError('Abweichung in '+n)
    r=json.loads(files['Ergebnisse.json']);print('PASS ·',r['cases'],'N22-Ordnungs-/Gewichtsfälle.')
    print({k:v['open'] for k,v in r['sectors'].items()},'offen; physische P3: 60 NOT_RUN.')

if __name__=='__main__':main()
