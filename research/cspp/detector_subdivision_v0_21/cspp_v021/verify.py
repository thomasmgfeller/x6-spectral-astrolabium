"""Independent integer counts, physical volumes, monotonicity and mass checks."""
import gzip,hashlib,json,math,sys,itertools
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb,ctx
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vendor_v020'))
from overlap import point,geometry,ball
from kernel import weight,absolute_expectation
from envelope import H,expected_H,certificate,upper
from domains import detector_cells,whole_detector,root_masks,detector_masks
import importlib.util
sp=importlib.util.spec_from_file_location('previous_run',HERE/'vendor_v020/run.py')
prev=importlib.util.module_from_spec(sp);sp.loader.exec_module(prev)
require=prev.require
def readgz(p):
    with gzip.open(p,'rt') as f:return json.load(f)

def integer_relation(center,half,z,first):
    """Independent integer arithmetic, explicit eight spatial corners."""
    center=point(center);half=point(half);z=point(z)
    den=math.lcm(*(v.denominator for v in center+half+z))
    cv=[int(v*den) for v in center];hv=[int(v*den) for v in half];zv=[int(v*den) for v in z]
    dt=zv[0]-cv[0] if first else cv[0]-zv[0]
    ds=[sum((cv[j]+s*hv[j]-zv[j])**2 for j,s in zip(range(1,4),signs)) for signs in itertools.product([-1,1],repeat=3)]
    nearest=[max(cv[j]-hv[j],min(cv[j]+hv[j],zv[j])) for j in range(1,4)]
    near=sum((v-zv[j])**2 for j,v in zip(range(1,4),nearest))
    return dt-hv[0]>0 and (dt-hv[0])**2>max(ds), dt+hv[0]>0 and (dt+hv[0])**2>near

