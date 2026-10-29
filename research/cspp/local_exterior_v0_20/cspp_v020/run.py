"""v0.20: exact overlaps, fixed local KG probes, certified finite root patch."""
import argparse, gzip, hashlib, itertools, json, math, sys, time
from fractions import Fraction as F
from pathlib import Path
import numpy as np
from flint import arb, acb, ctx
from overlap import Archive, point, before, geometry, lens_quadrature, ball
from kernel import weight, absolute_expectation, direct_sum
import kernel_table

HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE/'legacy/massive_reference_v0_5'))
import reference

def require(v,s):
    if not bool(v):raise ArithmeticError(s)
def enc(x):
    x=arb(x);require(x.is_finite(),'finite ball')
    s=x.str(50,more=True);require(arb(s).contains(x),'outward serialization');return s
def cenc(z):return [enc(z.real),enc(z.imag)]
def cunpack(z):return acb(arb(z[0]),arb(z[1]))
def digest(a):return hashlib.sha256(np.ascontiguousarray(a).tobytes()).hexdigest()
def write(path,d):
    if str(path).endswith('.gz'):
        with gzip.GzipFile(filename=str(path),mode='wb',mtime=0) as f:f.write((json.dumps(d,sort_keys=True)+'\n').encode())
    else:Path(path).write_text(json.dumps(d,indent=2)+'\n')

ROOTS=[[-6,0,0,0],[-6,0,0,2],[-6,0,0,4],[-5,0,0,2],[-5,0,0,4],[-4,0,0,2],[-4,0,0,3],[-3,0,0,F(9,4)]]

def source_l1():
    hc=arb(1)/64;end=(1-hc).sqrt()/2
    def fn(r,analytic):
        h=1-4*r*r
        if h.contains(0):return acb('nan')
        return 4*arb.pi()*r*r*(1-1/h).exp()
    core=acb.integral(fn,acb(0),acb(end),abs_tol=arb('1e-30'),rel_tol=arb('1e-30'))
    require(core.is_finite() and core.imag.contains(0),'L1 quadrature')
    tail=arb.pi()/6*(1-1/hc).exp()
    return core.real+arb(0).union(tail)

def field_cells(n,L1):
    """Partition [-6,-5] x [-2,2]^3, all in deep KG interior.

    The source-centered KG kernel is G(A)=0F1(3;-A/4).
    0<G(A)<=G(Amin)<=1 for 0<=A<=25; proof in PROOF.md.
    """
    cells=[];ht=F(1,2*n);hx=F(2,n);lag=ht+F(7,4)*hx
    vol=F(1,n)*F(4,n)**3
    for indices in itertools.product(range(n),repeat=4):
        it,*ix=indices;t=F(-6)+F(2*it+1,2*n)
        xyz=[F(-2)+F(2*j+1,2)*F(4,n) for j in ix]
        tau_lo=ball(-t-ht-1);tau_hi=ball(-t+ht-1)
        Rmax=ball(sum((abs(x)+hx)**2 for x in xyz)).sqrt()
        Amin=tau_lo**2-(Rmax+arb(1)/2)**2
        require(Amin>0 and tau_hi<=5,'deep interior patch topology')
        U=tau_hi*L1/(32*arb.pi())*(-Amin/4).hypgeom_0f1(3)
        require(U>0,'positive KG cell envelope')
        cells.append({'index':indices,'center':(t,*xyz),'minus':(t-lag,*xyz),'plus':(t+lag,*xyz),'volume':vol,'U':U})
    return cells

def kernel_hull(nlo,nhi,mulo,muhi):
    kappa=arb('4976184375/4294967296')
    require(nlo<=nhi and mulo.lower()>=0 and muhi.lower()>=0,'ordered local inputs')
    mu=arb(mulo.lower()).union(muhi.upper())
    # Positive polynomial majorants and sign cancellations are enclosed by Arb.
    # The independent pointwise kappa cap remains valid if a wide ball loses sharpness.
    upper=arb(0)
    for n in range(int(nlo),int(nhi)+1):
        e=absolute_expectation(n,mu)
        require(e.is_finite(),'finite conditional expectation enclosure')
        upper=max(upper,e.abs_upper())
        if upper>=kappa:return kappa
    return min(kappa,upper)

