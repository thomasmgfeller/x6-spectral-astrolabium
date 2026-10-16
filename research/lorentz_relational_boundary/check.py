"""Independent subset sums, alternating inversion and complete relation checks."""
from collections import Counter
import copy,gzip,importlib.util,json,math
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,ROOT/path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module); return module
old=load('boundary_check_old','research/lorentz_observable_comparison/check.py')
exact=load('boundary_check_iso','research/lorentz_n1_stress/check.py')
pair=load('boundary_check_pair','research/lorentz_residual_diagnosis/check.py')
require=old.require; match=old.match
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def readz(p): return json.loads(gzip.decompress(p.read_bytes()))
def transpose(b): return [[b[i][j] for i in range(len(b))] for j in range(len(b[0]))]

def cycle(blocks):
    m=sum(blocks); edges=set(); offset=0
    for length in blocks:
        require(length>=3,'cycle size')
        nodes=list(range(offset,offset+length))
        for i,j in zip(nodes,nodes[1:]+nodes[:1]): edges.update([(i,m+i),(i,m+j)])
        offset+=length
    return [[int((i,j) in edges) for j in range(2*m)] for i in range(2*m)]

def population(cfg):
    rr=[]
    for line in (ROOT/'research/lorentz_n1_stress/results/records.jsonl').read_text().splitlines():
        r=json.loads(line); rr.append({'id':r['id'],'family':'stress','m':r['m'],'relation_rows':r['relation_rows'],'features':dict(r['features'])})
    transfer=[json.loads(line) for line in gzip.decompress((ROOT/'research/lorentz_relational_transfer/results/records.jsonl.gz').read_bytes()).decode().splitlines()]
    for name in ['closed-rook','closed-shrikhande']:
        r=next(r for r in transfer if r['id']==name); rr.append({'id':name,'family':'structured','m':16,'relation_rows':r['relation_rows'],'features':{k:r['features'][k] for k in ['H7','N1','Q1']}})
    for m in cfg['population']['cycles']['m']:
        for kind in cfg['population']['cycles']['types']:
            rr.append({'id':f'cycle-m{m}-{kind}','family':'cycles','m':m,'relation_rows':old.rows(cycle([m] if kind=='one' else [3,m-3])),'features':{}})
    match(len(rr),217,'fixed input coverage'); return rr

def incidence(r):
    c=old.matrix(r['relation_rows']); m=r['m']; match(len(c),2*m,'size')
    d=old.degree(c); low=[i for i,x in enumerate(d) if x[0]==0 and x[1]>0]; high=[i for i,x in enumerate(d) if x[1]==0 and x[0]>0]
    match(low,list(range(m)),'lower side'); match(high,list(range(m,2*m)),'upper side')
    require(all(not c[i][j] or (i in low and j in high) for i in range(2*m) for j in range(2*m)),'height-two edges')
    return [[c[i][j] for j in high] for i in low]

def subsets(m,d): return {sum(2**i for i in s):s for k in range(d+1) for s in combinations(range(m),k)}
def encode(b):
    m=len(b); u=len(b[0]); require(m>0 and u>0 and all(len(row)==u and all(x in (0,1) for x in row) for row in b),'binary incidence')
    d=max(sum(b[i][j] for i in range(m)) for j in range(u))
    values=[[mask,sum(all(b[i][j] for i in group) for j in range(u))] for mask,group in sorted(subsets(m,d).items())]
    return {'rows':m,'columns':u,'degree_cap':d,'counts':values}

def decode(e):
    m,u,d=e['rows'],e['columns'],e['degree_cap']; require(all(type(x) is int for x in [m,u,d]) and m>0 and u>0 and 0<=d<=m,'metadata')
    ss=subsets(m,d); match([s for s,g in e['counts']],sorted(ss),'indexed domain')
    require(all(type(g) is int and 0<=g<=u for s,g in e['counts']),'count bounds'); require(e['counts'][0]==[0,u],'empty count')
    answer={s:0 for s in ss}
    for mask,g in e['counts']:
        if not g: continue
        group=ss[mask]
        for k in range(len(group)+1):
            sign=(-1)**(len(group)-k)
            for t in combinations(group,k): answer[sum(2**i for i in t)]+=sign*g
    require(all(a>=0 for a in answer.values()),'negative inversion'); require(sum(answer.values())==u,'multiplicity total')
    return [[s,a] for s,a in sorted(answer.items()) if a]

