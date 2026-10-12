"""Finite density-matrix model; explicit conventions and no physical state repair."""
import itertools,hashlib
import numpy as np
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
PAULI={'I':I,'X':X,'Y':Y,'Z':Z}
def kron_all(xs):
 out=np.array([[1]],complex)
 for a in xs:out=np.kron(out,a)
 return out
def rho_pure(v):return np.outer(v,v.conj())
def ghz(n):
 v=np.zeros(2**n,complex);v[0]=v[-1]=1/np.sqrt(2);return rho_pure(v)
def state(name,n,seed=None):
 d=2**n
 if name=='product3':v=np.zeros(d,complex);v[0]=1;return rho_pure(v)
 if name=='bell_ab_product_c':return np.kron(ghz(2),np.diag([1.,0.]))
 if name in ['ghz3','ghz6']:return ghz(n)
 if name=='classical_ghz3':v=np.zeros(d);v[0]=v[-1]=.5;return np.diag(v).astype(complex)
 if name=='w3':
  v=np.zeros(d,complex);v[[1,2,4]]=1/np.sqrt(3);return rho_pure(v)
 if name=='bell_pairs4':return np.kron(ghz(2),ghz(2))
 if name in ['cluster_chain4','graph_cycle5']:
  edges=[(i,i+1) for i in range(n-1)]
  if name=='graph_cycle5':edges.append((n-1,0))
  bits=((np.arange(d)[:,None] >> np.arange(n-1,-1,-1)) & 1)
  parity=sum(bits[:,a]*bits[:,b] for a,b in edges)%2
  return rho_pure(((-1.)**parity).astype(complex)/np.sqrt(d))
 if name=='maximally_mixed5':return np.eye(d,dtype=complex)/d
 if name=='classical_and3':
  v=np.zeros(d);v[[0,1,4,7]]=[.275,.225,.225,.275];return np.diag(v).astype(complex)
 rng=np.random.default_rng(seed)
 if name=='haar_pure':
  v=rng.standard_normal(d)+1j*rng.standard_normal(d);return rho_pure(v/np.linalg.norm(v))
 if name=='hilbert_schmidt_mixed':
  a=rng.standard_normal((d,d))+1j*rng.standard_normal((d,d));r=a@a.conj().T;return r/np.trace(r)
 raise ValueError(name)
def inspect_density(r,tol=1e-10):
 herm=float(np.max(np.abs(r-r.conj().T)));tr=np.trace(r);ev=np.linalg.eigvalsh(r)
 return {'hermiticity_error':herm,'trace_error':float(abs(tr-1)),'min_eigenvalue':float(ev.min()),'purity':float(np.trace(r@r).real),'valid':bool(herm<=tol and abs(tr-1)<=tol and ev.min()>=-tol)}
def entropy(r):
 info=inspect_density(r)
 if not info['valid']:raise ValueError('Invalid density matrix')
 ev=np.linalg.eigvalsh(r);ev=ev[ev>0]
 return float(-np.sum(ev*np.log2(ev)))
def partial_trace(r,keep,n):
 keep=list(keep);rest=[q for q in range(n) if q not in keep]
 assert len(set(keep))==len(keep) and all(0<=q<n for q in keep)
 order=keep+rest+[q+n for q in keep]+[q+n for q in rest]
 a=r.reshape([2]*(2*n)).transpose(order).reshape(2**len(keep),2**len(rest),2**len(keep),2**len(rest))
 return np.trace(a,axis1=1,axis2=3)
def partial_transpose(r,subsystem,n):
 order=list(range(2*n))
 for q in subsystem:order[q],order[q+n]=order[q+n],order[q]
 return r.reshape([2]*(2*n)).transpose(order).reshape(r.shape)
def negativity(r,subsystem,n):return float(-np.minimum(np.linalg.eigvalsh(partial_transpose(r,subsystem,n)),0).sum())
def concurrence(r):
 ev,u=np.linalg.eigh(r);sq=(u*np.sqrt(np.maximum(ev,0)))@u.conj().T
 yy=np.kron(Y,Y);flip=yy@r.conj()@yy
 a=sq@flip@sq;a=(a+a.conj().T)/2
 roots=np.sqrt(np.maximum(np.linalg.eigvalsh(a),0))[::-1]
 return float(max(0,roots[0]-roots[1:].sum()))
def kraus(channel,p):
 if not 0<=p<=1:raise ValueError('Channel strength outside [0,1]')
 if channel=='dephase':return [np.sqrt(1-p/2)*I,np.sqrt(p/2)*Z]
 if channel=='depolarize':return [np.sqrt(1-3*p/4)*I]+[np.sqrt(p/4)*a for a in [X,Y,Z]]
 if channel=='amplitude_damp':return [np.diag([1,np.sqrt(1-p)]).astype(complex),np.array([[0,np.sqrt(p)],[0,0]],complex)]
 if channel=='identity':return [I]
 raise ValueError(channel)
