"""Read-only provenance checks and isolated, byte-identical numerical replay."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--quick',action='store_true');args=ap.parse_args()
    subprocess.run([sys.executable,str(HERE/'verify.py')],check=True)
    if args.quick:return
    originals={str(p.relative_to(HERE)):digest(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.log'}
    with tempfile.TemporaryDirectory(prefix='cspp_v022_replay_') as td:
        dst=Path(td)/'cspp_v022';shutil.copytree(HERE,dst,ignore=shutil.ignore_patterns('__pycache__','*.log'))
        procs=[subprocess.Popen([sys.executable,str(dst/'run.py'),'--bits',str(bits)]) for bits in [128,192]]
        codes=[p.wait() for p in procs]
        if any(codes):raise ArithmeticError('precision replay failed: '+str(codes))
        subprocess.run([sys.executable,str(dst/'verify.py')],check=True)
        files=sorted(p for p in (HERE/'results').iterdir() if p.suffix in ['.json','.gz'])
        for p in files:
            if digest(p)!=digest(dst/'results'/p.name):raise ArithmeticError('nonidentical replay: '+p.name)
        for name,h in originals.items():
            if digest(HERE/name)!=h:raise ArithmeticError('original changed: '+name)
        print(json.dumps({'isolated_replay':'PASS','byte_identical_result_files':len(files),'originals_unchanged':True,'files':{p.name:digest(p) for p in files}}))
if __name__=='__main__':main()
