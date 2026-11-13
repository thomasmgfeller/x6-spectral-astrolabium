"""One frozen physical calibration question, exact and finite.

Derives signed current, proves a restricted positivity/coarse-graining no-go,
executes admissible charge variations and count/exposure nonidentifiability.
No classical collapse trajectories or physical CST measurements are inserted.
"""
from pathlib import Path
from fractions import Fraction as Q
import hashlib,json,itertools
import sympy as s

ROOT=Path(__file__).resolve().parents[2]
contract=ROOT/'contracts/einstein_calibration.json'
expected=contract.with_suffix('.sha256').read_text().split()[0]
actual=hashlib.sha256(contract.read_bytes()).hexdigest()
assert actual==expected
sources=json.loads((Path(__file__).parent/'source_manifest.json').read_text())
for item in sources:
    data=(ROOT/item['local']).read_bytes()
    assert hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()==item['sha']

class I:
    def __init__(self,a,b=None):self.a,self.b=Q(a),Q(a if b is None else b);assert self.a<=self.b
    def __add__(self,o):o=iv(o);return I(self.a+o.a,self.b+o.b)
    __radd__=__add__
    def __neg__(self):return I(-self.b,-self.a)
    def __sub__(self,o):return self+-iv(o)
    def __rsub__(self,o):return iv(o)+-self
    def __mul__(self,o):
        o=iv(o);p=[x*y for x in (self.a,self.b) for y in (o.a,o.b)]
        return I(min(p),max(p))
    __rmul__=__mul__
    def __truediv__(self,o):
        o=iv(o);assert o.a*o.b>0;return self*I(1/o.b,1/o.a)
    def __rtruediv__(self,o):return iv(o)/self
    def __pow__(self,n):
        z=I(1)
        for _ in range(n):z=z*self
        return z
    def out(self):return {'lower_exact':str(self.a),'upper_exact':str(self.b),'decimal_display':[float(self.a),float(self.b)]}
def iv(x):return x if isinstance(x,I) else I(x)
def zero(expr):assert s.cancel(s.expand(expr))==0,expr

a,b,c,d,t,u,w,v,h=s.symbols('a b c d t u w v h',real=True)
times=[a,b,c,d,t,u]
weights={4:w,5:v}
B={(0,4):-8,(1,4):16,(2,4):-9,(3,4):1,
   (1,5):-8,(2,5):16,(3,5):-9,(4,5):1}
C={j:1+sum(s.Rational(bij,2)*(times[j]-times[i])**2
              for (i,jj),bij in B.items() if jj==j) for j in (4,5)}
Sd=-sum(weights[j]*C[j] for j in (4,5))/2
J={(i,j):weights[j]*bij*(times[j]-times[i])/2 for (i,j),bij in B.items()}
q=[]
for z in range(6):
    divergence=sum(value for (i,j),value in J.items() if i==z)-sum(value for (i,j),value in J.items() if j==z)
    zero(divergence-s.diff(Sd,times[z]));q.append(divergence)
zero(sum(q))

r305=s.sqrt(305);k=(70-4*r305)/3
P=h-k;L=9*k-s.Rational(4,3)-s.Rational(17,2)*h;BB=12+36*h
T=9*h+h*L/P
U=9*h+P*BB/L+h*L/(2*P)
r=h*L/(2*P**2)-BB/L
jparam=h*L/P
sub={a:-r305/6,b:-s.Rational(5,2),c:-2,d:-s.Rational(4,3)+h,t:T,u:U,w:r*v}
zero(C[4].subs(sub));zero(C[5].subs(sub));zero(q[4].subs(sub))
Qcharge=v*jparam/2
zero(q[5].subs(sub)-Qcharge)
cut_d=sum(value for (i,j),value in J.items() if i<=3<j)
cut_t=sum(value for (i,j),value in J.items() if i<=4<j)
zero(cut_d.subs(sub)+Qcharge);zero(cut_t.subs(sub)+Qcharge)
pin=-q[3];pout=q[5]
zero((pin-pout-sum(q[:3])).subs(sub))

# Independent rational enclosures of the entire declared h domain.
sqrtI=I('17.46424919657298','17.46424919657299')
assert sqrtI.a**2<305<sqrtI.b**2
hI=I(Q(1,2000),Q(3,2000));kI=(70-4*sqrtI)/3
PI=hI-kI;LI=9*kI-Q(4,3)-Q(17,2)*hI;BI=12+36*hI
TI=9*hI+hI*LI/PI
UI=9*hI+PI*BI/LI+hI*LI/(2*PI)
rI=hI*LI/(2*PI**2)-BI/LI
jI=hI*LI/PI
assert PI.b<0 and LI.b<0 and rI.a>1 and jI.a>0
assert UI.a>TI.b and TI.a>0
QmaxI=jI/(2*rI)
Jtu_over_v=(UI-TI)/2
assert Jtu_over_v.a>0