def channel_all(r,channel,p,n):
 if channel=='identity':return r.copy()
 out=r.copy()
 for q in range(n):
  mats=[kron_all([k if j==q else I for j in range(n)]) for k in kraus(channel,p)]
  out=sum(k@out@k.conj().T for k in mats)
 return out
def observ(r,label):return float(np.trace(r@kron_all([PAULI[x] for x in label])).real)
def tomography_pair(r,n,i,j):
 coeff={};out=np.zeros((4,4),complex)
 for a,b in itertools.product(PAULI,repeat=2):
  lab=['I']*n;lab[i]=a;lab[j]=b;v=observ(r,''.join(lab));coeff[a+b]=v
  out+=v*np.kron(PAULI[a],PAULI[b])/4
 return out,coeff
def pair_data(r,n,tomography=False):
 singles=[partial_trace(r,[i],n) for i in range(n)];ss=[entropy(x) for x in singles]
 mi=np.zeros((n,n));neg=np.zeros((n,n));conc=np.zeros((n,n));pairs=[];min_eig=1.
 for i,j in itertools.combinations(range(n),2):
  two=partial_trace(r,[i,j],n);info=inspect_density(two)
  if not info['valid']:raise ValueError('Invalid marginal')
  min_eig=min(min_eig,info['min_eigenvalue'])
  raw_mi=ss[i]+ss[j]-entropy(two);raw_neg=negativity(two,[0],2);c=concurrence(two)
  mi[i,j]=mi[j,i]=raw_mi;neg[i,j]=neg[j,i]=raw_neg;conc[i,j]=conc[j,i]=c
  row={'i':i,'j':j,'MI_bits':raw_mi,'negativity':raw_neg,'concurrence':c,'marginal_min_eigenvalue':info['min_eigenvalue']}
  if tomography:
   tr,coeff=tomography_pair(r,n,i,j);row['tomography_error']=float(np.max(np.abs(tr-two)));row['pauli_expectations']=coeff
  pairs.append(row)
 emi=mi/2;eneg=2*neg
 for e in [emi,eneg]:
  if np.min(e)<-1e-10 or np.max(e)>1+1e-10:raise ValueError('Weight outside domain')
  np.fill_diagonal(e,1.)
 bound=max(float(emi[i,j]+emi[i,k]-ss[i]) for i,j,k in itertools.permutations(range(n),3))
 globals=[negativity(r,[i],n) for i in range(n)]
 return {'single_entropies_bits':ss,'pair_min_eigenvalue':min_eig,'pairs':pairs,'E_MI':emi,'E_NEG':eneg,'concurrence_matrix':conc,'weak_monotonicity_max_excess':bound,'one_vs_rest_negativity':globals}
def raw_distances(e,zero=1e-12):
 if np.min(e)<-1e-10 or np.max(e)>1+1e-10:raise ValueError('Invalid weights')
 d=np.full(e.shape,np.inf);positive=e>zero;d[positive]=-np.log(np.minimum(e[positive],1))
 d[e>=1-zero]=0;np.fill_diagonal(d,0.)
 return d
def audit_extended(d):
 n=len(d);u=np.triu_indices(n,1);bad=0;inf_bad=0;maxex=0.;worst=None
 for i,j,k in itertools.permutations(range(n),3):
  lhs=d[i,j];rhs=d[i,k]+d[k,j]
  if np.isinf(lhs) and np.isfinite(rhs):bad+=1;inf_bad+=1;worst=[i,j,k]
  elif np.isfinite(lhs) and np.isfinite(rhs):
   ex=float(lhs-rhs)
   if ex>1e-12+1e-12*max(lhs,rhs):bad+=1
   if ex>maxex:maxex=ex;worst=[i,j,k]
 zero=int(np.sum(d[u]==0));unresolved=int(np.isinf(d[u]).sum());total=n*(n-1)*(n-2)
 status='triangle_failed' if bad else ('extended_pseudometric' if unresolved and zero else ('extended_metric' if unresolved else ('finite_pseudometric' if zero else 'finite_metric')))
 return dict(status=status,violations=bad,infinite_lhs_finite_rhs=inf_bad,zero_pairs=zero,unresolved_pairs=unresolved,legacy_score=1-bad/n**3,pass_fraction=1-bad/total,max_finite_excess=maxex,worst=worst)
def geometry(e,zero=1e-12):
 d=raw_distances(e,zero);path=d.copy();n=len(d)
 for k in range(n):path=np.minimum(path,path[:,k,None]+path[None,k,:])
 u=np.triu_indices(n,1);both=np.isfinite(d[u])&np.isfinite(path[u]);shortened=int(np.sum(d[u][both]-path[u][both]>1e-10))
 reached=int(np.sum(np.isinf(d[u])&np.isfinite(path[u])))
 components=len({tuple(np.flatnonzero(np.isfinite(path[i]))) for i in range(n)})
 return {'raw':audit_extended(d),'path':audit_extended(path),'shortened_finite_pairs':shortened,'newly_finite_pairs':reached,'components':components},d,path
def digest(a):return hashlib.sha256(np.ascontiguousarray(a,dtype='<c16').tobytes()).hexdigest()
