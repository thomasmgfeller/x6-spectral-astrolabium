"""Independent checks of the post-screen two-count event.
SPDX-License-Identifier: Apache-2.0
"""
from cm_joint import *
from decimal import Decimal
from jr_audit import decimal_reference

def audit_joint():
    cert,summary=joint()
    assert cert==read(HERE/'joint_certificate.json')
    assert summary==read(HERE/'joint_summary.json')
    c=read(HERE/'joint_contract.json');checks=0
    for block in cert['event_records']:
        for row in block:
            answer=decimal_reference(F(row['x_mean']),F(row['y_mean']),2,891)
            lo,hi=map(Decimal,row['probability']);assert lo<=answer<=hi
            assert F(row['numerical_width_upper'])<=F('1e-65')
            assert all(int(row['normalization'][name]['tail'])>0 for name in ('x','y'))
            checks+=1
    # Reject falsely factoring dependent, identical Poisson counts:
    # X=Y gives P(Y-X<=0)=1, while the independent law gives less than 1.
    probability,_=jr.event(F(1),F(1),1,0,c)
    assert probability[1]<1
    w,z,ends=geometry();rows=read(HERE/'candidates.json');row=rows[c['candidate']]
    ray=read(HERE/'directions.json')[row['ray']];zz=moved(z,ray,F(row['step']))
    assert zz[:5]==z[:5]
    assert gap(exact_weights(z,F(w['scale'])),exact_weights(zz,F(w['scale'])))['relative']==cert['gap']
    assert certify_order(zz,w['full_order'])==row['order']
    assert intrinsic_gates(zz,exact_weights(zz,F(w['scale'])),F(w['scale']))==row['intrinsic_gates']
    p,q=[tuple(map(F,v)) for v in cert['event_probability']]
    assert F(1,4)<F(cert['full_law_tv_lower'])<=p[0]-q[1]
    assert sum(summary['initial_screen'].values())==420
    assert summary['initial_screen']['HOLD']==summary['newly_excluded']==1
    assert summary['unresolved_indices']==[]
    return dict(status='PASS',independent_110_digit_joint_pmf_checks=checks,
                infinite_tail_retained=True,dependence_negative_control=True,
                exact_candidate_geometry_and_weights_replayed=True,
                original_screen_preserved=True,scope='One paired point; not continuous coverage.')

if __name__=='__main__':
    result=audit_joint()
    if '--verify' in sys.argv:assert result==read(HERE/'joint_audit.json')
    else:save(HERE/'joint_audit.json',result)
    print(json.dumps(result))
