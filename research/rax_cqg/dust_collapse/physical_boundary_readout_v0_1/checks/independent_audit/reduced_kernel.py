#!/usr/bin/env python3
"""Independent exact normalization checks for the proposed scalar rigging kernels."""
from pathlib import Path
import json
import sympy as s

OUT=Path(__file__).resolve().parent
P=[0,1,2,3];I=[4,5,6];F=[7,8,9,10];B=P+F
full={(i,j) for i in range(11) for j in range(i+1,11)}
def hessian(rel):
    L=s.zeros(11)
    for i,j in rel:
        n=sum((i,k) in rel and (k,j) in rel for k in range(11))
        v=[1,-9,16,-8][n] if n<4 else 0
        L[i,i]+=v;L[j,j]+=v;L[i,j]-=v;L[j,i]-=v
    return -L/2
H0=hessian(full);H1=hessian(full-{(4,5),(5,6)})
x=s.Matrix(s.symbols('x0:3',real=True));y=s.Matrix(s.symbols('y0:3',real=True))
tm,tp=s.symbols('tminus tplus',real=True)
am=s.Matrix([-128,241,119,-232]);bm=s.Matrix([-46,-32,-16,0])
ap=s.Matrix([-232,119,241,-128]);bp=s.Matrix([0,16,32,46])
Ex=s.Matrix([0,*x]);Ey=s.Matrix([*y,0])
qp=Ex+bm*tm;qf=Ey+bp*tp
fm=tm*(am.dot(Ex))+am.dot(bm)*tm**2/2
fp=tp*(ap.dot(Ey))+ap.dot(bp)*tp**2/2
Hred=H0.extract(B,B)-H0.extract(B,I)*H0.extract(I,I).inv()*H0.extract(I,B)
z=qp.col_join(qf)
phase=s.expand((z.T*Hred*z)[0]/2+fp-fm)
D=s.hessian(phase,[tm,tp])
assert D==s.Matrix([[-s.Rational(7696,9),-s.Rational(4096,9)],[-s.Rational(4096,9),-s.Rational(7696,9)]])
assert D.det()==s.Rational(4716800,9)
assert D[0,0]<0 and D.det()>0  # Negative definite; two-dimensional Fresnel phase -i.
audit=json.loads((OUT/'results.json').read_text())
M0=s.Matrix(audit['scalar_boundary'][0]['endpoint_map_in_q_pi'])
M0red=s.Matrix(audit['conditional_common_scalar_reduction']['chain_reduced_map'])
detBfull=M0[:4,4:].det();detBred=M0red[:3,3:].det()
assert detBfull==s.Rational(9,65536)
assert detBred==s.Rational(737,35633440)
rational_norm=s.simplify(46**2*detBred/(detBfull*D.det()))
assert rational_norm==s.Rational(32,52625)

# C1: integrate q4,q6 (nondegenerate pair) and q5 (Fourier delta).
boundary_values=Ex.col_join(Ey)
h4=(H1.extract([4],B)*boundary_values)[0]
h5=(H1.extract([5],B)*boundary_values)[0]
h6=(H1.extract([6],B)*boundary_values)[0]
Phi=s.expand((boundary_values.T*H1.extract(B,B)*boundary_values)[0]/2-2*h4*h6)
ell=s.expand(h5)
expected=8*x[0]-s.Rational(9,2)*x[1]+x[2]/2+y[0]/2-s.Rational(9,2)*y[1]+8*y[2]
assert s.expand(ell-expected)==0
assert H1.extract([4,6],[4,6])==s.Matrix([[0,s.Rational(1,2)],[s.Rational(1,2),0]])
# In the K^*K integral, use one delta to eliminate y2, leaving one
# configuration constraint and two Fourier-delta constraints on x-xprime.
d=s.Matrix(s.symbols('d0:3',real=True))
prime={x[j]:x[j]-d[j] for j in range(3)}
phase_difference=s.expand(Phi-Phi.subs(prime,simultaneous=True))
y2solve=s.solve(ell,y[2])[0]
reduced_phase=s.expand(phase_difference.subs(y[2],y2solve))
constraints=[s.expand(ell-ell.subs(prime,simultaneous=True)),
             s.diff(reduced_phase,y[0]),s.diff(reduced_phase,y[1])]
Jac=s.Matrix(constraints).jacobian(d)
assert abs(Jac.det())==2116
# C_delta^2 * (2pi/beta)^2 /(8*|det Jac|) = 1.
assert 8*abs(Jac.det())==(92*s.sqrt(2))**2
# Reverse composition KK^dagger: eliminate x0 and Fourier-integrate x1,x2.
dy=s.Matrix(s.symbols('dy0:3',real=True))
yprime={y[j]:y[j]-dy[j] for j in range(3)}
reverse_phase=s.expand(Phi-Phi.subs(yprime,simultaneous=True))
reverse_phase=s.expand(reverse_phase.subs(x[0],s.solve(ell,x[0])[0]))
reverse_constraints=[s.expand(ell-ell.subs(yprime,simultaneous=True)),
                     s.diff(reverse_phase,x[1]),s.diff(reverse_phase,x[2])]
reverse_Jac=s.Matrix(reverse_constraints).jacobian(dy)
assert abs(reverse_Jac.det())==2116

result={'id':'INDEPENDENT-REDUCED-KERNEL-NORMALIZATION-0.1','all_checks_pass':True,
        'chain_gauge_hessian':[[str(v) for v in row] for row in D.tolist()],
        'chain_gauge_hessian_signature':-2,
        'chain_zero_gauge_momentum_slice_squared_norm_relative_to_unitary':'beta/(2*pi*(52625/32))',
        'chain_positive_FP_multiplier':'sqrt(2*pi*(52625/32)/beta)',
        'chain_gauge_Fresnel_phase':'-i; keep consistently with the full metaplectic phase convention',
        'variant_bare_section_factor':'8*pi^2/beta^2',
        'variant_delta_argument':str(ell),
        'variant_delta_phase':str(Phi),
        'variant_KdaggerK_constraint_jacobian':[[str(v) for v in row] for row in Jac.tolist()],
        'variant_KdaggerK_constraint_jacobian_abs_det':'2116',
        'variant_KKdagger_constraint_jacobian_abs_det':'2116',
        'variant_unitarity_both_directions_checked':True,
        'variant_unitary_delta_kernel_positive_coefficient':'92*sqrt(2)*beta/(2*pi)',
        'variant_positive_multiplier_relative_to_bare_section':'23*sqrt(2)*beta^3/(4*pi^3)',
        'scope':'Checks the declared Lebesgue scalar rigging contract; does not derive its physical selection or compact dust-clock reduction.'}
(OUT/'reduced_kernel_results.json').write_text(json.dumps(result,indent=2)+'\n')
print('PASS independent reduced scalar FP normalization and C1 delta-kernel unitarity constants')
