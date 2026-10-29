"""Complete finite exterior contribution with uniform KG and angular bounds."""
import argparse,hashlib,json,sys,time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb,acb,ctx
from common import HERE,require,ball,enc,write
from domains import cells,exact_volume,detector_bins,causal_cap
from fields import J2,moments,envelope,absolute_radial_derivative
sys.path.insert(0,str(HERE/'vendor/legacy/massive_reference_v0_5'))
import reference

def cenc(z):return [enc(z.real),enc(z.imag)]
def unpack(z):return acb(arb(z[0]),arb(z[1]))
def controls(M):
    out=[]
    for tau in [F(2),F(3),F(4),F(5)]:
        for shift in [F(-3,8),F(0),F(3,8)]:
            R=tau+shift;c={'kind':'front','tau0':tau,'tau1':tau,'r0':R,'r1':R}
            U,parts=envelope(c,M)
            for axis in [1,3]:
                p=[-tau-1,F(0),F(0),F(0)];p[axis]=R
                z,errors=reference.off_center(list(map(float,p)),1,arb(1).exp())
                require(z.is_finite() and z.abs_upper()<U,'independent wavefront KG envelope')
                require(max(z.real.rad(),z.imag.rad())<arb('1e-16'),'bounded KG control radius')
                out.append({'point':list(map(str,p)),'kind':'front','KG':cenc(z),'field_upper':enc(U)})
    for tau in [F(5,2),F(4),F(5)]:
        for R in [F(0),F(1)]:
            p=[-tau-1,F(0),F(0),R];c={'kind':'deep','tau0':tau,'tau1':tau,'r0':R,'r1':R}
            U,_=envelope(c,M)
            if R==0:z,_=reference.previous.massive_center(list(map(float,p)),1,arb(1).exp())
            else:z,_=reference.off_center(list(map(float,p)),1,arb(1).exp())
            require(z.is_finite() and z.abs_upper()<U,'independent interior KG envelope')
            require(max(z.real.rad(),z.imag.rad())<arb('1e-16'),'interior control radius')
            out.append({'point':list(map(str,p)),'kind':'deep','KG':cenc(z),'field_upper':enc(U)})
    return out

