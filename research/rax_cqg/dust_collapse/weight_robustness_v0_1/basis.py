"""Certified finite blocks in the weighted test/antidual norm. No network."""
import argparse
import hashlib
import json
from pathlib import Path
from time import monotonic
from flint import arb, acb, acb_mat, ctx
from inputs import core as pc
from inputs.prior_quadrature import Quadrature, ellipse_tail

ROOT = Path(__file__).resolve().parent
NAMES = ('coupled','decoupled','difference','connected','mean_response')

def save(path, data):
    (ROOT/path).write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')

def adj(a): return a.conjugate().transpose()
def matrix_pack(a): return [[pc.pack(a[i,j],32) for j in range(a.ncols())] for i in range(a.nrows())]
def matrix_unpack(a): return acb_mat([[pc.unpack(z) for z in row] for row in a])
def realstr(a): return a.str(30,more=True)

def scalar(h):
    """Boundary-first Gaussian pivots; polynomial moments by Wick's identity."""
    order = (0,1,3,4,2)
    b=pc.beta()
    q=acb_mat([[acb(int(i==j and k<4),-b*arb(str(h[i][j])))
                for j in order] for k,i in enumerate(order)])
    v=q.inv(); work=[[q[i,j] for j in range(5)] for i in range(5)]
    root=acb(1)
    for k in range(5):
        p=work[k][k]
        if not (p.real>0 or (k==4 and p.imag>0)):
            raise ArithmeticError('Gaussian branch not certified')
        root*=p.sqrt(analytic=True)
        for i in range(k+1,5):
            for j in range(k+1,5): work[i][j]-=work[i][k]*work[k][j]/p
    a=4*arb.pi()*(2*arb.pi()).sqrt()/root
    x=v[0,0]+v[1,1]-1; y=v[2,2]+v[3,3]-1
    cross=2*sum(v[i,j]*v[i,j] for i in (0,1) for j in (2,3))
    return acb_mat([[a,a*x],[a*y,a*(x*y+cross)]])

def gram_transform():
    # columns give an exactly V-orthonormal basis; original h0,hR are H-orthonormal
    return acb_mat([[1/arb(65).sqrt(),-arb(196)/(arb(65)*arb(20929)).sqrt()],
                    [0,(arb(65)/20929).sqrt()]])

def density_input():
    e=pc.E(arb(1)/2)
    return [acb(1),(2*e+e*e)/arb(3).sqrt(),(2*e-2*e*e)/arb(6).sqrt()]

def quadrature(n=40):
    q=Quadrature(n); rows=[]; start=monotonic()
    for code,members in pc.orbits().items():
        vals,error=q.single_masks(code)
        pred=[i for i,j,c in pc.pair_coefficients(code) if j==2]
        # outgoing atom mask: output clocks integrate to one exactly
        atom=acb(0)
        for i,wi in enumerate(q.w):
            for j,wj in enumerate(q.w):
                for k,wk in enumerate(q.w):
                    inds=(i,j,k)
                    k2=arb(1)/2+sum(q.dd[k][inds[a]] for a in pred)
                    atom+=wi*wj*wk*(1+pc.E(k2))/16
        degrees=[int(v in pred)+len(pred)*int(v==2) for v in range(5)]
        atom_error=ellipse_tail(n,degrees,2,arb(1)/8)
        rows.append({'code':code,'members':members,'F4':pc.f4(code),
                     'positive_masks':[pc.pack(z,32) for z in vals],
                     'mask_error':realstr(error),'atom':pc.pack(atom,32),'atom_error':realstr(atom_error)})
        print(f'orbit {code}: {monotonic()-start:.1f}s',flush=True)
    return {'n':n,'precision_bits':ctx.prec,'rows':rows}

def dust(row):
    v=[pc.unpack(z) for z in row['positive_masks']];e=arb(row['mask_error'])
    return ([pc.unpack(row['atom']),sum(v)/arb(3).sqrt(),(v[0]+v[1]-2*v[2])/arb(6).sqrt()],
            [arb(row['atom_error']),arb(3).sqrt()*e,4/arb(6).sqrt()*e])

