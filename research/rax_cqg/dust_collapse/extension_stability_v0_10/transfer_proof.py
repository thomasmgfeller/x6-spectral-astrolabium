"""Full-support tangent lower bounds under frozen v0.9 data, with separate inference modes."""
import argparse
from fractions import Fraction as F
from pathlib import Path
from unittest.mock import patch
import json
from math import isqrt
from source import ROOT,CACHE,reference
import bounds, planes
from reference import full
T=F(1,20)
TARGET='N15_356087'
COMPONENT=F('0.001301')

def fr(x): return F(float(x))

def rounded_lo(x,places=9):
    n=x*10**places
    i=n.numerator//n.denominator
    return ('-' if i<0 else '')+f'{abs(i)//10**places}.{abs(i)%10**places:0{places}d}'

def run():
    if not __debug__:raise RuntimeError('Run without -O')
    sampling=json.loads((ROOT/'sample.json').read_bytes())
    clocks={name:json.loads((ROOT/filename).read_bytes()) for name,filename in
            ((TARGET,'target.json'),('N15_39485','near_witness.json'))}
    prior=full.read(CACHE/'planes.json')
    bad=set(prior['outside_types'])
    if len(bad)!=119 or any(set(data)!=bad for data in sampling.values()):raise ValueError('sample coverage')
    rows,inds,_=planes.gram_rows()
    overall={'target_type':TARGET,'additional_direct_types':list(clocks),
             'old_full_transfer_per_million':prior['joint_full_transfer_per_million'],
             'deterministic_cases':{},'statistical_cases':{},'target_direct':{},'trial_mixture':{}}
    old_inputs=bounds.inputs
    def target_inputs(tag):
        names,reach,base,cols,known,mags,radii=old_inputs(tag)
        known,mags,radii=list(known),list(mags),list(radii)
        key={'coarse':'32,6','fine':'48,8'}[tag]
        for name,clock in clocks.items():
            j=names.index(name)
            if known[j] is not None or not any(j in r for r in reach):
                raise ValueError(('unexpected direct clock',name))
            a=[full.cf(complex(*x)) for x in clock[key]['amplitudes']]
            radius=F('1e-7')
            known[j]=a
            radii[j]=radius
            mags[j]=min(mags[j],max(map(full.modupper,a))+radius)
        return names,reach,base,cols,known,mags,radii
    with patch.object(full,'inputs',target_inputs):
        ref=full.calculate()
    overall['deterministic_seven_subsets_fraction']=ref['bound_fraction']
    least_det=least_stat=T
    safe=None
    for tag in ('coarse','fine'):
        names,reach,base,cols,known,mags,radii=target_inputs(tag)
        with patch.object(planes,'inputs',target_inputs):
            cases=planes.directions(rows,inds,tag)
        for v in cases:
            d=v['d'];case=f'{tag}_{d}';p,qb,qq=(v[k] for k in ('p','qb','qq'))
            b=[full.scale(F(1,2),known[j][d]) for j in inds[:2]]+[full.ZERO]*3
            nums=([202741,693388,103871],[201682,691688,106630])[d]
            q=[full.scale(1-T,x) for x in b[:2]]+[full.scale(T*F(k,10**6),known[j][d]) for k,j in zip(nums,inds[2:])]
            z=[planes.dot(q,col) for col in rows]
            h=v['h'].copy()
            exact_bad={names[j] for j in range(2,len(names)) if h[j]<v['critical']}
            safe=exact_bad if safe is None else (safe|exact_bad)
            def evaluate(h):
                js=[min(r,key=lambda j:h[j]) for r in reach]
                least=sum(h[j] for j in js)/2
                lower=(2*min(qb,(1-T)*qb+T*least)-qq)/p
                limit=min(T,(2*qb-qq-F('0.9')*p)/(2*(qb-least))) if least<qb else T
                return {'floor_ratio':str(lower),'floor_percent_down':rounded_lo(100*lower),
                        'parent_minima':[names[j] for j in js],
                        'transfer_fraction':str(limit)},limit
            det,t=evaluate(h);least_det=min(t,least_det);overall['deterministic_cases'][case]=det
            margins=[]
            for name in bad:
                j=names.index(name);re,im=map(fr,sampling[tag][name][d])
                low=full.mul(z[j],(re,im))[0]-COMPONENT*(abs(z[j][0])+abs(z[j][1]))
                margins.append((low-v['critical'],name))
                h[j]=max(h[j],low)
            margin,which=min(margins)
            st,t=evaluate(h);least_stat=min(t,least_stat)
            if margin<=0 or F(st['floor_ratio'])<=F('.9'):raise ValueError('unresolved '+case)
            st.update(minimum_sample_projection_slack=str(margin),sample_limiting_name=which)
            overall['statistical_cases'][case]=st
            # Explicit feasible transfer on the best-known adverse N14 triple.
            weights=[F(21,100),F(70,100),F(9,100)]
            if not all(set(inds[2:]).issubset(r) for r in reach):raise ValueError('unreachable trial')
            def gram(c):
                return sum(full.mul(planes.dot(c,rows[j]),y)[0] for y,j in zip(c,inds))
            for transfer in [T,F(50211,1000000)]:
                x=[full.scale(1-transfer,y) for y in b[:2]]+[full.scale(transfer*w,known[j][d]) for w,j in zip(weights,inds[2:])]
                # Norm of perturbation from clock radii bounded by weighted column norms.
                # Accepted S has diagonal <= sum of its three stored bin diagonals.
                def sqrt_up(value):
                    unit=10**18
                    return F(isqrt(value.numerator*unit**2//value.denominator)+1,unit)
                error=sum(transfer*w*radii[j]*sqrt_up(sum(cols[j][k][2][0] for k in range(3)))
                          for w,j in zip(weights,inds[2:]))
                val=gram(x)
                root_upper=sqrt_up(val)
                error_weight=2*root_upper*error+error**2
                overall['trial_mixture'][f'{case}_{transfer}']=[float((val-error_weight)/p),float((val+error_weight)/p)]
        # Direct four-outcome statistics for all transfer sent to the target.
        import numpy as np
        j=names.index(TARGET);gram_target=np.empty((3,3,3),complex);gram_target[:,:2,:2]=base
        col=np.array([[complex(*x) for x in line] for line in cols[j]])
        gram_target[:,:2,2]=col[:,:2];gram_target[:,2,:2]=col[:,:2].conj();gram_target[:,2,2]=col[:,2].real
        refs=[];trial=[]
        for d in range(2):
            b=np.array([complex(*known[k][d])/2 for k in (0,1)]+[0j])
            x=.95*b; x[-1]=.05*complex(*known[j][d])
            for state,out in ((b,refs),(x,trial)):
                y=np.einsum('i,kij,j->k',state.conj(),gram_target,state).real
                out.append(np.r_[y,1-y.sum()])
        refs,trial=np.array(refs),np.array(trial);dr=refs[1]-refs[0]
        overall['target_direct'][tag]={'relative_level':(.5*abs(trial-refs).sum(axis=1)/refs[:,:3].sum(axis=1)).tolist(),
             'relative_contrast':float(abs(trial[1]-trial[0]-dr).sum()/abs(dr).sum()),
             'success_difference':float(sum(trial[1,:3]-trial[0,:3]))}
    if any(not (lo > .9 if key.endswith('_1/20') else hi < .9 if '_1_' in key else True)
           for key,(lo,hi) in overall['trial_mixture'].items()):
        raise ValueError('adverse mixture control')
    if not all(F(x)<F(1,10) for x in planes.extra_gates().values()):
        raise ValueError('inherited level gates')
    overall.update(deterministic_certified_transfer_percent_down=rounded_lo(100*max(least_det,F(ref['bound_fraction'])),4),
        deterministic_safe_states=1217-len(safe),remaining_unconditionally_uncovered=sorted(safe),
        statistical_full_transfer_fraction=str(least_stat), statistical_safe_states=1217,
        simultaneous_alpha='1e-12', samples_per_clock=65536)
    return overall
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);args=p.parse_args()
    args.out.write_text(json.dumps(run(),indent=2,sort_keys=True)+'\n')
