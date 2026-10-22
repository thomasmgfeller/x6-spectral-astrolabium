"""Certified spatial integration on two moving cone strips; no random sampling.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,math,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'paired_atoms'))
from pa_run import F,read,save,outward,sqrt_bounds,inputs,void_bounds,constant
from ja_run import boosted,deform,input_record,setup,OLDUNIT,floor,ceil

def radial_bounds(rect,v):
    low=F(0);high=F(0)
    for (a,b),c in zip(rect,v):
        d=max(a-c,c-b,F(0));low+=d*d
        high+=max(abs(a-c),abs(b-c))**2
    return sqrt_bounds(low)[0],sqrt_bounds(high)[1]

def strip(rect,v,h):
    """Enclose r1-r0 using its correlated numerator, not subtraction of roots."""
    r0=radial_bounds(rect,v);r1=radial_bounds(rect,[v[0]+h,v[1]])
    q=[h*h-2*h*(x-v[0]) for x in rect[0]];qlo,qhi=min(q),max(q)
    assert qlo>=0 or qhi<=0  # split spatial grid at x=v_x+h/2
    sign=1 if qlo>=0 else -1
    numlo,numhi=(qlo,qhi) if sign==1 else (-qhi,-qlo)
    denlo=r0[0]+r1[0];denhi=r0[1]+r1[1]
    lower=numlo/denhi if denhi else F(0)
    upper=min(h,numhi/denlo) if denlo else h
    assert 0<=lower<=upper<=h
    return sign,(lower,upper),(min(r0[0],r1[0]),max(r0[1],r1[1]))

def labels(lower,upper,z,ends,node,side,forced,unit,detailed=False):
    lo=np.array([[floor(x*unit) for x in row] for row in z],dtype=np.int64)
    hi=np.array([[ceil(x*unit) for x in row] for row in z],dtype=np.int64)
    assert max(np.max(abs(a)) for a in [lo,hi,lower,upper])<10**7
    fi=[];fo=[];pi=[];po=[]
    for k,(a,b) in enumerate(zip(lo,hi)):
        mind=np.maximum(0,np.maximum(a[1:]-upper[:,1:],lower[:,1:]-b[1:]))
        maxd=np.maximum(abs(lower[:,1:]-b[1:]),abs(upper[:,1:]-a[1:]))
        rmin=np.sum(mind*mind,axis=1);rmax=np.sum(maxd*maxd,axis=1)
        for kind,dmin,dmax,inner,outer in [(1,lower[:,0]-b[0],upper[:,0]-a[0],fi,fo),(-1,a[0]-upper[:,0],b[0]-lower[:,0],pi,po)]:
            ii=(dmin>0)&(dmin*dmin>rmax);oo=(dmax>0)&(dmax*dmax>=rmin)
            if k==node and kind==side:ii=forced.copy();oo=forced.copy()
            inner.append(ii);outer.append(oo)
    inner=np.array([fi[a]&pi[b] for a,b in ends]);outer=np.array([fo[a]&po[b] for a,b in ends])
    assert np.all(~inner|outer)
    known=np.all(inner==outer,axis=0)
    result=(known,np.packbits(inner.T,axis=1,bitorder='little'),outer[ends.index((3,0))])
    if detailed:
        affected=[i for i,(a,b) in enumerate(ends) if (a==node if side==1 else b==node)]
        possible=np.any(outer[affected],axis=0) if affected else np.zeros(len(lower),dtype=bool)
        return (*result,possible,inner!=outer)
    return result

def balance(transfers,unknown,cap):
    assert unknown>=0 and cap>=0
    assert all(0<=lo<=hi for lo,hi in transfers.values())
    outgoing={};incoming={}
    for edge,(lo,hi) in transfers.items():
        a,b=edge.split('>')
        for table,key in [(outgoing,a),(incoming,b)]:
            x,y=table.get(key,(F(0),F(0)));table[key]=(x+lo,y+hi)
    total_upper=unknown+sum(x[1] for x in transfers.values())
    imbalance=F(0)
    for key in outgoing.keys()|incoming.keys():
        a,b=incoming.get(key,(F(0),F(0)));c,d=outgoing.get(key,(F(0),F(0)))
        imbalance+=max(abs(a-d),abs(b-c))
    cancellation_lower=sum(min(incoming.get(k,(F(0),F(0)))[0],outgoing.get(k,(F(0),F(0)))[0]) for k in incoming.keys()|outgoing.keys())
    total_upper=min(total_upper,cap)
    balanced_upper=min(total_upper-cancellation_lower,imbalance/2+unknown)
    assert 0<=balanced_upper<=total_upper<=cap
    return total_upper,balanced_upper,cancellation_lower

def integrate(w,z,zz,ends,selected,n,unit):
    node=selected['node'];h=F(selected['step']);v=z[node];box=setup(0)
    ranges=[(F(int(box['low'][j]),OLDUNIT),F(int(box['high'][j]),OLDUNIT)) for j in [1,2]]
    edges=[[a+(b-a)*i/n for i in range(n+1)] for a,b in ranges]
    cut=v[1]+h/2
    if edges[0][0]<cut<edges[0][-1]:edges[0]=sorted(set(edges[0]+[cut]))
    rects=[((a,b),(c,d)) for a,b in zip(edges[0],edges[0][1:]) for c,d in zip(edges[1],edges[1][1:])]
    records=[];factor=F(w['rho'])*F(w['scale'])**3
    transfers={};unknown=F(0);counts={'outside':0,'no_affected_interval':0,'same_label':0,'transfer':0,'unresolved':0}
    ambiguities=np.zeros(len(ends),dtype=np.int64)
    for side in [1,-1]:
        lower=[];upper=[];signs=[];masses=[]
        for rect in rects:
            sign,delta,r=strip(rect,v[1:],h)
            times=(v[0]+r[0],v[0]+r[1]) if side==1 else (v[0]-r[1],v[0]-r[0])
            lower.append([floor(times[0]*unit),floor(rect[0][0]*unit),floor(rect[1][0]*unit)])
            upper.append([ceil(times[1]*unit),ceil(rect[0][1]*unit),ceil(rect[1][1]*unit)])
            area=(rect[0][1]-rect[0][0])*(rect[1][1]-rect[1][0])
            masses.append(tuple(map(F,outward(factor*area*delta[0],factor*area*delta[1],digits=30))));signs.append(sign)
        lower=np.array(lower,dtype=np.int64);upper=np.array(upper,dtype=np.int64)
        # Both future/past cone memberships are r<|t-v_t|. On the strip,
        # original membership is true iff r1>r0, independently of side.
        forced=np.array(signs)>0
        k0,b0,o0,p0,u0=labels(lower,upper,z,ends,node,side,forced,unit,True)
        k1,b1,o1,p1,u1=labels(lower,upper,zz,ends,node,side,~forced,unit,True)
        for i,(lo,hi) in enumerate(masses):
            if not o0[i] or not o1[i]:counts['outside']+=1;continue
            if not (p0[i] or p1[i]):counts['no_affected_interval']+=1;continue
            if k0[i] and k1[i]:
                a,b=bytes(b0[i]).hex(),bytes(b1[i]).hex()
                if a==b:counts['same_label']+=1;continue
                assert any(bytes.fromhex(a)) and any(bytes.fromhex(b))
                counts['transfer']+=1
                key=a+'>'+b
                old=transfers.get(key,(F(0),F(0)));transfers[key]=(old[0]+lo,old[1]+hi)
            else:
                unknown+=hi;counts['unresolved']+=1;ambiguities+=(u0[:,i]|u1[:,i])
    total_upper,balanced_upper,cancellation_lower=balance(transfers,unknown,constant(w)*h/2)
    result=dict(level=n,surface_rectangles=2*len(rects),classification=counts,
        ambiguous_intervals=[dict(endpoints=list(ends[i]),cells=int(ambiguities[i])) for i in np.argsort(-ambiguities,kind='stable')[:5] if ambiguities[i]>0],
        directed_transfer_pairs=len(transfers),unknown_transfer_mean_upper=outward(unknown)[1],
        localized_changed_mean_upper=outward(total_upper)[1],balanced_residual_mean_upper=outward(balanced_upper)[1],
        certified_cancellation_gain_lower=outward(cancellation_lower)[0],
        localized_void_tv_upper=outward(void_bounds(total_upper)[1])[1],
        balanced_tv_upper=outward(void_bounds(balanced_upper)[1])[1],
        transfers={k:[str(a),str(b)] for k,(a,b) in sorted(transfers.items())},
        exact_unknown_upper=str(unknown))
    return result

def run():
    c=read(HERE/'contract.json')
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    w,z=inputs();old=read(HERE.parent/'shape_coupling'/'summary.json')['selected']
    assert old['axis']==1 and old['sign']==1
    zz=deform(z,old['node'],old['axis'],old['sign'],F(old['step']))
    packet,_,_=input_record(w['index']);lookup={v:i for i,v in enumerate(w['nodes'])}
    pairs=[(lookup[a],lookup[b]) for a,b in packet['pairs']];R=w['full_order']
    ends=[(a,b) if R[a][b] else (b,a) for a,b in pairs]
    results=[]
    for n in c['spatial_levels']:
        r=integrate(w,boosted(z),boosted(zz),ends,old,n,c['coordinate_unit']);results.append(r)
        print(json.dumps({k:v for k,v in r.items() if k not in ['transfers','exact_unknown_upper']}),flush=True)
    best=min(results,key=lambda r:F(r['balanced_tv_upper']))
    previous=read(HERE.parent/'paired_atoms'/'summary.json')['tv_upper']
    summary=dict(status='BOUNDARY_TRANSFER_CERTIFIED',pair_unchanged=True,levels=c['spatial_levels'],
        best_level=best['level'],previous_tv_upper=previous,tv_upper=best['balanced_tv_upper'],
        localization_only_tv_upper=best['localized_void_tv_upper'],
        cancellation_certified=F(best['certified_cancellation_gain_lower'])>0,
        cancellation_status='CERTIFIED' if F(best['certified_cancellation_gain_lower'])>0 else 'HOLD_FULL_PATTERN_LOCALIZATION',
        cancellation_gain_lower=best['certified_cancellation_gain_lower'],
        unknown_transfer_mean_upper=best['unknown_transfer_mean_upper'],
        symmetric_operator_gap=old['relative'],strong_pair_found=False,
        scope='Deterministic boundary-localized full count-law upper bound on unchanged PR95 pair. Unknown transfers retained. Neither actual-TV measurement nor improved reconstruction accuracy.')
    return results,summary

if __name__=='__main__':
    for name,data in zip(['transfers.json.gz','summary.json'],run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