def cancellation_weights(rows,scalars,ref):
    # Same exact affine barycentric definition and fixed orbit triple as predecessor.
    old=json.loads((ROOT/'inputs/prior_weight_counterexample.json').read_text())
    codes=old['orbit_codes'];vs={}
    for row in rows:
        d,e=dust(row); c=row['code']
        vs[c]=acb(0,row['F4']).exp()*pc.widen(d[1],e[1])*(scalars[c][0,0]-ref[0,0])
    cross=lambda a,b:a.real*b.imag-a.imag*b.real
    mass=arb(993)/1000; target=-sum(v for c,v in vs.items() if c not in codes)/1000
    a,b,c=[vs[k] for k in codes];u=a-c;v=b-c;r=target-mass*c;den=cross(u,v)
    if den.contains(0):raise ArithmeticError('weight determinant unresolved')
    w1=cross(r,v)/den;w2=cross(u,r)/den
    ws={k:arb(1)/1000 for k in vs};ws.update(dict(zip(codes,(w1,w2,mass-w1-w2))))
    if not all(w>0 for w in ws.values()):raise ArithmeticError('weights not positive')
    if not sum(ws.values()).contains(1):raise ArithmeticError('weights not normalized')
    return ws

def gram2_certificate(c):
    """Both squared singular values of a matrix with two columns."""
    h=adj(c)*c
    a=h[0,0].real;d=h[1,1].real;z=h[0,1]
    gap=((a-d)*(a-d)+4*(abs(z)**2)).sqrt()
    hi=(a+d+gap)/2;lo=(a+d-gap)/2
    if not (hi>0 and lo>0):raise ArithmeticError('rank two / positive eigenvalues not certified')
    return {'sigma_max':realstr(hi.sqrt()),'sigma_second':realstr(lo.sqrt()),
            'squared_singular_Gram':matrix_pack(h),'rank':'EXACTLY_TWO',
            'remaining_singular_values':'EXACT_ZERO by incoming-density factorization'}

def certify_general(b,gin,gout):
    """Independent generalized Rayleigh lower bound and Sylvester upper bound.

    Float64 supplies a trial vector and rational candidates only. Every reported
    inequality is then verified by interval arithmetic on the original Grams.
    """
    import numpy as np
    from scipy.linalg import eigh
    def npmat(m):return np.array([[complex(m[i,j]) for j in range(m.ncols())] for i in range(m.nrows())])
    h=adj(b)*gout.inv()*b
    hn=npmat(h);gn=npmat(gin)
    ev,vec=eigh((hn+hn.conj().T)/2,gn)
    center=float(max(ev[-1],0)**.5)
    v=acb_mat([[acb(arb(format(z.real,'.17g')),arb(format(z.imag,'.17g')))] for z in vec[:,-1]])
    ray=((adj(v)*h*v)[0,0].real/(adj(v)*gin*v)[0,0].real).sqrt()
    # Outward rational candidates, enlarged until a fully verified certificate exists.
    scale=10**10
    lower=arb(max(0,int(center*scale)-2))/scale
    upper=arb(int(center*scale)+3)/scale
    if not ray>lower:raise ArithmeticError('trial vector failed lower bound')
    positive=upper*upper*gin-h
    determinants=[]
    for k in range(1,b.ncols()+1):
        sub=acb_mat([[positive[i,j] for j in range(k)] for i in range(k)])
        det=sub.det()
        if not det.imag.contains(0) or not det.real>0:raise ArithmeticError('upper-bound positivity failed')
        determinants.append(realstr(det.real))
    return {'lower':realstr(lower),'upper':realstr(upper),'Rayleigh_lower':realstr(ray.lower()),
            'trial_vector':matrix_pack(v),'Sylvester_determinants':determinants}

