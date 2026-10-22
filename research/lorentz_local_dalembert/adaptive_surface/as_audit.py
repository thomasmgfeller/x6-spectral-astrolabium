"""Partition-tree, retained-certificate and independent causal-membership audit.
SPDX-License-Identifier: Apache-2.0
"""
from as_run import *
from itertools import product
sys.path.insert(0,str(HERE.parent/'surface_correlations'))
from sf_audit import point_bits,sqrt_bounds

def reconstruct(seed_map,key):
    parts=key.split('/');side,rect=seed_map[parts[0]]
    for digit in parts[1:]:
        assert digit in ['0','1','2','3'];i=int(digit)
        (a,b),(c,d)=rect;x=(a+b)/2;y=(c+d)/2
        rect=((x,b) if i>=2 else (a,x),(y,d) if i%2 else (c,y))
    return side,rect

def check_tree(data,c,seeds):
    cells={r['id']:r for r in data['evaluated_cells']};assert len(cells)==len(data['evaluated_cells'])
    seed_map={key:(side,rect) for key,side,rect in seeds};leaves={k:cells[k] for k in seed_map};used=set(leaves)
    assert data['seed_cells']==len(seeds)
    stages=[dict(leaves)];evaluations=0
    for round_id,action in enumerate(data['splits'],1):
        assert action['round']==round_id
        expected=sorted((k for k,v in leaves.items() if v['state']=='unresolved'),key=lambda k:(-F(leaves[k]['mass'][1]),k))[:c['parents_per_round']]
        assert action['parents']==expected
        locked={k:v for k,v in leaves.items() if v['state']!='unresolved'}
        for key in action['parents']:
            assert leaves[key]['state']=='unresolved';del leaves[key]
            side,rect=reconstruct(seed_map,key);parent_area=(rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0]);child_area=F(0)
            for i in range(4):
                child=key+'/'+str(i);assert child in cells and child not in used
                s,r=reconstruct(seed_map,child);assert s==side
                child_area+=(r[0][1]-r[0][0])*(r[1][1]-r[1][0])
                leaves[child]=cells[child];used.add(child);evaluations+=1
            assert child_area==parent_area
        assert all(leaves.get(k)==v for k,v in locked.items())
        stages.append(dict(leaves))
    assert used==set(cells) and evaluations<=c['additional_cell_budget']
    assert len(data['splits'])==c['rounds']
    return stages,seed_map,evaluations

def audit():
    c=read(HERE/'contract.json');w,z,ends,selected=geometry();seeds=seed_rectangles(z,selected,c['seed_grid'])
    data=read(HERE/'cells.json.gz');rounds=read(HERE/'rounds.json');stages,seed_map,evaluations=check_tree(data,c,seeds)
    for leaves,record in zip(stages,rounds):
        unknown=sum(F(v['mass'][1]) for v in leaves.values() if v['state']=='unresolved')
        table={};incoming={};outgoing={}
        for cell in leaves.values():
            lo,hi=map(F,cell['mass']);assert 0<=lo<=hi
            if cell['state']=='transfer':
                a,b=cell['labels'];assert a!=b;edge=a+'>'+b
                x,y=table.get(edge,(F(0),F(0)));table[edge]=(x+lo,y+hi)
                incoming[b]=incoming.get(b,F(0))+lo;outgoing[a]=outgoing.get(a,F(0))+lo
        C=sum(min(incoming.get(k,F(0)),outgoing.get(k,F(0))) for k in incoming.keys()|outgoing.keys())
        assert str(unknown)==record['exact_unknown_upper'] and outward(C)[0]==record['cancellation_lower']
        assert {k:[str(a),str(b)] for k,(a,b) in table.items()}==record['transfers']
        assert len(leaves)==record['leaf_cells']
    # The tree check must reject an omitted child and a dropped refinement round.
    first=data['splits'][0]['parents'][0]+'/0'
    malformed=[dict(data,evaluated_cells=[r for r in data['evaluated_cells'] if r['id']!=first]),dict(data,splits=data['splits'][:-1])]
    for bad in malformed:
        try:check_tree(bad,c,seeds)
        except (AssertionError,KeyError):continue
        raise AssertionError('incomplete partition accepted')
    # Stratified deterministic sample of NEW known leaves, both directions and depths.
    final=stages[-1];groups={}
    for key,cell in final.items():
        if cell['state']=='transfer' and '/' in key:
            side,_=reconstruct(seed_map,key);groups.setdefault((side,key.count('/')),[]).append(key)
    keys=[]
    for group in sorted(groups):
        ordered=sorted(groups[group]);keys+=ordered[:8]
    node=selected['node'];h=F(selected['step']);v=z[node]
    changed=[row[:] for row in z];changed[node][1]+=h;checks=0
    for key in keys:
        side,rect=reconstruct(seed_map,key)
        for fx,fy,u in product([F(1,4),F(1,2),F(3,4)],repeat=3):
            X=[a+f*(b-a) for (a,b),f in zip(rect,[fx,fy])]
            roots=[sqrt_bounds(sum((a-b)**2 for a,b in zip(X,tip[1:]))) for tip in [v,changed[node]]]
            radius=(1-u)*sum(roots[0])/2+u*sum(roots[1])/2
            point=[v[0]+side*radius,*X]
            assert [point_bits(point,g,ends) for g in [z,changed]]==final[key]['labels'];checks+=1
    assert rounds[-1]['tv_upper']<rounds[0]['tv_upper']
    return dict(status='PASS',seed_cells=len(seeds),new_evaluations=evaluations,
        exact_partition_and_priority=True,all_known_certificates_retained=True,negative_partition_controls=2,
        new_known_leaf_samples=len(keys),independent_scalar_membership_points=checks,
        mass_and_cancellation_ledger_reconstructed=True,
        scope='Deterministic coverage and interval certificates; point audits do not replace the whole-cell proof. Refinement does not add observations or new geometries.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
