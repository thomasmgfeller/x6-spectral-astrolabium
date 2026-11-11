"""Exact algebra and limiting-theory checks, not CST continuum qualification."""
import unittest
import itertools
import sympy as s
from model import bd_matrix, gamma, scalar_action, scalar_hessian, dust_action, green_data, gaussian_order, carrier, g


class FiniteActionTests(unittest.TestCase):
    def setUp(self):
        self.code = g.encode([(0,1),(1,2),(0,2)],3)
        self.B = bd_matrix(self.code,3)
        self.f = s.Matrix(s.symbols('f0:3', real=True))
        self.v = s.Matrix([s.Rational(2,3),s.Rational(3,2),s.Rational(5,4)])

    def test_product_identity_cancels_arbitrary_diagonal(self):
        diagonal=s.diag(*s.symbols('z0:3', real=True))
        h=s.Matrix(s.symbols('h0:3',real=True))
        self.assertEqual(s.simplify(gamma(self.B+diagonal,self.f,h)-gamma(self.B,self.f,h)),s.zeros(3,1))

    def test_product_and_pair_actions_agree(self):
        u=s.symbols('u',nonnegative=True)
        pairs=-sum(self.v[x]*self.B[x,y]*(self.f[x]-self.f[y])**2/4 for x in range(3) for y in range(3))
        mass=-u*sum(self.v[x]*self.f[x]**2 for x in range(3))/2
        self.assertEqual(s.expand(scalar_action(self.B,self.f,self.v,u)-pairs-mass),0)

    def test_hessian_from_independent_symbolic_variation(self):
        u=s.symbols('u',nonnegative=True)
        S=scalar_action(self.B,self.f,self.v,u)
        H=scalar_hessian(self.B,self.v,u)
        self.assertEqual(s.hessian(S,list(self.f)),H)
        self.assertEqual(s.simplify(s.Matrix([s.diff(S,f) for f in self.f])-H*self.f),s.zeros(3,1))
        self.assertEqual(H,H.T)

    def test_massless_shift_and_massive_constant_response(self):
        c=s.symbols('c',real=True);one=s.ones(3,1)
        self.assertEqual(s.expand(scalar_action(self.B,self.f+c*one,self.v)-scalar_action(self.B,self.f,self.v)),0)
        self.assertEqual(scalar_hessian(self.B,self.v,2)*one,-2*self.v)

    def test_parity_of_complete_matter_action(self):
        T=s.Matrix(s.symbols('T0:3',real=True));w=s.Matrix(s.symbols('w0:3',nonnegative=True))
        full=dust_action(self.B,T,w)+scalar_action(self.B,self.f,self.v,2)
        flipped=full.subs(dict(zip(self.f,-self.f)),simultaneous=True)
        self.assertEqual(s.expand(full-flipped),0)

    def test_no_direct_scalar_dust_derivatives(self):
        T=s.Matrix(s.symbols('T0:3',real=True));w=s.Matrix(s.symbols('w0:3',nonnegative=True))
        full=dust_action(self.B,T,w)+scalar_action(self.B,self.f,self.v,2)
        for f,z in itertools.product(self.f,list(T)+list(w)):
            self.assertEqual(s.diff(full,f,z),0)
        self.assertEqual(s.simplify(s.diff(full,w[2])+(gamma(self.B,T)[2]+1)/2),0)

    def test_field_persists_on_dust_null_atom(self):
        H=scalar_hessian(self.B,self.v,2)
        self.assertNotEqual(H,s.zeros(3))
        self.assertNotEqual(scalar_action(self.B,self.f,self.v,2),0)

    def test_green_identity_and_hessian(self):
        q=green_data(self.B,self.v,2)
        S=(self.f.T*s.diag(*self.v)*q['D']*self.f)[0]/2-q['tau'].dot(self.f.multiply_elementwise(self.f))/4-self.v.dot(self.f.multiply_elementwise(self.f))
        self.assertEqual(s.expand(S-scalar_action(self.B,self.f,self.v,2)),0)
        self.assertEqual(q['H'],scalar_hessian(self.B,self.v,2))
        self.assertEqual(q['tau'].dot(s.ones(3,1)),0)

    def test_boundary_term_cannot_be_dropped(self):
        B=bd_matrix(g.encode([(0,1)],2),2);f=s.Matrix([1,0]);q=green_data(B,[1,1])
        bulk=(f.T*q['D']*f)[0]/2
        true=scalar_action(B,f,[1,1])
        self.assertEqual(true-bulk,-q['tau'].dot(f.multiply_elementwise(f))/4)
        self.assertNotEqual(true,bulk)

    def test_variational_boundary_reaction_and_stationary_elimination(self):
        H=scalar_hessian(self.B,[1,1,1],0)
        b=s.Matrix(s.symbols('b0:2',real=True));ib=[0,2];ii=[1]
        A=H.extract(ii,ii);J=H.extract(ii,ib);B=H.extract(ib,ib)
        q=-A.inv()*J*b;phi=s.Matrix([b[0],q[0],b[1]])
        S=scalar_action(self.B,phi,[1,1,1])
        E=B-J.T*A.inv()*J
        self.assertEqual(s.simplify(S-(b.T*E*b)[0]/2),0)
        self.assertEqual(s.Matrix([s.diff(S,z) for z in b]),E*b)

    def test_joint_geometry_move_includes_dust_and_scalar(self):
        other=g.encode([(0,1),(0,2)],3);Bp=bd_matrix(other,3)
        T=s.Matrix([s.Rational(1,3),s.Rational(4,3),2]);w=s.Matrix([0,s.Rational(2,3),1]);phi=s.Matrix([1,-2,3])
        k=s.symbols('k',real=True)
        def total(B,code):return k*g.action(code,3)+dust_action(B,T,w)+scalar_action(B,phi,self.v,2)
        predicted=k*(g.action(other,3)-g.action(self.code,3))-sum((w[x]*(T[x]-T[y])**2+self.v[x]*(phi[x]-phi[y])**2)*(Bp[x,y]-self.B[x,y])/4 for x in range(3) for y in range(3))
        self.assertEqual(s.expand(total(Bp,other)-total(self.B,self.code)-predicted),0)

    def test_internal_split_needs_interval_reclassification(self):
        phi=s.Matrix([1,2,4]);full=scalar_action(self.B,phi,[1,1,1])
        a=[0,2];b=[1]
        Ba=bd_matrix(g.induced(self.code,3,5),2);Bb=bd_matrix(0,1)
        isolated=scalar_action(Ba,phi.extract(a,[0]),[1,1])+scalar_action(Bb,phi.extract(b,[0]),[1])
        cross=-sum(self.B[x,y]*(phi[x]-phi[y])**2/4 for x in range(3) for y in range(3) if (x in a)!=(y in a))
        regrade=-(self.B[2,0]-Ba[1,0])*(phi[2]-phi[0])**2/4
        self.assertEqual(s.expand(full-isolated-cross-regrade),0)
        self.assertNotEqual(regrade,0)

    def test_relabelling_covariance(self):
        p=(2,0,1);P=s.zeros(3)
        for i,j in enumerate(p):P[j,i]=1
        Bp=bd_matrix(g.relabel(self.code,3,p),3)
        self.assertEqual(Bp,P*self.B*P.T)
        self.assertEqual(scalar_hessian(Bp,P*self.v,2),P*scalar_hessian(self.B,self.v,2)*P.T)

    def test_gravity_curvature_identity(self):
        for n in (1,2,3):
            for code in g.all_posets(n):
                B=bd_matrix(code,n)
                self.assertEqual(-(s.ones(1,n)*B*s.ones(n,1))[0],g.action(code,n))

    def test_rejects_invalid_action_inputs(self):
        cases=[lambda:bd_matrix(1,2),lambda:bd_matrix(1<<10,2),lambda:bd_matrix(0,0),
               lambda:bd_matrix(0,2,-1),lambda:scalar_hessian(self.B,[1,0,1]),
               lambda:scalar_hessian(self.B,[1,1],0),lambda:scalar_hessian(self.B,[1,1,1],-1),
               lambda:scalar_hessian([[s.nan]], [1]),lambda:scalar_hessian([[s.I]], [1]),
               lambda:scalar_action([[0]],[s.I],[1]),lambda:dust_action([[0]],[0],[-1])]
        for f in cases:
            with self.assertRaises(ValueError):f()


