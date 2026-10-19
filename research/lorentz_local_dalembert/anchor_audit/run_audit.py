"""Paired fixed-seed execution. Coordinates never enter either intrinsic arm."""
import argparse
import copy
import hashlib
import json
import resource
import signal
import subprocess
import time
from pathlib import Path
import numpy as np
import scipy
from common import HERE, ROOT, core, config, encode, sources
import estimator
import experiment


def oracle_cap(z, marks, original, cfg):
    s = copy.deepcopy(original)
    if s['status'] == 'short_chain': return s
    for side in s['sides']:
        side['distances'] = [float(experiment.proper(z[b]-z[side['reference']], True)) for b in side['shell']]
        side['diagnostics'] = [{'status':'oracle','anchors':0} for b in side['shell']]
        side['selected'] = [b for b,d in zip(side['shell'],side['distances']) if d <= cfg['radius_over_tau_m']*s['tau_m']]
    s.pop('support', None); s.pop('weights', None)
    if min(len(side['selected']) for side in s['sides']) < cfg['minimum_neighborhood_population']:
        s['status'] = 'insufficient_neighborhood'
        return s
    s['status'] = 'ok'; weights = {}; c = cfg['coefficient_C']
    for b in s['temporal']: weights[b] = weights.get(b,0.)-(c+3)/s['tau_n']**2
    for side in s['sides']:
        for b in side['selected']: weights[b] = weights.get(b,0.)+c/(len(side['selected'])*s['tau_m']**2)
    s['support'] = sorted(weights,key=lambda b:marks[b])
    s['weights'] = [weights[b] for b in s['support']]
    return s


def relabel(relation, marks, bottom, top, rho, cfg, stencils, seed):
    perm = np.random.default_rng(seed+917).permutation(len(marks)); inv = np.argsort(perm)
    h = core.Poset(relation[np.ix_(perm,perm)], marks[perm])
    for name, fn in [('legacy64', core.neighborhood), ('balanced64', estimator.neighborhood)]:
        original = stencils[name]
        s = fn(h, rho, int(inv[bottom]), int(inv[top]), cfg)
        assert s['status'] == original['status']
        assert [int(perm[b]) for b in s['chain']] == original['chain']
        if 'sides' in s:
            for a,b in zip(s['sides'], original['sides']):
                assert [int(perm[i]) for i in a['shell']] == b['shell']
                assert [int(perm[i]) for i in a['selected']] == b['selected']
                assert a['diagnostics'] == b['diagnostics']
                assert [x is None for x in a['distances']] == [x is None for x in b['distances']]
                np.testing.assert_allclose([x or 0 for x in a['distances']], [x or 0 for x in b['distances']], rtol=1e-10, atol=1e-12)
        if s['status'] == 'ok':
            assert [int(perm[i]) for i in s['support']] == original['support']
            np.testing.assert_allclose(s['weights'], original['weights'], rtol=1e-10, atol=1e-12)
            a = core.intrinsic_chart(h,s,rho,int(inv[bottom]),cfg)
            g = core.Poset(relation,marks)
            b = core.intrinsic_chart(g,original,rho,bottom,cfg)
            assert a['status'] == b['status']
            if a['status'] == 'ok':
                assert [int(perm[i]) for i in a['landmarks']] == b['landmarks']
                np.testing.assert_allclose(a['fields'][inv],b['fields'],rtol=1e-10,atol=1e-12)
    return True


def run_cloud(rho, seed, cfg, do_relabel=False):
    start = time.monotonic()
    z, relation, marks, bottom, top = experiment.sprinkle(rho,seed)
    g = core.Poset(relation,marks); stencils = {}; evaluations = {}; timings = {}
    for name,fn in [('legacy64',core.neighborhood),('balanced64',estimator.neighborhood)]:
        tick = time.monotonic()
        stencils[name] = fn(g,rho,bottom,top,cfg)
        evaluations[name] = experiment.evaluate(g,z,stencils[name],rho,bottom,cfg)
        timings[name] = time.monotonic()-tick
    tick = time.monotonic()
    stencils['oracle_cap'] = oracle_cap(z,marks,stencils['balanced64'],cfg)
    evaluations['oracle_cap'] = experiment.evaluate(g,z,stencils['oracle_cap'],rho,bottom,cfg)
    timings['oracle_cap'] = time.monotonic()-tick
    rescued = 0; missing_before = 0
    for a,b in zip(stencils['legacy64'].get('sides',[]),stencils['balanced64'].get('sides',[])):
        assert a['shell'] == b['shell']
        rescued += sum(x is None and y is not None for x,y in zip(a['distances'],b['distances']))
        missing_before += sum(x is None for x in a['distances'])
    passed = relabel(relation,marks,bottom,top,rho,cfg,stencils,seed) if do_relabel else None
    return dict(rho=rho,seed=seed,poisson_count=len(z)-2,
                coordinates_sha256=hashlib.sha256(z.tobytes()).hexdigest(),
                relation_sha256=hashlib.sha256(relation.tobytes()).hexdigest(),
                marks_sha256=hashlib.sha256(marks.tobytes()).hexdigest(),
                stencils=stencils,evaluations=evaluations,rescued_distances=rescued,
                legacy_missing_distances=missing_before,relabel_pass=passed,
                method_seconds=timings,seconds=time.monotonic()-start)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--mode',choices=['development','test'],required=True)
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args(); audit,cfg = config()
    if args.output.exists(): raise SystemExit('Output exists: refusing overwrite')
    sha = subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    hashes = sources()
    if args.mode == 'test':
        for path,digest in hashes.items():
            data = subprocess.check_output(['git','show',sha+':'+path],cwd=ROOT)
            if hashlib.sha256(data).hexdigest() != digest: raise SystemExit('Unfrozen source '+path)
    args.output.mkdir(parents=True)
    execution = dict(mode=args.mode,source_commit=sha,source_sha256=hashes,numpy=np.__version__,
                     scipy=scipy.__version__,records=[],status='RUNNING')
    def save(): (args.output/'execution.json').write_text(json.dumps(execution,indent=2)+'\n')
    save(); start = time.monotonic()
    def timeout(signum,frame): raise TimeoutError('fixed wall budget exhausted')
    signal.signal(signal.SIGALRM,timeout); signal.alarm(audit['wall_budget_seconds'])
    try:
        for i,rho in enumerate(audit['densities']):
            seeds = audit['development_seeds'] if args.mode == 'development' else [audit['test_seed_base']+100*i+j for j in range(audit['test_replicates_per_density'])]
            for j,seed in enumerate(seeds):
                record = run_cloud(rho,seed,cfg,do_relabel=(j==0))
                name = f'rho-{rho}-seed-{seed}.json'; data = encode(record)
                (args.output/name).write_text(data)
                execution['records'].append(dict(file=name,sha256=hashlib.sha256(data.encode()).hexdigest()))
                save()
                print(json.dumps(dict(rho=rho,seed=seed,seconds=round(record['seconds'],2),rescued=record['rescued_distances'],
                    status={k:v['status'] for k,v in record['evaluations'].items()})),flush=True)
                if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024 > audit['memory_budget_mib']:
                    raise MemoryError('fixed memory budget exhausted')
        execution['status'] = 'COMPLETE'
    except (TimeoutError,MemoryError) as error:
        execution.update(status='BUDGET_HOLD',reason=str(error))
    except Exception as error:
        execution.update(status='ERROR',reason=repr(error)); raise
    finally:
        signal.alarm(0)
        execution.update(seconds=time.monotonic()-start,peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024)
        save()
    if execution['status'] != 'COMPLETE': raise SystemExit(2)


if __name__ == '__main__': main()
