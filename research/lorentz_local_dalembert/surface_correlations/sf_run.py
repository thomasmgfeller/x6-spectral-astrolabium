"""Cone membership certified on a moving cone strip with time-space correlation.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'boundary_transfers'))
from bt_run import F,read,save,outward,sqrt_bounds,inputs,void_bounds,constant,boosted,deform,input_record,setup,OLDUNIT,strip,radial_bounds,balance,labels,floor,ceil

def add(a,b):return a[0]+b[0],a[1]+b[1]
def mul(a,b):
    v=[x*y for x in a for y in b];return min(v),max(v)
def scale(a,c):return mul(a,(c,c))
def square(a):return (F(0) if a[0]<=0<=a[1] else min(x*x for x in a),max(x*x for x in a))
def rounded(a):return tuple(map(F,outward(*a,digits=30)))

def surface_cones(rect,v,w,side,r,e):
    """t=v_t+side*(r0+e), r0=|X-v_space|. e is signed strip offset."""
    dt=v[0]-w[0]
    time=add((dt,dt),scale(add(r,e),side))
    # Cancel r0^2 against spatial quadratic terms before interval evaluation.
    q=(dt*dt+sum(x*x-y*y for x,y in zip(v[1:],w[1:])),)*2
    for interval,a,b in zip(rect,v[1:],w[1:]):q=add(q,scale(interval,2*(b-a)))
    q=add(q,scale(r,2*side*dt))
    q=add(q,scale(e,2*side*dt))
    q=add(q,scale(mul(r,e),2));q=add(q,square(e))
    states=[]
    for kind in [1,-1]:
        signed=scale(time,kind)
        inside=signed[0]>0 and q[0]>0
        possible=signed[1]>0 and q[1]>0
        assert not inside or possible
        states.append((inside,possible))
    return states,q,time

def classify(rect,z,ends,node,side,h):
    v=z[node];sign,thickness,_=strip(rect,v[1:],h)
    r=radial_bounds(rect,v[1:]);e=(F(0),thickness[1]) if sign>0 else (-thickness[1],F(0))
    future=[];past=[]
    for i,w in enumerate(z):
        if i==node:
            # Active cone is imposed separately for the two geometries; opposite false.
            future.append((False,False));past.append((False,False));continue
        states,_,_=surface_cones(rect,v,w,side,r,e)
        future.append(states[0]);past.append(states[1])
    results=[]
    for base in [True,False]:
        f=future.copy();p=past.copy();active=(sign>0)==base
        (f if side==1 else p)[node]=(active,active)
        inner=[f[a][0] and p[b][0] for a,b in ends]
        outer=[f[a][1] and p[b][1] for a,b in ends]
        known=inner==outer
        bits=np.packbits(np.array(inner,dtype=bool),bitorder='little').tobytes().hex()
        affected=[i for i,(a,b) in enumerate(ends) if (a==node if side==1 else b==node)]
        possible=any(outer[i] for i in affected)
        results.append((known,bits,outer[ends.index((3,0))],possible,[a!=b for a,b in zip(inner,outer)]))
    return results,thickness

def integrate(w,z,ends,selected,n):
    h=F(selected['step']);node=selected['node'];v=z[node];box=setup(0)
    ranges=[(F(int(box['low'][j]),OLDUNIT),F(int(box['high'][j]),OLDUNIT)) for j in [1,2]]
    edges=[[a+(b-a)*i/n for i in range(n+1)] for a,b in ranges]
    cut=v[1]+h/2
    if edges[0][0]<cut<edges[0][-1]:edges[0]=sorted(set(edges[0]+[cut]))
    rects=[((a,b),(c,d)) for a,b in zip(edges[0],edges[0][1:]) for c,d in zip(edges[1],edges[1][1:])]
    factor=F(w['rho'])*F(w['scale'])**3
    transfers={};unknown=F(0);counts={'outside':0,'no_affected_interval':0,'same_label':0,'transfer':0,'unresolved':0}
    ambiguities=[0]*len(ends);witnesses=[];witness_counts={1:0,-1:0}
    unit=262144
    changed=[row[:] for row in z];changed[node][1]+=h
    for side in [1,-1]:
        lower=[];upper=[];signs=[]
        for rect in rects:
            sign,_,r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lower.append([floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)])
            upper.append([ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)])
            signs.append(sign)
        lower=np.array(lower,dtype=np.int64);upper=np.array(upper,dtype=np.int64);forced=np.array(signs)>0
        old0=labels(lower,upper,z,ends,node,side,forced,unit,True)
        old1=labels(lower,upper,changed,ends,node,side,~forced,unit,True)
        for i,rect in enumerate(rects):
            results,thickness=classify(rect,z,ends,node,side,h)
            merged=[]
            for result,old in zip(results,[old0,old1]):
                known,bits,outer,possible,uncertain=result
                if known and old[0][i]:assert bits==bytes(old[1][i]).hex()
                if old[0][i]:known=True;bits=bytes(old[1][i]).hex()
                merged.append((known,bits,outer and bool(old[2][i]),possible and bool(old[3][i]),uncertain))
            (k0,b0,o0,p0,u0),(k1,b1,o1,p1,u1)=merged
            if not o0 or not o1:counts['outside']+=1;continue
            if not(p0 or p1):counts['no_affected_interval']+=1;continue
            area=(rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0])
            lo,hi=rounded(scale(thickness,factor*area))
            if k0 and k1:
                if b0==b1:counts['same_label']+=1;continue
                assert any(bytes.fromhex(b0)) and any(bytes.fromhex(b1))
                counts['transfer']+=1;key=b0+'>'+b1
                if witness_counts[side]<16:
                    witnesses.append(dict(side=side,rect=[[str(x) for x in interval] for interval in rect],labels=[b0,b1]))
                    witness_counts[side]+=1
                a,b=transfers.get(key,(F(0),F(0)));transfers[key]=(a+lo,b+hi)
            else:
                unknown+=hi;counts['unresolved']+=1
                ambiguities=[x+int(a or b) for x,a,b in zip(ambiguities,u0,u1)]
    total,residual,cancel=balance(transfers,unknown,constant(w)*h/2)
    return dict(level=n,surface_rectangles=2*len(rects),classification=counts,
        ambiguous_intervals=[dict(endpoints=list(ends[i]),cells=ambiguities[i]) for i in sorted(range(len(ends)),key=lambda i:-ambiguities[i])[:5] if ambiguities[i]],
        known_cell_witnesses=witnesses,
        directed_transfer_pairs=len(transfers),exact_unknown_upper=str(unknown),
        unknown_transfer_mean_upper=outward(unknown)[1],localized_changed_mean_upper=outward(total)[1],
        balanced_residual_mean_upper=outward(residual)[1],certified_cancellation_lower=outward(cancel)[0],
        localization_tv_upper=outward(void_bounds(total)[1])[1],tv_upper=outward(void_bounds(residual)[1])[1],
        transfers={k:[str(a),str(b)] for k,(a,b) in sorted(transfers.items())})

def geometry():
    w,z=inputs();selected=read(HERE.parent/'shape_coupling'/'summary.json')['selected']
    assert selected['axis']==1 and selected['sign']==1
    zz=deform(z,selected['node'],1,1,F(selected['step']))
    a,b=boosted(z),boosted(zz)
    assert all(a[i]==b[i] for i in range(len(a)) if i!=selected['node'])
    packet,_,_=input_record(w['index']);lookup={v:i for i,v in enumerate(w['nodes'])}
    pairs=[(lookup[x],lookup[y]) for x,y in packet['pairs']];R=w['full_order']
    ends=[(x,y) if R[x][y] else (y,x) for x,y in pairs]
    return w,a,ends,selected

def run():
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z,ends,selected=geometry();records=[]
    for n in c['spatial_levels']:
        result=integrate(w,z,ends,selected,n);records.append(result)
        print(json.dumps({k:v for k,v in result.items() if k not in ['transfers','exact_unknown_upper','known_cell_witnesses']}),flush=True)
    best=min(records,key=lambda r:F(r['tv_upper']))
    previous=read(HERE.parent/'boundary_transfers'/'summary.json')['tv_upper']
    summary=dict(status='SURFACE_CORRELATION_CERTIFIED',pair_unchanged=True,spatial_levels=c['spatial_levels'],
        previous_tv_upper=previous,tv_upper=best['tv_upper'],combined_best_tv_upper=min(previous,best['tv_upper'],key=F),
        best_level=best['level'],directed_transfer_pairs=best['directed_transfer_pairs'],
        complete_pattern_cells=best['classification']['transfer'],
        cancellation_certified=F(best['certified_cancellation_lower'])>0,
        cancellation_lower=best['certified_cancellation_lower'],localization_tv_upper=best['localization_tv_upper'],
        unknown_transfer_mean_upper=best['unknown_transfer_mean_upper'],symmetric_operator_gap=selected['relative'],strong_pair_found=False,
        scope='Same geometry and grids as PR103. Correlation-preserving quadratic cone tests, not actual-TV or reconstruction-accuracy measurement. Unknown transfers retained.')
    return records,summary

if __name__=='__main__':
    for name,data in zip(['transfers.json.gz','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
