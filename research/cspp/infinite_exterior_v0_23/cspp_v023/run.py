"""Complete disjoint tail and global conditional expected absolute remainder."""
import argparse,hashlib,time
from fractions import Fraction as F
from flint import arb,acb,ctx
import numpy as np
from common import HERE,read,write,ball,enc,require
from bounds import BoundEngine

def calculate(bits):
    ctx.prec=bits;start=time.monotonic();protocol=read('PROTOCOL.json')
    prior=read('evidence/v19_BOUNDS_512.json');finite=read(f'evidence/v22_FINITE_{bits}.json');old=read(f'evidence/v20_LOCAL_{bits}.json');clouds=np.load(HERE/'evidence/v20_archived_omega5.npz')
    engine=BoundEngine(prior);audit=[];known=[]
    for archive in old['archives']:
        raw=clouds[archive['key']+'_outer'];digest=hashlib.sha256(np.ascontiguousarray(raw).tobytes()).hexdigest()
        require(digest==archive['coordinates_sha256'],'unchanged archive bytes')
        require(np.array_equal(raw[archive['active_archive_indices']],np.array(archive['active_coordinates'])),'unchanged active points')
        values=[]
        for j,p in enumerate(archive['active_coordinates']):
            point=list(map(lambda x:F(float(x)),p));t=point[0];r2=sum(x*x for x in point[1:]);r=ball(r2).sqrt();sigma=ball(t+1)
            require(t>-1 and (t+5)**2>r2,'active endpoint inside B')
            C=(r-sigma+arb(1)/4).upper();qcap=ball(((t+5)**2-r2)**2/128)
            result=engine.endpoint(C,sigma,qcap);v=arb(result['tail_bounds'][0]['direct_tail_upper']);values.append(v)
            audit.append({'kind':'known','archive':archive['key'],'active_index':j,'point':list(map(str,point)),**result})
        known.append(values);print('known',bits,archive['key'],len(values),flush=True)
    # Exact radial density of the unchanged shifted detector ball.
    def primitive(r):return -r**4+4*r**3-4*r*r
    windows=[]
    for wi in range(2):
        direct=arb(0);mass_total=F(0)
        for it in range(8):
            tl=F(3+wi,4)+F(it,32);th=tl+F(1,32)
            for ir in range(16):
                rl=1+F(ir,16);rh=rl+F(1,16);mass=(primitive(rh)-primitive(rl))/8;mass_total+=mass
                C=ball(rh-(tl+1)+F(1,4));sigma=ball(th+1);qcap=ball(((th+5)**2-rl*rl)**2/128)
                result=engine.endpoint(C,sigma,qcap);direct+=ball(mass)*arb(result['tail_bounds'][0]['direct_tail_upper'])
                audit.append({'kind':'detector','window':wi,'radius_bounds':list(map(str,[rl,rh])),'time_bounds':list(map(str,[tl,th])),'mass':str(mass),**result})
        require(mass_total==1,'whole detector exactly normalized')
        tmax=F(4+wi,4);C=ball(tmax+F(13,4));sigma=ball(tmax+1);qcap=ball(((tmax+5)**2-1)**2/128)
        uniform=engine.endpoint(C,sigma,qcap,include_tail_grid=True)
        D=arb(uniform['tail_bounds'][0]['direct_tail_upper']);rows=[]
        for k,archive in enumerate(old['archives']):
            n=len(known[k]);adjoints=[acb(*map(arb,z)) for z in archive['adjoints'][wi]]
            transport=sum((z.abs_upper()*f for z,f in zip(adjoints,known[k])),arb(0))
            unknown=D*(1+engine.gamma)**n*((engine.gamma*arb(29)/512).exp()-1)
            tail=direct+transport+unknown;fin=arb(finite['levels'][-1]['archives'][k]['windows'][wi]['finite_total_upper']);total=fin+tail
            G=(1+engine.gamma)**n*(engine.gamma*arb(29)/512).exp();baseline=D*G
            require(tail<baseline,'endpoint-dependent transport sharper than uniform path bound')
            oldglobal=arb(prior['windows'][wi]['archives'][k]['full_remainder_L1_bound'])
            require(total<oldglobal,'complete new global bound improves inherited global majorant')
            rows.append({'key':archive['key'],'active_count':n,'coordinates_sha256':archive['coordinates_sha256'],
              'known_first_tail_upper':list(map(enc,known[k])),'direct_tail_upper':enc(direct),'known_active_tail_upper':enc(transport),'unknown_active_tail_upper':enc(unknown),
              'complete_tail_upper':enc(tail),'finite_v022_upper':enc(fin),'complete_global_upper':enc(total),'uniform_transport_tail_upper':enc(baseline),
              'v019_global_upper':enc(oldglobal),'improvement_over_v019':enc(oldglobal/total)})
        windows.append({'window':wi,'direct_detector_upper':enc(direct),'detector_bins':128,'uniform_active_endpoint':uniform,'archives':rows})
        print('window',bits,wi,[(r['key'],float(arb(r['complete_global_upper'])),float(arb(r['improvement_over_v019']))) for r in rows],flush=True)
    out={'schema':protocol['schema'],'precision_bits':bits,'base_commit':protocol['base_commit'],'source_M0':enc(engine.M),'source_L2':enc(engine.norm),
      'history_partition':{'finite':'0<=tau<=5','infinite':'tau>5','finite_exterior_zero':'0<=tau<=7/4'},
      'endpoint_audits':len(audit),'windows':windows,'status':protocol['status'],'new_random_calls':0,
      'scope':'Complete conditional expected absolute exterior remainder from all history roots, finite plus disjoint infinite tail; no individual-realization guarantee'}
    write(HERE/f'results/ENDPOINTS_{bits}.json.gz',audit);write(HERE/f'results/GLOBAL_{bits}.json',out)
    print('DONE',bits,round(time.monotonic()-start,2),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--bits',type=int,choices=[128,192],required=True);calculate(p.parse_args().bits)
