"""Read-only verification; does not regenerate manifests or reference results."""
import argparse,hashlib,json,unittest,math
from calculus import ROOT
from run_reduction import compute
from gluing import analyze
from states import evidence
from independent_check import compute as independent

def render(x,ascii=False):return json.dumps(x,indent=2,sort_keys=True,ensure_ascii=ascii)+'\n'

def compare_float_oracle(actual,expected):
 if type(actual) is not type(expected):raise ArithmeticError('Independent oracle type mismatch')
 if isinstance(actual,dict):
  if actual.keys()!=expected.keys():raise ArithmeticError('Independent oracle key mismatch')
  for key in actual:compare_float_oracle(actual[key],expected[key])
 elif isinstance(actual,list):
  if len(actual)!=len(expected):raise ArithmeticError('Independent oracle length mismatch')
  for a,b in zip(actual,expected):compare_float_oracle(a,b)
 elif isinstance(actual,float):
  if not math.isfinite(actual) or abs(actual-expected)>3e-14:raise ArithmeticError('Independent float64 replay mismatch')
 elif actual!=expected:raise ArithmeticError('Independent oracle metadata mismatch')

def main(extended=False):
 manifest=json.loads((ROOT/'MANIFEST.sha256.json').read_text())
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name!='MANIFEST.sha256.json'}
 if actual!=set(manifest):raise SystemExit('Manifest inventory mismatch')
 for path,digest in manifest.items():
  if hashlib.sha256((ROOT/path).read_bytes()).hexdigest()!=digest:raise SystemExit('Hash mismatch: '+path)
 provenance=json.loads((ROOT/'provenance.json').read_text())
 for item in provenance['files']:
  b=(ROOT/item['local_path']).read_bytes()
  if hashlib.sha256(b).hexdigest()!=item['sha256'] or hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()!=item['git_blob_sha']:raise SystemExit('Upstream source mismatch: '+item['local_path'])
 suite=unittest.defaultTestLoader.discover(str(ROOT),pattern='test_reduction.py')
 result=unittest.TextTestRunner(verbosity=1).run(suite)
 if not result.wasSuccessful():return 1
 checks=[('results/reduction.json',lambda:compute(48,192,False),False),
         ('results/gluing.json',analyze,True),('results/states.json',evidence,True)]
 if extended:checks.append(('results/crosscheck_56.json',lambda:compute(56,224,False),False))
 for path,fn,ascii in checks:
  if render(fn(),ascii)!=(ROOT/path).read_text():raise SystemExit('Exact replay mismatch: '+path)
  print('PASS exact replay:',path,flush=True)
 if extended:
  compare_float_oracle(independent(),json.loads((ROOT/'results/independent_5d_n8.json').read_text()))
  print('PASS independent float64 replay: absolute tolerance 3e-14; not a certified error bound.',flush=True)
 print(f'PASS: {result.testsRun} tests; {len(manifest)} file hashes; {len(provenance["files"])} upstream blobs; {len(checks)} exact replays.')
 return 0

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--extended',action='store_true');a=p.parse_args();raise SystemExit(main(a.extended))
