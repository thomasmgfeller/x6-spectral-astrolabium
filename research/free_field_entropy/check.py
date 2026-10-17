"""Ledger, estimator and optional independent Hermitian covariance cross-check."""
import argparse
import json
from pathlib import Path
import math
import numpy as np
from scipy.linalg import eigh
from threadpoolctl import threadpool_limits
from core import require
from produce import draw
from analyze import summarize
from run import verify_freeze

HERE = Path(__file__).resolve().parent


def check_records(records, cfg):
    expected = {(n,r) for n in cfg['sampling']['sizes'] for r in range(cfg['sampling']['replicates_per_size'])}
    require(len(records)==len(expected) and {(r['n'],r['replicate']) for r in records}==expected, 'exact complete cohort')
    for record in records:
        _, _, metadata = draw(record['n'],record['replicate'],cfg)
        require(all(record[k]==v for k,v in metadata.items()), 'deterministic input provenance')
    return summarize(records,cfg)


def independent_entropy(order, region, coefficient):
    # Deliberately explicit full-matrix projection, then a Hermitian covariance
    # eigenproblem. Does not call production entropy() or regional_diagnostics().
    h = .5j*(order.T.astype(float)-order.astype(float))
    d,u = eigh(h)
    keep = np.abs(d)>coefficient*math.sqrt(len(order))/(4*math.pi)
    pos = d>coefficient*math.sqrt(len(order))/(4*math.pi)
    w = (u[:,pos]*d[pos])@u[:,pos].conj().T
    hh = (u[:,keep]*d[keep])@u[:,keep].conj().T
    w,h = w[np.ix_(region,region)],hh[np.ix_(region,region)]
    d,u = eigh(h)
    keep = np.abs(d)>coefficient*math.sqrt(len(region))/(4*math.pi)
    u,d = u[:,keep],d[keep]
    rr = u.conj().T@(w-h/2)@u
    rr = (rr+rr.conj().T)/2
    rd,ru = eigh(rr)
    require(rd.min()>0, 'positive reduced real covariance')
    root = (ru*np.sqrt(rd))@ru.conj().T
    herm = root@(root/d[:,None])
    require(np.linalg.norm(herm-herm.conj().T)<1e-8, 'Hermitian symplectic oracle')
    nu = eigh(herm,eigvals_only=True)
    nu = nu[nu>0]
    require(nu.min()>=.5-1e-8, 'uncertainty bound')
    nu=np.maximum(nu,.5)
    minus=nu-.5
    correction=np.zeros_like(minus)
    correction[minus>0]=minus[minus>0]*np.log(minus[minus>0])
    return float(np.sum((nu+.5)*np.log(nu+.5)-correction))


def main():
    p=argparse.ArgumentParser()
    p.add_argument('directory',type=Path)
    p.add_argument('--audit',action='store_true')
    args=p.parse_args()
    cfg=json.loads((HERE/'contract.json').read_text())
    env=json.loads((args.directory/'environment.json').read_text())
    freeze=verify_freeze(env['source_ref'])
    require(json.loads((args.directory/'freeze.json').read_text())==freeze,'result freeze matches sources')
    execution=json.loads((args.directory/'execution.json').read_text())
    require(execution['status']=='COMPLETED' and execution['returncode']==0,'completed execution')
    require(execution['source_ref']==env['source_ref'],'execution source reference')
    require(execution['elapsed_seconds']<=cfg['budget']['wall_seconds']+5,'wall budget')
    require(env['peak_rss_bytes']<=cfg['budget']['memory_bytes'],'resident memory budget')
    require(all(p['num_threads']==1 for p in env['threadpools']),'one BLAS thread')
    records=[json.loads(line) for line in (args.directory/'records.jsonl').read_text().splitlines()]
    with threadpool_limits(1):
        actual=check_records(records,cfg)
        expected=json.loads((args.directory/'summary.json').read_text())
        require(actual==expected,'summary recomputation')
        differences=[]
        if args.audit:
            for n in cfg['sampling']['sizes']:
                r=next(r for r in records if r['n']==n and r['replicate']==0)
                c,a,_=draw(n,0,cfg)
                value=independent_entropy(c,a,1.)
                delta=abs(value-r['diagnostics']['cutoffs']['1.0']['double']['entropy_nats'])
                require(delta<1e-9,'independent symplectic entropy')
                differences.append({'n':n,'replicate':0,'absolute_error_nats':delta})
    print(json.dumps({'status':'PASS_LEDGER_AND_ANALYSIS','scientific_status':actual['status'],
                      'independent_audit':differences},indent=2))


if __name__=='__main__':
    main()
