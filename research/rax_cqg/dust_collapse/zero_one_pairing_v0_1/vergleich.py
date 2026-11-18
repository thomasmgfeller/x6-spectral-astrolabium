"""Gemeinsamer skalarer Ausgang für null oder ein inneres AA-Ereignis."""
import argparse
import cmath
import hashlib
import json
import math
import sys
from collections import Counter
from fractions import Fraction as F
from pathlib import Path

from paketgrenze import certified_bessel
from schranken import decimal_bounds, dust_mean, norm_ratio_over_d2, scale

ROOT=Path(__file__).resolve().parent
STUDIES = ROOT.parent
REPO = ROOT.parents[3]
sys.path.insert(0, str(STUDIES / "seam_pairing_v0_1"))
import pruefung as prior


def require(ok, message):
    if not ok:
        raise ValueError(message)


def inputs():
    manifest=json.loads((ROOT/'quellen.json').read_bytes())
    for item in manifest['files'].values():
        name = item['path']
        data = (REPO / name).read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==item['git_blob'],name)
    histories=json.loads((STUDIES/'amplitude_existence_v0_1/inputs/aa_hessians.json').read_bytes())['histories']
    return manifest['commit'],histories


def restriction(code):
    return sum(1<<(2*i+j-3) for i,j in prior.relation(code) if i in (0,1) and j in (3,4))


def empty_response(mask, weight):
    rel={(i,j+2) for i in (0,1) for j in (0,1) if mask & (1<<(2*i+j))}
    action=prior.sewing.local_action(range(4),rel)
    k=[[F(n,2) for n in row] for row in prior.sewing.doubled_hessian(action)]
    left,cross,right=[r[:2] for r in k[:2]],[r[2:] for r in k[:2]],[r[2:] for r in k[2:]]
    require(left[0][1]==left[1][0]==0, 'linker Rand ist eine Antikette')
    metric=prior.inv(prior.linear(prior.I2,prior.mm(left,left),1,prior.B2))
    xt=list(zip(*cross))
    q=prior.linear(prior.I2,prior.mm(xt,prior.mm(metric,cross)),0,prior.B2)
    p=prior.linear(right,prior.mm(xt,prior.mm(left,prior.mm(metric,cross))),1,-prior.B2)
    detroot=math.prod(cmath.sqrt(1-1j*prior.B*left[j][j]) for j in range(2))
    amp=weight/8*2*math.sqrt(math.pi)*cmath.exp(1j*action['F4'])/detroot
    return dict(code=mask,q=q,p=p,amp=amp,parents=0,sector=0)


def average(p,d):
    real,imag=dust_mean(p,d)
    return complex(float(sum(real)/2),float(sum(imag)/2))


def entries(rows, d):
    values={0:1,1:float(d)*average(1,d),2:float(d)*average(2,d)}
    counts=Counter()
    pairs=[]
    exceptions=[]
    for x in rows:
        for y in rows:
            label,det0,_=prior.pair(x,y)
            sectors=(x['sector'],y['sector'])
            counts[sectors,label]+=1
            if label!='absolute':
                exceptions.append(dict(sectors=list(sectors),codes=[x['code'],y['code']],type=label))
            a=(x['amp']*values[x['parents']]).conjugate()*y['amp']*values[y['parents']]*math.pi
            h=[[complex(float(x['q'][k][l]+y['q'][k][l])/2,
                        prior.B*float(x['p'][k][l]-y['p'][k][l])/2)
                for l in range(2)] for k in range(2)]
            pairs.append((sectors,label,det0,h,a))
    return counts,exceptions,pairs


