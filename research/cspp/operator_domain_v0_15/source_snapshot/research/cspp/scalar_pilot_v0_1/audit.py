"""Independent controls and publication replay. Passing is software evidence, not G1."""
import argparse
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import tempfile
import numpy as np
from scipy.integrate import quad
from fields import fields
from scalar import HERE, counts, weights, points, probes, apply, propagate, sprinkle, extend, digest, volume
from reference import evaluate, interpolate, source, source_norm
from run import frozen, summarize

def require(test,label):
    if not bool(test):raise RuntimeError('AUDIT FAIL: '+label)
    return label
def exact_before(a,b):
    d=[Fraction(float(y))-Fraction(float(x)) for x,y in zip(a,b)]
    return d[0]>0 and d[0]**2>sum(z*z for z in d[1:])
def independent_counts(x,p):
    relation=np.array([[exact_before(a,b) for a in x] for b in x])
    pp=np.array([[exact_before(a,b) for a in x] for b in p])
    out=np.full(relation.shape,-1,np.int32);po=np.full(pp.shape,-1,np.int32)
    for i,j in zip(*np.where(relation)):out[i,j]=np.count_nonzero(relation[i]&relation[:,j])
    for i,j in zip(*np.where(pp)):po[i,j]=np.count_nonzero(pp[i]&relation[:,j])
    return out,po
def direct_weight(n,e):
    return sum(c*math.comb(n,k)*e**k*(1-e)**(n-k) for k,c in enumerate([1,-9,16,-8]) if k<=n) if n>=0 else 0.