def reconstruct(b,e):
    columns=decode(e); key=lambda j:sum(b[i][j]*2**i for i in range(len(b)))
    result={'columns':columns,'output_to_input_column_permutation':sorted(range(len(b[0])),key=key)}
    verify_reconstruction(b,e,result); return result

def verify_reconstruction(b,e,result):
    match(decode(e),result['columns'],'neighborhood multiplicities')
    p=result['output_to_input_column_permutation']; match(sorted(p),list(range(len(b[0]))),'column bijection')
    masks=[s for s,a in result['columns'] for _ in range(a)]; match(len(masks),len(p),'column coverage')
    rebuilt=[[int(bool(s&2**i)) for s in masks] for i in range(len(b))]
    match(rebuilt,[[row[j] for j in p] for row in b],'entire reconstructed relation')

def pooled(e):
    result=[]
    for k in range(1,e['rows']+1):
        values=[g for s,g in e['counts'] if s.bit_count()==k]
        if k>e['degree_cap']: result.append([[0,math.comb(e['rows'],k)]])
        else:
            match(len(values),math.comb(e['rows'],k),'profile domain')
            result.append([[v,values.count(v)] for v in sorted(set(values))])
    return result

def value(r,method):
    if '+' in method: return [value(r,k) for k in method.split('+')]
    if method.startswith('P') and method!='Pall':
        p=r['features']['Pall']; k=int(method[-1]); return [p[0],p[1],p[2][:k],p[3][:k]]
    return r['features'][method]

def reference(records):
    result=[]
    for i,a in enumerate(records):
        for b in records[i+1:]:
            if a['m']!=b['m']: continue
            if a['family']==b['family']=='structured':
                # Explicit four-root direct counts, independent of saved profile.
                hist=[]
                for r in [a,b]:
                    mat=incidence(r); values=[sum(all(mat[u][v] for u in group) for v in range(r['m'])) for group in combinations(range(r['m']),4)]
                    hist.append(Counter(values))
                require(hist[0]!=hist[1],'structured nonisomorphism witness'); same=False
            else: same=exact.iso(old.matrix(a['relation_rows']),old.matrix(b['relation_rows']))
            result.append({'ids':[a['id'],b['id']],'isomorphic':same})
    return result

def summary(records,refs,methods):
    cells={}
    for family in ['all','stress','structured','cycles']:
        selected=[r for r in records if family=='all' or r['family']==family]
        for m in sorted({r['m'] for r in selected}):
            rr=[r for r in selected if r['m']==m]; names=[r['id'] for r in rr]; lookup={r['id']:r for r in rr}; pp=[p for p in refs if all(x in names for x in p['ids'])]
            parent={x:x for x in names}
            def root(x):
                while parent[x]!=x: x=parent[x]
                return x
            for p in pp:
                if p['isomorphic']: parent[root(p['ids'][1])]=root(p['ids'][0])
            groups=[]
            for x in names:
                group=next((g for g in groups if root(g[0])==root(x)),None)
                if group is None: groups.append([x])
                else: group.append(x)
            require(all((root(p['ids'][0])==root(p['ids'][1]))==p['isomorphic'] for p in pp),'isomorphism transitivity')
            table={}
            for method in methods:
                fingerprints=[value(r,method) for r in rr]; unique=[]
                for f in fingerprints:
                    if f not in unique: unique.append(f)
                failures=[]
                for p in pp:
                    a,b=(lookup[x] for x in p['ids']); same=value(a,method)==value(b,method)
                    require(not p['isomorphic'] or same,'isomorphic fingerprints')
                    if same and not p['isomorphic']: failures.append(p['ids'])
                table[method]={'feature_classes':len(unique),'unresolved_pairs':len(failures),'pairs':failures}
            base=table['R2']['unresolved_pairs']; after=table['R2+Pall']['unresolved_pairs']
            cells[f'{family}/n{2*m}']={'orders':len(rr),'isomorphism_classes':len(groups),'isomorphism_groups':groups,'same_size_pairs':len(pp),'nonisomorphic_pairs':sum(not p['isomorphic'] for p in pp),'methods':table,
                'Pall_added_to_R2':{'opportunities':base,'separated':base-after,'status':'NO_OPPORTUNITY' if base==0 else 'ADDITIONAL_SEPARATION' if base!=after else 'NO_ADDITIONAL_SEPARATION'}}
    return {'schema':'x6.relational-boundary-summary/1','cells':cells,'scope':'Known corpus and theory-motivated controls; indexed counts are not included as an invariant fingerprint.'}

