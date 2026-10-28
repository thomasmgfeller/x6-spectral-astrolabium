"""Integrity, no-run gate and isolated replay; works under python -O."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import model as m
import audit,run


def integrity():
    run.frozen();m.ctx.prec=192;listed={}
    for line in (m.HERE/'SHA256SUMS').read_text().splitlines():
        digest,name=line.split('  ',1)
        audit.check(not Path(name).is_absolute() and '..' not in Path(name).parts and name not in listed,'safe unique manifest path')
        listed[name]=digest;audit.check(hashlib.sha256((m.HERE/name).read_bytes()).hexdigest()==digest,'hash '+name)
    actual={p.relative_to(m.HERE).as_posix() for p in m.HERE.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='SHA256SUMS'}
    audit.check(actual==set(listed),'complete package inventory')
    low=run.gzread(m.HERE/'results/SCAN.json.gz');high=run.gzread(m.HERE/'results/SCAN_192bit.json.gz');audit.compare(low,high)
    d=json.loads((m.HERE/'results/DECISION.json').read_text())
    audit.check(d['next_sprinkling']=='NOT_STARTED_NO_BUDGETED_CANDIDATE','no automatic simulation')
    audit.check(d['rejection_counts']==audit.validate(low),'decision counts')
    for key in ['summaries','relaxed_total_only','budget_sensitivity','fixed_mode_followups','gate_status']:
        audit.check(d[key]==low[key],'summary matches production '+key)
    checks=json.loads((m.HERE/'results/AUDIT.json').read_text());audit.check(checks['status']=='PASS','audit PASS')
    resources=json.loads((m.HERE/'results/RESOURCES.json').read_text());guard=resources['resource_overflow_planning_guard']
    audit.check(m.balls.decode(guard['union_upper_bound']).real<=m.a('1/100'),'Poisson count-cap guard')
    audit.check(m.balls.decode(guard['next_integer_union_upper_bound']).real>m.a('1/100'),'largest integer under declared Chernoff guard')
    audit.check(not resources['run_authorized_by_numerical_decision'],'no resource-driven hidden launch')
    return low


def main():
    p=argparse.ArgumentParser();p.add_argument('--replay',action='store_true');args=p.parse_args();low=integrity()
    if args.replay:
        with tempfile.TemporaryDirectory(prefix='cspp-joint-replay-') as tmp:
            subprocess.run([sys.executable,'-B',str(m.HERE/'run.py'),'all','--out',tmp],check=True)
            audit.compare(low,run.gzread(Path(tmp)/'SCAN.json.gz'))
        integrity()
    print(json.dumps({'status':'PASS','pairs':320,'new_poisson_clouds':0,'decision':low['decision'],
                      'isolated_replay':args.replay,'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'}))

if __name__=='__main__':main()
