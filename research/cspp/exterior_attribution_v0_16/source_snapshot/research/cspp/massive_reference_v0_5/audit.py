"""Controls for the extended spatial domain and source-coordinate change."""
import json
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx
import reference as r


def check(ok,message):
    if not ok:raise RuntimeError('FAIL: '+message)


def controls():
    r.balls.configure();A=r.previous.normalization(ctx.prec)[0]
    out={};count=0
    # A constant source inside a radius-b ball has exact intersection volume.
    # Independent closed-form ball-ball lens volume checks support and Jacobians.
    b=arb('.5');tau=arb(2)
    for R in [arb('1.25'),arb('1.75'),arb(2),arb('2.25')]:
        lo=max(arb(0),R-tau);hi=min(b,R+tau);split=tau-R
        edges=[lo]+([split] if lo<split<hi else [])+[hi]
        value=acb(0)
        for l,u in zip(edges[:-1],edges[1:]):
            full=(l+u)/2<split
            def f(s,analytic):
                v0=acb(-1) if full else (s/(2*R) if tau==R else (R*R+s*s-tau*tau)/(2*R*s))
                return s*s*(1-v0)/2
            value+=r.integrate(f,l,u)
        exact=b**3/3 if R<=tau-b else ((b+tau-R)**2*(R*R+2*R*tau-3*tau*tau+2*R*b+6*tau*b-3*b*b)/(48*R))
        check(value.real.overlaps(exact),'ball intersection volume')
        check(value.imag.contains(0),'real lens');count+=1
    out['independent_lens_volume_cases']=count
    count=0
    for p in [[-.5,.5,0,0],[0,0,0,.5],[1,.25,0,1.5],[1,0,0,1.75]]:
        for m in (1,2):
            z,_=r.off_center(p,m,A)
            reflection=[p[0],p[1],p[2],-p[3]]
            check(z.overlaps(r.off_center(reflection,m,A)[0].conjugate()),'z reflection')
            timeflip=[-2-p[0],*p[1:]]
            check(z.overlaps(r.off_center(timeflip,m,A)[0]),'time reversal')
            rotate=[p[0],-p[2],p[1],p[3]]
            check(z.overlaps(r.off_center(rotate,m,A)[0]),'axial rotation')
            count+=3
    out['massive_symmetry_cases']=count
    # All three spatial support topologies: empty, all-source, partial lens.
    for p in [[-.5,0,0,1],[-1,0,0,1],[0,0,0,2]]:
        check(r.off_center(p,1,A)[0].is_zero(),'causal support zero')
    p=[-1,0,0,.25]
    exact=A*(-1/(1-arb('.25')**2/arb('.5')**2)).exp()*acb(0,1).exp()
    check(r.off_center(p,2,A)[0].overlaps(exact),'initial data')
    out['support_and_initial_cases']=4
    # The existing 27 independent plane waves also check the inherited KG signs.
    import importlib.util
    spec=importlib.util.spec_from_file_location('old_audit',r.BASE/'audit.py')
    old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
    out['inherited_controls']=old.controls()
    rejected=0
    for p,m in [([0,0,0,0],1),([0,.5,0,0],3),([0,float('nan'),0,0],1)]:
        try:r.off_center(p,m,A)
        except ValueError:rejected+=1
    check(rejected==3,'scope guards');out['rejected_invalid_inputs']=3
    return out


def compare(low,high):
    expected={(i,m) for i in range(28) if i not in (0,7,14) for m in (1,2)}
    check({(x['probe_index'],x['mass']) for x in low['rows']}==expected,'50 fixed identities')
    check(len(low['rows'])==len(high['rows'])==50,'row counts')
    for x,y in zip(low['rows'],high['rows']):
        check((x['probe_index'],x['mass'],x['point'])==(y['probe_index'],y['mass'],y['point']),'row correspondence')
        check(r.balls.decode(x['value']).overlaps(r.balls.decode(y['value'])),'192-bit replay')
        for v in (x,y):
            z=r.balls.decode(v['value'])
            check(max(z.real.rad(),z.imag.rad())<arb('1e-12'),'serialized radius target')
            check(v['enclosure_status']=='WITHIN_RADIUS_GOAL','status')
            check(r.balls.decode(v['old_Green_absolute_difference_bound']).real<arb('1e-10'),'independent old Green regression')
    return {'amplitudes':50,'precisions_bits':[128,192],
            'overlap_is_regression_not_proof':True}



def detector_controls():
    import detector as d
    r.balls.configure();A=r.previous.normalization(ctx.prec)[0];count=0
    for p in [[1,0,0,1.25],[1,0,0,1.5],[1,.25,0,1.5],[1,0,0,1.75]]:
        tau,x,R=r.geometry(p);c=x[2]/R
        region=0 if R<2-d.parameters()[5] else 1
        for m in (1,2):
            coarse=d.field_range(acb(R),acb(c),m,region)
            tail=d.tail_bounds(m)[0]
            check(r.balls.inflate(coarse,tail).contains(r.off_center(p,m,A)[0]),'range formula contains sharp point certificate')
            count+=1
    intervals,delta=d.partition();sums=[arb(0) for _ in range(4)]
    covered=arb(0)
    for lo,hi,region in intervals:
        R=d.hull(lo,hi);cmin=d.cap_cos_range(lo,hi);w=(d.primitive(hi)-d.primitive(lo))/8
        for i in range(8):
            c=1-(1-cmin)*(1-d.hull(arb(i)/8,arb(i+1)/8));z=R*c
            for j,f in enumerate([arb(1),z,z*z,R*R]):sums[j]+=w*f
            covered+=w
    V=arb.pi()/6;cap=V-covered
    for got,exact,maxabs in zip(sums,[V,V*arb('1.5'),V*arb('2.3'),V*arb('2.4')],[1,2,4,4]):
        check((got+arb(0,(cap*maxabs).abs_upper())).contains(exact),'exact ball polynomial moment')
    check(cap>0 and cap<2*arb.pi()/3*delta**2,'tip cap estimate')
    # A local point-radius test is deliberately insufficient for spatial PASS.
    check(len(intervals)*8>7,'spatial coverage is not seven detector samples')
    return {'sharp_point_containment_cases':count,'exact_detector_moment_cases':4,
            'positive_tip_cap_checked':True,'spatial_cells':len(intervals)*8}


if __name__=='__main__':
    print(json.dumps({'source':controls(),'detector':detector_controls()},indent=2))
