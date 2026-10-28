"""Full causal graph audit in each CPU mode; no coordinates or seeds are replaced."""
import argparse,json,os
from pathlib import Path
import numpy as np
from flint import ctx
from common import HERE,PILOT,old,check,digest,write
import benchmark,geometry,initial_data as data,propagation as prop

class Recorded:
    def __init__(self,g):
        import hashlib
        self.g=g;self.h=hashlib.sha256()
    def __getattr__(self,name):
        def call(*a,**k):
            r=getattr(self.g,name)(*a,**k);v=np.asarray(r)
            self.h.update(name.encode()+v.dtype.str.encode()+str(v.shape).encode()+np.ascontiguousarray(v).tobytes());return r
        return call

def regenerate(d,i,x=None):
    original=old.rng;draws=[]
    def wrapped(*a,**k):
        g=Recorded(original(*a,**k));draws.append(g);return g
    old.rng=wrapped
    try:y=old.sprinkle(d,i) if x is None else old.extend(x,d,i)
    finally:old.rng=original
    check(len(draws)==1,'single unchanged RNG stream');return y,draws[0].h.hexdigest()

def compute(source_dir):
    ctx.prec=128;ref=benchmark.gzread(source_dir/'BENCHMARK_128.json.gz')
    targets={(r['key'],r['kind'],r['mass'],r['epsilon']):r for r in ref['rows']};graphs={r['key']:r for r in ref['geometry']}
    streams={r['key']:r for r in json.loads((HERE.parent/'scalar_pilot_portability_v0_1/STREAMS.json').read_text())['rows']}
    archive=np.load(PILOT/'results/clouds.npz');records=json.loads((PILOT/'results/RUNS.json').read_text());p=old.probes();rows=[];maxdiff=0.;maxnum=0.;outer_count=0
    A=float(data.source.normalization(ctx.prec)[0].mid())
    for r in records:
        key=r['key'];canonical=archive[key];x,stream=regenerate(r['density_index'],r['realization_index']);s=streams[key];g=graphs[key]
        check(stream==s['rng_draw_output_sha256'],'RNG output hash '+key)
        check(digest(canonical)==s['historical_coordinates_sha256']==g['coordinates_sha256'],'canonical input hash '+key)
        check(x.shape==canonical.shape and np.isfinite(x).all(),'regenerated shape and finite coordinates')
        difference=float(np.max(np.abs(x-canonical),initial=0));check(difference<=2**-48,'coordinate engineering screen');maxdiff=max(maxdiff,difference)
        cc,pc,rr,rp,stats=geometry.inventory(x,p)
        check(digest(rr)==g['relations_sha256'] and digest(rp)==g['probe_relations_sha256'],'ALL cloud/cloud and cloud/probe relations '+key)
        check(digest(cc)==g['counts_sha256'] and digest(pc)==g['probe_counts_sha256'],'ALL interval counts '+key)
        check(digest(x[:,0]<=-1)==g['history_mask_sha256'] and digest(x[:,0]<1)==g['active_mask_sha256'],'all solve-region masks')
        region,region_stats=geometry.region(x,4);check(np.all(region) and digest(region)==g['domain_mask_sha256'],'exact regenerated Omega4 membership')
        # Regenerated coordinates audit the sampler. Production reuses canonical
        # archives; rerun actual numerical propagation on those exact inputs.
        for e in ['1','1/4','1/16']:
            for kind,m in [('wave',1)]+([('compact',m) for m in [0,1,2]] if key=='d0_r00' else []):
                h=np.column_stack([data.float_wave_history(canonical,k,o) for o in [1,3] for k in [0,2,4,8]]) if kind=='wave' else np.column_stack([data.float_bump_history(canonical,m,o,A) for o in [1,3]])
                value,back=prop.float_solve(cc,pc[:28],canonical,p[:28],r['nu'],float(__import__('fractions').Fraction(e)),m,h)
                target=targets[(key,kind,m,e)]
                expected=np.column_stack([np.array(f['actual_float_probe_values'])[:,0]+1j*np.array(f['actual_float_probe_values'])[:,1] for f in target['fields']])
                check(np.allclose(value,expected,atol=1e-10,rtol=1e-11),'declared numeric propagation tolerance')
                check(back<1e-12,'backward residual diagnostic');maxnum=max(maxnum,float(np.max(np.abs(value-expected))))
        outer=None
        if 'outer_metric_index' in r:
            y,draw=regenerate(r['density_index'],r['realization_index'],x);yc=archive[key+'_outer']
            check(draw==s['outer_rng_draw_output_sha256'] and digest(yc)==s['historical_outer_sha256'],'outer archive/RNG identity')
            check(y.shape==yc.shape and np.max(np.abs(y-yc),initial=0)<=2**-48,'outer coordinate screen')
            _,oc,rel,prel,st=geometry.inventory(y,p,full=False)
            _,occ,relc,prelc,stc=geometry.inventory(yc,p,full=False)
            check(digest(oc)==digest(occ)==r['outer_probe_counts_sha256'],'outer interval counts')
            check(digest(rel)==digest(relc) and digest(prel)==digest(prelc),'ALL outer endpoint relations')
            for H in [4,5]:
                region,rs=geometry.region(y,H);canonical_region,rcs=geometry.region(yc,H)
                check(np.array_equal(region,canonical_region),'outer and shell exact domain membership')
                check(np.all(region) if H==5 else int(np.sum(region))==len(x),'exact paired outer-region inventory')
            outer={'relations_sha256':digest(relc),'probe_relations_sha256':digest(prelc),'N':len(y),**st};outer_count+=1
        rows.append({'key':key,'coordinate_bytes_identical':bool(np.array_equal(x,canonical)),'maximum_coordinate_difference':difference,'all_required_relations_counts_and_masks_exact':True,**stats,'outer':outer})
        print('CPU graph',os.getenv('NPY_DISABLE_CPU_FEATURES','default'),key,flush=True)
    check(len(rows)==64 and outer_count==8,'complete CPU relation scope')
    return {'status':'PASS_EXACT_REQUIRED_RELATIONS_AND_NUMERIC_REPLAY','numpy':np.__version__,'disabled_features':os.getenv('NPY_DISABLE_CPU_FEATURES'),
            'rows':rows,'inner_clouds':64,'outer_clouds':8,'maximum_coordinate_difference':maxdiff,'maximum_propagation_difference':maxnum,
            'scope':'exact dyadic archive geometry; regenerated sampler graphs match; not general coordinate-byte portability or exact-real sampler geometry',
            'scientific_status':{'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',type=Path,default=HERE/'results');p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    result=compute(a.source);write(a.out,result)
