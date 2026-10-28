"""Replay the deterministic admission decision and its analytical unit controls."""
import json
import unittest
from flint import arb, ctx
import admission as a
import test_admission


def compare(x, y):
    if isinstance(x,dict):
        a.require(x.keys()==y.keys(),'same decision inventory')
        for k in x:
            if k!='precision_bits': compare(x[k],y[k])
    elif isinstance(x,list):
        a.require(len(x)==len(y),'same list size')
        for u,v in zip(x,y): compare(u,v)
    elif isinstance(x,str):
        try: left,right=arb(x),arb(y)
        except (ValueError,TypeError): a.require(x==y,'same decision text')
        else: a.require(left.overlaps(right),'same enclosed structural quantity')
    else: a.require(x==y,'same exact decision')


def verify():
    a.freeze_check()
    docs=[a.read(a.HERE/'results'/f'DECISION_{b}.json') for b in [128,192]]
    for bits, doc in zip([128,192],docs): compare(doc,a.compute(bits))
    ctx.prec=256; compare(*docs)
    suite=unittest.defaultTestLoader.loadTestsFromModule(test_admission)
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    a.require(result.wasSuccessful(),'admission controls')
    for d in docs:
        a.require(d['admission']=='REJECTED_FOR_CONFIRMATORY_RUN','concrete no-go')
        a.require(d['macroscopic_decision']['previous_operator_rejected_fields']==9,'old operator evidence remains separate')
    return {'status':'PASS','analytical_tests':result.testsRun,'precision_bits':[128,192],
            'decision_replayed':True,'new_random_clouds':0,'new_rng_calls':0,
            'admission':'REJECTED_FOR_CONFIRMATORY_RUN',
            'fluctuation_decision':'NOT_TESTED_METHOD_GATE_FAILED',
            'macroscopic_mean':'NOT_ESTABLISHED','overall_status':'METHOD_HOLD','G1':'HOLD'}


if __name__=='__main__':
    result=verify();(a.HERE/'results/CHECKS.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