# Every interval partition keeping d,t,u distinct has mandatory cuts after d,t.
# There are exactly eight choices of the first three cuts. For orientation +,
# a negative total final-cut flux prevents all aggregate edges being positive.
# For orientation -, t and u are singleton cells and their edge is negative.
partitions=[]
for first_cuts in itertools.product((False,True),repeat=3):
    cuts=first_cuts+(True,True)
    groups=[];current=[0]
    for i,cut in enumerate(cuts):
        if cut:groups.append(current);current=[]
        current.append(i+1)
    groups.append(current)
    assert [4] in groups and [5] in groups
    partitions.append({'cells':[[str(times[i]) for i in group] for group in groups],
                       'orientation_plus':'FAIL: complete final cut=-Qcharge<0',
                       'orientation_minus':'FAIL: aggregate edge t->u=-v*(U-T)/2<0'})
assert len(partitions)==8

# Absolute values do not repair the conserved interior current.
absJ={(i,j):weights[j]*abs(bij)*(times[j]-times[i])/2 for (i,j),bij in B.items()}
abs_qt=sum(z for (i,j),z in absJ.items() if i==4)-sum(z for (i,j),z in absJ.items() if j==4)
rectification_defect=-w*(8*(t-a)+9*(t-c))
zero((abs_qt-rectification_defect).subs(sub))
abs_defect_per_w=8*(TI+sqrtI/6)+9*(TI+2)
assert abs_defect_per_w.a>0

# Two exact legal charge preparations; no constraint-inconsistent fixed momenta.
h0=s.Rational(1,1000)
rows=[]
for wvalue in (s.Rational(1,64),s.Rational(1,4)):
    vexpr=wvalue/r
    charge=s.cancel(Qcharge.subs(v,vexpr))
    point={h:h0}
    rows.append({'w':str(wvalue),'v_at_h0':float(vexpr.subs(point)),
                 'Q_exact_formula':str(wvalue)+'*jparam/(2*r)','Q_at_h0':float(charge.subs(point)),
                 't_at_h0':float(T.subs(point)),'u_at_h0':float(U.subs(point)),
                 'physical_mass':None})
ratio=s.cancel(Qcharge.subs(v,s.Rational(1,4)/r)/Qcharge.subs(v,s.Rational(1,64)/r))
assert ratio==16
assert s.diff(T,v)==0 and s.diff(U,v)==0
assert rows[0]['t_at_h0']==rows[1]['t_at_h0'] and rows[0]['u_at_h0']==rows[1]['u_at_h0']

# Existing reference adapter: counts determine exposure*volume, not volume alone.
lam,A,V,scale=s.symbols('lambda A V3 scale',positive=True)
count_mean=lam*A*V
zero(count_mean.subs({A:scale*A,V:V/scale},simultaneous=True)-count_mean)

# Transparent post-result corollaries under the same calibration question.
corollaries=ROOT/'contracts/einstein_corollaries.json'
corollary_contract=json.loads(corollaries.read_text())
assert corollary_contract['base_contract_sha256_unchanged']==actual
# Any fixed F(C,T) and G(C,T) receive identical arguments for Q and 16Q.
# Therefore any nonzero reconstructed Y secant has ratio 1, but the declared
# hypothetical M=cQ requires sqrt(16)=4 in the inherited classical reference.
assert s.sqrt(ratio)==4 and ratio!=1

pilot_path=ROOT/'contracts/pilot.json'
pilot=json.loads(pilot_path.read_text())
assert hashlib.sha256(pilot_path.read_bytes()).hexdigest()==pilot_path.with_suffix('.sha256').read_text().split()[0]
def closure(edges):
    rel=set(tuple(x) for x in edges)
    while True:
        nxt=rel|{(a,c) for a,b in rel for bb,c in rel if b==bb}
        if nxt==rel:return rel
        rel=nxt
orders=set()
hist=pilot['history_family']
for key in ('class_1_added_relations','class_2_added_relations'):
    base=closure(hist['common_generating_relations']+hist[key])
    for swA,swR in itertools.product((False,True),repeat=2):
        perm=list(range(6))
        if swA:perm[1],perm[2]=perm[2],perm[1]
        if swR:perm[4],perm[5]=perm[5],perm[4]
        orders.add(tuple(sorted((perm[i],perm[j]) for i,j in base)))
assert len(orders)==6
tt=s.symbols('T0:6',real=True);rr=s.symbols('r0:6',real=True)
beta=s.symbols('beta',positive=True)
reflection={time:-time for time in tt}
parity_edges=0
for ordered in sorted(orders):
    rel=set(ordered)
    bc={}
    for i,j in rel:
        between=sum((i,z) in rel and (z,j) in rel for z in range(6))
        bc[i,j]=[1,-9,16,-8][between] if between<4 else 0
    dust=-sum(rr[j]*(1+beta*sum(bij*(tt[j]-tt[i])**2 for (i,jj),bij in bc.items() if jj==j)/2) for j in range(6))/2
    zero(dust.xreplace(reflection)-dust)
    for (i,j),bij in bc.items():
        if bij:
            current=beta*rr[j]*bij*(tt[j]-tt[i])/2
            zero(current.xreplace(reflection)+current)
            parity_edges+=1

