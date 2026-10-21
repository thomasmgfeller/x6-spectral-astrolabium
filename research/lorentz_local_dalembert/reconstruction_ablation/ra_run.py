"""SPDX-License-Identifier: Apache-2.0"""
import gzip
import json
import resource
import signal
import subprocess
import time
from ra_common import HERE,ROOT,cfg,write,sha,inputs,source_check
from ra_core import evaluate
from ra_analyze import analyze


def main():
    freeze=source_check();dest=HERE/'results';assert not dest.exists(),'Preserve prior execution.'
    dest.mkdir();rows=[];start=time.monotonic()
    execution=dict(status='RUNNING',source_commit=freeze['commit'],
        execution_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
        started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),records=0)
    def save():
        execution.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,records=len(rows))
        write(dest/'execution.json',execution)
    def timeout(*args):raise TimeoutError('fixed wall budget')
    signal.signal(signal.SIGALRM,timeout);signal.alarm(cfg()['wall_budget_seconds'])
    try:
        save()
        for row in inputs():
            rows.append(evaluate(row));save()
            assert execution['peak_mib']<=cfg()['memory_budget_mib']
        execution['status']='COMPLETE'
    except Exception as exc:
        execution.update(status='HOLD',reason=repr(exc));raise
    finally:
        signal.alarm(0)
        raw=gzip.compress(json.dumps(rows,sort_keys=True,separators=(',',':'),allow_nan=False).encode(),mtime=0)
        (dest/'records.json.gz').write_bytes(raw);execution['records_sha256']=sha(raw);save()
    summary=analyze(rows,execution);write(dest/'summary.json',summary)
    print(json.dumps(dict(decision=summary['decision'],records=len(rows),
        paired={p:v['paired_complete'] for p,v in summary['phases'].items()},seconds=execution['seconds'])))


if __name__=='__main__':main()
