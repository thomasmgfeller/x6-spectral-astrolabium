"""Validate published enclosures, signed ledgers and separated conclusions."""
import hashlib
import json
import unittest
from collections import Counter
from flint import arb,acb,ctx
from run import HERE,gzread,unpack
import continuum
import test_continuum,test_ledger


def verify():
    ctx.prec=256;p=json.loads((HERE/'PROTOCOL.json').read_text())
    for n,h in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        continuum.require(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h,'input integrity '+n)
    docs=[gzread(HERE/'results'/f'BENCHMARK_{b}.json.gz') for b in p['precision_bits']]
    comparisons=0;ledgers=0
    for doc in docs:
        continuum.require(doc['new_random_clouds']==doc['new_causal_nodes']==0,'no new samples')
        continuum.require([r['key'] for r in doc['rows']]==p['clouds'],'complete archive inventory')
        for r in doc['reference']['windows']:
            z=unpack(r['normalized_value'])
            continuum.require(max(z.real.rad(),z.imag.rad())<=arb(p['reference_radius_goal']),'full reference radius')
            continuum.require(z.abs_lower()>0,'nonzero continuum response')
            core=unpack(r['normalized_core'])
            e=unpack(r['source_tail_upper']).real+unpack(r['bessel_tail_upper']).real
            # Serialization may widen the enclosing rectangle, but not erase its tails.
            continuum.require(z.overlaps(continuum.inflate(core,e)),'reference tail inclusion')
        for row in doc['rows']:
            continuum.require(len(row['oracle_history'])==row['history_nodes'],'complete history oracle')
            for wi,w in enumerate(row['windows']):
                continuum.require(w['time_window']==p['time_windows'][wi],'unchanged detector windows')
                reference=unpack(doc['reference']['windows'][wi]['normalized_value'])
                for m in w['models']:
                    pieces={k:unpack(v['value']) for k,v in m['components'].items()}
                    total=unpack(m['total_error']);numeric=unpack(m['numeric_response'])
                    continuum.require((sum(pieces.values())-total).contains(0),'signed sum')
                    continuum.require(total.overlaps(numeric-reference),'direct total error')
                    continuum.require(pieces['integration'].overlaps(sum(unpack(v) for v in m['integration_subparts'].values())),'integration subdivision')
                    for k,z in pieces.items():
                        lo=unpack(m['components'][k]['magnitude']['lower']).real
                        hi=unpack(m['components'][k]['magnitude']['upper']).real
                        continuum.require(lo>=0 and hi>=lo and lo<=z.abs_upper() and hi>=z.abs_lower(),'magnitude bounds')
                    if m['dominant_component']!='UNRESOLVED':
                        key=m['dominant_component']
                        lower=unpack(m['components'][key]['magnitude']['lower']).real
                        others=sum(unpack(v['magnitude']['upper']).real for k,v in m['components'].items() if k!=key)
                        continuum.require(lower>others,'strict dominance certificate')
                    continuum.require(m['solution_budget_pass']==bool(unpack(m['components']['solution']['magnitude']['upper']).real<=arb(p['solution_tolerance'])),'solution decision')
                    continuum.require(m['total_accuracy_pass']==bool(total.abs_upper()<=arb(p['comparison_tolerance'])),'total decision')
                    if row['source_support_hits']==0 and m['adapter']=='local_H1':
                        continuum.require(numeric.is_zero() and pieces['integration'].is_zero() and pieces['solution'].is_zero(),'empty source exact controls')
                    ledgers+=1
    for a,b in zip(docs[0]['reference']['windows'],docs[1]['reference']['windows']):
        for k in ['normalized_core','normalized_value','physical_value']:
            continuum.require(unpack(a[k]).overlaps(unpack(b[k])),'same continuum target');comparisons+=1
    for r,s in zip(docs[0]['rows'],docs[1]['rows']):
        continuum.require(r['coordinates_sha256']==s['coordinates_sha256'] and r['counts_sha256']==s['counts_sha256'],'same geometry')
        for x,y in zip(r['oracle_history'],s['oracle_history']):
            continuum.require(unpack(x).overlaps(unpack(y)),'same KG history');comparisons+=1
        for a,b in zip(r['windows'],s['windows']):
            for m,n in zip(a['models'],b['models']):
                continuum.require(m['dominant_component']==n['dominant_component'],'same attribution decision')
                for k in ['numeric_response','ideal_adapter_response','continuum_oracle_discrete_response','total_error']:
                    continuum.require(unpack(m[k]).overlaps(unpack(n[k])),'same target '+k);comparisons+=1
                for k in m['components']:
                    continuum.require(unpack(m['components'][k]['value']).overlaps(unpack(n['components'][k]['value'])),'same error component');comparisons+=1
    suite=unittest.TestSuite([unittest.defaultTestLoader.loadTestsFromModule(module) for module in [test_continuum,test_ledger]])
    result=unittest.TextTestRunner(verbosity=1).run(suite)
    continuum.require(result.wasSuccessful(),'analytical controls')
    ctx.prec=256;doc=docs[1]
    models=[m for r in doc['rows'] for w in r['windows'] for m in w['models']]
    upper=lambda z:float(unpack(z).real.upper())
    summary={'status':'PASS','analytical_tests':result.testsRun,'enclosed_target_comparisons':comparisons,
        'signed_ledgers_checked':ledgers,'oracle_history_nodes_per_precision':sum(r['history_nodes'] for r in doc['rows']),
        'reference_status':'FULL_SCALAR_REFERENCE_READY',
        'reference_max_component_radius_upper':max(float(max(unpack(w['normalized_value']).real.rad(),unpack(w['normalized_value']).imag.rad()).upper()) for w in doc['reference']['windows']),
        'solution_error_max_upper':max(upper(m['components']['solution']['magnitude']['upper']) for m in models),
        'solution_budget_pass':sum(m['solution_budget_pass'] for m in models),'total_accuracy_pass':sum(m['total_accuracy_pass'] for m in models),
        'evaluations':len(models),'dominance':{name:dict(Counter(m['dominant_component'] for m in models if m['adapter']==name)) for name in p['adapters']},
        'operator_domain_above_tolerance':sum(unpack(w['models'][0]['components']['operator_domain']['magnitude']['lower']).real>arb(p['comparison_tolerance']) for r in doc['rows'] for w in r['windows']),
        'overall_status':'METHOD_HOLD','G1':'HOLD'}
    (HERE/'results/CHECKS.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary


if __name__=='__main__':print(json.dumps(verify(),indent=2))
