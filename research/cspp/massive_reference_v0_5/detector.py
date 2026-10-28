"""Independent spatial interval cubature for the scalar KG detector Gram matrix.

Every spatial and source cell is evaluated as a full interval. No convergence
fit or midpoint-only quadrature is used in this certificate. This is explicitly
NOT the four-spinor E4 detector reference.
"""
from functools import lru_cache
from flint import arb, acb, ctx
import reference as ref

@lru_cache(None)
def _parameters(bits):
    A=ref.previous.normalization(bits)[0]
    a=arb('1/2');k=arb(4);tau=arb(2);hc=arb('1/32')
    return A,a,k,tau,hc,a*(1-hc).sqrt(),acb(0,1)

def parameters():return _parameters(ctx.prec)

def field_range(R,c,m,region):
 A,a,k,tau,hc,b,I=parameters()
 d=2-R; K=acb(0);M=acb(0);V=acb(0)
 def outer_integrate(f,l,u):
  total=acb(0)
  for i in range(128):
   q=acb(arb(2*i+1)/256,0)+acb(arb(0,arb(1)/256),0)
   ss=u-(u-l)*(1-q)
   v=f(ss,True)*(u-l)/128
   if not v.is_finite():return acb('nan')
   total+=v
  return total
 if region:
  def km(s,analytic,which):
   h=1-s*s/a**2
   if h.contains(0):return acb('nan')
   mu=(s*s-R*R-tau*tau)/(2*R*tau);w=k*k*tau*tau*(1-c*c)*(1-mu*mu)
   j0=(-w/4).hypgeom_0f1(1)
   kernel=j0 if which=='M' else (1-2*tau*(tau+R*mu)/(a*a)/h/h+I*k*tau*c*mu)*j0-w/2*(-w/4).hypgeom_0f1(2)
   return A/(2*R*tau)*s*(-1/h).exp()*(I*k*c*(R+tau*mu)).exp()*kernel
  K=outer_integrate(lambda s,z:km(s,z,'K'),d,b);M=outer_integrate(lambda s,z:km(s,z,'M'),d,b)
 edges=[(acb(0),d,True),(d,acb(b),False)] if region else [(acb(0),acb(b),True)]
 for lo,hi,full in edges:
  def f(s,analytic):
   h=1-s*s/a**2
   if h.contains(0):return acb('nan')
   v0=acb(-1) if full else s/(2*R)-d*(tau+R)/(2*R*s)
   def g(q,_):
    v=v0+(1-v0)*q;ss=tau*tau-R*R-s*s+2*R*s*v
    return (1-v0)*(I*k*c*s*v).exp()*(-k*k*s*s*(1-c*c)*(1-v*v)/4).hypgeom_0f1(1)*(-m*m*ss/4).hypgeom_0f1(3)
   inner=sum(g(acb(arb(2*j+1)/32+arb(0,arb(1)/32)),False)/16 for j in range(16))
   return s*s*A/2*(-1/h).exp()*inner
  V+=outer_integrate(f,lo,hi)
 return K-m*m*tau*tau/2*M+arb(m)**4*tau/8*V



def hull(lo,hi):
    return arb((lo+hi)/2,((hi-lo)/2).abs_upper())


def cap_cos_range(lo,hi):
    g=lambda x:(x+2/x)/3
    root=arb(2).sqrt()
    if hi<root:return hull(g(hi).lower(),g(lo).upper())
    if lo>root:return hull(g(lo).lower(),g(hi).upper())
    return hull((2*root/3).lower(),max(g(lo).upper(),g(hi).upper()))


def primitive(R):
    return 2*arb.pi()/3*(-R**4/4+R**3-R**2)


def partition():
    b=parameters()[5];split=2-b;delta=arb('1e-7')
    intervals=[]
    for i in range(32):
        intervals.append((1+(split-1)*i/32,1+(split-1)*(i+1)/32,0))
    ds=[b*j/32 for j in range(32,0,-1)]
    while ds[-1]/2>delta:ds.append(ds[-1]/2)
    ds.append(delta)
    for d0,d1 in zip(ds[:-1],ds[1:]):intervals.append((2-d0,2-d1,1))
    return intervals,delta