def adjoints(ar,coef,beta):
    keep=[i for i,p in enumerate(ar.q) if p[0]<F(5,4) and
       sum((v-c)**2 for v,c in zip(p[1:],(0,0,F(3,2))))<(F(7,4)-p[0])**2]
    z=ar.x[keep];require(digest(z)==coef['retained_coordinates_sha256'],'v16 retained coordinates')
    mapping={i:j for j,i in enumerate(keep)}
    counts=[ar.counts(p) for p in ar.p]
    matrix=[[None]*len(ar.p) for _ in ar.p]
    for i,p in enumerate(ar.p):
        for j,y in enumerate(ar.p[:i]):
            if before(y,p):matrix[i][j]=beta*ball(weight(int(counts[j][i])))
    out=[]
    for wi in range(2):
        q=[cunpack(coef['levels'][-1]['q'][wi][mapping[i]]) for i in ar.active]
        adj=q.copy()
        for i in reversed(range(len(q))):
            for j in range(i):
                if matrix[i][j] is not None:adj[j]+=adj[i]*matrix[i][j]
        # Forward unit forcing checks the same linear functional independently.
        forward=[]
        for i in range(len(q)):
            forward.append(1+sum((matrix[i][j]*forward[j] for j in range(i) if matrix[i][j] is not None),arb(0)))
        require(sum(q[i]*forward[i] for i in range(len(q))).overlaps(sum(adj,acb(0))),'forward adjoint identity')
        out.append(adj)
    return out

