import argparse,hashlib,json,shutil,subprocess,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    p=argparse.ArgumentParser();p.add_argument('--quick',action='store_true');args=p.parse_args()
    subprocess.run([sys.executable,'-B',str(HERE/'verify.py')],check=True)
    if args.quick:return
    before={str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.log'}
    with tempfile.TemporaryDirectory(prefix='cspp_v024_replay_') as td:
        dst=Path(td)/'cspp_v024';shutil.copytree(HERE,dst,ignore=shutil.ignore_patterns('__pycache__','*.log'))
        for bits in [128,192]:subprocess.run([sys.executable,'-B',str(dst/'run.py'),'--bits',str(bits)],check=True)
        subprocess.run([sys.executable,'-B',str(dst/'verify.py')],check=True)
        files=sorted((HERE/'results').glob('*.json'))
        for p in files:
            if sha(p)!=sha(dst/'results'/p.name):raise ArithmeticError('replay mismatch '+p.name)
        for n,h in before.items():
            if sha(HERE/n)!=h:raise ArithmeticError('original modified '+n)
        print(json.dumps({'isolated_replay':'PASS','byte_identical_result_files':len(files),'originals_unchanged':True,'files':{p.name:sha(p) for p in files}}))
if __name__=='__main__':main()
