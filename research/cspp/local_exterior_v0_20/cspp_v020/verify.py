"""Cross-precision, provenance, invariant and deliberately failing controls."""
import gzip, hashlib, json, math
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx
from overlap import point, before, geometry, lens_quadrature
from kernel import absolute_expectation
from run import cunpack, write, require, ROOTS

HERE=Path(__file__).resolve().parent

def scaled_integer_before(a,b):
    a,b=point(a),point(b)
    den=max(v.denominator for v in a+b)
    aa=[v.numerator*(den//v.denominator) for v in a]
    bb=[v.numerator*(den//v.denominator) for v in b]
    d=[v-u for u,v in zip(aa,bb)]
    return d[0]>0 and d[0]**2>sum(v*v for v in d[1:])

def verify():
    ctx.prec=256
    a=json.loads((HERE/'results/LOCAL_128.json').read_text())
    b=json.loads((HERE/'results/LOCAL_192.json').read_text())
    same=[];bounds=[];counters={'physical_ball_overlaps':0,'majorant_stability_checks':0,'integer_count_checks':0,'negative_controls':0,'table_point_checks':0,'source_blobs':0}
    def ov(x,y):
        require(arb(x).overlaps(arb(y)),'cross precision physical overlap');counters['physical_ball_overlaps']+=1
    ov(a['source_L1'],b['source_L1']);ov(a['G25'],b['G25'])
    for x,y in zip(a['roots'],b['roots']):
        for u,v in zip(x['KG'],y['KG']):ov(u,v)
        z=cunpack(y['KG']);require(max(z.real.rad(),z.imag.rad())<arb('1e-18'),'fixed KG radius')
    archive=np.load(HERE/'evidence/archived_omega5.npz')
    kappa=arb('4976184375/4294967296')
    for x,y in zip(a['archives'],b['archives']):
        require(x['active_archive_indices']==y['active_archive_indices'],'fixed active nodes')
        require(len(x['probes'])==len(y['probes']),'same causal probes')
        xx=archive[x['key']+'_outer']
        for p,q in zip(x['probes'],y['probes']):
            require((p['root'],p['archive_index'],p['n0'],p['branch'])==(q['root'],q['archive_index'],q['n0'],q['branch']),'same probe topology')
            root=ROOTS[p['root']];end=xx[p['archive_index']]
            n=sum(scaled_integer_before(root,z) and scaled_integer_before(z,end) for z in xx)
            require(n==p['n0'],'independent integer-scaled count');counters['integer_count_checks']+=1
            for key in ['rho_V_total','rho_V_overlap','mu_outside','E_abs_w']:ov(p[key],q[key])
            require((arb(q['rho_V_total'])-arb(q['rho_V_overlap'])).overlaps(arb(q['mu_outside'])),'volume split')
            require(0<arb(q['E_abs_w'])<kappa,'conditional weight range')
        for lx,ly in zip(x['levels'],y['levels']):
            require(lx['grid']==ly['grid'] and ly['cells']==ly['grid']**4,'partition complete')
            for wx,wy in zip(lx['windows'],ly['windows']):
                terms=sum((arb(wy[k]) for k in ['direct_detector_upper','known_active_transport_upper','unknown_active_paths_upper']),arb(0))
                require(terms.overlaps(arb(wy['patch_total_upper'])),'complete path-class sum')
                for key in ['direct_detector_upper','known_active_transport_upper','unknown_active_paths_upper','patch_total_upper']:
                    u,v=arb(wx[key]),arb(wy[key]);require(u>0 and v>0,'positive upper bounds')
                    require(abs(u-v)<arb('1e-8')*v,'upper construction precision stability');counters['majorant_stability_checks']+=1
                require(arb(wy['patch_total_upper'])<arb(ly['uniform_gain_patch_upper']),'actual inner transport improves uniform gain')
            with gzip.open(HERE/f"results/CELLS_192_{y['key']}_{ly['grid']}.json.gz",'rt') as f:cells=json.load(f)
            require(len(cells)==ly['cells'] and len({tuple(c['index']) for c in cells})==ly['cells'],'no cell duplication')
            for c in cells:
                require(all(lo<=hi for lo,hi in zip(c['n0_lower'],c['n0_upper'])),'ordered count enclosures')
                require(all(0<=arb(v)<=kappa for v in c['kernel_upper']+c['detector_kernel_upper']),'cell kernel caps')
        for wi in range(2):require(arb(y['levels'][-1]['windows'][wi]['patch_total_upper'])<arb(y['levels'][0]['windows'][wi]['patch_total_upper']),'refined partition improves bound')
    # Exact controls, including nested and Lorentz-boosted geometries.
    p=point([1,0,0,F(3,2)]);y=point([-6,0,0,2]);r=geometry(y,p)
    require(r[1].contains(arb('16731/128')),'exact lens control')
    require(r[1].overlaps(lens_quadrature(y,p)),'independent cap integral')
    require(geometry([-6,0,0,0],p)[2].contains(arb('2093/16')),'v19 nested control')
    def boost(q):
        t=q[0]+5;z=q[3]
        return (F(5,4)*(t-F(3,5)*z)-5,q[1],q[2],F(5,4)*(z-F(3,5)*t))
    require(r[1].overlaps(geometry(boost(y),boost(p))[1]),'Lorentz invariance')
    require(r[1].overlaps(geometry([y[0],y[3],y[1],y[2]],[p[0],p[3],p[1],p[2]])[1]),'spatial rotation')
    require(geometry([2,0,0,0],p)[3]=='noncausal','future root excluded')
    require(geometry([-4,0,0,0],p)[2]==0,'nested future exterior volume zero')
    # Deliberately invalid assumptions must be rejected by the checks.
    for bad in [lambda:require(r[1].overlaps(r[0]),'all interval wrongly treated as overlap'),
                lambda:geometry([-6,0,0,0],[5,0,0,0]),
                lambda:require(a['archives'][0]['probes'][0]['n0']==-1,'corrupted count')]:
        try:bad()
        except (ArithmeticError,ValueError):counters['negative_controls']+=1
        else:raise ArithmeticError('negative control accepted')
    for rec in json.loads((HERE/'PROVENANCE.json').read_text())['source_files']:
        if rec['package_path'] is None:continue
        d=(HERE/rec['package_path']).read_bytes()
        sha=hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()
        require(sha==rec['git_blob_sha1'],'pinned Git blob');counters['source_blobs']+=1
    table=np.load(HERE/'results/KERNEL_TABLE_192.npy')
    for n in [0,1,20,21,69,70,71,128,191]:
        for j in [0,1,4,16,32,64,128,256,511]:
            for frac in ['0','1/2','1']:
                mu=arb(2*j)+2*arb(frac);e=absolute_expectation(n,mu)
                require(e<=arb(float(table[n,j])),'outward table point control');counters['table_point_checks']+=1
    require(a['status']==b['status'] and b['new_random_calls']==0,'unchanged hold and no new random calls')
    result={'status':'PASS','counters':counters,'internal_run_checks':b['checks'],
       'independent_external_review':'NOT_CLAIMED','global_complement':'NOT_NEWLY_CERTIFIED'}
    write(HERE/'results/CHECKS.json',result);print(json.dumps(result,indent=2));return result

if __name__=='__main__':verify()
