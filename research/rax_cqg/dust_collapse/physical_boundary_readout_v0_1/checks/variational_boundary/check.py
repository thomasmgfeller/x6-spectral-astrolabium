#!/usr/bin/env python3
"""Exact N11 dust-clock boundary Legendre relation and constrained rank tests.

Clock coordinates: T=Delta*(u-5), beta*Delta^2=2/19.
All reported ranks and identities are exact SymPy expressions.
"""
from pathlib import Path
import json
import sympy as s

BASE=Path(__file__).resolve().parent
N=11; P=(0,1,2,3); I=(4,5,6); F=(7,8,9,10)
u=s.symbols('u0:11',real=True); r=s.symbols('r0:11',real=True)
rho=s.symbols('rho',positive=True); alpha=s.symbols('alpha',real=True)
COEFF=(1,-9,16,-8)
XI=[u[j]for j in I]+[r[j]for j in I]
XP=[u[j]for j in P]+[r[j]for j in P]
XF=[u[j]for j in F]+[r[j]for j in F]


def action(rel):
    constraints=[]
    for j in range(N):
        c=s.Integer(1)
        for i in range(j):
            if(i,j)not in rel:continue
            n=sum((i,k)in rel and(k,j)in rel for k in range(N))
            if n<4:c+=s.Rational(COEFF[n],19)*(u[j]-u[i])**2
        constraints.append(s.expand(c))
    return s.expand(-sum(r[j]*constraints[j]for j in range(N))/2),constraints


def point(variant=False):
    p={u[j]:s.Integer(j)for j in range(N)}|{r[j]:rho for j in range(N)}
    if variant:p.update({u[4]:4,u[5]:4,u[6]:5,r[4]:2*rho})
    return p


def grad(expr,variables):return s.Matrix([s.diff(expr,x)for x in variables])
def enc(m):return [[str(v)for v in row]for row in m.tolist()]
def ve(m):return list(map(str,m))


