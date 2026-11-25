"""Two spherical kinematic completions of a finite clock and density record."""
from fractions import Fraction as Q
from math import comb

R0 = Q(10)
PAST = (0, 1, 2, 3)
FUTURE = (7, 8, 9, 10)
RADIAL_LABEL = tuple(map(Q, (
    '.54', '.53', '.52', '.55', '.25', '.47', '1', '.59', '.60', '.61',
    '.62', '0', '.069', '.35', '.58')))
POSITIONS = tuple(R0 + Q(243, 250) * (a-1) for a in RADIAL_LABEL)
CASES = {'A': 1, 'B': 0}


def smooth(t):
    t = min(Q(1), max(Q(0), t))
    return t**3 * (10 - 15*t + 6*t*t)


def deformation(case, x, target=Q(1,2)):
    return Q(199, 5000)*smooth(x) + Q(161, 625)*smooth(64*(x-target) + CASES[case])


def shape(u):
    return (-65*u**2 + 154*u**4 - 81*u**6)/8


def sphere(d, u):
    """Area in units of 4 pi R0^2."""
    return u*u*(1 - d*shape(u))


def volume(d, u):
    """Volume from the centre in units of 4 pi R0^3."""
    return u**3/3 - d*(-13*u**5 + 22*u**7 - 9*u**9)/8


def regularity():
    # g = f + (u/2) f' in powers of z = u^2.
    coeffs = [Q(0), -Q(65,4), Q(231,4), -Q(81,2)]
    bounds = []
    for j in range(128):
        width = Q(81,64*128)
        left = width*j
        # Translate and rescale the polynomial to [0,1], then use Bernstein bounds.
        power = [sum(c*comb(k,i)*left**(k-i)*width**i
                     for k,c in enumerate(coeffs) if k>=i) for i in range(4)]
        bernstein = [sum(power[i]*Q(comb(k,i),comb(3,i)) for i in range(k+1))
                     for k in range(4)]
        bounds.append(max(bernstein))
    g_upper = max(bounds)
    d_max = deformation('A', Q(1))
    assert d_max == deformation('B', Q(1)) == Q(1487,5000)
    assert g_upper < Q(13,4) and 1-d_max*g_upper > 0
    # Independent rational quadrature, exact for polynomials through degree eight.
    # Nine equally spaced nodes, closed Newton-Cotes weights.
    numerators = [989,5888,-928,10496,-4540,10496,-928,5888,989]
    for n in range(9):
        assert sum(Q(w,28350)*Q(i,8)**n for i,w in enumerate(numerators)) == Q(1,n+1)
    for x in (Q(0),Q(31,64),Q(63,128),Q(1,2),Q(65,128),Q(33,64),Q(1)):
        for case in CASES:
            d = deformation(case,x)
            for a,b in [(Q(0),Q(1)), (Q(31,32),Q(1)), (Q(1),Q(33,32))]:
                integral = (b-a)*sum(Q(w,28350)*sphere(d,a+(b-a)*Q(i,8))
                                     for i,w in enumerate(numerators))
                assert integral == volume(d,b)-volume(d,a)
            assert volume(d,Q(1)) == Q(1,3)
    return {'g_upper':str(g_upper), 'd_max':str(d_max),
            'area_derivative_factor_lower':str(1-d_max*g_upper)}


def conserved_profile(sample_x, sample_w, target=Q(1,2)):
    # Construct one common positive comoving mass density per coordinate volume.
    nodes = []
    for r,x,w in sorted(zip(POSITIONS,sample_x,sample_w)):
        da,db = deformation('A',x,target),deformation('B',x,target)
        assert da==db and w>0
        value = w*(1-da*shape(r/R0))
        assert value>0
        nodes.append((r,value))
    nodes.insert(0,(Q(0),nodes[0][1]))
    def profile(r):
        if r>R0:
            return Q(0)
        for (a,lo),(b,hi) in zip(nodes,nodes[1:]):
            if a<=r<=b:
                return lo+(hi-lo)*smooth((r-a)/(b-a))
        raise ValueError(r)
    for r,x,w in zip(POSITIONS,sample_x,sample_w):
        for case in CASES:
            assert profile(r)/(1-deformation(case,x,target)*shape(r/R0)) == w
    # In either metric the proper mass per dr/(4 pi) is profile(r)*r^2.
    # On each interpolation cell the integrand has degree at most seven.
    weights = (751,3577,1323,2989,2989,1323,3577,751)
    norm = sum(weights)
    for n in range(8):
        assert sum(Q(w,norm)*Q(i,7)**n for i,w in enumerate(weights))==Q(1,n+1)
    mass = Q(0)
    for (a,_),(b,_) in zip(nodes,nodes[1:]):
        for i,weight in enumerate(weights):
            r=a+(b-a)*Q(i,7)
            mass += (b-a)*Q(weight,norm)*profile(r)*r**2
    # Check the conserved proper mass measure in both metrics inside the transition.
    for x in (Q(0),target-Q(1,128),target,target+Q(1,128),Q(1)):
        for case in CASES:
            d=deformation(case,x,target)
            for a,b in zip(nodes,nodes[1:]):
                r=(a[0]+b[0])/2
                density=profile(r)/(1-d*shape(r/R0))
                assert density*R0**2*sphere(d,r/R0)==profile(r)*r**2
    assert mass>0 and profile(R0)>0 and profile(R0+Q(1,1000))==0
    return mass
