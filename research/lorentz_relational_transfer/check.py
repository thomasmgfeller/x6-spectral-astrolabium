"""Separate input replay, exact arithmetic, pair kernels and pairwise accounting."""
from collections import Counter
import copy
import gzip
import hashlib
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path)
    module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module
old=load('transfer_reference_spectral','research/lorentz_observable_comparison/check.py')
pair=load('transfer_reference_pair','research/lorentz_residual_diagnosis/check.py')
bipartite=load('transfer_reference_iso','research/lorentz_n1_stress/check.py')
require=old.require
match=old.match

def save(path,x): path.write_text(json.dumps(x,indent=2)+'\n')
def digest(parts): return hashlib.sha256('|'.join(str(x) for x in parts).encode()).hexdigest()
def from_edges(n,edges): return [[int((i,j) in edges) for j in range(n)] for i in range(n)]

def regular(seed,m,draw,degree=3):
    edges={(i,(i+k)%m) for i in range(m) for k in range(degree)}; accepted=0
    for step in range(20*m*m):
        h=digest([seed,'regular',m,draw,step]); i,k,j,l=[int(h[z:z+8],16)%m for z in (0,8,16,24)]
        before={(i,j),(k,l)}; after={(i,l),(k,j)}
        if len({i,k})==len({j,l})==2 and before<=edges and not edges&after:
            edges-=before; edges|=after; accepted+=1
    return from_edges(2*m,{(i,m+j) for i,j in edges}),accepted

def sampled(seed,family,n,p,draw):
    width=n//(2 if family=='height2' else 3); edges=set()
    for i in range(n):
        for j in range(n):
            if j//width-i//width==1 and int(digest([seed,family,n,p,draw,i,j])[:2],16)%8<p: edges.add((i,j))
    closure=set()
    for root in range(n):
        pending=[v for u,v in edges if u==root]; seen=set()
        while pending:
            v=pending.pop()
            if v not in seen:
                seen.add(v); pending.extend(w for u,w in edges if u==v)
        closure.update((root,v) for v in seen)
    return from_edges(n,closure)

def structured(name,side=4):
    points=[(a,b) for a in range(side) for b in range(side)]; edges=set(); m=len(points)
    for i,(a,b) in enumerate(points):
        if name=='closed-rook': neighbors={(a,t) for t in range(side)}|{(t,b) for t in range(side)}
        else: neighbors={((a+da)%side,(b+db)%side) for da,db in [(0,0),(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1)]}
        for j,point in enumerate(points):
            if point in neighbors: edges.add((i,m+j))
    return from_edges(2*m,edges)

def inputs(cfg):
    cc=cfg['inputs']; seed=cc['seed']; result=[]
    def put(name,family,c,meta): result.append({'id':name,'family':family,'n':len(c),'relation_rows':old.rows(c),'generation':meta})
    for m in cc['regular']['m']:
        for d in range(cc['regular']['draws_each']):
            c,a=regular(seed,m,d); put(f'reg-m{m}-d{d:02d}','regular',c,{'m':m,'draw':d,'accepted_switches':a})
    for family,field in [('height2','bernoulli_height_two'),('height3','three_layer')]:
        for n in cc[field]['n']:
            for p in cc[field]['thresholds_out_of_8']:
                for d in range(cc[field]['draws_each']): put(f'{family}-n{n}-p{p}-d{d:02d}',family,sampled(seed,family,n,p,d),{'threshold':p,'draw':d})
    for name in cc['structured_controls']['names']: put(name,'structured',structured(name),{})
    return result

def certificate(c):
    degrees=old.degree(c); lower=[i for i,d in enumerate(degrees) if d[0]==0 and d[1]>0]; upper=[i for i,d in enumerate(degrees) if d[1]==0 and d[0]>0]
    require(len(lower)+len(upper)==len(c),'certificate layer partition')
    result=[]
    for verts,future in [(lower,True),(upper,False)]:
        counts=Counter()
        for group in combinations(verts,4):
            count=sum(all(c[v][w] if future else c[w][v] for v in group) for w in range(len(c)))
            counts[count]+=1
        result.append([list(item) for item in sorted(counts.items())])
    return result