def run():
    chain={(i,j)for i in range(N)for j in range(i+1,N)}
    variant=chain-{(4,5),(5,6)}
    output={}
    for name,rel in [('C0',chain),('C1',variant)]:
        S,C=action(rel);pt=point(name=='C1')
        E=grad(S,XI)
        pP=-grad(S,XP);pF=grad(S,XF)
        assert E.subs(pt)==s.zeros(6,1)
        # Structural initial density constraints; no saddle is needed here.
        for k,j in enumerate(P):
            assert s.expand(pP[4+k]-C[j]/2)==0
            assert all(s.diff(C[j],x)==0 for x in XI+XF)
        equation=E.col_join(pP)
        J_general=equation.jacobian(XI+XF)
        assert J_general[10:14,:]==s.zeros(4,14)
        J=J_general.subs(pt)
        J_quarter=J.subs(rho,s.Rational(1,4))
        expected_rank=10 if name=='C0' else 9
        assert J.rank()==J_quarter.rank()==expected_rank
        ns=J.nullspace()
        assert len(ns)==14-expected_rank
        assert all(J*v==s.zeros(14,1)for v in ns)
        assert s.Matrix.hstack(*ns).rank()==14-expected_rank
        HII=s.hessian(S,XI).subs(pt)
        assert s.factor(HII.det())==-s.Rational(1,19**6)
        # IFT elimination of the six inner variables; pP=-d_P Sbar.
        H_PF=grad(S,[u[j]for j in P]).jacobian(XF).subs(pt)
        H_PI=grad(S,[u[j]for j in P]).jacobian(XI).subs(pt)
        H_IF=E.jacobian(XF).subs(pt)
        reduced=-s.simplify(H_PF-H_PI*HII.inv()*H_IF)
        assert reduced.rank()==(4 if name=='C0' else 3)
        fixed_rF=J[:10,:10]
        fixed_det=s.factor(fixed_rF.det())
        if name=='C0':
            assert fixed_det==s.Rational(2**27,19**10)*rho**4
        else:
            assert fixed_det==0 and fixed_rF.rank()==9
        output[name]={
            'stationary_initial_configuration_u':[str(pt[u[j]])for j in P],
            'stationary_initial_momenta':ve(pP.subs(pt)),
            'stationary_future_momenta':ve(pF.subs(pt)),
            'initial_density_constraints_p_rP':ve(s.Matrix([C[j]/2 for j in P])),
            'interior_Hessian_determinant':str(s.factor(HII.det())),
            'rank14_symbolic_positive_rho':expected_rank,
            'rank14_at_rho_quarter':J_quarter.rank(),
            'structural_zero_rows':[10,11,12,13],
            'jacobian14':enc(J),
            'null_basis14_at_rho_quarter':[ve(v)for v in J_quarter.nullspace()],
            'reduced_initial_clock_momentum_jacobian_vs_future':enc(reduced),
            'rank_of_reduced_mixed_map':reduced.rank(),
            'fixed_future_density_10x10_determinant':str(fixed_det),
            'fixed_future_density_10x10_rank':fixed_rF.rank(),
        }
        if name=='C1':
            v=(0,8,16,23)
            path=dict(pt)
            path.update({u[j]:pt[u[j]]+alpha*a for j,a in zip(F,v)})
            inner_on_path=s.simplify(E.subs(path))
            initial_change=s.simplify(pP.subs(path)-pP.subs(pt))
            future_change=s.simplify(pF.subs(path)-pF.subs(pt))
            S_change=s.factor(S.subs(path)-S.subs(pt))
            assert inner_on_path==s.zeros(6,1)
            assert initial_change==s.zeros(8,1)
            assert S_change==-alpha*rho*(932*alpha+217)/19
            expected_clock=s.Matrix([232,-119,-241,128])*alpha*rho/19
            assert future_change[:4,:]==expected_clock
            assert s.simplify(sum(grad(S,XF).subs(path)[k]*s.diff(path[XF[k]],alpha)
                                  for k in range(8))-s.diff(S_change,alpha))==0
            # One explicit distinct admissible point lies within the shared [-1.5,1.5] box.
            # Delta^2=sqrt(6)/38<5/76, so this rational upper bound is strict.
            a0=s.Rational(1,1000)
            assert (5+23*a0)**2*s.Rational(5,76)<s.Rational(9,4)
            assert future_change.subs(alpha,a0)!=s.zeros(8,1)
            output[name]['exact_future_family']={
                'uF_base':[7,8,9,10],'uF_direction':list(v),
                'all_r_fixed':True,'all_P_I_fields_fixed':True,
                'interior_Euler_residuals':ve(inner_on_path),
                'initial_momentum_changes':ve(initial_change),
                'future_momentum_changes':ve(future_change),
                'stationary_action_change':str(S_change),
                'explicit_admissible_distinct_alpha':str(a0),
                'within_original_followup_clock_box':True,
                'gauge_identification':'NOT_PROVED; not a global clock shift; future data and action change'}

    # Canonical algebra of the initial boundary constraint image.
    S,C=action(chain)
    pu=s.symbols('pu0:4');pr=s.symbols('pr0:4');coords=list(u[:4])+list(r[:4]);momenta=list(pu)+list(pr)
    def poisson(a,b):return s.expand(sum(s.diff(a,x)*s.diff(b,p)-s.diff(a,p)*s.diff(b,x)for x,p in zip(coords,momenta)))
    chi=[pr[j]-C[j]/2 for j in P]
    pi=[pu[j]-sum(r[k]*s.diff(C[k],u[j])/2 for k in P)for j in P]
    for a,b in [(a,b)for a in range(4)for b in range(4)]:
        assert poisson(chi[a],chi[b])==0
        assert poisson(pi[a],chi[b])==0
        assert poisson(pi[a],pi[b])==0
        assert poisson(u[a],pi[b])==int(a==b)
    endpoint=s.expand(sum(r[j]*C[j]/2 for j in P))
    for j in P:
        assert s.expand(pu[j]-pi[j]-s.diff(endpoint,u[j]))==0
        assert s.expand(C[j]/2-s.diff(endpoint,r[j]))==0
    # Initial momenta of the two known saddles differ, despite equal configurations.
    p0=s.Matrix([s.sympify(x,locals={'rho':rho})for x in output['C0']['stationary_initial_momenta']])
    p1=s.Matrix([s.sympify(x,locals={'rho':rho})for x in output['C1']['stationary_initial_momenta']])
    difference=s.simplify(p1-p0)
    assert difference==s.Matrix([64,-96,4,46,0,0,0,0])*rho/19
    result={
        'id':'CST-DUST-DUSTCLOCK-BOUNDARY-RELATION-0.1','all_checks_pass':True,
        'P':list(P),'I':list(I),'F':list(F),
        'rho_domain':'0<rho<1/2','normalization':'T=Delta*(u-5), beta*Delta^2=2/19; p_u=Delta*p_T',
        'row_order':['dS/du4','dS/du5','dS/du6','dS/dr4','dS/dr5','dS/dr6']+['p_'+str(x)for x in XP],
        'column_order':list(map(str,XI+XF)),
        'boundary_convention':'pP=-d_P Sbar; pF=+d_F Sbar; dSbar=pF dxiF-pP dxiP',
        'models':output,
        'initial_boundary_reduction':{
            'chi':'p_rP-C_P(uP)/2=0','poisson_constraints_commute':True,
            'invariant_clock_momenta':list(map(str,pi)),
            'restricted_one_form':'sum p_u du+p_r dr =sum pi du+d(sum r*C/2)',
            'local_reduced_symplectic_form':'sum_j d(u_j) wedge d(pi_j), using omega=-d(theta)',
            'physical_gauge_identification':'NOT_DERIVED; boundary densities are source data in the inherited protocol'},
        'known_saddles_initial_momentum_difference_C1_minus_C0':ve(difference),
        'quantum_density_translation_obstruction':{
            'measure':'nu=(delta_0+1_(0,1)dr)/2',
            'multiplication_operator_spectrum':'[0,1], with an eigenvector at0',
            'excluded_claim':'a self-adjoint generator with U(s) r U(s)^dagger=r+sI for all real s on the original Hilbert space',
            'proof':'Unitary conjugation preserves spectrum, while r+sI has spectrum[s,1+s]. These differ for every nonzero s.',
            'scope':'No automatic global Weyl/RAQ realization of the classical density-translation reduction on this measure; not an exclusion of all quantizations.'},
        'new_integrations':0,
        'physical_evolution':'NOT_DERIVED; exact canonical relation established, graph property conditional or degenerate'}
    (BASE/'results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'all_checks_pass':True,'ranks14':{k:output[k]['rank14_at_rho_quarter']for k in output},
        'fixed_rF_ranks10':{k:output[k]['fixed_future_density_10x10_rank']for k in output},
        'exact_nonunique_future_family':True,'new_integrations':0},indent=2))


if __name__=='__main__':run()
