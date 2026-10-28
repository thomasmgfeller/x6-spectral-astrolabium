"""Validated triangular propagation and four-term observable error accounting."""
import numpy as np
from flint import arb,acb,ctx
from common import old,check,balls

def coefficient_table(maxn,nu,epsilon,mass):
    e=arb(epsilon);rho=arb(3)*nu/(512*arb.pi());a=4*(e*rho/6).sqrt();beta=a*e/(a+mass*mass)
    table=[]
    for n in range(maxn+1):
        if e==1:w=arb([1,-9,16,-8][n]) if n<4 else arb(0)
        else:
            u=e/(1-e)
            w=(1-e)**n*(1-9*n*u+8*n*(n-1)*u*u-arb(4)/3*n*(n-1)*(n-2)*u**3)
        table.append(beta*w)
    return table

def edges(counts,table):
    return [[(int(j),table[int(row[j])]) for j in np.flatnonzero(row>=0) if table[int(row[j])]!=0] for row in counts]

def dot_row(row,values,ncols,absolute=False):
    out=[acb(0) for _ in range(ncols)]
    for j,w in row:
        if absolute:w=abs(w)
        v=values[j]
        for c in range(ncols):out[c]+=w*v[c]
    return out

def solve(counts,probe_counts,nu,epsilon,mass,history,nh):
    """Every ball coefficient and RHS is enclosed; strict lower triangle ends recursion."""
    n=len(counts);nc=len(history[0]);check(len(history)==nh and nh>0,'history inventory')
    table=coefficient_table(max(int(counts.max(initial=0)),int(probe_counts.max(initial=0))),nu,epsilon,mass)
    erows=edges(counts,table);prows=edges(probe_counts,table)
    values=[list(v) for v in history];amplification=[[acb(1)] for _ in range(nh)]
    for i in range(nh,n):
        check(all(j<i for j,w in erows[i]),'strict causal solve ordering')
        values.append(dot_row(erows[i],values,nc));amplification.append(dot_row(erows[i],amplification,1,True))
    out=[dot_row(row,values,nc) for row in prows]
    gain=[dot_row(row,amplification,1,True)[0].real for row in prows]
    return out,values,gain,erows,prows

def float_solve(c,pc,x,p,nu,e,mass,h):
    rho=nu/old.volume(4);z=np.zeros_like(h);zp=np.zeros((len(p),h.shape[1]),complex)
    return old.propagate(c,pc,x,p,rho,float(e),h,z,zp,[mass]*h.shape[1])

def enclose_norm(z):
    lo=(sum(v.abs_lower()**2 for v in z)/len(z)).sqrt()
    hi=(sum(v.abs_upper()**2 for v in z)/len(z)).sqrt()
    return {'lower':balls.encode(lo),'upper':balls.encode(hi)}

def detector_weights(p):
    center=[arb(0),arb(0),arb('3/2')];w=[]
    for point in p[21:28]:
        r2=sum((arb(float(point[j+1]))-center[j])**2 for j in range(3));h=1-r2/arb('1/4')
        check(h>0,'point diagnostic inside unchanged detector support');w.append((-1/h).exp())
    s=sum(w);return [x/s for x in w]

def intensity(z,w):return sum(a*(x.real**2+x.imag**2) for a,x in zip(w,z))

def field_result(out,truth,float_out,p,nfields,index,order,gain):
    # Groups are oracle history, P1 exact, P3 exact, P1 rounded, P3 rounded.
    g=1 if order==1 else 2
    reference=[v[index] for v in truth]
    oracle=[v[index] for v in out]
    adapter=[v[g*nfields+index] for v in out]
    rounded=[v[(g+2)*nfields+index] for v in out]
    numeric=[acb(complex(v[(g-1)*nfields+index])) for v in float_out]
    components={'operator_and_domain':[a-b for a,b in zip(oracle,reference)],
                'initial_extension':[a-b for a,b in zip(adapter,oracle)],
                'initial_evaluation_rounding':[a-b for a,b in zip(rounded,adapter)],
                'linear_solve_and_coefficient_rounding':[a-b for a,b in zip(numeric,rounded)]}
    total=[a-b for a,b in zip(numeric,reference)]
    for j,z in enumerate(total):check((sum(v[j] for v in components.values())-z).contains(0),'signed error telescopes')
    w=detector_weights(p);states=[reference,oracle,adapter,rounded,numeric]
    intensities=[intensity(z[21:28],w) for z in states]
    stages=[]
    for i,key in enumerate(components):
        before=states[i][21:28];err=components[key][21:28]
        bound=sum(a*(2*b.abs_upper()*e.abs_upper()+e.abs_upper()**2) for a,b,e in zip(w,before,err))
        delta=intensities[i+1]-intensities[i]
        check(delta.abs_lower()<=bound.abs_upper(),'intensity perturbation upper bound compatible')
        stages.append({'component':key,'signed_intensity_change':balls.encode(delta),'absolute_change_upper':balls.encode(bound.abs_upper())})
    check((sum(balls.decode(s['signed_intensity_change']).real for s in stages)-(intensities[-1]-intensities[0])).contains(0),'observable budget telescopes')
    norm=enclose_norm(total);den=enclose_norm(reference)
    denomlo=balls.decode(den['lower']).real
    check(denomlo>0,'fixed relative RMS denominator')
    rel=balls.decode(norm['upper']).real/denomlo
    return {'adapter_order':order,'probe_values':[balls.encode(z) for z in adapter],
            'actual_float_probe_values':[[float(z.real.mid()),float(z.imag.mid())] for z in numeric],
            'component_RMS':{key:enclose_norm(v) for key,v in components.items()},
            'total_RMS':norm,'relative_total_RMS_upper':balls.encode(rel),
            'reference_RMS':den,'relative_10pct_screen':'WITHIN' if rel<=arb('0.1') else 'EXCEEDS' if balls.decode(norm['lower']).real/balls.decode(den['upper']).real>arb('.1') else 'UNDECIDED',
            'history_linf_to_each_probe_upper':[balls.encode(x) for x in gain],
            'detector_point_intensity':{'reference':balls.encode(intensities[0]),'exact_adapter_discrete':balls.encode(intensities[2]),
             'actual_float':balls.encode(intensities[-1]),'components':stages,'scope':'seven fixed weighted point probes, not spatial detector integration'}}
