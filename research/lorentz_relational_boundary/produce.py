"""Fixed pooled profiles and labelled incidence reconstruction; exact integers."""
from collections import Counter,defaultdict
import gzip,hashlib,importlib.util,json,math,time
from itertools import combinations
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parents[1]
def load(name,path):
    s=importlib.util.spec_from_file_location(name,ROOT/path); m=importlib.util.module_from_spec(s); s.loader.exec_module(m); return m
old=load('boundary_old','research/lorentz_observable_comparison/produce.py')
exact=load('boundary_iso','research/lorentz_n1_stress/produce.py')
pair=load('boundary_pair','research/lorentz_residual_diagnosis/produce.py')
require=old.require
def token(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def save(p,x): p.write_text(json.dumps(x,indent=2)+'\n')
def savez(p,x): p.write_bytes(gzip.compress((token(x)+'\n').encode(),mtime=0))
def matrix(rows): return [[int(x) for x in row] for row in rows]
def rows(c): return [''.join(map(str,row)) for row in c]
def transpose(b): return list(map(list,zip(*b)))
def domain(m,d): return sorted(sum(1<<i for i in s) for k in range(d+1) for s in combinations(range(m),k))

def cycle(blocks):
    m=sum(blocks); b=[[0]*m for _ in range(m)]; start=0
    for length in blocks:
        require(length>=3,'cycle block size')
        for i in range(length): b[start+i][start+i]=b[start+i][start+(i+1)%length]=1
        start+=length
    return [[0]*m+row for row in b]+[[0]*(2*m) for _ in range(m)]

def population(cfg):
    original=[json.loads(s) for s in (ROOT/'research/lorentz_n1_stress/results/records.jsonl').read_text().splitlines()]
    transfer=[json.loads(s) for s in gzip.decompress((ROOT/'research/lorentz_relational_transfer/results/records.jsonl.gz').read_bytes()).decode().splitlines()]
    result=[{'id':r['id'],'family':'stress','m':r['m'],'relation_rows':r['relation_rows'],'features':dict(r['features'])} for r in original]
    for name in ['closed-rook','closed-shrikhande']:
        r=next(r for r in transfer if r['id']==name)
        result.append({'id':name,'family':'structured','m':16,'relation_rows':r['relation_rows'],'features':{k:r['features'][k] for k in ['H7','N1','Q1']}})
    for m in cfg['population']['cycles']['m']:
        for kind in cfg['population']['cycles']['types']:
            result.append({'id':f'cycle-m{m}-{kind}','family':'cycles','m':m,'relation_rows':rows(cycle([m] if kind=='one' else [3,m-3])),'features':{}})
    require(len(result)==cfg['population']['orders'],'population count'); return result

def incidence(r):
    c=matrix(r['relation_rows']); m=r['m']; require(len(c)==2*m and all(len(row)==2*m for row in c),'square size')
    require(all(x in (0,1) and (not x or i<m<=j) for i,row in enumerate(c) for j,x in enumerate(row)),'strict two-layer form')
    b=[row[m:] for row in c[:m]]; require(all(map(any,b)) and all(map(any,transpose(b))),'positive layers'); return b

def encode(b):
    m=len(b); u=len(b[0]); require(m>0 and u>0 and all(len(row)==u and all(x in (0,1) for x in row) for row in b),'binary incidence')
    d=max(map(sum,transpose(b))); masks=[sum(x<<j for j,x in enumerate(row)) for row in b]; values=[]
    for s in domain(m,d):
        common=(1<<u)-1; pending=s
        while pending:
            bit=pending&-pending; common&=masks[bit.bit_length()-1]; pending-=bit
        values.append([s,common.bit_count()])
    return {'rows':m,'columns':u,'degree_cap':d,'counts':values}

def decode(e):
    m,u,d=e['rows'],e['columns'],e['degree_cap']
    require(all(type(x) is int for x in [m,u,d]) and m>0 and u>0 and 0<=d<=m,'metadata')
    require([s for s,g in e['counts']]==domain(m,d),'complete indexed domain')
    require(all(type(g) is int and 0<=g<=u for s,g in e['counts']),'count bounds')
    remaining=dict(e['counts']); require(remaining[0]==u,'empty subset count'); recovered={}
    for t in sorted(remaining,key=lambda x:(-x.bit_count(),x)):
        a=remaining[t]; require(a>=0,'negative neighborhood multiplicity')
        if a:
            recovered[t]=a
            if t:
                s=(t-1)&t
                while True:
                    remaining[s]-=a
                    if not s: break
                    s=(s-1)&t
    require(sum(recovered.values())==u,'column multiplicity total')
    return [[s,a] for s,a in sorted(recovered.items())]

def reconstruct(b,e):
    columns=decode(e); original=[sum(b[i][j]<<i for i in range(len(b))) for j in range(len(b[0]))]
    permutation=sorted(range(len(original)),key=lambda j:original[j])
    require([original[j] for j in permutation]==[s for s,a in columns for _ in range(a)],'reconstruction mismatch')
    return {'columns':columns,'output_to_input_column_permutation':permutation}

def pooled(e):
    m,d=e['rows'],e['degree_cap']; hist=[]
    for k in range(1,m+1):
        counts=Counter(g for s,g in e['counts'] if s.bit_count()==k) if k<=d else Counter({0:math.comb(m,k)})
        require(sum(counts.values())==math.comb(m,k),'profile subset coverage')
        hist.append([[g,a] for g,a in sorted(counts.items())])
    return hist

def value(r,method):
    if '+' in method: return [value(r,k) for k in method.split('+')]
    if method in ['P1','P12','P123','P1234']:
        k=len(method)-1; p=r['features']['Pall']; return p[:2]+[p[2][:k],p[3][:k]]
    return r['features'][method]

def reference(records):
    result=[]
    for a,b in combinations(records,2):
        if a['m']!=b['m']: continue
        if a['family']==b['family']=='structured':
            require(a['features']['Pall'][2][3]!=b['features']['Pall'][2][3],'known fourth-order certificate'); same=False
        else:
            x,y=matrix(a['relation_rows']),matrix(b['relation_rows'])
            same=exact.prefilter(x)==exact.prefilter(y) and exact.iso(x,y)
        result.append({'ids':[a['id'],b['id']],'isomorphic':same})
    return result

def summary(records,refs,methods):
    output={}
    for family in ['all','stress','structured','cycles']:
        for m in sorted({r['m'] for r in records if family=='all' or r['family']==family}):
            rr=[r for r in records if r['m']==m and (family=='all' or r['family']==family)]; lookup={r['id']:r for r in rr}
            pp=[p for p in refs if all(x in lookup for x in p['ids'])]; groups=[]
            for r in rr:
                group=next((g for g in groups if any(set(p['ids'])=={g[0],r['id']} and p['isomorphic'] for p in pp)),None)
                if group is None: groups.append([r['id']])
                else: group.append(r['id'])
            table={}
            for method in methods:
                eq=lambda ids:value(lookup[ids[0]],method)==value(lookup[ids[1]],method)
                require(all(eq(p['ids']) for p in pp if p['isomorphic']),'isomorphic feature mismatch')
                bad=[p['ids'] for p in pp if not p['isomorphic'] and eq(p['ids'])]
                table[method]={'feature_classes':len({token(value(r,method)) for r in rr}),'unresolved_pairs':len(bad),'pairs':bad}
            base=table['R2']['unresolved_pairs']; combined=table['R2+Pall']['unresolved_pairs']
            output[f'{family}/n{2*m}']={'orders':len(rr),'isomorphism_classes':len(groups),'isomorphism_groups':groups,'same_size_pairs':len(pp),'nonisomorphic_pairs':sum(not p['isomorphic'] for p in pp),'methods':table,
                'Pall_added_to_R2':{'opportunities':base,'separated':base-combined,'status':'NO_OPPORTUNITY' if not base else 'ADDITIONAL_SEPARATION' if base>combined else 'NO_ADDITIONAL_SEPARATION'}}
    return {'schema':'x6.relational-boundary-summary/1','cells':output,'scope':'Known corpus and theory-motivated controls; indexed counts are not included as an invariant fingerprint.'}

def components(c):
    unseen=set(range(len(c))); count=0
    while unseen:
        count+=1; pending=[unseen.pop()]
        while pending:
            v=pending.pop(); new={w for w in unseen if c[v][w] or c[w][v]}; unseen-=new; pending.extend(new)
    return count

def controls(records):
    lookup={r['id']:r for r in records}; targets=[['m8-r012','m8-r070'],['closed-rook','closed-shrikhande']]+[[f'cycle-m{m}-one',f'cycle-m{m}-split'] for m in [6,7,8,9]]; result=[]
    for ids in targets:
        a,b=(lookup[name] for name in ids); p,q=a['features']['Pall'],b['features']['Pall']
        first=next((k+1 for k in range(a['m']) if p[2][k]!=q[2][k] or p[3][k]!=q[3][k]),None)
        result.append({'ids':ids,'Pall':[p,q],'first_distinguishing_order':first,'R2_equal':a['features']['R2']==b['features']['R2'],
            'H7_N1_Q1_equal':value(a,'H7+N1+Q1')==value(b,'H7+N1+Q1'),'undirected_components':[components(matrix(r['relation_rows'])) for r in [a,b]]})
    return result

def run(directory):
    directory.mkdir(parents=True,exist_ok=False); cfg=json.loads((HERE/'contract.json').read_text()); records=population(cfg)
    save(directory/'inputs.json',[{k:v for k,v in r.items() if k!='features'} for r in records]); encodings=[]; rebuilt=[]; timing={k:0.0 for k in ['H7','D','M11','N1','Q1']}; begin=time.perf_counter()
    for r in records:
        b=incidence(r); e=[encode(b),encode(transpose(b))]
        encodings.append({'id':r['id'],'future':e[0],'past':e[1]}); rebuilt.append({'id':r['id'],'future':reconstruct(b,e[0]),'past':reconstruct(transpose(b),e[1])})
        r['features']['Pall']=[len(b),len(b[0]),pooled(e[0]),pooled(e[1])]
        if r['family']=='cycles':
            f=old.features(matrix(r['relation_rows']),timing); r['features'].update({k:f[k] for k in ['H7','N1','Q1']})
    timing['encoding_and_cycle_features']=time.perf_counter()-begin; traces={}; begin=time.perf_counter()
    for m in sorted({r['m'] for r in records}):
        rr=[r for r in records if r['m']==m]; t=pair.pair_refine([(r['id'],matrix(r['relation_rows'])) for r in rr],cfg['resources']['max_refinement_rounds']); traces[str(2*m)]=t
        for r,a in zip(rr,t['rounds'][-1]['matrices']): r['features']['R2']=pair.hist(a)
    timing['R2']=time.perf_counter()-begin; begin=time.perf_counter(); refs=reference(records); timing['reference']=time.perf_counter()-begin
    require(len(refs)==cfg['population']['same_size_pairs'],'pair coverage'); result=summary(records,refs,cfg['pooled_features']['methods'])
    for name,obj in [('records',records),('indexed',encodings),('reconstruction',rebuilt),('rounds',traces),('reference',refs),('summary',result)]: savez(directory/(name+'.json.gz'),obj)
    counts=json.loads(token(result))
    for cell in counts['cells'].values():
        del cell['isomorphism_groups']
        for row in cell['methods'].values(): del row['pairs']
    save(directory/'summary_counts.json',counts); save(directory/'controls.json',controls(records))
    costs={'indexed_directions':[{'id':r['id'],'binary_incidence_entries':r['m']**2,'future_entries':len(e['future']['counts']),'past_entries':len(e['past']['counts']),'future_degree_cap':e['future']['degree_cap'],'past_degree_cap':e['past']['degree_cap']} for r,e in zip(records,encodings)],
        'new_characteristic_polynomials':sum(3+12*r['m'] for r in records if r['family']=='cycles'),
        'reused_previously_verified_feature_records':209,'Pall_integer_payload':sum(pair.integer_count(r['features']['Pall']) for r in records),
        'indexed_subset_and_count_integers':sum(2*(len(e['future']['counts'])+len(e['past']['counts'])) for e in encodings),
        'R2_intermediate_contributions':sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values()),
        'R2_rounds_by_n':{n:t['stabilized_round'] for n,t in traces.items()},'R2_trace_integer_payload':sum(pair.integer_count(a) for t in traces.values() for s in t['rounds'] for a in s['matrices']),
        'warning':'Indexed subsets retain row labels. R2 color numbers require the jointly refined corpus. No standalone-fingerprint or generic compression claim.'}
    save(directory/'costs.json',costs); save(directory/'timing.json',timing)
    print(token({'status':'PRODUCED','orders':len(records),'pairs':len(refs)}),flush=True)

if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
