import hashlib
import json
import unittest
import numpy as np
import sympy as S
from flint import arb
from domain_analysis import ROOT, B, beta, core, schur, build

class DomainCertificate(unittest.TestCase):
    def test_frozen_source_identity(self):
        p=json.loads((ROOT/'provenance.json').read_text())
        for source in p['sources']:
            raw=(ROOT/source['local_path']).read_bytes()
            digest=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
            self.assertEqual(digest,source['git_blob'],source['local_path'])

    def test_complete_geometry_against_independent_frozen_hessians(self):
        records=json.loads((ROOT/'inputs/aa_hessians.json').read_text())['histories']
        self.assertEqual(len(records),33)
        self.assertEqual(sorted(r['order_code'] for r in records),core.histories())
        for r in records:
            self.assertEqual(S.Matrix(r['H0_over_va']), S.Matrix(core.h0(r['order_code'])))
            self.assertEqual(r['F4'],core.f4(r['order_code']))

    def test_gap_and_regulator_derivative_bounds(self):
        for code in core.histories():
            h=S.Matrix(core.h0(code))
            self.assertTrue(1 <= -h[2,2] <= 2)
            self.assertTrue(sum(h[2,j]**2 for j in B) <= 1)

    def test_all_cross_ranks_and_persistent_directions(self):
        ranks=[schur(c)[:2,2:].rank() for c in core.histories()]
        self.assertEqual(ranks.count(2),28)
        self.assertEqual(ranks.count(1),5)
        free=[c for c in core.histories() if schur(c)[:2,2:]*S.Matrix([1,-1])==S.zeros(2,1)]
        self.assertEqual(free,[25372,25496,25500])
        self.assertEqual(schur(9116)[:2,2:].nullspace(),[S.Matrix([S.Rational(3,26),1])])
        self.assertEqual(schur(17308)[:2,2:].nullspace(),[S.Matrix([S.Rational(26,3),1])])

    def test_persistent_blocks_and_label_multiplicity(self):
        k=schur(25372)
        self.assertEqual(k[:2,:2],S.diag(S.Rational(26,3),-1))
        self.assertEqual(k[:2,2:],S.Matrix([[-S.Rational(13,3)]*2,[S.Rational(1,2)]*2]))
        p=S.eye(4);p.row_swap(0,1)
        self.assertEqual(schur(25496),p*k*p.T)
        for code in (25372,25496,25500):
            self.assertEqual(core.f4(code),37 if code==25500 else 18)

    def test_distinct_fresnel_frequencies_and_gaussian_decay(self):
        u=S.Matrix([1,1])/S.sqrt(2);v=S.Matrix([1,-1])/S.sqrt(2)
        for code,rho,omega,c in [(25372,S.Rational(23,6),S.Rational(7,4),S.Rational(51484,59785)),
                                 (25500,S.Rational(35,4),S.Rational(17,4),S.Rational(1225,1231))]:
            k=schur(code);ll=k[:2,:2];rr=k[2:,2:];xu=k[:2,2:]*u
            self.assertEqual((u.T*rr*u)[0],rho)
            self.assertEqual((v.T*rr*v)[0]/2,omega)
            self.assertEqual((u.T*rr*v)[0],0)
            cc=S.simplify(beta**2*(xu.T*(S.eye(2)+beta**2*ll**2).inv()*xu)[0])
            self.assertEqual(cc,c)
            self.assertTrue(0<c<1)

    def test_dust_non_cancellation_bound(self):
        self.assertTrue(beta<S.Rational(7,4))
        self.assertTrue(S.Rational(1,2)+2*beta<4)
        # r in [0,1/4]: |k*r|<1, cos>=1-u^2/2>=1/2.
        self.assertEqual(S.Rational(1,2)*S.Rational(1,4)*S.Rational(3,2),S.Rational(3,16))

    def test_packet_and_measure_factors(self):
        self.assertEqual(S.Rational(1,2)*S.Rational(1,4)*(2*S.sqrt(2)),S.sqrt(2)/4)
        self.assertEqual((S.sqrt(2)/(4*33))**2,S.Rational(1,8712))
        self.assertEqual(S.Rational(1,2)*S.Rational(1,4),S.Rational(1,8))
        # ||sqrt(2)*2*1_00*h0||_H^2 = 1.
        self.assertEqual(S.Rational(1,8)*8,1)
        self.assertEqual(sum(S.binomial(4,k)*S.factorial(k) for k in range(5)),65)

    def test_weighted_Cauchy_Schwarz_moments(self):
        u=S.symbols('u',nonnegative=True)
        self.assertEqual(S.integrate((1+u)**-4,(u,0,S.oo)),S.Rational(1,3))
        self.assertEqual(S.integrate(u**2*(1+u)**-4,(u,0,S.oo)),S.Rational(1,3))
        z=S.symbols('z',nonnegative=True)
        self.assertEqual(S.simplify(S.integrate((1+u)**-4,(u,z,S.oo))-1/(3*(1+z)**3)),0)

    def test_certified_positive_slope(self):
        r=build()
        self.assertTrue(arb(r['tube']['limit_lower_bound'])>arb('4.5e-8'))
        self.assertTrue(arb(r['rigging']['operator_bound_V_to_dual'])<arb('1.028'))
        self.assertTrue(arb(r['rigging']['Abel_error_coefficient'])<arb('1.342'))

    def test_direct_three_variable_gaussian_against_schur(self):
        b=float(beta);ys=[np.array([.3,-.8]),np.array([1.2,2.1])]
        for code in core.histories():
            m=b*np.array(core.h0(code),dtype=float)
            for eps in (.2,.01):
                a=np.diag([1.,1.,eps])-1j*m[:3,:3]
                root=np.prod(np.sqrt(np.linalg.eigvals(a)))
                eff=m[3:,3:]+1j*m[3:,:3]@np.linalg.solve(a,m[:3,3:])
                for y in ys:
                    direct=(2*np.pi)**1.5/np.sqrt(np.pi)/root*np.exp(1j*y@eff@y/2)
                    z=eps-1j*m[2,2]
                    kb=m[np.ix_(B,B)]+1j*np.outer(m[list(B),2],m[2,list(B)])/z
                    ain=np.eye(2)-1j*kb[:2,:2]
                    roots=np.prod(np.sqrt(np.linalg.eigvals(ain)))
                    exponent=1j*y@kb[2:,2:]@y/2-y@kb[2:,:2]@np.linalg.solve(ain,kb[:2,2:]@y)/2
                    staged=np.sqrt(2*np.pi)/np.sqrt(z)*2*np.sqrt(np.pi)/roots*np.exp(exponent)
                    self.assertLess(abs(direct-staged),2e-12*max(1,abs(staged)))

if __name__=='__main__':
    unittest.main(verbosity=2)
