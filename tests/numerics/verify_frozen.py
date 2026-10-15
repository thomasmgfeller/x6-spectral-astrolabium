#!/usr/bin/env python3
"""Reuse the historical evaluator and controls, without changing numerical gates."""
from pathlib import Path
import argparse,hashlib,json,subprocess,sys,types,zipfile,platform
import numpy,scipy

ROOT=Path(__file__).resolve().parents[2]
HISTORY=ROOT/'docs/numerics-v1/historical'
CONTRACT=HISTORY/'check3-contract.json'

def load_original():
    archive=HISTORY/'check3-original.zip'
    with zipfile.ZipFile(archive) as z:
        source=z.read('X6_Pruefung_3_v1/verify.py')
        frozen=z.read('X6_Pruefung_3_v1/contract.json')
    if frozen!=CONTRACT.read_bytes():raise ValueError('Historical contract changed')
    mod=types.ModuleType('historical_check3')
    mod.__file__=str(HISTORY/'historical_verify.py')
    exec(compile(source,'historical_check3/verify.py','exec'),mod.__dict__)
    return mod,hashlib.sha256(source).hexdigest()

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);ap.add_argument('--allow-working-tree',action='store_true');args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    data_path=args.output/'x6-output.json'
    subprocess.run(['node',str(ROOT/'tests/numerics/export.cjs'),str(CONTRACT),str(data_path)],check=True,stdout=subprocess.DEVNULL)
    data=json.loads(data_path.read_text());contract=json.loads(CONTRACT.read_text())
    evaluator,evaluator_hash=load_original()
    source=data['source'];commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    expected_app=hashlib.sha256((ROOT/'app/index.html').read_bytes()).hexdigest()
    def envelope(d,c):
        errors=[]
        if d['source']['commit']!=commit:errors.append('commit')
        if d['source']['app_sha256']!=expected_app:errors.append('source_hash')
        if d['source']['contract_sha256']!=hashlib.sha256(CONTRACT.read_bytes()).hexdigest():errors.append('contract_hash')
        if [r['id'] for r in d['runs']]!=[c['id'] for c in c['cases']]:errors.append('case_set')
        if d['source']['source_dirty'] and not args.allow_working_tree:errors.append('dirty_source')
        return errors
    # Only provenance is rebound to the new source. evaluate() and controls() are unchanged.
    evaluator.envelope_errors=envelope
    errors=envelope(data,contract)
    if errors:raise ValueError('Envelope: '+repr(errors))
    results=[evaluator.evaluate(c,r,contract) for c,r in zip(contract['cases'],data['runs'])]
    negative,positive=evaluator.controls(data,contract)
    success=all(x['status']=='PASS' for x in results+negative+positive)
    result={'schema':'x6.numerics.frozen-replay/1','status':'PASS' if success else 'FAIL',
        'source':source,'frozen_contract_sha256':source['contract_sha256'],'historical_evaluator_sha256':evaluator_hash,
        'binding_note':'Original numeric contract and evaluator unchanged; only source envelope rebound to target commit.',
        'environment':{'python':platform.python_version(),'numpy':numpy.__version__,'scipy':scipy.__version__},
        'summary':{'passed':sum(x['status']=='PASS' for x in results),'total':len(results),'negative_passed':sum(x['status']=='PASS' for x in negative),'negative_total':len(negative),'positive_passed':sum(x['status']=='PASS' for x in positive),'positive_total':len(positive)},
        'results':results,'negative_controls':negative,'positive_controls':positive,
        'scope':'Finite frozen corpus; numerical reference, not a general proof or physical evidence.'}
    (args.output/'frozen-results.json').write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'status':result['status'],**result['summary'],'failed':[x['id'] for x in results if x['status']!='PASS']}))
    return 0 if success else 1
if __name__=='__main__':sys.exit(main())
