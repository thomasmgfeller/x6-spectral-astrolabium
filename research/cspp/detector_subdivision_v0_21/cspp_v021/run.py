"""v0.21: certified detector subdivision on the fixed v0.20 root patch."""
import argparse,gzip,hashlib,json,sys,time,importlib.util
from pathlib import Path
import numpy as np
from flint import arb,ctx
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'vendor_v020'))
spec=importlib.util.spec_from_file_location('previous_run',HERE/'vendor_v020/run.py')
previous=importlib.util.module_from_spec(spec);spec.loader.exec_module(previous)
from overlap import point,before,geometry,ball
from envelope import upper,certificate
from domains import root_masks,detector_masks,detector_cells,whole_detector
enc=previous.enc;require=previous.require;write=previous.write

def calculate(bits):
    ctx.prec=bits;start=time.monotonic()
    old=json.loads((HERE/f'evidence/v20_LOCAL_{bits}.json').read_text())
    frozen=np.load(HERE/'evidence/v20_archived_omega5.npz')
    L1=arb(old['source_L1']);roots=previous.field_cells(4,L1)
    a=1/(2*arb.pi()).sqrt();beta=a/(16*(1+a));rho=3/arb.pi();cap=arb('4976184375/4294967296')
    root_factor=[beta*rho*ball(c['volume'])*c['U'] for c in roots]
    domains={};meta=None
    for wi in range(2):
        domains[wi]={0:[whole_detector(wi)]}
        for n in [2,4]:domains[wi][n],meta=detector_cells(n,wi)
    # Geometry is shared across the four archives; each ball has exact endpoints.
    geoms={};grows=[]
    for wi in range(2):
        for n in [0,2,4]:
            vals=[]
            for ci,c in enumerate(roots):
                row=[]
                for d in domains[wi][n]:
                    ml=geometry(c['plus'],d['minus'])[2]
                    mh=geometry(c['minus'],d['plus'])[2]
                    require(ml.upper()<=mh.upper(),'ordered exterior volumes')
                    row.append((ml,mh))
                vals.append(row)
            geoms[wi,n]=vals
            grows.append({'window':wi,'detector_grid':n,'mu_bounds':[[[enc(x),enc(y)] for x,y in row] for row in vals]})
            print('geometry',bits,wi,n,flush=True)
    write(HERE/f'results/GEOMETRY_{bits}.json.gz',grows)
    output=[];audit=[]
    for oldrow in old['archives']:
        key=oldrow['key'];x=frozen[key+'_outer'];q=[point(z) for z in x]
        require(previous.digest(x)==oldrow['coordinates_sha256'],'unchanged archive')
        rm=np.stack([root_masks(c,q) for c in roots]);wins=[]
        for wi in range(2):
            bounds={};levels=[]
            for n in [0,2,4]:
                ds=domains[wi][n]
                if n==0:
                    dm=np.array([[[before(z,ds[0][k]) for z in q] for k in ['minus','plus']]],dtype=np.int16)
                else:dm=np.stack([detector_masks(d,q) for d in ds])
                nlo=rm[:,0,:]@dm[:,0,:].T;nhi=rm[:,1,:]@dm[:,1,:].T
                require(np.all(nlo<=nhi),'ordered exact rectangle counts')
                kvals=[];direct=arb(0);raw_sharp=0;parent_clips=0
                for ci,c in enumerate(roots):
                    kr=[]
                    for di,d in enumerate(ds):
                        K=upper(int(nlo[ci,di]),geoms[wi,n][ci][di][0])
                        raw_sharp+=int(K<cap)
                        if n:
                            parent=bounds[0][ci][0] if n==2 else bounds[2][ci][np.ravel_multi_index(tuple(v//2 for v in d['index']),(2,)*4)]
                            parent_clips+=int(K>parent);K=min(K,parent)
                        kr.append(K)
                    kvals.append(kr)
                    if not n:avg=kr[0]
                    else:
                        K0=bounds[0][ci][0]
                        avg=K0-sum((d['probability_lower']*(K0-K) for d,K in zip(ds,kr)),arb(0))
                    require(avg>=0 and avg<=cap,'normalized detector majorant')
                    direct+=root_factor[ci]*avg
                bounds[n]=kvals
                oldwin=oldrow['levels'][-1]['windows'][wi]
                known=arb(oldwin['known_active_transport_upper']);unknown=arb(oldwin['unknown_active_paths_upper'])
                total=direct+known+unknown
                levels.append({'detector_grid':n,'endpoint_cells':len(ds),'direct_detector_upper':enc(direct),
                    'known_active_transport_upper':enc(known),'unknown_active_paths_upper':enc(unknown),
                    'patch_total_upper':enc(total),'raw_kernels_below_kappa':raw_sharp,'parent_clips':parent_clips})
                audit.append({'key':key,'window':wi,'detector_grid':n,'n0_lower':nlo.tolist(),'n0_upper':nhi.tolist(),
                              'kernel_upper':[[enc(k) for k in row] for row in kvals]})
                print('bound',bits,key,wi,n,enc(direct),enc(total),flush=True)
            wins.append({'window':wi,'v20':oldrow['levels'][-1]['windows'][wi],'levels':levels})
        output.append({'key':key,'coordinates_sha256':previous.digest(x),'windows':wins})
    write(HERE/f'results/CELLS_{bits}.json.gz',audit)
    mass=ball(meta['inside_volume'])*6/arb.pi()
    result={'schema':'cspp.detector-subdivision/0.21','base_commit':'22eab46877dc03b1c0f1bee81c2d1d65bbf45d65',
      'precision_bits':bits,'root_grid':4,'root_cells':256,'mass_certificate':meta,'resolved_detector_mass_lower':enc(mass),
      'monotone_envelope_certificate':certificate(),'archives':output,
      'new_random_calls':0,'status':{'METHOD':'HOLD','G1':'HOLD','global_exterior_complement':'NOT_NEWLY_CERTIFIED','fresh_confirmation':'NOT_RUN'}}
    write(HERE/f'results/DETECTOR_{bits}.json',result)
    print('DONE',bits,round(time.monotonic()-start,2),flush=True)
    return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True)
    calculate(ap.parse_args().bits)
