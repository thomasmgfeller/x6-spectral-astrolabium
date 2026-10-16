"""Predeclared small-N pilot sweep with matrices, seeds, replicates and t intervals.

The intervals describe Monte Carlo sampling of this generator. They do not
include model/systematic errors, guarantee Gaussianity or establish a limit.
"""
import argparse
import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import scipy
from scipy.stats import t
from rax_cqg_twin import VERSION, experiment

ROOT=Path(__file__).resolve().parent
SIZES=[8,16,24,32,48]
CONFIGS=[('percolation',.15),('percolation',.25),('percolation',.35),
         ('three_layer',.5),('minkowski_2d',.25),('minkowski_4d',.25)]
REPLICATES=8
SUMMARY_METRICS=['ordering_fraction','links','height','bdg4_bracket','spectral_radius','algebraic_connectivity','h2_spectral_entropy']


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,default=ROOT/'rax_cqg_sweep_results.json')
    args=parser.parse_args()
    runs,groups=[],[]
    for n_index,n in enumerate(SIZES):
        for c_index,(model,p) in enumerate(CONFIGS):
            group=[]
            config_index=n_index*len(CONFIGS)+c_index
            for replicate in range(REPLICATES):
                seed=100000+100*config_index+replicate
                record=experiment(model,n,seed,p)
                record['run_id']=f'n{n}-{model}-p{p}-r{replicate}'
                record['replicate']=replicate
                runs.append(record);group.append(record)
            summary={}
            for metric in SUMMARY_METRICS:
                values=np.asarray([r['metrics'][metric] for r in group if r['metrics'][metric] is not None],dtype=float)
                count=len(values)
                if count<2:
                    summary[metric]={'count':count,'undefined_count':REPLICATES-count,'mean':float(values.mean()) if count else None,'sd':None,'sem':None,'t95_interval':None}
                else:
                    mean,sd=float(values.mean()),float(values.std(ddof=1))
                    sem=sd/count**.5;half=float(t.ppf(.975,count-1))*sem
                    summary[metric]={'count':count,'undefined_count':REPLICATES-count,'mean':mean,'sd':sd,'sem':sem,'t95_interval':[mean-half,mean+half]}
            groups.append({'model':model,'size':n,'p':p if model in ('percolation','three_layer') else None,
                           'replicates':REPLICATES,'summary':summary})
    result={'schema':'RAX-CQG-SWEEP-0.2','software_version':VERSION,'study_date':'2026-10-16',
            'status':'COMPUTED_PILOT_DATA','purpose':'Finite-ensemble reference data; no continuum, suppression or quantum-emergence claim',
            'plan':{'sizes':SIZES,'configurations':[{'model':m,'p':p if m in ('percolation','three_layer') else None} for m,p in CONFIGS],
                    'replicates':REPLICATES,'seed_rule':'100000 + 100*(size_index*6 + configuration_index) + replicate',
                    'sampling_uncertainty':'Student t 95% interval, df=count-1; small-sample approximation; raw values retained; means condition on defined values, undefined_count is reported',
                    'comparison_limits':'Different ensembles have different densities; raw differences do not establish geometry-specific information'},
            'environment':{'python':sys.version,'numpy':np.__version__,'scipy':scipy.__version__,'platform':platform.platform()},
            'source_sha256':{name:hashlib.sha256((ROOT/name).read_bytes()).hexdigest() for name in ['rax_cqg_twin.py','run_sweep.py']},
            'runs':runs,'groups':groups}
    args.output.write_text(json.dumps(result,indent=2,allow_nan=False)+'\n')
    print(json.dumps({'runs':len(runs),'groups':len(groups),'output':str(args.output),'bytes':args.output.stat().st_size}))


if __name__=='__main__':main()
