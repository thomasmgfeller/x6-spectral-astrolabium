"""SPDX-License-Identifier: Apache-2.0
Replay preserved observations, not new scientific evidence or a new frame search.
"""
import json
import subprocess
import numpy as np
from ec_common import HERE,ROOT,cfg,sha,source_check,load_phase,prepare,models,config,coordinates_only,digest
from ec_measure import evaluate
from ec_prepare import fit_development
from ec_calibrate import calibrate
from ec_analyze import analyze


def compare(a,b,path='root'):
    if isinstance(b,dict):
        assert a.keys()==b.keys(),path
        for k in b:compare(a[k],b[k],path+'.'+k)
    elif isinstance(b,list):
        assert len(a)==len(b),path
        for i,(x,y) in enumerate(zip(a,b)):compare(x,y,f'{path}[{i}]')
    elif isinstance(b,float):np.testing.assert_allclose(a,b,atol=cfg()['numerical_atol'],rtol=cfg()['numerical_rtol'],err_msg=path)
    else:assert a==b,(path,a,b)


def main():
    frozen=source_check()
    for name,h in frozen['files'].items():
        assert sha(subprocess.check_output(['git','show',frozen['commit']+':'+name],cwd=ROOT))==h,name
    subprocess.run(['git','merge-base','--is-ancestor',frozen['commit'],'HEAD'],cwd=ROOT,check=True)
    public=json.loads((HERE/'calibration_freeze.json').read_text())
    path=str((HERE/'frozen_calibration.json').relative_to(ROOT))
    assert subprocess.check_output(['git','show',public['commit']+':'+path],cwd=ROOT)==(HERE/'frozen_calibration.json').read_bytes()
    compare(fit_development(),json.loads((HERE/'development_fit.json').read_text()))
    compare(calibrate(),json.loads((HERE/'frozen_calibration.json').read_text()))
    _,oc,_,_=config();fitted=models();complete=hashes=noise_inputs=noise_outputs=0
    for phase in ['calibration','test']:
        executions,rows=load_phase(phase)
        if phase=='test':assert all(e['execution_commit']==public['commit'] for e in executions)
        for row in rows:
            r=row['cloud'];p=prepare(r['intrinsic'],fitted)
            compare(p,row['prepared'])
            z=coordinates_only(r['rho'],r['seed'],oc)
            hashes+=int(digest(z)==r['coordinates_sha256'])
            fresh=evaluate(r,z,p,row['noise_key'])
            # Numerical replay is explicit; byte identity is reported separately.
            saved=row['evaluation']
            if fresh['status']=='COMPLETE':
                for a,b in zip(fresh['fields'],saved['fields']):
                    noise_inputs+=int(a['noise']['input_sha256']==b['noise']['input_sha256'])
                    noise_outputs+=int(a['noise']['output_sha256']==b['noise']['output_sha256'])
                    a['noise']['input_sha256']=b['noise']['input_sha256']
                    a['noise']['output_sha256']=b['noise']['output_sha256']
                complete+=1
            compare(fresh,saved)
    summary,tests=analyze()
    compare(summary,json.loads((HERE/'results/summary.json').read_text()))
    compare(tests,json.loads((HERE/'results/noise_checks.json').read_text()))
    print(json.dumps(dict(verification='PASS_NUMERICAL_REPLAY',clouds=64,complete=complete,
        coordinate_hash_matches=hashes,frozen_files=len(frozen['files']),scientific_decision=summary['decision'],
        noise_banks=4*complete,noise_input_hash_matches=noise_inputs,noise_output_hash_matches=noise_outputs,
        limits='No full frame-search replay; floating point tolerance predeclared; input/output noise byte hashes are not acceptance gates.')))


if __name__=='__main__':main()