def calculate(bits,grids=(2,4)):
    ctx.prec=bits;start=time.monotonic()
    protocol=json.loads((HERE/'PROTOCOL.json').read_text())
    archive=np.load(HERE/'evidence/archived_omega5.npz');runs=json.loads((HERE/'evidence/RUNS.json').read_text())
    with gzip.open(HERE/'evidence/v16_COEFFICIENTS_192.json.gz','rt') as f:co=json.load(f)
    a=1/(2*arb.pi()).sqrt();beta=a/(16*(1+a));rho=3/arb.pi();kappa=arb('4976184375/4294967296');gamma=beta*kappa
    L1=source_l1();G25=(-arb(25)/4).hypgeom_0f1(3)
    lower4=1-arb(25)/16+arb(25)**2/640-arb(25)**3/46080
    require(G25>0 and lower4>0,'kernel monotonicity certificate')
    fields=[]
    for i,y in enumerate(ROOTS):
        yf=list(map(float,y))
        if all(v==0 for v in y[1:]):z,tail=reference.previous.massive_center(yf,1,arb(1).exp());meta={'tail':enc(tail)}
        else:
            z,err=reference.off_center(yf,1,arb(1).exp())
            meta={k:enc(v) if isinstance(v,arb) else v for k,v in err.items()}
        require(z.is_finite() and max(z.real.rad(),z.imag.rad())<arb('1e-18'),'local KG radius')
        fields.append({'point':list(map(str,y)),'KG':cenc(z),'abs_upper':enc(z.abs_upper()),'errors':meta})
        print('KG',bits,i,cenc(z),flush=True)
    table=kernel_table.make_table();np.save(HERE/f'results/KERNEL_TABLE_{bits}.npy',table)
    print('conditional kernel table',bits,'complete',flush=True)
    rows=[];quad_checks=0;poisson_checks=0
    for ki,key in enumerate(protocol['archives']):
        x=archive[key+'_outer'];prior=next(r for r in runs if r['key']==key)
        require(digest(x)==prior['outer_sha256'],'unchanged archived coordinates')
        ar=Archive(x);require(len(ar.active)==protocol['known_active_nodes'][ki],'active inventory')
        coef=next(r for r in co['rows'] if r['key']==key);adj=adjoints(ar,coef,beta)
        probes=[]
        for yi,y in enumerate(ROOTS):
            counts=ar.counts(y)
            for pi,p in enumerate(ar.p):
                total,over,mu,branch=geometry(y,p)
                if branch=='noncausal':continue
                n=int(counts[pi]);E=absolute_expectation(n,mu)
                require(E>0 and E<kappa,'proper conditional kernel at fixed point')
                if pi==0 or pi==len(ar.p)-1:
                    if branch=='lens':require(over.overlaps(lens_quadrature(y,p)),'independent cap quadrature');quad_checks+=int(branch=='lens')
                    require(E.overlaps(direct_sum(n,mu,512)),'direct Poisson sum');poisson_checks+=1
                probes.append({'root':yi,'archive_index':ar.active[pi],'active_index':pi,'n0':n,'branch':branch,
                  'rho_V_total':enc(total),'rho_V_overlap':enc(over),'mu_outside':enc(mu),'E_abs_w':enc(E),
                  'beta_rho_abs_U_E_abs_w':enc(beta*rho*arb(fields[yi]['abs_upper'])*E)})
        detector_bounds=[point([t,0,0,F(3,2)]) for t in [F(1,4),F(3,2),F(1,2),F(7,4)]]
        detector_past=np.array([[before(z,d) for z in ar.q] for d in detector_bounds],dtype=bool)
        levels=[]
        for grid in grids:
            cells=field_cells(grid,L1);Fnode=[arb(0) for _ in ar.p];integralU=arb(0);cellrows=[];sharper=0;direct_windows=[arb(0),arb(0)]
            for ci,c in enumerate(cells):
                clo=ar.counts(c['plus']);chi=ar.counts(c['minus']);dv=ball(c['volume']);integralU+=dv*c['U']
                kern=[]
                for pi,p in enumerate(ar.p):
                    _,_,mulo,_=geometry(c['plus'],p);_,_,muhi,branch=geometry(c['minus'],p)
                    if branch=='noncausal':K=arb(0)
                    else:K=min(kernel_hull(clo[pi],chi[pi],mulo,muhi),kernel_table.upper(table,clo[pi],chi[pi],mulo,muhi))
                    Fnode[pi]+=beta*rho*dv*c['U']*K
                    sharper+=int(K<kappa);kern.append(enc(K))
                flo=np.array([before(c['plus'],z) for z in ar.q],dtype=bool)
                fhi=np.array([before(c['minus'],z) for z in ar.q],dtype=bool)
                dc_lo=np.sum(detector_past & flo,axis=1);dc_hi=np.sum(detector_past & fhi,axis=1);dk=[]
                for wi in range(2):
                    _,_,mulo,_=geometry(c['plus'],detector_bounds[2*wi])
                    _,_,muhi,_=geometry(c['minus'],detector_bounds[2*wi+1])
                    K=kernel_table.upper(table,dc_lo[2*wi],dc_hi[2*wi+1],mulo,muhi)
                    direct_windows[wi]+=beta*rho*dv*c['U']*K;dk.append(enc(K))
                cellrows.append({'index':list(c['index']),'U_upper':enc(c['U']),'n0_lower':clo.tolist(),'n0_upper':chi.tolist(),'kernel_upper':kern,'detector_kernel_upper':dk})
            direct=beta*rho*kappa*integralU
            unknown=direct*(1+gamma)**len(ar.p)*((gamma*arb(29)/512).exp()-1)
            wins=[]
            for wi in range(2):
                known=sum((v.abs_upper()*f for v,f in zip(adj[wi],Fnode)),arb(0))
                total=direct_windows[wi]+known+unknown
                wins.append({'window':wi,'direct_detector_upper':enc(direct_windows[wi]),'known_active_transport_upper':enc(known),'unknown_active_paths_upper':enc(unknown),'patch_total_upper':enc(total),
                  'adjoint_abs_gain':enc(sum(z.abs_upper() for z in adj[wi]))})
            levels.append({'grid':grid,'cells':len(cells),'sharper_kernel_cells':sharper,'integral_abs_U_upper':enc(integralU),
              'uniform_gain_patch_upper':enc(direct*(1+gamma)**len(ar.p)*(gamma*arb(29)/512).exp()),'F_node_upper':list(map(enc,Fnode)),'windows':wins})
            write(HERE/f'results/CELLS_{bits}_{key}_{grid}.json.gz',cellrows)
            print('patch',bits,key,grid,[w['patch_total_upper'] for w in wins],flush=True)
        rows.append({'key':key,'coordinates_sha256':digest(x),'N5':len(x),'active_archive_indices':ar.active,'active_coordinates':x[ar.active].tolist(),
             'probes':probes,'levels':levels,'adjoints':[list(map(cenc,v)) for v in adj]})
    result={'schema':'cspp.local-exterior/0.20','precision_bits':bits,'base_commit':protocol['base_commit'],
         'source_L1':enc(L1),'G25':enc(G25),'derivative_kernel_positive_lower':enc(lower4),'roots':fields,'archives':rows,
         'checks':{'cap_quadratures':quad_checks,'direct_poisson_sums':poisson_checks},
         'status':{'METHOD':'HOLD','G1':'HOLD','full_exterior_remainder':'NOT_IMPROVED_BY_PATCH_ALONE','fresh_confirmation':'NOT_RUN'},'new_random_calls':0}
    write(HERE/f'results/LOCAL_{bits}.json',result)
    print('DONE',bits,round(time.monotonic()-start,2),flush=True)
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--bits',type=int,choices=[128,192],required=True);args=parser.parse_args();calculate(args.bits)