class ContinuumAndCarrierTests(unittest.TestCase):
    def test_curvature_cancellation_in_polarized_product(self):
        f,h,bf,bh,dot,R=s.symbols('f h bf bh dot R')
        Bf=bf-R*f/2;Bh=bh-R*h/2;Bfh=f*bh+h*bf+2*dot-R*f*h/2;B1=-R/2
        self.assertEqual(s.expand((Bfh-f*Bh-h*Bf+f*h*B1)/2),dot)

    def test_continuum_euler_equation_and_positive_energy(self):
        t,x=s.symbols('t x',real=True);mu=s.symbols('mu',nonnegative=True);f=s.Function('f')(t,x)
        L=(s.diff(f,t)**2-s.diff(f,x)**2-mu**2*f**2)/2
        EL=s.diff(L,f)-s.diff(s.diff(L,s.diff(f,t)),t)-s.diff(s.diff(L,s.diff(f,x)),x)
        self.assertEqual(s.simplify(EL-(-s.diff(f,t,2)+s.diff(f,x,2)-mu**2*f)),0)
        E=s.diff(L,s.diff(f,t))*s.diff(f,t)-L
        self.assertEqual(s.simplify(E-(s.diff(f,t)**2+s.diff(f,x)**2+mu**2*f**2)/2),0)

    def test_minkowski_dispersion(self):
        t,x,omega,k,mu=s.symbols('t x omega k mu',real=True)
        f=s.exp(s.I*(k*x-omega*t))
        residual=s.expand((-s.diff(f,t,2)+s.diff(f,x,2)-mu**2*f)/f)
        self.assertEqual(residual,omega**2-k**2-mu**2)

    def test_dust_perturbation_is_constrained(self):
        e,rho,pdot,px,sigma=s.symbols('e rho pdot px sigma',real=True)
        L=-(rho+e*sigma)*(-(1+e*pdot)**2+e**2*px**2+1)/2
        second=s.expand(L).coeff(e,2)
        self.assertEqual(s.expand(second-rho*(pdot**2-px**2)/2-sigma*pdot),0)
        self.assertEqual(s.diff(second,sigma),pdot)

    def test_direct_density_mass_coupling_changes_dust_norm(self):
        w,Gamma,gamma0,phi,F=s.symbols('w Gamma gamma0 phi F',nonzero=True)
        S=-w*(Gamma+1)/2-gamma0*w*phi**2/(2*F**2)
        self.assertEqual(s.diff(S,w),-(Gamma+1+gamma0*phi**2/F**2)/2)

    def test_full_stress_tensor_and_dust_norm(self):
        # Independent variation with respect to a general symmetric inverse metric.
        variables=s.symbols('g0:10',real=True);pairs=[(i,j) for i in range(4) for j in range(i,4)]
        inv=s.zeros(4)
        for z,(i,j) in zip(variables,pairs):inv[i,j]=inv[j,i]=z
        T=s.Matrix(s.symbols('T0:4',real=True));f=s.Matrix(s.symbols('f0:4',real=True))
        rho,mu,phi=s.symbols('rho mu phi',real=True)
        L=-rho*((T.T*inv*T)[0]+1)/2-((f.T*inv*f)[0]+mu**2*phi**2)/2
        eta=s.diag(-1,1,1,1);atflat=dict(zip(variables,[eta[i,j] for i,j in pairs]))
        for z,(i,j) in zip(variables,pairs):
            # Metric derivative for offdiagonals contains two equal components.
            Tij=-2*s.diff(L,z)/(1 if i==j else 2)+eta[i,j]*L.subs(atflat)
            expected=rho*T[i]*T[j]+f[i]*f[j]+eta[i,j]*L.subs(atflat)
            self.assertEqual(s.expand(Tij-expected),0)
        self.assertEqual(s.diff(L,rho),-((T.T*inv*T)[0]+1)/2)

    def test_all_aa_interiors_have_uniform_gap(self):
        u=s.symbols('u',nonnegative=True)
        hist={}
        for covered,count in [(False,49),(True,33)]:
            codes=carrier('A','A',covered);self.assertEqual(len(codes),count)
            histogram={}
            for code in codes:
                B=bd_matrix(code,5);H=scalar_hessian(B,[1]*5,u)
                rel=set(g.pairs(code,5));p=sum((i,2) in rel for i in [0,1]);q=sum((2,j) in rel for j in [3,4])
                self.assertEqual(H[2,2],-s.Rational(p+q,2)-u)
                self.assertTrue(s.simplify(-H[2,2]-1-u).is_nonnegative)
                histogram[str(H[2,2]+u)]=histogram.get(str(H[2,2]+u),0)+1
            hist[covered]=histogram
        self.assertEqual(hist[True],{'-1':20,'-3/2':12,'-2':1})
        self.assertEqual(hist[False],{'-1':32,'-3/2':16,'-2':1})

    def test_all_directed_hessians_and_adapter(self):
        count=0
        for x,y in itertools.product('AK',repeat=2):
            for code in carrier(x,y):
                B=bd_matrix(code,5);H=scalar_hessian(B,[1]*5)
                self.assertEqual(H,H.T)
                self.assertEqual(H*s.ones(5,1),s.zeros(5,1))
                self.assertEqual(H,green_data(B,[1]*5)['H'])
                adapted=gaussian_order(H)
                self.assertEqual(adapted[4,4],H[2,2])
                self.assertEqual(adapted[:4,4],H.extract([0,1,3,4],[2]))
                count+=1
        self.assertEqual(count,107)

    def test_chain_collar_singularity_not_excluded_by_aa_theorem(self):
        # Full five-chain: interior diagonal is 8-u, hence zero at u=8.
        code=g.encode([(i,j) for i in range(5) for j in range(i+1,5)],5)
        H=scalar_hessian(bd_matrix(code,5),[1]*5,8)
        self.assertEqual(H[2,2],0)
        self.assertNotEqual(H.extract([2],[0,1,3,4]),s.zeros(1,4))

    def test_geometry_sum_does_not_factorize(self):
        # Exact two-history identity; no model amplitudes assigned.
        d1,d2,a1,a2=s.symbols('d1 d2 a1 a2')
        joint=(d1*a1+d2*a2)/2;product=(d1+d2)*(a1+a2)/4
        self.assertEqual(s.expand(joint-product),s.expand((d1-d2)*(a1-a2)/4))


if __name__ == '__main__':
    unittest.main()
