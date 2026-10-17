"""Separate generator, geometric/LIS reference, regression and bootstrap check.

All paths remain internal to this research process; not external replication.
"""
from bisect import bisect_right
from collections import Counter
from fractions import Fraction
import hashlib
import json
import math
import numpy as np
from proper_common import HERE, MODELS, NS, coverage, packet, readz, save
from proper_core import predict, require


class Replay:
    def __init__(self, *parts):
        self.prefix = json.dumps(['x6-matching-geometry-v1', *parts], separators=(',', ':'))
        self.counter = 0

    def word(self):
        value = int(hashlib.sha256((self.prefix+':'+str(self.counter)).encode()).hexdigest()[:16], 16)
        self.counter += 1
        return value

    def unit(self):
        return ((self.word() // 4096)+0.5)/4503599627370496

    def below(self, n):
        end = 18446744073709551616 - (18446744073709551616 % n)
        value = self.word()
        while value >= end:
            value = self.word()
        return value % n


def replay(family, m, split, draw, namespace=NS):
    rng = Replay(namespace, family, m, split, draw)
    for attempts in range(1,10001):
        a,b,c,d = [rng.unit() for _ in range(4)]
        if a < c and b < d:
            break
    else:
        raise ValueError('reference endpoint cap')
    xy = [[a,b],[c,d]]
    if family == 'uniform':
        for _ in range(m):
            xy.append([rng.unit(),rng.unit()])
    else:
        s = 2*math.isqrt(m)
        sites = list(range(s*s))
        for k in reversed(range(1,len(sites))):
            j = rng.below(k+1)
            sites[k],sites[j] = sites[j],sites[k]
        for site in sites[:m]:
            u,v = divmod(site,s)
            xy.append([(u+0.5+0.4*(rng.unit()-0.5))/s,(v+0.5+0.4*(rng.unit()-0.5))/s])
    return xy,attempts


def lis_height(xy):
    tails = []
    for u,v in sorted(xy):
        k = bisect_right(tails,v)
        if k == len(tails):
            tails.append(v)
        else:
            tails[k] = v
    return len(tails)


def geometry_oracle(xy, marks):
    x = np.asarray(xy)
    t, space = (x[:,0]+x[:,1])/2, (x[:,0]-x[:,1])/2
    dt, dx = t[None,:]-t[:,None], space[None,:]-space[:,None]
    c = (dt > 0) & (dt >= np.abs(dx))
    # Resolve only numerically marginal cone boundaries by exact float rationals.
    uncertain = (np.abs(dt-np.abs(dx)) <= 2e-15) & ~np.eye(len(x),dtype=bool)
    for i,j in zip(*np.where(uncertain)):
        du = Fraction(xy[j][0])-Fraction(xy[i][0])
        dv = Fraction(xy[j][1])-Fraction(xy[i][1])
        c[i,j] = du >= 0 and dv >= 0 and (du > 0 or dv > 0)
    p,q = marks
    inside = [xy[i] for i in range(len(xy)) if i not in marks and
              xy[p][0] <= xy[i][0] <= xy[q][0] and xy[p][1] <= xy[i][1] <= xy[q][1]]
    f = dict(N=len(xy),m=len(xy)-2,R=int(c.sum()),H=lis_height(xy),K=len(inside),ell=lis_height(inside))
    return [''.join(map(str,row.astype(int))) for row in c],f,float(dt[p,q]**2-dx[p,q]**2)


def independent_matching(records,cfg):
    result = {}
    for m in cfg['sampling']['m_values']:
        subset = [r for r in records if r['m']==m and r['split']=='test']
        strata_keys = sorted({(r['features']['R'],r['features']['H']) for r in subset})
        pools = {}
        for r in sorted(subset,key=lambda r:r['draw']):
            f=r['features']; k=(f['R'],f['H'],r['family'])
            pools.setdefault(k,[]).append(r['id'])
        pairs,strata=[],[]
        for R,H in strata_keys:
            aa=pools.get((R,H,'uniform'),[]); bb=pools.get((R,H,'jittered_grid'),[])
            strata.append(dict(R=R,H=H,uniform=len(aa),jittered_grid=len(bb)))
            for k in range(min(len(aa),len(bb))):
                ids=[aa[k],bb[k]]
                serial=json.dumps([NS,'match',m,*ids],separators=(',',':'))
                pairs.append(dict(ids=ids,R=R,H=H,priority=hashlib.sha256(serial.encode()).hexdigest()))
        pairs=sorted(pairs,key=lambda p:(p['priority'],p['ids']))
        cap=cfg['matched_transfer']['minimum_pairs']
        result[str(m)]=dict(m=m,N=m+2,eligible=len(pairs),required=cap,
                           status='EVALUABLE' if len(pairs)>=cap else 'INSUFFICIENT_COMMON_SUPPORT',
                           all_eligible_pairs=pairs,selected_pairs=pairs[:cap] if len(pairs)>=cap else [],strata=strata)
    return result


def near(a,b,path=''):
    if isinstance(a,dict):
        require(isinstance(b,dict) and a.keys()==b.keys(),'keys '+path)
        for k in a:
            near(a[k],b[k],path+'/'+k)
    elif isinstance(a,list):
        require(isinstance(b,list) and len(a)==len(b),'length '+path)
        for i,(x,y) in enumerate(zip(a,b)):
            near(x,y,path+'/'+str(i))
    elif type(a) is float or type(b) is float:
        require(type(a) in (float,int) and type(b) in (float,int) and math.isfinite(a) and math.isfinite(b)
                and math.isclose(a,b,abs_tol=1e-10,rel_tol=1e-9),'numeric '+path)
    else:
        require(a==b,'exact '+path)


def quantiles(values):
    s=sorted(values)
    out=[]
    for p in [0.025,0.975]:
        position=(len(s)-1)*p
        i=math.floor(position); frac=position-i
        out.append(float(s[i]+frac*(s[min(i+1,len(s)-1)]-s[i])))
    return out


def independent_metrics(records,indices):
    # A separate loss table and reduction order from the vectorized producer.
    errors=np.asarray([[r['predictions']['clipped'][model]-r['theta'] for model in MODELS] for r in records])
    squares=errors**2
    boot_sq=np.empty((len(indices),len(MODELS)))
    boot_abs=np.empty_like(boot_sq); boot_bias=np.empty_like(boot_sq)
    for k,idx in enumerate(indices):
        boot_sq[k]=np.sum(squares[idx],axis=0)/len(records)
        boot_abs[k]=np.sum(np.abs(errors[idx]),axis=0)/len(records)
        boot_bias[k]=np.sum(errors[idx],axis=0)/len(records)
    methods={}
    for j,model in enumerate(MODELS):
        mse=math.fsum(squares[:,j])/len(records)
        methods[model]=dict(count=len(records),mse=mse,rmse=math.sqrt(mse),mae=math.fsum(abs(v) for v in errors[:,j])/len(records),
          bias=math.fsum(errors[:,j])/len(records),mse_bootstrap_95=quantiles(boot_sq[:,j]),
          rmse_bootstrap_95=quantiles(np.sqrt(boot_sq[:,j])),mae_bootstrap_95=quantiles(boot_abs[:,j]),bias_bootstrap_95=quantiles(boot_bias[:,j]))
    comparisons={base:dict(mse_difference=math.fsum(squares[:,0]-squares[:,MODELS.index(base)])/len(records),
                         paired_bootstrap_95=quantiles(boot_sq[:,0]-boot_sq[:,MODELS.index(base)])) for base in ['D','C0']}
    ae=[r['features']['K']/r['m']-r['a'] for r in records]
    return dict(methods=methods,comparisons=comparisons,zero_K=sum(r['features']['K']==0 for r in records),
      squared_time=dict(bias=math.fsum(ae)/len(ae),mse=math.fsum(v*v for v in ae)/len(ae),iid_uniform_analytic_mse=1/(12*records[0]['m'])),
      scope='Fixed calibration; analytic formula applies only to unselected uniform continuum model.')


def reference_indices(n,repeats,key):
    rng=Replay(*key)
    return np.array([[rng.below(n) for _ in range(n)] for _ in range(repeats)],dtype=np.int32)


def verify_summary(records,selection,report,cfg):
    repeats=cfg['evaluation']['bootstrap']['replicates']
    expected_cells={}
    for m in cfg['sampling']['m_values']:
        for family in cfg['sampling']['families']:
            rr=[r for r in records if r['m']==m and r['family']==family and r['split']=='test']
            ix=reference_indices(len(rr),repeats,[NS,'bootstrap',family,m])
            expected_cells[f'{family}/m{m}']=independent_metrics(rr,ix)
    near(expected_cells,report['cells'],'all unselected outcomes')
    primary=expected_cells['uniform/m256']; v=primary['methods']['V']
    gates=dict(rmse_at_most_005=v['rmse']<=0.05)
    for base in ['D','C0']:
        gates['mse_reduction_'+base]=v['mse']<=0.90*primary['methods'][base]['mse']
        gates['bootstrap_upper_negative_'+base]=primary['comparisons'][base]['paired_bootstrap_95'][1]<0
    expected=dict(status='QUALIFIED_IN_DECLARED_MODEL' if all(gates.values()) else 'NO_QUALIFICATION_DEMONSTRATED',
                  family='uniform',m=256,gates=gates,integrity_required=True)
    require(report['primary']==expected,'all primary gates')
    lookup={r['id']:r for r in records}
    matched={}
    for key,cell in selection.items():
        if cell['status']!='EVALUABLE':
            matched[key]=dict(status=cell['status'],eligible=cell['eligible'])
            continue
        uu=[lookup[p['ids'][0]] for p in cell['selected_pairs']]
        jj=[lookup[p['ids'][1]] for p in cell['selected_pairs']]
        ix=reference_indices(len(uu),repeats,[NS,'matched-bootstrap',cell['m']])
        first,second=independent_metrics(uu,ix),independent_metrics(jj,ix)
        transfer={}
        for model in MODELS:
            delta=[(b['predictions']['clipped'][model]-b['theta'])**2-(a['predictions']['clipped'][model]-a['theta'])**2 for a,b in zip(uu,jj)]
            bs=[math.fsum(delta[i] for i in row)/len(row) for row in ix]
            transfer[model]=dict(jittered_minus_uniform_mse=math.fsum(delta)/len(delta),paired_bootstrap_95=quantiles(bs))
        matched[key]=dict(status='EVALUABLE',pairs=len(uu),uniform=first,jittered_grid=second,transfer=transfer)
    near(matched,report['matched'],'all matched outcomes')
    require(report['repeats']==repeats and set(report)=={'primary','cells','matched','repeats','caveat'},'summary coverage')


def run(directory):
    cfg=json.loads((HERE/'contract.json').read_text())
    records=readz(directory/'records.json.gz')
    coverage(records,cfg)
    models=json.loads((directory/'models.json').read_text())
    relabel_count=0; maximum_coordinate_error=0.0
    for r in records:
        xy,attempts=replay(r['family'],r['m'],r['split'],r['draw'])
        require(xy==r['coordinates'] and attempts==r['endpoint_attempts'],'complete independent generator replay')
        require(r['rng_key']==[NS,r['family'],r['m'],r['split'],r['draw']] and r['N']==r['m']+2
                and r['marks']==[0,1] and r['id']==f"{r['family']}-m{r['m']}-{r['split']}-{r['draw']:04d}",'identity and marks')
        ties={name:sum(v*(v-1)//2 for v in Counter(row[a] for row in xy).values()) for a,name in enumerate(['u_equal_pairs','v_equal_pairs'])}
        ties['duplicate_points']=len(xy)-len(set(map(tuple,xy)))
        require(ties==r['ties'] and not ties['duplicate_points'],'coordinate tie ledger')
        rows,f,a=geometry_oracle(xy,r['marks'])
        require(rows==r['relation_rows'] and f==r['features'],'full metric relation and independent LIS features')
        maximum_coordinate_error=max(maximum_coordinate_error,abs(a-r['a']))
        require(abs(a-r['a'])<=2e-14 and math.isclose(math.sqrt(max(0,a)),r['theta'],abs_tol=1e-12,rel_tol=1e-10),'coordinate target oracle')
        perm=list(reversed(range(r['N'])))
        c=r['relation_rows']
        relabel=dict(N=r['N'],marks=[perm.index(k) for k in r['marks']],relation_rows=[''.join(c[i][j] for j in perm) for i in perm])
        out=predict(relabel,models[str(r['m'])])
        require(out['features']==r['features'],'transported full features')
        near({k:out[k] for k in ['raw','clipped']},r['predictions'],'transported predictions')
        near({k:v-r['theta'] for k,v in out['clipped'].items()},r['errors'],'complete per-order errors')
        relabel_count+=1
    print('all records, relations and transported predictions checked',flush=True)
    for m in cfg['sampling']['m_values']:
        train=[r for r in records if r['m']==m and r['split']=='calibration']
        x=[]
        for r in train:
            f=r['features']; density=f['R']/(r['N']*(r['N']-1)/2); h=f['H']/r['N']
            x.append([1,density,h,density*density,density*h,h*h])
        x=np.asarray(x); y=np.asarray([r['theta'] for r in train])
        coef,resid,rank,s=np.linalg.lstsq(x,y,rcond=1e-12)
        model=models[str(m)]
        require(model['calibration_ids']==[r['id'] for r in train] and model['rank']==rank and model['N']==m+2,'calibration provenance and rank')
        require(np.allclose(coef,model['coefficients'],atol=1e-8,rtol=1e-8) and np.allclose(s,model['singular_values'],atol=1e-10,rtol=1e-10),'separate least-squares fit')
        require(model['normal_equation_residual']<=1e-8*(1+float(np.max(np.abs(x.T@y)))),'least-squares residual')
        near(model['calibration_mse'],float(np.mean((x@coef-y)**2)),'calibration mse')
    selection=readz(directory/'selection.json.gz')
    require(selection==independent_matching(records,cfg),'independent complete matching')
    for cell in selection.values():
        ids=[name for pair in cell['selected_pairs'] for name in pair['ids']]
        require(len(ids)==len(set(ids)),'no matched replacement')
    report=json.loads((directory/'summary.json').read_text())
    verify_summary(records,selection,report,cfg)
    import selftest
    toys=selftest.run()
    save(directory/'verification.json',dict(status='PASS',orders_verified=len(records),full_relation_checks=len(records),
         coordinate_oracle_max_a_error=maximum_coordinate_error,relabelings=relabel_count,predictions_verified=len(records)*4,
         independent_generator_replay=True,independent_matching=True,independent_bootstrap_reductions=True,
         toys=toys,scope='Separate formulas and RNG replay in one authoring process; not external replication.'))


if __name__=='__main__':
    from pathlib import Path
    import sys
    run(Path(sys.argv[1]))
