"""Synthetic positive, negative and boundary controls; never physical instrument records."""
from copy import deepcopy
from fractions import Fraction as F
from eichen import KS,SIGNS,MU,H,H_LIMIT,evaluate,action_floor,force_weight
from intervall import interval,relative,around


def fixture(S0):
    devices=[]
    for k in KS:
        ell=F(1);dt=F(1);m=2*k*MU*S0*dt/(ell*ell)
        gain=ell/(2*k*MU*S0)
        d={'device_id':'synthetic-k='+str(k),'kappa':str(k),
           'impulse_reference':'synthetic injected SI impulse',
           'length_reference':'synthetic length standard','mass_time_reference':'synthetic free mass and time',
           'metres_per_q':relative(ell,F(1,2000)).data(),'kg':relative(m,F(1,2000)).data(),
           'seconds_per_step':relative(dt,F(1,10000)).data(),'blocks':{}}
        for role,width,factor in [('fit',F(1,10),1),('hold',F(2,5),3),('zero',0,0)]:
            rows=[]
            for i,sign in enumerate(SIGNS):
                kick=sign*factor*F(3,40000)*k
                # Independent analytic integration of a rectangle centred on the middle point.
                response=gain*kick*(1-F(width)/4)
                bg=F(1,10**8)+F(1,10**9)*i
                # Deliberately vary unobserved initial position and velocity between the runs.
                q0=F(2-i,7);vq=F(i*i-3,13)
                q1=q0+vq
                q2=q1+vq+bg+response
                rows.append({'block_time':str(3*i+1),'dust_source':'0',
                    'positions_q':[around(q,F(1,10**12)).data() for q in (q0,q1,q2)],
                    'impulse_segments':[{'start':str(-F(width)/2),'end':str(F(width)/2),
                                         'total_Ns':relative(kick,F(1,1000)).data()}]})
            d['blocks'][role]=rows
        devices.append(d)
    return {'kind':'synthetic','devices':devices}


def run(prev,early):
    from proben import samples
    from gemischt import ORDER
    fixtures,_=samples(prev,early)
    for _,_,w in fixtures:
        assert all(w[i].data()==['1/8','1/8'] for i in (0,1,2))
    assert all(ij in ORDER for ij in ((0,1),(1,2),(2,16),(2,18)))
    floor=action_floor()
    assert floor.inside(['2372.78658','2372.78660'])
    stationary_checks=0
    # Independent exact central differences of the calibrated two-edge action.
    for k in KS:
        for kick in (-F(3,7),F(0),F(1,4)):
            for S0 in (2000,3000):
                ell=F(3,13);q0=F(-3,8);q1=F(9,5)
                q2=2*q1-q0+ell*kick/(2*k*MU*S0)
                action=lambda u:S0*k*MU*((u-q0)**2+(q2-u)**2)+ell*kick*u
                assert action(q1+F(1,37))==action(q1-F(1,37))
                stationary_checks+=1
    assert [sum(s*i**p for i,s in enumerate(SIGNS)) for p in (0,1,2)]==[0,0,4]
    inputs=[('above',3000,'ABOVE'),('below',2000,'BELOW'),('boundary',F('2372.8'),'UNRESOLVED')]
    results={}
    for name,value,outcome in inputs:
        report=evaluate(fixture(F(value)))
        assert report['scale_status']==outcome and interval(report['common_S0_Js']).overlaps(value)
        results[name]=report
    base=fixture(F(3000))
    challenges={}
    def reject(name,data):
        try:evaluate(data)
        except (ValueError,KeyError,ZeroDivisionError) as exc:
            challenges[name]=str(exc)
        else:raise AssertionError(name+' passed unexpectedly')
    x=deepcopy(base)
    positions=x['devices'][0]['blocks']['hold']
    for row,sgn in zip(positions,SIGNS):
        row['positions_q'][2]=(interval(row['positions_q'][2])+sgn*F(1,10**7)).data()
    reject('nonlinear_holdout',x)
    x=deepcopy(base)
    for device in x['devices']:
        for block in device['blocks'].values():
            for row in block:
                for seg in row['impulse_segments']:seg['start']=seg['end']='0'
    reject('pulse_duration_ignored',x)
    x=deepcopy(base); x['devices'][1]=fixture(F(4000))['devices'][1]
    reject('inconsistent_device_scales',x)
    x=deepcopy(base)
    for row in x['devices'][0]['blocks']['fit']:
        for seg in row['impulse_segments']:seg['total_Ns']=(-interval(seg['total_Ns'])).data()
    reject('wrong_kick_polarity',x)
    x=deepcopy(base)
    x['devices'][0]['blocks']['fit'][0]['positions_q'][0]=around(0,1).data()
    reject('coarse_detection',x)
    x=deepcopy(base);x['devices'][0]['length_reference']=''
    reject('unknown_length_reference',x)
    x=deepcopy(base);x['devices'][0]['blocks']['fit'][2]['block_time']='7.5'
    reject('unequal_block_times',x)
    x=deepcopy(base);x['devices'][0]['kg']=relative(800,F(1,2000)).data()
    reject('inertial_cross_check',x)
    x=deepcopy(base);x['devices'][0]['blocks']['zero'][0]['positions_q'][1]=around(1,0).data()
    reject('bad_zero_control',x)
    assert all(force_weight(a,b)==z for a,b,z in [(0,0,1),(-1,1,F(1,2)),(-2,2,F(1,4)),
               (F(1,4),F(3,4),F(1,2)),(F(1,3),F(1,3),F(2,3)),(1,2,0)])
    # Independent expressions for an ideal co-wavelength interferometer and recoil.
    optical=[]
    for k in KS:
        for N in (1000001,10**18+7):
            gamma=F(3,2)*10**6;wavelength=F(1064,10**9)
            ell=gamma*wavelength/2
            imp=2*N*H/wavelength
            qcontrast=ell*imp/(2*k*MU*3000)
            fringes=gamma*qcontrast
            photon_ratio=gamma**2*N/(2*k*MU*fringes)
            assert H*photon_ratio==3000
            optical.append({'k':str(k),'effective_photon_contrast':str(N),'S0_Js':'3000'})
    return {'threshold_common_Js':floor.data(),'threshold_strong_only_Js':action_floor(H_LIMIT*10**11).data(),
            'synthetic_fits':results,'rejected_controls':challenges,'independent_fringe_formula':optical,'two_edge_variational_checks':stationary_checks,
            'ABBA_response_to_unit_quadratic_drift':'4',
            'rectangle_duration_two_fifths_response_factor':'9/10','collar_weights_confirmed_backgrounds':len(fixtures)}
