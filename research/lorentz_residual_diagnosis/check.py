"""Countercheck using explicit incidence sums and intersections of color classes.

No import of the new producer. Frozen predecessor solvers recheck the known target.
"""
from collections import Counter
import copy
import importlib.util
from itertools import combinations
import json
from pathlib import Path

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[1]
METHODS=['H7+N1+Q1','I2','I3','R2']+[p+k for p in ['H7+N1+','H7+N1+Q1+'] for k in ['I2','I3','R2']]


def require(ok, why):
    if not ok:
        raise ValueError(why)


def match(a,b,why):
    require(json.dumps(a,sort_keys=True)==json.dumps(b,sort_keys=True),why)


def save(path,obj):
    path.write_text(json.dumps(obj,indent=2)+'\n')


def incidence(lines, cubic=True):
    n=len(lines)
    require(all(len(row)==n and set(row)<={'0','1'} for row in lines),'binary square relation')
    c=[[int(x) for x in row] for row in lines]
    incoming=[{u for u in range(n) if c[u][v]} for v in range(n)]
    outgoing=[{v for v in range(n) if c[u][v]} for u in range(n)]
    low=[v for v in range(n) if not incoming[v] and outgoing[v]]
    up=[v for v in range(n) if incoming[v] and not outgoing[v]]
    require(sorted(low+up)==list(range(n)),'strict height-two layers')
    require(all(outgoing[v]<=set(up) for v in low),'height-two edges')
    if cubic:
        require(len(low)==len(up) and all(len(outgoing[v])==3 for v in low) and all(len(incoming[v])==3 for v in up),'cubic regularity')
    return c,low,up


def intersections(c):
    n=len(c); low=[v for v in range(n) if not any(c[u][v] for u in range(n))]
    up=[v for v in range(n) if not any(c[v])]; pairs=[]; triples=[]
    for roots,future in [(low,True),(up,False)]:
        relation=lambda u,w: c[u][w] if future else c[w][u]
        pairs.append(sorted(sum(relation(u,w)*relation(v,w) for w in range(n)) for u,v in combinations(roots,2)))
        items=[]
        for group in combinations(roots,3):
            overlap=sorted(sum(relation(u,w)*relation(v,w) for w in range(n)) for u,v in combinations(group,2))
            common=sum(all(relation(u,w) for u in group) for w in range(n))
            items.append(overlap+[common])
        triples.append(sorted(items))
    return {'I2':pairs,'I3':triples}


def assign(values):
    vocabulary=sorted(set(x for graph in values for row in graph for x in row))
    indices=dict(zip(vocabulary,range(len(vocabulary))))
    return [[[indices[x] for x in row] for row in graph] for graph in values],len(vocabulary)


def refine_step(colors):
    n=len(colors[0])
    signatures=[]
    for color in colors:
        outgoing=[]; incoming=[]
        for v in range(n):
            a={}; b={}
            for w in range(n):
                a.setdefault(color[v][w],set()).add(w)
                b.setdefault(color[w][v],set()).add(w)
            outgoing.append(a); incoming.append(b)
        graph=[]
        for u in range(n):
            row=[]
            for v in range(n):
                terms=[]
                for a,aa in sorted(outgoing[u].items()):
                    for b,bb in sorted(incoming[v].items()):
                        terms.extend([(a,b)]*len(aa.intersection(bb)))
                require(len(terms)==n,'joint color count')
                row.append((color[u][v],tuple(terms)))
            graph.append(row)
        signatures.append(graph)
    return assign(signatures)


def refine(graphs,maximum=200):
    n=len(graphs[0][1]); initial=[]
    for name,c in graphs:
        degree=[(sum(c[w][v] for w in range(n)),sum(c[v][w] for w in range(n))) for v in range(n)]
        initial.append([[degree[u]+degree[v]+(int(u==v),c[u][v],c[v][u]) for v in range(n)] for u in range(n)])
    colors,size=assign(initial); rounds=[{'round':0,'colors':size,'matrices':colors}]
    for step in range(1,maximum+1):
        new,count=refine_step(colors)
        require(count>=size,'nonmonotone refinement')
        rounds.append({'round':step,'colors':count,'matrices':new})
        if count==size:
            return {'n':n,'ids':[name for name,_ in graphs],'rounds':rounds,'stabilized_round':step}
        colors,size=new,count
    raise ValueError('INCONCLUSIVE: no stability inside fixed round budget')


def histogram(a):
    values=sorted(x for row in a for x in row)
    return [[x,values.count(x)] for x in sorted(set(values))]


def vertex_control(c):
    n=len(c); colors=[(sum(c[w][v] for w in range(n)),sum(c[v])) for v in range(n)]
    for _ in range(3):
        colors=[(colors[v],tuple(sorted(colors[w] for w in range(n) if c[w][v])),tuple(sorted(colors[w] for w in range(n) if c[v][w]))) for v in range(n)]
        require(len(set(colors))==2,'vertex color-control unexpectedly split regular layers')
    return True


