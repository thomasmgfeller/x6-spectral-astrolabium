from pathlib import Path
import argparse
import io
import json
import sys
import unittest
import test_contract

def ids(suite):
    for item in suite:
        if isinstance(item,unittest.TestSuite):
            yield from ids(item)
        else: yield item.id()

def run(out):
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_contract)
    names=list(ids(suite))
    stream=io.StringIO()
    result=unittest.TextTestRunner(stream=stream,verbosity=2).run(suite)
    if not result.wasSuccessful():
        print(stream.getvalue(),file=sys.stderr)
        raise SystemExit(1)
    out.mkdir(parents=True,exist_ok=True)
    record={'tests_run':result.testsRun,'status':'PASS','tests':names,
            'scope':'FINITE_EXACT_AND_NUMERICAL_CONTROLS_NOT_PHYSICAL_QUALIFICATION',
            'quadrature_absolute_tolerance':1e-11,
            'physical_gates':'HOLD'}
    (out/'checks.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(f'{result.testsRun} controls PASS; physical gates HOLD')

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--out',type=Path,default=Path(__file__).resolve().parent/'results')
    run(p.parse_args().out)
