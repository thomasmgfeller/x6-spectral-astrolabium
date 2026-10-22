"""Budgeted deterministic refinement of unresolved moving-surface cells.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'surface_correlations'))
from sf_run import F,read,save,outward,geometry,setup,OLDUNIT,strip,classify,labels,floor,ceil,rounded,scale,balance,constant,void_bounds

def seed_rectangles(z,selected,n):
    v=z[selected['node']];h=F(selected['step']);box=setup(0)
    ranges=[(F(int(box['low'][j]),OLDUNIT),F(int(box['high'][j]),OLDUNIT)) for j in [1,2]]
    edges=[[a+(b-a)*i/n for i in range(n+1)] for a,b in ranges]
    cut=v[1]+h/2
    if edges[0][0]<cut<edges[0][-1]:edges[0]=sorted(set(edges[0]+[cut]))
    rects=[((a,b),(c,d)) for a,b in zip(edges[0],edges[0][1:]) for c,d in zip(edges[1],edges[1][1:])]
    return [(str(i),side,rect) for i,(side,rect) in enumerate((s,r) for s in [1,-1] for r in rects)]

def split(rect):
    (a,b),(c,d)=rect;x=(a+b)/2;y=(c+d)/2
    return [((a,x),(c,y)),((a,x),(y,d)),((x,b),(c,y)),((x,b),(y,d))]

def evaluate(batch,w,z,ends,selected,unit):
    node=selected['node'];h=F(selected['step']);v=z[node]
    changed=[row[:] for row in z];changed[node][1]+=h
    factor=F(w['rho'])*F(w['scale'])**3;result={}
    for side in [1,-1]:
        group=[row for row in batch if row[1]==side]
        if not group:continue
        lower=[];upper=[];signs=[]
        for key,_,rect in group:
            sign,_,r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lower.append([floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)])
            upper.append([ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)]);signs.append(sign)
        lower=np.array(lower,dtype=np.int64);upper=np.array(upper,dtype=np.int64);forced=np.array(signs)>0
        old0=labels(lower,upper,z,ends,node,side,forced,unit,True)
        old1=labels(lower,upper,changed,ends,node,side,~forced,unit,True)
        for i,(key,_,rect) in enumerate(group):
            surface,thickness=classify(rect,z,ends,node,side,h);merged=[]
            for row,old in zip(surface,[old0,old1]):
                known,bits,outer,possible,_=row
                if known and old[0][i]:assert bits==bytes(old[1][i]).hex()
                if old[0][i]:known=True;bits=bytes(old[1][i]).hex()
                merged.append((known,bits,outer and bool(old[2][i]),possible and bool(old[3][i])))
            (k0,b0,o0,p0),(k1,b1,o1,p1)=merged
            record=dict(id=key,state='unresolved',mass=['0','0'])
            if not o0 or not o1:record['state']='outside'
            elif not(p0 or p1):record['state']='no_affected_interval'
            elif k0 and k1 and b0==b1:record['state']='same_label'
            else:
                area=(rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0])
                record['mass']=[str(x) for x in rounded(scale(thickness,factor*area))]
                if k0 and k1:
                    assert any(bytes.fromhex(b0)) and any(bytes.fromhex(b1))
                    record.update(state='transfer',labels=[b0,b1])
            result[key]=record
    assert len(result)==len(batch)
    return result

def aggregate(leaves,cap):
    table={};unknown=F(0);counts={k:0 for k in ['outside','no_affected_interval','same_label','transfer','unresolved']}
    for cell in leaves.values():
        counts[cell['state']]+=1;lo,hi=map(F,cell['mass'])
        if cell['state']=='unresolved':unknown+=hi
        elif cell['state']=='transfer':
            edge='>'.join(cell['labels']);a,b=table.get(edge,(F(0),F(0)));table[edge]=(a+lo,b+hi)
    total,residual,cancel=balance(table,unknown,cap)
    return dict(leaf_cells=len(leaves),classification=counts,directed_transfer_pairs=len(table),
        exact_unknown_upper=str(unknown),unknown_transfer_mean_upper=outward(unknown)[1],
        localized_changed_mean_upper=outward(total)[1],balanced_residual_mean_upper=outward(residual)[1],
        cancellation_lower=outward(cancel)[0],tv_upper=outward(void_bounds(residual)[1])[1],
        transfers={k:[str(a),str(b)] for k,(a,b) in sorted(table.items())})

def run():
    c=read(HERE/'contract.json')
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    w,z,ends,selected=geometry();cap=constant(w)*F(selected['step'])/2
    seeds=seed_rectangles(z,selected,c['seed_grid']);rectangles={key:(side,rect) for key,side,rect in seeds}
    leaves=evaluate(seeds,w,z,ends,selected,c['coordinate_unit']);archive=dict(leaves)
    base=aggregate(leaves,cap);base.update(round=0,additional_evaluations=0)
    reference=read(HERE.parent/'surface_correlations'/'transfers.json.gz')[-1]
    assert base['classification']==reference['classification']
    assert base['tv_upper']==reference['tv_upper'] and base['transfers']==reference['transfers']
    rounds=[base];splits=[];count=0
    print(json.dumps({k:v for k,v in base.items() if k!='transfers'}),flush=True)
    locked={k:v for k,v in leaves.items() if v['state']!='unresolved'}
    for round_id in range(1,c['rounds']+1):
        keys=sorted((k for k,v in leaves.items() if v['state']=='unresolved'),key=lambda k:(-F(leaves[k]['mass'][1]),k))[:c['parents_per_round']]
        assert keys and count+4*len(keys)<=c['additional_cell_budget']
        batch=[]
        for key in keys:
            side,rect=rectangles[key]
            for i,child in enumerate(split(rect)):
                child_id=key+'/'+str(i);rectangles[child_id]=(side,child);batch.append((child_id,side,child))
        children=evaluate(batch,w,z,ends,selected,c['coordinate_unit']);count+=len(children)
        for key in keys:del leaves[key]
        leaves.update(children);archive.update(children)
        assert all(leaves.get(k)==v for k,v in locked.items())
        locked.update({k:v for k,v in children.items() if v['state']!='unresolved'})
        record=aggregate(leaves,cap);record.update(round=round_id,additional_evaluations=count)
        # New child lower masses may round down, but old known transfers are never replaced.
        assert F(record['cancellation_lower'])>=F(rounds[-1]['cancellation_lower'])
        assert F(record['unknown_transfer_mean_upper'])<=F(rounds[-1]['unknown_transfer_mean_upper'])
        splits.append(dict(round=round_id,parents=keys));rounds.append(record)
        print(json.dumps({k:v for k,v in record.items() if k!='transfers'}),flush=True)
    best=min(rounds,key=lambda r:F(r['tv_upper']));old=rounds[0]
    summary=dict(status='ADAPTIVE_SURFACE_CERTIFIED',pair_unchanged=True,seed_replay_exact=True,
        additional_evaluations=count,budget=c['additional_cell_budget'],best_round=best['round'],
        previous_tv_upper=old['tv_upper'],tv_upper=best['tv_upper'],
        previous_unknown_mean_upper=old['unknown_transfer_mean_upper'],unknown_mean_upper=best['unknown_transfer_mean_upper'],
        cancellation_lower=best['cancellation_lower'],complete_transfer_cells=best['classification']['transfer'],
        unresolved_leaf_cells=best['classification']['unresolved'],directed_transfer_pairs=best['directed_transfer_pairs'],
        all_known_certificates_retained=True,symmetric_operator_gap=selected['relative'],strong_pair_found=False,
        scope='Deterministic refinement of unresolved surface rectangles only; no new geometries, measured TV or reconstruction-accuracy claim. Unresolved intensity remains in the bound.')
    return dict(seed_cells=len(seeds),evaluated_cells=list(archive.values()),splits=splits),rounds,summary

if __name__=='__main__':
    for name,data in zip(['cells.json.gz','rounds.json','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