def summary(records):
    cells={}
    for m in sorted({r['m'] for r in records}):
        rr=[r for r in records if r['m']==m]; methods={}
        for method in METHODS:
            keys=method.split('+')
            equal=lambda a,b: all(a['features'][k]==b['features'][k] for k in keys)
            pending=list(rr); groups=[]
            while pending:
                first=pending[0]; group=[r for r in pending if equal(first,r)]
                groups.append(group); pending=[r for r in pending if not equal(first,r)]
            methods[method]={'classes':len(groups),'unresolved_pairs':sum(equal(a,b) for a,b in combinations(rr,2)),
                             'max_class_size':max(map(len,groups)),'residual_groups':sorted(sorted(r['id'] for r in g) for g in groups if len(g)>1)}
        cells[str(m)]={'n':2*m,'orders':len(rr),'same_size_pairs':len(list(combinations(rr,2))),'methods':methods}
    return {'schema':'x6.residual-summary/1','cells':cells,'scope':'Retrospective existing corpus; equal features never certify identity.'}


def validate(actual,expected,trace,expected_trace,result,expected_summary):
    match(actual,expected,'features or representative coverage mismatch')
    match(trace,expected_trace,'R2 trace mismatch')
    match(result,expected_summary,'summary mismatch')


def load_module(name,path):
    spec=importlib.util.spec_from_file_location(name,path); module=importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def target_reference(raw,ids):
    producer=load_module('frozen_stress_producer',HERE.parent/'lorentz_n1_stress/produce.py')
    checker=load_module('frozen_stress_checker',HERE.parent/'lorentz_n1_stress/check.py')
    rr=[next(r for r in raw if r['id']==name) for name in ids]
    cc=[]
    for r in rr:
        c,_,_=incidence(r['relation_rows']); cc.append(c)
        p=producer.prior.features(c,{k:0.0 for k in ['H7','D','M11','N1','Q1']}); q=checker.prior.compute(c)
        match({k:p[k] for k in ['H7','N1','Q1']},r['features'],'target producer spectral recheck')
        match({k:q[k] for k in ['H7','N1','Q1']},r['features'],'target checker spectral recheck')
    match(rr[0]['features'],rr[1]['features'],'target is original complete feature collision')
    a,b=cc; dual=[list(row) for row in zip(*b)]; m=len(b)//2
    # The frozen row/column solver expects its lower layer first.
    p=list(range(m,2*m))+list(range(m)); ordered_dual=[[dual[i][j] for j in p] for i in p]
    tests={'producer_nonisomorphic':not producer.iso(a,b),'checker_nonisomorphic':not checker.iso(a,b),
           'producer_nondual':not producer.iso(a,dual),'checker_nondual':not checker.iso(a,ordered_dual)}
    require(all(tests.values()),'target identity/duality reference')
    return {**tests,'two_arithmetic_paths':True,'characteristic_polynomials_per_path':2*(3+6*len(a))}


def witness(records,traces,ids):
    a,b=[next(r for r in records if r['id']==name) for name in ids]; out={'ids':ids,'separated':{},'intersection_differences':{}}
    for key in ['I2','I3','R2']:
        out['separated'][key]=a['features'][key]!=b['features'][key]
    for key in ['I2','I3']:
        differences={}
        for direction,index in [('future',0),('past',1)]:
            encode=lambda x: (x,) if type(x) is int else tuple(x)
            ca=Counter(encode(x) for x in a['features'][key][index]); cb=Counter(encode(x) for x in b['features'][key][index])
            differences[direction]=[{'entry':list(x),'first_count':ca[x],'second_count':cb[x]} for x in sorted(set(ca)|set(cb)) if ca[x]!=cb[x]]
        out['intersection_differences'][key]=differences
    trace=traces[str(a['m'])]; ia,ib=[trace['ids'].index(name) for name in ids]
    first=next((r for r in trace['rounds'] if histogram(r['matrices'][ia])!=histogram(r['matrices'][ib])),None)
    out['R2_first_distinguishing_round']=None if first is None else first['round']
    if first:
        ha=dict(histogram(first['matrices'][ia])); hb=dict(histogram(first['matrices'][ib])); color=next(k for k in sorted(set(ha)|set(hb)) if ha.get(k,0)!=hb.get(k,0))
        out['R2_witness_color']={'context':'m=8 corpus; reconstruct exact color signatures from the preceding round in rounds.json',
                                  'round':first['round'],'color':color,'first_count':ha.get(color,0),'second_count':hb.get(color,0)}
    return out


