"""Independent local Poisson generator and radar encoding. Angular variables are marginalized."""
import numpy as np
from math import pi
from auslese import END,TICKS,membership
from design import CASES


def smooth_vector(s):
    t=np.clip(s,0,1)
    return t**3*(10-15*t+6*t*t)


def generate(n,m,density):
    streams=np.random.SeedSequence(2026112503).spawn(len(CASES))
    recordings={};diagnostics=[]
    width=10/n
    dur=1/m
    for idx,((target,case),seed) in enumerate(zip(CASES,streams)):
        z=float(target)
        rng=np.random.Generator(np.random.PCG64(seed))
        tables=[];total=0;kept=0
        raw_counts=[0,0]
        for side in (-1,1):
            pad=2/TICKS
            reach=width+END*pad
            rmax=10+(reach if side>0 else 0)
            proposed=rng.poisson(density*4*pi*rmax**2*reach*2*(dur+pad)*END)
            x=rng.uniform(z-dur-pad,z+dur+pad,proposed)
            dist=rng.uniform(0,reach,proposed)
            u=(10+side*dist)/10
            f=1-(u**2-1)**2*(81*u**2+8)/8
            d=.0398*smooth_vector(x)+.2576*smooth_vector(64*(x-z)+(case=='A'))
            acceptance=(10*u/rmax)**2*(1-d*f)
            assert np.min(acceptance)>0 and np.max(acceptance)<=1
            chosen=rng.random(proposed)<acceptance
            x=x[chosen];dist=dist[chosen]
            emit=np.rint(TICKS*(x-dist/END)).astype('int32')
            receive=np.rint(TICKS*(x+dist/END)).astype('int32')
            block=np.column_stack((emit,receive,np.full(len(x),side,'int32')))
            lower,upper=membership(block,z,width,dur)
            original_lower=(side==-1)&(x>=z)&(x<=z+dur)&(dist<=width)
            original_upper=(side==1)&(x>=z-dur)&(x<=z)&(dist<=width)
            assert np.all(~lower|original_lower) and np.all(~original_upper|upper)
            raw_counts[0]+=int(original_lower.sum());raw_counts[1]+=int(original_upper.sum())
            tables.append(block);total+=int(proposed);kept+=len(x)
        key=f'aufnahme_{idx+1}'
        recordings[key]=np.vstack(tables)
        diagnostics.append({'id':key,'case':case,'target':str(target),'proposed':total,
                            'recorded':kept,'ideal_membership_counts':raw_counts})
    return recordings,diagnostics
