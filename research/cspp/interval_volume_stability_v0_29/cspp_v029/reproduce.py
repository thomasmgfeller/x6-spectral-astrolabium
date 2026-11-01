#!/usr/bin/env python3
"""Certified Poisson interval-volume path budgets. Standard library only.

All enclosures use integers/Fractions with outward rounding. No random clouds.
The infinite statements and the domain restriction are proved in PROOF.md.
"""
from fractions import Fraction as F
from math import comb, factorial, isqrt
from pathlib import Path
import hashlib
import importlib.util
import itertools
import json
import sys

ROOT = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def verify_sources():
    meta = json.loads((ROOT / 'evidence/SOURCES.json').read_text())
    for item in meta['sources']:
        b = (ROOT / 'evidence' / item['file']).read_bytes()
        require(hashlib.sha256(b).hexdigest() == item['sha256'], 'source SHA256')
        require(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
                == item['git_blob'], 'source Git blob')
    return len(meta['sources'])

verify_sources()
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('frozen_v027', ROOT/'evidence/reproduce_v027.py')
base = importlib.util.module_from_spec(spec)
spec.loader.exec_module(base)
COEFFS = {0: list(map(F, [1,-9,16,-8])),
          21: [F(197,8),F(-3033,8),F(2363,2),F(-1331),F(504)]}
DIAGONAL = {0:F(-1),21:F(-71,8)}
CAP = {0:F(4976184375,4294967296),21:F(161390925,4194304)}
T, H = F(9,4), F(4)
POISSON_CUTOFF = 512

