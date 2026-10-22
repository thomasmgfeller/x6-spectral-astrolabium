"""Finite larger-shape search with localized Poisson coupling certificates.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'boundary_transfers'))
from bt_run import F,read,save,outward,inputs,void_bounds,constant,boosted,deform,input_record,setup,OLDUNIT,floor,ceil,strip,labels
from sc_run import gap,exact_weights,certify_order,intrinsic_gates

def frame(z,axis,sign):
    """A spatial isometry makes each signed axis displacement a +x move."""
    assert axis in (1,2) and sign in (-1,1)
    return [[row[0],sign*row[axis],row[3-axis]] for row in z]

def rectangles(v,h,axis,sign,n):
    assert h>0 and n>0
    box=setup(0)
    a,b=[F(int(box[k][axis]),OLDUNIT) for k in ('low','high')]
    c,d=[F(int(box[k][3-axis]),OLDUNIT) for k in ('low','high')]
    ranges=[(min(sign*a,sign*b),max(sign*a,sign*b)),(c,d)]
    edges=[[a+(b-a)*i/n for i in range(n+1)] for a,b in ranges]
    cut=v[1]+h/2
    if edges[0][0]<cut<edges[0][-1]:edges[0]=sorted(set(edges[0]+[cut]))
    return [((a,b),(c,d)) for a,b in zip(edges[0],edges[0][1:]) for c,d in zip(edges[1],edges[1][1:])]

def tv_upper(m):
    assert m>=0
    # The inherited alternating-series enclosure is certified on [0,1].
    # Above it, the trivial upper bound is retained (never evaluated out of range).
    return F(1) if m>1 else F(outward(void_bounds(m)[1])[1])

def localize(w,z,zz,ends,node,axis,sign,h,n,unit):
    z=frame(boosted(z),axis,sign);zz=frame(boosted(zz),axis,sign)
    assert zz[node]==[z[node][0],z[node][1]+h,z[node][2]]
    rects=rectangles(z[node],h,axis,sign,n);v=z[node]
    factor=F(w['rho'])*F(w['scale'])**3
    mass=F(0);counts=dict(outside=0,no_affected_interval=0,same_label=0,retained=0)
    for side in (1,-1):
        lows=[];highs=[];signs=[];masses=[]
        for rect in rects:
            s,delta,r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lows.append([floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)])
            highs.append([ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)])
            area=(rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0])
            masses.append(F(outward(factor*area*delta[1],digits=30)[1]));signs.append(s)
        lows=np.array(lows,dtype=np.int64);highs=np.array(highs,dtype=np.int64)
        forced=np.array(signs)>0
        k0,b0,o0,p0,_=labels(lows,highs,z,ends,node,side,forced,unit,True)
        k1,b1,o1,p1,_=labels(lows,highs,zz,ends,node,side,~forced,unit,True)
        for i,m in enumerate(masses):
            if not (o0[i] and o1[i]):counts['outside']+=1
            elif not (p0[i] or p1[i]):counts['no_affected_interval']+=1
            elif k0[i] and k1[i] and np.array_equal(b0[i],b1[i]):counts['same_label']+=1
            else:mass+=m;counts['retained']+=1
    cap=constant(w)*h/2
    m=min(mass,cap)
    return dict(level=n,surface_rectangles=2*len(rects),classification=counts,
                exact_localized_mean_upper=str(mass),exact_global_mean_upper=str(cap),
                exact_changed_mean_upper=str(m),tv_upper=str(tv_upper(m)))

def geometry():
    w,z=inputs();packet,_,_=input_record(w['index']);lookup={v:i for i,v in enumerate(w['nodes'])}
    pairs=[(lookup[a],lookup[b]) for a,b in packet['pairs']]
    ends=[(a,b) if w['full_order'][a][b] else (b,a) for a,b in pairs]
    assert len(ends)==90 and (3,0) in ends
    return w,z,ends

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z,ends=geometry();scale=F(w['scale'])
    base=exact_weights(z,scale);base_gates=intrinsic_gates(z,base,scale)
    rows=[]
    for node in c['moved_nodes']:
      for axis in c['axes']:
       for sign in c['signs']:
        for step in c['steps']:
            h=F(step);zz=deform(z,node,axis,sign,h)
            row=dict(index=len(rows),node=node,axis=axis,sign=sign,step=step)
            rows.append(row)
            try: row['order']=certify_order(zz,w['full_order'])
            except AssertionError:row['status']='ORDER_OR_MARGIN_REJECTED';continue
            try:alt=exact_weights(zz,scale)
            except (StopIteration,ZeroDivisionError):row['status']='RANK_REJECTED';continue
            row.update(status='LAW_BOUND_ABOVE_GATE',**gap(base,alt))
            row['coarse']=localize(w,z,zz,ends,node,axis,sign,h,c['spatial_level'],c['coordinate_unit'])
            row['tv_upper']=row['coarse']['tv_upper']
      print(json.dumps(dict(node=node,completed=len(rows),order_rank_pass=sum('coarse' in r for r in rows))),flush=True)
    assert len(rows)==c['candidate_count']
    ref=c['refinement'];gate=F(c['tv_gate'])
    candidates=[r for r in rows if 'coarse' in r and gate<F(r['tv_upper'])<=F(1,2)]
    candidates=sorted(candidates,key=lambda r:(-F(r['relative'][0]),r['index']))[:ref['maximum_candidates']]
    for row in candidates:
        zz=deform(z,row['node'],row['axis'],row['sign'],F(row['step']))
        row['refined']=localize(w,z,zz,ends,row['node'],row['axis'],row['sign'],F(row['step']),ref['level'],c['coordinate_unit'])
        row['tv_upper']=str(min(F(row['tv_upper']),F(row['refined']['tv_upper'])))
        print(json.dumps(dict(refined=row['index'],tv_upper=row['tv_upper'])),flush=True)
    eligible=[]
    for row in rows:
        if 'tv_upper' not in row or F(row['tv_upper'])>gate:continue
        zz=deform(z,row['node'],row['axis'],row['sign'],F(row['step']))
        alt=exact_weights(zz,scale)
        try:row['intrinsic_gates']=intrinsic_gates(zz,alt,scale)
        except (AssertionError,StopIteration,ZeroDivisionError):row['status']='CONDITIONING_REJECTED';continue
        row['status']='ALL_GATES_CERTIFIED';eligible.append(row)
    assert eligible
    selected=max(eligible,key=lambda r:(F(r['relative'][0]),-r['index']))
    zz=deform(z,selected['node'],selected['axis'],selected['sign'],F(selected['step']))
    witness=dict(selected_row=selected['index'],coordinates=[[str(v) for v in p] for p in zz],
                 exact_weight_vectors=[[str(v) for v in a] for a in (base,exact_weights(zz,scale))])
    threshold=F(c['strong_gap_gate'])
    strong=F(selected['relative'][0])>threshold
    assert not any(F(r['relative'][0])<=threshold<=F(r['relative'][1]) for r in eligible)
    old=read(HERE.parent/'shape_coupling'/'summary.json')['selected']
    best_geometry=max((r for r in rows if 'relative' in r),key=lambda r:F(r['relative'][0]))
    summary=dict(status='STRONG_PAIR_FOUND' if strong else 'NO_CERTIFIED_STRONG_PAIR_IN_FIXED_SPATIAL_SEARCH',
      candidates=len(rows),order_rank_pass=sum('coarse' in r for r in rows),refined_indices=[r['index'] for r in candidates],
      all_gates_pass=len(eligible),selected=selected,base_intrinsic_gates=base_gates,
      strongest_order_rank_candidate=dict(index=best_geometry['index'],relative=best_geometry['relative'],tv_upper=best_geometry['tv_upper'],status=best_geometry['status']),
      previous_symmetric_gap=old['relative'],gap_gain_lower=outward(F(selected['relative'][0])/F(old['relative'][1]))[0],
      strong_pair_found=strong,
      scope='Finite single-node spatial family at a fixed base. Known density, fixed selected-node order/landmarks/root/outer domain; complete 90-count and overlap channel. TV upper bounds above the gate are inconclusive, not distinguishability certificates. No continuous-family exclusion, global stability or physical accuracy claim.')
    return rows,witness,summary

if __name__=='__main__':
    for name,data in zip(('candidates.json.gz','witness.json','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