def repeated_gram(count):
    g=((65,196),(196,913))
    return acb_mat([[g[i%2][j%2] if i//2==j//2 else 0 for j in range(2*count)] for i in range(2*count)])

def analyze(data,alternative=False):
    rows=data['rows'];ref=scalar(pc.reference_h0());ss={r['code']:scalar(pc.h0(r['code'])) for r in rows}
    weights=cancellation_weights(rows,ss,ref) if alternative else {r['code']:arb(len(r['members']))/33 for r in rows}
    z=sum(weights[r['code']]*acb(0,r['F4']).exp() for r in rows)
    if not z.abs_lower()>0:raise ArithmeticError('gravity normalization for diagnostic unresolved')
    avg=sum((weights[r['code']]*acb(0,r['F4']).exp()*ss[r['code']] for r in rows),acb_mat(2,2))/z
    raw={n:acb_mat(6,2) for n in NAMES};errors={n:[[arb(0) for j in range(2)] for i in range(6)] for n in NAMES}
    for row in rows:
        code=row['code'];p=weights[code]*acb(0,row['F4']).exp();ds,es=dust(row)
        factors=dict(zip(NAMES,(ss[code],ref,ss[code]-ref,ss[code]-avg,avg-ref)))
        for name,a in factors.items():
            for density in range(3):
                for i in range(2):
                    for j in range(2):
                        raw[name][2*density+i,j]+=p*ds[density]*a[i,j]
                        errors[name][2*density+i][j]+=abs(weights[code])*es[density]*abs(a[i,j])
    t=gram_transform();r=density_input();rnorm=sum(abs(x)**2 for x in r).sqrt()
    output={}
    for name in NAMES:
        enclosed=acb_mat([[pc.widen(raw[name][i,j],errors[name][i][j]) for j in range(2)] for i in range(6)])
        normalized=acb_mat(6,2)
        for density in range(3):
            sub=acb_mat([[enclosed[2*density+i,j] for j in range(2)] for i in range(2)])
            a=adj(t)*sub*t
            for i in range(2):
                for j in range(2):normalized[2*density+i,j]=a[i,j]
        full=acb_mat([[enclosed[i,j%2]*r[j//2] for j in range(6)] for i in range(6)])
        normfull=acb_mat([[normalized[i,j%2]*r[j//2] for j in range(6)] for i in range(6)])
        positive=acb_mat([[normalized[i,j] for j in range(2)] for i in range(2,6)])
        rawpositive=acb_mat([[enclosed[i,j] for j in range(2)] for i in range(2,6)])
        output[name]={'raw_block':matrix_pack(full),'V_normalized_block':matrix_pack(normfull),
                      'compressed_atom_input':matrix_pack(enclosed),
                      'analytic_entry_error_atom_input':[[realstr(x) for x in row] for row in errors[name]],
                      'full6':gram2_certificate(normalized*rnorm),
                      'atom_to_positive':gram2_certificate(positive),
                      'independent_full6':certify_general(full,repeated_gram(3),repeated_gram(3)),
                      'independent_atom_to_positive':certify_general(rawpositive,repeated_gram(1),repeated_gram(2))}
    return {'weights':'previous_full_support_cancellation' if alternative else 'uniform_label',
            'orbit_weights':{str(k):realstr(v) for k,v in weights.items()},'gravity_sum':pc.pack(z,32),
            'scalar_average':matrix_pack(avg),'scalar_reference':matrix_pack(ref),
            'incoming_density_row': [pc.pack(x,32) for x in r],
            'incoming_density_norm':realstr(rnorm),'blocks':output}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--reuse-quadrature',action='store_true');args=parser.parse_args()
    if hashlib.sha256((ROOT/'contract.json').read_bytes()).hexdigest()!=(ROOT/'contract.sha256').read_text().strip():
        raise ArithmeticError('fixed contract changed')
    ctx.prec=192
    data=json.loads((ROOT/'results/quadrature.json').read_text()) if args.reuse_quadrature else quadrature()
    if not args.reuse_quadrature:save('results/quadrature.json',data)
    for alt,file in ((False,'uniform'),(True,'cancellation_control')):
        result=analyze(data,alt);save(f'results/{file}.json',result)
        print(file,{name:{k:b[k]['sigma_max'] for k in ('full6','atom_to_positive')} for name,b in result['blocks'].items()},flush=True)

if __name__=='__main__':main()
