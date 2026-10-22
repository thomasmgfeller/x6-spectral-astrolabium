"""Algebraic controls and archived-grid decision audit.
SPDX-License-Identifier: Apache-2.0
"""
from rs_run import *

def audit():
    c=read(HERE/'contract.json');rows=read(HERE/'candidates.json');bases=read(HERE/'bases.json');s=read(HERE/'summary.json')
    assert [(r['a'],r['relative_step']) for r in rows]==[(a,d) for a in c['base_parameters'] for d in c['relative_steps']]
    # Independent scalar null-coordinate group law, including inverse and tips.
    checks=0
    f=lambda k,u:(u+k)/(1+k*u)
    for a in map(F,c['base_parameters']):
        for d in map(F,c['relative_steps']):
            b=(a+d)/(1+a*d)
            assert (b-a)/(1-a*b)==d
            for u in [F(-1),F(-3,4),F(0),F(2,3),F(1)]:
                assert f(d,f(a,u))==f(b,u)
                assert f(-a,f(a,u))==u
                checks+=2
    selected=max((i for i,r in enumerate(rows) if r['eligible']),key=lambda i:F(rows[i]['relative'][0]))
    assert selected==s['selected_row']
    assert s['eligible']==sum(r['eligible'] for r in rows)
    assert s['selected']==rows[selected]
    assert s['status']==('STRONG_PAIR_FOUND' if any(r['strong'] for r in rows) else 'NO_STRONG_PAIR_IN_FIXED_SCAN')
    old=read(HERE.parent/'conformal_transport'/'summary.json')['selected']
    zero=next(r for r in rows if r['a']=='0' and r['relative_step']==old['k'])
    assert zero['relative']==old['relative'] and zero['base_normalized']==old['base_normalized']
    # Reproduce exact zero-reference sensitivity from the previous certificate.
    previous=read(HERE.parent/'conformal_sensitivity'/'summary.json')['local_sensitivity']
    assert next(b for b in bases if b['a']=='0')['local']==previous
    return dict(status='PASS',scalar_group_and_inverse_checks=checks,grid_complete=True,selection_recomputed=True,previous_gap_reproduced=True,previous_derivative_reproduced=True,
                scope='Independent scalar group controls and decision audit; rational coordinate/weight replay is rs_run.py --verify.')

if __name__=='__main__':
    result=audit()
    if '--verify' in sys.argv:assert result==read(HERE/'audit.json')
    else:save(HERE/'audit.json',result)
    print(json.dumps(result))