def self_test():
    checks=[];g=np.random.Generator(np.random.PCG64DXSM(314159))
    x=points(g,37);p=np.array([[-.25,0,0,0],[.7,.2,0,0]])
    a,b=counts(x,p);aa,bb=independent_counts(x,p)
    checks.append(require(np.array_equal(a,aa) and np.array_equal(b,bb),'all toy interval counts against exact-rational brute force'))
    boost=np.array([[1.25,.75,0,0],[.75,1.25,0,0],[0,0,1,0],[0,0,0,1.]])
    y=x@boost.T;order=np.argsort(y[:,0]);aa,bb=counts(y[order],p@boost.T)
    checks.append(require(np.array_equal(aa,a[order][:,order]) and np.array_equal(bb,b[:,order]),'joint Lorentz transform preserves toy interval counts'))
    for e in [1,.25,.0625]:
        n=np.arange(-1,81)
        checks.append(require(np.allclose(weights(n,e),[direct_weight(int(k),e) for k in n],rtol=2e-13,atol=2e-14),f'binomial weight oracle epsilon={e}'))
    for e in [0,-1,1.1]:
        try:weights([0],e)
        except ValueError:pass
        else:raise RuntimeError('invalid epsilon accepted')
    checks.append('invalid epsilon rejected')
    test=np.array([[.3,.2,.1,.4],[1.7,.8,.4,1.1],[-1.8,.2,.9,1.4]])
    f,box=fields(test);h=1e-4;num=np.zeros_like(f)
    for j in range(4):
        dx=np.zeros(4);dx[j]=h
        num+=(-1 if j==0 else 1)*(fields(test+dx)[0]-2*f+fields(test-dx)[0])/h**2
    checks.append(require(np.allclose(box,num,atol=4e-5,rtol=3e-5),'analytic Box against centered numerical derivative'))
    checks.append(require(np.max(np.abs(box+num))>.1,'wrong Box sign detected'))
    # Independent row recursion, using scalar math.comb weights, checks the solve.
    x=points(g,90);p=probes()[:28];cc,pc=counts(x,p);f,bf=fields(x);fp,bp=fields(p)
    hist=f[:,6:];J=bf[:,6:]-hist;Jp=bp[:,6:]-fp[:,6:];rho=2.;e=.25
    calculated,res=propagate(cc,pc,x,p,rho,e,hist,J,Jp,[1]*4)
    aa=4/math.sqrt(6)*math.sqrt(e*rho);v=hist.copy()
    for i in range(len(x)):
        if x[i,0]>-1:
            v[i]=(aa*e*sum((direct_weight(int(cc[i,j]),e)*v[j] for j in range(i)),start=np.zeros(4,complex))-J[i])/(aa+1)
    expected=[]
    for i in range(len(p)):
        expected.append((aa*e*sum((direct_weight(int(pc[i,j]),e)*v[j] for j in range(len(x))),start=np.zeros(4,complex))-Jp[i])/(aa+1))
    checks.append(require(np.allclose(calculated,expected,atol=1e-11,rtol=1e-11) and res<1e-13,'retarded triangular solve against independent row recursion'))
    # Exact zero history/forcing stays zero; cancellation guards not normalization.
    z,_=propagate(cc,pc,x,p,rho,e,hist*0,J*0,Jp*0,[1]*4)
    checks.append(require(np.array_equal(z,np.zeros_like(z)),'zero solution preserved'))
    norm,_=quad(lambda r:4*np.pi*r*r*abs(source(np.array([[0,0,r]]))[0])**2,0,.5,epsabs=1e-12)
    checks.append(require(abs(norm-1)<2e-12,'compact-source continuum normalization'))
    n=16;L=12.;q=(np.arange(n)-n//2)*L/n;xyz=np.array([[q[i],q[j],q[k]] for i,j,k in [(0,0,0),(2,7,10),(15,14,1)]])
    grid=np.exp(2j*np.pi*(np.arange(n)[:,None,None]+2*np.arange(n)[None,:,None]+3*np.arange(n)[None,None,:])/n)
    expected=np.exp(2j*np.pi*((xyz[:,0]+6)+2*(xyz[:,1]+6)+3*(xyz[:,2]+6))/L)
    checks.append(require(np.allclose(interpolate(grid,xyz,L),expected,atol=1e-13),'Fourier grid interpolation at exact nodes'))
    import reference as reference_module
    saved_source=reference_module.source
    mode=2*np.pi/L
    query=np.column_stack([[-.5,.5,1.],xyz])
    try:
        reference_module.source=lambda v:np.exp(1j*mode*np.asarray(v)[...,2])
        computed,_=reference_module.evaluate(query,16,.125)
    finally:
        reference_module.source=saved_source
    exact=np.exp(1j*mode*xyz[:,2,None])*np.cos(np.sqrt(mode*mode+np.array([0,1,2])**2)[None,:]*(query[:,0,None]+1))
    checks.append(require(np.allclose(computed,exact,atol=1e-13),'Fourier KG evolution against exact periodic plane mode for all three masses'))
    # Null-sensitive control must block an unresolved exactly-null comparison.
    try:counts(np.array([[0.,0,0,0],[1.,1,0,0]]),np.empty((0,4)))
    except RuntimeError:checks.append('unresolved null pair blocks computation')
    else:raise RuntimeError('near-null guard failed')
    return checks
def replay(out):
    from prepare_reference import prepare
    prepare()
    frozen();z=np.load(out/'metrics.npz');clouds=np.load(out/'clouds.npz');ref=np.load(out/'reference.npz')
    records=json.loads((out/'RUNS.json').read_text());p=probes();fp,bp=fields(p)
    original=json.loads((HERE/'amendment_01/UNCHANGED_PRIMARY_HASHES.json').read_text())
    for key,value in original.items():
        require(digest(z[key])==value,'amendment leaves primary array unchanged: '+key)
    count=0;maxdelta=0.
    for r in records:
        d,i,key=r['density_index'],r['realization_index'],r['key']
        if r['status']!='COMPUTED_DIAGNOSTIC':raise RuntimeError('HOLD: replay requires all planned run statuses to be resolved')
        x=sprinkle(d,i);require(np.array_equal(x,clouds[key]),'seed replay '+key)
        require(digest(x)==r['coordinates_sha256'],'raw cloud hash '+key)
        cc,pc=counts(x,p);require(digest(cc)==r['interval_counts_sha256'] and digest(pc)==r['probe_counts_sha256'],'count replay '+key)
        f,b=fields(x);h=np.column_stack([f[:,6:],ref[key+'_fine'],np.ones(len(x))])
        J=np.column_stack([b[:,6:]-f[:,6:],np.zeros((len(x),4))]);Jp=np.column_stack([bp[:28,6:]-fp[:28,6:],np.zeros((28,4))])
        for ei,e in enumerate([1,.25,.0625]):
            rho=r['nu']/volume(4)
            op=apply(pc,rho,e,f,fp)
            v,res=propagate(cc,pc[:28],x,p[:28],rho,e,h,J,Jp,[1,1,1,1,0,1,2,1])
            require(np.allclose(op,z['operator'][d,i,ei],atol=1e-10,rtol=1e-11),'operator replay '+key)
            require(np.allclose(v,z['propagation'][d,i,ei],atol=1e-10,rtol=1e-11) and res<1e-12,'propagation replay '+key)
            maxdelta=max(maxdelta,float(np.max(np.abs(v-z['propagation'][d,i,ei]))))
        if 'outer_metric_index' in r:
            y=extend(x,d,i);require(np.array_equal(y,clouds[key+'_outer']),'paired shell replay '+key)
            _,oc=counts(y,p,full=False);require(digest(oc)==r['outer_probe_counts_sha256'],'outer count replay '+key)
            fy,_=fields(y)
            for ei,e in enumerate([1,.25,.0625]):
                require(np.allclose(apply(oc,rho,e,fy,fp),z['outer_operator'][r['outer_metric_index'],ei],atol=1e-10,rtol=1e-11),'paired operator replay '+key)
        count+=1
    for label,n,dt in [('coarse',64,.125),('fine',128,.0625)]:
        v,_=evaluate(p[:28],n,dt)
        require(np.allclose(v,ref['probes_'+label],atol=1e-12,rtol=1e-11),'independent probe Fourier replay '+label)
    # Recompute all published summaries rather than trusting rounded prose.
    with tempfile.TemporaryDirectory() as tmp:
        temp=Path(tmp)
        for name in ['metrics.npz','reference.npz','RUNS.json']:(temp/name).symlink_to((out/name).resolve())
        summarize(temp)
        require(json.loads((temp/'RESULTS.json').read_text())==json.loads((out/'RESULTS.json').read_text()),'exact summary replay')
    return {'runs_replayed':count,'maximum_propagation_absolute_replay_difference':maxdelta,'status':'PASS_SOFTWARE_REPLAY_NOT_G1'}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--replay',action='store_true');ap.add_argument('--output',type=Path);a=ap.parse_args()
    result={'checks':self_test(),'status':'PASS_SOFTWARE_CONTROLS_NOT_G1'}
    if a.replay:result['replay']=replay(HERE/'results')
    text=json.dumps(result,indent=2)+'\n'
    if a.output:a.output.write_text(text)
    print(text)
if __name__=='__main__':main()
