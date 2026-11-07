#!/usr/bin/env python3
"""Source-only isolated replay of five exact outputs, never copy result files."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=['continuum_certificates.json','history_events.json','cut_controls.json','joint_relative_measure.json','verification.json']
def main():
    checks=[]
    with tempfile.TemporaryDirectory(prefix='cst-positive-histories-') as tmp:
        p=Path(tmp)
        for name in ['analyze.py','plan.json','plan.sha256','supplement_01.json']:shutil.copyfile(ROOT/name,p/name)
        shutil.copytree(ROOT/'inputs',p/'inputs')
        subprocess.run([sys.executable,'-O','-B','analyze.py'],cwd=p,check=True,capture_output=True,text=True)
        for name in FILES:
            old=(ROOT/'results'/name).read_bytes();new=(p/'results'/name).read_bytes()
            if old!=new:raise RuntimeError('Replay mismatch: '+name)
            checks.append({'name':name,'byte_identical':True,'sha256':hashlib.sha256(new).hexdigest()})
    receipt={'isolated_replay':'PASS','result_files':len(checks),'checks':checks,
             'quadrature':'Archived independent supplement; not rerun by this standard-library replay'}
    (ROOT/'results/replay.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
