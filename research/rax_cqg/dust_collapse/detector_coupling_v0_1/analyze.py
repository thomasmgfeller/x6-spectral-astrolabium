"""Exact audit of record-preserving detector couplings and a mixing witness."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import sys,json,hashlib
ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from previous_core import C,matrix,mul,add,scale,dag,trace,outer,real,I,P,Q

def require(ok,message):
    if not ok:raise RuntimeError(message)
def encode(x):
    if isinstance(x,F):return str(x)
    if isinstance(x,C):return {'re':str(x.r),'im':str(x.i)}
    if isinstance(x,dict):return {str(k):encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x
def dump(name,x):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(x),indent=2,sort_keys=True)+'\n')
def eye(n):return matrix([[int(i==j) for j in range(n)] for i in range(n)])
def zeros(n):return matrix([[0]*n for _ in range(n)])
def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def blocks(a,b):
    z=zeros(len(a)+len(b))
    for i in range(len(a)):
        for j in range(len(a)):z[i][j]=a[i][j]
    for i in range(len(b)):
        for j in range(len(b)):z[len(a)+i][len(a)+j]=b[i][j]
    return z
def rotation(c,s):return matrix([[c,s],[-s,c]])
def diagonal(a,b):return matrix([[a,0],[0,b]])
def effective(t,sigma):
    return [[trace(mul(sigma,[[t[2*i+k][2*j+l] for l in range(2)] for k in range(2)])) for j in range(2)] for i in range(2)]
def prob(e,rho):return real(trace(mul(e,rho)))
def gitsha(b):return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
def sqrt_interval(x,den=10**12):
    k=isqrt(x.numerator*den*den//x.denominator)
    lo=F(k,den);hi=lo if lo*lo==x else F(k+1,den)
    require(lo*lo<=x<=hi*hi,'Rational square-root enclosure');return [lo,hi]

def run():
    plan=json.loads((ROOT/'plan.json').read_text())
    ph=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(ph==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'provenance.json').read_text())
    for name,info in prov['inputs'].items():require(gitsha((ROOT/name).read_bytes())==info['git_blob'],'Pinned source '+name)
    rotations=[rotation(*map(F,row)) for row in plan['pointer_rotations']]
    for r in rotations:require(mul(dag(r),r)==I and mul(r,dag(r))==I,'Rational pointer rotation unitary')
    pa=diagonal(1,0);pc=diagonal(0,1);mixed=scale(I,F(1,2))
    states={'zero':pa,'one':pc,'plus':P,'mixed':mixed}
    pi=matrix([[F(1,2),C(F(0),F(-1,2))],[C(F(0),F(1,2)),F(1,2)]])
    effects={'zero':pa,'plus':P,'plus_i':pi}
    gates={'identity':I,'bit_flip':matrix([[0,1],[1,0]]),'phase_i':diagonal(1,C(F(0),F(1)))}
    rows=[];joint_controls=unitaries=0
    for i,ri in enumerate(rotations):
        for j,rj in enumerate(rotations):
            first=blocks(ri,rj);last=blocks(rj,ri)
            for gn in plan['pointer_middle_gates']:
                w=mul(mul(last,kron(I,gates[gn])),first)
                require(mul(dag(w),w)==eye(4) and mul(w,dag(w))==eye(4),'Two-pulse joint unitary');unitaries+=1
                for en in plan['pointer_effects']:
                    f=effects[en];require(mul(f,f)==f,'Pointer projector')
                    t=mul(mul(dag(w),kron(I,f)),w)
                    for sn in plan['pointer_states']:
                        sigma=states[sn];e=effective(t,sigma)
                        require(e[0][1]==e[1][0]==C(),'Controlled pointer effect is diagonal')
                        vals=[real(e[k][k]) for k in range(2)]
                        require(all(0<=v<=1 for v in vals),'Valid effect')
                        pp,pm=prob(e,P),prob(e,Q)
                        require(pp==pm,'Equal classical records remain indistinguishable')
                        require(real(trace(mul(kron(P,sigma),t)))==pp,'Direct joint Born rule');joint_controls+=1
                        require(prob(e,mul(mul(diagonal(1,-1),P),diagonal(1,-1)))==pp,'Fixed readout blind to inserted diagonal phase')
                        rows.append({'rotation_i':i,'rotation_j':j,'middle_gate':gn,'pointer_state':sn,'pointer_effect':en,'effect_diagonal':vals,'prob_plus':pp,'prob_minus':pm})
    dump('controlled_effects.json',{'joint_unitaries':unitaries,'direct_joint_controls':joint_controls,'cases':rows,
         'scope':'Finite joint-system controls of the general decomposable-coupling theorem; no continuous CST quadrature.'})

    feedback=[];nonzero=0
    for i,ri in enumerate(rotations):
        for j,rj in enumerate(rotations):
            total=zeros(2);branches=[]
            for y in range(2):
                k1=diagonal(ri[y][0],rj[y][0])
                r2a,r2c=(rj,ri) if y==0 else (rotations[(i+1)%len(rotations)],rotations[(j+2)%len(rotations)])
                for z in range(2):
                    k2=diagonal(r2a[z][0],r2c[z][0]);k=mul(k2,k1)
                    e=mul(dag(k),k);total=add(total,e)
                    state=mul(mul(k,mixed),dag(k));p=real(trace(state))
                    require(state[0][1]==state[1][0]==C(),'No cross-block coherence from incoherent input')
                    require(prob(e,P)==prob(e,Q),'Adaptive branch cannot distinguish coherent signs')
                    if p:
                        conditioned=scale(state,1/p)
                        require(trace(conditioned)==C(F(1)) and conditioned[0][1]==C(),'Valid conditioning preserves zero coherence');nonzero+=1
                        require(prob(P,conditioned)<=F(1,2),'Conditioned target fidelity at most one half')
                    branches.append({'first':y,'second':z,'probability_from_mixed':p,'effect_diagonal':[real(e[0][0]),real(e[1][1])]})
            require(total==I,'Adaptive instrument complete')
            feedback.append({'rotation_i':i,'rotation_j':j,'branches':branches})
    dump('feedback_preparation.json',{'instruments':feedback,'nonzero_conditioned_branches':nonzero,'claim':'Record-preserving instruments and postselection cannot create atom/continuous cross-block coherence from a block-diagonal input.'})

    diagonal_bounds=[]
    for a in map(F,plan['diagonal_effect_grid']):
        for b in map(F,plan['diagonal_effect_grid']):
            e=diagonal(a,b);q=prob(e,P)
            lower=max(q,1-q);require(lower>=F(1,2),'Balanced-state minimax bound')
            center=abs((a+b-1)/2);radius2=((a-b)**2+1)/4
            require(radius2>=F(1,4),'Exact spectral lower bound')
            rad=sqrt_interval(radius2)
            diagonal_bounds.append({'diagonal':[a,b],'witness_lower_bound':lower,'operator_norm_interval':[center+rad[0],center+rad[1]]})
    half=scale(I,F(1,2));diff=add(half,scale(P,-1))
    require(mul(diff,diff)==scale(I,F(1,4)),'One-half bound is attained')
    weighted=[]
    for s0,s1 in (map(F,row) for row in plan['transport_scales']):
        u=diagonal(s0,s1);ui=diagonal(1/s0,1/s1);g=mul(dag(u),u);gi=mul(ui,dag(ui))
        pt=mul(mul(ui,P),u);dt=add(half,scale(pt,-1))
        require(mul(mul(gi,dag(pt)),g)==pt,'Weighted target adjoint')
        require(mul(dt,dt)==scale(I,F(1,4)),'Representation-independent obstruction')
        weighted.append({'scales':[s0,s1],'optimal_error':'1/2'})
    mixing=[]
    for c,s in (map(F,row) for row in plan['mixing_rotations']):
        r=rotation(c,s);require(mul(dag(r),r)==I,'Mixing rotation unitary')
        e=mul(mul(dag(r),pa),r);require(e==outer((c,s)) and mul(e,e)==e,'Rotated rank-one effect')
        err2=(1-2*c*s)/2;d=add(e,scale(P,-1));require(mul(d,d)==scale(I,err2),'Exact return-error norm squared')
        off=add(e,scale(pa,-1));require(mul(off,off)==scale(I,s*s),'Exact distance to diagonal base')
        bound=max(F(0),F(1,2)-abs(s));require(err2>=bound*bound,'Necessary mixing-distance bound')
        mixing.append({'cos':c,'sin':s,'target_error_squared':err2,'target_error_interval':sqrt_interval(err2),'effect_change_from_diagonal':abs(s),'success_plus':prob(e,P),'success_minus':prob(e,Q)})
    numerator=matrix([[1,1],[-1,1]])
    require(mul(dag(numerator),numerator)==scale(I,2),'Ideal pi/4 rotation normalization')
    ideal=scale(mul(mul(dag(numerator),pa),numerator),F(1,2))
    require(ideal==P,'Off-diagonal history mixing realizes target in 2D only')
    bad=blocks(P,matrix([[1]]));target=blocks(P,matrix([[0]]));leak=outer((0,0,1))
    require(mul(bad,bad)==bad and mul(target,target)==target,'Embedding effects valid')
    require([[bad[i][j] for j in range(2)] for i in range(2)]==P,'Compressed target agrees')
    require(prob(bad,leak)-prob(target,leak)==1,'Full-space leakage error is one')
    budgets=[{'gamma':F(x),'necessary_tau_lower':max(F(0),F(1,2)-F(x))} for x in plan['mixing_budgets']]
    tolerances=[{'tau':F(x),'necessary_gamma_lower':max(F(0),F(1,2)-F(x))} for x in plan['target_tolerances']]
    dump('obstruction_and_mixing.json',{'diagonal_grid':diagonal_bounds,'optimal_diagonal_error':'1/2',
         'weighted_controls':weighted,'mixing_cases':mixing,'ideal_2d_mixing':{'effect':'P_plus','integrated_generator_norm':'pi/4','status':'ALGEBRAIC_CONTROL_NOT_CST_COUPLING'},
         'leakage_counterexample':{'compressed_error':'0','full_space_error':'1'},
         'diagnostic_mixing_budgets':budgets,'necessary_resources':tolerances,
         'bound':'For bounded V and the stated common apparatus, gamma=integral ||V(t)||dt/hbar gives tau >= max(0,1/2-gamma). Necessary, not sufficient or an optimized speed limit.'})

    negative=[]
    def reject(name,fn):
        try:fn()
        except RuntimeError:negative.append({'case':name,'status':'REJECTED'});return
        raise RuntimeError('Negative case not rejected: '+name)
    reject('record-diagonal effect equals coherent target',lambda:require(half==P,'Off-diagonal target'))
    reject('noncommuting pointer controls create history mixing',lambda:require(any(x['prob_plus']!=x['prob_minus'] for x in rows if x['middle_gate']!='identity'),'No history mixing'))
    reject('postselection creates coherence from block-diagonal state',lambda:require(state[0][1]!=C(),'Zero cross coherence'))
    reject('compressed success certifies full-space rank-one effect',lambda:require(bad==target,'Leakage sector'))
    reject('missing normalization in ideal rotation',lambda:require(mul(dag(numerator),numerator)==I,'Factor two'))
    reject('extend the diagonal obstruction to all quantum couplings',lambda:require(prob(ideal,P)==prob(ideal,Q),'Mixing control escapes restricted class'))
    reject('changed source byte',lambda:require(gitsha((ROOT/'inputs/previous_core.py').read_bytes()+b' ')==prov['inputs']['inputs/previous_core.py']['git_blob'],'Source changed'))
    result={'status':'PASS_RESTRICTED_COUPLING_AUDIT','plan_sha256':ph,'joint_unitaries':unitaries,
       'controlled_pointer_cases':len(rows),'direct_joint_controls':joint_controls,'adaptive_instruments':len(feedback),
       'adaptive_branches':4*len(feedback),'nonzero_conditioned_branches':nonzero,'diagonal_grid_cases':len(diagonal_bounds),
       'weighted_obstruction_controls':len(weighted),'rational_mixing_controls':len(mixing),'negative_controls':negative,
       'candidate_record_preserving_return_detector':'RULED_OUT_AS_UNIVERSAL_TARGET_WITH_ERROR_BELOW_1_2',
       'physical_mixing_coupling':'NOT_DERIVED','physical_gates':plan['physical_gates'],'n5_production_run':False,'external_replication':False}
    dump('verification.json',result);return result

if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
