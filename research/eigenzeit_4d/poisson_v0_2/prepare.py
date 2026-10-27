"""Freeze geometry, protocol and executable sources before primary sampling."""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,datetime
import numpy as np
import model as m

ROOT=Path(__file__).resolve().parent

def main():
    p=json.loads((ROOT/'PROTOCOL.json').read_text())
    rng=np.random.Generator(np.random.PCG64(p['geometry_seed']))
    geos=[]
    for k,f in enumerate(p['base_families']):
        g=m.exact_geometry(m.base(f['epsilon'],f['q_sign']))
        g.update(id=f'base_{k}',family=k,kind='fixed_reference',epsilon=f['epsilon'])
        geos.append(g)
    for k in range(p['fresh_geometries']):
        family=k%4; f=p['base_families'][family]
        pts=m.base(f['epsilon'],f['q_sign'])
        jitter=rng.integers(-1,2,size=(6,4))
        pts=[pts[0]]+[tuple(x+F(int(jitter[i-1,j]),64) for j,x in enumerate(pt)) for i,pt in enumerate(pts[1:],1)]
        g=m.exact_geometry(pts)
        g.update(id=f'fresh_{k:02}',family=family,kind='held_out_jitter',epsilon=f['epsilon'])
        geos.append(g)
    (ROOT/'geometries.json').write_text(json.dumps(geos,indent=2)+'\n')
    hashes={x.name:hashlib.sha256(x.read_bytes()).hexdigest() for x in sorted(ROOT.iterdir())
            if x.suffix in ('.py','.json') and x.name!='FREEZE.json'}
    freeze={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
            'stage':'before all primary count draws','sha256':hashes,
            'geometry_count':len(geos),'covariance_identities':sum(g['exact_covariance_identities'] for g in geos)}
    (ROOT/'FREEZE.json').write_text(json.dumps(freeze,indent=2)+'\n')
    print(json.dumps({'frozen':list(hashes),'geometries':len(geos),'exact_covariance_identities':freeze['covariance_identities']}))

if __name__=='__main__':main()
