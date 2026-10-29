"""Isolated replay; original inputs/results are never overwritten."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');a=ap.parse_args()
    subprocess.run([sys.executable,str(HERE/'verify.py')],check=True)
    if a.quick:return
    with tempfile.TemporaryDirectory(prefix='cspp_v020_replay_') as td:
        root=Path(td)/'cspp_v020';shutil.copytree(HERE,root,ignore=shutil.ignore_patterns('__pycache__','*.log'))
        for bits in [128,192]:subprocess.run([sys.executable,str(root/'run.py'),'--bits',str(bits)],check=True)
        subprocess.run([sys.executable,str(root/'verify.py')],check=True)
        tested=[p for p in (HERE/'results').iterdir() if p.suffix in ['.json','.gz','.npy']]
        for p in tested:
            if digest(p)!=digest(root/'results'/p.name):raise ArithmeticError('nonidentical replay: '+p.name)
        print(json.dumps({'isolated_replay':'PASS','byte_identical_result_files':len(tested)}))
if __name__=='__main__':main()
