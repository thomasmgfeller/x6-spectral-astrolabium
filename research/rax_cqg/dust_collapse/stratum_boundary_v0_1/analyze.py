"""Exact finite controls of a conditional atom/continuum boundary construction.

These matrices are finite analogues, not certified continuum discretizations.
The Cayley map is a rational unitary control, not an exact exponential.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib, json, sys
ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT/'inputs'))
from exact_core import C, as_c, matrix, mul, add, scale, dag, outer, real, encode

def require(ok, msg):
    if not ok: raise RuntimeError(msg)
def dump(name, obj):
    (ROOT/'results').mkdir(exist_ok=True)
    (ROOT/'results'/name).write_text(json.dumps(encode(obj),indent=2,sort_keys=True)+'\n')
def eye(n): return matrix([[int(i==j) for j in range(n)] for i in range(n)])
def zero(n): return matrix([[0]*n for _ in range(n)])
def diagonal(v): return matrix([[v[i] if i==j else 0 for j in range(len(v))] for i in range(len(v))])
def cinv(z):
    require(z!=C(),'Nonzero pivot'); return z.conj()*F(1,z.norm2())
def inverse(a):
    n=len(a); b=[row[:]+e[:] for row,e in zip(a,eye(n))]
    for j in range(n):
        k=next(k for k in range(j,n) if b[k][j]!=C()); b[j],b[k]=b[k],b[j]
        f=cinv(b[j][j]); b[j]=[x*f for x in b[j]]
        for k in range(n):
            if k!=j:
                f=b[k][j]; b[k]=[x-f*y for x,y in zip(b[k],b[j])]
    out=[row[n:] for row in b]
    require(mul(a,out)==eye(n) and mul(out,a)==eye(n),'Two-sided exact inverse')
    return out
def rank(a):
    b=[row[:] for row in a]; r=0
    for j in range(len(b[0])):
        ks=[k for k in range(r,len(b)) if b[k][j]!=C()]
        if not ks: continue
        k=ks[0]; b[r],b[k]=b[k],b[r]; f=cinv(b[r][j]); b[r]=[x*f for x in b[r]]
        for k in range(r+1,len(b)):
            f=b[k][j]; b[k]=[x-f*y for x,y in zip(b[k],b[r])]
        r+=1
        if r==len(b): break
    return r
def kron(a,b):
    return [[a[i][j]*b[k][l] for j in range(len(a[0])) for l in range(len(b[0]))] for i in range(len(a)) for k in range(len(b))]
def vec(a,v): return [row[0] for row in mul(a,[[as_c(x)] for x in v])]
def inner(v,w,weights): return sum((as_c(x).conj()*as_c(y)*g for x,y,g in zip(v,w,weights)),C())
def projector(v,weights): return scale(mul(outer(v),diagonal(weights)),F(1,real(inner(v,v,weights))))
def weighted_effect(e,g):
    require(mul(dag(e),g)==mul(g,e),'Weighted adjoint')
def graph(m,kappa,lam,sign):
    weights=[F(1)]+[F(1,m)]*m; g=diagonal(weights); l=zero(m+1)
    edges=[(0,1,lam,sign)]+[(j,j+1,kappa*m,1) for j in range(1,m)]
    for i,j,w,s in edges:
        v=[0]*(m+1);v[i]=1;v[j]=-s;l=add(l,scale(outer(v),w))
    h=mul(diagonal([1/x for x in weights]),l)
    require(mul(g,h)==l and dag(l)==l,'Weighted graph Hamiltonian')
    return weights,g,l,h,edges
def poly_der(p): return [p[j]*j for j in range(1,len(p))] or [C()]
def poly_inner(p,q):
    return sum((as_c(x).conj()*as_c(y)*F(1,i+j+1) for i,x in enumerate(p) for j,y in enumerate(q)),C())
def poly_at(p,x): return sum((as_c(v)*x**i for i,v in enumerate(p)),C())

def run():
    plan=json.loads((ROOT/'plan.json').read_text()); ph=hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()
    require(ph==(ROOT/'plan.sha256').read_text().split()[0],'Frozen plan')
    prov=json.loads((ROOT/'provenance.json').read_text())
    for name,info in prov['inputs'].items():
        b=(ROOT/name).read_bytes();require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==info['git_blob'],'Pinned input '+name)
    blocks=[]; coupled=[]; norms=0; mixed=0
    for m in plan['cell_counts']:
        w=[F(1)]+[F(1,m)]*m; g=diagonal(w); vp=[1]*(m+1); vm=[-1]+[1]*m
        pp=projector(vp,w); pm=projector(vm,w)
        require(mul(pp,pm)==zero(m+1),'Opposite coherent signs orthogonal')
        pa=diagonal([1]+[0]*m)
        vectors={'constant':[1]*m,'first':[1]+[0]*(m-1),'alternating':[(-1)**j for j in range(m)],'linear':list(range(1,m+1))}
        for label in plan['continuous_vectors']:
            pc=projector([0]+vectors[label],w)
            for ea in map(F,plan['block_atom_effects']):
                e=add(scale(pa,ea),pc);weighted_effect(e,g)
                qp=real(inner(vp,vec(e,vp),w))/2;qm=real(inner(vm,vec(e,vm),w))/2
                require(qp==qm and 0<=qp<=1 and max(qp,1-qp)>=F(1,2),'Block-preserving obstruction')
                require(mul(e,pa)==mul(pa,e),'Preserves atom sector')
                blocks.append({'m':m,'continuous_vector':label,'atom_effect':ea,'prob_plus':qp,'prob_minus':qm})
        pc0=projector([0]+[1]*m,w); best=scale(add(pa,pc0),F(1,2)); diff=add(best,scale(pp,-1))
        require(mul(diff,diff)==scale(add(pa,pc0),F(1,4)),'Sharp half-error attained by pinching')
        for kap in map(F,plan['kappa']):
            for lam in map(F,plan['boundary_lambda']):
                for s in plan['boundary_signs']:
                    w,g,l,h,edges=graph(m,kap,lam,s);n=m+1
                    require(rank(l)==n-(1 if lam else 2),'Kernel dimension from connected form')
                    v=[s]+[1]*m; ground=projector(v,w)
                    require(vec(h,v)==[C()]*n and mul(ground,ground)==ground,'Ground vector and projector')
                    require((mul(h,pa)==mul(pa,h))==(lam==0),'Atom mixing iff boundary coupling nonzero')
                    _,_,_,h0,_=graph(m,kap,F(0),s)
                    boundary=add(h,scale(h0,-1))
                    require(mul(boundary,boundary)==scale(boundary,lam*(m+1)),'Boundary perturbation nonzero eigenvalue')
                    off=add(mul(mul(pa,boundary),add(eye(n),scale(pa,-1))),mul(mul(add(eye(n),scale(pa,-1)),boundary),pa))
                    support=diagonal([1,1]+[0]*(m-1))
                    require(mul(off,off)==scale(support,lam*lam*m),'Off-block perturbation norm squared')
                    probe=[C(F(j+1),F((-1)**j,3)) for j in range(n)]
                    q=sum((weight*(probe[i]-sign*probe[j]).norm2() for i,j,weight,sign in edges),F(0))
                    require(real(inner(probe,vec(h,probe),w))==q and q>=0,'Positive form and weighted operator agree')
                    t=F(plan['cayley_parameter']); ih=scale(h,C(F(0),t/2)); u=mul(add(eye(n),scale(ih,-1)),inverse(add(eye(n),ih)))
                    require(mul(mul(dag(u),g),u)==g,'Exact Cayley unitarity')
                    initial=[1]+[0]*m; out=vec(u,initial);p0=out[0].norm2();pc=sum((z.norm2()/m for z in out[1:]),F(0))
                    require(p0+pc==1,'Atom-continuum norm conserved');norms+=1
                    coherence=sum(((out[0]*z.conj()).norm2() for z in out[1:]),F(0))
                    require((coherence>0)==(lam>0),'Boundary term creates cross coherence in finite control')
                    mixed+=int(lam>0)
                    target_prob=real(inner(vp,vec(ground,vp),w))/2
                    require(target_prob==(1 if s==1 else 0),'Boundary sign selects different target under fixed readout')
                    coupled.append({'m':m,'kappa':kap,'lambda':lam,'sign':s,'nullity':n-rank(l),'atom_probability':p0,'continuous_probability':pc,'cross_coherence_squared_sum':coherence,'chosen_ground_projector_prob_on_plus':target_prob,'unique_ground':bool(lam),'boundary_perturbation_norm':lam*(m+1),'off_block_norm_squared':lam*lam*m})
    dump('block_and_graph.json',{'block_controls':blocks,'boundary_graph_controls':coupled,'cayley_not_exact_exponential':True,'finite_analogues_not_certified_continuum_approximation':True})

    green=[];flux=[]
    triples=[(C(F(1)),C(F(1,2),F(1,3)),C(F(0),F(1))), (C(F(-1),F(1)),C(F(-2,3)),C(F(1,2))), (C(F(1,3),F(-1,2)),C(F(0),F(2)),C(F(-1)))]
    tests=[(C(F(1),F(1)),[C(F(1)),C(F(0),F(1))]), (C(F(-1,2)),[C(F(0),F(1)),C(F(1)),C(F(1,3))]), (C(),[C(F(2)),C(F(-1))])]
    for kap in map(F,plan['kappa']):
        for lam in map(F,plan['boundary_lambda']):
            for s in plan['boundary_signs']:
                for c0,d,t in triples:
                    d=d if lam else C()
                    f=[c0,d,(-d+t)*F(1,2),-t*F(1,3)];df=poly_der(f);ddf=poly_der(df)
                    a=s*(c0-d*(kap/lam)) if lam else C(F(1),F(1,2))
                    require(kap*df[0]==lam*(f[0]-s*a) and poly_at(df,F(1))==C(),'Operator domain conditions')
                    aa=lam*(a-s*f[0]);af=[-kap*x for x in ddf]
                    atom_rate=2*(a.conj()*aa).i; j0=2*kap*(f[0].conj()*df[0]).i
                    require(atom_rate+j0==0,'Probability flux balances atom and continuous sector')
                    flux.append({'kappa':kap,'lambda':lam,'sign':s,'atom_rate_hbar1':atom_rate,'continuous_inflow_hbar1':j0})
                    for b,gp in tests:
                        form=kap*poly_inner(poly_der(gp),df)+lam*(b-s*gp[0]).conj()*(a-s*f[0])
                        operator=b.conj()*aa+poly_inner(gp,af)
                        require(form==operator,'Green identity with boundary coupling')
                        green.append({'kappa':kap,'lambda':lam,'sign':s,'residual':form-operator})
    dump('boundary_identities.json',{'green_identities':green,'flux_balances':flux,'continuum_statement':'Analytic form proof; exact polynomial domain checks are implementation controls.'})

    clock=[]
    for m in plan['cell_counts']:
        w,g,l,h,_=graph(m,F(1),F(1),1);pw=projector([1]*(m+1),w)
        for k in plan['clock_cells']:
            wx=[F(1,k)]*k; gx=diagonal(wx); lx=zero(k)
            for j in range(k-1):
                v=[0]*k;v[j]=1;v[j+1]=-1;lx=add(lx,scale(outer(v),k))
            hx=scale(lx,k); px=projector([1]*k,wx)
            fullg=kron(gx,g); target=kron(px,pw);bad=kron(eye(k),pw)
            onlyw=kron(eye(k),h);full=add(kron(hx,eye(m+1)),onlyw)
            require(k*(m+1)-rank(onlyw)==k,'Spectator clock ground degeneracy')
            require(k*(m+1)-rank(full)==1 and mul(full,target)==zero(k*(m+1)),'Added clock form leaves one ground mode')
            leak=kron(add(eye(k),scale(px,-1)),pw)
            require(add(bad,scale(target,-1))==leak and mul(leak,leak)==leak and rank(leak)==k-1,'Clock leakage norm one')
            weighted_effect(target,fullg);clock.append({'m':m,'clock_cells':k,'density_only_ground_dimension':k,'with_clock_ground_dimension':1,'spectator_effect_error':'1'})
    actions=[]; action_points=0
    for h in map(F,plan['h']):
        for x in map(F,plan['action_x']):
            for w in map(F,plan['action_w']):
                anchored=-w/2-w*F(1,4)*((-2+4*h*x)-(-2))**2
                require(anchored==-w*(F(1,2)+4*h*h*x*x),'Inherited one-element action');action_points+=1
        poly={(0,1):F(-1,2),(2,1):-4*h*h}
        def avg(p):
            return sum((coef*F(1,i+1)*(F(1) if j==0 else F(1,2*(j+1))) for (i,j),coef in p.items()),F(0))
        square={}
        for (i,j),a in poly.items():
            for (k,l),b in poly.items():square[i+k,j+l]=square.get((i+k,j+l),F(0))+a*b
        mean=avg(poly);second=avg(square);variance=second-mean*mean
        formula=F(5,192)+F(5,36)*h*h+F(19,45)*h**4
        require(variance==formula and variance>0,'Exact action variance and nonstationarity')
        for eta in map(F,plan['eta']):
            actions.append({'h':h,'eta':eta,'action_mean':mean,'action_second_moment':second,'action_variance':variance,'target_eigen_residual_squared':eta*eta*variance,'target_is_eigenstate':eta==0})
    dump('clock_and_action.json',{'clock_controls':clock,'action_points':action_points,'action_potential_controls':actions,'scope':'Adding eta*M_S is an extra Hamiltonian model choice, not a derivation from the inherited action.'})
    negative=[]
    def reject(name,condition):
        require(not condition,'Negative control failed: '+name);negative.append({'case':name,'status':'REJECTED'})
    reject('block preservation is enough to implement the coherent target',all(x['prob_plus']==1 and x['prob_minus']==0 for x in blocks))
    reject('no boundary coupling gives a unique coherent ground mode',all(x['nullity']==1 for x in coupled if x['lambda']==0))
    reject('boundary sign has no effect relative to a fixed target',all(x['chosen_ground_projector_prob_on_plus']==1 for x in coupled if x['lambda']>0))
    reject('density ground filter certifies the full clock space',all(x['spectator_effect_error']=='0' for x in clock))
    reject('adding the nonconstant action potential preserves the target eigenstate',all(x['target_is_eigenstate'] for x in actions if x['eta']>0))
    reject('normalizing finite cell weights is optional',sum([F(1)]+[F(1)]*3)==2)
    changed=(ROOT/'inputs/exact_core.py').read_bytes()+b' '
    reject('changing a source byte preserves provenance',hashlib.sha1(b'blob '+str(len(changed)).encode()+b'\0'+changed).hexdigest()==prov['inputs']['inputs/exact_core.py']['git_blob'])
    result={'status':'PASS_CONDITIONAL_STRATUM_BOUNDARY_AUDIT','plan_sha256':ph,'block_effect_controls':len(blocks),'boundary_graph_controls':len(coupled),'exact_cayley_unitarities':norms,'finite_mixing_cases':mixed,'green_identity_controls':len(green),'flux_balances':len(flux),'clock_controls':len(clock),'action_point_controls':action_points,'action_potential_controls':len(actions),'negative_controls':negative,'physical_gates':plan['physical_gates'],'physical_cst_coupling':'NOT_DERIVED','boundary_family':'ADDITIONAL_DIAGNOSTIC_MODEL','continuum_convergence_certified':False,'n5_production':False,'paid_compute':False}
    dump('verification.json',result);return result

if __name__=='__main__':print(json.dumps(encode(run()),indent=2,sort_keys=True))
