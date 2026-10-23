"""One post-screen joint Poisson certificate, preserving the original HOLD.
SPDX-License-Identifier: Apache-2.0
"""
from cm_run import *
sys.path.insert(0,str(HERE.parent/'joint_ray_obstruction'))
import jr_run as jr

def joint():
    for name,digest in read(HERE/'joint_freeze.json')['files'].items():
        assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==digest,name
    c=read(HERE/'joint_contract.json');rows=read(HERE/'candidates.json');r=rows[c['candidate']]
    assert r['status']=='HOLD'
    old=read(HERE/'summary.json');assert old['unresolved_indices']==[c['candidate']]
    ray=read(HERE/'directions.json')[r['ray']];w,z,ends=geometry();zz=moved(z,ray,F(r['step']))
    certify_order(zz,w['full_order']);pi=pi_bounds()
    allmeans=[means(w,v,ends,pi) for v in (z,zz)];pairs=[c['statistics'][s]['interval'] for s in ('X','Y')]
    x,y=pairs;assert x[1]==y[0]==5
    for v in (z,zz):
        # All points of X precede tip 5, all points of Y follow it.
        assert v[x[0]][0]<v[5][0]<v[y[1]][0]
        assert direct_interval(v,*x)>0 and direct_interval(v,*y)>0
    selected=[]
    for mu in allmeans:
        block=[]
        for name,pair in zip(('X','Y'),pairs):
            k=c['statistics'][name]['index'];assert list(ends[k])==pair;block.append(mu[k])
        selected.append(block)
    # Check declared midpoint rule from exact mean enclosures.
    values=[(y[0]-2*x[1],y[1]-2*x[0]) for x,y in selected]
    mid=((values[0][0]+values[1][0])/2,(values[0][1]+values[1][1])/2)
    assert all(v.numerator//v.denominator==c['event']['threshold'] for v in mid)
    probabilities=[];records=[]
    for block in selected:
        p,record=jr.enclose_event(*block,c);probabilities.append(p);records.append(record)
    p,q=probabilities;lower=max(F(0),p[0]-q[1],q[0]-p[1]);excluded=lower>F(c['tv_gate'])
    cert=dict(candidate=c['candidate'],statistics=c['statistics'],event=c['event'],
        mean_intervals=[[[str(v) for v in p] for p in block] for block in selected],
        event_probability=[outward(*p,digits=60) for p in probabilities],
        full_law_tv_lower=outward(lower)[0],event_records=records,
        independence='Only I(2,5) and I(5,1), proved disjoint under BOTH geometries. No independence of other counts.',
        gap=r['relative'],domain='ONE_EXACT_PAIRED_CANDIDATE')
    summary=dict(status='FINITE_PAIRED_GRID_EXCLUDED' if excluded else 'HOLD_COORDINATED_LAW',
        candidate_count=old['candidates'],paired_rays_sampled=old['rays'],initial_screen=old['states'],
        joint_candidate=c['candidate'],joint_full_law_tv_lower=cert['full_law_tv_lower'],
        newly_excluded=1 if excluded else 0,unresolved_indices=[] if excluded else [c['candidate']],
        scope='No strong close-law pair in these 420 sampled coupled motions. All-step paired-ray coverage and general stability remain OPEN.')
    return cert,summary

def direct_interval(v,a,b):
    t,x,y=[q-p for p,q in zip(v[a],v[b])]
    return t*t-x*x-y*y

if __name__=='__main__':
    for name,result in zip(('joint_certificate.json','joint_summary.json'),joint()):
        if '--verify' in sys.argv:assert result==read(HERE/name),name
        else:save(HERE/name,result)
    print(json.dumps(read(HERE/'joint_summary.json')))
