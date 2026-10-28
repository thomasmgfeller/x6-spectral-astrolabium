"""Independent output/decision audit; compare targets, never bound-to-bound overlap."""
import gzip
import hashlib
import json
from pathlib import Path
import unittest
from flint import arb,acb,ctx
import numpy as np
import adapter
import test_adapter

HERE=Path(__file__).resolve().parent

def unpack(v):return acb(arb(v[0]),arb(v[1]))
def require(v,msg):
    if not v:raise AssertionError(msg)


def verify():
    ctx.prec=256
    p=json.loads((HERE/'PROTOCOL.json').read_text())
    for name,expected in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        require(hashlib.sha256((HERE/name).read_bytes()).hexdigest()==expected,'freeze '+name)
    docs=[json.load(gzip.open(HERE/'results'/f'BENCHMARK_{bits}.json.gz','rt')) for bits in p['precision_bits']]
    archive=np.load(HERE.parent/'scalar_pilot_v0_1/results/clouds.npz')
    comparisons=0
    for doc in docs:
        require([r['key'] for r in doc['rows']]==p['clouds'],'all archive slots')
        require(doc['new_causal_nodes']==doc['new_random_clouds']==0,'unchanged sampling')
        for r in doc['rows']:
            original=archive[r['key']]
            # Predecessor digest includes dtype and shape; exact formula below is imported.
            import sys
            sys.path.insert(0,str(HERE.parent/'detector_methods_v0_10'))
            from common10 import digest
            require(digest(original)==r['coordinates_sha256'],'archive hash')
            x=original[original[:,0]<=-1]
            mesh=adapter.certify_mesh(x[:,1:])
            require(adapter.ball_covered(mesh)==r['source_ball_covered'],'source coverage')
            require(hashlib.sha256(json.dumps(mesh['tetrahedra']).encode()).hexdigest()==r['mesh_sha256'],'exact certified mesh')
            require([l['depth'] for l in r['levels']]==p['depths'],'all levels')
            for l in r['levels']:
                require(l['leaf_tetrahedra']==r['tetrahedra']*2**l['depth'],'all tetrahedral leaves')
                for z,passed in zip(l['relative_L2_projection_error'],l['resolution_pass']):
                    require(bool(z is not None and unpack(z).real<=arb(p['spatial_relative_L2_tolerance']))==passed,'L2 decision')
                for w in l['windows']:
                    for z,passed in zip(w['history_error_upper'],w['history_budget_pass']):
                        e=unpack(z).real
                        require(e>=0,'nonnegative history upper bound')
                        require(bool(e<=arb(p['detector_history_tolerance']))==passed,'history decision')
                    for z,passed in zip(w['responses'],w['integration_budget_pass']):
                        z=unpack(z)
                        require(bool(max(z.real.rad(),z.imag.rad())<=arb(p['combined_integration_radius_tolerance']))==passed,'integration decision')
        good=all(r['source_ball_covered'] and all(r['levels'][-1]['resolution_pass']) and all(all(w['history_budget_pass']) and all(w['integration_budget_pass']) for w in r['levels'][-1]['windows']) for r in doc['rows'])
        require(doc['decision']==('DEVELOPMENT_BUDGETS_ONLY' if good else 'METHOD_HOLD'),'overall decision')
    for r,s in zip(docs[0]['rows'],docs[1]['rows']):
        for key in ['coordinates_sha256','history_nodes','tetrahedra','mesh_sha256','source_support_hits','source_ball_covered']:
            require(r[key]==s[key],'same geometry and inventory')
        for l,m in zip(r['levels'],s['levels']):
            require(l['resolution_pass']==m['resolution_pass'],'same L2 decisions')
            for rr,ss in zip(l['coefficient_enclosures'],m['coefficient_enclosures']):
                for x,y in zip(rr,ss):
                    require(unpack(x).overlaps(unpack(y)),'same projected coefficient');comparisons+=1
            for x,y in zip(l['relative_L2_projection_error'],m['relative_L2_projection_error']):
                if x is not None:require(unpack(x).overlaps(unpack(y)),'same L2 residual');comparisons+=1
            for w,v in zip(l['windows'],m['windows']):
                require(w['history_budget_pass']==v['history_budget_pass'],'same history decisions')
                require(w['integration_budget_pass']==v['integration_budget_pass'],'same integration decisions')
                for x,y in zip(w['responses'],v['responses']):
                    require(unpack(x).overlaps(unpack(y)),'same detector target');comparisons+=1
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_adapter)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    require(result.wasSuccessful(),'analytic controls')
    ctx.prec=256
    rows=docs[1]['rows'];last=[r['levels'][-1] for r in rows]
    summary={'status':'PASS','analytical_tests':result.testsRun,'enclosed_target_comparisons':comparisons,
        'clouds':len(rows),'source_ball_covered':sum(r['source_ball_covered'] for r in rows),
        'previously_empty_source_clouds':[r['key'] for r in rows if r['source_support_hits']==0],
        'source_non_erasure_certificates':sum(r['source_not_erased_by_exact_projection'] for r in rows),
        'spatial_budget_pass':sum(sum(l['resolution_pass']) for l in last),'spatial_budget_total':40,
        'spatial_definite_fail':sum(unpack(v).real>arb(p['spatial_relative_L2_tolerance']) for l in last for v in l['relative_L2_projection_error'] if v is not None),
        'history_budget_pass':sum(sum(w['history_budget_pass']) for l in last for w in l['windows']),'history_budget_total':80,
        'integration_budget_pass':sum(sum(w['integration_budget_pass']) for l in last for w in l['windows']),'integration_budget_total':80,
        'decision':docs[1]['decision'],'G1':'HOLD',
        'condition_upper_range_display':[min(float(unpack(r['coefficient_condition_upper']).real.upper()) for r in rows),max(float(unpack(r['coefficient_condition_upper']).real.upper()) for r in rows)]}
    (HERE/'results'/'CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':print(json.dumps(verify(),indent=2))
