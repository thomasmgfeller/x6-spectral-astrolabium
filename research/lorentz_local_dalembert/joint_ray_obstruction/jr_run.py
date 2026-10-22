"""Uniform joint Poisson event obstruction on the remaining spatial ray.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'continuous_energy'))
from ce_common import F,read,save,outward,setup,ray_data,q_bounds,mean_bounds,interval

def frozen():
    for name,digest in read(HERE/'freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name

def weights(mu,digits,steps,maximum):
    """Directed integer relative PMFs, including the omitted infinite tail."""
    assert 0<=mu<=maximum and digits>0 and steps>0
    mode=mu.numerator//mu.denominator;upper=mode+steps;unit=10**digits
    lo=[0]*(upper+1);hi=lo.copy();lo[mode]=hi[mode]=unit
    if mu==0:
        return dict(lo=lo,hi=hi,zlo=unit,zhi=unit,tail=0,mode=0,upper=upper)
    n,d=mu.numerator,mu.denominator
    for j in range(mode,0,-1):
        lo[j-1]=lo[j]*j*d//n;hi[j-1]=-((-hi[j]*j*d)//n)
    for j in range(mode+1,upper+1):
        lo[j]=lo[j-1]*n//(d*j);hi[j]=-((-hi[j-1]*n)//(d*j))
    assert mu<upper+2
    tail=F(hi[-1])*mu/(upper+1)/(1-mu/(upper+2))
    tail=-((-tail.numerator)//tail.denominator)
    return dict(lo=lo,hi=hi,zlo=sum(lo),zhi=sum(hi)+tail,tail=tail,mode=mode,upper=upper)

def event(mu_x,mu_y,coefficient,threshold,c):
    assert isinstance(coefficient,int) and coefficient>0 and isinstance(threshold,int)
    x=weights(mu_x,c['cdf_grid_digits'],c['x_upper_steps'],c['maximum_mean'])
    y=weights(mu_y,c['cdf_grid_digits'],c['y_upper_steps'],c['maximum_mean'])
    assert threshold+coefficient*x['upper']<=y['upper'],'insufficient Y support'
    prefix_lo=[];prefix_hi=[];a=b=0
    for lo,hi in zip(y['lo'],y['hi']):
        a+=lo;b+=hi;prefix_lo.append(a);prefix_hi.append(b)
    numerator_lo=numerator_hi=0
    for j,(lo,hi) in enumerate(zip(x['lo'],x['hi'])):
        k=threshold+coefficient*j
        if k>=0:
            numerator_lo+=lo*prefix_lo[k];numerator_hi+=hi*prefix_hi[k]
    lower=F(numerator_lo,x['zhi']*y['zhi'])
    upper=min(F(1),F(numerator_hi,x['zlo']*y['zlo'])+F(x['tail'],x['zlo']))
    assert 0<=lower<=upper<=1
    metadata=dict(x={k:str(x[k]) for k in ('mode','upper','zlo','zhi','tail')},
                  y={k:str(y[k]) for k in ('mode','upper','zlo','zhi','tail')})
    return (lower,upper),metadata

def enclose_event(x,y,c):
    assert 0<=x[0]<=x[1] and 0<=y[0]<=y[1]
    records=[];bounds=[]
    # The event is increasing in X and decreasing in Y under Poisson coupling.
    for label,a,b in [('lower',x[0],y[1]),('upper',x[1],y[0])]:
        p,meta=event(a,b,c['event']['x_coefficient'],c['event']['threshold'],c)
        assert p[1]-p[0]<=F(c['numerical_event_width_target'])
        bounds.append(p)
        records.append(dict(endpoint=label,x_mean=str(a),y_mean=str(b),probability=outward(*p,digits=65),
                            numerical_width_upper=outward(p[1]-p[0],digits=75)[1],normalization=meta))
    return (bounds[0][0],bounds[1][1]),records

def run():
    frozen();c=read(HERE/'contract.json');b=setup();d=c['domain'];lo,hi=map(F,d['h'])
    old=read(HERE.parent/'continuous_energy'/'summary.json')
    assert old['unresolved_rays']==1 and old['unresolved_intervals']==[
        dict(ray=40,node=d['node'],axis=d['axis'],sign=d['sign'],intervals=[d['h']])]
    assert old['states']['HOLD']==30 and old['rays']==64
    xpair=c['statistics']['X']['interval'];ypair=c['statistics']['Y']['interval']
    assert list(b['ends'][c['statistics']['X']['index']])==xpair
    assert list(b['ends'][c['statistics']['Y']['index']])==ypair
    assert xpair[1]==ypair[0]==d['node']
    # Fixed boosted times put every point of X strictly before the moving tip,
    # and every point of Y strictly after it, throughout this spatial motion.
    assert b['boost'][xpair[0]][0]<b['boost'][d['node']][0]<b['boost'][ypair[1]][0]
    ray=ray_data(b,d['node'],d['axis'],d['sign']);base=[];changed=[];q_records=[]
    for pair in (xpair,ypair):
        q0=interval(b['z'],*pair);q=q_bounds(b,ray,*pair,lo,hi)
        assert q0>0 and q[0]>0
        base.append(mean_bounds(b,(q0,q0)));changed.append(mean_bounds(b,q))
        q_records.append(dict(interval=pair,base=str(q0),moved=[str(v) for v in q]))
    p,pr=enclose_event(*base,c);q,qr=enclose_event(*changed,c)
    difference=(p[0]-q[1],p[1]-q[0]);tv=max(F(0),difference[0])
    excluded=tv>F(c['tv_gate'])
    certificate=dict(domain=d,statistics=c['statistics'],event=c['event'],quadratic_ranges=q_records,
        base_mean_intervals=[[str(v) for v in a] for a in base],
        moved_mean_intervals=[[str(v) for v in a] for a in changed],
        base_event_probability=outward(*p,digits=60),moved_event_probability=outward(*q,digits=60),
        signed_event_difference=outward(*difference,digits=60),full_law_tv_lower=outward(tv)[0],
        event_records=dict(base=pr,moved=qr),
        independence='Proved only for I(2,15) and I(15,1): disjoint past/future of the shared tip. No independence assumption on other interval or overlap counts.',
        optimal_event_claim=False)
    summary=dict(status='FIXED_BASE_64_RAY_FAMILY_EXCLUDED' if excluded else 'HOLD_JOINT_RAY',
        uniform_full_law_tv_lower=certificate['full_law_tv_lower'],tv_gate=c['tv_gate'],
        newly_excluded_terminal_cells=30 if excluded else 0,
        total_covered_terminal_cells=old['active_cells'],complete_rays_excluded=64 if excluded else 63,
        unresolved_intervals=[] if excluded else old['unresolved_intervals'],
        inherited_states=old['states'],new_joint_event_cells=30 if excluded else 0,
        scope='No pair between the one fixed reference and its 64 declared single-node spatial rays with h in [0,0.1] simultaneously preserves the selected-node order, has symmetric weight gap >20%, and full conditional count/overlap-law TV<=1/4.' if excluded else 'One fixed joint-event certificate did not settle the inherited remaining interval.',
        not_claimed=['global stability','arbitrary pairs of displaced geometries','coordinated node motions','other reference geometries','full A/B data likelihood','physical Lorentzian continuum accuracy'])
    return certificate,summary

if __name__=='__main__':
    for name,data in zip(('certificate.json','summary.json'),run()):
        if '--verify' in sys.argv:assert data==read(HERE/name),name
        else:save(HERE/name,data)
    print(json.dumps(read(HERE/'summary.json')))
