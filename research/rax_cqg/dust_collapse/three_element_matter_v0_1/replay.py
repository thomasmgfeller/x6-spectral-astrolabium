"""Recompute six result files from source only in a fresh temporary directory."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent
FILES=['geometry_controls.json','quadrature_certificates.json','three_element_amplitudes.json',
       'extended_results.json','tail_reduction.json','verification.json']


def main():
    checks=[]
    with tempfile.TemporaryDirectory(prefix='cst-three-element-') as tmp:
        work=Path(tmp)
        for name in ['analyze.py','integrate.py','geometry.py','gauss.py','intervals_fp.py','plan.json','plan.sha256']:
            shutil.copyfile(ROOT/name,work/name)
        shutil.copytree(ROOT/'inputs',work/'inputs',ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
        subprocess.run([sys.executable,'-O','-B','analyze.py'],cwd=work,check=True,capture_output=True,text=True)
        for name in FILES:
            actual=(work/'results'/name).read_bytes()
            if actual!=(ROOT/'results'/name).read_bytes():raise RuntimeError('Replay mismatch: '+name)
            checks.append({'name':name,'byte_identical':True,'sha256':hashlib.sha256(actual).hexdigest()})
    result={'isolated_replay':'PASS','result_files':len(FILES),'checks':checks}
    (ROOT/'results/replay.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