def gram(pairs,t,eps):
    # det W=1; W has eigenvalues t,1/t on symmetric/antisymmetric field axes.
    w=(t+1/t)/2
    off=(t-1/t)/2
    terms={(i,j):[] for i in (0,1) for j in (0,1)}
    for key,_,det0,h,a in pairs:
        linear=w*prior.trace(h)-2*off*h[0][1]
        terms[key].append(a/cmath.sqrt(det0+eps*linear+eps**2))
    values={key:complex(math.fsum(z.real for z in stack),math.fsum(z.imag for z in stack))
            for key,stack in terms.items()}
    v0,v1=values[0,0],values[1,1]
    cross=values[0,1]
    require(abs(v0.imag)+abs(v1.imag)+abs(cross-values[1,0].conjugate())<1e-9,'Hermitizität')
    require(v0.real*v1.real>=abs(cross)**2,'Positivität bei endlichem Regulator')
    return dict(zero=prior.fmt(v0.real),one=prior.fmt(v1.real),
                cross=prior.complex_fmt(cross),ratio=prior.fmt(v1.real/v0.real))


def packet_modes(rows, d):
    # h_00, h_20, h_02 are orthonormal in dy. s,a=(y1 +/- y2)/sqrt(2).
    modes={i:[0j,0j,0j] for i in (0,1)}
    for r in rows:
        k=[[complex(int(i==j)+float(r['q'][i][j]),-prior.B*float(r['p'][i][j]))
            for j in range(2)] for i in range(2)]
        # Both Schur pivots have positive real part.
        root=cmath.sqrt(k[0][0])*cmath.sqrt(k[1][1]-k[1][0]*k[0][1]/k[0][0])
        c=prior.inv(k)
        z_s=prior.trace(c)+2*c[0][1]-1
        z_a=prior.trace(c)-2*c[0][1]-1
        time=1 if r['parents']==0 else float(d)*average(r['parents'],d)
        a=2*math.sqrt(math.pi)*r['amp']*time/root
        sector=r['sector']
        for j,factor in enumerate((1,z_s/math.sqrt(2),z_a/math.sqrt(2))):
            modes[sector][j]+=a*factor
    return modes


