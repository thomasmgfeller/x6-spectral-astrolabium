"""Offline replay of the conditional area control and the N19 eligibility test."""
from fractions import Fraction as F
from hashlib import sha256
from pathlib import Path
import json

from klassische_kontrolle import control
from ereignisschnitt import mesh_audit

ROOT=Path(__file__).resolve().parent


def read(name):
    return json.loads((ROOT/name).read_bytes())


def study():
    for name,entry in read('Quellen.json').items():
        if sha256((ROOT/name).read_bytes()).hexdigest()!=entry['sha256']:
            raise ValueError('source mismatch '+name)
    witness = read('basis/N15_Radiuszeuge.json')
    a, b = (F(witness['radii'][side]) for side in ('A', 'B'))
    estimate = 2 * a * b / (a + b)
    error = (b - a) / (a + b)
    assert estimate / a - 1 == 1 - estimate / b == error
    assert estimate == F(witness['minimax_estimate']) == F(1683, 184)
    assert error == F(witness['minimax_relative']) == F(7, 92)
    n15_witness = {'radii': [str(a), str(b)], 'minimax_estimate': str(estimate),
                   'relative_error': str(error), 'scope': 'kinematic_pair'}
    refs=read('basis/Zwei_Massen.json')
    classical=control()
    for case in classical['cases']:
        target=refs['p3_reference_check']['reference'][case['model_mass']]
        tlo,thi=map(F,target['radius_bounds_exact'])
        lo,hi=map(F,case['radius_interval'])
        assert F(95,100)*thi<=lo<=tlo<=thi<=hi<=F(105,100)*tlo
    n15=read('basis/Eichstand.json')['physical_CST']
    n19=read('basis/Paar.json')
    gate=refs['physical']
    assert all(n15[k] is None for k in ('physical_vacuum','independent_mass_pair','gain'))
    assert n19['post_hoc_source'] and n19['operational_radius'] is None
    assert all(gate[k] is None for k in ('radius_M_1_4','radius_M_4','weight_uniform_radius_intervals'))
    p3=read('basis/P3.json')
    assert len(p3)==60 and all(r['execution']=='NOT_RUN' for r in p3)
    selected=[r for r in p3 if r['checkpoint_context']['M'] in ('1/4','4') and r['checkpoint_context']['x']=='1/2']
    pairs={(r['checkpoint_context']['M'],r['checkpoint_context']['density_ratio']) for r in selected}
    assert len(selected)==8 and pairs=={(m,k) for m in ('1/4','4') for k in (1,2,4,8)}
    mesh=mesh_audit(read('basis/Driftzertifikat.json'))
    records=[{'sector':r['checkpoint_context'],'original_execution':r['execution'],
              'original_eligibility':r['gates']['CORRESPONDENCE']['eligibility']['outcome'],
              'physical_radius':None} for r in selected]
    return {'n15_witness':n15_witness,'classical_control':classical,'n19_finite_test':mesh,'CST_two_mass_pilot':
            {'status':'HOLD_NOT_ELIGIBLE','radius_evaluation':'NOT_RUN','P3_registered':len(p3),'rows':records,
             'independent_mass_and_vacuum':False,'same_history_material_surface_and_area_established':False,
             'radius_range_over_admissible_weights':None,'dynamical_indistinguishable_pair':'NOT_ESTABLISHED'}}


def raw(value):
    return (json.dumps(value,ensure_ascii=False,indent=2,sort_keys=True)+'\n').encode()


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Python ohne -O starten.')
    for name in ('SHA256SUMS','Pruefplan.sha256','Ergaenzung.sha256'):
        for line in (ROOT/name).read_text().splitlines():
            expected,f=line.split('  ',1)
            if sha256((ROOT/f).read_bytes()).hexdigest()!=expected:
                raise SystemExit('FAIL '+f)
    assert (ROOT/'Ergebnisse.json').read_bytes()==raw(study())
    print('PASS – N15-Minimaxwert 7/92, klassische gemeinsame Auslese und endliche N19-Ordnungsprüfung.')
    print('Physischer Radiuspilot HOLD_NOT_ELIGIBLE. Acht Zielwerte und alle 60 P3-Einträge NOT_RUN.')
