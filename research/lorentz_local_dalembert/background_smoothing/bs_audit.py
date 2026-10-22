"""Independent common-box membership and residual/smoothing controls.
SPDX-License-Identifier: Apache-2.0
"""
from bs_run import *
from itertools import product
from sf_audit import point_bits

def audit():
    boxes=read(HERE/'background.json.gz');c=read(HERE/'contract.json');w,z,ends,selected=geometry()
    changed=[row[:] for row in z];changed[selected['node']][1]+=F(selected['step'])
    unit=c['coordinate_unit'];factor=F(w['rho'])*F(w['scale'])**3/unit**3
    base={k:F(v) for k,v in boxes['original_background'].items()};best=dict(base);chosen={}
    for row in boxes['certified_boxes']:
        assert all(a<b for a,b in zip(row['lower'],row['upper']))
        mean=factor*__import__('math').prod(b-a for a,b in zip(row['lower'],row['upper']))
        assert mean==F(row['mean'])
        label=row['label'];best[label]=max(best.get(label,F(0)),mean)
        if label not in chosen or mean>F(chosen[label]['mean']):chosen[label]=row
    assert {k:str(v) for k,v in best.items()}==boxes['background']
    checks=0
    for label,row in chosen.items():
        for coords in list(product([F(0),F(1)],repeat=3))+[(F(1,2),)*3]:
            p=[F(a+f*(b-a),unit) for a,b,f in zip(row['lower'],row['upper'],coords)]
            for g in [z,changed]:assert point_bits(p,g,ends)==label;checks+=1
    # Separate marginal lower volumes must not be mistaken for common diagonal mass.
    toytable={('a','b'):(F(2),F(2))}
    diagonal=original_background([{'a':F(7),'b':F(5)},{'a':F(5),'b':F(7)}],toytable,F(1))
    assert diagonal=={'a':F(4),'b':F(4)}
    # With ample diagonal background, the Hellinger method really can improve coupling.
    exact=law({'a':F(100),'b':F(100)},{('a','b'):(F(1),F(1))},F(0))
    assert F(exact['tv_upper'])<F(71,1000) and F(exact['known_coupling_tv_upper'])>F(63,100)
    # Unknown transfers still impose the coupling term even for empty known table.
    missing=law({}, {},F(1,4));assert F(missing['tv_upper'])>F(22,100)
    with_residual=law({'a':F(100),'b':F(100)},{('a','b'):(F(1),F(1))},F(1,20))
    assert F(with_residual['tv_upper'])>F(exact['tv_upper'])
    # These residual probabilities combine multiplicatively, not by dropping bad labels.
    bad=F(outward(void_bounds(F(1,20))[1])[1]);known=F(with_residual['known_component_tv_upper'])
    assert abs(F(with_residual['tv_upper'])-(bad+(1-bad)*known))<F(1,10**18)
    rejected=0
    for b,t,r in [({'a':F(-1)},{},F(0)),({}, {('a','b'):(F(-1),F(0))},F(0)),({}, {},F(-1))]:
        try:law(b,t,r)
        except AssertionError:rejected+=1;continue
        raise AssertionError('invalid inputs accepted')
    summary=read(HERE/'summary.json');assert summary['positive_background_labels']==158
    methods=read(HERE/'methods.json');assert F(methods['local_background']['known_hellinger_tv_upper'])<F(methods['inherited_background']['known_hellinger_tv_upper'])
    assert summary['status']=='HOLD_BACKGROUND_SMOOTHING' and summary['tv_upper']==summary['previous_tv_upper']
    return dict(status='PASS',maximal_common_boxes_checked=len(chosen),exact_scalar_membership_checks=checks,
        no_overlap_summing=True,marginal_to_diagonal_control=True,positive_smoothing_control=exact,
        unresolved_mass_control=missing,invalid_inputs_rejected=rejected,
        scope='Whole-box interval certificates establish common positive intensity. Scalar corner/center tests audit implementation; common positivity alone does not imply a useful smoothing gain.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