def calibrated(modes):
    results={}
    for labels,k in [('00',1),('00_20_02',3)]:
        zero,one=modes[0][:k],modes[1][:k]
        w0,w1=sum(abs(v)**2 for v in zero),sum(abs(v)**2 for v in one)
        cross=sum(x.conjugate()*y for x,y in zip(zero,one))
        require(w0<1,'Vergleichszweig normierbar')
        values={}
        for t in ('1','4'):
            ratio=float(sum(norm_ratio_over_d2(F(1,8),F(t),F(9,33)))/2)/64
            weight=w1+(1-w0)*ratio
            require(weight>abs(cross)**2,'positive normalisierte Form')
            values[t]=prior.fmt(weight)
        results[labels]=dict(test_zero_weight=prior.fmt(w0),test_one_weight=prior.fmt(w1),
                             fixed_mixed=prior.complex_fmt(cross),normalized_one_weight=values)
    return results


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--out',type=Path,required=True)
    opt=parser.parse_args()
    commit,hist=inputs()
    m=Counter(restriction(h['order_code']) for h in hist)
    require(sorted(m.items())==[(6,2),(7,5),(9,2),(11,5),(13,5),(14,5),(15,9)],'Nullfamilie')
    ref=json.loads((STUDIES/'scalar_boundary_conditions_v0_1/ergebnis.json').read_bytes())
    factors={r['order']:F(r['reduced_squared_norm_factor']) for r in ref['histories'] if r['rank']==1}
    require(factors=={9116:F(9,69185),17308:F(9,69185),25372:F(9,12871),25496:F(9,12871),
                      25500:F(9,1423450)},'publizierte transversale Normen')
    zero=[empty_response(mask,F(n,33)) for mask,n in sorted(m.items())]
    one=[dict(prior.response(h),sector=1) for h in hist]
    d=F(1,8)
    counts,exceptions,pairs=entries(zero+one,d)
    tally={}
    for i,j in ((0,0),(0,1),(1,0),(1,1)):
        tally[f'{i}{j}']=[counts[(i,j),k] for k in ('absolute','fresnel','length')]
    require(tally=={'00':[48,0,1],'01':[228,3,0],'10':[228,3,0],'11':[1078,4,7]},'Klassifikation')
    # The six mixed Fresnel terms all have a different quadratic phase on the axial null line.
    axial = {r['code']:r for r in [zero[-1],*one] if r['code'] in (15,25372,25496,25500)}
    slopes={k:(r['p'][0][0]+r['p'][1][1]-2*r['p'][0][1])/2 for k,r in axial.items()}
    require(slopes=={15:-1,25372:F(7,2),25496:F(7,2),25500:F(17,2)},'axiale Phasen')
    certified={}
    for width in (F(0),F(1,32),d,F(1)):
        certified[str(width)]={}
        for t in (F(1),F(4)):
            c=norm_ratio_over_d2(width,t,F(m[15],33))
            certified[str(width)][str(t)]=dict(ratio_over_d2=decimal_bounds(c),
                ratio=decimal_bounds(scale(width**2,c)) if width else ['0','0'])
    cert1,cert4=[norm_ratio_over_d2(d,t,F(9,33)) for t in (F(1),F(4))]
    require(cert4[1] < cert1[0],'Regulatorformen trennen')
    finite={}
    for t in (1.,4.):
        finite[str(int(t))]={}
        for e in (4.,1e-3,1e-7,1e-12,1e-18,1e-24):
            finite[str(int(t))][str(e)]=gram(pairs,t,e)
        target=float(sum(norm_ratio_over_d2(d,F(t),F(9,33)))/2)*float(d*d)
        require(abs(float(finite[str(int(t))]['1e-24']['ratio'])-target)<2e-8*target,'Grenzwert')
    mixed=sum(a/cmath.sqrt(det0) for key,_,det0,_,a in pairs if key==(0,1))
    modes=packet_modes(zero+one,d)
    multiplier=(F(m[15],33)/F(1,len(m)))**2
    require(multiplier==F(441,121),'alternatives Zählmass')
    from runpy import run_path
    interval=run_path(str(STUDIES/'m1_pilot_clock_v0_1/uhrtest.py'))['exp_minus_interval']
    e_lo,e_hi=interval(d)
    clock={}
    for beta in (F(5,4),F(4,3)):
        h0=(e_lo+(1-beta)*d,e_hi+(1-beta)*d)
        h1=(e_lo+beta-1,e_hi+beta-1)
        require(h0[0]>0,'offene Uhr')
        clock[str(beta)]=dict(no_birth=decimal_bounds(h0),
                         one_to_zero=decimal_bounds((d*h1[0]/h0[1],d*h1[1]/h0[0])))
    result=dict(open_clock_comparison_at_one_eighth=clock,bessel=certified_bessel(),packet_amplitudes={str(k):list(map(prior.complex_fmt,v)) for k,v in modes.items()},
                packet_order=['00','20','02'],anchored_products=calibrated(modes),commit=commit,scope='outgoing density atom; clock unmarked in AA window',
                left_restriction_multiplicities=dict(sorted(m.items())),pair_type_order=['absolute','fresnel','length'],
                ordered_counts=tally,nonabsolute=exceptions,primary_window=str(d),
                limit_zero_normalized_gram='diag(1,R); mixed element tends to zero',
                axial_phase_curvatures_over_b={str(k):str(v) for k,v in slopes.items()},
                certified=certified,uniform_zero_vs_pushforward_ratio_multiplier=str(multiplier),
                finite_regulator_grams=finite,unscaled_mixed_abel_value=prior.complex_fmt(mixed),
                short_time_ratio_over_d_limit='0 (untagged AA clock)',physical_relative_norm='HOLD',
                open_clock_candidate_rates=['5/4','4/3'],P3_M1_first_density_physical_comparisons=0)
    opt.out.write_text(json.dumps(result,sort_keys=True,indent=2,ensure_ascii=False)+'\n')


if __name__=='__main__':
    main()