def reference(records,certs):
    result=[]
    for i in range(len(records)):
        for j in range(i+1,len(records)):
            a,b=records[i],records[j]
            if a['n']!=b['n']: continue
            x,y=old.matrix(a['relation_rows']),old.matrix(b['relation_rows'])
            if a['family']==b['family']=='structured' and certs[a['id']]!=certs[b['id']]: same=False
            elif a['n']<=12: same=old.iso(x,y)
            else: same=bipartite.iso(x,y)
            result.append({'ids':[a['id'],b['id']],'isomorphic':same})
    return result

def structural(c):
    def length(v): return 1+max((length(u) for u in range(len(c)) if c[u][v]),default=0)
    d=old.degree(c)
    return {'height':max(length(v) for v in range(len(c))),'isolates':sum(not any(x) for x in d),'degree_multiplicities':[[list(k),v] for k,v in sorted(Counter(d).items())]}

def summary(records,refs,methods):
    output={}
    for family in ['all','regular','height2','height3','structured']:
        for n in sorted({r['n'] for r in records if family=='all' or r['family']==family}):
            rr=[r for r in records if r['n']==n and (family=='all' or r['family']==family)]; names=[r['id'] for r in rr]; f={r['id']:r['features'] for r in rr}
            pp=[p for p in refs if all(x in names for x in p['ids'])]; parent={x:x for x in names}
            def root(x):
                while parent[x]!=x: x=parent[x]
                return x
            for p in pp:
                if p['isomorphic']: parent[root(p['ids'][1])]=root(p['ids'][0])
            groups=[]
            for name in names:
                g=next((g for g in groups if root(g[0])==root(name)),None)
                if g is None: groups.append([name])
                else: g.append(name)
            # Pair reference must itself define the exact same equivalence relation.
            require(all((root(p['ids'][0])==root(p['ids'][1]))==p['isomorphic'] for p in pp),'reference equivalence inconsistency')
            table={}
            for method in methods:
                failures=[]
                for p in pp:
                    a,b=p['ids']; equal=all(f[a][k]==f[b][k] for k in method.split('+'))
                    require(not p['isomorphic'] or equal,'invariance failure')
                    if not p['isomorphic'] and equal: failures.append([a,b])
                table[method]={'unresolved_nonisomorphic_pairs':len(failures),'pairs':failures}
            base=len(table['H7+N1+Q1']['pairs']); residual=len(table['H7+N1+Q1+R2']['pairs'])
            output[f'{family}/n{n}']={'inputs':len(rr),'isomorphism_classes':len(groups),'isomorphism_groups':groups,'draw_pairs':len(pp),'nonisomorphic_draw_pairs':sum(not p['isomorphic'] for p in pp),'methods':table,
                'incremental_R2':{'opportunities':base,'separated':base-residual,'status':'NO_OPPORTUNITY' if not base else 'ADDITIONAL_SEPARATION' if base!=residual else 'NO_ADDITIONAL_SEPARATION'}}
    return {'schema':'x6.relational-transfer-summary/1','cells':output,'scope':'Fixed draws include repeated isomorphism classes; structured controls are separate from prospective samples.'}

def validate(actual,expected):
    for r in actual['inputs']: old.matrix(r['relation_rows'])
    for name in expected: match(actual[name],expected[name],'artifact mismatch: '+name)

