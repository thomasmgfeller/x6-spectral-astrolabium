"""RAX-G1 broker: fresh JSON-only workers, exact replay and phase-bound records.
The protected capability is the declarative policy language, NOT arbitrary Python.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
import os
from pathlib import Path
import secrets
import subprocess
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parent))
import worker as w

ROOT=Path(__file__).resolve().parent
FILES=('contract.json','freeze.json','predictions.json','challenge.json','assessment.json')


def encode(d):return (json.dumps(d,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def digest(b):return hashlib.sha256(b).hexdigest()
def read(p):
    w.require(not p.is_symlink() and p.is_file() and p.stat().st_size<=2_000_000,'INVALID_FILE')
    return w.parse(p.read_text()) if p.stat().st_size<=65536 else json.loads(p.read_text(),object_pairs_hook=unique,parse_constant=bad_number)
def unique(pairs):
    d={}
    for k,v in pairs:w.require(k not in d,'DUPLICATE_KEY');d[k]=v
    return d
def bad_number(_):raise ValueError('NONFINITE')
def write(p,d):
    with p.open('xb') as f:f.write(encode(d));f.flush();os.fsync(f.fileno())


def validate(c):
    w.exact_keys(c,['schema','id','purpose','model','episodes','budget','holdout_per_action','plans'])
    w.require(c['schema']=='rax.guarded-contract/1' and c['id']=='RAX-G1-TECHNICAL-1','CONTRACT')
    w.require(c['purpose']=='Finite synthetic execution qualification; no superiority, RAX-U2 or physical claim','SCOPE')
    p=w.model(c['model']);w.integer(c['episodes'],1,64);b=w.integer(c['budget'],1,32);w.integer(c['holdout_per_action'],1,32)
    w.require(type(c['plans']) is list and 1<=len(c['plans'])<=8,'PLAN_COUNT')
    for plan in c['plans']:w.policy(plan,len(p[0]),b)
    ids=[plan['id'] for plan in c['plans']];w.require(len(ids)==len(set(ids)),'DUPLICATE_PLAN')
    return p


def source_hashes():return {n:digest((ROOT/n).read_bytes()) for n in ['runner.py','worker.py']}


def bernoulli(seed, domain, probability):
    # All allowed denominators divide 2**256; no float or modulo bias.
    u=int.from_bytes(hashlib.sha256(bytes.fromhex(seed)+domain.encode()).digest(),'big')
    return int(u < probability.numerator*((1<<256)//probability.denominator))


def bank(c,seed):
    p=validate(c)
    return [[[bernoulli(seed,f'acq:{i}:{a}:{t}',p[i%len(p)][a]) for t in range(c['budget'])]
            for a in range(len(p[0]))] for i in range(c['episodes'])]


def action(c,plan,history):
    public={'schema':'rax.public-prefix/1','model':c['model'],'plan':plan,'history':history,'budget':c['budget']}
    # Fresh interpreter; no inherited Python closures, planner import, callback,
    # secret environment, user hooks, private file path or RNG state in the request.
    with tempfile.TemporaryDirectory(prefix='rax-public-') as cwd:
        p=subprocess.run([sys.executable,'-I','-S','-B',str(ROOT/'worker.py')],input=encode(public),
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,cwd=cwd,env={'PYTHONHASHSEED':'0'},timeout=3,close_fds=True)
    w.require(p.returncode==0 and len(p.stdout)<=256 and not p.stderr,'WORKER_REJECTED')
    result=w.parse(p.stdout.decode());w.exact_keys(result,['action'])
    return w.integer(result['action'],0,len(c['model'][0])-1)


def predict(c, acquisition):
    p=validate(c);rows=[]
    for i in range(c['episodes']):
        for plan in c['plans']:
            history=[];counts=[0]*len(p[0])
            for _ in range(c['budget']):
                a=action(c,plan,history);y=acquisition[i][a][counts[a]];counts[a]+=1;history.append([a,y])
            posterior=w.posterior(p,history)
            prediction=[str(sum(v*r[a] for v,r in zip(posterior,p))) for a in range(len(p[0]))]
            rows.append({'episode_index':i,'episode_id':f'episode:{i}','plan':plan['id'],'history':history,'prediction':prediction})
    return {'schema':'rax.predictions/1','rows':rows}


def challenge(c,seed):
    p=validate(c)
    return [[[bernoulli(seed,f'holdout:{i}:{a}:{t}',p[i%len(p)][a]) for t in range(c['holdout_per_action'])]
             for a in range(len(p[0]))] for i in range(c['episodes'])]


def assess(c,predictions,holdout):
    rows=predictions['rows'];expected={(i,plan['id']) for i in range(c['episodes']) for plan in c['plans']};seen=set();scores={plan['id']:[] for plan in c['plans']}
    for row in rows:
        w.exact_keys(row,['episode_index','episode_id','plan','history','prediction']);i=w.integer(row['episode_index'],0,c['episodes']-1)
        key=(i,row['plan']);w.require(row['episode_id']==f'episode:{i}' and key in expected and key not in seen,'ROW_IDENTITY_OR_COVERAGE');seen.add(key)
        q=[F(v) for v in row['prediction']];w.require(len(q)==len(c['model'][0]) and all(0<=v<=1 for v in q),'PREDICTION')
        scores[row['plan']].append(sum((q[a]-y)**2 for a,ys in enumerate(holdout[i]) for y in ys)/(len(q)*c['holdout_per_action']))
    w.require(seen==expected,'MISSING_CELLS')
    return {'schema':'rax.technical-assessment/1','status':'TECHNICAL_RUN_COMPLETE','scientific_claim_supported':False,
            'independent_replication':'NOT_PERFORMED','episodes':c['episodes'],'cells':len(rows),
            'mean_brier_exact':{k:str(sum(v)/len(v)) for k,v in scores.items()}}


def replay_payload(c,acquisition_seed,holdout_seed):
    p=predict(c,bank(c,acquisition_seed));h=challenge(c,holdout_seed)
    return p,h,assess(c,p,h)


def run(contract_path,output):
    c=read(contract_path);validate(c)
    # A new directory is the only admitted phase; old test artefacts never qualify.
    output.mkdir(parents=False,exist_ok=False)
    acq_seed=secrets.token_hex(32);test_seed=secrets.token_hex(32)
    freeze={'schema':'rax.freeze/1','contract_sha256':digest(encode(c)),'sources':source_hashes(),
            'acquisition_seed_commitment':digest(bytes.fromhex(acq_seed)),
            'holdout_seed_commitment':digest(bytes.fromhex(test_seed)),
            'attestation':'LOCAL_PHASE_ORDER_ONLY_NOT_PROOF_OF_HUMAN_BLINDNESS'}
    write(output/'contract.json',c);write(output/'freeze.json',freeze)
    predictions=predict(c,bank(c,acq_seed));write(output/'predictions.json',predictions)
    # No holdout outcomes are generated until ALL plans/episodes are sealed.
    h=challenge(c,test_seed)
    released={'schema':'rax.challenge/1','predictions_sha256':digest(encode(predictions)),
              'acquisition_seed':acq_seed,'holdout_seed':test_seed,'holdout':h}
    write(output/'challenge.json',released);assessment=assess(c,predictions,h);write(output/'assessment.json',assessment)
    write(output/'complete.json',{'schema':'rax.complete/1','status':'COMPLETE','files':{n:digest((output/n).read_bytes()) for n in FILES}})
    return assessment


def verify(output):
    w.require(not output.is_symlink() and output.is_dir(),'OUTPUT_DIRECTORY')
    w.require({p.name for p in output.iterdir()}==set(FILES)|{'complete.json'},'EXACT_FILE_SET')
    d={n:read(output/n) for n in FILES+('complete.json',)}
    for n,value in d.items():w.require((output/n).read_bytes()==encode(value),'CANONICAL_JSON')
    w.require(encode(d['complete.json'])==encode({'schema':'rax.complete/1','status':'COMPLETE','files':{n:digest(encode(d[n])) for n in FILES}}),'INVENTORY')
    c=d['contract.json'];validate(c);h=d['challenge.json'];w.exact_keys(h,['schema','predictions_sha256','acquisition_seed','holdout_seed','holdout'])
    for k in ['acquisition_seed','holdout_seed']:w.require(type(h[k]) is str and len(h[k])==64 and all(x in '0123456789abcdef' for x in h[k]),'SEED')
    f={'schema':'rax.freeze/1','contract_sha256':digest(encode(c)),'sources':source_hashes(),
       'acquisition_seed_commitment':digest(bytes.fromhex(h['acquisition_seed'])),'holdout_seed_commitment':digest(bytes.fromhex(h['holdout_seed'])),
       'attestation':'LOCAL_PHASE_ORDER_ONLY_NOT_PROOF_OF_HUMAN_BLINDNESS'}
    w.require(encode(d['freeze.json'])==encode(f),'FREEZE_OR_SOURCES')
    p,expected_h,assessment=replay_payload(c,h['acquisition_seed'],h['holdout_seed'])
    w.require(encode(d['predictions.json'])==encode(p),'PREDICTIONS_REPLAY')
    w.require(encode(h)==encode(dict(schema='rax.challenge/1',predictions_sha256=digest(encode(p)),acquisition_seed=h['acquisition_seed'],holdout_seed=h['holdout_seed'],holdout=expected_h)),'HOLDOUT_REPLAY')
    w.require(encode(d['assessment.json'])==encode(assessment),'ASSESSMENT_REPLAY')
    return {'status':'PASS_GUARDED_REPLAY','cells':len(p['rows']),'scientific_claim_supported':False}


def main():
    a=argparse.ArgumentParser(description=__doc__);sub=a.add_subparsers(dest='command',required=True)
    r=sub.add_parser('run');r.add_argument('--contract',type=Path,default=ROOT/'contract.json');r.add_argument('--output',type=Path,required=True)
    v=sub.add_parser('verify');v.add_argument('output',type=Path);args=a.parse_args()
    try:
        value=run(args.contract,args.output) if args.command=='run' else verify(args.output)
        print(json.dumps(value));return 0
    except (ValueError,TypeError,KeyError,IndexError,OSError,RecursionError,subprocess.TimeoutExpired) as exc:
        print(json.dumps({'status':'REJECTED','reason':str(exc),'scientific_claim_supported':False}));return 1


if __name__=='__main__':sys.exit(main())
