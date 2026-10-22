"""Uniform interval certificate and exact local sensitivity along PR96's flow.
SPDX-License-Identifier: Apache-2.0
"""
import sys,json,hashlib
from pathlib import Path
import numpy as np
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'conformal_transport'))
from ct_run import inputs,bounds,flow,dot,atanh_bounds,F,read,save,sqrt_bounds,outward,boosted,exact_weights
from st_certificate import solve
from cs_interval import I,D,T,matvec,mm,verified_solve

def design(z,k):
    V=[b-a for a,b in zip(z[3],z[0])];c=[(a+b)/2 for a,b in zip(z[3],z[0])];R2=dot(V,V)/4;zz=[]
    for row in z:
        X=[v-a for v,a in zip(row,c)];q=dot(X,X);v=dot(V,X)
        denominator=1+k*v/R2+k*k*q/R2
        f=(k*(R2+q)+k*k*v)/(2*R2)
        zz.append([a+((1-k*k)*x+e*f)/denominator for a,x,e in zip(c,X,V)])
    y=[[a-b for a,b in zip(row,zz[4])] for row in zz[5:]]
    M=list(map(list,zip(*[[t,x,v,t*t,x*x,v*v,t*x,t*v,x*v] for t,x,v in y])))
    sums=[sum(row) for row in M]
    S=[[sum(a*b for a,b in zip(ri,rj))-si*sj/17 for rj,sj in zip(M,sums)] for ri,si in zip(M,sums)]
    return M,S

def weights_from(M,lam,scale):
    a=matvec(list(zip(*M)),lam);correction=sum(a)/17
    a=[v-correction for v in a]
    return [v/scale**2 for v in [-sum(a),*a]]

def exact_local(z,scale,U):
    # Automatic differentiation evaluated with zero-width fixed-point intervals
    # is an enclosure; exact sensitivity uses rational symmetric difference of
    # the rational design's analytic first-order coefficients via exact duals.
    from cs_exact import E
    M,S=design(z,E(F(0),F(1)))
    A=[[v.v for v in row] for row in S];Ap=[[v.d for v in row] for row in S]
    b=[F(v) for v in [0,0,0,-2,2,2,0,0,0]]
    lam=solve(A,b);lamp=solve(A,[-v for v in matvec(Ap,lam)])
    ww=weights_from(M,[E(v,d) for v,d in zip(lam,lamp)],scale)
    base=[v.v for v in ww];derivative=[v.d for v in ww]
    assert base==exact_weights(z,scale)
    n=sqrt_bounds(sum(v*v for v in base));d=sqrt_bounds(sum(v*v for v in derivative));cost=(sqrt_bounds(F(9,10)*U[0])[0],sqrt_bounds(F(9,10)*U[1])[1])
    sensitivity=(d[0]/n[1],d[1]/n[0])
    return dict(relative_weight_speed=outward(*sensitivity),transport_certificate_speed=outward(*cost),
      weight_speed_per_certificate_speed=outward(sensitivity[0]/cost[1],sensitivity[1]/cost[0]),
      derivative=[str(v) for v in derivative]),base,n

def certify_cell(z,scale,base,normbase,lo,hi,Qdata):
    M,S=design(z,D(I(lo,hi),1));A=[[v.v for v in row] for row in S];Ap=[[v.d for v in row] for row in S]
    Q=[[I(F(v)) for v in row] for row in Qdata]
    # Mean-value theorem, applied AFTER preconditioning, avoids interval
    # dependency inflation in Q*S. This encloses every parameter in the cell.
    Mc,Sc=design(z,D(I((lo+hi)/2),1))
    center=[[v.v for v in row] for row in Sc]
    QAp=mm(Q,Ap);QC=mm(Q,center);offset=I(-(hi-lo)/2,(hi-lo)/2)
    preconditioned=[[a+b*offset for a,b in zip(ra,rb)] for ra,rb in zip(QC,QAp)]
    identity=[[I(int(i==j)) for j in range(9)] for i in range(9)]
    qb=matvec(Q,list(map(I,[0,0,0,-2,2,2,0,0,0])))
    lam,eta=verified_solve(preconditioned,qb,identity)
    lamp,_=verified_solve(preconditioned,[-v for v in matvec(QAp,lam)],identity)
    centered_M=[[D(center.v+value.d*offset,value.d) for center,value in zip(cr,row)] for cr,row in zip(Mc,M)]
    ww=weights_from(centered_M,[D(v,d) for v,d in zip(lam,lamp)],scale)
    normupper=lambda vals:sqrt_bounds(sum(F(v.mag(),T)**2 for v in vals))[1]
    distance=normupper([v.v-I(b) for v,b in zip(ww,base)])/normbase[0]
    speed=normupper([v.d for v in ww])/normbase[0]
    return dict(lo=str(lo),hi=str(hi),inverse_residual_upper=outward(eta)[1],base_relative_gap_upper=outward(distance)[1],relative_speed_upper=outward(speed)[1])