def components(c):
    groups=[{i} for i in range(len(c))]
    for i in range(len(c)):
        for j in range(len(c)):
            if c[i][j]:
                a=next(g for g in groups if i in g); b=next(g for g in groups if j in g)
                if a is not b: a.update(b); groups.remove(b)
    return len(groups)

def controls(records):
    names=[['m8-r012','m8-r070'],['closed-rook','closed-shrikhande']]+[[f'cycle-m{m}-one',f'cycle-m{m}-split'] for m in [6,7,8,9]]; lookup={r['id']:r for r in records}; result=[]
    for ids in names:
        a,b=[lookup[x] for x in ids]; p,q=a['features']['Pall'],b['features']['Pall']; differences=[k+1 for k in range(a['m']) if [p[2][k],p[3][k]]!=[q[2][k],q[3][k]]]
        if a['family']=='cycles':
            m=a['m']; prediction=[[[2,m]],[[0,math.comb(m,2)-m],[1,m]]]+[[[0,math.comb(m,k)]] for k in range(3,m+1)]
            match(p,[m,m,prediction,prediction],'cycle all-order formula'); match(p,q,'cycle pooled collision')
        result.append({'ids':ids,'Pall':[p,q],'first_distinguishing_order':differences[0] if differences else None,'R2_equal':a['features']['R2']==b['features']['R2'],
            'H7_N1_Q1_equal':value(a,'H7+N1+Q1')==value(b,'H7+N1+Q1'),'undirected_components':[components(old.matrix(r['relation_rows'])) for r in [a,b]]})
    return result

def validate(actual,expected):
    for r in actual['inputs']: incidence(r)
    for name,obj in expected.items(): match(actual[name],obj,'artifact mismatch: '+name)

