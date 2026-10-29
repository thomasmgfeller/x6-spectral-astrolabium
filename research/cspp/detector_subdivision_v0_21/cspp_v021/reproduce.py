"""Verify inputs/results; replay both precisions in an isolated temporary copy."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');a=ap.parse_args()
    subprocess.run([sys.executable,str(HERE/'verify.py')],check=True)
    if a.quick:return
    with tempfile.TemporaryDirectory(prefix='cspp_v021_replay_') as td:
        dst=Path(td)/'cspp_v021';shutil.copytree(HERE,dst,ignore=shutil.ignore_patterns('__pycache__','*.log'))
        procs=[subprocess.Popen([sys.executable,str(dst/'run.py'),'--bits',str(bits)]) for bits in [128,192]]
        codes=[p.wait() for p in procs]
        if any(codes):raise ArithmeticError('precision replay failed: '+str(codes))
        subprocess.run([sys.executable,str(dst/'verify.py')],check=True)
        files=[p for p in (HERE/'results').iterdir() if p.suffix in ['.json','.gz']]
        for p in files:
            if digest(p)!=digest(dst/'results'/p.name):raise ArithmeticError('nonidentical replay: '+p.name)
        print(json.dumps({'isolated_replay':'PASS','byte_identical_result_files':len(files)}))
if __name__=='__main__':main()
