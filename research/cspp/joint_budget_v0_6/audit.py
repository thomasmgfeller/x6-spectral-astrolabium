"""Exact identities, independent bounded quadrature, fixed-physics and decision checks."""
from fractions import Fraction as Q
from collections import Counter
import json
from flint import arb,ctx
import model as m
import optimize as o


def check(ok,message):
    if not ok:raise RuntimeError('FAIL: '+message)


def controls():
    p=o.plan();out={};count=0
    for j in range(31):
        z=Q(j+1,2)
        polynomial=1-9*z+8*z*(z+1)-Q(4,3)*z*(z+1)*(z+2)
        check(polynomial==-Q(j*(j-1)*(j-2),6),'exact signed Gamma-moment polynomial')
        direct=sum(m.a(c)*(m.a(j+2*l+1)/2).gamma()/2 for l,c in enumerate([1,-9,8,Q(-4,3)]))
        check(direct.overlaps(m.gamma_moment(j)),'Gamma moment ball formula');count+=1
    out['exact_moment_identities']=count
    count=0
    for H in [2,Q(11,4),20]:
        x=m.a(H)**2/16;G=[(-x).exp(),x.expint(1)]
        for j in range(2,17):G.append((x**(1-j)*(-x).exp()-G[-1])/(j-1))
        for j,value in enumerate(G):
            check(value.overlaps(x.gamma_upper(1-j)),'incomplete Gamma independent implementation');count+=1
    out['gamma_recurrence_crosschecks']=count
    boundary=[]
    for ell,H in [(Q(1,8),2),(Q(37,256),Q(11,4)),(Q(1,4),4)]:
        series,meta=m.outside_boundary(ell,H);direct=m.boundary_direct(ell,H)
        check(series.rad()<arb('1e-12') and direct.rad()<arb('1e-12'),'meaningful boundary radius')
        check(series.overlaps(direct),'independent boundary rectangle')
        check(not (-series).overlaps(direct),'wrong boundary sign rejected')
        refined,_=m.outside_boundary(ell,H,order=16)
        check(refined.overlaps(series),'higher Taylor-order boundary check')
        boundary.append({'ell_k':str(ell),'H':str(H),'series':m.encode(series),'independent_rectangle':m.encode(direct)})
    out['independent_bounded_boundary_cases']=boundary
    # Independent ordinary Gauss quadrature in Cartesian time/radius, not the
    # null-coordinate integration used in production. Regression only.
    import numpy as np
    nodes,weights=np.polynomial.legendre.leggauss(96)
    ell,H,L=1.5,2.,2.;q=ell**-4;averages=[]
    for w,k in [(0.,0.),(.25,0.),(0.,.25),(.25,.25)]:
        total=0j
        for lo,hi in [(0.,H/2),(H/2,H)]:
            u=(lo+hi)/2+(hi-lo)*nodes/2;wu=(hi-lo)*weights/2
            rmax=np.minimum(u,H-u);r=rmax[:,None]*(nodes[None,:]+1)/2
            xi=q*np.pi/24*(u[:,None]**2-r*r)**2
            kernel=4*np.pi*r*r*np.exp(-xi-(u[:,None]**2+r*r)/(2*L*L))*(1-9*xi+8*xi**2-4*xi**3/3)
            total+=np.sum(wu[:,None]*rmax[:,None]*weights[None,:]/2*kernel*np.exp(1j*w*u[:,None])*np.sinc(k*r/np.pi))
        legacy=4*np.sqrt(q/6)*(-1+q*total)
        bounded=m.finite_mode_direct('3/2',2,w,k)
        check((bounded-m.balls.acb(complex(legacy))).abs_upper()<arb('1e-11'),'independent time-radius mode regression')
        averages.append({'omega':w,'k':k,'difference_upper':m.encode((bounded-m.balls.acb(complex(legacy))).abs_upper())})
    out['independent_mode_regressions_not_certificates']=averages
    old,detail=m.variance.local_lower_coefficient()
    new=m.lower_box(Q(1,8),20,Q(19,10),Q(21,10))
    check(new is not None and new[0].overlaps(old),'v0.4 lower coefficient recovered')
    check(m.lower_box(Q(1,8),2,Q(19,10),Q(21,10)) is None,'shell outside diamond rejected')
    # Geometric region: at t in [-1,1], r<=t+3/2. The null margins are
    # t-r+H >= H-3/2 and 4-t-r >= 5/2-2t, hence at least 1/2 for H>=2.
    check(all(m.a(H)>=2 for H in p['H']),'fixed source-wave support margin')
    contract=json.loads((m.HERE.parent/'e4_v0_1/contract.json').read_text())
    check(contract['source']['time_L0']==-1 and contract['source']['radius_L0']==.5 and contract['source']['k0_L0']==4,'fixed source')
    check(contract['detector']['time_L0']==1 and contract['detector']['center_L0']==[0,0,1.5] and contract['detector']['radius_L0']==.5,'fixed detector')
    check(contract['pilot']['scalar_test_k_L0']==[0,2,4,8],'unchanged physical wave numbers')
    check(p['witness']=={'L':2,'omega':0,'k':0,'point':[0,0,0,0],'exact_Box':'-1/2'},'fixed witness, no field rescaling')
    check(p['fixed_physics']['field_scale_rescaled_with_ell_or_H'] is False,'no physical rescaling')
    # Local-domain volume versus full-domain volume is not a change in density.
    N=m.a(4096)*m.volume(20)
    check(N>85786423 and N<85786424,'85.8-million D20 admissibility reproduced')
    check(m.volume(8).overlaps(512*arb.pi()/3),'full-length versus half-duration convention')
    check(m.volume(m.a('11/4')+4)>m.volume('11/4'),'full source/detector domain costs more')
    rejected=0
    for f in [lambda:m.outside_boundary(-1,2),lambda:m.finite_mode_direct(0,2),lambda:m.lower_box(0,2,1,2)]:
        try:f()
        except ValueError:rejected+=1
    check(rejected==3,'invalid physical scales rejected')
    out.update({'lower_bound_baseline_recovered':True,'out_of_domain_shell_rejected':True,
                'source_detector_and_wavelengths_unchanged':True,'D20_admissibility_reproduced':True,
                'scope_negative_controls':rejected})
    return out


