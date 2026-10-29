"""Audit exact prediction targets, nonlinear remainder bounds and scope gates."""
import json,unittest
from flint import arb,acb,ctx
from run import HERE,unpack,freeze_check,encode
from kernel import require
import test_transfer


def balls(obj,prefix=''):
    if isinstance(obj,dict) and set(obj)=={'re','im'}:
        yield prefix,unpack(obj)
    elif isinstance(obj,dict):
        for k,v in obj.items():yield from balls(v,prefix+'/'+k)
    elif isinstance(obj,list):
        for i,v in enumerate(obj):yield from balls(v,prefix+'/'+str(i))

def target_inventory(doc):
    out={}
    for group in ['skeleton','oscillator','original_source']:
        for path,z in balls(doc[group],group):
            if any(k in path for k in ['upper','lower','cutoff','cutoffs','count_states','elapsed']):continue
            out[path]=z
    return out

def verify():
    ctx.prec=256;freeze_check();p=json.loads((HERE/'PROTOCOL.json').read_text())
    docs=[json.loads((HERE/'results'/f'PREDICTIONS_{bits}.json').read_text()) for bits in p['precision_bits']]
    inv=[target_inventory(d) for d in docs];require(inv[0].keys()==inv[1].keys(),'same target inventory')
    for name,z in inv[0].items():
        require(z.overlaps(inv[1][name]),'same exact prediction target '+name)
        require(max(z.real.rad(),z.imag.rad())<arb(p['exact_target_radius_goal']),'prediction certificate radius '+name)
    audit=json.loads((HERE/'results/COUNT_SUM_DIAGNOSTIC.json').read_text());d=docs[1]
    maxdiff=arb(0)
    for name in ['mean','covariance','relation']:
        def compare(exact,approx):
            nonlocal maxdiff
            if isinstance(exact,dict) and 're' in exact:
                diff=(unpack(exact)-acb(complex(*approx))).abs_upper();maxdiff=max(maxdiff,diff)
            else:
                for x,y in zip(exact,approx):compare(x,y)
        compare(d['skeleton'][name],audit[name])
    require(maxdiff<arb(p['count_sum_audit_tolerance']),'independent finite Poisson sum diagnostic')
    for doc in docs:
        require(doc['new_random_clouds']==doc['fitted_parameters']==0,'no empirical calibration')
        require(doc['original_ensemble_moments']=='NOT_EVALUATED' and doc['nonlocal_ensemble']=='MODEL_HOLD','no false ensemble closure')
        r=doc['skeleton'];mu=[unpack(x) for x in r['mean']]
        for i in range(2):
            require((sum(unpack(row[i]) for row in r['order_means'])-mu[i]).contains(0),'order means telescope')
            require(unpack(r['order_means'][1][i]).contains(0),'centered linear term')
            require(unpack(r['mean_shift'][i]).abs_upper()<=unpack(r['linear_remainder_L2_upper'][i]).real,'mean remainder')
            for j in range(2):
                C=unpack(r['covariance'][i][j]);P=unpack(r['relation'][i][j]);bound=unpack(r['linear_covariance_error_upper'][i][j]).real
                require((C-unpack(r['covariance'][j][i]).conjugate()).contains(0),'Hermitian covariance')
                require((P-unpack(r['relation'][j][i])).contains(0),'symmetric relation')
                require((C-unpack(r['linear_covariance'][i][j])).abs_upper()<=bound,'covariance remainder')
                require((P-unpack(r['linear_relation'][i][j])).abs_upper()<=bound,'relation remainder')
        require(unpack(r['covariance_determinant']).real>0,'positive covariance determinant')
        require(all(unpack(v).real>arb('.001') for v in doc['original_source']['RMS_error_lower']),'original local RMS obstruction')
        require(unpack(doc['original_source']['nonlocal_adapter_fewer_than_four_history_points_probability']).real>0,'positive failure probability')
        box=doc['general_overlap_control'];require(unpack(box['volume_enclosure']).contains(unpack(box['analytic_volume'])),'generic geometry encloses exact overlap')
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_transfer)
    result=unittest.TextTestRunner(verbosity=1).run(suite);require(result.wasSuccessful(),'analytical controls')
    summary={'status':'PASS','analytical_tests':result.testsRun,'enclosed_prediction_comparisons':len(inv[0]),
             'count_sum_states':audit['count_states'],'count_sum_max_abs_difference':float(maxdiff),
             'max_exact_target_component_radius':max(float(max(z.real.rad(),z.imag.rad()).upper()) for z in inv[0].values()),
             'control_status':'PREDICTIVE_MEAN_COVARIANCE_AND_RELATION_CERTIFIED',
             'original_local_status':'ZERO_SOURCE_MOMENT_CONSTRAINTS_AND_TRUNCATION_BOUNDS_CERTIFIED',
             'original_ensemble_moments':'NOT_EVALUATED','nonlocal_ensemble':'MODEL_HOLD',
             'overall_status':'METHOD_HOLD','G1':'HOLD'}
    (HERE/'results/CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n');return summary

if __name__=='__main__':print(json.dumps(verify(),indent=2))
