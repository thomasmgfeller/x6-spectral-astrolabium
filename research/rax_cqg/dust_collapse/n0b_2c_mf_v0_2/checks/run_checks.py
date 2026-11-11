#!/usr/bin/env python3
"""Small exact/synthetic controls. No CST kernel or PDE production run."""
import argparse
import json
from pathlib import Path
import sympy as s


def evaluate():
    records = []

    def check(name, condition, detail):
        if condition is not True and condition != s.true:
            raise RuntimeError(f"FAILED: {name}: {condition}")
        records.append({"id": name, "result": "PASS", "scope": "algebraic_or_finite_control", "detail": detail})

    q, z, t = s.symbols('q z t', real=True)
    a, b, h = s.symbols('a b h', positive=True)
    f, fc = s.Function('f')(q,z,t), s.Function('fc')(q,z,t)
    v = s.Function('v')(q,z)
    ft = s.I*(a*s.diff(f,q,2)+b*s.diff(f,z,2)-v*f)/h
    fct = -s.I*(a*s.diff(fc,q,2)+b*s.diff(fc,z,2)-v*fc)/h
    sub = {s.diff(f,t):ft,s.diff(fc,t):fct}
    for x in (q,z):
        sub[s.diff(f,x,t)] = s.diff(ft,x)
        sub[s.diff(fc,x,t)] = s.diff(fct,x)
    e = a*s.diff(fc,q)*s.diff(f,q)+b*s.diff(fc,z)*s.diff(f,z)+v*fc*f
    sq = -a*(fct*s.diff(f,q)+s.diff(fc,q)*ft)
    sz = -b*(fct*s.diff(f,z)+s.diff(fc,z)*ft)
    re = s.simplify(s.diff(e,t).subs(sub,simultaneous=True)+s.diff(sq,q)+s.diff(sz,z))
    check('BAL-ENERGY',re==0,'Scalar product-rule identity; Hermitian matrix terms cancel by the same inner-product identity.')
    p = h*(fc*s.diff(f,q)-s.diff(fc,q)*f)/(2*s.I)
    pqq = a*(s.diff(fc,q)*s.diff(f,q)-(fc*s.diff(f,q,2)+s.diff(fc,q,2)*f)/2)
    pqz = b*(s.diff(fc,z)*s.diff(f,q)+s.diff(fc,q)*s.diff(f,z)-fc*s.diff(f,q,z)-s.diff(fc,q,z)*f)/2
    rp = s.simplify(s.diff(p,t).subs(sub,simultaneous=True)+s.diff(pqq,q)+s.diff(pqz,z)+fc*s.diff(v,q)*f)
    check('BAL-MOMENTUM',rp==0,'Local bulk identity with the declared stress; boundary integration is a separate operation.')
    u,w,uc,wc,g = s.symbols('u w uc wc g', real=False)
    transfer = s.I*g*wc*u/h-uc*s.I*g*w/h
    J = 2*g*(uc*w-u*wc)/(2*s.I*h)
    check('BAL-TRANSFER',s.simplify(transfer-J)==0,'Positive source in channel 0, negative source in channel + for real local G.')
    check('BAL-SOURCE-CANCEL',s.simplify(transfer + (s.I*g*uc*w-wc*s.I*g*u)/h)==0,'The two mixing sources cancel.')

    x=s.symbols('x', nonnegative=True)
    psi=2/s.pi**s.Rational(1,4)*x*s.exp(-x*x/2)
    check('WALL-NORM',s.integrate(psi**2,(x,0,s.oo))==1,'Normalized half-line packet, hbar=M=1.')
    wall=s.simplify(s.diff(psi,x).subs(x,0)**2/2)
    pdot=s.integrate((-s.diff(psi,x,2)*s.diff(psi,x)+psi*s.diff(psi,x,3))/2,(x,0,s.oo))
    check('WALL-IMPULSE',s.simplify(pdot-wall)==0 and wall==2/s.sqrt(s.pi),'Bulk potential force zero; dP/dt=2/sqrt(pi) from the wall.')
    check('WALL-ZERO-FLUX',psi.subs(x,0)==0 and s.diff(psi,x,2).subs(x,0)==0,'Norm flux and instantaneous energy flux vanish at the wall for this regular free packet.')

    sx=s.Matrix([[0,1],[1,0]]); szm=s.diag(1,-1); eye=s.eye(2)
    R=s.kronecker_product(eye,szm); parity=s.kronecker_product(szm,szm)
    mix=s.kronecker_product(sx,sx)
    check('SYM-MATTER-ODD',R*mix*R==-mix,'Pure matter reflection forbids this term if it is an unbroken channel-neutral symmetry.')
    check('SYM-COMBINED',parity*mix==mix*parity,'Combined parity permits the odd matter/channel-flip term.')
    state=s.Matrix([0,s.Rational(1,2),s.sqrt(3)/2,0])
    rho=state*state.T
    rs=s.Matrix(2,2,lambda i,j:sum(rho[2*i+k,2*j+k] for k in range(2)))
    check('QS-PARITY',parity*state==-state,'Synthetic state lies in one combined parity sector.')
    check('QS-ZERO-COHERENCE',rs[0,1]==0 and rs[0,0]==s.Rational(1,4),'N0=1/4 despite exactly zero reduced channel coherence.')
    check('QS-ENTANGLE',s.trace(rs*rs)==s.Rational(5,8),'Pure global state, channel purity 5/8: entanglement with matter in this Q-free toy.')
    evolved=s.cos(t)*state-s.I*s.sin(t)*mix*state
    rho_t=evolved*evolved.conjugate().T
    reduced_t=s.Matrix(2,2,lambda i,j:sum(rho_t[2*i+k,2*j+k] for k in range(2)))
    rate=s.simplify(s.diff(reduced_t[0,0],t).subs(t,s.pi/4))
    check('QS-WEIGHTED-COHERENCE',(state.T*mix*state)[0]==s.sqrt(3)/2 and reduced_t[0,1]==0 and rate==s.Rational(1,2),'Under H=sigma_x tensor sigma_x, reduced coherence stays zero while dN0/dt=1/2 at t=pi/4; joint coherence survives.')
    check('QS-RECORD',rho[0,0]==0 and rho[3,3]==0,'Conditional matter states are orthogonal |1> and |0>; fidelity zero, same reference frequency.')

    A,B,m,omega,ell=s.symbols('A B m omega ell', positive=True)
    annih=s.Matrix([[0,1,0],[0,0,s.sqrt(2)],[0,0,0]])
    phi=ell*(annih+annih.T); mom=s.I*m*omega*ell*(annih.T-annih)
    G=A*phi+B*mom
    for n in (0,1):
        up=s.simplify(G[n+1,n]/(ell*s.sqrt(n+1)))
        down=s.simplify(G[n,n+1]/(ell*s.sqrt(n+1)))
        check(f'OP-UP-DOWN-{n}',up==A+s.I*B*m*omega and down==A-s.I*B*m*omega,'Both bands in the SAME block distinguish coordinate and momentum terms.')
    G=-s.I*B*mom
    H=s.zeros(3).row_join(G).col_join(G.conjugate().T.row_join(s.zeros(3)))
    check('OP-HERMITIAN-TRAP',H==H.conjugate().T and s.simplify(G[1,0]/ell)==B*m*omega and s.simplify(G[0,1]/ell)==-B*m*omega,'Real constant upper-band coefficient and full Hermiticity alone do not prove G=g phi.')
    check('OP-VACUUM',phi[0,0]==0,'Strict common-vacuum projection removes the direct linear coupling.')

    # Exact normalized first-order mode estimate versus exact spectral projector.
    mat=s.Matrix([[s.Rational(19,10),s.Rational(1,10)],[s.Rational(1,10),2]])
    lo=(39-s.sqrt(5))/20; hi=(39+s.sqrt(5))/20
    proj=(hi*s.eye(2)-mat)/(hi-lo)
    exact=s.simplify(proj[1,1]); estimate=s.Rational(1,101)
    check('MODE-EXACT-PROJECTOR',s.simplify(proj*proj-proj)==s.zeros(2),'Exact lowest spectral projector of A0+delta A, A0=diag(1,2).')
    check('MODE-FALSE-PASS',bool(estimate<s.Rational(1,100)) and bool(exact>s.Rational(27,100)),'First-order estimate 1/101; actual discarded weight (1-1/sqrt(5))/2. Not a CST result.')

    k=s.Matrix([[2,0],[-1,2]]); xx,yy=s.symbols('xx yy',real=True); vec=s.Matrix([xx,yy])
    action=(vec.T*k*vec)[0]/2
    grad=s.Matrix([s.diff(action,xx),s.diff(action,yy)])
    check('ACTION-SYMMETRIZATION',grad==(k+k.T)*vec/2 and grad!=k*vec,'A retarded triangular matrix does not equal the variation of its real quadratic form.')
    mat=s.Matrix([[3,1,1],[1,4,2],[1,2,5]])
    bb=mat[:2,:2]; bi=mat[:2,2:]; ii=mat[2:,2:]
    schur=bb-bi*ii.inv()*bi.T
    inner=-(ii.inv()*bi.T*vec)[0]; whole=s.Matrix([xx,yy,inner])
    check('SCHUR-STATIONARY',s.simplify((whole.T*mat*whole)[0]-(vec.T*schur*vec)[0])==0,'Symmetric, invertible interior block: exact stationary elimination.')
    check('GAUSSIAN-FACTOR',s.simplify(s.sqrt(s.Rational(5,20)))==s.Rational(1,2),'Changing interior eigenvalue 5 to 20 changes Gaussian magnitude by 1/2 even at identical effective boundary action.')
    kernel_hessian=s.Matrix([[0,-m*omega],[-m*omega,0]])
    check('MODE-FREQUENCY-TRAP',kernel_hessian.eigenvals()=={-m*omega:1,m*omega:1},'Stable oscillator boundary Hessian at quarter period has both signs; its eigenvalues are not potential stiffnesses.')

    # Exact two-channel revival and commensurate-step aliasing, not sampled floating exponentials.
    atpi=s.cos(s.pi)*eye-s.I*s.sin(s.pi)*sx
    check('KERNEL-REVIVAL',atpi==-eye and sx[0,1]==1,'K0+=0 at t=pi for H=sigma_x although H0+=1.')
    check('BRANCH-ALIAS',all(s.exp(-s.I*8*s.pi/d)==1 for d in (1,2,4)),'Energy shift 8*pi*hbar/delta is invisible at delta, delta/2, delta/4.')
    gamma,dt=s.symbols('gamma dt',positive=True)
    check('UNITARITY-RATE',s.limit((1-s.exp(-2*gamma*dt))/dt,dt,0)==2*gamma,'Vanishing step defect can hide finite dissipation per unit clock.')
    E=s.symbols('E',positive=True); pp=s.symbols('pp',real=True)
    check('CLOCK-SUPPORT',s.solve(pp**2-E**2,pp)==[-E,E] and s.diff(pp**2-E**2,pp).subs(pp,E)==2*E,'Quadratic constraint has the same selected root as a linear constraint, with a distinct delta weight.')

    mass=s.Function('mass')(q); om=s.Function('omega')(q); momentum=s.symbols('momentum')
    hm=momentum**2/(2*mass)+mass*om**2*z**2/2
    force=s.diff(mass,q)*momentum**2/(2*mass**2)-s.diff(mass*om**2,q)*z**2/2
    check('MASS-BACKREACTION',s.simplify(-s.diff(hm,q)-force)==0,'Variable matter mass adds a kinetic geometric-force contribution.')
    eps=s.symbols('eps',positive=True)
    check('FORCE-REST',s.diff(eps*s.sin(q/eps**2),q).subs(q,0)==1/eps,'Small coordinate-coupling amplitude alone does not control its geometric derivative.')
    theta=s.symbols('theta',real=True)
    check('REFINE-LEAKAGE',s.trigsimp(2*(1-s.cos(theta))-s.sin(theta)**2-(1-s.cos(theta))**2)==0,'For scalar compression cos(theta), leakage sin^2(theta)<=2|1-cos(theta)|; general proof in the contract.')
    ratios=[s.Rational(121-1,81-1),s.Rational(137-1,91-1),s.Rational(121-1,81-1)]
    check('GRID-NONHOMOTHETIC',len(set(ratios))==2,'G2/G1 interval ratios differ across the proposed axes.')

    return {"schema_version":"1.0","package":"N0B-2C-MF v0.2",
            "scope":"algebraic identities and finite synthetic controls only",
            "count":len(records),"controls":records,
            "physical_gates":{k:"HOLD" for k in ('MODEL','CURRENT','CORRESPONDENCE','BOUNCE','REGULARITY','BOUNDARY','TRAPPING','EXTENSION')},
            "grid_study":"NOT_RUN","cst_kernel_extraction":"NOT_RUN",
            "mode_counterexample":{"estimate_exact":"1/101","discarded_weight_exact":"(1-1/sqrt(5))/2"}}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    result=evaluate()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8')
    print(f"PASS: {result['count']} scoped controls; physical gates HOLD")


if __name__=='__main__':
    main()
