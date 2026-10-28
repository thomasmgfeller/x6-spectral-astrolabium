"""All required graph relations and canonical numerical actions in either CPU mode."""
import argparse,json,os
from pathlib import Path
import numpy as np
from support import HERE,old,legacy_fields,check,digest,write,plan,draw,freeze_check,gzread,geometry

def compute(source):
    freeze_check();p=plan();saved=gzread(source/'BENCHMARK_128.json.gz')
    targets={(r['density_index'],r['realization_index'],r['epsilon']):r for r in saved['rows']}
    graphs={g['key']:g for g in saved['graphs']};rows=[];maxcoord=0.;maxnum=0.
    for d,nu in enumerate(p['nu']):
        archive=np.load(source/f'clouds_d{d}.npz')
        for i in range(64):
            key=f'd{d}_r{i:02d}';g=graphs[key]
            if g['status']!='COMPLETE':rows.append({'key':key,'status':'UNAVAILABLE'});continue
            x,meta=draw(d,i);canonical=archive[key]
            check(meta['rng_draw_output_sha256']==g['rng_draw_output_sha256'],'exact RNG outputs')
            check(digest(canonical)==g['coordinates_sha256'],'exact canonical coordinates')
            delta=float(np.max(np.abs(x-canonical),initial=0));maxcoord=max(maxcoord,delta)
            check(delta<=2**-48,'coordinate engineering tolerance')
            _,pc,rr,rp,st=geometry.inventory(x,old.probes()[:21],full=False)
            for actual,k in [(pc,'probe_counts_sha256'),(rr,'relations_sha256'),(rp,'probe_relations_sha256')]:
                check(digest(actual)==g[k],'all required exact relations and interval counts')
            domain,ds=geometry.region(x,4);check(np.all(domain) and digest(domain)==g['domain_mask_sha256'],'exact domain membership')
            phi,_=legacy_fields.fields(canonical);phip,_=legacy_fields.fields(old.probes()[:21])
            for e in p['epsilon']:
                target=targets[d,i,e]
                if target['status']!='COMPLETE':continue
                values=old.apply(pc,nu/old.volume(4),float(__import__('fractions').Fraction(e)),phi,phip)
                expected=np.column_stack([np.array(f['numeric_values'])[:,0]+1j*np.array(f['numeric_values'])[:,1] for f in target['fields']])
                maxnum=max(maxnum,float(np.max(np.abs(values-expected))))
                check(np.allclose(values,expected,atol=1e-10,rtol=1e-11),'numeric CPU tolerance')
            rows.append({'key':key,'status':'PASS','coordinate_difference':delta,**st})
    return {'status':'PASS','disabled_features':os.environ.get('NPY_DISABLE_CPU_FEATURES'),
            'clouds_checked':sum(r['status']=='PASS' for r in rows),'rows':rows,
            'maximum_coordinate_difference':maxcoord,'maximum_numeric_difference':maxnum,
            'scope':'all cloud/cloud and cloud/probe relations, probe counts, domain membership, canonical numerical operator; no unused propagation relations claimed'}

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--source',type=Path,required=True);a.add_argument('--out',type=Path,required=True);z=a.parse_args();write(z.out,compute(z.source))