def ceildiv(a,b):
    require(b > 0, 'nonpositive divisor')
    return -((-a)//b)

class Fixed:
    """Closed nonnegative intervals [l,u]/10**digits; integer-directed operations."""
    def __init__(self,digits):
        self.digits=digits; self.s=10**digits; self.one=(self.s,self.s)
    def exact(self,x):
        x=F(x); return (x.numerator*self.s//x.denominator,
                        ceildiv(x.numerator*self.s,x.denominator))
    def add(self,x,y): return (x[0]+y[0],x[1]+y[1])
    def mul(self,x,y):
        require(x[0]>=0 and y[0]>=0,'negative interval multiplication')
        return (x[0]*y[0]//self.s,ceildiv(x[1]*y[1],self.s))
    def div(self,x,y):
        require(x[0]>=0 and y[0]>0,'unsafe interval division')
        return (x[0]*self.s//y[1],ceildiv(x[1]*self.s,y[0]))
    def scale(self,x,q):
        q=F(q); require(q>=0,'negative scale')
        return (x[0]*q.numerator//q.denominator,
                ceildiv(x[1]*q.numerator,q.denominator))
    def sqrt(self,x):
        require(x[0]>=0,'negative square root')
        lo=isqrt(x[0]*self.s); hi=isqrt(x[1]*self.s)
        if hi*hi < x[1]*self.s: hi+=1
        return lo,hi
    def fractions(self,x): return F(x[0],self.s),F(x[1],self.s)
    def expneg(self,x):
        """Positive Taylor enclosure of exp(x/2**m), reciprocal, then squaring."""
        x=F(x); require(x>=0,'negative exponent argument')
        m=0
        while x>1: x/=2; m+=1
        r=self.exact(x); term=self.one; total=self.one
        for k in range(1,self.digits+1):
            term=self.scale(self.mul(term,r),F(1,k)); total=self.add(total,term)
        nxt=self.scale(self.mul(term,r),F(1,self.digits+1))
        tail=self.div(nxt,self.exact(1-x/F(self.digits+2)))
        positive=(total[0],total[1]+tail[1])
        out=self.div(self.one,positive)
        for _ in range(m): out=self.mul(out,out)
        return max(0,out[0]),min(self.s,out[1])

def weight(c,e,n):
    return sum((ck*comb(n,k)*e**k*(1-e)**(n-k)
                for k,ck in enumerate(c) if k<=n),F(0))

def poisson_mean(ctx,mu,weights,cap):
    """E b_Pois(mu), with bounded infinite tail. Not |E w|."""
    mu=F(mu); require(0<=mu<POISSON_CUTOFF+2,'Poisson tail ratio invalid')
    if mu==0: return weights[0]
    x=ctx.exact(mu); term=ctx.one; total=weights[0]
    for n in range(1,len(weights)):
        term=ctx.scale(ctx.mul(term,x),F(1,n))
        total=ctx.add(total,ctx.mul(term,weights[n]))
    nxt=ctx.scale(ctx.mul(term,x),F(1,len(weights)))
    tail=ctx.div(nxt,ctx.exact(1-mu/F(len(weights)+1)))
    total=(total[0],total[1]+ctx.mul(cap,tail)[1])
    out=ctx.mul(ctx.expneg(mu),total)
    return max(0,out[0]),min(cap[1],out[1])

def interval_json(lo,hi,places=12):
    require(lo<=hi,'reversed output interval'); scale=10**places
    l=F(lo.numerator*scale//lo.denominator,scale)
    u=F(ceildiv(hi.numerator*scale,hi.denominator),scale)
    return dict(lower_fraction=str(l),upper_fraction=str(u),
                lower_decimal=base.decimal_out(l,places),
                upper_decimal=base.decimal_out(u,places,True))

def pair_json(ctx,pair): return interval_json(*ctx.fractions(pair))

def weight_table(ctx,theta):
    values=[abs(weight(COEFFS[theta],F(1,16),n)) for n in range(POISSON_CUTOFF+1)]
    require(max(values)==CAP[theta],'inherited sharp cap mismatch')
    return [ctx.exact(v) for v in values]

def poisson_cells(ctx,theta,den,weights):
    cap=ctx.exact(CAP[theta]); radius=ctx.exact(CAP[theta]/(2*den))[1]
    max_mu=(T+H)**4/8; count=ceildiv(max_mu.numerator*den,max_mu.denominator)
    cells=[]
    for j in range(count):
        midpoint=F(2*j+1,2*den)
        lo,hi=poisson_mean(ctx,midpoint,weights,cap)
        require(lo<=hi,'Poisson enclosure invalid')
        cells.append((max(0,lo-radius),min(cap[1],hi+radius)))
    return cells

def kernel_table(ctx,theta,time_den,mu_den,cells):
    """Exact radial shell integration of the piecewise constant A bounds."""
    al,au=base.a_bounds(60)
    # 4*pi*beta/3 = a / (4*(1-a*d_local)) at the frozen q0.
    pref=tuple(ctx.exact(a/(4*(1-a*DIAGONAL[theta])))[i]
               for i,a in enumerate((al,au)))
    roots=[ctx.sqrt(ctx.exact(F(8*j,mu_den))) for j in range(len(cells)+1)]
    output=[(0,0)]; count=int((T+H)*time_den)
    for n in range(1,count+1):
        s=F(n,time_den); s2=ctx.exact(s*s); max_mu=s**4/8
        bins=ceildiv(max_mu.numerator*mu_den,max_mu.denominator)
        previous=ctx.exact(s**3); total=(0,0)
        for j in range(bins):
            root=roots[j+1]
            z=(max(0,s2[0]-root[1]),max(0,s2[1]-root[0]))
            current=ctx.mul(z,ctx.sqrt(z))
            shell=(max(0,previous[0]-current[1]),max(0,previous[1]-current[0]))
            total=ctx.add(total,ctx.mul(shell,cells[j]));previous=current
        require(previous==(0,0),'radial shells did not reach the cone centre')
        output.append(ctx.mul(pref,total))
    # Physical h is monotone, but loose bounds need not be. Intersect envelopes.
    for i in range(1,len(output)):
        output[i]=(max(output[i][0],output[i-1][0]),output[i][1])
    for i in range(len(output)-2,-1,-1):
        output[i]=(output[i][0],min(output[i][1],output[i+1][1]))
    require(all(0<=lo<=hi for lo,hi in output),'kernel intervals inconsistent')
    return output

def volterra(ctx,kernel,time_den):
    """Monotone left/right rectangles; implicit upper first cell is solved."""
    nmax=int(T*time_den); history=int(H*time_den); scale=ctx.s
    low_prefix=[0];high_prefix=[0]
    for lo,hi in kernel:
        low_prefix.append(low_prefix[-1]+lo);high_prefix.append(high_prefix[-1]+hi)
    g=[]
    for n in range(nmax+1):
        gl=(low_prefix[n+history]-low_prefix[n])//time_den
        gu=ceildiv(high_prefix[n+history+1]-high_prefix[n+1],time_den)
        g.append((gl,gu))
    active=[ctx.one];hist=[g[0]]
    denom=time_den*scale-kernel[1][1]
    require(denom>0,'upper Volterra first-cell contraction fails')
    for n in range(1,nmax+1):
        for values,forcing in ((active,ctx.one),(hist,g[n])):
            lo_sum=sum(kernel[j-1][0]*values[n-j][0] for j in range(1,n+1))
            # j=1 multiplies the unknown current value and is moved to the left.
            hi_sum=sum(kernel[j][1]*values[n-j+1][1] for j in range(2,n+1))
            lo=forcing[0]+lo_sum//(time_den*scale)
            hi=ceildiv(forcing[1]*time_den*scale+hi_sum,denom)
            require(0<=lo<=hi,'Volterra enclosure invalid')
            values.append((lo,hi))
    f=active[-1];h=hist[-1]
    ba=(scale+100*(f[0]-scale),scale+100*(f[1]-scale))
    bj=(ba[0]+100*h[0],ba[1]+100*h[1])
    return {'F':f,'history_H':h,'B_active':ba,'B_joint':bj,
            'eta_active':ctx.div(ctx.exact(F(1,1000)),ba),
            'eta_joint':ctx.div(ctx.exact(F(1,1000)),bj)},g[0]

def chain_audit():
    counts={}; chains=0; multi=0
    for n in range(1,6):
        orders=list(base.orders(n));counts[str(n)]=len(orders)
        for relation in orders:
            for size in range(2,n+1):
                for vertices in itertools.combinations(range(n),size):
                    if not all(relation[b][a] for a,b in zip(vertices,vertices[1:])):continue
                    interiors=[{z for z in range(n) if relation[b][z] and relation[z][a]}
                               for a,b in zip(vertices,vertices[1:])]
                    require(all(not (s&set(vertices)) for s in interiors),'inserted chain vertex inside adjacent edge')
                    require(sum(map(len,interiors))==len(set().union(*interiors)),
                            'adjacent chain interiors overlap')
                    chains+=1;multi+=size>=3
    require(sum(counts.values())==407,'order count changed')
    return dict(orders_by_size=counts,chains=chains,multi_edge_chains=multi)

def thinning_audit():
    count=0
    for theta,p,n in itertools.product(COEFFS,[F(1),F(1,2),F(2,3),F(3,7)],range(25)):
        c=COEFFS[theta];e=F(1,16)
        probabilities=[F(comb(n,m))*p**m*(1-p)**(n-m) for m in range(n+1)]
        signed=sum((b*weight(c,e,m) for m,b in enumerate(probabilities)),F(0))
        absolute=sum((b*abs(weight(c,e,m)) for m,b in enumerate(probabilities)),F(0))
        require(signed==weight(c,p*e,n) and abs(signed)<=absolute<=CAP[theta],
                'binomial conditional Jensen check')
        count+=1
    return count

def expneg_rational(x):
    """Independent exact-Fraction enclosure, with no fixed-point operations."""
    x=F(x);m=0
    while x>1:x/=2;m+=1
    term=F(1);total=term
    for k in range(1,101):term*=x/k;total+=term
    tail=term*x/101/(1-x/102)
    lo,hi=1/(total+tail),1/total
    for _ in range(m):lo*=lo;hi*=hi
    return lo,hi

def rational_spots():
    ctx=Fixed(120);rows=[]
    for theta in COEFFS:
        exact=[abs(weight(COEFFS[theta],F(1,16),n)) for n in range(POISSON_CUTOFF+1)]
        fixed=[ctx.exact(b) for b in exact]
        for mu in [F(0),F(1,2),F(3),F(16),F(64)]:
            observed=ctx.fractions(poisson_mean(ctx,mu,fixed,ctx.exact(CAP[theta])))
            term=F(1);total=exact[0]
            for n in range(1,len(exact)):term*=mu/n;total+=exact[n]*term
            tail=term*mu/len(exact)/(1-mu/(len(exact)+1))*CAP[theta]
            el,eu=expneg_rational(mu);reference=(el*total,eu*(total+tail))
            require(max(observed[0],reference[0])<=min(observed[1],reference[1]),
                    'independent rational Poisson evaluation disagrees')
            rows.append(dict(theta=theta,mu=str(mu),enclosure=interval_json(*observed)))
    return rows

def constant_kernel_audit():
    # Check the full Volterra machinery against the v0.28 closed positive series.
    archived=json.loads((ROOT/'evidence/RESULTS_v028.json').read_text())
    ctx=Fixed(120);den=64;rows=[]
    al,au=base.a_bounds(60)
    for theta in COEFFS:
        pref=tuple(ctx.exact(a*CAP[theta]/(4*(1-a*DIAGONAL[theta])))[i]
                   for i,a in enumerate((al,au)))
        kernel=[ctx.scale(pref,F(n,den)**3) for n in range(int((T+H)*den)+1)]
        result,_=volterra(ctx,kernel,den)
        old=next(r for r in archived['budgets'] if r['theta']==theta and r['kind']=='smoothed_1/16')
        for key in ['F','history_H','B_active','B_joint']:
            lo,hi=ctx.fractions(result[key]);ref=old[key]
            require(lo<=F(ref['lower_fraction'])<=F(ref['upper_fraction'])<=hi,
                    'constant-kernel Volterra fails archived analytic enclosure')
        # Separate spatial regression: all radial cells contain the same cap.
        mu_den=16;max_mu=(T+H)**4/8
        cell_count=ceildiv(max_mu.numerator*mu_den,max_mu.denominator)
        shells=kernel_table(ctx,theta,16,mu_den,[ctx.exact(CAP[theta])]*cell_count)
        for n,shell in enumerate(shells):
            exact=ctx.scale(pref,F(n,16)**3)
            require(max(shell[0],exact[0])<=min(shell[1],exact[1]),
                    'radial shell integration differs from analytic cone volume')
        rows.append(dict(theta=theta,constant_kernel_encloses_v028=True,
                         radial_shell_cone_checks=len(shells)))
    return rows

def negative_controls():
    caught=[]
    def reject(name,fn):
        try:fn()
        except ValueError:caught.append(name)
        else:raise ValueError('negative control escaped: '+name)
    # Shared Poisson count pgf: E z1^N z2^N=e^(lambda*(z1*z2-1)).
    # The exponent of the falsely independent product differs by lambda*(1-z1)*(1-z2).
    lam,z1,z2=F(2),F(1,2),F(3,4)
    reject('overlapping_intervals_are_not_independent',
           lambda:require(lam*(z1*z2-1)==lam*(z1-1)+lam*(z2-1),'overlap covariance'))
    c=COEFFS[21];w0=weight(c,F(1,16),0);w1=weight(c,F(1,16),1)
    require(w0>0>w1,'opposite-sign witness missing')
    ctx=Fixed(120);weights=weight_table(ctx,21);cap=ctx.exact(CAP[21])
    mean_absolute=poisson_mean(ctx,F(1),weights,cap)
    z=F(1,16);polynomial=sum((ck*z**k/factorial(k) for k,ck in enumerate(c)),F(0))
    absolute_mean=ctx.scale(ctx.expneg(z),abs(polynomial))
    reject('absolute_mean_is_not_mean_absolute',
           lambda:require(mean_absolute[0]<=absolute_mean[1],'actual Poisson strict Jensen witness'))
    full_volume=poisson_mean(ctx,F(160),weights,cap)
    reject('full_volume_not_valid_for_clipped_interval',
           lambda:require(ctx.exact(abs(c[0]))[0]<=full_volume[1],
                          'empty clipped interval has c0, exceeding full-volume mean at mu=160'))
    reject('extra_factorial_in_ordered_chain_measure',
           lambda:require(F(1)==F(1,2),'causal order already fixes labelling'))
    reject('history_must_not_propagate_internally',
           lambda:require(base.forward([[F(0)]*3,[F(1),F(0),F(0)],[F(0),F(1),F(0)]])
                          ==base.forward([[F(0)]*3,[F(0)]*3,[F(0),F(1),F(0)]]),'history rows'))
    reject('density_below_floor_not_covered',
           lambda:require(abs(weight(c,F(1),3))<=CAP[21],'rho=q counterexample'))
    reject('poisson_tail_requires_ratio_below_one',
           lambda:poisson_mean(Fixed(30),F(POISSON_CUTOFF+2),[(1,1)],(1,1)))
    # Direct edge containing a vertex from another path: the Mecke insertion shifts its count.
    reject('other_path_insertions_cannot_be_ignored',
           lambda:require(weight(c,F(1,16),0)==weight(c,F(1,16),1),'Palm shift'))
    return caught

def main():
    archived=json.loads((ROOT/'evidence/RESULTS_v028.json').read_text())
    runs=[];raw={}
    # Grid refinement and independent arithmetic precision are separate checks.
    settings=[(120,32,16),(120,64,32),(160,64,32)]
    for digits,time_den,mu_den in settings:
        ctx=Fixed(digits)
        for theta in COEFFS:
            print(f'certify theta={theta}, digits={digits}, dt=1/{time_den}, dmu=1/{mu_den}',flush=True)
            weights=weight_table(ctx,theta)
            cells=poisson_cells(ctx,theta,mu_den,weights)
            kernel=kernel_table(ctx,theta,time_den,mu_den,cells)
            result,g0=volterra(ctx,kernel,time_den)
            pairs={key:ctx.fractions(value) for key,value in result.items()}
            raw[digits,time_den,mu_den,theta]=pairs
            samples=[dict(t=str(F(i,time_den)),h=pair_json(ctx,kernel[i]))
                     for i in [0,time_den,2*time_den,int(T*time_den),4*time_den,int((T+H)*time_den)]]
            runs.append(dict(theta=theta,integer_decimal_digits=digits,time_step=str(F(1,time_den)),
                             poisson_mean_step=str(F(1,mu_den)),poisson_cells=len(cells),
                             poisson_count_cutoff=POISSON_CUTOFF,kernel_samples=samples,
                             direct_history_at_zero=pair_json(ctx,g0),
                             **{key:interval_json(*value) for key,value in pairs.items()}))
    budgets=[]
    for theta in COEFFS:
        coarse=raw[120,32,16,theta];fine=raw[120,64,32,theta];precise=raw[160,64,32,theta]
        combined={}
        for key in fine:
            require(max(fine[key][0],precise[key][0])<=min(fine[key][1],precise[key][1]),'precision overlap')
            require(max(coarse[key][0],fine[key][0])<=min(coarse[key][1],fine[key][1]),'mesh overlap')
            combined[key]=(max(coarse[key][0],fine[key][0],precise[key][0]),
                           min(coarse[key][1],fine[key][1],precise[key][1]))
        old=next(r for r in archived['budgets'] if r['theta']==theta and r['kind']=='smoothed_1/16')
        ratios={}
        for key in ['B_active','B_joint']:
            require(combined[key][1]<F(old[key]['lower_fraction']),'no certified improvement')
            ratios[key]=interval_json(F(old[key]['lower_fraction'])/combined[key][1],
                                      F(old[key]['upper_fraction'])/combined[key][0])
        budgets.append(dict(theta=theta,**{key:interval_json(*value) for key,value in combined.items()},
                            v028_to_v029_bound_ratio=ratios))
    result=dict(version='0.29',base_commit=json.loads((ROOT/'evidence/SOURCES.json').read_text())['commit'],
                sources_verified=verify_sources(),chain_audit=chain_audit(),
                conditional_thinning_checks=thinning_audit(),rational_poisson_crosschecks=rational_spots(),
                constant_kernel_regressions=constant_kernel_audit(),negative_controls=negative_controls(),
                settings=settings,runs=runs,budgets=budgets,
                scope=dict(q='3/(16*pi)',rho_floor='3/pi',T='9/4',H='4',delta='1/100',Q='1',output_budget='1/1000',
                           domain='complete causal intervals; causal diamonds included'),
                method='HOLD',g1='HOLD',new_random_clouds=0,
                interpretation='enclosures of a sufficient positive-path amplification bound; not actual response or measured errors')
    encoded=(json.dumps(result,indent=2,sort_keys=True)+'\n').encode();out=ROOT/'results/RESULTS.json'
    if '--check' in sys.argv:
        require(out.read_bytes()==encoded,'byte replay mismatch');print('PASS: exact byte-for-byte v0.29 replay')
    else:
        out.write_bytes(encoded)
        print(json.dumps({'budgets':budgets,'chain_audit':result['chain_audit'],'negative_controls':result['negative_controls']},indent=2))

if __name__=='__main__':main()
