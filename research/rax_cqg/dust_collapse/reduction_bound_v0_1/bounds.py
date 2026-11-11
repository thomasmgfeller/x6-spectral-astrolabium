"""Analytic whole-tail bounds in the declared weighted test topology.

No truncated coefficient sum is used as an upper tail bound. All 33 histories
enter the constants, and both directions of the pairing are controlled.
"""
from functools import lru_cache
from math import factorial, comb
from pathlib import Path
import json
import sympy as s
from flint import arb, acb, acb_mat, ctx
from inputs import prior_core as pc
from inputs import prior_sewing as ps

ROOT=Path(__file__).resolve().parent
BETA2=s.Rational(8,3)
BETA=4/s.sqrt(6)
OUTER=(0,1,6,7); INNER=(2,3,4,5)

def aa(x):
    x=s.expand(x)
    if x.is_Rational:return arb(int(s.numer(x)))/int(s.denom(x))
    a=s.expand(x).coeff(s.sqrt(6),0);b=s.expand(x).coeff(s.sqrt(6),1)
    if s.simplify(x-a-b*s.sqrt(6))!=0:raise ValueError('unsupported algebraic constant: '+str(x))
    return aa(a)+aa(b)*arb(6).sqrt()

def pack(z):return z.str(30,more=True)

def expectation(poly,ts,rs=(),density_profile=None):
    """Exact moments: normalized box clocks; atom-plus-uniform densities.

    Optional output profiles condition density coordinates 3,4 to 00 or +.
    The + profile is the equal mixture of the three positive-support masks
    under the positive measure used in a norm bound, not a decoherence claim.
    """
    variables=tuple(ts)+tuple(rs);total=s.Rational(0)
    for powers,c in s.Poly(s.expand(poly),*variables).terms():
        pt=powers[:len(ts)];pr=powers[len(ts):]
        if any(k%2 for k in pt):continue
        value=c*s.prod(s.Rational(1,k+1) for k in pt)
        for i,k in enumerate(pr):
            if density_profile is not None and i in (3,4):continue
            if k:value*=s.Rational(1,2*(k+1))
        if density_profile is not None:
            k,l=pr[3],pr[4]
            if density_profile=='0':factor=int(k==0 and l==0)
            elif density_profile=='+':
                factor=(s.Rational(int(l==0),k+1)+s.Rational(int(k==0),l+1)+s.Rational(1,(k+1)*(l+1)))/3
            else:raise ValueError('density profile')
            value*=factor
        total+=value
    return s.factor(total)

@lru_cache(None)
def density_moment(incoming,constant=s.Rational(1,2)):
    t=s.symbols('t:'+str(len(incoming)+1));A=sum(c*(t[0]-t[i+1])**2 for i,c in enumerate(incoming))
    moments=[expectation(A**k,t) for k in range(5)]
    def kpower(n):
        return sum(comb(n,k)*constant**(n-k)*(BETA/4)**k*moments[k] for k in range(n+1))
    return s.expand(kpower(2)/6+kpower(4)/60)

@lru_cache(None)
def clock_moment(terms,j,density_profile=None):
    t=s.symbols('t:5');r=s.symbols('r:5')
    a=s.Rational(0);b=s.Rational(0)
    for i,k,c in terms:
        if j not in (i,k):continue
        other=k if j==i else i
        a-=s.Rational(c,2)*r[k]*(t[j]-t[other]);b-=s.Rational(c,2)*r[k]
    first=expectation((1-t[j]**2)**2*a**4,t,r,density_profile)
    second=expectation((2*t[j]*a-(1-t[j]**2)*b)**2,t,r,density_profile)
    return s.factor(BETA2**2*first+BETA2*second)

def field_energy(D0,E0):
    """Exact normalized L2 norm squared of H_y[s(y)s(x)e^(i phi)].

    s(q)=(1+|q|^2)^-2. The full field integral is (pi/3)^2
    times this rational expression. D=beta*D0, E=beta*E0.
    """
    d2=BETA2*(D0*D0).trace();d4=BETA2**2*(D0**4).trace()
    trd2=BETA2*D0.trace()**2
    B0=E0*E0.T;trb=BETA2*B0.trace();trb2=BETA2**2*(B0*B0).trace()
    dbd=BETA2**2*(D0*B0*D0).trace()
    value=s.Rational(583,35)+s.Rational(11,5)*d2-s.Rational(1,5)*trd2+s.Rational(53,20)*trb
    value+=(d2**2+2*d4+trb*d2+2*dbd+trb**2+2*trb2)/8
    return s.factor(value)

def schur(code):
    h=s.Matrix(pc.h0(code));b=(0,1,3,4)
    return h.extract(b,b)-h.extract(b,(2,))*h.extract((2,),b)/h[2,2]

