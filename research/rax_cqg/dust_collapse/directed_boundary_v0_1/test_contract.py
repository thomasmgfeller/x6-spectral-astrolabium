"""Independent finite and analytic controls, not physical qualification."""
import unittest
from itertools import product
from fractions import Fraction
import json
import math
import numpy as np
import sympy as s
from numpy.polynomial.hermite import hermgauss
from analyze import g, carrier, boundary_group, admissible, summarize, ROOT
from gaussian import project, regulated_project, continuous_sqrt_det

class DirectedCarrierTests(unittest.TestCase):
    def test_full_unrestricted_enumeration(self):
        universe = g.all_posets(5)
        self.assertEqual(len(universe), 4231)
        for x, y, covered in product('AK', 'AK', (False, True)):
            self.assertEqual(carrier(x,y,covered), [c for c in universe if admissible(c,x,y,covered)])

    def test_counts(self):
        for flag, wanted in [(False,[49,23,23,12]),(True,[33,14,14,7])]:
            self.assertEqual([len(carrier(x,y,flag)) for x,y in product('AK',repeat=2)],wanted)

    def test_no_back_relations_and_convex_collars(self):
        for x,y in product('AK',repeat=2):
            for code in carrier(x,y):
                edges=set(g.pairs(code,5))
                self.assertFalse(any(a>=2 and b<2 for a,b in edges))
                self.assertFalse(any(a>=3 and b<3 for a,b in edges))
                for collar in [{0,1},{3,4}]:
                    self.assertFalse(any(a in collar and b in collar and k not in collar
                                         for a,b in edges for k in range(5)
                                         if (a,k) in edges and (k,b) in edges))

    def test_antichain_extrema(self):
        for code in carrier('A','A',True):
            rel=set(g.pairs(code,5))
            self.assertEqual({i for i in range(5) if not any(j==i for _,j in rel)},{0,1})
            self.assertEqual({i for i in range(5) if not any(j==i for j,_ in rel)},{3,4})

    def test_chain_is_not_a_slice(self):
        for code in carrier('K','K',True):
            self.assertIn((0,1), g.pairs(code,5))
            self.assertIn((3,4), g.pairs(code,5))

    def test_orbit_stabilizers_and_action_invariance(self):
        for x,y,covered in product('AK','AK',(False,True)):
            rec=summarize(x,y,covered); group=boundary_group(x,y)
            self.assertEqual(Fraction(rec['orbit_weight_sum']),Fraction(rec['count'],len(group)))
            for orbit in rec['orbits']:
                self.assertEqual(len(orbit['members'])*orbit['stabilizer'],len(group))
                self.assertEqual(len({g.action(c,5) for c in orbit['members']}),1)

    def test_orientation_reversal_bijection(self):
        perm=(4,3,2,1,0)
        for x,y,covered in product('AK','AK',(False,True)):
            dual={g.encode([(perm[b],perm[a]) for a,b in g.pairs(c,5)],5) for c in carrier(x,y,covered)}
            self.assertEqual(dual,set(carrier(y,x,covered)))
        # This test concerns combinatorics only, not adjointness of matter amplitudes.

    def test_aa_combinatorial_formula(self):
        # Nonempty P,Q; their product is forced, remaining A-A edges arbitrary.
        total=sum(math.comb(2,p)*math.comb(2,q)*2**(4-p*q) for p in (1,2) for q in (1,2))
        self.assertEqual(total,49)
        # Covered: (p,q)=(1,1): five patterns per P,Q, other cases 3,3,1.
        self.assertEqual(4*5+2*3+2*3+1,33)
        breakdown={}
        for c in carrier('A','A',True):
            rel=set(g.pairs(c,5))
            key=(sum((i,2) in rel for i in (0,1)),sum((2,j) in rel for j in (3,4)))
            breakdown[key]=breakdown.get(key,0)+1
        self.assertEqual(breakdown,{(1,1):20,(1,2):6,(2,1):6,(2,2):1})

