#!/usr/bin/env python3
"""Check 4: unchanged frozen evaluator plus relabeling and gap diagnostics."""
from pathlib import Path
import argparse,copy,gzip,hashlib,json,platform,subprocess,sys,time
import numpy as np
import scipy
from verify_frozen import ROOT,load_original

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    args.output.mkdir(parents=True,exist_ok=True)
    path=ROOT/'docs/numerics-v1/extended/contract.json';cb=path.read_bytes();contract=json.loads(cb)
    evaluator,evhash=load_original();raw=args.output/'extended-output.json'
    start=time.monotonic()
    subprocess.run(['node',str(ROOT/'tests/numerics/export.cjs'),str(path),str(raw)],check=True,stdout=subprocess.DEVNULL)
    elapsed=time.monotonic()-start;data=json.loads(raw.read_text())
    assert data['source']['app_sha256']==contract['app_sha256']
    assert data['source']['contract_sha256']==hashlib.sha256(cb).hexdigest()
    assert not data['source']['source_dirty']
    assert [r['id'] for r in data['runs']]==[c['id'] for c in contract['cases']]
    results=[evaluator.evaluate(c,r,contract) for c,r in zip(contract['cases'],data['runs'])]
    byid={r['id']:r for r in data['runs']}
    def gap_check(c,r):
        actual=r['analysis']['numerical']['positiveGap']['status']
        return dict(id=c['id'],expected=c['expected_gap_status'],actual=actual,status='PASS' if actual==c['expected_gap_status'] else 'FAIL')
    diagnostics=[]
    for c,r in zip(contract['cases'],data['runs']):
        if 'expected_gap_status' in c:
            diagnostics.append(gap_check(c,r))

    def metamorphic(c,r):
        b=byid[c['base']];scale=float(np.linalg.norm(np.array(b['L']),ord=np.inf))
        w=np.array([e['value'] for e in b['eigenpairs']])/scale
        u=np.array([e['value'] for e in r['eigenpairs']])/scale
        V=np.array([e['vector'] for e in b['eigenpairs']]).T
        mapped=[c['to_base'][label] for label in r['nodes']]
        order=[mapped.index(label) for label in b['nodes']]
        W=np.array([e['vector'] for e in r['eigenpairs']]).T[order,:]
        boundaries=[0]+[i for i in range(1,len(w)) if w[i]-w[i-1]>contract['cluster_relative_gap']]+[len(w)]
        proj=max(float(np.linalg.norm(V[:,a:z]@V[:,a:z].T-W[:,a:z]@W[:,a:z].T,'fro')) for a,z in zip(boundaries,boundaries[1:]))
        eig=float(np.max(np.abs(w-u)))
        return dict(id=c['id'],eigenvalue_scaled_error=eig,projector_frobenius=proj,status='PASS' if eig<=contract['metamorphic_spectrum_scaled_limit'] and proj<=contract['metamorphic_projector_frobenius_limit'] else 'FAIL')
    transformations=[metamorphic(c,r) for c,r in zip(contract['cases'],data['runs']) if c['family']=='metamorphic']
    c=next(c for c in contract['cases'] if c['family']=='metamorphic');base=byid[c['id']]
    controls=[]
    r=copy.deepcopy(base);r['eigenpairs'][0]['value']+=1
    controls.append(dict(id='changed_metamorphic_eigenvalue',status='PASS' if metamorphic(c,r)['status']=='FAIL' else 'FAIL'))
    r=copy.deepcopy(base);r['eigenpairs'][0]['vector']=r['eigenpairs'][-1]['vector'][:]
    controls.append(dict(id='changed_metamorphic_eigenspace',status='PASS' if metamorphic(c,r)['status']=='FAIL' else 'FAIL'))
    r=copy.deepcopy(base);r['eigenpairs'][0]['vector']=[-x for x in r['eigenpairs'][0]['vector']]
    controls.append(dict(id='allowed_sign_flip',status=metamorphic(c,r)['status']))
    gap_case=next(c for c in contract['cases'] if c['family']=='unresolved_gap')
    r=copy.deepcopy(byid[gap_case['id']]);r['analysis']['numerical']['positiveGap']['status']='RESOLVED_AT_TOLERANCE'
    controls.append(dict(id='false_resolved_gap_claim',status='PASS' if gap_check(gap_case,r)['status']=='FAIL' else 'FAIL'))
    success=all(r['status']=='PASS' for r in results+diagnostics+transformations+controls)
    compressed=gzip.compress(raw.read_bytes(),mtime=0);archive=args.output/'extended-output.json.gz';archive.write_bytes(compressed);raw.unlink()
    report=dict(schema='x6.numerics.extended-results/1',status='PASS' if success else 'FAIL',source=data['source'],
        evaluator_sha256=evhash,contract_sha256=hashlib.sha256(cb).hexdigest(),raw_output_archive_sha256=hashlib.sha256(compressed).hexdigest(),
        environment=dict(python=platform.python_version(),numpy=np.__version__,scipy=scipy.__version__),
        export_elapsed_seconds=elapsed,timing_scope='Both original and observation-only Node executions; environment-specific, not a performance guarantee.',
        summary=dict(cases=len(results),passed=sum(r['status']=='PASS' for r in results),metamorphic=len(transformations),gap_diagnostics=len(diagnostics),controls=len(controls)),
        results=results,metamorphic=transformations,gap_diagnostics=diagnostics,controls=controls,
        scope=contract['scope'])
    (args.output/'extended-results.json').write_text(json.dumps(report,indent=2,allow_nan=False)+'\n')
    print(json.dumps({k:report[k] for k in ['status','summary','export_elapsed_seconds']}))
    for r in results+diagnostics+transformations+controls:
        if r['status']!='PASS':print(json.dumps(r))
    return 0 if success else 1
if __name__=='__main__':sys.exit(main())
