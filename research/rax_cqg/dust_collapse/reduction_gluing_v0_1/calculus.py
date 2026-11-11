"""Finite-dimensional Gaussian projections with explicit Fresnel branches."""
from pathlib import Path
import sympy as s
from flint import arb,acb,acb_mat
from inputs import prior_core as pc

ROOT=Path(__file__).resolve().parent

def rational_matrix(h):return s.Matrix([[s.Rational(str(v)) for v in row] for row in h])
def ball(v):return arb(str(v))

def gaussian_data(h,interior=(2,),boundary=(0,1,3,4),sigma_s=1,sigma_a=1):
 h=rational_matrix(h) if not isinstance(h,s.MatrixBase) else h
 if len(boundary)!=4 or not interior or set(interior)&set(boundary):raise ValueError('two points at each outer boundary and disjoint interior required')
 if sorted(list(interior)+list(boundary))!=list(range(h.rows)):raise ValueError('indices must partition the matrix')
 si=ball(sigma_s);ai=ball(sigma_a)
 if not si>0 or not ai>0:raise ValueError('positive packet widths required')
 inner=h.extract(interior,interior)
 if inner.det()==0:raise ValueError('singular interior block requires a different domain analysis')
 _,ld=inner.LDLdecomposition(hermitian=False)
 signs=[s.sign(ld[i,i]) for i in range(ld.rows)]
 if not all(v in (-1,1) for v in signs):raise ValueError('zero or unresolved exact LDL pivot')
 signature=sum(signs)
 schur=h.extract(boundary,boundary)-h.extract(boundary,interior)*inner.inv()*h.extract(interior,boundary)
 b=pc.beta();g=[[arb(int(i==j)) for j in range(4)] for i in range(4)]
 g[2][2]=g[3][3]=(1/(si*si)+1/(ai*ai))/2
 g[2][3]=g[3][2]=(1/(si*si)-1/(ai*ai))/2
 q=acb_mat([[acb(g[i][j],-b*ball(schur[i,j])) for j in range(4)] for i in range(4)])
 cov=q.inv();work=[[q[i,j] for j in range(4)] for i in range(4)];root=acb(1);pivots=[]
 for k in range(4):
  pivot=work[k][k]
  if not pivot.real>0:raise ArithmeticError('boundary Gaussian pivot not in right half-plane')
  pivots.append(pivot);root*=pivot.sqrt(analytic=True)
  for i in range(k+1,4):
   for j in range(k+1,4):work[i][j]-=work[i][k]*work[k][j]/pivot
 m=len(interior)
 pref=4*arb.pi()/(si*ai).sqrt()*(2*arb.pi()/b)**(arb(m)/2)/ball(abs(inner.det())).sqrt()
 amplitude=pref*acb(0,arb.pi()*int(signature)/4).exp()/root
 if not amplitude.is_finite():raise ArithmeticError('nonfinite Gaussian projection')
 return amplitude,cov,{'interior_determinant_h0':str(inner.det()),'signature':int(signature),
                      'ldl_pivots':[str(ld[i,i]) for i in range(m)],
                      'schur_h0':[[str(schur[i,j]) for j in range(4)] for i in range(4)],
                      'boundary_pivots':[pc.pack(p) for p in pivots]}

def scalar_factors(h):
 a,v,data=gaussian_data(h)
 return {'00':a,'10':acb(0),'01':acb(0),
         '20':a*(v[2,2]+2*v[2,3]+v[3,3]-1)/arb(2).sqrt(),
         '02':a*(v[2,2]-2*v[2,3]+v[3,3]-1)/arb(2).sqrt(),
         '11':a*(v[2,2]-v[3,3])},data

def summarize(raw,error):
 if not raw.is_finite() or not error.is_finite() or error<0:raise ArithmeticError('nonfinite amplitude or invalid error')
 z=pc.widen(raw,error)
 return {'quadrature_ball':pc.pack(raw),'analytic_quadrature_error_bound':error.str(25,more=True),
         'arithmetic_complex_radius_bound':(raw.real.rad()*raw.real.rad()+raw.imag.rad()*raw.imag.rad()).sqrt().str(25,more=True),
         'certified_ball':pc.pack(z),'absolute_value':abs(z).str(25,more=True),
         'classification':'EXACT_PARITY_ZERO' if raw.is_zero() and error.is_zero() else ('NONZERO' if z.abs_lower()>0 else 'UNRESOLVED')}

def norm_ball(records):
 total=arb(0)
 for r in records:
  a=abs(pc.unpack(r['certified_ball']));total+=a*a
 return total.sqrt()
