"""Analytic intersections plus rigorously budgeted randomized cell integration.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib,math
from pathlib import Path
from functools import lru_cache
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'finite_poisson_bounds'))
from fp_common import F,read,save,OLD,input_record,count_box,outward,sqrt_bounds,pi_bounds,interval,confidence_bound
UNIT=2**16
@lru_cache(None)
def cb(n,c):return count_box(n,c)
def flo(x):return x.numerator//x.denominator
def cei(x):return -((-x.numerator)//x.denominator)
def boosted(z):return [[F(17,8)*t+F(15,8)*x,F(15,8)*t+F(17,8)*x,y] for t,x,y in z]
def classify_cells(cells,lo,hi):
    """Integer interval arithmetic, entire unit cells and enclosed endpoints."""
    lower=cells;upper=cells+1
    assert max(int(np.max(abs(lower))),int(np.max(abs(upper))),int(np.max(abs(lo))),int(np.max(abs(hi))))<10**7
    inner_f=[];outer_f=[];inner_p=[];outer_p=[]
    for a,b in zip(lo,hi):
        mind=np.maximum(0,np.maximum(a[1:]-upper[:,1:],lower[:,1:]-b[1:]))
        maxd=np.maximum(abs(lower[:,1:]-b[1:]),abs(upper[:,1:]-a[1:]))
        rmin=np.sum(mind*mind,axis=1);rmax=np.sum(maxd*maxd,axis=1)
        for sign,ins,outs in [(1,inner_f,outer_f),(-1,inner_p,outer_p)]:
            if sign==1:dmin=lower[:,0]-b[0];dmax=upper[:,0]-a[0]
            else:dmin=a[0]-upper[:,0];dmax=b[0]-lower[:,0]
            ins.append((dmin>0)&(dmin*dmin>rmax))
            outs.append((dmax>0)&(dmax*dmax>=rmin))
    return np.array(inner_f),np.array(outer_f),np.array(inner_p),np.array(outer_p)
def enclose(a,b):return [str(a),str(b)]
def outcome(bounds,target):
    lo,hi=bounds;L,U=target
    if hi<L or lo>U:return 'EXCLUDED'
    if L<=lo<=hi<=U:return 'INSIDE'
    return 'UNRESOLVED'
def subtract(a,b):return max(F(0),a[0]-b[1]),max(F(0),a[1]-b[0])

def setup():
    w=read(OLD/'witness.json');p,obs,mask=input_record(w['index'])
    assert [obs['counts'][i] for i in mask]==w['counts']
    assert mask==w['input_mask_indices']
    C=np.array(obs['overlaps'],dtype=np.int64)[np.ix_(mask,mask)]
    R=w['full_order'];ends=[(a,b) if R[a][b] else (b,a) for a,b in w['pairs']]
    assert all(R[a][b] for a,b in ends)
    def le(a,b):return a==b or R[a][b]
    items=[]
    for i,(a,b) in enumerate(ends):
      for j,(c,d) in enumerate(ends[:i]):
        lows=sorted(v for v in {a,c} if not any(v!=z and le(v,z) for z in {a,c}))
        ups=sorted(v for v in {b,d} if not any(v!=z and le(z,v) for z in {b,d}))
        kind='ZERO' if any(not R[x][y] for x in lows for y in ups) else 'DIAMOND' if len(lows)==len(ups)==1 else 'INTEGRATE'
        n=int(C[i,j]);targets=[cb(n,20),cb(w['counts'][i]-n,20),cb(w['counts'][j]-n,20)]
        items.append(dict(i=i,j=j,kind=kind,lows=lows,ups=ups,targets=targets))
    return w,ends,items

def geometry(g,contract):
    w,ends,items=setup();z=[[F(v) for v in row] for row in w['coordinates'][g]]
    zz=boosted(z);R=w['full_order']
    for a in range(len(z)):
      for b in range(len(z)):
        assert interval(z,a,b)==interval(zz,a,b)
        assert bool(interval(zz,a,b)>0 and zz[b][0]>zz[a][0])==R[a][b]
    factor=F(w['rho'])*F(w['scale'])**3;pi0,pi1=pi_bounds()
    def mean(a,b):
        q=interval(z,a,b);assert q>0
        lo,hi=sqrt_bounds(q);return factor*pi0*q*lo/12,factor*pi1*q*hi/12
    means=[mean(a,b) for a,b in ends]
    exact=[];todo=[];allstatuses=[]
    for k,mu in enumerate(means):
        status=outcome(mu,cb(w['counts'][k],12));allstatuses.append(status)
        exact.append(dict(type='MARGINAL',i=k,bounds=enclose(*mu),status=status))
    for item in items:
        i,j=item['i'],item['j']
        if item['kind']=='INTEGRATE':todo.append(item);continue
        v=(F(0),F(0)) if item['kind']=='ZERO' else mean(item['lows'][0],item['ups'][0])
        values=[v,subtract(means[i],v),subtract(means[j],v)]
        statuses=[outcome(v,t) for v,t in zip(values,item['targets'])];allstatuses+=statuses
        exact.append(dict(type=item['kind'],i=i,j=j,bounds=[enclose(*v) for v in values],statuses=statuses))
    assert len(todo)==480
    # Every selected interval is within I(3,0), verified by exact order.
    assert all((a==3 or R[3][a]) and (b==0 or R[b][0]) for a,b in ends)
    a,b=zz[3],zz[0];T=b[0]-a[0];dx=b[1]-a[1];dy=b[2]-a[2]
    # Spatial projection of a diamond is an ellipse.
    rx=sqrt_bounds(T*T-dy*dy)[1]/2;ry=sqrt_bounds(T*T-dx*dx)[1]/2
    low=[flo(a[0]*UNIT),flo(((a[1]+b[1])/2-rx)*UNIT),flo(((a[2]+b[2])/2-ry)*UNIT)]
    high=[cei(b[0]*UNIT),cei(((a[1]+b[1])/2+rx)*UNIT),cei(((a[2]+b[2])/2+ry)*UNIT)]
    assert all(h>l for l,h in zip(low,high))
    boxmean=factor*F(math.prod(h-l for l,h in zip(low,high)),UNIT**3)
    lo=np.array([[flo(v*UNIT) for v in row] for row in zz],dtype=np.int64)
    hi=np.array([[cei(v*UNIT) for v in row] for row in zz],dtype=np.int64)
    rng=np.random.Generator(np.random.PCG64(contract['seeds'][g]));inner=[bytearray() for _ in ends];outer=[bytearray() for _ in ends]
    stages=[];done=0
    for exponent in contract['sample_exponents']:
        target=2**exponent
        while done<target:
            n=min(contract['chunk_size'],target-done)
            cells=rng.integers(low,high,size=(n,3),dtype=np.int64)
            fi,fo,pi,po=classify_cells(cells,lo,hi)
            for k,(a,b) in enumerate(ends):
                inner[k].extend(np.packbits(fi[a]&pi[b],bitorder='little').tobytes())
                outer[k].extend(np.packbits(fo[a]&po[b],bitorder='little').tobytes())
            done+=n
        inside=[int.from_bytes(v,'little') for v in inner];outside=[int.from_bytes(v,'little') for v in outer]
        assert all(i&~o==0 for i,o in zip(inside,outside))
        def numerical(ki,ko):
            assert 0<=ki<=ko<=target
            lb=cb(ki,contract['integration_c'])[0]/target
            ub=min(F(1),cb(ko,contract['integration_c'])[1]/target)
            return boxmean*lb,boxmean*ub
        controls=[]
        for k in range(len(ends)):
            ki,ko=inside[k].bit_count(),outside[k].bit_count();v=numerical(ki,ko)
            status='ENCLOSES_ANALYTIC' if v[0]<=means[k][0] and means[k][1]<=v[1] else 'CONTROL_FAILURE'
            controls.append(dict(i=k,inner=ki,outer=ko,status=status))
        rows=[];statuses=[];slacks=[]
        for item in todo:
            i,j=item['i'],item['j']
            counts=[((inside[i]&inside[j]).bit_count(),(outside[i]&outside[j]).bit_count()),
                    ((inside[i]&~outside[j]).bit_count(),(outside[i]&~inside[j]).bit_count()),
                    ((inside[j]&~outside[i]).bit_count(),(outside[j]&~inside[i]).bit_count())]
            values=[numerical(*v) for v in counts]
            states=[outcome(v,t) for v,t in zip(values,item['targets'])];statuses+=states
            for v,t,s in zip(values,item['targets'],states):
                if s=='INSIDE':slacks.append(min(v[0]-t[0],t[1]-v[1]))
            rows.append(dict(i=i,j=j,counts=counts,bounds=[enclose(*v) for v in values],statuses=states))
        stage=dict(samples=target,rows=rows,controls=controls,status_counts={s:statuses.count(s) for s in ['INSIDE','EXCLUDED','UNRESOLVED']},
                   minimum_inside_slack=outward(min(slacks))[0] if slacks else None,
                   membership_sha256=hashlib.sha256(b''.join(inner)+b''.join(outer)).hexdigest())
        stages.append(stage);print(json.dumps({'geometry':g,'samples':target,'status_counts':stage['status_counts']}),flush=True)
        if any(v['status']=='CONTROL_FAILURE' for v in controls):break
        if 'EXCLUDED' in statuses or 'UNRESOLVED' not in statuses:break
    last=stages[-1]
    state='INTEGRATION_CONTROL_HOLD' if any(v['status']=='CONTROL_FAILURE' for v in last['controls']) else 'EXCLUDED' if ('EXCLUDED' in allstatuses or last['status_counts']['EXCLUDED']) else 'COMPATIBLE_WITH_CHECKED_CONFIDENCE_SET' if ('UNRESOLVED' not in allstatuses and not last['status_counts']['UNRESOLVED']) else 'UNRESOLVED'
    return dict(geometry=g,status=state,analytic=exact,analytic_status_counts={s:allstatuses.count(s) for s in ['INSIDE','EXCLUDED','UNRESOLVED']},
      integration_pairs=len(todo),box_lower=low,box_upper=high,box_mean=str(boxmean),stages=stages)

def main():
    verify='--verify' in sys.argv
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');rows=[]
    for g in range(2):
        r=geometry(g,c);path=HERE/f'geometry-{g}.json.gz'
        if verify:assert json.loads(json.dumps(r))==read(path),g
        else:save(path,r)
        rows.append(dict(geometry=g,status=r['status'],samples=r['stages'][-1]['samples'],analytic_status_counts=r['analytic_status_counts'],numerical_status_counts=r['stages'][-1]['status_counts']))
    family=2*len(c['sample_exponents'])*2*(480*3+74)
    risk=confidence_bound(family,c['integration_c'])
    out=dict(status='COMPLETE',records=rows,integration_scalar_family=family,numerical_failure_upper=outward(risk)[1],
             numerical_coverage_lower=outward(1-risk)[0],measurement_set_coverage_lower=read(HERE.parent/'joint_overlap_bounds/summary.json')['coverage_lower'],
             scope='Numerical probability under ideal iid uniform cell sampling; seeded PCG64 implementation. Not deterministic integration, posterior probability, testing distance, or physical validation.')
    if verify:assert out==read(HERE/'summary.json')
    else:save(HERE/'summary.json',out)
    print(json.dumps(out),flush=True)
if __name__=='__main__':main()
