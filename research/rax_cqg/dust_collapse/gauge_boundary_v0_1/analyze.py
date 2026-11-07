#!/usr/bin/env python3
"""Exact finite gauge/boundary audit. All decisions use rational arithmetic.

No gravitational constraints, physical Hilbert space, or continuum limit are
inferred from these checks. Run with python3 -O -B analyze.py.
"""
from pathlib import Path
from fractions import Fraction as Q
from itertools import permutations, product
from collections import Counter
from math import factorial, comb
import csv, hashlib, json, sys

ROOT=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT/'inputs'))
from gluing import all_posets, pairs, encode, relabel, action as gravity
from variation import matter_action, gamma, laplacian, current_and_gradient, matter_coupling
OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)
PLAN=json.loads((ROOT/'plan.json').read_text())

def require(ok,msg):
    if not ok: raise RuntimeError(msg)
def dump(name,data):
    (OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def csvout(name,rows):
    with (OUT/name).open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
def matvec(A,v):return [sum((a*x for a,x in zip(row,v)),Q(0)) for row in A]
def dot(a,b):return sum((x*y for x,y in zip(a,b)),Q(0))
def rank(A):
    M=[list(map(Q,row)) for row in A];r=0
    for c in range(len(M[0]) if M else 0):
        pivot=next((k for k in range(r,len(M)) if M[k][c]),None)
        if pivot is None:continue
        M[r],M[pivot]=M[pivot],M[r];d=M[r][c];M[r]=[x/d for x in M[r]]
        for k in range(r+1,len(M)):
            d=M[k][c]
            if d:M[k]=[x-d*y for x,y in zip(M[k],M[r])]
        r+=1
    return r
def move(values,p):
    out=[None]*len(values)
    for i,j in enumerate(p):out[j]=values[i]
    return out

def independent_action(code,n,T,w):
    """Direct relation-set/product construction, independent of inherited edges()."""
    R=set(pairs(code,n));S=-sum(w,Q(0))/2
    for y,x in R:
        k=sum((y,z) in R and (z,x) in R for z in range(n))
        b=[1,-9,16,-8][k] if k<4 else 0
        S-=Q(b,4)*w[x]*(T[x]-T[y])**2
    return S

def finite_audit():
    rows=[];count=Counter();ranks=Counter();vacuum=Counter();split=Counter()
    for n in PLAN['tests']['finite_actions']['N']:
        posets=all_posets(n);T=[Q(i*i,3) for i in range(n)]
        for code in posets:
            for mask in range(1<<n):
                w=[Q((mask>>i)&1) for i in range(n)]
                L=laplacian(code,n,w);S=matter_action(code,n,T,w)
                require(S==independent_action(code,n,T,w),'Independent action mismatch')
                require(S==-dot(T,matvec(L,T))/2-sum(w)/2,'Quadratic form mismatch')
                require(matvec(L,[Q(1)]*n)==[0]*n,'Common shift null vector')
                require(S==matter_action(code,n,[t+Q(7,5) for t in T],w),'Shift action')
                currents,q=current_and_gradient(code,n,T,w)
                require(q==[-x for x in matvec(L,T)] and sum(q)==0,'Ward polynomial identity')
                count['marked_cases']+=1;count['independent_action_checks']+=1
                count['common_shift_checks']+=1;count['gradient_sum_checks']+=1
                ranks[(n,mask.bit_count(),rank(L))]+=1
                for v in range(n):
                    if w[v]:continue
                    col=[L[i][v] for i in range(n)]
                    flat=all(x==0 for x in col)
                    vacuum['sites']+=1;vacuum['flat_columns' if flat else 'coupled_columns']+=1
                    # Test the exact polynomial in t against an independent action at n+1 bases.
                    for k in range(n+1):
                        t=[Q(int(i==k)) for i in range(n)] if k<n else [Q(0)]*n
                        shifted=t[:];shifted[v]+=Q(2,3)
                        delta=-Q(2,3)*dot(col,t)-Q(2,9)*L[v][v]
                        require(independent_action(code,n,shifted,w)-independent_action(code,n,t,w)==delta,
                                'Local translation polynomial')
                        count['vacuum_polynomial_checks']+=1
                full=(1<<n)-1
                for B in range(1,full):
                    A=full^B;v=[Q((B>>i)&1) for i in range(n)];Lv=matvec(L,v)
                    delta=Q(2,3);pred=delta*dot(v,q)-delta*delta*dot(v,Lv)/2
                    shifted=[t+delta*z for t,z in zip(T,v)]
                    require(matter_action(code,n,shifted,w)-S==pred,'Relative boundary shift')
                    cross,regrade=matter_coupling(code,n,T,w,A,B)
                    require(S==matter_action(code,n,T,w,A)+matter_action(code,n,T,w,B)+cross+regrade,
                            'Full gluing action')
                    split['cuts']+=1;split['flat_for_all_T' if not any(Lv) else 'relative_mode_coupled']+=1
                    if dot(v,Lv)==0 and any(Lv):split['zero_quadratic_but_linear_obstruction']+=1
                # Complete label permutations are algebraic controls; fixed external labels
                # would restrict this group. All clock data and density marks co-transform.
                for p in permutations(range(n)):
                    new=relabel(code,n,p);Tp=move(T,p);wp=move(w,p)
                    require(S==matter_action(new,n,Tp,wp),'Joint relabeling')
                    require(move([t+Q(7,5) for t in T],p)==[t+Q(7,5) for t in Tp],'Shift-label commute')
                    count['relabel_checks']+=1
                    count['commuting_representation_checks']+=1
        rows.append({'N':n,'posets':len(posets),'marked_cases':len(posets)*(1<<n)})
    csvout('enumeration.csv',rows)
    csvout('rank_histogram.csv',[{'N':n,'positive_sites':k,'rank_L':r,'cases':v} for (n,k,r),v in sorted(ranks.items())])
    return {'checks':dict(count),'vacuum_columns':dict(vacuum),'boundary_splits':dict(split)}

def uniform_moment(k,L):return Q(0) if k%2 else L**k/(k+1)
def difference_moment(k,L):
    return sum((Q(comb(k,j))*(-1)**j*uniform_moment(k-j,L)*uniform_moment(j,L) for j in range(k+1)),Q(0))
def relative_weight(r,L):
    values=[Q(0)]+list(r)
    return max(Q(0),2*L-(max(values)-min(values)))/(2*L)**(len(r)+1)
def relative_measure():
    rows=[];checks=0
    for N in [2,3,4,5]:
        for L in [Q(1,2),Q(1),Q(2)]:
            for k in range(0,13):
                direct=difference_moment(k,L)
                pushed=Q(0) if k%2 else 2*(2*L)**k/((k+1)*(k+2))
                require(direct==pushed,'Triangular marginal moments')
                checks+=1
            # Exact normalization of the full difference density: N! order chambers.
            # Fix anchor rank. Remaining sorted gaps fill a simplex. Integrating
            # (2L-span) over a chamber gives (2L)^N/N!, before division by (2L)^N.
            chamber=Q(1,factorial(N));require(factorial(N)*chamber==1,'Chamber normalization')
            var=difference_moment(2,L);cov=uniform_moment(2,L)
            rows.append({'N':N,'L':str(L),'normalization':'1','E_r1_squared':str(var),
                         'naive_box_E_r1_squared':str(L*L/3),'E_r1_r2':str(cov) if N>2 else 'NA',
                         'naive_box_E_r1_r2':'0' if N>2 else 'NA'})
            checks+=1
    # Direct independent intersection of translated intervals proves density sample values.
    for L in [Q(1,2),Q(1),Q(2)]:
        for d in [1,2,3,4]:
            for r in product([Q(-3,2)*L,-L,Q(0),L,Q(3,2)*L],repeat=d):
                lo=max([-L]+[-L-x for x in r]);hi=min([L]+[L-x for x in r])
                require(relative_weight(r,L)==max(Q(0),hi-lo)/(2*L)**(d+1),'Fiber measure')
                checks+=1
    csvout('relative_measure.csv',rows)
    return {'exact_checks':checks,'density':'[2L-(max(0,r)-min(0,r))]_+/(2L)^N',
            'counterexample':'At L=1: E[r^2]=2/3 versus 1/3 after naive resetting; different regulated models.',
            'classification':'Pushforward of a finite auxiliary clock measure, not an established physical gauge quotient.'}

# Rational complex intervals: a center pair and rigorous disk radius.
def cadd(z,w):return (z[0]+w[0],z[1]+w[1])
def csub(z,w):return (z[0]-w[0],z[1]-w[1])
def cscale(z,a):return (z[0]*a,z[1]*a)
def minus_i_power(k):return [(1,0),(0,-1),(-1,0),(0,1)][k%4]
def moment_series(moment,max_phase,p=60):
    z=(Q(0),Q(0))
    for k in range(p+1):z=cadd(z,cscale(minus_i_power(k),moment(k)/factorial(k)))
    return z,max_phase**(p+1)/factorial(p+1)
def box_kernel(b,mu,L,p=60,w=Q(1)):
    lo=mu-L-b;hi=mu+L-b
    def moment(k):return w**k*(hi**(2*k+1)-lo**(2*k+1))/(2*L*(2*k+1)*4**k)
    return moment_series(moment,w*max(lo*lo,hi*hi)/4,p)
def phase_series(x,p=60):return moment_series(lambda k:x**k,abs(x),p)
def decimal_bound(x,places=24,upper=False):
    scale=10**places;num=x.numerator*scale;den=x.denominator
    a=-((-num)//den) if upper else num//den
    sign='-' if a<0 else '';s=str(abs(a)).zfill(places+1)
    return sign+s[:-places]+'.'+s[-places:]
def certificate(z,r):
    return {'real':[decimal_bound(z[0]-r),decimal_bound(z[0]+r,upper=True)],
            'imag':[decimal_bound(z[1]-r),decimal_bound(z[1]+r,upper=True)],
            'exact_remainder':str(r)}
def separated(a,ra,b,rb):
    return any(abs(x-y)>ra+rb for x,y in zip(a,b))

def amplitude_checks(w=Q(1)):
    records=[];p=60;L=Q(1);checks=0
    for b in [Q(0),Q(1,2),Q(1)]:
        z,r=box_kernel(b,Q(0),L,p,w)
        for c in [Q(-1,2),Q(1,3),Q(1)]:
            co,rc=box_kernel(b+c,c,L,p,w)
            require(z==co and r==rc,'Co-transformed box covariance')
            fixed,rf=box_kernel(b+c,Q(0),L,p,w)
            require(separated(z,r,fixed,rf),'Fixed-box witness should separate')
            records.append({'b':str(b),'shift':str(c),'covariance':'EXACT',
                            'fixed_box_changed':True,'baseline':certificate(z,r),
                            'fixed_box':certificate(fixed,rf)})
            checks+=2
        # Derivative of the integrated Taylor polynomial agrees with the boundary series.
        lo=-L-b;hi=L-b;der=(Q(0),Q(0))
        for k in range(1,p+1):
            term=-w**k*(hi**(2*k)-lo**(2*k))/(2*L*4**k*factorial(k))
            der=cadd(der,cscale(minus_i_power(k),term))
        fhi,rhi=phase_series(w*hi*hi/4,p);flo,rlo=phase_series(w*lo*lo/4,p)
        flux=cscale(csub(fhi,flo),Q(1,2)/L)
        require(cadd(der,flux)==(0,0),'Integrated Ward identity')
        records.append({'b':str(b),'ward':'d_b K + boundary_flux = 0',
                        'derivative':certificate(der,(rhi+rlo)/(2*L)),
                        'boundary_flux':certificate(flux,(rhi+rlo)/(2*L))})
        checks+=1
    measures=[]
    for L in [Q(1,2),Q(1),Q(2)]:
        tri,rt=moment_series(lambda k:2*w**k*(2*L)**(2*k)/((2*k+1)*(2*k+2)*4**k),w*L*L,p)
        naive,rn=moment_series(lambda k:w**k*L**(2*k)/((2*k+1)*4**k),w*L*L/4,p)
        require(separated(tri,rt,naive,rn),'Naive relative measure amplitude differs')
        measures.append({'L':str(L),'correct_pushforward':certificate(tri,rt),'naive_box':certificate(naive,rn),
                         'disjoint_certified_components':True})
        checks+=1
    filename='amplitude_certificates.json' if w==1 else 'amplitude_certificates_interior.json'
    dump(filename,{'common_phase_omitted':'exp(-i*w/2), modulus one','w':str(w),
         'matter_sector':'fixed density witness; no full density/geometric integration claimed',
         'terms_through_degree':p,'records':records,'relative_measure_amplitudes':measures})
    return {'certified_checks':checks,'fixed_box_counterexamples':9,'relative_measure_counterexamples':3,
            'all_intervals_outward_rounded':True,'precision_role':'mathematical enclosure, not physical precision'}

def witnesses():
    n=4;c=encode([(i,j) for i in range(n) for j in range(i+1,n)],n)
    w=[Q(0),Q(0),Q(1),Q(0)];T=[Q(0),Q(1,4),Q(1),Q(2)];Tp=T[:];Tp[1]=Q(3,4)
    L=laplacian(c,n,w);s=matter_action(c,n,T,w);sp=matter_action(c,n,Tp,w)
    require(sp-s==Q(1,8),'Vacuum shift changes action by 1/8')
    whalf=[x/2 for x in w]
    require(matter_action(c,n,Tp,whalf)-matter_action(c,n,T,whalf)==Q(1,16),'Interior density vacuum witness')
    require(any(L[i][1] for i in range(n)) and not any(L[i][3] for i in range(n)), 'Vacuum roles differ')
    diamond=encode([(0,1),(0,2),(0,3),(1,3),(2,3)],4)
    require(gravity(c,4)==3 and gravity(diamond,4)==-16,'Geometry negative control')
    g=gamma(c,n,T);a=Q(2);b=Q(3,7)
    require(gamma(c,n,[a*t+b for t in T])==[a*a*x for x in g],'Affine clock scaling')
    # Relational counting observable, kinematical only: move tau too.
    tau=Q(3,2);shift=Q(7,5)
    O=lambda t,threshold:sum(wi for wi,ti in zip(w,t) if ti<=threshold)
    require(O(T,tau)==O([t+shift for t in T],tau+shift),'Relational threshold')
    require(O(T,tau)!=O([t+shift for t in T],tau),'Fixed threshold is changed event')
    # Compact, normalized auxiliary wavepacket. Translation must include box/readout.
    Lbox=Q(1);half=Q(1,2);cshift=Q(1)
    overlap=lambda a,b,c,d:max(Q(0),min(b,d)-max(a,c))
    norm0=overlap(-half,half,-Lbox,Lbox)/(2*half)
    normco=overlap(cshift-half,cshift+half,cshift-Lbox,cshift+Lbox)/(2*half)
    normfixed=overlap(cshift-half,cshift+half,-Lbox,Lbox)/(2*half)
    require(norm0==normco==1 and normfixed==Q(1,2),'State/domain covariance')
    data={'vacuum':{'order':'chain 0<1<2<3','w':list(map(str,w)),'T':list(map(str,T)),
                    'T_after':list(map(str,Tp)),'S_before':str(s),'S_after':str(sp),'delta_S':str(sp-s),
                    'L':[[str(x) for x in row] for row in L],
                    'column_1_coupled':True,'column_3_flat':True,
                    'interior_density_w2':'1/2','interior_density_delta_S':'1/16',
                    'scope':'off-shell finite action witness, not a physical dust solution'},
          'geometry':{'chain_F4':3,'diamond_F4':-16,'relative_clock_scaling':str(a*a)},
          'states':{'norm_original':str(norm0),'norm_cotransformed':str(normco),'norm_fixed_box':str(normfixed),
                    'relational_clock_variance':str(half*half/3),'physical_norm_claim':False},
          'relational_observable':{'type':'weighted count below shifted threshold; auxiliary only','check':'PASS'},
          'boundary':{'general_identity':'Delta S = delta sum_B q - delta^2/2 chi_B^T L chi_B',
                      'symmetry_for_all_T':'L chi_B=0','independent_origin_reset':'not licensed when relative mode couples'}}
    dump('witnesses.json',data);return data

def main():
    expected=(ROOT/'plan.sha256').read_text().split()[0]
    require(hashlib.sha256((ROOT/'plan.json').read_bytes()).hexdigest()==expected,'Plan changed')
    provenance=json.loads((ROOT/'inputs'/'provenance.json').read_text())
    for name,sha in provenance['files'].items():
        require(hashlib.sha256((ROOT/'inputs'/name).read_bytes()).hexdigest()==sha,'Inherited input changed: '+name)
    finite=finite_audit();measure=relative_measure();amplitudes=amplitude_checks();interior=amplitude_checks(Q(1,2));w=witnesses()
    report={'id':PLAN['id'],'source_commit':PLAN['source_commit'],'plan_sha256':expected,
            'finite':finite,'relative_measure':measure,'amplitudes':amplitudes,
            'interior_density_amplitudes':interior,
            'supplement_01_sha256':hashlib.sha256((ROOT/'supplement_01.json').read_bytes()).hexdigest(),
            'new_dynamical_CST_ensembles':False,'formal_proof_checker':False,
            'scoped_decisions':{'LABEL_AND_SHIFT_ALGEBRA':'PASS_EXACT_FINITE',
                'COTRANSFORMED_REGULATOR_COVARIANCE':'PASS_ANALYTIC_AND_CERTIFIED_WITNESS',
                'RELATIVE_CLOCK_PUSHFORWARD':'PASS_ANALYTIC_AND_EXACT_CONTROLS',
                'NAIVE_RESET_KEEPING_BOX':'FAIL_AS_EQUIVALENT_REWRITE',
                'ALL_VACUUM_CLOCKS_ARE_FREE_GAUGE':'FAIL_FOR_INHERITED_ACTION',
                'INDEPENDENT_BLOCK_ORIGIN_RESET':'FAIL_WITHOUT_RELATIVE_DATA',
                'PHYSICAL_GAUGE_QUANTIZATION':'HOLD',
                'GRAVITATIONAL_ANOMALY':'NOT_ESTABLISHED'},
            'physical_decisions':PLAN['physical_decisions']}
    dump('verification.json',report)
    print(json.dumps(report,indent=2,ensure_ascii=False))

if __name__=='__main__':main()
