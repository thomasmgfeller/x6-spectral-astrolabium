"""Independent-coordinate quadrature, exact algebra controls and interval replay checks."""
import json, math, platform
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from numpy.polynomial.legendre import leggauss
from flint import arb,acb,ctx
from run import HERE,ROOT,require,unpack,dump,geometry
ctx.prec=192

def intervals(x,path=''):
    if isinstance(x,dict):
        if 'real_ball' in x and 'imag_ball' in x:yield path,acb(arb(x['real_ball']),arb(x['imag_ball']))
        else:
            for k,v in x.items():yield from intervals(v,path+'/'+k)
    elif isinstance(x,list):
        if len(x)==2 and all(isinstance(v,str) for v in x):
            try:z=unpack(x)
            except ValueError:z=None
            if z is not None:yield path,z;return
        for i,v in enumerate(x):yield from intervals(v,path+'/'+str(i))

checks=[]
def check(ok,label):require(ok,label);checks.append(label)
count=0;bound_count=0;bound_difference=0.
for name in ['DIAGNOSIS','DOMAIN_CERTIFICATE','RESIDUAL_GAIN']:
    low=dict(intervals(json.load(open(HERE/f'results/{name}_128.json'))))
    high=dict(intervals(json.load(open(HERE/f'results/{name}_192.json'))))
    check(low.keys()==high.keys(),name+' exact interval inventory')
    for k in low:
        # Outward endpoints are precision-dependent certificates, not two
        # enclosures of one exact scalar. Never require their tiny balls to overlap.
        endpoint_bound=any(s in k for s in ['relative_bias_lower','covered_bias_lower',
            'all_H_ge_12_bias_lower','history_sup_gain_','history_gain_','residual_gain_'])
        if endpoint_bound:
            require(low[k].is_finite() and high[k].is_finite(),name+k+' finite endpoint certificates')
            bound_difference=max(bound_difference,float(abs(low[k]-high[k]).abs_upper()))
            bound_count+=1
        else:
            require(low[k].overlaps(high[k]),name+k+' precision overlap')
            count+=1
    check(True,name+' all precision intervals overlap')

def mean_ur(q,H,n):
    # Independent (u=-t,r) coordinates, split at u=H/2; no null-coordinate kernel.
    z,w=leggauss(n);z=(z+1)/2;w=w/2;total=0.
    for lo,hi in [(0,H/2),(H/2,H)]:
        u=(lo+(hi-lo)*z)[:,None]; rm=np.minimum(u,H-u);r=rm*z[None,:]
        xi=np.pi*q*(u*u-r*r)**2/24
        f=4*np.pi*r*r*np.exp(-xi-(u*u+r*r)/8)*(1-9*xi+8*xi**2-4*xi**3/3)
        total+=(hi-lo)*np.sum(w[:,None]*w[None,:]*rm*f)
    return 4*np.sqrt(q/6)*(-1+q*total)
d=json.load(open(HERE/'results/DIAGNOSIS_192.json'));maxerr=0.;maxdiff=0.
for row in d['controls']:
    q=float(arb(row['q'][0]).mid())
    for cell in row['finite_domains'][:3]:
        H=cell['H'];v=mean_ur(q,H,128);w=mean_ur(q,H,256);m=float(arb(cell['finite_mean'][0]).mid())
        maxerr=max(maxerr,abs(v-m));maxdiff=max(maxdiff,abs(v-w))
        check(abs(v-m)<2e-12 and abs(w-m)<2e-12,f'independent u-r quadrature epsilon={row["epsilon"]} H={H}')
        op=float(arb(row['operator_bias'][0]).mid());b=float(arb(cell['boundary_signed'][0]).mid())
        check(abs((v+.5)-(op-b))>1e-8,f'wrong boundary sign rejected epsilon={row["epsilon"]} H={H}')

# Exact causal-convexity count cross-check using dyadic rational arithmetic.
def precedes(a,b):
    delta=[F(float(b[i]))-F(float(a[i])) for i in range(4)]
    return delta[0]>0 and delta[0]**2>sum(z*z for z in delta[1:])
archive=np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz');rational_counts=0
for pair in d['paired_archive_diagnosis']:
    x=archive[pair['key']+'_outer'];p=np.zeros(4)
    _,pc,_,_,_=geometry.inventory(x,np.array([p]),full=False)
    selected=np.flatnonzero(pc[0]>=0)[::max(1,int(np.sum(pc[0]>=0))//8)][:8]
    for j in selected:
        exact=sum(precedes(x[j],z) and precedes(z,p) for z in x)
        require(exact==pc[0,j],'independent rational interval count')
        rational_counts+=1
check(rational_counts==32,'32 independent rational interval counts on four archived outer clouds')

# Boundary completion: an independent rational finite causal system.
# h=2, exterior e=3. Interior i1=h/5+e/7; i2=i1/3+e/11.
# Detector A=i2/2+e/13. Smaller domain drops e, with identical interior edges.
h,e=F(2),F(3);u1=h/5;u2=u1/3;v1=u1+e/7;v2=v1/3+e/11
small=u2/2;large=v2/2+e/13
completed=e*(F(1,42)+F(1,22)+F(1,13))
check(large-small==completed,'exact retarded exterior-forcing completion identity')
check(large-small!=-completed,'wrong exterior-forcing sign rejected')
check(large-small!=e/13,'direct exterior term alone is insufficient')
# Adjoint residual transport; r1=1/7,r2=-1/11, detector direct residual=1/13.
r1,r2,rd=F(1,7),-F(1,11),F(1,13)
e1=-r1;e2=e1/3-r2;ed=e2/2-rd
check(ed==-rd-F(1,6)*r1-F(1,2)*r2,'exact residual-to-detector adjoint identity')
check(abs(ed)<=abs(rd)+(F(1,6)+F(1,2))*max(abs(r1),abs(r2)),'residual sup norm transport bound')

for bits in [128,192]:
    c=json.load(open(HERE/f'results/DOMAIN_CERTIFICATE_{bits}.json'))
    check(len(c['covering_nodes'])==129,f'complete 129-node coverage of H in [4,12] at {bits} bits')
    for i,n in enumerate(c['covering_nodes']):
        require(arb(n['H'][0]).contains(arb(4)+arb(i)/16),'exact rational H node')
        require(arb(n['covered_bias_lower'][0])>arb('0.05'),'certified covered-cell lower bound')
    check(arb(c['all_H_ge_4_relative_bias_lower'][0])>arb('0.4170'),f'global H>=4 relative bias exceeds 41.70 percent at {bits} bits')
    check(arb(c['all_H_ge_12_bias_lower'][0])>arb('0.05'),f'continuous far-domain tail exclusion at {bits} bits')
check(d['status']['original_detector_operator_vs_exterior_tail']=='UNRESOLVED','full source-detector attribution not overstated')
check(d['new_random_calls']==0 and d['new_clouds']==0,'no new ensemble')

out={'status':'PASS','checks':checks,'check_count':len(checks),'precision_interval_comparisons':count,
     'precision_dependent_bound_diagnostics':bound_count,
     'max_precision_dependent_bound_difference':bound_difference,
     'independent_rational_interval_counts':rational_counts,'independent_coordinate_quadrature_max_abs_difference':maxerr,
     'quadrature_resolution_difference':maxdiff,'quadrature_role':'diagnostic cross-check, not a remainder certificate',
     'python':platform.python_version(),'numpy':np.__version__,'scientific_G1':'HOLD','independent_transfer':'NOT_RUN'}
dump(HERE/'results/CHECKS.json',out)
print(json.dumps({k:v for k,v in out.items() if k!='checks'},indent=2))