def verify():
    ctx.prec=256
    counter={'physical_volume_overlaps':0,'kernel_majorants_checked':0,'integer_box_count_checks':0,
             'point_kernel_dominance_checks':0,'direct_poisson_controls':0,'source_blobs':0,'negative_controls':0}
    results=[json.loads((HERE/f'results/DETECTOR_{b}.json').read_text()) for b in [128,192]]
    old=json.loads((HERE/'evidence/v20_LOCAL_192.json').read_text())
    roots=prev.field_cells(4,arb(old['source_L1']));frozen=np.load(HERE/'evidence/v20_archived_omega5.npz')
    cap=arb('4976184375/4294967296');cert=certificate()
    require(results[0]['monotone_envelope_certificate']==results[1]['monotone_envelope_certificate']==cert,'same exact proof')
    for n in range(512):require(H(n)>=abs(weight(n)) and H(n)>=H(n+1),'pointwise suffix envelope')
    # Different evaluation: direct Poisson summation of the suffix function.
    for n in [0,8,36,70,94,95,128,192]:
        for m in [F(0),F(1,4),F(8),F(64),F(256)]:
            mu=ball(m);p=(-mu).exp();s=arb(0);cut=1024
            for j in range(cut+1):s+=p*ball(H(n+j));p*=mu/(j+1)
            tail=arb(0) if not m else (-mu).exp()*(arb(1).exp()*mu/(cut+1))**(cut+1)*cap
            direct=s+arb(0).union(tail)
            require(expected_H(n,mu).overlaps(direct),'independent suffix Poisson sum')
            require(absolute_expectation(n,mu).upper()<=expected_H(n,mu).upper()+arb('1e-60'),'H dominates absolute kernel')
            counter['direct_poisson_controls']+=1
    domains={(wi,n):detector_cells(n,wi)[0] for wi in range(2) for n in [2,4]}
    mass=results[1]['mass_certificate'];require(mass==results[0]['mass_certificate'],'same exact mass enclosure')
    resolved=arb(results[1]['resolved_detector_mass_lower'])
    require(0<resolved<1,'partial detector mass covered')
    for wi in range(2):
        for n in [2,4]:
            ds=domains[wi,n];require(len(ds)==n**4,'complete detector box partition')
            require(sum((d['volume_time_fraction'] for d in ds),F(0))==F(mass['inside_volume']),'all voxel mass exactly once')
        for di,d in enumerate(domains[wi,2]):
            child=[e for e in domains[wi,4] if tuple(v//2 for v in e['index'])==d['index']]
            require(len(child)==16 and sum((e['volume_time_fraction'] for e in child),F(0))==d['volume_time_fraction'],'nested mass conservation')
    ga=readgz(HERE/'results/GEOMETRY_128.json.gz');gb=readgz(HERE/'results/GEOMETRY_192.json.gz')
    require(len(ga)==len(gb)==6,'complete geometry record inventory')
    for a,b in zip(ga,gb):
        require((a['window'],a['detector_grid'])==(b['window'],b['detector_grid']),'same geometry domain')
        nd=max(1,b['detector_grid']**4)
        require(len(a['mu_bounds'])==len(b['mu_bounds'])==256 and all(len(r)==nd for r in a['mu_bounds']+b['mu_bounds']),'complete product geometry partition')
        for ar,br in zip(a['mu_bounds'],b['mu_bounds']):
            for av,bv in zip(ar,br):
                for x,y in zip(av,bv):require(arb(x).overlaps(arb(y)),'physical cross-precision overlap');counter['physical_volume_overlaps']+=1
    bygeo={(r['window'],r['detector_grid']):r['mu_bounds'] for r in gb}
    del ga,gb
    aa=readgz(HERE/'results/CELLS_128.json.gz');bb=readgz(HERE/'results/CELLS_192.json.gz')
    require(len(aa)==len(bb)==24,'complete archive audit inventory')
    for a,b in zip(aa,bb):
        key,wi,n=b['key'],b['window'],b['detector_grid']
        require((a['key'],a['window'],a['detector_grid'])==(key,wi,n),'same audit domain')
        require(a['n0_lower']==b['n0_lower'] and a['n0_upper']==b['n0_upper'],'exact cross-precision counts')
        for label in ['n0_lower','n0_upper','kernel_upper']:
            require(len(a[label])==len(b[label])==256 and all(len(row)==max(1,n**4) for row in a[label]+b[label]),'complete audit product partition')
        require(np.all(np.array(b['n0_lower'])<=np.array(b['n0_upper'])),'ordered full count inventory')
        for ar,br in zip(a['kernel_upper'],b['kernel_upper']):
            for x,y in zip(ar,br):
                u,v=arb(x),arb(y)
                require(0<=u<=cap and 0<=v<=cap,'kernel in range')
                require(abs(u-v)<arb('1e-8')*max(v,arb('1e-30')),'majorant precision stability')
                counter['kernel_majorants_checked']+=1
        q=[point(v) for v in frozen[key+'_outer']]
        ds=[whole_detector(wi)] if n==0 else domains[wi,n]
        for ci in [0,85,170,255]:
            rm=[integer_relation(roots[ci]['center'],[F(1,8),F(1,2),F(1,2),F(1,2)],z,True) for z in q]
            for di in sorted({0,len(ds)//2,len(ds)-1}):
                d=ds[di]
                if n:dm=[integer_relation(d['center'],d['half'],z,False) for z in q]
                else:dm=[(integer_relation(d['minus'],[0]*4,z,False)[0],integer_relation(d['plus'],[0]*4,z,False)[0]) for z in q]
                lo=sum(x[0] and y[0] for x,y in zip(rm,dm));hi=sum(x[1] and y[1] for x,y in zip(rm,dm))
                require((lo,hi)==(b['n0_lower'][ci][di],b['n0_upper'][ci][di]),'independent exact integer box counts')
                counter['integer_box_count_checks']+=1
                # A center probe is a control, never used to integrate detector/source.
                end=d['center'] if n else ((F(7,8) if wi==0 else F(9,8)),F(0),F(0),F(3,2))
                y=roots[ci]['center'];ct=sum(integer_relation(y,[0]*4,z,True)[0] and integer_relation(end,[0]*4,z,False)[0] for z in q)
                mu=geometry(y,end)[2];ml,mh=map(arb,bygeo[wi,n][ci][di])
                require(lo<=ct<=hi and ml.lower()<=mu.lower() and mu.upper()<=mh.upper(),'joint center containment')
                e=absolute_expectation(ct,mu)
                require(e.upper()<=arb(b['kernel_upper'][ci][di]),'point kernel below inherited cell bound')
                counter['point_kernel_dominance_checks']+=1
    for ra,rb in zip(results[0]['archives'],results[1]['archives']):
        for wa,wb in zip(ra['windows'],rb['windows']):
            last=arb(wb['v20']['direct_detector_upper'])
            for la,lb in zip(wa['levels'],wb['levels']):
                d=arb(lb['direct_detector_upper']);require(d<last,'strict refinement gain');last=d
                total=sum((arb(lb[k]) for k in ['direct_detector_upper','known_active_transport_upper','unknown_active_paths_upper']),arb(0))
                require(total.overlaps(arb(lb['patch_total_upper'])),'complete path class balance')
                for k in ['direct_detector_upper','patch_total_upper']:
                    require(abs(arb(la[k])-arb(lb[k]))<arb('1e-8')*arb(lb[k]),'integral precision stability')
                for k in ['known_active_transport_upper','unknown_active_paths_upper']:
                    require(arb(lb[k]).overlaps(arb(wb['v20'][k])),'transport unchanged')
    for item in json.loads((HERE/'PROVENANCE.json').read_text())['files']:
        d=(HERE/item['package_path']).read_bytes()
        require(hashlib.sha256(d).hexdigest()==item['sha256'],'input SHA256')
        require(hashlib.sha1(b'blob '+str(len(d)).encode()+b'\0'+d).hexdigest()==item['git_blob_sha1'],'main Git blob')
        counter['source_blobs']+=1
    for bad in [lambda:require(H(0)==abs(weight(0)),'unsafe local weight used as suffix'),
                lambda:require(resolved>=1,'unresolved sphere boundary omitted'),
                lambda:upper(-1,arb(1)),
                lambda:require(F(mass['inside_volume'])==F(1,1),'cube used as normalized sphere')]:
        try:bad()
        except (ArithmeticError,ValueError):counter['negative_controls']+=1
        else:raise ArithmeticError('negative control accepted')
    require(results[0]['status']==results[1]['status'] and results[1]['new_random_calls']==0,'unchanged gate')
    out={'status':'PASS','counters':counter,'external_review':'NOT_CLAIMED','global_complement':'NOT_NEWLY_CERTIFIED'}
    prev.write(HERE/'results/CHECKS.json',out);print(json.dumps(out,indent=2));return out
if __name__=='__main__':verify()
