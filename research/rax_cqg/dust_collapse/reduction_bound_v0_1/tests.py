"""Independent checks of analytic moments, Gaussian phases and stop decisions."""
import json,math,subprocess,sys,unittest
from functools import lru_cache
from itertools import product
from pathlib import Path
import numpy as np
import sympy as s
from flint import arb,ctx
import bounds as b
import basis

ROOT=Path(__file__).resolve().parent
ctx.prec=192

@lru_cache(None)
def radial_cartesian(a,c,k):
    if a%2 or c%2:return s.Rational(0)
    a//=2;c//=2
    return s.Rational(3*math.factorial(2*a)*math.factorial(2*c),4**(a+c)*math.factorial(a)*math.factorial(c))*s.gamma(3+k-a-c)/s.gamma(4+k)

def independent_field_integral(D0,E0):
    x=s.Matrix(s.symbols('x0:2'));y=s.Matrix(s.symbols('y0:2'))
    D=b.BETA*D0;E=b.BETA*E0;p=D*y+E*x
    r=(y.T*y)[0];a=r+(p.T*p)[0];v=(y.T*p)[0];tr=D.trace()
    numerators={0:a*a+tr*tr,1:-16*tr*v,2:2*a*(8-16*r)+64*v*v,4:(8-16*r)**2}
    answer=0
    for k,polynomial in numerators.items():
        for powers,coefficient in s.Poly(s.expand(polynomial),*x,*y).terms():
            answer+=coefficient*radial_cartesian(*powers[:2],0)*radial_cartesian(*powers[2:],k)
    return s.simplify(answer)

@lru_cache(None)
def clock_tensor(count):
    nodes,weights=np.polynomial.legendre.leggauss(5)
    choices=np.array(list(product(range(5),repeat=count)),dtype=int)
    return nodes[choices],np.prod((weights/2)[choices],axis=1)

@lru_cache(None)
def density_tensor(count):
    nodes,weights=np.polynomial.legendre.leggauss(3)
    nodes=np.r_[0,(nodes+1)/2];weights=np.r_[.5,weights/4]
    choices=np.array(list(product(range(4),repeat=count)),dtype=int)
    return nodes[choices],np.prod(weights[choices],axis=1)

def clock_cubature(terms,j):
    incident=[(i,k,c) for i,k,c in terms if j in (i,k)]
    vertices=sorted({j}|{i for i,k,c in incident}|{k for i,k,c in incident})
    later=sorted({k for i,k,c in incident});ts,tw=clock_tensor(len(vertices));rs,rw=density_tensor(len(later))
    pos={k:i for i,k in enumerate(vertices)};rpos={k:i for i,k in enumerate(later)}
    t=ts[:,pos[j]];A=np.zeros((len(ts),len(rs)));B=np.zeros(len(rs))
    beta=4/math.sqrt(6)
    for i,k,c in incident:
        other=k if i==j else i
        A-=beta*c/2*(t-ts[:,pos[other]])[:,None]*rs[:,rpos[k]][None,:]
        B-=beta*c/2*rs[:,rpos[k]]
    value=(1-t[:,None]**2)**2*A**4+(2*t[:,None]*A-(1-t[:,None]**2)*B[None,:])**2
    return float(tw@value@rw)

class CertificateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows=json.loads((ROOT/'results/geometry_constants.json').read_text());cls.c=b.constants(cls.rows)
    def test_01_all_field_moments_independent_cartesian_integral(self):
        for row in self.rows:
            k=b.schur(row['code'])
            for side,D,E in [('in',k[:2,:2],k[:2,2:]),('out',k[2:,2:],k[2:,:2])]:
                self.assertEqual(s.simplify(independent_field_integral(D,E)-s.sympify(row['field_energy_'+side])),0)
    def test_02_all_clock_moments_independent_degree_exact_cubature(self):
        # Every clock degree <=8, every density degree <=4: 5 and 3 GL nodes.
        # Floating cubature is an independent regression, not the certified bound.
        for row in self.rows:
            terms=b.pc.pair_coefficients(row['code'])
            for j in (0,1,3,4):
                expected=float(s.sympify(row['clock_energy'][str(j)]))
                self.assertAlmostEqual(clock_cubature(terms,j),expected,delta=2e-11*max(1,expected))
    def test_03_density_derivative_norm_with_separate_atom(self):
        r,k=s.symbols('r k',real=True)
        integrated=s.integrate((k*k*(1-2*r)**2+k**4*r*r*(1-r)**2)/2,(r,0,1))
        self.assertEqual(s.expand(integrated-k*k/6-k**4/60),0)
        self.assertEqual(b.density_moment(()),s.Rational(41,960))
        self.assertEqual(b.density_moment((),s.Rational(0)),0)
    def test_04_original_four_and_previous_modes_retained(self):
        for n,norm in [(0,65),(1,261)]:
            embedded=basis.original_field_embedding(n)
            self.assertEqual(embedded['V_norm_squared'],norm)
            self.assertTrue(all(x['na']%2==0 for x in embedded['coefficients']))
        modes=basis.labels(6,0,2)
        self.assertEqual(len(modes),516)
        self.assertTrue(any(x['swap_relative_sign']==-1 for x in modes))
        self.assertTrue(all(x['swapped_partner'] or x['field'][1]%2==0 for x in modes))
        with self.assertRaises(ValueError):basis.labels(10000,0,2)
        # Prior field-degree <=2 times U's degree-4 polynomial fits N=6;
        # degree-2 clocks and density masks lie in T=2,D=0.
        for ns,na in [(0,0),(1,0),(2,0),(0,2),(0,1),(1,1)]:
            p=s.Poly((1+basis.X**2+basis.Y**2)**2*basis.hermite_polynomial(ns,na),basis.X,basis.Y)
            self.assertLessEqual(p.total_degree(),6)
    def test_05_initial_density_factor_is_exact_for_every_history(self):
        for code in b.pc.histories():
            self.assertTrue(all(j not in (0,1) for i,j,c in b.pc.pair_coefficients(code)))
        for left in b.pc.histories():
            for right in b.pc.histories():
                rel=b.ps.transitive_closure(range(8),b.pc.relations(left)|{(i+3,j+3) for i,j in b.pc.relations(right)})
                self.assertTrue(all(j not in (0,1) for i,j in rel))
        self.assertTrue(self.c['zeta_abs']>1)
        self.assertTrue(self.c['forward']['density'][0]>self.c['backward']['density'][0])
    def test_06_enclosures_and_monotone_whole_tails(self):
        for direction in ('forward','backward'):
            c=self.c[direction];base=b.tail_constant(c,6,0,2)
            for cut in [(7,0,2),(6,1,2),(6,0,3)]:self.assertTrue(b.tail_constant(c,*cut)<base)
        certificate=json.loads((ROOT/'results/reduction_certificate.json').read_text())
        self.assertTrue(arb(certificate['single_step']['full_C_M_class_error'])<arb('1/100'))
        self.assertTrue(arb(certificate['composition']['total_class_bound_before_numerics'])<arb('1/100'))
        self.assertEqual(certificate['single_step_resource_decision'],'HOLD')
        self.assertEqual(certificate['composition_resource_decision'],'HOLD')
    def test_07_gaussian_branch_and_odd_moments_independent_numpy(self):
        cases=[(b.pc.histories()[i],b.pc.histories()[j]) for i,j in [(0,0),(0,32),(16,16),(32,32)]]
        epsilon=.25
        for l,r in cases:
            h,_=b.joint_data(l,r);matrix=np.array(h.tolist(),dtype=float)*(4/math.sqrt(6))
            diag=np.array([1,1,epsilon,epsilon,epsilon,epsilon,1,1])
            scaled=matrix/np.sqrt(diag[:,None]*diag[None,:])
            eigen=np.linalg.eigvalsh(scaled)
            # Accretive Gaussian branch: product of roots of 1-i*real eigenvalues.
            exact=16*math.pi**3/(np.sqrt(np.prod(diag))*np.prod(np.sqrt(1-1j*eigen)))
            inv=np.linalg.inv(np.diag(diag)-1j*matrix)
            odd=exact*sum(inv[i,j] for i in (0,1) for j in (6,7))
            value=b.scalar_pair(h,'1/4')
            for got,expected in zip(value,[exact,odd]):
                z=complex(float(got.real.mid()),float(got.imag.mid()))
                self.assertAlmostEqual(abs(z-expected),0,delta=2e-10*max(1,abs(expected)))
    def test_08_both_conditional_tails_are_needed(self):
        a=np.array([1.,2.]);bb=np.array([3.,5.]);projected=a[0]*bb[0]
        self.assertEqual(float(bb@a)-projected,10.)
        self.assertEqual(np.linalg.norm(a[1:])*np.linalg.norm(bb[1:]),10.)
        self.assertEqual(b.dimension(6,0,2,False),1008)
        self.assertGreater(b.dimension(6,0,2,False),b.dimension(6,0,2))
    def test_09_stop_rule_includes_numerics_and_mode_cap(self):
        def check(*args):
            r=subprocess.run([sys.executable,'-B',str(ROOT/'check_budget.py'),*args],check=True,capture_output=True,text=True)
            return json.loads(r.stdout)
        small=check('--field','6','--density','0','--clock','2')
        self.assertEqual(small['decision'],'EXTEND_BASIS')
        big=['--field','151306','--density','124','--clock','192']
        self.assertEqual(check(*big)['decision'],'HOLD_RESOURCE_CAP')
        cap=['--mode-cap','4000000000000000000']
        self.assertEqual(check(*big,*cap)['decision'],'TOLERANCE_PASS')
        self.assertEqual(check(*big,*cap,'--numerical-error','1/50')['decision'],'EXTEND_BASIS')
    def test_10_weighted_gram_independent_radial_moments(self):
        r=s.symbols('r',nonnegative=True)
        self.assertEqual(s.integrate(s.exp(-r)*(1+r)**4,(r,0,s.oo)),65)
        self.assertEqual(s.integrate(r*s.exp(-r)*(1+r)**4,(r,0,s.oo)),261)

if __name__=='__main__':unittest.main(verbosity=2)
