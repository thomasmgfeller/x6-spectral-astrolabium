"""Intrinsic interval-volume weights. No coordinates, simulator or fields accepted."""
import copy
import math


def assemble(stencil,marks,c,times,both=False):
    out=copy.deepcopy(stencil)
    if out['status']!='ok':return out
    weights={}
    for b in out['temporal']:
        q=times[b] if both else out['tau_n']
        if not math.isfinite(q) or q<=0:raise ValueError('positive finite time required')
        weights[b]=weights.get(b,0.)-(c+3)/q**2
    for side in out['sides']:
        for b in side['selected']:
            q=times[b]
            if not math.isfinite(q) or q<=0:raise ValueError('positive finite time required')
            weights[b]=weights.get(b,0.)+c/(len(side['selected'])*q**2)
    out['support']=sorted(weights,key=lambda b:marks[b]);out['weights']=[weights[b] for b in out['support']]
    return out


def reweight(g,stencil,rho,c,both=False):
    if not math.isfinite(rho) or rho<=0:raise ValueError('known positive finite density required')
    out=copy.deepcopy(stencil);out['interval_times']=[]
    if out['status']!='ok':return out
    needed={b for side in out['sides'] for b in side['selected']}
    if both:needed.update(out['temporal'])
    times={};bad=False
    for b in sorted(needed,key=lambda b:g.marks[b]):
        root=out['root']
        if g.r[root,b]:n=g.interval(root,b)
        elif g.r[b,root]:n=g.interval(b,root)
        else:raise ValueError('selected point is not causally related to root')
        q=(n/(rho*(math.pi/12)))**(1/3) if n>0 else None
        out['interval_times'].append(dict(point=b,interior_count=n,time=q))
        if q is None:bad=True
        else:times[b]=q
    if bad:
        out['status']='zero_interval';out.pop('support',None);out.pop('weights',None)
        return out
    return assemble(out,g.marks,c,times,both)
