"""C01 uncertainty budget following JCGM 100:2008 clause 8, for the documented input model."""
import argparse
from fractions import Fraction as F
import json
import math
from pathlib import Path
from scipy.stats import t
from c01 import DESIGN,NODE,loads,number,require

NAMES=("Y","P","A","C")
ONE_MILLION=10**6


def calculate(rec):
    require(isinstance(rec,dict) and rec.get("design")==DESIGN and rec.get("node")==NODE and rec.get("mode") in ("field","synthetic"),"scope or mode")
    require(isinstance(rec.get("scope_id"),str) and rec["scope_id"].strip(),"missing scope")
    base=dict(node=NODE,scope_id=rec["scope_id"],mode=rec["mode"],geometry_release=False)
    items=("paired_blocks","gain_certificate","transfer_rectangular","model_evidence")
    missing=[k for k in items if not rec.get(k)]
    if missing:return dict(base,status="HOLD_GUM_INPUT",missing=missing)
    md=rec["model_evidence"]
    for k in ("paired_repeatability","external_input_independence","type_b_dof","correction_inventory","approximate_95_percent","data_origin"):
        require(isinstance(md.get(k),str) and bool(md[k].strip()),"missing basis: "+k)
    require(rec.get("model")=="paired_YP_independent_A_and_C","unsupported joint model")
    data=rec["paired_blocks"]
    require(isinstance(data,list) and len(data)>=2 and all(isinstance(x,list) and len(x)==2 for x in data),"paired independent blocks required")
    data=[tuple(map(number,pair)) for pair in data]
    require(all(0<=x<=1 for row in data for x in row),"block probability out of range")
    n=len(data); y,p=(sum(row[i] for row in data)/n for i in (0,1))
    den=n*(n-1)
    vy=sum((yy-y)**2 for yy,pp in data)/den
    vp=sum((pp-p)**2 for yy,pp in data)/den
    cov=sum((yy-y)*(pp-p) for yy,pp in data)/den
    g=rec["gain_certificate"];a=number(g["estimate"]);U_a=number(g["expanded_U"]);k_a=number(g["coverage_factor"])
    c_in=rec["transfer_rectangular"];cl,ch=number(c_in["low"]),number(c_in["high"])
    require(F(99,100)<=a<=F(101,100) and U_a>=0 and k_a>0 and cl<=ch,"invalid Type B input")
    for src in (g,c_in):
        require(src.get("dof")=="infinite","this implementation requires justified effectively known Type B variances")
    va=(U_a/k_a)**2
    c=(ch+cl)/2; vc=(ch-cl)**2/12
    contrast=vy+a*a*vp-2*a*cov
    var1=contrast+p*p*va+vc
    exact=var1+va*vp
    d=y-a*p+c
    require(var1>0 and contrast>=0,"degenerate variance")
    uc=math.sqrt(float(var1)); u_exact=math.sqrt(float(exact))
    matrix=[[vy,cov,0,0],[cov,vp,0,0],[0,0,va,0],[0,0,0,vc]]
    jac=[F(1),-a,-p,F(1)]
    require(sum(jac[i]*matrix[i][j]*jac[j] for i in range(4) for j in range(4))==var1,"matrix crosscheck")
    nu=float(var1**2*(n-1)/contrast**2) if contrast else math.inf
    deg=math.floor(nu) if math.isfinite(nu) else math.inf
    from scipy.stats import norm
    # Project reporting rule: reject, rather than linearize, when the variance
    # check changes u by more than 0.001 ppm. Distributional adequacy is separate.
    nonlinear_ok=(u_exact-uc)*ONE_MILLION<=.001
    # Annex G approximation only for roughly normal output. A dominant rectangular
    # component is outside the implemented model's coverage route.
    coverage_ok=vc <= var1/10 and contrast>0 and n>=10
    valid_U=nonlinear_ok and coverage_ok
    k=(float(t.ppf(.975,float(deg))) if math.isfinite(deg) else float(norm.ppf(.975))) if valid_U else None
    signed=[float(v*float(dg)*ONE_MILLION) for v,dg in zip(map(lambda x:math.sqrt(float(x)),(vy,vp,va,vc)),jac)]
    return dict(base,status=("GUM_BUDGET_95_APPROX" if valid_U else "HOLD_COVERAGE_METHOD"),
        estimate_ppm=float(d*ONE_MILLION),input_order=NAMES,
        estimates=list(map(str,(y,p,a,c))),
        observation_pairs=n,standard_uncertainties=[math.sqrt(float(x)) for x in (vy,vp,va,vc)],
        input_degrees_of_freedom=[n-1,n-1,"infinite","infinite"],
        sensitivity=list(map(str,jac)),signed_standard_contributions_ppm=signed,
        covariance_matrix=[[str(v) for v in row] for row in matrix],
        cross_term_in_ppm_squared=float(-2*a*cov*ONE_MILLION**2),
        uc_first_order_ppm=uc*ONE_MILLION,uc_exact_moments_ppm=u_exact*ONE_MILLION,
        nonlinear_extra_variance_ppm2=float(va*vp*ONE_MILLION**2),
        effective_dof=nu if math.isfinite(nu) else "infinite",
        report_dof=deg if math.isfinite(deg) else "infinite",
        coverage=0.95 if valid_U else None,k=k if valid_U else None,
        expanded_U_ppm=k*uc*ONE_MILLION if valid_U else None,
        interval_ppm=[(float(d)-k*uc)*ONE_MILLION,(float(d)+k*uc)*ONE_MILLION] if valid_U else None,
        coverage_status="approximate; model and degrees of freedom must be justified",
        audit_risk_certified_by_GUM=False)


def assess_file(path):
    return calculate(loads(path.read_text()))


if __name__=="__main__":
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("record",type=Path)
    args=parser.parse_args()
    try:
        result=assess_file(args.record)
    except (ValueError,ArithmeticError,TypeError,KeyError,AttributeError,OSError) as exc:
        result={"status":"HOLD_GUM_INPUT","reason":str(exc),"geometry_release":False}
    print(json.dumps(result,indent=2,sort_keys=True,allow_nan=False))