result={
 'contract_sha256':actual,
 'verified_reused_git_sources':len(sources),
 'status':'EXACT_RESTRICTED_CURRENT_CALIBRATION_OBSTRUCTION_AND_LEGAL_CHARGE_TEST_EXECUTED',
 'physical_CST_measurements':0,
 'current_derivation':{'six_node_derivative_identities':6,'global_shift_identity':'sum q_z=0',
   'stationary_interior_identity':'q_t=0','two_complete_cuts':'F_after_d=F_after_t=-Qcharge',
   'charge':'Qcharge=p_out=v*(t-t_star)/2>0',
   'collar_reaction':'p_in-p_out=q_a+q_b+q_c'},
 'intervals':{'t':TI.out(),'u':UI.out(),'r':rI.out(),'jparam':jI.out(),
   'Q_upper_envelope':QmaxI.out(),'J_tu_over_v':Jtu_over_v.out(),
   'minus_abs_rectification_defect_over_w':abs_defect_per_w.out()},
 'charge_bound':'0<Qcharge<jparam/(2*r); a conservative uniform upper bound is the upper endpoint of Q_upper_envelope',
 'record_preserving_aggregation':{'partitions_tested':8,'all_failed_for_both_global_orientations':True,'partitions':partitions,
   'scope':'Exact order-convex aggregation retaining initial d and later t,u in distinct cells; other derived current observables are not excluded'},
 'absolute_value_control':{'interior_divergence':'-w*(8*(t-a)+9*(t-c))<0',
   'status':'FAIL_CONSERVATION'},
 'legal_charge_comparison':{'h_exact':'1/1000','preparations':rows,'charge_ratio_exact':str(ratio),
   'all_clock_records_unchanged':True,'all_orders_unchanged':True,
   'meaning':'Legal charge response, not physical M-to-R data; both boundary momenta vary consistently with the same family'},
 'count_geometry_identifiability':{'identity':'lambda*A*V3=lambda*(s*A)*(V3/s)',
   'status':'VOLUME_NOT_IDENTIFIABLE_WITHOUT_INDEPENDENT_EXPOSURE',
   'additional_limit':'fixed cardinality is a spacetime count, not an independently measured areal radius'},
 'fixed_order_clock_adapter_obstruction':{
   'assumptions':'Same F(C,T) for radius, same G(C,T) for physical time; hypothetical common M=c*Q with c>0',
   'configuration_identity':'The executed Q and 16Q preparations have exactly identical C and all T',
   'nonzero_reconstructed_Y_secant_ratio':'1',
   'classical_nonzero_Y_slope_ratio_required':'4',
   'zero_secant_case':'Both zero, incompatible with nonzero collapsing slopes at positive mass',
   'status':'EXCLUDED_ADAPTER_CLASS_ONLY',
   'not_excluded':'A different independently derived geometry observable involving additional degrees of freedom, or an enlarged dynamical order family'},
 'actual_six_history_pilot_current_parity':{
   'orders_checked':len(orders),'nonzero_edge_current_parities_checked':parity_edges,
   'action_parity':'S_d(-T)=S_d(T)','current_parity':'J_yx(-T)=-J_yx(T)',
   'other_factors':'Original scalar/gravity factors are clock independent; clock packets and measures are reflection invariant; four event flags depend only on order class and density stratum',
   'conclusion':'Every single-current-inserted event amplitude and oriented cut-charge insertion vanishes exactly for every positive Abel regulator and for an existing paired Abel limit',
   'not_claimed':'No physical mean-current, probability, mass-zero or universal no-go statement; even current correlations may remain nonzero',
   'status':'EXACT_ORIENTED_CURRENT_INSERTION_ZERO'},
 'physical_correspondence':{'status':'NOT_DEFINED_FOR_THIS_CURRENT_AND_RECORD_ADAPTER',
   'specific_obstruction':'No globally oriented positive record-preserving current from exact aggregation; rectification breaks conservation. A conserved scalar charge alone and count/exposure product leave mass normalization and radius unidentified.',
   'scope':'Does not exclude a different derived positive current, enlarged coupled geometry family, or future physical calibration'},
 'checks_passed':True
}
out=ROOT/'results/einstein_calibration.json';out.parent.mkdir(parents=True,exist_ok=True)
out.write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'partitions':8,'Q_uniform_upper':float(QmaxI.b),
                  'charge_ratio':16,'physical_points':0}))