def run(directory):
    cfg=json.loads((HERE/'contract.json').read_text()); raw=[json.loads(s) for s in (ROOT/cfg['input']['records']).read_text().splitlines()]
    require(len(raw)==cfg['input']['representatives'] and len({r['id'] for r in raw})==len(raw),'reference count')
    expected=[]; traces={}
    for r in raw:
        c,low,up=incidence(r['relation_rows']); require(len(low)==r['m'],'cell size'); vertex_control(c)
        expected.append({'id':r['id'],'m':r['m'],'features':{**r['features'],**intersections(c)}})
    for m in sorted({r['m'] for r in raw}):
        graphs=[(r['id'],incidence(r['relation_rows'])[0]) for r in raw if r['m']==m]
        require(len(graphs)==cfg['input']['cells'][str(m)],'fixed cell coverage')
        trace=refine(graphs,cfg['resources']['max_refinement_rounds']); traces[str(m)]=trace
        for name,a in zip(trace['ids'],trace['rounds'][-1]['matrices']):
            next(r for r in expected if r['id']==name)['features']['R2']=histogram(a)
        p=list(reversed(range(2*m))); moved=[(name,[[c[u][v] for v in p] for u in p]) for name,c in graphs]
        second=refine(moved,cfg['resources']['max_refinement_rounds'])
        require(second['stabilized_round']==trace['stabilized_round'],'relabelled stabilization')
        for step,other in zip(trace['rounds'],second['rounds']):
            match(step['colors'],other['colors'],'relabelled palette')
            for a,b in zip(step['matrices'],other['matrices']):
                match([[a[u][v] for v in p] for u in p],b,'every pair color transport')
        for (_,a),(_,b) in zip(graphs,moved):
            match(intersections(a),intersections(b),'relabelled intersection features')
        print(json.dumps({'phase':'checker','m':m,'orders':len(graphs),'rounds':trace['stabilized_round']}),flush=True)
    actual=[json.loads(s) for s in (directory/'features.jsonl').read_text().splitlines()]
    baseline={r['id']:r for r in raw}
    for r in actual:
        require(r['id'] in baseline and set(r['features'])=={'I2','I3','R2'},'feature encoding')
        r['features']={**baseline[r['id']]['features'],**r['features']}
    trace=json.loads((directory/'rounds.json').read_text()); result=json.loads((directory/'summary.json').read_text()); expected_summary=summary(expected)
    validate(actual,expected,trace,traces,result,expected_summary)
    rejected=[]
    def reject(name,fn):
        try: fn()
        except ValueError: rejected.append(name)
        else: raise ValueError('accepted negative control '+name)
    bad=list(raw[0]['relation_rows']);bad[0]='1'+bad[0][1:]
    reject('self_loop',lambda:incidence(bad))
    bad=copy.deepcopy(actual);bad[0]['features']['I3'][0][0][0]+=1
    reject('altered_triple_intersection',lambda:validate(bad,expected,trace,traces,result,expected_summary))
    bad=copy.deepcopy(actual);bad[0]['features']['I2'][0].pop()
    reject('lost_multiplicity',lambda:validate(bad,expected,trace,traces,result,expected_summary))
    reject('omitted_representative',lambda:validate(actual[1:],expected,trace,traces,result,expected_summary))
    bad=copy.deepcopy(trace);bad['6']['rounds'][0]['matrices'][0][0][0]+=1
    reject('corrupted_pair_trace',lambda:validate(actual,expected,bad,traces,result,expected_summary))
    bad=copy.deepcopy(result);bad['cells']['6']['methods']['I2']['residual_groups']=[['forged']]
    reject('omitted_residual_summary',lambda:validate(actual,expected,trace,traces,bad,expected_summary))
    # Check the exact logical cost ledger independently from feature generation.
    payload=lambda x: 1 if type(x) is int else sum(payload(y) for y in x)
    costs=json.loads((directory/'costs.json').read_text())
    for key in ['I2','I3','R2']:
        require(costs[key]['characteristic_polynomial_calls']==0,'new-feature polynomial cost')
        require(costs[key]['integer_payload']==sum(payload(r['features'][key]) for r in expected),'integer payload ledger')
    require(costs['I2']['pair_intersection_evaluations']==sum(2*len(list(combinations(range(r['m']),2))) for r in expected),'I2 cost')
    triples=sum(2*len(list(combinations(range(r['m']),3))) for r in expected)
    require(costs['I3']['triple_intersection_evaluations']==triples and costs['I3']['pair_intersection_evaluations']==3*triples,'I3 cost')
    match(costs['R2']['rounds_by_m'],{m:t['stabilized_round'] for m,t in traces.items()},'round ledger')
    require(costs['R2']['intermediate_vertex_contributions']==sum(len(t['ids'])*t['n']**3*t['stabilized_round'] for t in traces.values()),'R2 cost')
    require(costs['R2']['round_trace_integer_payload']==sum(payload(a) for t in traces.values() for step in t['rounds'] for a in step['matrices']),'trace cost')
    target=target_reference(raw,cfg['input']['target_ids']); proof=witness(expected,traces,cfg['input']['target_ids'])
    save(directory/'target.json',proof)
    save(directory/'verification.json',{'status':'PASS_EXACT_DIAGNOSIS','representatives':len(raw),'all_round_matrices_compared':True,
        'relabelled_representatives':len(raw),'vertex_refinement_control_rounds':3,'negative_controls_rejected':rejected,
        'target_reference':target,'scope':'Two implementations in one authoring process; retrospective corpus, no external review.'})


if __name__=='__main__':
    import sys
    run(Path(sys.argv[1]))
