"""Independent-coordinate diagnostics, provenance and certificate checks."""
import hashlib,json,math
from pathlib import Path
from fractions import Fraction as F
from scipy.integrate import quad
import scipy
from flint import arb,ctx
import run

ROOT=Path(__file__).resolve().parent
def require(x,msg):
    if not x:raise RuntimeError(msg)

def iterballs(obj,path=''):
    if isinstance(obj,dict):
        if 'ball' in obj:yield path,obj['ball']
        else:
            for k,v in obj.items():yield from iterballs(v,path+'/'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):yield from iterballs(v,path+'/'+str(i))

def null_quadrature(L,coeff,diag):
    q=3/(16*math.pi); aa=4*math.sqrt(q/6); H=64
    pp=[float(c)/math.factorial(n) for n,c in enumerate(coeff)]
    def outer(v):
        def inner(s):
            z=math.pi*q*s*s*v*v/24
            poly=sum(c*z**n for n,c in enumerate(pp))
            return (v-s)**2*math.exp(-z-(v*v+s*s)/(4*L*L))*poly
        return quad(inner,0,v,epsabs=1e-11,epsrel=1e-11,limit=300)[0]
    core=quad(outer,0,H,epsabs=1e-10,epsrel=1e-10,limit=300)[0]
    out=aa*(float(diag)+q*math.pi*core/2)
    # Analytic bound on v>H, evaluated with Arb. The finite SciPy integral
    # remains diagnostic, with no claim that its error estimator is a proof.
    l=arb(L);h=arb(H);qb=3/(16*arb.pi());ab=4*(qb/6).sqrt()
    C=sum(abs(run.a(c))/math.factorial(n)*(1 if n==0 else arb(n)**n*(-arb(n)).exp()) for n,c in enumerate(coeff))
    tail=ab*qb*arb.pi()/2*C*l*arb.pi().sqrt()*(2*l*l*h*(-h*h/(4*l*l)).exp()+2*l**3*arb.pi().sqrt()*(h/(2*l)).erfc())
    return out,run.enc(tail)

def main():
    ctx.prec=192
    r128=json.loads((ROOT/'results/CERTIFICATE_128.json').read_text())
    r192=json.loads((ROOT/'results/CERTIFICATE_192.json').read_text())
    b128=dict(iterballs(r128));b192=dict(iterballs(r192))
    require(b128.keys()==b192.keys(),'different target sets')
    for k in b128:require(arb(b128[k]).overlaps(arb(b192[k])),f'precision mismatch: {k}')
    src=json.loads((ROOT/'evidence/SOURCES.json').read_text())
    for x in src['files']:
        raw=(ROOT/'evidence'/x['file']).read_bytes()
        require(hashlib.sha256(raw).hexdigest()==x['sha256'],'source SHA256')
        require(hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==x['git_blob'],'source Git blob')
    old=json.loads((ROOT/'evidence/DIAGNOSIS_v015_128.json').read_text())
    baseline={z['epsilon']:arb(z['infinite_mean'][0]) for z in old['controls']}
    require(arb(r192['rows'][0]['base_mean']['ball']).overlaps(baseline['1/16']),'old L2 base')
    # Scaling identity mu(q,L=4)=mu(16q,L=2)/4 for this unchanged base kernel.
    require(arb(r192['rows'][1]['base_mean']['ball']).overlaps(baseline['1']/4),'scaled old L4 base')
    diagnostics=[]
    for row in r192['rows']:
        for key,co,diag in [('base_mean',run.C0,F(-1)),('direction_mean',run.CQ,F(-3,8)),('candidate_mean',run.CT,F(-71,8))]:
            value,tail=null_quadrature(row['L'],co,diag)
            diff=abs(value-row[key]['display_mid'])
            require(diff<1e-9,'independent coordinate integral disagreement')
            diagnostics.append({'L':row['L'],'component':key,'diagnostic_value':value,'abs_difference':diff,'H':64,'tail_bound':tail})
    require(r192['rows'][0]['candidate_passes_mean_screen'],'L2 candidate screen')
    require(not r192['rows'][1]['candidate_passes_mean_screen'],'L4 candidate rejection')
    require(arb(r192['family']['minimax_relative_bias']['ball'])>arb('0.2847'),'family lower bound')
    require(r192['METHOD']=='HOLD' and r192['G1']=='HOLD','gate laundering')
    require(r192['compact_detector_production']=='NOT_RUN_EARLY_ABORT','compact nonclaim')
    require(r192['new_random_clouds']==0 and not r192['confirmation_seed_used'],'no new ensemble')
    weights=[run.weight(n) for n in range(128)]
    require(all(abs(x)<=1331 for x in weights),'bounded binomial weights')
    # Wrong local coefficient preserves the three cancellations but changes
    # the zero-order term: it must be caught by the separate diagonal rule.
    require(F(-1)!=-3*run.dmellin(run.CT,F(1)),'negative local-diagonal control')
    checks={'status':'PASS','precision_overlap_targets':len(b128),'source_files_verified':len(src['files']),
      'rational_identity_checks_per_precision':len(r192['rational']['checks']),
      'finite_stability_checks_per_precision':len(r192['finite_stability']['checks']),
      'archival_baseline_checks':2,'binomial_weight_checks':128,
      'independent_null_coordinate_checks':diagnostics,'scipy':scipy.__version__,
      'max_diagnostic_difference':max(x['abs_difference'] for x in diagnostics),
      'diagnostic_tolerance':1e-9,'diagnostic_tolerance_is_not_a_certificate':True,
      'METHOD':'HOLD','G1':'HOLD'}
    run.write(ROOT/'results/CHECKS.json',checks)
    print(json.dumps({k:v for k,v in checks.items() if k!='independent_null_coordinate_checks'},indent=2))

if __name__=='__main__':main()
