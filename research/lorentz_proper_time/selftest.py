"""Deterministic/small toy checks only; never uses target sizes or namespace."""
import copy
import json
import math
from itertools import permutations
import numpy as np
import check_design
from proper_common import HERE, NS, coverage, matching, packet, sample
from proper_core import features, fit_D, predict, require
from proper_analysis import metrics, primary_decision, resamples
from check import geometry_oracle, independent_matching, independent_metrics, near, replay


def run():
    design=check_design.run()
    ex=json.loads((HERE/'design_examples.json').read_text())
    for name in ['A','B','antichain']:
        xy=[[float(v) for v in p] for p in check_design.points(ex[name])]
        rows,expected,_=geometry_oracle(xy,ex[name]['marks'])
        pkt=dict(N=len(xy),marks=ex[name]['marks'],relation_rows=rows)
        require(features(pkt)==expected,'toy full interval features')
    # Empty strict interval while retaining N>2 as required by the estimator.
    xy=[[0.1,0.1],[0.2,0.2],[0.9,0.05]]
    rows,expected,_=geometry_oracle(xy,[0,1])
    require(features(dict(N=3,marks=[0,1],relation_rows=rows))['K']==0,'empty interval retained')
    generated=[]
    for family in ['uniform','jittered_grid']:
        for draw in range(3):
            r=sample(family,4,'toy',draw,namespace=NS+'-toy-only')
            xy,attempts=replay(family,4,'toy',draw,namespace=NS+'-toy-only')
            require(xy==r['coordinates'] and attempts==r['endpoint_attempts'],'toy independent stream and sampling')
            rows,f,a=geometry_oracle(xy,[0,1])
            require(rows==r['relation_rows'] and features(packet(r))==f,'toy metric and chain oracle')
            generated.append(r)
    calibration=[dict(split='calibration',packet=packet(r),theta=r['theta']) for r in generated[:3]]
    model=fit_D(calibration)
    r=generated[-1]; original=predict(packet(r),model)
    poisoned=copy.deepcopy(r)
    poisoned.update(theta=0.99,a=0.9801,coordinates=[[999,999]]*r['N'],family='poison',id='poison',rng_key=['poison'])
    require(predict(packet(poisoned),model)==original,'coordinate target family identity poison cannot affect inference')
    rejected=[]
    def rejects(name,fn):
        try:
            fn()
        except ValueError:
            rejected.append(name)
        else:
            raise ValueError('negative control failed '+name)
    for forbidden in ['coordinates','theta','a','rng_key','family','id']:
        bad={**packet(r),forbidden:poisoned[forbidden]}
        rejects('forbidden '+forbidden,lambda bad=bad: predict(bad,model))
    rejects('full record at inference',lambda:predict(r,model))
    bad=copy.deepcopy(calibration); bad[-1]['split']='test'
    rejects('test split in calibration',lambda:fit_D(bad))
    extra=copy.deepcopy(calibration); extra[0]['coordinates']=[]
    rejects('extra calibration metadata',lambda:fit_D(extra))
    badpacket=packet(r); badpacket['marks']=[-1,1]
    rejects('negative mark alias',lambda:predict(badpacket,model))
    badorder=dict(N=3,marks=[0,1],relation_rows=['010','001','000'])
    rejects('nontransitive order',lambda:features(badorder))
    # Regression calibration is a function only of the explicit training list.
    require(fit_D(calibration)==model,'test poison cannot mutate calibration fit')
    swaps=0
    for perm in permutations(range(4)):
        rows=ex['shared']['relation_rows']
        pkt=dict(N=4,marks=[perm.index(0),perm.index(3)],relation_rows=[''.join(rows[i][j] for j in perm) for i in perm])
        require(features(pkt)==dict(N=4,m=2,R=6,H=4,K=2,ell=2),'all toy marked relabelings')
        swaps+=1
    cfg={'sampling':{'m_values':[4],'families':['uniform','jittered_grid'],'calibration':{'uniform_per_m':0,'jittered_grid_per_m':0},'test_per_family_m':4},
         'matched_transfer':{'minimum_pairs':4}}
    fake=[]
    for family in cfg['sampling']['families']:
        for draw in range(4):
            fake.append(dict(id=f'{family}-{draw}',family=family,m=4,split='test',draw=draw,
                             features=dict(R=draw+4,H=2,K=0,ell=0),theta=0.1*draw))
    coverage(fake,cfg)
    selected=matching(fake,cfg)
    require(selected==independent_matching(fake,cfg) and selected['4']['status']=='EVALUABLE','exact toy matching')
    poison=copy.deepcopy(fake)
    for row in poison:
        row['features']['K']=999; row['features']['ell']=999; row['theta']=float('nan'); row['coordinates']=['poison']
    require(matching(poison,cfg)==selected,'selection excludes target and local geometric features')
    require(matching(fake[:-1],cfg)['4']['status']=='INSUFFICIENT_COMMON_SUPPORT','support failure is explicit')
    rejects('missing cohort member',lambda:coverage(fake[:-1],cfg))
    rejects('reordered cohort',lambda:coverage(list(reversed(fake)),cfg))
    rr=[]
    for i in range(4):
        rr.append(dict(theta=0.1*(i+1),a=(0.1*(i+1))**2,m=4,features=dict(K=i),
                       predictions=dict(clipped=dict(V=0.1*i,L=0.2*i,C0=64/225,D=0.25))))
    indices=resamples(4,20,[NS+'-toy','bootstrap'])
    near(metrics(rr,indices),independent_metrics(rr,indices),'toy bootstrap oracle')
    cell=dict(methods={'V':dict(rmse=0.05,mse=0.0025),'D':dict(mse=0.01),'C0':dict(mse=0.02)},
              comparisons={base:dict(paired_bootstrap_95=[-0.02,-0.001]) for base in ['D','C0']})
    require(primary_decision(cell)['status']=='QUALIFIED_IN_DECLARED_MODEL','known qualification gates')
    cell['comparisons']['D']['paired_bootstrap_95'][1]=0.0
    require(primary_decision(cell)['status']=='NO_QUALIFICATION_DEMONSTRATED','zero CI boundary fails')
    return dict(status='PASS_TOY_ONLY',target_samples_generated=0,design=design,small_generator_draws=6,
                new_relabelings=swaps,rejected_controls=rejected,poison_checks=True,bootstrap_oracle=True)


if __name__=='__main__':
    print(json.dumps(run(),indent=2))