def calculate(bits):
    ctx.prec=bits;start=time.monotonic();protocol=json.loads((HERE/'PROTOCOL.json').read_text())
    old=json.loads((HERE/f'evidence/v20_LOCAL_{bits}.json').read_text())
    prior=json.loads((HERE/'evidence/v19_BOUNDS_512.json').read_text());M=arb(prior['source_M0'])
    clouds=np.load(HERE/'evidence/v20_archived_omega5.npz')
    a=1/(2*arb.pi()).sqrt();beta=a/(16*(1+a));rho=3/arb.pi();kappa=arb('4976184375/4294967296');gamma=beta*kappa;factor=beta*rho*kappa
    L1=4*arb.pi()*J2(F(0),bits);require(L1.overlaps(arb(old['source_L1'])),'unchanged source L1')
    G25=(-arb(25)/4).hypgeom_0f1(3);lower4=1-arb(25)/16+arb(25)**2/640-arb(25)**3/46080
    require(G25>0 and lower4>0,'positive decreasing KG kernel on [0,25]')
    records=[];nodes=[]
    for row in old['archives']:
        raw=clouds[row['key']+'_outer'];digest=hashlib.sha256(np.ascontiguousarray(raw).tobytes()).hexdigest()
        require(digest==row['coordinates_sha256'],'original cloud identity')
        require(np.array_equal(raw[row['active_archive_indices']],np.array(row['active_coordinates'])),'original active point coordinates')
        start_node=len(nodes)
        for p in row['active_coordinates']:
            pp=[F(float(v)) for v in p];rp=ball(sum(x*x for x in pp[1:])).sqrt();nodes.append((rp,ball(pp[0])))
        records.append({'key':row['key'],'start':start_node,'end':len(nodes),'adjoints':[[unpack(z) for z in w] for w in row['adjoints']],
                        'coordinates_sha256':digest,'active_count':len(row['active_coordinates'])})
    require([r['active_count'] for r in records]==protocol['known_active_nodes'],'fixed active inventory')
    det=detector_bins(protocol['detector_radius_bins'],protocol['detector_time_bins'])
    det_balls=[[(ball(d['r0']).union(ball(d['r1'])),ball(d['t_hi']),ball(d['mass'])) for d in window] for window in det]
    levels=[]
    for n in protocol['grid_denominators']:
        cs=cells(n);require(sum(c['volume_over_pi'] for c in cs)==exact_volume(),'exact complete finite support')
        integrals={k:arb(0) for k in ['deep','front']};direct=[arb(0),arb(0)];forces=[arb(0) for _ in nodes];audit=[]
        for ci,c in enumerate(cs):
            U,parts=envelope(c,M);measure=ball(c['volume_over_pi'])*arb.pi();weighted=measure*U
            integrals[c['kind']]+=weighted
            for j,(rp,tp) in enumerate(nodes):forces[j]+=factor*weighted*causal_cap(c,rp,tp)
            dc=[]
            for wi,db in enumerate(det_balls):
                avg=sum((mass*causal_cap(c,rp,tp) for rp,tp,mass in db),arb(0))
                require(0<=avg<=1,'normalized full detector angular weight')
                direct[wi]+=factor*weighted*avg;dc.append(enc(avg))
            audit.append({'index':c['index'],'tau_bounds':[str(c['tau0']),str(c['tau1'])],
              'radius_bounds':[str(c['r0']),str(c['r1'])],'volume_over_pi':str(c['volume_over_pi']),
              'U_upper':enc(U),'field_parts':{k:enc(v) for k,v in parts.items()},'detector_cap_upper':dc})
        integral=sum(integrals.values(),arb(0));uniform=factor*integral;rows=[]
        for rec in records:
            active=rec['active_count'];unknown=uniform*(1+gamma)**active*((gamma*arb(29)/512).exp()-1)
            fs=forces[rec['start']:rec['end']];wins=[]
            for wi in range(2):
                gain=sum((z.abs_upper() for z in rec['adjoints'][wi]),arb(0))
                known=sum((z.abs_upper()*v for z,v in zip(rec['adjoints'][wi],fs)),arb(0))
                total=direct[wi]+known+unknown
                baseline=uniform*(1+gain)+unknown
                wins.append({'window':wi,'direct_upper':enc(direct[wi]),'known_active_upper':enc(known),'unknown_active_upper':enc(unknown),
                    'finite_total_upper':enc(total),'without_angular_caps_upper':enc(baseline),'adjoint_abs_gain':enc(gain)})
            rows.append({'key':rec['key'],'active_count':active,'coordinates_sha256':rec['coordinates_sha256'],
                         'first_forcing_upper':list(map(enc,fs)),'windows':wins})
        level={'grid_denominator':n,'cells':len(cs),'deep_cells':sum(c['kind']=='deep' for c in cs),'front_cells':sum(c['kind']=='front' for c in cs),
          'volume_over_pi':str(exact_volume()),'volume':enc(arb.pi()*ball(exact_volume())),
          'field_L1_integral_upper':enc(integral),'field_integrals_by_region':{k:enc(v) for k,v in integrals.items()},
          'uniform_first_forcing_upper':enc(uniform),'constant_sobolev_field_integral_upper':enc(M*arb.pi()*ball(exact_volume())),
          'archives':rows}
        levels.append(level);write(HERE/f'results/CELLS_{bits}_{n}.json.gz',audit)
        print('finite',bits,n,len(cs),[r['windows'][0]['finite_total_upper'] for r in rows],flush=True)
    ctrl=controls(M);print('KG controls',bits,len(ctrl),flush=True)
    result={'schema':protocol['schema'],'precision_bits':bits,'base_commit':protocol['base_commit'],
      'time_cutoff':'-6','source_L1':enc(L1),'global_field_M':enc(M),'G25':enc(G25),'derivative_kernel_positive_lower':enc(lower4),
      'levels':levels,'field_controls':ctrl,'status':protocol['status'],'new_random_calls':0,
      'scope':'All finite exterior history for -6<=t<=-1 on the entire exact compact KG support, including unchanged discrete transport; no infinite tail combined'}
    write(HERE/f'results/FINITE_{bits}.json',result);print('DONE',bits,round(time.monotonic()-start,2),flush=True);return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True);calculate(ap.parse_args().bits)
