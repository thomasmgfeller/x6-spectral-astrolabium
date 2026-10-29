"""Analytic controls, all executed before archive production."""
from fractions import Fraction as F
import numpy as np
from common10 import arb, acb, ctx, check, previous, pack
from time_integral import integrate, prepare, time_coefficients, ball, ARRIVAL_BITS, WEIGHT_BITS, sector, arrivals
from adapter import polynomials, evaluate_polynomial, constants, history_bounds


def radial_remaining(t,a=F(0),b=F(1,2)):
    r0=max(F(0),min(F(1,2),a-t));r1=max(F(0),min(F(1,2),b-t))
    def antiderivative(r):return (b-t)*r**3/3-r**4/4
    return 24*((b-a)*r0**3/3+antiderivative(r1)-antiderivative(r0))/(b-a)


def compute():
    ctx.prec=192
    controls=[]
    x=np.array([[-.25,0,0,1.5],[0,0,0,1.5],[.25,0,0,1.5]])
    counts=np.array([[-1,-1,-1],[0,-1,-1],[1,0,-1]],dtype=np.int32)
    table=list(map(arb,[1,-2,3,1]))
    result=integrate(x,counts,table,[['0','1/2']],[2,4])
    for y in range(3):
        expected=F(0)
        for k,z in enumerate(range(y,3)):
            coefficient=[1,-2,3][k]-([1,-2,3][k-1] if k else 0)
            expected+=coefficient*radial_remaining(F(float(x[z,0])))
        exact=arb(expected.numerator)/expected.denominator
        check(all(level['q'][0][y].contains(exact) for level in result),'signed concentric cone integral')
    controls.append('signed_multi_event_exact_radial_time_integrals')
    # The last event enters at t=1/4; its reference is not assumed zero.
    check(radial_remaining(F(0))==F(1,4),'single-cone analytic value')
    controls.append('single_cone_average_one_quarter')
    x2=np.array([[-4,0,0,1.5],[-3,0,0,1.5]])
    c2=np.array([[-1,-1],[0,-1]],dtype=np.int32)
    const=integrate(x2,c2,[arb(-3)]*3,[['0','1/2']],[2])[0]['q'][0]
    check(all(q.contains(-3) and q.rad()<arb('1e-20') for q in const),'constant exact ball volume')
    controls.append('constant_exact_volume_no_sphere_boundary_hull')
    # Both successors can cross in arrival order; use two exact realizations.
    counts=np.array([[-1,-1,-1],[0,-1,-1],[0,-1,-1]])
    prepared=prepare(table,counts);s=1<<ARRIVAL_BITS
    arrival=[(-s,-s),(s//8,3*s//8),(s//8,3*s//8)]
    enclosure=time_coefficients(arrival,prepared,['0','1/2'])
    for times in [(-s,s//8,3*s//8),(-s,3*s//8,s//8),(-s,s//4,s//4)]:
        q=time_coefficients([(t,t) for t in times],prepared,['0','1/2'])
        check(all(a<=c<=d<=b for (a,b),(c,d) in zip(enclosure,q)),'crossing and tied arrival orders')
        # Direct integration of the state at each interval midpoint.
        cuts=sorted(set([0,s//2]+[t for t in times if 0<t<s//2]))
        truth=F(0)
        for a,b in zip(cuts,cuts[1:]):
            t=F(a+b,2);past=[j for j,z in enumerate(times) if z<t]
            n=sum(counts[j,0]>=0 for j in past)
            truth+=F(b-a,s)*[1,-2,3][n]
        check(ball(*enclosure[0],ARRIVAL_BITS+WEIGHT_BITS).contains(arb(truth.numerator)/truth.denominator),'direct event sweep agrees')
    controls.append('crossing_tied_arrivals_and_independent_event_sweep')
    s=1<<ARRIVAL_BITS;box=[(0,0),(0,0),(3*s//2,3*s//2)]
    for t in [np.nextafter(.375,-np.inf),.375,np.nextafter(.375,np.inf)]:
        lo,hi=arrivals([[t,0,0,1]],box)[0]
        exact=F(float(t))+F(1,2)
        check(F(lo,s)<=exact<=F(hi,s),'exact-null plus/minus ULP arrival')
    controls.append('null_and_adjacent_binary64_arrivals')
    ps=polynomials();A=arb(1)
    for xyz in [[0,0,0],[.125,.0625,-.125],[.25,0,.125]]:
        point=[-1]+xyz
        f,g,l2,l3=previous.initial_data.bump_jets(point,1,A)
        poly=evaluate_polynomial(ps[1],list(map(arb,xyz)))
        check((poly*f+l2).contains(0),'independent first L derivative formula')
    check([len(p) for p in ps]==[1,9,52,170],'exact derivative polynomial inventory')
    controls.append('Gaussian_integer_derivatives_vs_independent_bump_L')
    for tau in ['-3','-1/8','0','1/8','3']:
        for k in [0,2,4,8]:
            z=arb(tau)*(arb(k*k+1)).sqrt()
            check((z.cos()-1).abs_upper()<=z*z/2+arb('1e-40'),'H1 cosine remainder')
            check((z.cos()-1+z*z/2).abs_upper()<=z**4/24+arb('1e-40'),'H3 cosine remainder')
    controls.append('Taylor_remainder_controls')
    for point in [[-2,1,0,0],[-3,0,0,-1]]:
        jets=previous.initial_data.bump_jets(point,1,A)
        check(all(z.is_zero() for z in jets),'compact jets vanish outside support')
        check(all(previous.initial_data.extension(point,jets,o).is_zero() for o in [1,3]),'missed source stays zero')
    c=constants();check(all(z>0 for z in c.values()),'nonzero approximation error upper bounds')
    controls.append('zero_source_history_is_not_zero_error_certificate')
    from run10 import forward,evaluate
    x=np.array([[-2,0,0,0],[-1.25,0,0,0],[0,0,0,0],[.5,0,0,0]])
    counts=np.array([[i-j-1 if j<i else -1 for j in range(4)] for i in range(4)],dtype=np.int32)
    history,values,edges,table,scales,errors=forward(x,counts,arb(1))
    out,t=evaluate(list(map(arb,[1,-2,3,1])),history,values,edges)
    w0,w1,w2=table[:3]
    exact_t=[1+3*w1+w2+w0*w1,-2+3*w0+w1+w0*w0]
    for a,b in zip(t,exact_t):check(a.overlaps(b),'explicit four-node transfer polynomial')
    for i in range(6):check(out[i].overlaps(sum(a*h[i] for a,h in zip(exact_t,history))),'synthetic H1/H3 full transfer')
    controls.append('full_initial_adapter_solve_and_adjoint_transfer')
    return {'status':'PASS','controls':controls,'count':len(controls),
            'normalized_remainder_constants':{str(o):pack(v) for o,v in c.items()}}


if __name__=='__main__':
    import json
    print(json.dumps(compute(),indent=2))