class GaussianTests(unittest.TestCase):
    def test_weighted_profile_basis_is_not_fock_transition(self):
        W=s.diag(2,3); L=s.diag(2,6)
        V=s.diag(1/s.sqrt(2),1/s.sqrt(3))
        lam=s.diag(1,2)
        self.assertEqual(V.T*W*V,s.eye(2))
        self.assertEqual(L*V,W*V*lam)
        self.assertEqual(V.T*L*V,lam)
        rotation=s.Matrix([[1,-1],[1,1]])/s.sqrt(2)
        reference=V*rotation
        self.assertEqual(s.simplify(reference.T*L*reference),s.Matrix([[s.Rational(3,2),s.Rational(1,2)],[s.Rational(1,2),s.Rational(3,2)]]))

    def test_retarded_matrix_is_not_action_hessian(self):
        x,y=s.symbols('x y',real=True); phi=s.Matrix([x,y])
        D=s.Matrix([[1,0],[2,3]])
        action=(phi.T*D*phi)[0]/2
        grad=s.Matrix([s.diff(action,x),s.diff(action,y)])
        self.assertEqual(grad,(D+D.T)*phi/2)
        self.assertNotEqual(grad,D*phi)

    def test_schur_stationary_identity_exact(self):
        B=s.Matrix([[2,1],[1,3]]); J=s.Matrix([[1,-2]]); A=s.Matrix([[-3]])
        x,y=s.symbols('x y',real=True); b=s.Matrix([x,y]); q=-A.inv()*J*b
        E=B-J.T*A.inv()*J
        self.assertEqual(s.expand((b.T*B*b+2*q.T*J*b+q.T*A*q-b.T*E*b)[0]),0)

    def test_gaussian_moment_source_derivatives(self):
        t,u,c11,c12,c22,h=s.symbols('t u c11 c12 c22 h')
        Z=s.exp(h*(c11*t*t+2*c12*t*u+c22*u*u)/2)
        self.assertEqual(s.diff(Z,t).subs({t:0,u:0}),0)
        self.assertEqual(s.diff(Z,t,u).subs({t:0,u:0}),h*c12)
        self.assertEqual(s.diff(Z,u,2).subs({t:0,u:0}),h*c22)

    def test_packet_orthonormality(self):
        x=s.symbols('x',real=True)
        ps=[s.pi**(-s.Rational(1,4))*s.exp(-x*x/2),
            s.sqrt(2)*x*s.pi**(-s.Rational(1,4))*s.exp(-x*x/2),
            (2*x*x-1)/s.sqrt(2)*s.pi**(-s.Rational(1,4))*s.exp(-x*x/2)]
        for i,j in product(range(3),repeat=2):
            self.assertEqual(s.integrate(ps[i]*ps[j],(x,-s.oo,s.oo)),int(i==j))

    def test_schur_boundary_quadrature(self):
        H=np.array([[.2,.1,.3],[.1,-.15,-.2],[.3,-.2,-1.5]])
        out=project(H,[[1.2]],[[.8]])
        nodes,w=hermgauss(64)
        x,y=np.meshgrid(nodes*np.sqrt(2/1.2),nodes*np.sqrt(2/.8),indexing='ij')
        E=out['E']; phase=np.exp(.5j*(E[0,0]*x*x+2*E[0,1]*x*y+E[1,1]*y*y))
        weight=w[:,None]*w[None,:]
        norm=(1.2*.8)**.25/np.sqrt(np.pi)
        fresnel=np.sqrt(2*np.pi/1.5)*np.exp(-1j*np.pi/4)
        pref=norm*fresnel*2/np.sqrt(1.2*.8)
        self.assertLess(abs(pref*np.sum(weight*phase)-out['B00']),1e-11)
        self.assertLess(abs(pref*np.sum(weight*phase*2*np.sqrt(1.2*.8)*x*y)-out['B11']),1e-11)
        self.assertLess(abs(pref*np.sum(weight*phase*(2*.8*y*y-1)/np.sqrt(2))-out['B20']),1e-11)

    def test_full_regulated_quadrature(self):
        H=np.array([[.2,.1,.1],[.1,-.15,-.12],[.1,-.12,.15]])
        epsilon=.8
        out=regulated_project(H,[[1.2]],[[.8]],epsilon)
        nodes,w=hermgauss(32)
        a,b,c=np.meshgrid(nodes*np.sqrt(2/1.2),nodes*np.sqrt(2/.8),nodes*np.sqrt(2/epsilon),indexing='ij')
        phase=np.exp(.5j*(H[0,0]*a*a+H[1,1]*b*b+H[2,2]*c*c+2*H[0,1]*a*b+2*H[0,2]*a*c+2*H[1,2]*b*c))
        value=np.sum(w[:,None,None]*w[None,:,None]*w[None,None,:]*phase)
        value *= (1.2*.8)**.25/np.sqrt(np.pi)*np.sqrt(8/(1.2*.8*epsilon))
        self.assertLess(abs(value-out['B00']),1e-11)

    def test_schur_abel_limit(self):
        H=np.array([[.2,.1,.3],[.1,-.15,-.2],[.3,-.2,-1.5]])
        exact=project(H,[[1.2]],[[.8]])['B00']
        errors=[abs(regulated_project(H,[[1.2]],[[.8]],e)['B00']-exact) for e in (.01,.001,.0001)]
        self.assertTrue(errors[2]<errors[1]<errors[0])
        self.assertLess(errors[2],.001)

    def test_singular_coupled_finite_exact(self):
        e=s.symbols('e',positive=True)
        H=s.Matrix([[0,0,1],[0,0,0],[1,0,0]])
        Q=s.diag(1,1,e)-s.I*H
        self.assertEqual(Q.det(),1+e)
        self.assertEqual(Q.subs(e,0).det(),1)
        # Independent distribution evaluation: integral dq exp(i q x)=2 pi delta(x).
        y=s.symbols('y',real=True)
        direct=2*s.pi/s.sqrt(s.pi)*s.integrate(s.exp(-y*y/2),(y,-s.oo,s.oo))
        self.assertEqual(s.simplify(direct-2*s.sqrt(2)*s.pi),0)
        self.assertAlmostEqual(abs(regulated_project(np.array(H).astype(float),[[1]],[[1]],.25)['B00']),float(2*s.sqrt(2)*s.pi/s.sqrt(s.Rational(5,4))),places=11)

    def test_invisible_interior_null_diverges(self):
        e=s.symbols('e',positive=True)
        self.assertEqual(s.diag(1,1,e).det(),e)
        self.assertEqual(s.limit(1/s.sqrt(e),e,0,dir='+'),s.oo)

    def test_joint_kernel_rank_criterion_examples(self):
        for A,J in [(s.zeros(1),s.Matrix([[1,0]])),(s.zeros(1),s.zeros(1,2)),
                    (s.diag(1,0),s.Matrix([[1,0],[0,1]])),(s.diag(1,0),s.Matrix([[1,0],[0,0]]))]:
            H=s.zeros(2+A.rows); H[2:,2:]=A; H[2:,:2]=J; H[:2,2:]=J.T
            Q=s.diag(1,1,*([0]*A.rows))-s.I*H
            stacked=A.col_join(J.T)
            self.assertEqual(Q.det()!=0,stacked.rank()==A.rows)

    def test_determinant_branch_counterexample(self):
        continued=continuous_sqrt_det(np.eye(4),2*np.eye(4))
        naive=np.sqrt(np.linalg.det((1-2j)*np.eye(4)))
        self.assertLess(abs(continued-(-3-4j)),1e-12)
        self.assertLess(abs(naive-(3+4j)),1e-12)

    def test_invalid_inputs_and_singular_schur_rejected(self):
        cases=[lambda:project([[1,2],[0,1]],[[1]],[[1]]),
               lambda:project(np.eye(2),[[-1]],[[1]]),
               lambda:project(np.zeros((3,3)),[[1]],[[1]]),
               lambda:regulated_project(np.eye(2),[[1]],[[1]],0),
               lambda:project(np.eye(2),[[1]],[[1]],hbar=0)]
        for f in cases:
            with self.assertRaises(ValueError): f()