def run(generate=False):
    for name,h in read(HERE/'freeze.json')['files'].items():assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    c=read(HERE/'contract.json');w,z0=inputs();z=boosted(z0);scale=F(w['scale']);_,U,_=bounds(w,z0)
    local,base,normbase=exact_local(z,scale,U)
    assert base==exact_weights(z0,scale)
    left,right=map(F,c['parameter_interval']);assert left==-right
    cost_lower=sqrt_bounds(F(9,10)*U[0])[0]
    assert cost_lower*atanh_bounds(right)[0]>F(c['tv_certificate_gate'])
    proposals=[] if generate else read(HERE/'proposals.json.gz');attempts=[];cursor=0;selected=[]
    for count in c['partition_levels']:
        rows=[];failed=False;level=[]
        for j in range(count):
            lo=left+(right-left)*j/count;hi=left+(right-left)*(j+1)/count
            if generate:
                _,S=design(z,(lo+hi)/2)
                Q=np.linalg.inv(np.array(S,dtype=float))
                data=[[str(float(v)) for v in row] for row in Q]
                level.append(data)
            else:data=proposals[cursor]['matrices'][j]
            try:rows.append(certify_cell(z,scale,base,normbase,lo,hi,data))
            except AssertionError:failed=True;break
        maxgap=max([F(r['base_relative_gap_upper']) for r in rows],default=F(10))
        symmetric=2*maxgap/(2-maxgap) if maxgap<2 else F(10)
        passed=not failed and len(rows)==count and symmetric<F(1,5)
        attempts.append(dict(cells=count,verified_cells=len(rows),contraction_failure=failed,relative_gap_upper=outward(symmetric)[1],passed=passed))
        if generate:proposals.append(dict(cells=count,matrices=level))
        cursor+=1
        print(json.dumps(attempts[-1]),flush=True)
        if passed:selected=rows;break
    assert selected,'UNRESOLVED: fixed partition budget exhausted'
    assert generate or cursor==len(proposals)
    L=max(F(r['relative_speed_upper']) for r in selected)
    direct=max(F(r['base_relative_gap_upper']) for r in selected)
    integrated=L*right;best=min(direct,integrated)
    summary=dict(status='CERTIFIED_CONTINUOUS_FAMILY_STOP',parameter_interval=c['parameter_interval'],
      covering_partition_cells=len(selected),transport_gate_implies_inside_interval=True,
      local_sensitivity={k:v for k,v in local.items() if k!='derivative'},
      uniform_relative_derivative_upper=outward(L)[1],uniform_base_relative_gap_upper=outward(best)[1],
      uniform_symmetric_relative_gap_upper=outward(2*best/(2-best))[1],
      uniform_gain_per_certificate_budget_upper=outward(L/cost_lower)[1],
      strong_gate='symmetric relative gap >1/5',strong_gate_excluded_in_covered_interval=True,
      attempts=attempts,
      scope='Uniform fixed-base-to-flow exclusion only along the PR96 one-parameter family within the current TV-upper-certificate gate; not arbitrary pairs of nonzero parameters. Not an actual-TV lower bound, global stability result, or exclusion of true close-law pairs outside this certified region. Inner landmarks move.')
    return proposals,selected,local,summary

if __name__=='__main__':
    generate='--generate' in sys.argv
    proposals,rows,local,summary=run(generate)
    for name,data in [('proposals.json.gz',proposals),('cells.json',rows),('local.json',local),('summary.json',summary)]:
        if generate:save(HERE/name,data)
        else:assert data==read(HERE/name)
    print(json.dumps(summary))