def geometry_records():
    records=[]
    for code in pc.histories():
        terms=tuple(pc.pair_coefficients(code));h=s.Matrix(pc.h0(code));k=schur(code)
        record={'code':code,'alpha_over_beta':str(-h[2,2]),
                'field_energy_in':str(field_energy(k[:2,:2],k[:2,2:])),
                'field_energy_out':str(field_energy(k[2:,2:],k[2:,:2])),
                'density_energy':{},'clock_energy':{},'sewing':{}}
        for j in (0,1,3,4):
            inc=tuple(sorted(c for i,k2,c in terms if k2==j))
            record['density_energy'][str(j)]=str(density_moment(inc))
            record['clock_energy'][str(j)]=str(clock_moment(terms,j))
        for side,seam,other in [('left',(3,4),(0,1,2)),('right',(0,1),(2,3,4))]:
            d=h.extract(seam,seam);b=h.extract(seam,other)
            data={'D_frobenius_squared':str(BETA2*sum(x*x for x in d)),
                  'B_frobenius_squared':str(BETA2*sum(x*x for x in b)),
                  'abs_trace_D_over_beta':str(abs(d.trace()))}
            if side=='left':
                data['density_energy_sum']=str(sum(density_moment(tuple(sorted(c for i,k2,c in terms if k2==j)),s.Rational(0)) for j in seam))
                data['clock_energy_sum']=str(sum(clock_moment(terms,j) for j in seam))
            else:
                data['density_energy_sum']=str(2*density_moment(()))
                data['clock_energy_sum_by_output_density']={p:str(sum(clock_moment(terms,j,p) for j in seam)) for p in ('0','+')}
            record['sewing'][side]=data
        records.append(record)
    return records

def constants(records):
    beta=pc.beta();pref=arb.pi()/6
    answer={}
    for side,vertices in [('forward',(3,4)),('backward',(0,1))]:
        f=arb(0);rho=[arb(0),arb(0)];clock=[arb(0),arb(0)]
        for row in records:
            c=(2*arb.pi()/(beta*aa(s.sympify(row['alpha_over_beta'])))).sqrt()/33
            f+=c*aa(s.sympify(row['field_energy_out' if side=='forward' else 'field_energy_in'])).sqrt()
            for k,j in enumerate(vertices):
                rho[k]+=c*aa(s.sympify(row['density_energy'][str(j)])).sqrt()
                clock[k]+=c*aa(s.sympify(row['clock_energy'][str(j)])).sqrt()
        answer[side]={'field':pref*f,'density':[(pref*x) for x in rho],'clock':[(pref*x) for x in clock]}
    answer['kernel_norm']=(arb.pi()/6)*(2*arb.pi()/beta).sqrt()
    e=acb(0,-arb(1)/4).exp()*(arb(1)/4).sinc()
    zeta=(2*e+e*e)/arb(3).sqrt()
    answer['zeta']=zeta;answer['zeta_abs']=abs(zeta)
    return answer

def tail_constant(c,N,D,T):
    if min(N,D,T)<0:raise ValueError('nonnegative cutoffs required')
    lq=2*N+4;lr=(D+1)*(D+2);lt=(T+1)*(T+2)
    return ((c['field']/lq)**2+sum((x/lr)**2 for x in c['density'])+sum((x/lt)**2 for x in c['clock'])).sqrt()

