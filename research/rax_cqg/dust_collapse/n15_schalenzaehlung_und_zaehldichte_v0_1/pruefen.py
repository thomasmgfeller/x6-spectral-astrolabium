"""Replay archived shell readings and independent checks of the statistical design."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
from itertools import product
from math import pi,sqrt
from pathlib import Path
import json
import sys
import numpy as np
from scipy.special import gammaincinv,gammainccinv
from scipy.integrate import quad
from scipy.stats import poisson
from auslese import END,TAIL,TICKS,LAMBDA0,readout,radius
from design import (select,layout,four_volume,NS,MS,CASES,FACTORS,
                    deformation,volume,sphere,average_d)
from punktprobe import generate
from geometrie import regularity,shape

ROOT=Path(__file__).resolve().parent


def array_digest(arr):
    return sha256(np.asarray(arr,dtype='<i4',order='C').tobytes()).hexdigest()


def upper_at_nominal(n,m,f):
    """Even an ideal inner count cannot exceed its own threshold more often."""
    lam=f*LAMBDA0
    _,_,r2,norm,_=layout(n,m)
    lowtarget=lam*norm*r2*.95**2*1.01
    h=Q(1,m);width=Q(1,n)
    kmin=poisson.isf(TAIL,lowtarget).astype(int)+1
    kmax=poisson.ppf(TAIL,lam*norm*r2*1.05**2*.99).astype(int)-1
    counts=[(four_volume(z,c,z,z+h,1-width,Q(1)),
             four_volume(z,c,z-h,z,Q(1),1+width)) for z,c in CASES]
    a,b=lam*np.array(counts).T
    # Same-trial independence of disjoint material sides only.
    return float(np.min(poisson.sf(kmin-1,a)*poisson.cdf(kmax,b)))


def check_layout(winner):
    f,n,m=map(winner.get,('factor','n','m'))
    lam=f*LAMBDA0
    inner,outer,r2,norm,operator=layout(n,m)
    details=[]
    cutoff_i=lam*norm*r2*.95**2*1.01;cutoff_o=lam*norm*r2*1.05**2*.99
    h,eps,rad=Q(1,m),Q(1,TICKS),Q(373,1000*TICKS)
    for j,(z,c) in enumerate(CASES):
        # Check threshold integers with Gamma quantiles evaluated directly.
        k=int(poisson.isf(TAIL,cutoff_i[j]))+1
        l=int(poisson.ppf(TAIL,cutoff_o[j]))-1
        assert gammaincinv(k-1,TAIL)<cutoff_i[j]<=gammaincinv(k,TAIL)
        assert gammainccinv(l+1,TAIL)<=cutoff_o[j]<gammainccinv(l+2,TAIL)
        for a,b,left,right,vol in [(z+eps,z+h-eps,1-Q(1,n)+rad,Q(1),inner[j]),
                                  (z-h-eps,z+eps,Q(1),1+Q(1,n)+rad,outer[j])]:
            def temporal(x):
                # Independent polynomial evaluation in T, direct radial area integration in u.
                t=float(z)
                def smooth(s):
                    s=max(0,min(1,s))
                    return 6*s**5-15*s**4+10*s**3
                d=.0398*smooth(x)+.2576*smooth(64*(x-t)+(c=='A'))
                def density(u):
                    shape=(-65*u**2+154*u**4-81*u**6)/8
                    return u*u*(1-d*shape)
                return quad(density,float(left),float(right),epsabs=1.e-14)[0]
            knots=[float(v) for v in [z-Q(1,64),z,z+Q(1,64)] if a<v<b]
            other=4*pi*1000*END*quad(temporal,float(a),float(b),points=knots,epsabs=1e-13)[0]
            assert abs(other/vol-1)<3e-12
        v_in=four_volume(z,c,z,z+h,1-Q(1,n),Q(1))
        v_out=four_volume(z,c,z-h,z,Q(1),1+Q(1,n))
        details.append({'x':str(z),'case':c,'radius':sqrt(r2[j]),
                        'expected_nominal':[lam*v_in,lam*v_out],'n_inner_min':k,'n_outer_max':l,
                        'worst_tail_inner':float(poisson.cdf(k-1,.99*lam*inner[j])),
                        'worst_tail_outer':float(poisson.sf(l,1.01*lam*outer[j]))})
    direct=1-12*TAIL-sum(r['worst_tail_inner']+r['worst_tail_outer'] for r in details)
    assert abs(direct-winner['joint_lower'])<2e-13
    return details


def sampling_edge_width(design,case_data):
    # Additional diagnostic: contribution of the one-sided confidence limit relative
    # to the plug-in endpoint, on the explicit integer count range [1000,100000].
    k=np.arange(1000,100001)
    low=float(np.max(np.sqrt(k)-np.sqrt(gammaincinv(k,TAIL))))
    high=float(np.max(np.sqrt(gammainccinv(k+1,TAIL))-np.sqrt(k)))
    vi,vo,r2,norm,_=layout(design['n'],design['m'])
    lam=LAMBDA0*design['factor']
    edge=max(low/sqrt(1.01),high/sqrt(.99))/sqrt(lam*norm*min(r2))
    # All raw inner counts lie between eroded and nominal, outer between nominal and enlarged.
    lam_min=min(.99*lam*min(vi),.99*min(r['expected_nominal'][1] for r in case_data))
    lam_max=max(1.01*lam*max(vo),1.01*max(r['expected_nominal'][0] for r in case_data))
    # Chernoff log tails, no numerical underflow interpreted as a zero probability.
    from math import log,ceil
    def rate(k,mu):
        return k*log(k/mu)-k+mu
    assert 999<lam_min<=lam_max<100001
    logbound=log(24)-min(rate(999,lam_min),rate(100001,lam_max))
    return {'count_range':[1000,100000],'outside_probability_log10_upper_ceiling':ceil(logbound/log(10)),
            'max_statistical_endpoint_extension_over_true_radius':edge}


def audit_n15(winners):
    data=json.loads((ROOT/'basis/n15_ergebnisse.json').read_text())
    clocks=data['geometry']['normalized_clock_intervals']
    assert len(clocks)==15 and data['geometry']['type']==1767356
    for design in winners.values():
        h=Q(1,design['m'])+Q(2,TICKS)
        for z,_ in CASES:
            assert all(Q(hi)<z-h or Q(lo)>z+h for lo,hi in clocks.values())
    plan=json.loads((ROOT/'basis/plan.json').read_text())
    assert plan['physical_refinement']['actual_lambda0'] is None
    assert plan['family']['total']==524 and plan['error_budget_fractions']['operator']==.15
    records=json.loads((ROOT/'basis/checkpoints.json').read_text())
    assert len(records)==60 and all(r['execution']=='NOT_RUN' and r['checkpoint_id']=='P3' for r in records)
    assert json.loads((ROOT/'basis/zulassung.json').read_text())['decision']=='HOLD_NOT_ELIGIBLE'
    assert readout(None,.5,1,.01,10.,False)['status']=='MISSING_EXPOSURE'
    zero=readout(np.empty((0,3),dtype=int),.5,1,.01,10.,True)
    assert zero['lower']==0 and zero['upper']>0
    assert abs(zero['upper']**2*4*pi*(END*.01)*.99*10+np.log(TAIL))<1e-12
    for bad in (np.array([[2,1,-1]]),np.array([[1,2,0]]),np.array([[1.5,2.,1.]])):
        try: readout(bad,.5,1,.01,10.,True)
        except ValueError: pass
        else: raise AssertionError('Ungültiges Echo akzeptiert.')
    assert radius(1000000,0,1,1,1)['status']=='INCONSISTENT'
    # Negative control for the direction of the time bins: at coarse exposure the
    # wrong inner-before mean area exceeds the true middle sphere, or outer-after is too small.
    z=Q(1,2);h=Q(1,32);w=Q(1,64)
    wrong=[]
    for c in ('A','B'):
        ri2=float(100*sphere(deformation(c,z,z),Q(1)))
        unit=4*pi*(10/64)*END*float(h)*ri2
        wrong.append([sqrt(four_volume(z,c,z-h,z,1-w,Q(1))/unit),
                      sqrt(four_volume(z,c,z,z+h,Q(1),1+w)/unit)])
    assert wrong[0][0]>1.05 and wrong[1][1]<.95
    return {'N15_events':len(clocks),'in_each_target_window':0,'N15_readout':'MISSING_EXPOSURE',
            'physical_density':None,'P3_NOT_RUN':60,'wrong_time_order_radius_ratios':wrong}


def main(create):
    if not __debug__: sys.exit('Für die Nachrechnung Python ohne -O starten.')
    if not create:
        for line in (ROOT/'SHA256SUMS').read_text().splitlines():
            digest,path=line.split('  ',1)
            assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    source=json.loads((ROOT/'Herkunft.json').read_text())
    for path,digest in source['inputs'].items():
        assert sha256((ROOT/path).read_bytes()).hexdigest()==digest,path
    assert sha256((ROOT/'Pruefplan.md').read_bytes()).hexdigest()==source['plan_sha256']
    assert regularity()['d_max']=='1487/5000'
    # On the smallest enclosing radial guard strip f >= 1 - upper bound > 0.
    u=Q(107,100)
    assert 1-(u*u-1)**2*(81*u*u+8)/8>0
    assert 1-Q(1,16)-Q(373,1000*TICKS)>Q(93,100) and 1+Q(1,16)+Q(373,1000*TICKS)<u
    winners,scan=select()
    assert set(winners)=={'total','operator_cap'}
    checked={name:check_layout(row) for name,row in winners.items()}
    ideal_upper={}
    for f in (1,2,4,8):
        best=max((upper_at_nominal(n,m,f),n,m) for n,m in product(NS,MS))
        ideal_upper[f]={'joint_upper_at_nominal':best[0],'n':best[1],'m':best[2]}
    chosen=winners['total']
    density=LAMBDA0*chosen['factor'];n,m=chosen['n'],chosen['m']
    pulses,diag=generate(n,m,density)
    if create:
        np.savez_compressed(ROOT/'Radarzeitpaare.npz',**pulses)
    instrument={'width':10/n,'normalized_window':1/m,'nominal_density':density,
                'quantization_ticks':TICKS,'density_relative_error':.01,
                'complete_reference_exposures':True,'time_unit':END,
                'acquisitions':{r['id']:r['target'] for r in diag}}
    with np.load(ROOT/'Radarzeitpaare.npz',allow_pickle=False) as saved:
        assert set(saved.files)==set(pulses)
        for rec,row in zip(diag,checked['total']):
            key=rec['id'];arr=saved[key]
            assert np.array_equal(arr,pulses[key])
            rec['sha256_int32_le']=array_digest(arr)
            res=readout(arr,float(Q(rec['target'])),10/n,1/m,density,True)
            a,b=rec['ideal_membership_counts']
            assert res['inner_sure']<=a and res['outer_possible']>=b
            rec['blind_result']=res
            rec['covered_in_band']=bool(.95*row['radius']<=res['lower']<=row['radius']<=res['upper']<=1.05*row['radius'])
            rec['radius_reference']=row['radius']
    data={'winners':winners,'screens':scan,'forecast_details':checked,'ideal_upper':ideal_upper,
          'sampling_edge_width':{k:sampling_edge_width(v,checked[k]) for k,v in winners.items()},
          'fixed_synthetic_sample':diag,'n15':audit_n15(winners),'grid_designs':len(NS)*len(MS)}
    for name,value in [('Instrument.json',instrument),('ergebnisse.json',data)]:
        encoded=json.dumps(value,indent=2,ensure_ascii=False,allow_nan=False)+'\n'
        path=ROOT/name
        if create:path.write_text(encoded)
        else:
            # Scientific special functions may differ by ulps across platforms.
            def match(a,b):
                if isinstance(a,dict):return a.keys()==b.keys() and all(match(a[k],b[k]) for k in a)
                if isinstance(a,list):return len(a)==len(b) and all(match(x,y) for x,y in zip(a,b))
                if isinstance(a,float):return np.isclose(a,b,rtol=1e-11,atol=1e-13)
                return a==b
            assert match(json.loads(encoded),json.loads(path.read_text())),name
    print('Prüflauf abgeschlossen. 30 Geometrie-/Zeitfenster, 390 Dichtevarianten, '
          f'{sum(r["covered_in_band"] for r in diag)}/6 synthetische Radiusintervalle innerhalb des Zielbands, 60 physische Einträge NOT_RUN.')


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--erzeugen',action='store_true')
    main(parser.parse_args().erzeugen)
