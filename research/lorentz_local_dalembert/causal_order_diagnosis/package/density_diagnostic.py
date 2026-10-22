"""New conditional count clouds using independent box-Poisson rejection.
SPDX-License-Identifier: Apache-2.0
"""
import gzip
import hashlib
import json
import time
import numpy as np
from diagnose import HERE,SRC,OUT,save,sha,matrices,reconstruct,summary_geometry,old

def draw_counts(points,packet,index,factor,repeat,base_density,duration):
    entropy=[2026102201,index,factor,repeat]
    rng=np.random.default_rng(np.random.SeedSequence(entropy))
    rho=base_density*factor;n=int(rng.poisson(rho*duration**3))
    ids=packet['landmarks']+[packet['root']]+packet['support'];lookup={a:i for i,a in enumerate(ids)}
    pairs=np.array([[lookup[a],lookup[b]] for a,b in packet['pairs']])
    order=np.array(packet['full_order'],bool);lower=[];upper=[]
    for i,j in pairs:
        if order[j,i]:i,j=j,i
        assert order[i,j]
        lower.append(i);upper.append(j)
    lower=np.array(lower);upper=np.array(upper)
    counts=np.zeros(len(pairs),dtype=np.int64);accepted=0;digest=hashlib.sha256()
    for start in range(0,n,50000):
        box=(rng.random((min(50000,n-start),3))-.5)*duration
        z=box[abs(box[:,0])+np.sqrt(box[:,1]**2+box[:,2]**2)<duration/2]
        accepted+=len(z);digest.update(z.astype('<f8').tobytes())
        dt=z[None,:,0]-points[:,None,0]
        space=(z[None,:,1]-points[:,None,1])**2+(z[None,:,2]-points[:,None,2])**2
        timelike=dt**2>space
        future=(dt>0)&timelike;past=(dt<0)&timelike
        counts+=np.count_nonzero(future[lower]&past[upper],axis=1)
    return dict(entropy=entropy,index=index,factor=factor,repeat=repeat,rho=rho,
                box_points=n,diamond_points=accepted,accepted_coordinates_sha256=digest.hexdigest(),counts=counts)

def controls():
    # Causally convex diamond and exact analytic interval count mean are checked
    # separately in diagnose.py. Check strict endpoint exclusion directly here.
    points=np.array([[-.5,0,0],[.5,0,0]])
    z=np.array([[-.5,0,0],[.5,0,0],[0,0,0],[0,.49,0],[0,.5,0],[0,.6,0]])
    dt=z[None,:,0]-points[:,None,0];space=(z[None,:,1]-points[:,None,1])**2+(z[None,:,2]-points[:,None,2])**2
    good=(dt[0]>0)&(dt[1]<0)&(dt[0]**2>space[0])&(dt[1]**2>space[1])
    assert good.tolist()==[False,False,True,True,False,False]

def main():
    controls();c=json.loads((SRC/'contract.json').read_text());start=time.monotonic()
    records=[];complete=True
    for path in sorted((SRC/'results/truth').glob('cloud-*.json')):
        truth=json.loads(path.read_text());index=truth['index'];p=np.array(truth['points'])
        row=json.loads(gzip.decompress((SRC/f'results/cloud-{index:02d}.json.gz').read_bytes()))
        packet=row['selection']['fourth']['packet'];H,Z,groups,ids=matrices(packet)
        for factor in [1,4,16]:
            for repeat in range(4):
                if time.monotonic()-start>600:complete=False;break
                raw=draw_counts(p,packet,index,factor,repeat,c['count_density'],c['duration'])
                counts=np.array(raw['counts']);q=(counts/(raw['rho']*np.pi/12))**(2/3)/packet['scale']**2
                geo=reconstruct(q,packet,H,Z)
                if min(counts[groups!='unused'])<c['minimum_measurement_count']:
                    full=dict(status='COUNT_HOLD',qualified=False)
                else:
                    try:
                        f=old.four(q,packet)
                        full=dict(status=f['status'],qualified=f['qualified'],order=f['order'])
                    except (ValueError,np.linalg.LinAlgError) as exc:full=dict(status='UNRESOLVED',reason=str(exc),qualified=False)
                raw.update(geometry=summary_geometry(geo),full_frozen_checks=full)
                records.append(raw)
            if not complete:break
        save('density_records.json',records)
        print(json.dumps(dict(stage='density',index=index,completed=len(records),seconds=round(time.monotonic()-start,1))),flush=True)
        if not complete:break
    # Reproduce exactly one complete highest-density draw, including accepted
    # point hash, without using it as an extra observation.
    first=next(x for x in records if x['factor']==16)
    truth=json.loads((SRC/f"results/truth/cloud-{first['index']:02d}.json").read_text())
    row=json.loads(gzip.decompress((SRC/f"results/cloud-{first['index']:02d}.json.gz").read_bytes()))
    again=draw_counts(np.array(truth['points']),row['selection']['fourth']['packet'],first['index'],16,first['repeat'],c['count_density'],c['duration'])
    assert again['accepted_coordinates_sha256']==first['accepted_coordinates_sha256']
    np.testing.assert_array_equal(again['counts'],first['counts'])
    grouped={}
    for factor in [1,4,16]:
        xs=[x for x in records if x['factor']==factor]
        grouped[str(factor)]=dict(count_clouds=len(xs),selected_configurations=len(set(x['index'] for x in xs)),
             geometry_order_pass=sum(x['geometry'].get('passed',False) for x in xs),
             full_solve_valid=sum(x['full_frozen_checks']['status']=='WEIGHTS_VALID' for x in xs),
             qualified=sum(x['full_frozen_checks'].get('qualified',False) for x in xs),
             total_missing=sum(x['geometry'].get('missing',0) for x in xs),
             total_extra=sum(x['geometry'].get('extra',0) for x in xs),
             per_configuration=[dict(index=i,n=sum(x['index']==i for x in xs),
                passed=sum(x['full_frozen_checks'].get('qualified',False) for x in xs if x['index']==i)) for i in sorted(set(x['index'] for x in xs))])
    summary=dict(status='COMPLETE' if complete and len(records)==216 else 'BUDGET_HOLD',
                 scheduled_count_clouds=216,completed_count_clouds=len(records),
                 scope='conditional on 18 already selected configurations; four repeats per density do not give 72 independent selection clouds',
                 density_levels=grouped,replay_high_density='PASS',seconds=time.monotonic()-start)
    save('density_summary.json',summary);print(json.dumps(summary,indent=2))

if __name__=='__main__':main()
