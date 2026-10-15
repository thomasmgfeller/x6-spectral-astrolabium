#!/usr/bin/env python3
"""Executable capability attacks, actual-future noninterference, and output forgeries."""
import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'experimental/rax_guarded'))
import runner as r
import worker as w


def qualify(output):
    output.mkdir(exist_ok=False)
    cases=[]
    def reject(name,fun):
        try: fun()
        except (ValueError,TypeError,OSError,KeyError,IndexError):cases.append({'id':name,'result':'REJECTED_EXPECTED'});return
        raise ValueError('ATTACK_ACCEPTED:'+name)
    c=r.read(r.ROOT/'contract.json')
    attacks={
        'negative_observation_alias':{'if_observation':-1,'then':{'action':0},'else':{'action':1}},
        'boolean_index_alias':{'if_observation':True,'then':{'action':0},'else':{'action':1}},
        'future_observation':{'if_observation':1,'then':{'action':0},'else':{'action':1}},
        'holdout_lookup':{'holdout':0},'future_bank_lookup':{'acquisition':0},
        'callback_introspection':{'callback':'__closure__'},'python_payload':{'python':'open("holdout.json").read()'},
        'filesystem_lookup':{'read':'/proc/1/environ'},'network_lookup':{'url':'https://example.org'},
        'negative_action':{'action':-1},'boolean_action':{'action':True},'out_of_range_action':{'action':2},
        'foreign_primitive':{'choose':'load_pickle'},'covert_extra_field':{'action':0,'seed':'private'}
    }
    for name,expr in attacks.items():
        bad=copy.deepcopy(c);bad['plans'][0]['steps'][1]=expr
        reject(name,lambda bad=bad:r.validate(bad))
    bad=copy.deepcopy(c);bad['plans'][0]['steps'].append({'action':0})
    reject('budget_overrun',lambda:r.validate(bad))
    bad=copy.deepcopy(c);bad['plans'][0]['steps'][1]={'if_observation':0,'then':{'action':0},'else':{'read':'holdout'}}
    reject('forbidden_unexecuted_branch',lambda:r.validate(bad))
    deep={'action':0}
    for _ in range(10):deep={'if_observation':0,'then':deep,'else':{'action':0}}
    bad=copy.deepcopy(c);bad['plans'][0]['steps'][1]=deep
    reject('complexity_limit',lambda:r.validate(bad))
    for name,text in [('duplicate_json_key','{"action":0,"action":1}'),('nonfinite_json','{"action":NaN}')]:
        reject(name,lambda text=text:w.parse(text))
    req={'schema':'rax.public-prefix/1','model':c['model'],'plan':c['plans'][0],'history':[],'budget':c['budget']}
    bad=copy.deepcopy(req);bad['holdout']=[1]
    reject('private_data_in_request',lambda:w.respond(bad))
    bad=copy.deepcopy(req);bad['history']=[[0,True]]
    reject('boolean_outcome',lambda:w.respond(bad))
    # Attack the real subprocess entrance, not an unused holdout variable.
    p=subprocess.run([sys.executable,'-I','-S','-B',str(r.ROOT/'worker.py')],input=r.encode(dict(req,holdout=[1])),capture_output=True)
    w.require(p.returncode==2 and w.parse(p.stdout.decode())['status']=='REJECTED','PROCESS_GATE')
    cases.append({'id':'subprocess_private_payload','result':'REJECTED_EXPECTED'})
    small=copy.deepcopy(c);small['episodes']=1
    a=[[[0]*c['budget'] for _ in c['model'][0]]]
    b=copy.deepcopy(a)
    for row in b[0]:row[1:]=[1]*(len(row)-1)
    p0=r.predict(small,a);p1=r.predict(small,b)
    for x,y in zip(p0['rows'],p1['rows']):
        w.require(x['history'][0]==y['history'][0] and
                  x['history'][1][0]==y['history'][1][0],'FUTURE_ACQUISITION_LEAK')
    w.require(any(x['history']!=y['history'] for x,y in zip(p0['rows'],p1['rows'])),'INEFFECTIVE_BANK_MUTATION')
    h0=[[[0]*c['holdout_per_action'] for _ in c['model'][0]]]
    h1=[[[1]*c['holdout_per_action'] for _ in c['model'][0]]]
    score0=r.assess(small,p0,h0);score1=r.assess(small,p0,h1)
    w.require(score0!=score1 and r.predict(small,a)==p0,'INEFFECTIVE_HOLDOUT_MUTATION')
    # Known bad holdout-dependent planner is detected by the same two-world test.
    def bad_planner(holdout):return holdout[0][0][0]
    reject('deliberately_holdout_dependent_control',lambda:w.require(bad_planner(h0)==bad_planner(h1),'HOLDOUT_DEPENDENCE_DETECTED'))
    # Independent closed form for the fixed plan's all-zero prefix posterior.
    fixed=next(x for x in p0['rows'] if x['plan']=='fixed_alternating')
    w.require(fixed['prediction']==['13/24','13/24'],'EXACT_PREDICTION_REFERENCE')
    run=output/'run';r.run(r.ROOT/'contract.json',run);r.verify(run)
    reject('existing_output_directory',lambda:r.run(r.ROOT/'contract.json',run))
    def forge(name,mutation):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run';shutil.copytree(run,path)
            d=r.read(path/'predictions.json');mutation(d);(path/'predictions.json').write_bytes(r.encode(d))
            complete=r.read(path/'complete.json');complete['files']['predictions.json']=r.digest((path/'predictions.json').read_bytes());(path/'complete.json').write_bytes(r.encode(complete))
            r.verify(path)
    mutations={
        'negative_episode_rehashed':lambda d:d['rows'][0].update(episode_index=-1),
        'boolean_episode_rehashed':lambda d:d['rows'][1].update(episode_index=False),
        'duplicate_cell_rehashed':lambda d:d['rows'].append(d['rows'][0]),
        'missing_cell_rehashed':lambda d:d['rows'].pop(),
        'wrong_identity_rehashed':lambda d:d['rows'][0].update(episode_id='episode:5'),
        'holdout_tuned_prediction_rehashed':lambda d:d['rows'][0].update(prediction=['1','1']),
        'invented_future_measurement_rehashed':lambda d:d['rows'][0]['history'].append([0,1])}
    for name,mutation in mutations.items():reject(name,lambda name=name,mutation=mutation:forge(name,mutation))
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'run';shutil.copytree(run,path);(path/'complete.json').unlink()
        reject('missing_completion',lambda:r.verify(path))
    with tempfile.TemporaryDirectory() as tmp:
        path=Path(tmp)/'run';shutil.copytree(run,path);(path/'assessment.json').unlink();(path/'assessment.json').symlink_to(run.resolve()/'assessment.json')
        reject('linked_result',lambda:r.verify(path))
    result={'schema':'rax.guarded-qualification/1','status':'PASS','negative_controls':len(cases),'controls':cases,
            'actual_future_bank_mutation':'PASS_PREFIX_INVARIANCE_AND_LATER_CHANGE',
            'actual_holdout_mutation':'PASS_PREDICTIONS_UNCHANGED_SCORES_CHANGED',
            'independent_exact_fixed_prediction':'13/24,13/24','source_hashes':r.source_hashes(),
            'execution_profile':'JSON_DECLARATIVE_POLICIES_ONLY','arbitrary_python_sandbox':'NOT_PROVIDED',
            'external_person_reproduction':'NOT_PERFORMED','scientific_claim_supported':False}
    r.write(output/'qualification.json',result);print(json.dumps(result));return result


if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--output',type=Path,required=True);args=a.parse_args()
    qualify(args.output)
