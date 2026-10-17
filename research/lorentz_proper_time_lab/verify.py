#!/usr/bin/env python3
"""Cross-language numerical acceptance and actual Jupyter-kernel replay.

Implementation verification only, not a new preregistered scientific benchmark.
"""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import base64
import contextlib
import io
import numpy as np
import nbformat
from nbclient import NotebookClient
from scipy.stats import binomtest

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
spec = importlib.util.spec_from_file_location('domain', HERE.parent/'lorentz_proper_time_domain/domain.py')
domain = importlib.util.module_from_spec(spec)
spec.loader.exec_module(domain)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--execute', action='store_true')
    parser.add_argument('--save-notebook', action='store_true')
    parser.add_argument('--report', type=Path)
    parser.add_argument('--in-process', action='store_true', help='Execute ordinary Python cells without a Jupyter transport; reported separately')
    args = parser.parse_args()
    cases = []
    for m in [1, 2, 8, 64, 256, 1024, 4096, 16384]:
        ks = range(m+1) if m <= 256 else sorted({0,1,2,3,8,m//100,m//16,m//4,m//2,m-8,m-3,m-2,m-1,m})
        for d in [2,3,4]:
            for k in ks:
                cases.append([k,m,d])
    program = r"""
const fs=require('node:fs'),P=require('./core.js');
const cases=JSON.parse(fs.readFileSync(0,'utf8'));
const answers=cases.map(([k,m,d])=>P.infer(k,m,d));
const moments=[];
for(const d of [2,3,4])for(const m of [64,1024,16384])for(const theta of [.1,.5,.85])
  moments.push({d,m,theta,...P.exactMoments(m,d,theta)});
const geometry=[];
for(const d of [2,3,4]) {
  let k=0,t2=0;
  for(let seed=800;seed<810;seed++) {
    const c=P.cloud({m:16384,d,theta:.5,seed});k+=c.k;
    for(const p of c.points) {
      if(!(Math.abs(p[0])+Math.hypot(...p.slice(1))<.5))throw Error('outside diamond');
      t2+=p[0]*p[0];
    }
  }
  geometry.push({d,m:163840,k,t2:t2/163840});
}
const c=P.cloud({m:256,d:4,theta:.5,seed:123}),chain=P.longestChain(c.points,c.inside);
const permutations=c.points.map((_,i)=>i).reverse();
if(P.longestChain(permutations.map(i=>c.points[i]),permutations.map(i=>c.inside[i])).height!==chain.height)throw Error('chain not invariant');
for(let i=1;i<chain.path.length;i++)if(!P.precedes(c.points[chain.path[i-1]],c.points[chain.path[i]]))throw Error('invalid chain');
const chainControl=P.longestChain([[-.3,0],[-.1,0],[.2,0]],[true,true,true]);
const antiControl=P.longestChain([[0,-.3],[0,0],[0,.2]],[true,true,true]);
if(chainControl.height!==3||antiControl.height!==1||P.longestChain([],[]).height!==0)throw Error('chain controls');
const invalid=[()=>P.infer(-1,64,4),()=>P.infer(65,64,4),()=>P.infer(1,0,4),()=>P.infer(1,64,1),()=>P.infer(1,64,4,.05,0),()=>P.cloud({m:64,d:4,theta:.5,seed:-1}),()=>P.rng(1.1)];
for(const f of invalid){let rejected=false;try{f();}catch(e){rejected=true;}if(!rejected)throw Error('invalid input accepted');}
const raw=P.infer(3,64,4),scaled=P.infer(3,64,4,.05,123);
for(const key of ['estimate','lower','upper'])if(Math.abs(raw[key]*123-scaled[key])>1e-12)throw Error('scale failure');
process.stdout.write(JSON.stringify({answers,moments,geometry,cloud:c,chain,invalidRejected:invalid.length}));
"""
    process = subprocess.run(['node','-e',program], input=json.dumps(cases), text=True, capture_output=True, cwd=HERE, check=True)
    js = json.loads(process.stdout)
    max_error = 0.0
    for (k,m,d),answer in zip(cases,js['answers'],strict=True):
        ref = domain.infer(k,m,d)
        expected = [ref['theta_hat'], *ref['interval']]
        actual = [answer['estimate'],answer['lower'],answer['upper']]
        error = float(np.max(np.abs(np.array(actual)-expected)))
        max_error = max(max_error,error)
        assert error < 2e-10, (k,m,d,expected,actual)
    moment_error = 0.0
    for row in js['moments']:
        ref = domain.exact_summary(row['d'],row['m'],row['theta'])
        for key,other in [('rmse','rmse'),('bias','bias'),('expectedK','expected_K'),('zeroProbability','zero_probability')]:
            error = abs(row[key]-ref[other]);moment_error=max(moment_error,error)
            assert error < 2e-10,(row,key,ref)
    geometry = []
    for row in js['geometry']:
        pvalue = float(binomtest(row['k'],row['m'],.5**row['d']).pvalue)
        assert pvalue > 1e-6, row
        # This moment rejects the common erroneous uniform-time sampler.
        expected_t2 = 1/(2*(row['d']+1)*(row['d']+2))
        assert abs(row['t2']-expected_t2) < .0004,row
        geometry.append({**row,'binomial_pvalue':pvalue,'expected_t2':expected_t2})
    c = js['cloud']
    p,q = domain.endpoints(4,.5,'central')
    pts = np.array(c['points'])
    included = domain.chronological(p,pts) & domain.chronological(pts,q)
    assert np.array_equal(included,c['inside'])
    full = domain.full_relation_squared(np.concatenate(([p,q],pts)))
    assert domain.order_count(full,[0,1]) == (c['k'],256)
    assert js['chain']['height'] <= c['k']
    nb = nbformat.read(HERE/'eigenzeit.ipynb',as_version=4)
    nbformat.validate(nb)
    assert nb.metadata.x6.domain_sha256 == hashlib.sha256((HERE.parent/'lorentz_proper_time_domain/domain.py').read_bytes()).hexdigest()
    executions=0
    if args.execute or args.save_notebook:
        if args.in_process:
            import matplotlib
            matplotlib.use('Agg')
            import matplotlib.pyplot as plt
            namespace = {}
            original_show = plt.show
            try:
                for cell in nb.cells:
                    if cell.cell_type != 'code': continue
                    executions += 1
                    cell.outputs = []
                    cell.execution_count = executions
                    def capture_show(*unused_args, **unused_kwargs):
                        for number in plt.get_fignums():
                            fig = plt.figure(number)
                            data = io.BytesIO()
                            fig.savefig(data, format='png', bbox_inches='tight')
                            cell.outputs.append(nbformat.v4.new_output('display_data', data={'image/png':base64.b64encode(data.getvalue()).decode('ascii'), 'text/plain':'Matplotlib figure'}, metadata={}))
                            plt.close(fig)
                    plt.show = capture_show
                    output = io.StringIO()
                    with contextlib.redirect_stdout(output): exec(compile(cell.source,cell.id,'exec'),namespace)
                    if output.getvalue(): cell.outputs.append(nbformat.v4.new_output('stream',name='stdout',text=output.getvalue()))
                executed = nb
                executed.metadata.x6.output_execution = 'sequential Python cells, in process; Jupyter kernel checked separately in CI'
            finally:
                plt.show = original_show
        else:
            executed = NotebookClient(nb,timeout=180,kernel_name='python3',resources={'metadata':{'path':str(HERE)}},record_timing=False).execute()
        executions=sum(c.cell_type=='code' for c in executed.cells)
        for cell in executed.cells:
            if cell.cell_type=='code':
                assert not any(o.output_type=='error' for o in cell.outputs)
        # Compare the actual in-notebook function to the existing reference on a fixed grid.
        namespace={}
        for cell in executed.cells:
            if cell.cell_type=='code' and cell.source.startswith('def infer('):
                exec('import numpy as np\nfrom scipy.special import betaincinv\n'+cell.source.split('assert infer')[0],namespace)
        for k,m,d in cases:
            n=namespace['infer'](k,m,d);ref=domain.infer(k,m,d)
            assert np.allclose([n['theta_hat'],n['lower'],n['upper']],[ref['theta_hat'],*ref['interval']],rtol=0,atol=2e-14)
        if args.save_notebook:
            nbformat.write(executed,HERE/'eigenzeit.ipynb')
    report={'status':'PASS_PROPER_TIME_LAB_IMPLEMENTATION','scope':'Numerical/software verification; not independent scientific replication',
            'interval_cases':len(cases),'maximum_browser_reference_abs_error':max_error,
            'moment_cases':len(js['moments']),'maximum_moment_abs_error':moment_error,
            'sampler_checks':geometry,'rejected_invalid_inputs':js['invalidRejected'],
            'full_relation_count_check':True,'notebook_code_cells_executed':executions,
            'notebook_python':sys.version.split()[0]}
    report['notebook_execution_mode'] = ('in_process_python' if args.in_process else 'jupyter_kernel') if executions else 'not_executed'
    if args.report: args.report.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__=='__main__':
    main()
