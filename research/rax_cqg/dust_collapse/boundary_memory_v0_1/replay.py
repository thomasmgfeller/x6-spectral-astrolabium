#!/usr/bin/env python3
"""Source-only isolated replay of the five exact result files."""
import hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).resolve().parent
FILES=['finite_growth.json','counting_measure.json','memory_counterexamples.json','boundary_norms.json','verification.json']
def main():
    checks=[]
    with tempfile.TemporaryDirectory(prefix='cst-boundary-memory-') as tmp:
        p=Path(tmp)
        for name in ['analyze.py','memory.py','plan.json','plan.sha256']:shutil.copyfile(ROOT/name,p/name)
        shutil.copytree(ROOT/'inputs',p/'inputs');(p/'results').mkdir()
        subprocess.run([sys.executable,'-O','-B','analyze.py'],cwd=p,check=True,capture_output=True,text=True)
        for name in FILES:
            old=(ROOT/'results'/name).read_bytes();new=(p/'results'/name).read_bytes()
            if old!=new:raise RuntimeError('Replay mismatch: '+name)
            checks.append({'name':name,'byte_identical':True,'sha256':hashlib.sha256(new).hexdigest()})
    result={'isolated_replay':'PASS','result_files':len(checks),'checks':checks}
    (ROOT/'results/replay.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
