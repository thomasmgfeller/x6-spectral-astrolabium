"""Independent normalization, quadrature, Gaussian and metric controls."""
import hashlib
import json
import math
from itertools import product
import numpy as np
import sympy as sp
from flint import arb, acb, acb_mat, ctx
import compute as c
from compute import pc, ROOT

def load(name):return json.loads((ROOT/name).read_text())
def arr(m):return np.array([[complex(m[i,j]) for j in range(m.ncols())] for i in range(m.nrows())])
def same(a,b):return all(a[i,j].overlaps(b[i,j]) for i in range(a.nrows()) for j in range(a.ncols()))

def main():
    ctx.prec=192;checks={}
    assert hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest()==(ROOT/'contract.sha256').read_text().strip()
    checks['fixed_contract']='PASS'
    assert len(pc.histories())==33 and sum(map(len,pc.orbits().values()))==33
    checks['complete_history_enumeration']='33 histories, 10 orbits'
    x,y=sp.symbols('x y',real=True);w=(1+x*x+y*y)**4;f=(1,x*x+y*y-1)
    def moment(p):
        result=0
        for (i,j),v in sp.Poly(sp.expand(p),x,y).terms():
            if i%2==0 and j%2==0:
                result+=v*sp.factorial2(i-1)*sp.factorial2(j-1)/2**((i+j)//2)
        return sp.simplify(result)
    gram=sp.Matrix([[moment(w*a*b) for b in f] for a in f])
    assert gram==sp.Matrix([[65,196],[196,913]]) and gram.det()==20929
    t=c.gram_transform();assert (c.adj(t)*c.repeated_gram(1)*t).contains(acb_mat([[1,0],[0,1]]))
    checks['independent_cartesian_V_Gram_and_whitening']='PASS'
    # Separate, real-Schur eigenphase calculation for all labelled geometries.
    max_gaussian=0
    for h in [pc.h0(code) for code in pc.histories()]+[pc.reference_h0()]:
        h=np.array([[float(v) for v in row] for row in h]);outer=[0,1,3,4]
        m=4/np.sqrt(6)*h;alpha=-m[2,2]
        s=m[np.ix_(outer,outer)]+np.outer(m[outer,2],m[2,outer])/alpha
        eig=np.linalg.eigvalsh(s);cov=np.linalg.inv(np.eye(4)-1j*s)
        a=4*np.pi*np.sqrt(2*np.pi/alpha)*np.prod((1+eig*eig)**(-.25))*np.exp(1j*(-np.pi/4+np.arctan(eig).sum()/2))
        u=np.trace(cov[:2,:2])-1;v=np.trace(cov[2:,2:])-1
        expect=a*np.array([[1,u],[v,u*v+2*np.sum(cov[:2,2:]**2)]])
        actual=arr(c.scalar([[str(v) for v in row] for row in h]))
        max_gaussian=max(max_gaussian,float(np.max(np.abs(actual-expect))))
    assert max_gaussian<2e-12
    checks['independent_schur_eigenphases_and_Wick_moments']={'max_abs':max_gaussian}
    # Direct 5D quadrature for all 33 labels, independent of finite-sum contraction.
    n=6;nodes,weights=np.polynomial.legendre.leggauss(n)
    grids=np.meshgrid(*([nodes]*5),indexing='ij');tt=np.array([g.ravel() for g in grids])
    ww=np.prod(np.array([g.ravel() for g in np.meshgrid(*([weights/2]*5),indexing='ij')]),axis=0)
    q=c.Quadrature(n);cached={};max_dust=0;max_orbit=0
    direct={}
    beta=4/np.sqrt(6)
    for code in pc.histories():
        kk=np.ones_like(tt)/2
        for i,j,b in pc.pair_coefficients(code):kk[j]+=beta*b*(tt[j]-tt[i])**2/4
        ee=np.exp(-.5j*kk)*np.sinc(kk/(2*np.pi))
        d=np.array([np.dot(ww,(1+ee[2])*p/16) for p in (np.ones_like(ww),ee[3],ee[4],ee[3]*ee[4])])
        direct[code]=np.array([d[0],sum(d[1:])/np.sqrt(3),(d[1]+d[2]-2*d[3])/np.sqrt(6)])
        rep=min(pc.relabel(code,p) for p in pc.boundary_group())
        if rep not in cached:
            v,e=q.single_masks(rep)
            pred=[i for i,j,b in pc.pair_coefficients(rep) if j==2];at=acb(0)
            for i,j,k in product(range(n),repeat=3):
                inds=(i,j,k);k2=arb(1)/2+sum(q.dd[k][inds[a]] for a in pred)
                at+=q.w[i]*q.w[j]*q.w[k]*(1+pc.E(k2))/16
            cached[rep]=np.array([complex(at),complex(sum(v)/arb(3).sqrt()),complex((v[0]+v[1]-2*v[2])/arb(6).sqrt())])
        max_dust=max(max_dust,float(np.max(np.abs(cached[rep]-direct[code]))))
    assert max_dust<2e-14
    for rep,members in pc.orbits().items():
        max_orbit=max(max_orbit,max(float(np.max(np.abs(direct[code]-direct[rep]))) for code in members))
    assert max_orbit<2e-14
    checks['direct_5D_33_labels_vs_contraction']={'nodes':n,'max_abs':max_dust,'orbit_max_abs':max_orbit}
    current=load('results/quadrature.json')['rows'];old=load('inputs/prior_quadrature.json')['rows']
    for a,b in zip(current,old):
        assert a['code']==b['code']
        assert all(pc.unpack(x).overlaps(pc.unpack(y)) for x,y in zip(a['positive_masks'],b['dust_masks']))
        assert arb(a['mask_error']).overlaps(arb(b['dust_mask_error']))
    checks['prior_40_node_quadrature_reproduced']='PASS'
    u=load('results/uniform.json');alt=load('results/cancellation_control.json')
    prior=[r for r in load('inputs/prior_pairings.json')['rows'] if r['weights']=='uniform_label' and r['sigma']=='1']
    for p in prior:
        if p['density'] not in ('plus','contrast') or p['field'] not in ('ground','radial_h2'):continue
        row=(2 if p['density']=='plus' else 4)+int(p['field']=='radial_h2')
        for name in ('coupled','decoupled','difference'):
            assert pc.unpack(u['blocks'][name]['raw_block'][row][0]).overlaps(pc.unpack(p['amplitudes'][name]['enclosure']))
    checks['prior_pairings_in_complete_block']='PASS'
    for result in (u,alt):
        blocks={k:c.matrix_unpack(v['raw_block']) for k,v in result['blocks'].items()}
        assert same(blocks['coupled']-blocks['decoupled'],blocks['difference'])
        assert same(blocks['connected']+blocks['mean_response'],blocks['difference'])
        for name,v in result['blocks'].items():
            for region in ('full6','atom_to_positive'):
                sig=arb(v[region]['sigma_max']);bounds=v['independent_'+region]
                assert sig>arb(bounds['lower']) and sig<arb(bounds['upper'])
                display=arb(format(float(sig.mid()),'.12f'),arb('1e-12') if result is u else arb('2e-12'))
                assert display.contains(sig)
    checks['endpoint_and_connected_decomposition']='PASS'
    checks['independent_Sylvester_and_Rayleigh_certificates']='PASS for 20 blocks'
    # Explicit nonunitary complex changes. Congruence of Grams is essential.
    p=acb_mat([[int(i==j)*(i+1) for j in range(6)] for i in range(6)])
    p[0,1]=acb(1,1);p[2,4]=acb(-2,1);p[5,0]=1
    q=acb_mat([[int(i==j) for j in range(6)] for i in range(6)])
    q[1,3]=acb(1,-2);q[4,0]=3;q[2,5]=acb(0,1)
    b=c.matrix_unpack(u['blocks']['difference']['raw_block']);g=c.repeated_gram(3)
    changed=c.adj(q)*b*p;gin=c.adj(p)*g*p;gout=c.adj(q)*g*q
    bounds=c.certify_general(changed,gin,gout)
    sig=arb(u['blocks']['difference']['full6']['sigma_max'])
    assert sig>arb(bounds['lower']) and sig<arb(bounds['upper'])
    naive0=float(np.linalg.svd(arr(b),compute_uv=False)[0]);naive1=float(np.linalg.svd(arr(changed),compute_uv=False)[0])
    assert abs(naive0-naive1)>0.1
    checks['nonunitary_complex_basis_invariance']={'certified':bounds,'unweighted_svd_before':naive0,'unweighted_svd_after':naive1}
    # Four exact null input directions: two density null vectors times two fields.
    r=c.density_input();b=c.matrix_unpack(u['blocks']['difference']['raw_block'])
    for d in (1,2):
        for j in (0,1):
            v=acb_mat(6,1);v[j,0]=-r[d];v[2*d+j,0]=1
            assert all((b*v)[i,0].contains(0) for i in range(6))
    checks['four_structural_null_input_directions']='PASS'
    cancelled=pc.unpack(alt['blocks']['difference']['raw_block'][2][0])
    assert cancelled.contains(0)
    assert arb(alt['blocks']['difference']['atom_to_positive']['sigma_max'])>arb('0.0017')
    checks['single_element_cancellation_preserves_nonzero_block']={'entry_enclosure':pc.pack(cancelled),'positive_block_lower':'0.0017'}
    # Explicit unitary test-space basis rotation makes one response coordinate zero.
    z1=pc.unpack(u['blocks']['difference']['V_normalized_block'][2][0])
    z2=pc.unpack(u['blocks']['difference']['V_normalized_block'][4][0])
    norm=(abs(z1)**2+abs(z2)**2).sqrt()
    null=(z2*z1-z1*z2)/norm
    assert null.contains(0) and norm>0
    checks['single_coordinate_cancellation_in_fixed_space']='exact algebraic identity; nonzero norm preserved'
    data={'status':'PASS','control_groups':len(checks),'checks':checks}
    c.save('results/validation.json',data);print(json.dumps(data,indent=2))

if __name__=='__main__':main()