def dimension(N,D,T,invariant=True):
    F=(N+1)*(N+2)//2;L=(D+2)*(T+1)
    return (F*L*L+(N//2+1)*L)//2 if invariant else F*L*L

def single_bounds(c,N,D,T):
    if N<5:raise ValueError('N>=5 required to retain all four original inputs exactly')
    forward=tail_constant(c['forward'],N,D,T);backward=tail_constant(c['backward'],N,D,T)
    C0=(2*arb.pi()/pc.beta()).sqrt();embed=(arb.pi()/6).sqrt()
    L1=[2*arb.pi().sqrt(),arb(4)];density=[1/(2*arb(2).sqrt()),arb(3).sqrt()/(2*arb(2).sqrt())]
    fn=[];bn=[]
    # The minimum of two upper bounds is again an upper bound; use endpoints.
    minimum=lambda a,b: arb(min(a.upper(),b.upper()))
    for si in (0,1):
        for n in (0,1):
            vf=arb(65 if n==0 else 261).sqrt()
            atom=minimum(forward*vf,C0*embed*density[0]*L1[n])
            fn.append(minimum(atom*(1 if si==0 else c['zeta_abs']),forward*vf))
            bn.append(minimum(backward*vf,C0*embed*density[si]*L1[n]))
    forward_class=minimum(arb(261).sqrt()*forward,(1+c['zeta_abs']**2).sqrt()*max(fn[0].upper(),fn[1].upper()))
    backward_class=minimum(arb(261).sqrt()*backward,arb(max((bn[0]**2+bn[2]**2).sqrt().upper(),(bn[1]**2+bn[3]**2).sqrt().upper())))
    return {'cutoffs':[N,D,T],'invariant_dimension':dimension(N,D,T),
            'forward_columns':[pack(x) for x in fn],'backward_columns':[pack(x) for x in bn],
            'forward_class_bound':pack(arb(forward_class)),'backward_class_bound':pack(arb(backward_class)),
            'full_V_to_Vprime_error':pack(minimum(c['kernel_norm'],(forward**2+backward**2).sqrt())),
            'full_C_M_class_error':pack(arb(261).sqrt()*minimum(c['kernel_norm'],(forward**2+backward**2).sqrt()))}

def joint_data(l,r):
    rel=ps.transitive_closure(range(8),pc.relations(l)|{(i+3,j+3) for i,j in pc.relations(r)})
    action=ps.local_action(range(8),rel)
    return s.Matrix(ps.doubled_hessian(action))/2,action['F4']

def joint_matrix(l,r):return joint_data(l,r)[0]

def scalar_pair(h,epsilon):
    """Exactly integrated 00/11 scalar pairings with a certified Abel branch."""
    eps=arb(epsilon);order=OUTER+INNER;beta=pc.beta()
    q=[[acb((1 if i in OUTER else eps) if i==j else 0,-beta*aa(h[i,j])) for j in order] for i in order]
    original=acb_mat(q);root=acb(1)
    for k in range(8):
        pivot=q[k][k]
        if eps>0:
            if not pivot.real>0:raise ArithmeticError('Gaussian accretivity lost')
        elif not(pivot.real>0 or pivot.imag>0 or pivot.imag<0):raise ArithmeticError('uncertified Abel pivot')
        root*=pivot.sqrt(analytic=True)
        for i in range(k+1,8):
            for j in range(k+1,8):q[i][j]-=q[i][k]*q[k][j]/pivot
    inv=original.inv()
    base=16*arb.pi()**3/root
    odd=sum(inv[i,j] for i in (0,1) for j in (2,3))
    return base,base*odd

def sewing_sector(row,side,n,density,epsilon,N,D,T):
    eps=arb(epsilon);v=row['sewing'][side]
    d2=aa(s.sympify(v['D_frobenius_squared']));b2=aa(s.sympify(v['B_frobenius_squared']))
    d=d2.sqrt();tr=pc.beta()*aa(s.sympify(v['abs_trace_D_over_beta']))
    c=3*eps/2+abs(1-eps**2/4)*arb(8).sqrt()/eps+2*d2*arb(8).sqrt()/eps+d*arb(8).sqrt()+tr
    m2=arb(n+2)+1/eps;m4=arb((n+2)*(n+4))+2*(n+2)/eps+3/eps**2
    U=c*c+6*c*b2*m2+9*b2*b2*m4
    R=aa(s.sympify(v['density_energy_sum']))
    Tenergy=aa(s.sympify(v['clock_energy_sum'] if side=='left' else v['clock_energy_sum_by_output_density'][density]))
    tail=(U/(2*N+4)**2+R/((D+1)*(D+2))**2+Tenergy/((T+1)*(T+2))**2).sqrt()
    return tail,{'field_energy':U,'density_energy':R,'clock_energy':Tenergy}

def sewing_cut_bound(records,c,epsilon,N,D,T):
    eps=arb(epsilon);density=[1/(2*arb(2).sqrt()),arb(3).sqrt()/(2*arb(2).sqrt())]
    envelopes=[[arb(0) for _ in range(4)] for _ in range(4)];classes=[]
    for n in (0,1):
        L1=2*arb.pi().sqrt() if n==0 else arb(4)
        left=sum(sewing_sector(row,'left',n,'0',epsilon,N,D,T)[0] for row in records)/33
        column=[]
        for ri,p in enumerate(('0','+')):
            right=sum(sewing_sector(row,'right',n,p,epsilon,N,D,T)[0] for row in records)/33
            val=4*arb.pi()**2*L1**2/eps**2*left*right*density[0]*density[ri]
            envelopes[2*ri+n][n]=val
            envelopes[2*ri+n][2+n]=val*c['zeta_abs']
            column.append(val)
        classes.append((1+c['zeta_abs']**2).sqrt()*(column[0]**2+column[1]**2).sqrt())
    return envelopes,arb(max(x.upper() for x in classes))

def write(name,data):
    p=ROOT/name;p.parent.mkdir(parents=True,exist_ok=True)
    p.write_text(json.dumps(data,sort_keys=True,indent=2)+'\n')

if __name__=='__main__':
    ctx.prec=192
    rows=geometry_records();write('results/geometry_constants.json',rows)
    c=constants(rows)
    data={side:{'field':pack(c[side]['field']),'density':[pack(x) for x in c[side]['density']],
                'clock':[pack(x) for x in c[side]['clock']]} for side in ('forward','backward')}
    data['kernel_norm']=pack(c['kernel_norm']);data['zeta']={'real':pack(c['zeta'].real),'imag':pack(c['zeta'].imag),'absolute':pack(c['zeta_abs'])}
    write('results/operator_constants.json',data)
    print(json.dumps(data,indent=2))
