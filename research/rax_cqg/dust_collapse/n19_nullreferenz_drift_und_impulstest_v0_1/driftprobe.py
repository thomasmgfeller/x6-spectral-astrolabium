"""Known-truth drift trials, calibration confounding and registry controls."""
from copy import deepcopy
from fractions import Fraction as F
from drifteichung import PATTERN,evaluate


def fixture(true_scale=2350,apparent=2400,irregular=False):
    from eichprobe import fixture as old_fixture
    from eichen import MU
    from intervall import around,relative
    doc=old_fixture(F(true_scale))
    for d in doc['devices']:
        k=F(d['kappa']);g=1/(2*k*MU*true_scale);false=1/(2*k*MU*apparent)
        d['kg']=relative(2*k*MU*true_scale,F(3,100)).data()
        for role,width,level in [('fit',F(1,10),1),('hold',F(2,5),3),('zero',0,0)]:
            base=F(3,40000)*k*level
            eff=base*(1-F(width)/4)
            rows=[]
            for i,sign in enumerate(PATTERN):
                t=F(i)+(F(i%3,17) if irregular else 0)
                c=(false-g)*eff
                noise=F(1,10**8)+F(1,10**9)*t+c*t*t
                q0=F(2-i,7);v=F(i*i-3,13)
                q2=q0+2*v+g*sign*eff+noise
                rows.append({'block_time':str(t),'dust_source':'0','error_reference':'synthetic controlled bound',
                             'nonquadratic_error_q':'0',
                             'positions_q':[around(z,F(1,10**12)).data() for z in (q0,q0+v,q2)],
                             'impulse_segments':[{'start':str(-F(width)/2),'end':str(F(width)/2),
                                                  'total_Ns':relative(sign*base,F(1,1000)).data()}]})
            d['blocks'][role]=rows
    return doc


def run():
    from eichen import evaluate as legacy
    from intervall import interval,around
    doc=fixture()
    old=deepcopy(doc)
    for device in old['devices']:
        device['blocks']={role:rows[:4] for role,rows in device['blocks'].items()}
    first=legacy(old)
    second=evaluate(doc)
    uneven=evaluate(fixture(irregular=True))
    assert first['scale_status']=='ABOVE' and not interval(first['common_S0_Js']).overlaps(2350)
    assert all(r['scale_status']=='BELOW' and interval(r['common_S0_Js']).overlaps(2350) for r in (second,uneven))
    rejected={}
    for name in ('cubic','repeated_time','missing_residual_reference','incorrect_sign','coarse_null','bad_inertia','nonlinear_hold'):
        bad=deepcopy(doc);d=bad['devices'][0]
        if name=='cubic':
            for i,row in enumerate(d['blocks']['fit']):
                row['positions_q'][2]=(interval(row['positions_q'][2])+F(i**3,10**8)).data()
        if name=='repeated_time':d['blocks']['fit'][2]['block_time']='1'
        if name=='missing_residual_reference':d['blocks']['fit'][0]['error_reference']=''
        if name=='incorrect_sign':d['blocks']['fit'][2]['impulse_segments'][0]['total_Ns']='1'
        if name=='coarse_null':
            for row in d['blocks']['zero']:row['nonquadratic_error_q']='1/10'
        if name=='bad_inertia':d['kg']='10000'
        if name=='nonlinear_hold':
            for i,row in enumerate(d['blocks']['hold']):
                row['positions_q'][2]=(interval(row['positions_q'][2])+PATTERN[i]*F(1,10**7)).data()
        try:evaluate(bad)
        except ValueError as exc:rejected[name]=str(exc)
        else:raise AssertionError(name)
    # Even infinitely many reversals cannot distinguish a force proportional to the drive.
    alias=fixture(true_scale=2400,apparent=2400)
    for d in alias['devices']:
        k=F(d['kappa'])
        d['kg']=around(2*k*F(1,8)*2350,2*k*F(1,8)*2350*F(3,100)).data()
    proportional=evaluate(alias)
    assert proportional['scale_status']=='ABOVE'
    # Inflate the residual allowance by the independent upper bound |G_2400 - G_2350| |I|.
    # A large bound can lose a conclusive result; allow resolution or conservative rejection.
    from eichen import sample
    bounded=deepcopy(alias)
    for d in bounded['devices']:
        k=F(d['kappa']);dg=abs(1/(2*k*F(1,8)*2400)-1/(2*k*F(1,8)*2350))
        for rows in d['blocks'].values():
            for row in rows:
                _,imp,_=sample(row)
                row['nonquadratic_error_q']=str(dg*max(abs(imp.lo),abs(imp.hi)))
    try:protected=evaluate(bounded)['scale_status']
    except ValueError as exc:protected='REJECTED: '+str(exc)
    assert protected!='ABOVE'
    moments=[sum(s*i**j for i,s in enumerate(PATTERN)) for j in range(4)]
    assert moments==[0,0,0,-48]
    return {'true_S0_Js':'2350','apparent_S0_Js':'2400','old_four':first,'new_eight':second,
            'irregular_times':uneven,'polarity_time_moments':moments,'rejected':rejected,
            'unbounded_drive_proportional_confound':proportional['scale_status'],
            'with_independent_confound_bound':protected}
