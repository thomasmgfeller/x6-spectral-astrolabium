"""SPDX-License-Identifier: Apache-2.0
Reanalyze the frozen observations; never draw new seeds or replace a result.
"""
import json
import math
import subprocess
from analyze import HERE, analyze, sha


def compare(actual, expected, path='root'):
    if isinstance(expected,dict):
        assert actual.keys()==expected.keys(), path
        for k in expected:
            if k != 'python_runtime':
                compare(actual[k],expected[k],path+'.'+k)
    elif isinstance(expected,list):
        assert len(actual)==len(expected), path
        for i,(a,b) in enumerate(zip(actual,expected)):
            compare(a,b,f'{path}[{i}]')
    elif isinstance(expected,float):
        assert math.isclose(actual,expected,rel_tol=1e-12,abs_tol=1e-12), (path,actual,expected)
    else:
        assert actual==expected, (path,actual,expected)


def main():
    frozen=json.loads((HERE/'freeze.json').read_text())
    root=HERE.parents[2]
    commit=frozen['commit']
    prefix=HERE.relative_to(root).as_posix()
    for name,digest in frozen['files'].items():
        archived=subprocess.check_output(['git','show',f'{commit}:{prefix}/{name}'],cwd=root)
        assert sha(archived)==digest==sha((HERE/name).read_bytes()), name
    subprocess.run(['git','merge-base','--is-ancestor',commit,'HEAD'],cwd=root,check=True)
    actual=analyze()
    expected=json.loads((HERE/'results/decision.json').read_text())
    compare(actual,expected)
    print(json.dumps(dict(verification='PASS',frozen_source_files=len(frozen['files']),
        scientific_decision=actual['decision'],gates=actual['gate_counts'],
        historical_v1b=actual['historical_v1b'],positive_controls=actual['positive_controls'])))


if __name__=='__main__':
    main()
