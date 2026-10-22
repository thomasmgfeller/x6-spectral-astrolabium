"""Fixed-budget archived-data search for close-count/different-operator pairs.
SPDX-License-Identifier: Apache-2.0
"""
import hashlib,json,platform,resource,signal,time
import numpy as np
import scipy
from scipy.optimize import minimize
from st_common import HERE,PRIOR,read,save,encode,frozen,estimate
from st_model import Stability

def main():
    frozen();c=read(HERE/'contract.json');begin=time.monotonic();records=[]
    def timeout(*_):raise TimeoutError('fixed campaign budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(c['worker_seconds'])
    for index in c['indices']:
        start=time.monotonic();path=PRIOR/f'results/cloud-{index:02d}.json.gz';r=read(path)
        p=r['selection']['arms']['candidate']['packet'];obs=r['replicates'][0]['arms']['candidate']['observed']
        base=estimate(p,obs['counts'],obs['overlaps'],c['rho'],c['fit'],'full_gls')
        out=dict(index=index,source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),base=base,trials=[],status='BASE_HOLD')
        if base.get('qualified',False):
            m=Stability(p,obs['counts'],obs['overlaps'],c['rho'],c['fit']);x0=m.pack(np.array(base['coordinates']));mu0,J=m.means(x0)
            w0,W=m.weights(x0);A=np.linalg.solve(m.L,J);U,s,Vt=np.linalg.svd(A,full_matrices=False)
            rank=int(np.sum(s>1e-10*s[0]));P=(Vt.T/s)@U.T;G=W@P;uw,gain,vg=np.linalg.svd(G,full_matrices=False)
            residual0=float((mu0-m.counts)@m.precision@(mu0-m.counts));normalizer=np.linalg.norm(w0)
            out.update(status='SEARCH_COMPLETE',packet=p,observed=obs,base_weights=w0,base_squared_discrepancy=residual0,
                local=dict(rows=len(mu0),columns=len(x0),rank=rank,singular_values=s,operator_gains=gain,
                    relative_leading_gain=float(gain[0]/normalizer),scope='Unconstrained tangent sensitivity. Active order constraints may restrict these directions; no global bound.'))
            if residual0>len(mu0) or rank<len(x0):out['status']='BASE_DISCREPANCY_OR_RANK_HOLD'
            else:
                for direction in range(c['objective_directions']):
                    v=uw[:,direction]
                    for sign in c['signs']:
                        begun=time.monotonic();visited=[x0.copy()];result=None;error=None
                        def objective(x):
                            if time.monotonic()-begun>c['seconds_per_search']:raise TimeoutError('fixed objective budget')
                            try:w,dw=m.weights(x);return float(-sign*v@w/normalizer),-sign*v@dw/normalizer
                            except np.linalg.LinAlgError:return 1e20,np.zeros(len(x))
                        def constraints(x):
                            cc,cj=m.constraints(x);ss,ds,_=m.interval(x,m.a,m.b);q=np.maximum(-ss,1e-12)
                            mu=m.factor*q**1.5;J=-1.5*m.factor*np.sqrt(q)[:,None]*ds;J[-ss<=1e-12]=0
                            delta=mu-mu0;res=mu-m.counts;Pdelta=m.precision@delta;Pres=m.precision@res
                            return np.r_[cc,c['pair_discrepancy_limit']**2-delta@Pdelta,len(mu)-res@Pres],np.vstack((cj,-2*Pdelta@J,-2*Pres@J))
                        try:
                            result=minimize(objective,x0,jac=True,method='SLSQP',bounds=[(-c['coordinate_bound'],c['coordinate_bound'])]*len(x0),
                                constraints=[dict(type='ineq',fun=lambda x:constraints(x)[0],jac=lambda x:constraints(x)[1])],
                                callback=lambda x:visited.append(x.copy()),options=dict(maxiter=c['max_iterations'],ftol=1e-10))
                            visited.append(result.x.copy())
                        except (TimeoutError,ValueError,np.linalg.LinAlgError) as exc:error=repr(exc)
                        trial=dict(direction=direction,sign=sign,seconds=time.monotonic()-begun,error=error,
                            optimizer_success=bool(result.success) if result is not None else False,
                            optimizer_message=str(result.message) if result is not None else None,visited=len(visited),status='NO_QUALIFIED_PAIR')
                        candidates=[]
                        # Inspect only the last point and the best visited objective, then fixed backtracking.
                        scored=[]
                        for k,x in enumerate(visited):
                            try:scored.append((float(sign*v@m.weights(x,False)),k))
                            except np.linalg.LinAlgError:pass
                        picks=sorted(set([len(visited)-1,max(scored)[1] if scored else 0]))
                        for k in picks:
                            for step in range(c['backtrack_steps']):
                                fraction=.999*2.**(-step);z=np.round(m.unpack(x0+fraction*(visited[k]-x0)),c['round_coordinate_digits']);x=m.pack(z)
                                zbase=np.round(m.unpack(x0),c['round_coordinate_digits']);xb=m.pack(zbase)
                                try:
                                    f=m.gate(x);fb=m.gate(xb);mu,_=m.means(x);mub,_=m.means(xb);w=m.weights(x,False);wb=m.weights(xb,False)
                                    delta=mu-mub;pair=float(delta@m.precision@delta);res=mu-m.counts;rb=mub-m.counts
                                    observed=float(res@m.precision@res);observed_base=float(rb@m.precision@rb)
                                    separation=float(np.linalg.norm(w-wb));relative=separation/(.5*(np.linalg.norm(w)+np.linalg.norm(wb)))
                                    if pair>c['pair_discrepancy_limit']**2-1e-7 or max(observed,observed_base)>len(mu)-1e-7:continue
                                    candidates.append(dict(coordinates=[zbase,z],weights=[wb,w],squared_pair_discrepancy=pair,
                                        squared_observed_discrepancies=[observed_base,observed],relative_weight_separation=relative,
                                        weight_separation=separation,maximum_marginal_mean_shift=float(np.max(abs(delta)/np.sqrt(m.counts))),
                                        backtrack_fraction=fraction,visited_index=k,conditions=[fb['certificate']['condition'],f['certificate']['condition']]))
                                except (ValueError,np.linalg.LinAlgError):continue
                        if candidates:
                            best=max(candidates,key=lambda v:v['relative_weight_separation']);trial.update(best=best,status='STRONG_PAIR' if best['relative_weight_separation']>=c['minimum_relative_weight_separation'] else 'SMALL_PAIR')
                        out['trials'].append(trial)
        out['seconds']=time.monotonic()-start;save(HERE/f'results/cloud-{index:02d}.json.gz',out)
        rec=dict(index=index,status=out['status'],base_status=base['status'],seconds=out['seconds'],strong_pairs=sum(t['status']=='STRONG_PAIR' for t in out['trials']),
            maximum_relative_separation=max([t['best']['relative_weight_separation'] for t in out['trials'] if 'best' in t],default=None))
        records.append(rec);print(json.dumps(rec),flush=True)
    signal.alarm(0)
    save(HERE/'execution.json',dict(status='COMPLETE',seconds=time.monotonic()-begin,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,records=records,
        versions=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__)))

if __name__=='__main__':main()
