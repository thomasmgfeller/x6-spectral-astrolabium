"""Full replay checks inputs and independently verifies nonunique LP witnesses."""
import argparse
import copy
import hashlib
import json
import subprocess
import tempfile
from pathlib import Path
import numpy as np
from feas_common import HERE,ROOT,config,sources,encode,compare
from feas_controls import check
from feas_analysis import load,summarize
from feasibility import validate_record
from run_feasibility import run_cloud

def lp_compare(a,b,path='root'):
    if isinstance(a,dict):
        assert a.keys()==b.keys(),path
        for k in a:lp_compare(a[k],b[k],path+'.'+k)
    elif isinstance(a,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):lp_compare(x,y,path+f'[{i}]')
    elif isinstance(a,float):
        assert np.isfinite(a) and np.isfinite(b),path
        assert abs(a-b)<=1e-8+1e-7*abs(a),path
    else:assert a==b,path

def compare_clouds(a,b,contract):
    assert validate_record(a,contract) and validate_record(b,contract)
    aa=copy.deepcopy(a);bb=copy.deepcopy(b)
    for name in contract['supports']:
        x=aa['supports'][name];y=bb['supports'][name]
        if x['status']!='ok':continue
        xp=x.pop('policies');yp=y.pop('policies')
        for policy in contract['policies']:
            u=xp[policy];v=yp[policy];assert u['status']==v['status']
            compare(u['rank'],v['rank']);compare(u['singular_values'],v['singular_values'])
            if u['status']=='FEASIBLE':
                for k in ['minimum_mass','mass_ratio']:lp_compare(u[k],v[k])
    compare(aa,bb)

def verify(directory):
    contract,cfg=config();e,rows=load(directory)
    assert sources()==e['source_sha256'],'local frozen-source mismatch'
    for path,digest in sources().items():
        data=subprocess.check_output(['git','show',e['source_commit']+':'+path],cwd=ROOT)
        assert hashlib.sha256(data).hexdigest()==digest,'public source mismatch '+path
    controls=check();expected=json.loads((directory/'summary.json').read_text())
    assert expected['complete'] and expected['budget_pass'] and expected['certificates_pass'] and expected['algebra_pass']
    compare(expected,summarize(directory));exact=0;problems=0
    with tempfile.TemporaryDirectory(prefix='bk-feas-') as tmp:
        p=Path(tmp);execution=dict(e,records=[])
        for row in rows:
            actual=run_cloud(row['rho'],row['seed'],cfg,contract,controls=row['cloud_controls'] is not None)
            data=encode(actual);compare_clouds(row,json.loads(data),contract)
            exact+=row['coordinates_sha256']==actual['coordinates_sha256']
            problems+=sum(len(s.get('policies',{})) for s in row['supports'].values())
            name=f"rho-{row['rho']}-seed-{row['seed']}.json";(p/name).write_text(data)
            execution['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
        (p/'execution.json').write_text(json.dumps(execution));lp_compare(expected,summarize(p))
    return dict(status='PASS_NUMERICAL_REPLAY',clouds=len(rows),coordinate_hashes_equal=exact,lp_problems=problems,
                relation_marks_support_and_classifications_exact=True,controls=controls,
                baseline_tolerance=contract['baseline_replay_tolerance'],lp_tolerance=contract['lp_replay_tolerance'],
                decision=expected['decision'],phase3='HOLD_PHASE3',
                note='Every archived and replayed witness checked independently. Nonunique weights/dual vectors may differ; objectives and summary must agree. Coordinate byte hashes are separate.')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--directory',type=Path,default=HERE/'results');a=p.parse_args()
    print(json.dumps(verify(a.directory),indent=2))
