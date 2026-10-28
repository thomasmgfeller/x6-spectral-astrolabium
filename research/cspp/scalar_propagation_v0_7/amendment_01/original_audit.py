"""Independent exact predicates, manufactured solves, derivative and error identities."""
from fractions import Fraction as F
import numpy as np
from flint import arb,acb,acb_mat,ctx
from common import check,old,balls,protocol
import geometry,initial_data as data,propagation as prop

def rational_relation(a,b):
    d=[F(float(v))-F(float(u)) for u,v in zip(a,b)]
    return d[0]>0 and d[0]**2>sum(v*v for v in d[1:])

def controls():
    near=np.nextafter(1.,0.);far=np.nextafter(1.,2.)
    points=np.array([[0,0,0,0],[1,1,0,0],[1,near,0,0],[1,far,0,0],
                     [1,0,0,0],[0,1,0,0],[-1,0,0,0],[2,0,0,0]],float)
    checks=0;fallbacks=0
    for a in points:
        for b in points:
            got,stats=geometry.relation(a,b);check(got==rational_relation(a,b),'exact rational predicate');checks+=1;fallbacks+=stats[1]
    check(fallbacks>0,'near-null exact fallback exercised')
    x=points[np.argsort(points[:,0],kind='stable')];p=np.array([[3,0,0,0],[1,0,0,0]],float)
    cc,pc,past,pp,stats=geometry.inventory(x,p)
    for i,a in enumerate(x):
        for j,b in enumerate(x):
            expected=sum(rational_relation(b,z) and rational_relation(z,a) for z in x) if rational_relation(b,a) else -1
            check(cc[i,j]==expected,'independent exact interval enumeration')
    for i,a in enumerate(p):
        for j,b in enumerate(x):
            expected=sum(rational_relation(b,z) and rational_relation(z,a) for z in x) if rational_relation(b,a) else -1
            check(pc[i,j]==expected,'independent exact probe enumeration')
    # Equal probe counts do not by themselves pin the internal causal graph.
    x1=np.array([[-2,0,0,0],[-1,0,0,.5]],float);x2=x1.copy();x2[1,3]=2
    y=np.array([[-3,0,0,0]],float)
    c1,p1,r1,_,_=geometry.inventory(x1,y);c2,p2,r2,_,_=geometry.inventory(x2,y)
    check(np.array_equal(p1,p2) and not np.array_equal(r1,r2),'missing internal-relation guard negative control')
    # Independent dense ball solve on a small exact chronological chain.
    x=np.array([[-2,0,0,0],[-1.5,0,0,0],[-.5,0,0,0],[0,0,0,0],[.5,0,0,0]],float)
    p=np.array([[1,0,0,0]],float);cc,pc,*_=geometry.inventory(x,p)
    h=[[acb(1)],[acb(2)]];nh=2
    out,values,gain,erows,prows=prop.solve(cc,pc,512,'1/4',1,h,nh)
    A=acb_mat(3,3);b=acb_mat(3,1)
    for i in range(3):
        A[i,i]=1
        for j,w in erows[i+nh]:
            if j<nh:b[i,0]+=w*h[j][0]
            else:A[i,j-nh]-=w
    exact=A.solve(b,algorithm='lu')
    check(all(exact[i,0].overlaps(values[i+nh][0]) for i in range(3)),'independent dense solve')
    # The full induced norm on this small graph is computed by every basis response.
    basis=[[acb(1),acb(0)],[acb(0),acb(1)]]
    br=prop.solve(cc,pc,512,'1/4',1,basis,nh)[0][0]
    check(sum(z.abs_upper() for z in br)<=gain[0].upper(),'history gain bounds all basis directions')
    wrong=out[0][0]+1
    check(not wrong.overlaps(out[0][0]),'wrong solution rejected by forward enclosure')
    # Independent finite differences check analytic compact-source jets; regression only.
    A0=data.source.normalization(ctx.prec)[0];point=[-1.,.1,.05,.15];eps=arb('0.000001')
    f,g,lap,_=data.bump_jets(point,1,A0);fd=acb(0)
    for j in range(1,4):
        lo=point.copy();hi=point.copy();lo[j]-=float(eps);hi[j]+=float(eps)
        fd+=(data.bump_jets(lo,1,A0)[0]-2*f+data.bump_jets(hi,1,A0)[0])/(eps*eps)
    check((fd-f-lap).abs_upper()<arb('1e-5'),'compact Laplacian regression')
    for k in [0,2,4,8]:
        exact,f,g,l2,l3=data.wave([-1,0,0,.25],k)
        for order in [1,3]:
            check(data.extension([-1,0,0,.25],(f,g,l2,l3),order).overlaps(f),'adapter initial value')
        check(g.overlaps(-acb(0,(arb(k*k)+1).sqrt())*f),'adapter initial derivative')
    return {'exact_pair_predicates':checks,'near_null_fallbacks_exercised':fallbacks,
            'exact_interval_enumerations':80,'missing_internal_relation_negative_control':True,
            'independent_dense_ball_solve':True,'all_history_basis_directions_checked':True,
            'incorrect_forward_solution_negative_control':True,'compact_jet_finite_difference_regression':True,
            'initial_values_and_derivatives_checked':True,'status':'PASS'}

def validate(record):
    rows=record['rows'];check(len(rows)==201,'complete 201 cells')
    expected={(f'd{d}_r{i:02d}','wave',1,e) for d in range(4) for i in range(16) for e in protocol()['epsilon']}
    expected|={('d0_r00','compact',m,e) for m in [0,1,2] for e in protocol()['epsilon']}
    check({(r['key'],r['kind'],r['mass'],r['epsilon']) for r in rows}==expected,'fixed identities')
    check(record['scientific_status']=={'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'} and record['new_random_realizations']==0,'scope and gates')
    total=0
    for r in rows:
        check(len(r['fields'])==(8 if r['kind']=='wave' else 2),'all fields and adapters')
        for f in r['fields']:
            total+=1;check(len(f['probe_values'])==28,'28 observations')
            check(set(f['component_RMS'])==set(protocol()['error_components']),'four separate contributions')
            for value in f['probe_values']:
                z=balls.decode(value);check(z.is_finite() and max(z.real.rad(),z.imag.rad())<=arb(protocol()['solution_component_radius_max']),'meaningful solution enclosure')
            check(f['relative_10pct_screen'] in ['WITHIN','EXCEEDS','UNDECIDED'],'complete failure accounting')
    check(total==1554,'1536 wave field/adapter cases plus 18 compact cases')
    return total

def compare(low,high):
    validate(low);validate(high)
    check(low['geometry']==high['geometry'],'same exact graph and masks at both precisions')
    n=0
    for a,b in zip(low['rows'],high['rows']):
        check((a['key'],a['kind'],a['mass'],a['epsilon'])==(b['key'],b['kind'],b['mass'],b['epsilon']),'replay identities')
        for x,y in zip(a['fields'],b['fields']):
            check((x['field'],x['adapter_order'])==(y['field'],y['adapter_order']),'field identity')
            check(x['relative_10pct_screen']==y['relative_10pct_screen'],'stable diagnostic screen')
            for u,v in zip(x['probe_values'],y['probe_values']):check(balls.decode(u).overlaps(balls.decode(v)),'solution overlap');n+=1
    return {'status':'PASS','field_adapter_cases':1554,'overlapping_amplitudes':n,'precision_bits':[128,192],'precision_overlap_is_regression_not_proof':True}
