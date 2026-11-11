import unittest
import sympy as s
from boundary import *

class BoundaryTests(unittest.TestCase):
    def test_scalar_integrals(self):
        self.assertEqual(scalar_gram(),s.eye(2))

    def test_density_integrals_and_orthogonality(self):
        d=densities()
        self.assertEqual(gram([d[n] for n in ('zero','mixed','double')]),s.eye(3))
        self.assertEqual(gram([d['zero'],d['plus']]),s.eye(2))

    def test_atom_is_not_continuous_endpoint(self):
        r=s.symbols('r', real=True)
        self.assertEqual(s.integrate(s.S.Half,(r,0,1)),s.S.Half)
        self.assertEqual(s.S.Half*s.S.Half,s.Rational(1,4))
        # A Lebesgue endpoint alone has zero mass; the atom must be a distinct term.
        self.assertEqual(s.integrate(1,(r,0,0)),0)

    def test_orbit_weights(self):
        self.assertEqual(WEIGHT[0,0],s.Rational(1,4)/2)
        self.assertEqual(WEIGHT[1,1]+WEIGHT[2,2],s.Rational(1,4))
        self.assertEqual(WEIGHT[3,3],s.Rational(1,4)/2)

    def test_exchange_invariance(self):
        for d in densities().values(): self.assertEqual(SWAP*d,d)
        x,y,u,v,h0,h1,ha=scalar_packets()
        for h in (h0,h1): self.assertEqual(h.subs(y,-y),h)
        self.assertEqual(ha.subs(y,-y),-ha)

    def test_projector_and_discarded_antisymmetric_scalar(self):
        self.assertEqual(PROJECTOR**2,PROJECTOR)
        self.assertEqual(PROJECTOR.T*WEIGHT,WEIGHT*PROJECTOR)
        x,y,u,v,h0,h1,ha=scalar_packets()
        self.assertEqual(s.simplify((ha+ha.subs(y,-y))/2),0)

    def test_mixed_label_duplication_after_projection(self):
        raw=s.sqrt(8)*s.eye(4)
        normed=[]
        for i in range(4):
            a=PROJECTOR*raw[:,i]
            normed.append(a/s.sqrt(gram([a])[0,0]))
        self.assertEqual(normed[1],normed[2])
        self.assertEqual(gram(normed).rank(),3)

    def test_minimal_rank_four(self):
        g=full_gram(['zero','plus'])
        self.assertEqual(g,s.eye(4)); self.assertEqual(g.rank(),4)

    def test_resolved_rank_six(self):
        g=full_gram(['zero','mixed','double'])
        self.assertEqual(g,s.eye(6)); self.assertEqual(g.rank(),6)

    def test_redundant_rank_and_spectrum(self):
        g=full_gram(['zero','mixed','double','plus'])
        self.assertEqual(g.rank(),6)
        self.assertEqual(g.eigenvals(),{s.Integer(0):2,s.Integer(1):4,s.Integer(2):2})

    def test_plus_relation_and_nullvectors(self):
        d=densities()
        self.assertEqual(s.simplify(d['plus']-s.sqrt(s.Rational(2,3))*d['mixed']-d['double']/s.sqrt(3)),s.zeros(4,1))
        g=gram([d[n] for n in ('zero','mixed','double','plus')])
        null=s.Matrix([0,-s.sqrt(s.Rational(2,3)),-1/s.sqrt(3),1])
        self.assertEqual(s.simplify(g*null),s.zeros(4,1))

    def test_omitted_density_direction(self):
        d=densities(); delta=d['mixed']/s.sqrt(3)-s.sqrt(s.Rational(2,3))*d['double']
        self.assertEqual(gram([d['zero'],d['plus'],delta]),s.eye(3))

    def test_plus_is_not_double_only(self):
        d=densities()
        self.assertEqual(gram([d['plus'],d['double']])[0,1],1/s.sqrt(3))

    def test_pure_plus_differs_from_mixture(self):
        pure,mixed=density_mixture()
        self.assertEqual(s.trace(pure),1); self.assertEqual(s.trace(mixed),1)
        self.assertEqual(pure**2,pure)
        self.assertEqual(s.trace(mixed**2),s.Rational(5,9))
        self.assertEqual(pure[1,2],s.sqrt(2)/3)
        self.assertEqual(mixed[1,2],0)

    def test_parity(self):
        x,y,u,v,h0,h1,ha=scalar_packets()
        for n,h in enumerate((h0,h1)):
            self.assertEqual(h.subs({x:-x,y:-y}, simultaneous=True),(-1)**n*h)

    def test_measure_transport(self):
        d=s.Matrix.hstack(*densities().values())
        r=s.symbols('r',positive=True)
        self.assertEqual(s.simplify((d/s.sqrt(r)).T*(r*WEIGHT)*(d/s.sqrt(r))-d.T*WEIGHT*d),s.zeros(4))

    def test_input_output_widths(self):
        self.assertEqual(compare_widths(1,1,1,1),s.eye(2))
        self.assertEqual(compare_widths(1,1,2,1),s.diag(2/s.sqrt(5),8/(5*s.sqrt(5))))
        for bad in (0,-1,s.oo,s.I):
            with self.assertRaises(ValueError): compare_widths(bad,1,1,1)

    def test_width_overlap_independent_integrals(self):
        x=s.symbols('x',real=True)
        h=lambda a:s.exp(-x*x/(2*a*a))/(s.pi*a*a)**s.Rational(1,4)
        ov0=s.integrate(h(1)*h(2),(x,-s.oo,s.oo))
        ov1=s.integrate((s.sqrt(2)*x*h(1))*(s.sqrt(2)*x/2*h(2)),(x,-s.oo,s.oo))
        self.assertEqual(s.simplify(ov0-compare_widths(1,1,2,1)[0,0]),0)
        self.assertEqual(s.simplify(ov1-compare_widths(1,1,2,1)[1,1]),0)

    def test_correlated_exchange_even_state_is_not_exhausted(self):
        a=s.Matrix([0,2,-2,0])
        self.assertEqual(SWAP*a,-a); self.assertEqual(gram([a])[0,0],1)
        for d in densities().values(): self.assertEqual(gram([a,d])[0,1],0)

    def test_density_moment_in_declared_plus_packet(self):
        # Conditional uniform r has mean 1/2. Conditional mask probabilities = 1/3.
        total_means=[0,s.Rational(1,2),s.Rational(1,2),1]
        p=densities()['plus']
        mean=sum(WEIGHT[i,i]*p[i]**2*total_means[i] for i in range(4))
        self.assertEqual(s.simplify(mean),s.Rational(2,3))

if __name__=='__main__': unittest.main()
