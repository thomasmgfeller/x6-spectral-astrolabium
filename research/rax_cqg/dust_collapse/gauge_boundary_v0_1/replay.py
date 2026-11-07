#!/usr/bin/env python3
"""Isolated stdlib-only replay and byte comparison of exact result files."""
from pathlib import Path
import hashlib,json,shutil,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parent
NAMES=['enumeration.csv','rank_histogram.csv','relative_measure.csv',
       'amplitude_certificates.json','amplitude_certificates_interior.json',
       'witnesses.json','verification.json']
with tempfile.TemporaryDirectory(prefix='cst_gauge_replay_') as tmp:
    p=Path(tmp)
    for name in ['analyze.py','plan.json','plan.sha256','supplement_01.json']:
        shutil.copy2(ROOT/name,p/name)
    shutil.copytree(ROOT/'inputs',p/'inputs')
    run=subprocess.run([sys.executable,'-O','-B','analyze.py'],cwd=p,capture_output=True,text=True)
    if run.returncode:raise RuntimeError(run.stderr)
    checks=[]
    for name in NAMES:
        original=(ROOT/'results'/name).read_bytes();new=(p/'results'/name).read_bytes()
        if original!=new:raise RuntimeError('Replay mismatch: '+name)
        checks.append({'name':name,'sha256':hashlib.sha256(new).hexdigest(),'byte_identical':True})
    report={'isolated_replay':'PASS','result_files':len(checks),'checks':checks,
            'physical_validation':False,'scope':'Reproducibility of the exact finite audit only.'}
    (ROOT/'results'/'replay.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'isolated_replay':'PASS','result_files':len(checks)}))
