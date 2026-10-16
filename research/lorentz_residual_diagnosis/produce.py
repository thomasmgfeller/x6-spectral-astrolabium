"""Fixed retrospective intersection and directed pair-refinement diagnosis."""
from collections import Counter, defaultdict
from itertools import combinations
import json
from pathlib import Path
import time

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
METHODS = ['H7+N1+Q1', 'I2', 'I3', 'R2'] + [prefix+k for prefix in ['H7+N1+', 'H7+N1+Q1+'] for k in ['I2','I3','R2']]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def token(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'))


def save(path, obj):
    path.write_text(json.dumps(obj, indent=2)+'\n')


def degrees(c):
    return [(sum(c[i][v] for i in range(len(c))), sum(c[v])) for v in range(len(c))]


def layers(c):
    n=len(c); d=degrees(c)
    require(all(len(row)==n and all(x in (0,1) for x in row) for row in c), 'binary square relation')
    low=[i for i in range(n) if d[i][0]==0 and d[i][1]>0]
    up=[i for i in range(n) if d[i][1]==0 and d[i][0]>0]
    require(len(low)+len(up)==n and not set(low)&set(up), 'two disjoint nonempty degree layers')
    require(all(not c[i][j] or (i in low and j in up) for i in range(n) for j in range(n)), 'strict height-two relation')
    return low,up


def intersections(c, size):
    low,up=layers(c); result=[]
    for roots,neighbors,future in [(low,up,True),(up,low,False)]:
        masks={v:sum(1<<w for w in neighbors if (c[v][w] if future else c[w][v])) for v in roots}
        items=[]
        for group in combinations(roots,size):
            if size==2:
                items.append((masks[group[0]]&masks[group[1]]).bit_count())
            else:
                a,b,d=(masks[v] for v in group)
                items.append(sorted([(a&b).bit_count(),(a&d).bit_count(),(b&d).bit_count()])+[(a&b&d).bit_count()])
        result.append(sorted(items))
    return result


def compress(signatures):
    palette={s:i for i,s in enumerate(sorted({s for graph in signatures for row in graph for s in row}))}
    return [[[palette[s] for s in row] for row in graph] for graph in signatures],len(palette)


def refine_step(colors,marginal=False):
    n=len(colors[0]); signatures=[]
    for c in colors:
        if marginal:
            signatures.append([[(c[u][v],tuple(sorted(c[u])),tuple(sorted(c[w][v] for w in range(n)))) for v in range(n)] for u in range(n)])
        else:
            signatures.append([[(c[u][v],tuple(sorted((c[u][w],c[w][v]) for w in range(n)))) for v in range(n)] for u in range(n)])
    return compress(signatures)


def pair_refine(graphs, maximum=200, marginal=False):
    n=len(graphs[0][1]); init=[]
    for _,c in graphs:
        d=degrees(c)
        init.append([[(*d[u],*d[v],int(u==v),c[u][v],c[v][u]) for v in range(n)] for u in range(n)])
    colors,k=compress(init); history=[{'round':0,'colors':k,'matrices':colors}]
    for step in range(1,maximum+1):
        new,new_k=refine_step(colors,marginal)
        require(new_k>=k,'refinement must not merge colors')
        history.append({'round':step,'colors':new_k,'matrices':new})
        if new_k==k:
            return {'n':n,'ids':[name for name,_ in graphs],'rounds':history,'stabilized_round':step}
        colors,k=new,new_k
    raise ValueError('INCONCLUSIVE: refinement round cap')


def hist(matrix):
    return [[k,v] for k,v in sorted(Counter(x for row in matrix for x in row).items())]


def integer_count(x):
    return 1 if type(x) is int else sum(integer_count(v) for v in x)


def summary(records):
    cells={}
    for m in sorted({r['m'] for r in records}):
        rr=[r for r in records if r['m']==m]; methods={}
        for method in METHODS:
            groups=defaultdict(list)
            for r in rr:
                groups[token([r['features'][f] for f in method.split('+')])].append(r['id'])
            residual=sorted(sorted(g) for g in groups.values() if len(g)>1)
            methods[method]={'classes':len(groups),'unresolved_pairs':sum(len(g)*(len(g)-1)//2 for g in residual),
                             'max_class_size':max(map(len,groups.values())),'residual_groups':residual}
        cells[str(m)]={'n':2*m,'orders':len(rr),'same_size_pairs':len(rr)*(len(rr)-1)//2,'methods':methods}
    return {'schema':'x6.residual-summary/1','cells':cells,'scope':'Retrospective existing corpus; equal features never certify identity.'}


def run(directory):
    directory.mkdir(parents=True,exist_ok=False)
    cfg=json.loads((HERE/'contract.json').read_text())
    raw=[json.loads(s) for s in (ROOT/cfg['input']['records']).read_text().splitlines()]
    records=[]; timing={'I2':0.0,'I3':0.0,'R2_by_m':{}}; traces={}
    for r in raw:
        c=[[int(x) for x in line] for line in r['relation_rows']]; f=dict(r['features'])
        for k,size in [('I2',2),('I3',3)]:
            start=time.perf_counter(); f[k]=intersections(c,size); timing[k]+=time.perf_counter()-start
        records.append({'id':r['id'],'m':r['m'],'features':f})
    for m in sorted({r['m'] for r in raw}):
        graphs=[(r['id'],[[int(x) for x in row] for row in r['relation_rows']]) for r in raw if r['m']==m]
        start=time.perf_counter(); trace=pair_refine(graphs,cfg['resources']['max_refinement_rounds']); elapsed=time.perf_counter()-start
        traces[str(m)]=trace; timing['R2_by_m'][str(m)]=elapsed
        lookup={name:hist(a) for name,a in zip(trace['ids'],trace['rounds'][-1]['matrices'])}
        for r in records:
            if r['m']==m:
                r['features']['R2']=lookup[r['id']]
        print(token({'phase':'producer','m':m,'orders':len(graphs),'rounds':trace['stabilized_round']}),flush=True)
    (directory/'features.jsonl').write_text(''.join(token({'id':r['id'],'m':r['m'],'features':{k:r['features'][k] for k in ['I2','I3','R2']}})+'\n' for r in records))
    (directory/'rounds.json').write_text(token(traces)+'\n'); save(directory/'summary.json',summary(records))
    costs={k:{'characteristic_polynomial_calls':0,'integer_payload':sum(integer_count(r['features'][k]) for r in records)} for k in ['I2','I3','R2']}
    costs['I2']['pair_intersection_evaluations']=sum(2*(r['m']*(r['m']-1)//2) for r in records)
    costs['I3']['pair_intersection_evaluations']=sum(6*(r['m']*(r['m']-1)*(r['m']-2)//6) for r in records)
    costs['I3']['triple_intersection_evaluations']=sum(2*(r['m']*(r['m']-1)*(r['m']-2)//6) for r in records)
    costs['R2']['intermediate_vertex_contributions']=sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values())
    costs['R2']['rounds_by_m']={m:t['stabilized_round'] for m,t in traces.items()}
    costs['R2']['round_trace_integer_payload']=sum(sum(integer_count(a) for a in step['matrices']) for t in traces.values() for step in t['rounds'])
    costs['R2']['context']='Histogram IDs require the jointly refined corpus and reconstruction of exact color signatures; not a portable standalone fingerprint.'
    save(directory/'costs.json',costs); save(directory/'timing.json',timing)


if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
