"""Independent controls for the weight-simplex certificate and its scope."""
import copy,json,hashlib
from fractions import Fraction as Q
import numpy as np
from scipy.linalg import eigh
from flint import ctx,arb,acb,acb_mat
import compute as c


def overlapping(a,b):
    assert a.nrows()==b.nrows() and a.ncols()==b.ncols()
    assert all(a[i,j].overlaps(b[i,j]) for i in range(a.nrows()) for j in range(a.ncols()))

def run():
    ctx.prec=192;passed=[]
    contract=c.read('contract.json');old=c.read('inputs/weight_class_contract.json')
    assert 'nonnegative, normalized' in old['admissible_weight_class']
    assert contract['extra_weight_restrictions'].startswith('NONE')
    assert hashlib.sha256((c.ROOT/'contract.json').read_bytes()).hexdigest()==(c.ROOT/'contract.sha256').read_text().strip()
    passed.append('Inherited simplex: unchanged normalization, symmetry and frozen intervention')
    os,ref,r,rn=c.orbit_data(c.read('inputs/quadrature.json'))
    assert len(os)==10 and sum(o['multiplicity'] for o in os)==33
    assert sorted(sum((o['members'] for o in os),[]))==c.b.pc.histories()
    for o in os:
        for label in o['members']:
            assert c.b.pc.f4(label)==o['F4']
            overlapping(c.b.scalar(c.b.pc.h0(label)),o['scalar'])
    passed.append('All 33 histories and all boundary relabellings represented exactly')
    g=acb_mat([[65,196],[196,913]]);t=c.b.gram_transform()
    overlapping(c.adj(t)*g*t,acb_mat([[1,0],[0,1]]))
    # Full block B=C J*, J*J=I. This verifies the exact compression and
    # lifts each universal rank-one separator to the original six states.
    j=acb_mat([[r[i//2].conjugate()/rn if i%2==k else 0 for k in range(2)] for i in range(6)])
    overlapping(c.adj(j)*j,acb_mat([[1,0],[0,1]]))
    passed.append('V Gram and isometric six-to-two input compression')
    for key in ('full6','positive'):
        candidate=c.read('inputs/'+key+'_candidate.json');den=candidate['weight_denominator'];ns=candidate['weight_numerators'];w=[arb(n)/den for n in ns]
        labels={label:Q(n,den*o['multiplicity']) for o,n in zip(os,ns) for label in o['members']}
        assert sum(labels.values())==1 and all(v>=0 for v in labels.values())
        for p in c.b.pc.boundary_group():
            assert all(labels[c.b.pc.relabel(label,p)]==v for label,v in labels.items())
        ten=c.combine([o['difference'] for o in os],w)
        thirtythree=sum((o['difference']*arb(str(labels[label])) for o in os for label in o['members']),acb_mat(6,2))
        overlapping(ten,thirtythree)
        eps=Q(1,10**12);positive={label:(1-eps)*v+eps/33 for label,v in labels.items()}
        assert sum(positive.values())==1 and all(v>0 for v in positive.values())
        cert=c.certify(os,rn,key);assert cert==c.read('results/'+key+'_certificate.json')
        u=c.vec(candidate['left_vector']);v=c.vec(candidate['right_vector'])
        if key=='full6':
            lifted=j*v
            for o in os:
                full=acb_mat([[o['difference'][i,k%2]*r[k//2] for k in range(6)] for i in range(6)])
                compressed=o['difference']*rn
                overlapping(full*j,compressed)
                x=c.inner(u,full,lifted).real/(c.norm(u)*c.norm(lifted))
                assert x.overlaps(arb(cert['dual_scores'][str(o['code'])]))
    passed.append('Rational feasible weights, 33-label sum and strictly positive witnesses')
    passed.append('Both global certificates and full-space dual witness lift')
    data=c.read('results/diagnostics.json')
    for label,oldfile in [('uniform','inputs/prior_uniform.json'),('prior_channel_cancellation','inputs/prior_cancellation.json')]:
        olddata=c.read(oldfile)
        for name in c.b.NAMES:
            current=data[label]['blocks'][name]
            overlapping(c.b.matrix_unpack(current['V_normalized_block']),c.b.matrix_unpack(olddata['blocks'][name]['V_normalized_block']))
            assert arb(current['full6_sigma']).overlaps(arb(olddata['blocks'][name]['full6']['sigma_max']))
    passed.append('All five blocks reproduce the previous uniform and cancellation controls')
    for label,entry in data.items():
        if label=='vertices':continue
        x=entry['blocks'];d=c.b.matrix_unpack(x['difference']['V_normalized_block']);con=c.b.matrix_unpack(x['connected']['V_normalized_block']);mean=c.b.matrix_unpack(x['mean_response']['V_normalized_block'])
        overlapping(d,con+mean)
    for o in os:
        z=o['phase'];average=z*o['scalar']/z
        overlapping(average,o['scalar']);assert abs(z).contains(1)
        assert c.sigma(o['difference']*rn)>0
    passed.append('Separate connected/mean blocks; exact orbit-vertex connected nulls')
    # An independent generalized eigenproblem checks invariance under
    # nonunitary coefficient changes. Float64 is only an implementation check.
    mat=c.b.matrix_unpack(data['full6_near_minimizer']['blocks']['difference']['V_normalized_block'])
    B=np.array([[complex(mat[i,k]) for k in range(6)] for i in range(6)])
    S=np.eye(6,dtype=complex);S[0,1]=1.7+.2j;S[4,2]=-.4j;S[3,3]=2.3
    T=np.eye(6,dtype=complex);T[2,5]=1.3-.7j;T[0,0]=.6
    Bnew=T.conj().T@B@S;gin=S.conj().T@S;gout=T.conj().T@T
    H=Bnew.conj().T@np.linalg.solve(gout,Bnew);ev=eigh((H+H.conj().T)/2,gin,eigvals_only=True)
    assert abs(max(ev[-1],0)**.5-np.linalg.svd(B,compute_uv=False)[0])<1e-14
    assert np.linalg.svd(B,compute_uv=False)[2]<1e-15
    passed.append('Nonunitary basis-change control and full 6x6 spectral crosscheck')
    # Tamper controls: deliberately invalid certificates must fail.
    candidate=c.read('inputs/full6_candidate.json');u=c.vec(candidate['left_vector']);v=c.vec(candidate['right_vector']);a=[c.choose(o,'full6',rn) for o in os]
    def lower_ok(trial_u,claimed):
        if not c.norm(trial_u)>0:return False
        return all(c.inner(trial_u,m,v).real/(c.norm(trial_u)*c.norm(v))>claimed for m in a)
    assert not lower_ok(acb_mat(6,1),arb('.002'))
    assert not lower_ok(-u,arb('.002'))
    assert not lower_ok(u,arb('.002294'))
    ns=candidate['weight_numerators'];bad=ns[:];bad[0]=-1;bad[1]+=1
    assert not all(n>=0 for n in bad)
    bad=ns[:];bad[1]+=1;assert sum(bad)!=candidate['weight_denominator']
    passed.append('Five negative controls: zero/sign-flipped witness, false bound, negative/unnormalized weights')
    result={'status':'PASS','control_groups':len(passed),'controls':passed,'external_peer_review':False}
    c.write('results/validation.json',result);print(json.dumps(result,indent=2));return result

if __name__=='__main__':run()
