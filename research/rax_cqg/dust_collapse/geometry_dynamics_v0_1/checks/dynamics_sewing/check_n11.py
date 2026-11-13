#!/usr/bin/env python3
"""Independent N11 endpoint-action sewing and stationary collar audit."""
from pathlib import Path
import json
import sympy as s

BASE = Path(__file__).resolve().parent
N = 11
I = (4, 5, 6)
B = tuple(i for i in range(N) if i not in I)
bcoef = (1, -9, 16, -8)
u = s.symbols('u0:11', real=True)
r = s.symbols('r0:11', real=True)
q = s.symbols('q0:11', real=True)
rho = s.symbols('rho', positive=True)


def action(rel, nodes):
    rows = [(a, b, bcoef[n] if n < 4 else 0)
            for a, b in sorted(rel) if a in nodes and b in nodes
            for n in [sum((a, x) in rel and (x, b) in rel for x in nodes)]]
    return (s.Integer(len(nodes)-sum(c for a,b,c in rows)),
            s.expand(-sum(r[x] for x in nodes)/2-sum(s.Rational(c,38)*r[b]*(u[b]-u[a])**2 for a,b,c in rows)),
            s.expand(-sum(s.Rational(c,4)*(q[b]-q[a])**2 for a,b,c in rows)))


def increment(rel, previous, n):
    assert not any((n, j) in rel for j in previous)
    now = set(previous) | {n}
    rows = [(a, c) for a in previous if (a,n) in rel
            for k in [sum((a,x) in rel and (x,n) in rel for x in now)]
            for c in [bcoef[k] if k<4 else 0]]
    return (s.Integer(1-sum(c for a,c in rows)),
            s.expand(-r[n]/2-sum(s.Rational(c,38)*r[n]*(u[n]-u[a])**2 for a,c in rows)),
            s.expand(-sum(s.Rational(c,4)*(q[n]-q[a])**2 for a,c in rows)))


def enc(matrix):
    return [[str(v) for v in row] for row in matrix.tolist()]


def run():
    chain = {(i,j) for i in range(N) for j in range(i+1,N)}
    other = chain-{(4,5),(5,6)}
    out = {}
    count=0
    for name, rel in [('chain',chain),('two_relation_variant',other)]:
        full=action(rel,set(range(N)))
        steps=[]
        previous=set()
        for n in range(N):
            step=increment(rel,previous,n)
            before=action(rel,previous);after=action(rel,previous|{n})
            for k in range(3):
                assert s.expand(after[k]-before[k]-step[k])==0
                count+=1
            steps.append(step);previous.add(n)
        for k in range(3):
            assert s.expand(sum(x[k] for x in steps)-full[k])==0
            count+=1
        shells=[tuple(s.expand(sum(steps[n][k] for n in nodes)) for k in range(3))
                for nodes in [range(4),range(4,7),range(7,11)]]
        point={r[i]:rho for i in range(N)}|{u[i]:s.Integer(i) for i in range(N)}|{q[i]:0 for i in range(N)}
        if name!='chain':
            point.update({u[4]:4,u[5]:4,u[6]:5,r[4]:2*rho})
        C=[s.simplify(-2*s.diff(full[1],r[i]).subs(point)) for i in I]
        ET=[s.simplify(s.diff(full[1],u[i]).subs(point)) for i in I]
        EQ=[s.simplify(s.diff(full[2],q[i]).subs(point)) for i in I]
        assert C==ET==EQ==[0,0,0]
        inner=[s.simplify(s.diff(shells[1][1],u[i]).subs(point)) for i in I]
        future=[s.simplify(s.diff(shells[2][1],u[i]).subs(point)) for i in I]
        assert any(inner) and all(s.simplify(a+b)==0 for a,b in zip(inner,future))
        H=s.hessian(full[2],q); HII=H.extract(I,I); HIB=H.extract(I,B)
        assert HII.col_join(HIB.T).rank()==3
        on_shell=s.simplify(full[0]+full[1].subs(point))
        clock_boundary=[s.simplify(s.diff(full[1],u[j]).subs(point)) for j in B]
        density_boundary=[s.simplify(s.diff(full[1],r[j]).subs(point)) for j in B]
        # Boundary density path changes every r_B equally; the chain rule needs
        # no inner saddle derivatives because their gradients vanish.
        assert s.simplify(sum(density_boundary)-s.diff(on_shell,rho))==0
        # Common clock shift is a symmetry of the action, and full derivative sum vanishes.
        assert s.simplify(sum(clock_boundary))==0
        out[name]={'F4':str(full[0]),'on_shell_action_q0':str(on_shell),
                   'inner_density_constraints':list(map(str,C)),
                   'inner_clock_stationarity':list(map(str,ET)),
                   'inner_scalar_stationarity':list(map(str,EQ)),
                   'inner_shell_clock_gradient':list(map(str,inner)),
                   'future_shell_clock_gradient':list(map(str,future)),
                   'boundary_clock_derivative_in_u_units':list(map(str,clock_boundary)),
                   'boundary_density_derivative':list(map(str,density_boundary)),
                   'source_derivative_of_stationary_action':str(s.diff(on_shell,rho)),
                   'HII_over_beta':enc(HII),'HIB_over_beta':enc(HIB),
                   'rank_inner_scalar':HII.rank(),
                   'rank_including_boundary_coupling':HII.col_join(HIB.T).rank(),
                   'boundary_decoupled_inner_scalar_null_mode':False}
        # The incomparable 4,5 can be exchanged in the natural labelling.
        if name!='chain':
            ordering=[0,1,2,3,5,4,6,7,8,9,10]
            prev=set(); alt=[]
            for n in ordering:
                alt.append(increment(rel,prev,n));prev.add(n)
            for k in range(3):
                assert s.expand(sum(x[k] for x in alt)-full[k])==0
                count+=1
    difference=s.simplify(s.sympify(out['two_relation_variant']['on_shell_action_q0'],locals={'rho':rho})-s.sympify(out['chain']['on_shell_action_q0'],locals={'rho':rho}))
    assert difference==8+s.Rational(23,19)*rho
    result={'all_checks_pass':True,'exact_sector_sewing_checks':count,
            'fixed_boundary':list(B),'free_interior':list(I),
            'beta':'4/sqrt(6)','clock_scale':'beta*Delta^2=2/19; T_j=Delta*(u_j-5)',
            'rho_range_for_both_saddles':'0<rho<1/2',
            'clock_support_required':'|T|<=5*Delta, approximately1.26945, beyond original[-1,1]',
            'models':out,'variant_minus_chain_action':str(difference),
            'derivative_of_difference_wrt_rho':'23/19',
            'future_collar_required_for_stationarity':True,
            'alternate_natural_labelling_action_invariance':True,
            'new_integrations':0,
            'physical_scope':'Exact stationary-action source response and conditional sewing. Not a normalized physical geometric probability or calibrated mass/radius dynamics.'}
    (BASE/'results_n11.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))


if __name__=='__main__':
    run()
