"""Prospective fixed draws; unchanged exact feature kernels. Standard library only."""
from collections import Counter, defaultdict
import gzip
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path
import time

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
spectral=load('transfer_spectral','research/lorentz_observable_comparison/produce.py')
pair=load('transfer_pair','research/lorentz_residual_diagnosis/produce.py')
exact=load('transfer_exact','research/lorentz_n1_stress/produce.py')
require=spectral.require

def token(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def save(path,x): path.write_text(json.dumps(x,indent=2)+'\n')
def rows(c): return [''.join(map(str,r)) for r in c]
def matrix(r): return [[int(x) for x in s] for s in r]
def dumpz(path,text): path.write_bytes(gzip.compress(text.encode(),mtime=0))
def hashbytes(*parts): return hashlib.sha256('|'.join(map(str,parts)).encode()).digest()

def regular(seed,m,draw,degree=3):
    b=[[int((j-i)%m<degree) for j in range(m)] for i in range(m)]; accepted=0
    for s in range(20*m*m):
        h=hashbytes(seed,'regular',m,draw,s)
        i,k,j,l=[int.from_bytes(h[t:t+4],'big')%m for t in (0,4,8,12)]
        if i!=k and j!=l and b[i][j] and b[k][l] and not b[i][l] and not b[k][j]:
            b[i][j]=b[k][l]=0; b[i][l]=b[k][j]=1; accepted+=1
    return [[0]*m+r for r in b]+[[0]*(2*m) for _ in range(m)],accepted

def sampled(seed,family,n,p,draw):
    layers=2 if family=='height2' else 3; width=n//layers
    c=[[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if j//width==i//width+1:
                c[i][j]=int(hashbytes(seed,family,n,p,draw,i,j)[0]%8<p)
    for w in range(n):
        for i in range(n):
            for j in range(n): c[i][j]=int(c[i][j] or (c[i][w] and c[w][j]))
    return c

def structured(name,side=4):
    m=side*side; vertices=[(i//side,i%side) for i in range(m)]
    shifts={(1%side,0),((-1)%side,0),(0,1%side),(0,(-1)%side),(1%side,1%side),((-1)%side,(-1)%side)}
    b=[]
    for i,(a,b0) in enumerate(vertices):
        row=[]
        for j,(x,y) in enumerate(vertices):
            adjacent=(a==x or b0==y) if name=='closed-rook' else ((a-x)%side,(b0-y)%side) in shifts
            row.append(int(i==j or adjacent))
        b.append(row)
    return [[0]*m+r for r in b]+[[0]*(2*m) for _ in range(m)]

def inputs(cfg):
    cc=cfg['inputs']; seed=cc['seed']; result=[]
    def add(name,family,c,**meta): result.append({'id':name,'family':family,'n':len(c),'relation_rows':rows(c),'generation':meta})
    for m in cc['regular']['m']:
        for d in range(cc['regular']['draws_each']):
            c,a=regular(seed,m,d); add(f'reg-m{m}-d{d:02d}','regular',c,m=m,draw=d,accepted_switches=a)
    for family,field in [('height2','bernoulli_height_two'),('height3','three_layer')]:
        for n in cc[field]['n']:
            for p in cc[field]['thresholds_out_of_8']:
                for d in range(cc[field]['draws_each']):
                    add(f'{family}-n{n}-p{p}-d{d:02d}',family,sampled(seed,family,n,p,d),threshold=p,draw=d)
    for name in cc['structured_controls']['names']: add(name,'structured',structured(name))
    require(len(result)==cc['total_draws']+cc['total_controls'],'input count')
    return result

def certificate(c):
    n=len(c); d=spectral.degrees(c)
    low=[i for i in range(n) if d[i][0]==0 and d[i][1]>0]
    high=[i for i in range(n) if d[i][1]==0 and d[i][0]>0]
    require(len(low)+len(high)==n,'certificate requires positive height two')
    result=[]
    for verts,future in [(low,True),(high,False)]:
        masks={i:sum(1<<j for j in range(n) if (c[i][j] if future else c[j][i])) for i in verts}
        counts=Counter((masks[a]&masks[b]&masks[d0]&masks[e]).bit_count() for a,b,d0,e in combinations(verts,4))
        result.append([[k,v] for k,v in sorted(counts.items())])
    return result

def reference(records,certs):
    result=[]
    for a,b in combinations(records,2):
        if a['n']!=b['n']: continue
        x,y=matrix(a['relation_rows']),matrix(b['relation_rows'])
        if a['family']==b['family']=='structured' and certs[a['id']]!=certs[b['id']]: same=False
        else: same=exact.iso(x,y)
        result.append({'ids':[a['id'],b['id']],'isomorphic':same})
    return result

def structural(c):
    d=spectral.degrees(c); heights=[1]*len(c)
    # Full relation in generated topological order.
    for v in range(len(c)): heights[v]=1+max((heights[u] for u in range(v) if c[u][v]),default=0)
    return {'height':max(heights),'isolates':sum(x==[0,0] for x in d),'degree_multiplicities':[[list(k),v] for k,v in sorted(Counter(map(tuple,d)).items())]}

def summary(records,refs,methods):
    cells={}
    for family in ['all','regular','height2','height3','structured']:
        chosen=[r for r in records if family=='all' or r['family']==family]
        for n in sorted({r['n'] for r in chosen}):
            rr=[r for r in chosen if r['n']==n]; names={r['id'] for r in rr}; lookup={r['id']:r for r in rr}
            pp=[p for p in refs if set(p['ids'])<=names]; noniso=[p for p in pp if not p['isomorphic']]
            groups=[]
            for r in rr:
                target=next((g for g in groups if any(set(p['ids'])=={g[0],r['id']} and p['isomorphic'] for p in pp)),None)
                if target is None: groups.append([r['id']])
                else: target.append(r['id'])
            table={}
            for method in methods:
                def eq(ids): return all(lookup[ids[0]]['features'][k]==lookup[ids[1]]['features'][k] for k in method.split('+'))
                collisions=[p['ids'] for p in noniso if eq(p['ids'])]
                require(all(eq(p['ids']) for p in pp if p['isomorphic']),'isomorphic feature disagreement')
                table[method]={'unresolved_nonisomorphic_pairs':len(collisions),'pairs':collisions}
            baseline=table['H7+N1+Q1']['unresolved_nonisomorphic_pairs']; joint=table['H7+N1+Q1+R2']['unresolved_nonisomorphic_pairs']
            cells[f'{family}/n{n}']={'inputs':len(rr),'isomorphism_classes':len(groups),'isomorphism_groups':groups,'draw_pairs':len(pp),'nonisomorphic_draw_pairs':len(noniso),'methods':table,
                'incremental_R2':{'opportunities':baseline,'separated':baseline-joint,'status':'NO_OPPORTUNITY' if baseline==0 else 'ADDITIONAL_SEPARATION' if baseline>joint else 'NO_ADDITIONAL_SEPARATION'}}
    return {'schema':'x6.relational-transfer-summary/1','cells':cells,'scope':'Fixed draws include repeated isomorphism classes; structured controls are separate from prospective samples.'}

def run(directory):
    directory.mkdir(parents=True,exist_ok=False); cfg=json.loads((HERE/'contract.json').read_text())
    records=inputs(cfg); save(directory/'inputs.json',records)
    timing={k:0.0 for k in ['H7','D','M11','N1','Q1']}; traces={}
    for r in records:
        c=matrix(r['relation_rows']); f=spectral.features(c,timing)
        r['features']={k:f[k] for k in ['H7','N1','Q1']}; r['structure']=structural(c)
        print(token({'phase':'features','id':r['id']}),flush=True)
    begin=time.perf_counter()
    for n in sorted({r['n'] for r in records}):
        group=[r for r in records if r['n']==n]
        t=pair.pair_refine([(r['id'],matrix(r['relation_rows'])) for r in group],cfg['resources']['max_refinement_rounds']); traces[str(n)]=t
        for r,a in zip(group,t['rounds'][-1]['matrices']): r['features']['R2']=pair.hist(a)
    timing['R2']=time.perf_counter()-begin
    certs={r['id']:certificate(matrix(r['relation_rows'])) for r in records if r['family']=='structured'}
    refs=reference(records,certs); require(len(refs)==541,'reference coverage')
    dumpz(directory/'records.jsonl.gz',''.join(token(r)+'\n' for r in records)); dumpz(directory/'rounds.json.gz',token(traces)+'\n')
    save(directory/'reference.json',refs); save(directory/'certificate.json',certs); save(directory/'summary.json',summary(records,refs,cfg['methods']))
    costs={k:{'integer_payload':sum(pair.integer_count(r['features'][k]) for r in records),'polynomial_calls':3*len(records) if k=='H7' else sum(6*r['n'] for r in records) if k=='Q1' else 0} for k in ['H7','N1','Q1','R2']}
    costs['R2'].update({'rounds_by_n':{n:t['stabilized_round'] for n,t in traces.items()},'intermediate_contributions':sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values()),'trace_integer_payload':sum(sum(pair.integer_count(a) for a in s['matrices']) for t in traces.values() for s in t['rounds']),'context':'Histograms require the joint corpus and reconstructed exact palette; not standalone fingerprints.'})
    save(directory/'costs.json',costs); save(directory/'timing.json',timing)

if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