def run(directory):
    cfg=json.loads((HERE/'contract.json').read_text())
    actual={name:json.loads((directory/(name+'.json')).read_text()) for name in ['inputs','reference','certificate','summary','costs']}
    actual['records']=[json.loads(s) for s in gzip.decompress((directory/'records.jsonl.gz').read_bytes()).decode().splitlines()]
    actual['rounds']=json.loads(gzip.decompress((directory/'rounds.json.gz').read_bytes()))
    expected={'inputs':inputs(cfg)}; match(actual['inputs'],expected['inputs'],'input replay')
    expected['records']=copy.deepcopy(expected['inputs']); records=expected['records']; traces={}
    for r in records:
        c=old.matrix(r['relation_rows']); f=old.compute(c)
        r['features']={k:f[k] for k in ['H7','N1','Q1']}; r['structure']=structural(c)
        print(json.dumps({'phase':'checker-features','id':r['id']}),flush=True)
    for n in sorted({r['n'] for r in records}):
        rr=[r for r in records if r['n']==n]; graphs=[(r['id'],old.matrix(r['relation_rows'])) for r in rr]
        t=pair.refine(graphs,cfg['resources']['max_refinement_rounds']); traces[str(n)]=t
        perm=list(reversed(range(n))); relabelled=[(name,[[c[i][j] for j in perm] for i in perm]) for name,c in graphs]
        transport=pair.refine(relabelled,cfg['resources']['max_refinement_rounds'])
        match(t['stabilized_round'],transport['stabilized_round'],'relabel stabilization')
        for step,other in zip(t['rounds'],transport['rounds']):
            match(step['colors'],other['colors'],'relabel colors')
            match([[[a[i][j] for j in perm] for i in perm] for a in step['matrices']],other['matrices'],'relabel round transport')
        for r,a in zip(rr,t['rounds'][-1]['matrices']): r['features']['R2']=pair.histogram(a)
    expected['rounds']=traces
    expected['certificate']={r['id']:certificate(old.matrix(r['relation_rows'])) for r in records if r['family']=='structured'}
    expected['reference']=reference(records,expected['certificate']); match(len(expected['reference']),541,'reference coverage')
    expected['summary']=summary(records,expected['reference'],cfg['methods'])
    def count(x): return 1 if isinstance(x,int) else sum(count(y) for y in x)
    costs={k:{'integer_payload':sum(count(r['features'][k]) for r in records),'polynomial_calls':len(records)*3 if k=='H7' else 6*sum(r['n'] for r in records) if k=='Q1' else 0} for k in ['H7','N1','Q1','R2']}
    costs['R2'].update({'rounds_by_n':{n:t['stabilized_round'] for n,t in traces.items()},'intermediate_contributions':sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values()),'trace_integer_payload':sum(sum(count(a) for a in s['matrices']) for t in traces.values() for s in t['rounds']),'context':'Histograms require the joint corpus and reconstructed exact palette; not standalone fingerprints.'})
    expected['costs']=costs; validate(actual,expected)
    rejected=[]
    for kind in ['self_loop','missing_input','Q1_coefficient','R2_multiplicity','R2_round','missing_reference_pair']:
        bad=copy.deepcopy(actual)
        if kind=='self_loop':
            row=bad['inputs'][0]['relation_rows'][0]; bad['inputs'][0]['relation_rows'][0]='1'+row[1:]
        elif kind=='missing_input': bad['inputs'].pop()
        elif kind=='Q1_coefficient': bad['records'][0]['features']['Q1'][0][0][0][0]+=1
        elif kind=='R2_multiplicity': bad['records'][0]['features']['R2'][0][1]+=1
        elif kind=='R2_round': bad['rounds']['8']['rounds'][0]['matrices'][0][0][0]+=1
        else: bad['reference'].pop()
        try: validate(bad,expected)
        except ValueError: rejected.append(kind)
    match(len(rejected),6,'negative-control coverage')
    save(directory/'verification.json',{'status':'PASS_EXACT_FIXED_TRANSFER','inputs':len(records),'same_size_reference_pairs':len(expected['reference']),
        'polynomials_per_arithmetic_path':costs['H7']['polynomial_calls']+costs['Q1']['polynomial_calls'],
        'all_round_matrices_agree':True,'all_relabelled_rounds_agree':True,'all_reference_pairs_agree':True,'negative_controls_rejected':rejected,
        'independence_scope':'Separate code paths from one authoring process; not independent human review.'})

if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
