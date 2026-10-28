"""Frozen evidence, complete inventory, scientific HOLD and optional isolated replay."""
import argparse,json,os,subprocess,sys,tempfile
from pathlib import Path
from flint import ctx
from common import HERE,sha,check,balls
import benchmark,audit,run

def integrity():
    run.frozen();ctx.prec=192;manifest={}
    for line in (HERE/'SHA256SUMS').read_text().splitlines():
        h,p=line.split('  ',1);check(not Path(p).is_absolute() and '..' not in Path(p).parts and p not in manifest,'safe unique package path')
        manifest[p]=h;check(sha(HERE/p)==h,'package hash '+p)
    actual={p.relative_to(HERE).as_posix() for p in HERE.rglob('*') if p.is_file() and p.name!='SHA256SUMS' and '__pycache__' not in p.parts}
    check(actual==set(manifest),'complete package inventory')
    low=benchmark.gzread(HERE/'results/BENCHMARK_128.json.gz');high=benchmark.gzread(HERE/'results/BENCHMARK_192.json.gz');audit.compare(low,high)
    check(json.loads((HERE/'results/SUMMARY.json').read_text())==run.summary(low),'summary recomputes')
    for label in ['DEFAULT','BASELINE']:
        x=json.loads((HERE/f'results/CPU_{label}.json').read_text())
        check(x['status']=='PASS_EXACT_REQUIRED_RELATIONS_AND_NUMERIC_REPLAY' and len(x['rows'])==64 and x['outer_clouds']==8,'complete CPU scope')
    check(json.loads((HERE/'results/AUDIT.json').read_text())['status']=='PASS','independent audit')
    return low

def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');a=p.parse_args();low=integrity()
    if a.replay:
        with tempfile.TemporaryDirectory(prefix='cspp-propagation-') as tmp:
            subprocess.run([sys.executable,'-B',str(HERE/'run.py'),'all','--out',tmp],check=True)
            audit.compare(low,benchmark.gzread(Path(tmp)/'BENCHMARK_128.json.gz'))
        integrity()
    print(json.dumps({'status':'PASS','field_adapter_cases':1554,'isolated_replay':a.replay,'new_random_realizations':0,'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}))
if __name__=='__main__':main()