def tail_bounds(m):
    A,a,k,tau,hc,b,I=parameters()
    K=A*(-1/hc).exp()*(1+k*tau+2*tau*(tau+2)/(a*a*hc*hc))
    M=m*m*tau*tau/2*A*(-1/hc).exp()
    V=arb(m)**4*tau*A*a**3/24*(-1/hc).exp()
    # Source gradient: |∇f| <= A[(2/a) max e^-1/h h^-2 + k/e].
    F0=A/arb(1).exp();F1=A*(8/a*(-arb(2)).exp()+k/arb(1).exp())
    bound=F0+tau*F1+m*m*tau*tau/2*F0+arb(m)**4*tau*a**3/24*F0
    return K+M+V,bound


def compute():
    intervals,delta=partition();G11=arb(0);G22=arb(0);G12=acb(0);volume=arb(0)
    cells=0
    for j,(lo,hi,region) in enumerate(intervals):
        R=hull(lo,hi);cmin=cap_cos_range(lo,hi)
        weight=(primitive(hi)-primitive(lo))/8
        if not weight>0:raise ArithmeticError('nonpositive cell weight')
        for i in range(8):
            u=hull(arb(i)/8,arb(i+1)/8)
            c=1-(1-cmin)*(1-u)
            f=field_range(acb(R),acb(c),1,region)
            g=field_range(acb(R),acb(c),2,region)
            if not (f.is_finite() and g.is_finite()):
                raise ArithmeticError('DETECTOR_HOLD: nonfinite range cell '+str((j,i)))
            G11+=weight*(f.real**2+f.imag**2)
            G22+=weight*(g.real**2+g.imag**2)
            G12+=weight*f*g.conjugate();volume+=weight;cells+=1
        if j%8==0:print('detector radial strip',j,'/',len(intervals),flush=True)
    full_volume=arb.pi()/6
    cap=full_volume-volume
    e1,B1=tail_bounds(1);e2,B2=tail_bounds(2)
    # If |phi_j - core_j|<=e_j and |phi_j|<=B_j, product error is
    # <= B_i e_j+B_j e_i+e_i e_j. Use full volume conservatively.
    tails={'11':full_volume*(2*B1*e1+e1*e1),
           '22':full_volume*(2*B2*e2+e2*e2),
           '12':full_volume*(B1*e2+B2*e1+e1*e2)}
    caps={'11':cap.abs_upper()*B1*B1,'22':cap.abs_upper()*B2*B2,'12':cap.abs_upper()*B1*B2}
    raw={'11':acb(G11),'22':acb(G22),'12':G12}
    final={}
    for key,z in raw.items():
        error=tails[key]+caps[key]
        final[key]=acb(z.real+arb(0,error.abs_upper())) if key!='12' else ref.balls.inflate(z,error)
    return {'schema':'cspp.scalar-detector-interval-cubature/0.5','precision_bits':ctx.prec,
        'detector':{'time':1,'center':[0,0,1.5],'radius':0.5},
        'integrand':'G_ij = integral_D phi_mi conjugate(phi_mj) d3x; zero-velocity scalar KG',
        'masses':[1,2],'spatial_cells':cells,'source_radial_cells':128,'source_angular_cells':16,
        'spatial_volume_included':ref.balls.encode(volume),'omitted_cap_volume':ref.balls.encode(cap),
        'source_component_tail_bounds':{'1':ref.balls.encode(e1),'2':ref.balls.encode(e2)},
        'uniform_field_bounds':{'1':ref.balls.encode(B1),'2':ref.balls.encode(B2)},
        'rows':[{'entry':key,'value':ref.balls.encode(final[key]),
                 'interval_cubature_core':ref.balls.encode(raw[key]),
                 'source_edge_product_error':ref.balls.encode(tails[key]),
                 'detector_cap_product_error':ref.balls.encode(caps[key])} for key in ('11','22','12')],
        'error_control':'full-cell interval ranges, exact positive cell volumes, separate source edge and detector cap bounds',
        'radius_goal': '1e-3',
        'status':'WITHIN_RADIUS_GOAL' if all(max(z.real.rad(),z.imag.rad())<arb('1e-3') for z in final.values()) else 'ENCLOSED_BUT_SPATIAL_RADIUS_GOAL_NOT_MET',
        'E4_Dirac_detector':'HOLD_NOT_A_SPINOR_REFERENCE','conditional_normalization':'NOT_PERFORMED',
        'gate_status':{'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}}