class StratumTests(unittest.TestCase):
    def test_normalized_atom_and_positive_packets(self):
        # Each support has nu measure 1/2. Both normalized constants are sqrt(2).
        self.assertEqual(Fraction(1,2)*2,1)
        # wf=0,wi>0: sqrt(2)*sqrt(2)*(1/2)*(1/2) = 1/2.
        self.assertEqual(Fraction(1,2)**2*2,Fraction(1,2))

    def test_atom_extension_not_fixed_by_bulk(self):
        w,c=s.symbols('w c',real=True)
        # Addition c 1_atom(wf)1_plus(wi) shifts normalized B_0+ by c/2.
        self.assertEqual(s.integrate(c/2,(w,0,1)),c/2)
        # A vanishing density weight on the atom kills this factor only, not its neighbours.
        self.assertEqual((w*c).subs(w,0),0)

    def test_physical_unknowns_remain_unknown(self):
        inputs=json.loads((ROOT/'physical_inputs.json').read_text())
        self.assertIsNone(inputs['numerical_physical_entries'])
        self.assertEqual(set(inputs['physical_gates'].values()),{'HOLD'})
        self.assertTrue(all(v is None for v in inputs['required_physical_inputs'].values()))

class BasisProjectionTests(unittest.TestCase):
    def test_complete_index_map_and_boundary_orientation(self):
        contract=json.loads((ROOT/'basis_contract.json').read_text())
        geo=contract['geometry_major_order']; old=contract['preserved_order']
        p=contract['preserved_order_indices_in_geometry_major_zero_based']
        self.assertEqual(old,json.loads((ROOT/'physical_inputs.json').read_text())['preserved_planning_basis'])
        self.assertEqual([geo[i] for i in p],old)
        P=s.zeros(8)
        for row,col in enumerate(p): P[row,col]=1
        self.assertEqual(P*P.T,s.eye(8))
        # Distinct labelled entries catch swaps hidden by symmetric counting data.
        entries={(a,b):s.Symbol(f'entry_{i}_{j}') for i,a in enumerate(geo) for j,b in enumerate(geo)}
        original=s.Matrix(8,8,lambda i,j:entries[(geo[i],geo[j])])
        expected=s.Matrix(8,8,lambda i,j:entries[(old[i],old[j])])
        self.assertEqual(P*original*P.T,expected)
        self.assertEqual(P.T*expected*P,original)
        for matrix_label,carrier_label in contract['matrix_block_to_carrier_label'].items():
            self.assertEqual(carrier_label,matrix_label[::-1])

    def test_conditional_parity_blocks_preserve_stratum_mixing(self):
        labels=json.loads((ROOT/'basis_contract.json').read_text())['geometry_major_order']
        parity=[1 if x.endswith('0m') else -1 for x in labels]
        D=s.diag(*parity)
        M=s.Matrix(8,8,lambda i,j:s.Symbol(f'allowed_{i}_{j}') if parity[i]==parity[j] else 0)
        self.assertEqual(D*M-M*D,s.zeros(8))
        p=[0,2,4,6,1,3,5,7]
        regrouped=M.extract(p,p)
        self.assertEqual(regrouped[:4,4:],s.zeros(4))
        self.assertEqual(regrouped[4:,:4],s.zeros(4))
        self.assertNotEqual(M[0,2],0)  # even, same geometry, different stratum
        self.assertNotEqual(M[1,3],0)  # odd, same geometry, different stratum

    def test_parity_preserving_unitary_can_leave_two_occupations(self):
        # Exact abstract control on |0>,|1>,|2>, not a CST dynamics proposal.
        U=s.Matrix([[s.Rational(3,5),0,-s.Rational(4,5)],
                    [0,1,0],[s.Rational(4,5),0,s.Rational(3,5)]])
        V=s.Matrix([[1,0],[0,1],[0,0]])
        D=s.diag(1,-1,1); P=V*V.T
        K=V.T*U*V; leakage=(s.eye(3)-P)*U*V
        self.assertEqual(U.T*U,s.eye(3))
        self.assertEqual(D*U-U*D,s.zeros(3))
        self.assertEqual(s.eye(2)-K.T*K,leakage.T*leakage)
        self.assertEqual(leakage.T*leakage,s.diag(s.Rational(16,25),0))
        self.assertNotEqual(K.T*K,s.eye(2))

if __name__=='__main__': unittest.main()