def run(directory):
    cfg=json.loads((HERE/'contract.json').read_text()); records=population(cfg); expected={'inputs':[{k:v for k,v in r.items() if k!='features'} for r in records]}; encodings=[]; rebuilt=[]
    for r in records:
        b=incidence(r); e=[encode(b),encode(transpose(b))]; encodings.append({'id':r['id'],'future':e[0],'past':e[1]}); rebuilt.append({'id':r['id'],'future':reconstruct(b,e[0]),'past':reconstruct(transpose(b),e[1])})
        r['features']['Pall']=[r['m'],r['m'],pooled(e[0]),pooled(e[1])]
        reverse=[list(reversed(row)) for row in reversed(b)]
        for original,other in zip(e,[encode(reverse),encode(transpose(reverse))]):
            match(pooled(original),pooled(other),'pooled relabel invariance')
            m=original['rows']; transported=sorted([[sum(((s>>i)&1)<<(m-1-i) for i in range(m)),g] for s,g in original['counts']])
            match(transported,other['counts'],'subset identity transport')
        if r['family']=='cycles':
            f=old.compute(old.matrix(r['relation_rows'])); r['features'].update({k:f[k] for k in ['H7','N1','Q1']})
    traces={}
    for m in sorted({r['m'] for r in records}):
        rr=[r for r in records if r['m']==m]; graphs=[(r['id'],old.matrix(r['relation_rows'])) for r in rr]; t=pair.refine(graphs,cfg['resources']['max_refinement_rounds']); traces[str(2*m)]=t
        reverse=[(name,[list(reversed(row)) for row in reversed(c)]) for name,c in graphs]; other=pair.refine(reverse,cfg['resources']['max_refinement_rounds'])
        match(t['stabilized_round'],other['stabilized_round'],'relabel stable round')
        for s,q in zip(t['rounds'],other['rounds']):
            match(s['colors'],q['colors'],'relabel palette'); match([[list(reversed(row)) for row in reversed(a)] for a in s['matrices']],q['matrices'],'relabel round matrices')
        for r,a in zip(rr,t['rounds'][-1]['matrices']): r['features']['R2']=pair.histogram(a)
    refs=reference(records); match(len(refs),7088,'pair coverage'); full=summary(records,refs,cfg['pooled_features']['methods'])
    expected.update({'records':records,'indexed':encodings,'reconstruction':rebuilt,'rounds':traces,'reference':refs,'summary':full,'controls':controls(records)})
    counts=copy.deepcopy(full)
    for cell in counts['cells'].values():
        del cell['isomorphism_groups']
        for row in cell['methods'].values(): del row['pairs']
    expected['summary_counts']=counts
    def integers(x): return 1 if type(x) is int else sum(integers(v) for v in x)
    expected['costs']={'indexed_directions':[{'id':r['id'],'binary_incidence_entries':r['m']**2,'future_entries':len(e['future']['counts']),'past_entries':len(e['past']['counts']),'future_degree_cap':e['future']['degree_cap'],'past_degree_cap':e['past']['degree_cap']} for r,e in zip(records,encodings)],
        'new_characteristic_polynomials':sum(3+12*r['m'] for r in records if r['family']=='cycles'),'reused_previously_verified_feature_records':209,
        'Pall_integer_payload':sum(integers(r['features']['Pall']) for r in records),'indexed_subset_and_count_integers':sum(2*(len(e['future']['counts'])+len(e['past']['counts'])) for e in encodings),
        'R2_intermediate_contributions':sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values()),'R2_rounds_by_n':{n:t['stabilized_round'] for n,t in traces.items()},
        'R2_trace_integer_payload':sum(integers(a) for t in traces.values() for s in t['rounds'] for a in s['matrices']),
        'warning':'Indexed subsets retain row labels. R2 color numbers require the jointly refined corpus. No standalone-fingerprint or generic compression claim.'}
    zipped={'records','indexed','reconstruction','rounds','reference','summary'}
    actual={name:readz(directory/(name+'.json.gz')) if name in zipped else json.loads((directory/(name+'.json')).read_text()) for name in expected}; validate(actual,expected)
    rejected=[]
    for kind in ['missing_subset','wrong_degree_cap','altered_count','lost_column_multiplicity','false_column_witness','corrupted_R2_trace','omitted_input','omitted_residual_pair']:
        e=copy.deepcopy(encodings[0]['future']); r=copy.deepcopy(rebuilt[0]['future']); bad=None
        if kind=='missing_subset': e['counts'].pop()
        elif kind=='wrong_degree_cap': e['degree_cap']-=1
        elif kind=='altered_count': e['counts'][0][1]+=1
        elif kind=='lost_column_multiplicity': r['columns'][0][1]-=1
        elif kind=='false_column_witness': r['output_to_input_column_permutation'][0]=r['output_to_input_column_permutation'][1]
        else:
            bad=copy.deepcopy(actual)
            if kind=='corrupted_R2_trace': bad['rounds']['12']['rounds'][0]['matrices'][0][0][0]+=1
            elif kind=='omitted_input': bad['inputs'].pop()
            else: bad['summary']['cells']['structured/n32']['methods']['R2']['pairs'].pop()
        try:
            if bad is not None: validate(bad,expected)
            else: verify_reconstruction(incidence(records[0]),e,r)
        except ValueError: rejected.append(kind)
    match(len(rejected),8,'negative controls')
    for r,e in zip(records,encodings):
        for direction in ['future','past']:
            x=e[direction]; match(len(x['counts']),sum(math.comb(x['rows'],k) for k in range(x['degree_cap']+1)),'indexed storage formula')
    save(directory/'verification.json',{'status':'PASS_EXACT_BOUNDARY_STUDY','orders':len(records),'exact_reference_pairs':len(refs),'new_polynomials_per_arithmetic_path':expected['costs']['new_characteristic_polynomials'],
        'reused_prior_feature_records':209,'indexed_directions_reconstructed':2*len(records),'all_subset_transports_and_round_matrices_agree':True,
        'negative_controls_rejected':rejected,'scope':'Separate implementations from one authoring process. The 209 historical H7/N1/Q1 records are hash-bound reuse, not newly recomputed polynomials.'})
    print(json.dumps({'status':'PASS_EXACT_BOUNDARY_STUDY','orders':len(records),'pairs':len(refs)}))

if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
