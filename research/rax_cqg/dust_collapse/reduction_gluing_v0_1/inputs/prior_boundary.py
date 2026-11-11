"""Explicit finite boundary packet family; no physical CST kernel.

Mask order: 00, 10, 01, 11. Density amplitudes below include sqrt(2)
for the boundary quotient measure (labelled product measure)/|S2|.
The scalar packets use dimensionless Lebesgue dq1 dq2.
"""
import sympy as s

MASKS = ('00', '10', '01', '11')
WEIGHT = s.eye(4)/8
SWAP = s.Matrix([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]])
PROJECTOR = (s.eye(4)+SWAP)/2
GATES = {k:'HOLD' for k in ('MODEL','CURRENT','CORRESPONDENCE','BOUNCE',
                           'REGULARITY','BOUNDARY','TRAPPING','EXTENSION')}

def densities():
    z=s.zeros(4,1); z[0]=s.sqrt(8)
    m=s.Matrix([0,2,2,0])
    d=s.Matrix([0,0,0,s.sqrt(8)])
    p=s.Matrix([0,s.sqrt(s.Rational(8,3)),s.sqrt(s.Rational(8,3)),s.sqrt(s.Rational(8,3))])
    return {'zero':z, 'mixed':m, 'double':d, 'plus':p}

def gram(columns):
    a=s.Matrix.hstack(*columns)
    return s.simplify(a.conjugate().T*WEIGHT*a)

def scalar_packets():
    x,y=s.symbols('q_s q_a', real=True)
    u,v=s.symbols('sigma_s sigma_a', positive=True)
    h=s.exp(-(x*x/u**2+y*y/v**2)/2)/s.sqrt(s.pi*u*v)
    return (x,y,u,v,h,s.sqrt(2)*x/u*h,s.sqrt(2)*y/v*h)

def scalar_gram():
    x,y,u,v,h0,h1,_=scalar_packets()
    return s.Matrix(2,2,lambda i,j:s.simplify(s.integrate(
        s.integrate((h0,h1)[i]*(h0,h1)[j],(x,-s.oo,s.oo)),(y,-s.oo,s.oo))))

def full_gram(names):
    d=densities()
    return s.kronecker_product(gram([d[n] for n in names]),s.eye(2))

def compare_widths(sin,ain,sout,aout):
    values=[s.sympify(t) for t in (sin,ain,sout,aout)]
    if not all(t.is_positive is True and t.is_finite is True for t in values):
        raise ValueError('All dimensionless packet widths must be positive and finite')
    si,ai,so,ao=values
    r=2*si*so/(si**2+so**2)
    t=2*ai*ao/(ai**2+ao**2)
    return s.diag(s.sqrt(r*t),r*s.sqrt(r*t))

def density_mixture():
    d=densities()
    # In orthonormal resolved coordinates: zero, mixed, double.
    plus=s.Matrix([0,s.sqrt(s.Rational(2,3)),1/s.sqrt(3)])
    pure=plus*plus.T
    mixture=s.diag(0,s.Rational(2,3),s.Rational(1,3))
    return pure,mixture

def encode_matrix(a):
    return [[str(s.simplify(a[i,j])) for j in range(a.cols)] for i in range(a.rows)]

def evidence():
    matrices={}
    for name,labels in [('minimal',['zero','plus']),('resolved',['zero','mixed','double']),
                        ('redundant',['zero','mixed','double','plus'])]:
        a=full_gram(labels)
        matrices[name]={'order':[f'A|{l}|{n}m' for l in labels for n in (0,1)],
                        'gram':encode_matrix(a),'rank':a.rank(),
                        'eigenvalues':{str(k):v for k,v in a.eigenvals().items()}}
    return {'scope':'DECLARED_KINEMATIC_BOUNDARY_PACKETS_ONLY',
            'mask_order':list(MASKS),'quotient_mask_weights':['1/8']*4,
            'scalar_gram':encode_matrix(scalar_gram()),'families':matrices,
            'Hilbert_space_dimension':'infinite',
            'physical_inner_product':'NOT_DERIVED','physical_kernel':'NOT_CONSTRUCTED',
            'physical_K_0plus':'NOT_COMPUTED','physical_gates':GATES}
