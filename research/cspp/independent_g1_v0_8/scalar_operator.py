"""Analytic fields and BD action enclosed with Arb/Acb matrix arithmetic."""
from flint import arb,acb,acb_mat
import numpy as np
from support import check,old,legacy_fields,pack,unpack,norm,plan

def taper(q):
    if q<=1:return arb(1)
    if q>=3:return arb(0)
    check(q>1 and q<3,'cutoff branch resolved')
    s=(q-1)/2
    return 1/(1+(-1/s+1/(1-s)).exp())

def values(x,probe=False):
    rows=[];boxes=[]
    for point in x:
        t,a,b,z=map(lambda v:arb(float(v)),point)
        r=(a*a+b*b+z*z).sqrt();chi=taper(abs(t))*taper(r)
        poly=[arb(1),t,z,t*t,z*z,t*z]
        waves=[acb(0,k*z-(arb(k*k+1)).sqrt()*t).exp() for k in [0,2,4,8]]
        row=[acb(chi*v) for v in poly+waves];rows.append(row)
        if probe:
            check(abs(t)<1 and r<1,'reference probes strictly in plateau; cutoff derivatives vanish')
            boxes.append([acb(0),acb(0),acb(0),acb(-2),acb(2),acb(0)]+waves)
    return rows,boxes

def weights(maxn,e):
    e=arb(e);out=[]
    for n in range(maxn+1):
        if e==1:w=arb([1,-9,16,-8][n]) if n<4 else arb(0)
        else:
            u=e/(1-e)
            w=(1-e)**n*(1-9*n*u+8*n*(n-1)*u*u-arb(4)/3*n*(n-1)*(n-2)*u**3)
        out.append(w)
    return out

def compute(x,pc,nu,e,field_values=None):
    p=old.probes()[:21];vp,bp=values(p,True)
    vx=values(x)[0] if field_values is None else field_values
    fx,_=legacy_fields.fields(x);fp,_=legacy_fields.fields(p)
    fv=[[acb(complex(z)) for z in row] for row in fx]
    table=weights(int(pc.max(initial=0)),e)
    matrix=acb_mat([[table[int(n)] if n>=0 else arb(0) for n in row] for row in pc])
    exact=matrix*acb_mat(vx);rounded=matrix*acb_mat(fv)
    a=4*(arb(e)*arb(3)*nu/(512*arb.pi())/6).sqrt()
    ef=float(__import__('fractions').Fraction(e))
    numeric=old.apply(pc,nu/old.volume(4),ef,fx,fp)
    fields=[]
    for j,name in enumerate(plan()['fields']):
        ref=[row[j] for row in bp];pv=[row[j] for row in vp]
        act=[a*(-pv[q]+arb(e)*exact[q,j]) for q in range(21)]
        rnd=[a*(-acb(complex(fp[q,j]))+arb(e)*rounded[q,j]) for q in range(21)]
        num=[acb(complex(z)) for z in numeric[:,j]]
        denlo=max(norm(pv)[0],norm(ref)[0]);denhi=max(norm(pv)[1],norm(ref)[1])
        check(denlo>0,'nonzero fixed denominator')
        lo,hi=norm([v-r for v,r in zip(act,ref)]);lo=(lo/denhi).lower();hi=(hi/denlo).upper()
        inp=norm([r-v for r,v in zip(rnd,act)])[1]/denlo
        calc=norm([n-r for n,r in zip(num,rnd)])[1]/denlo
        radius=max(max(z.real.rad(),z.imag.rad()) for z in act+ref)
        check(radius<=arb(plan()['error_budgets']['reference_and_Arb_component_radius_max']),'reference/Arb radius budget')
        check(inp<=arb(plan()['error_budgets']['normalized_input_evaluation_RMS_upper_max']),'input evaluation budget')
        check(calc<=arb(plan()['error_budgets']['normalized_coefficient_and_sum_RMS_upper_max']),'coefficient and summation budget')
        for q in range(21):check(((act[q]-ref[q])+(rnd[q]-act[q])+(num[q]-rnd[q])-(num[q]-ref[q])).contains(0),'error identity')
        fields.append({'field':name,'operator_values':[pack(z) for z in act],
                       'reference_values':[pack(z) for z in ref],
                       'relative_operator_RMS':[pack(lo),pack(hi)],
                       'normalized_input_rounding_RMS_upper':pack(inp.upper()),
                       'normalized_coefficient_sum_RMS_upper':pack(calc.upper()),
                       'maximum_component_radius':pack(radius),
                       'numeric_values':[[float(z.real),float(z.imag)] for z in numeric[:,j]],
                       'certified_exceedance':bool(lo>arb('1/5'))})
    return fields