def validate(record):
    p=o.plan();expected={(ell,H) for ell in p['ell_k'] for H in p['H']}
    check(len(record['rows'])==len(expected)==320,'complete joint scan')
    check({(r['ell_k'],r['H']) for r in record['rows']}==expected,'fixed scan identities')
    check(record['new_poisson_clouds']==0 and not record['confirmation_seed_used'],'no hidden sampling')
    check(record['decision']=='NO_NEW_SPRINKLING_AT_INHERITED_BUDGET','run decision')
    check(record['gate_status']=={'G1':'HOLD','G2':'NOT_RUN','G3':'NOT_RUN'},'scientific gates unchanged')
    counts=Counter()
    for row in record['rows']:
        status=row['family_budget_status'];counts[status]+=1
        b=row['budget_D'];q=m.balls.decode(row['q_rho_admissibility_min']).real
        check(q.overlaps(m.a(row['ell_k'])**-4),'admissibility independent of variance')
        if status=='ADMISSIBILITY_REJECT':
            check(m.balls.decode(row['expected_N_admissibility_D']).real>record['expected_point_budget'],'admissibility exclusion')
        elif status=='GAUSSIAN_TOTAL_RMS_REJECT':
            check(m.balls.decode(b['relative_total_RMS_lower_at_budget']).real>m.a('.1'),'Gaussian total-RMS exclusion')
        elif status=='FIXED_MODE_BIAS_REJECT':
            check(any(m.balls.decode(t['relative_bias_lower']).real>m.a('.1') for t in row['additional_fixed_mode_checks']),'unchanged mode rejects accidental cancellation')
        else:raise RuntimeError('FAIL: unresolved case cannot give NO_NEW_SPRINKLING')
        if row['allocation_status']=='WITHIN':
            check(row['positive_variance_lower_established'],'positive lower coefficient for retained candidate')
            check(m.balls.decode(row['relative_nonlocal_bias']).real<=m.a('.05'),'nonlocal allocation')
            check(m.balls.decode(row['relative_boundary']).real<=m.a('.01'),'boundary allocation')
            rho=int(row['rho_sufficient_for_all_allocations'])
            K=m.balls.decode(row['upper_variance_coefficient']).real
            check(K/rho<=m.a('7/200')**2,'sufficient stochastic inequality')
            check(m.a(rho)>=q/m.a(row['upper_epsilon_cap']),'upper-certificate smoothing regime')
            check(m.balls.decode(row['relative_total_RMS_upper_at_sufficient_density']).real<=m.a('.1'),'sufficient total RMS')
    check(sum(counts.values())==320,'all rows accounted')
    for label in ['D','Omega']:
        eligible=[r for r in record['rows'] if r['allocation_status']=='WITHIN']
        summary=record['summaries'][label]
        for skey,valuekey in [('smallest_necessary_budget_candidate','expected_N_necessary_plan'),('smallest_sufficient_bound_candidate','expected_N_sufficient_plan')]:
            selected=summary[skey];row=next(r for r in eligible if r['ell_k']==selected['ell_k'] and r['H']==selected['H'])
            chosen=m.balls.decode(row['budget_'+label][valuekey]).real
            for other in eligible:
                if (other['ell_k'],other['H'])!=(row['ell_k'],row['H']):
                    check(chosen<m.balls.decode(other['budget_'+label][valuekey]).real,'certified finite-grid ordering')
    return dict(counts)


def compare(low,high):
    validate(low);validate(high)
    for x,y in zip(low['rows'],high['rows']):
        check((x['ell_k'],x['H'])==(y['ell_k'],y['H']),'replay pair identity')
        for key in ['allocation_status','family_budget_status','finite_mean_method','positive_variance_lower_established']:
            check(x[key]==y[key],'replay discrete status '+key)
        for key in ['mean_finite','signed_boundary_delta','relative_finite_bias','variance_lower_coefficient']:
            check(m.balls.decode(x[key]).overlaps(m.balls.decode(y[key])),'replay enclosure '+key)
        # Endpoint-chosen sufficient densities/lower bounds may improve in the
        # last digits. Each precision must satisfy its own inequalities above.
    for label in ['D','Omega']:
        for key in ['smallest_necessary_budget_candidate','smallest_sufficient_bound_candidate']:
            check(low['summaries'][label][key]==high['summaries'][label][key],'stable finite-grid choice')
    check(low['decision']==high['decision'],'stable no-run decision')
    return {'joint_pairs':320,'precision_bits':[128,192],'status':'PASS','overlap_is_not_the_certificate_proof':True}
