"""SPDX-License-Identifier: Apache-2.0"""
import gzip
import json
import subprocess
import numpy as np
from ra_common import HERE,ROOT,cfg,sha,source_check,inputs
from ra_core import evaluate
from ra_analyze import analyze
from ra_controls import check


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
    f=source_check()
    subprocess.run(['git','merge-base','--is-ancestor',f['commit'],'HEAD'],cwd=ROOT,check=True)
    for name,h in f['files'].items():
        assert sha(subprocess.check_output(['git','show',f['commit']+':'+name],cwd=ROOT))==h,name
    execution=json.loads((HERE/'results/execution.json').read_text())
    assert execution['execution_commit']==f['commit']
    raw=(HERE/'results/records.json.gz').read_bytes();assert sha(raw)==execution['records_sha256']
    recorded=json.loads(gzip.decompress(raw));fresh=[evaluate(r) for r in inputs()]
    compare(fresh,recorded)
    summary=analyze(fresh,execution);compare(summary,json.loads((HERE/'results/summary.json').read_text()))
    print(json.dumps(dict(verification='PASS_NUMERICAL_REPLAY',records=len(recorded),
        complete=sum(r['status']=='COMPLETE' for r in recorded),frozen_files=len(f['files']),
        scientific_decision=summary['decision'],controls=check(),
        limits='Same archived true coordinates/supports; no new cloud draw, frame search, or independent replication.')))


if __name__=='__main__':main()
