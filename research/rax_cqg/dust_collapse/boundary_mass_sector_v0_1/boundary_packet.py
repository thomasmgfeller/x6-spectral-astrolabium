"""Two normalized boundary Fourier packets and tests of the charge they resolve."""
from fractions import Fraction as F
from cmath import exp
from math import pi,sqrt,sin
from charge import beta,delta,catalogue,order,row,I

def packet_value(tau,center,width):
    arg=width*tau/2
    sinc=1 if arg==0 else sin(arg)/arg
    return sqrt(width/(2*pi))*exp(-1j*center*tau)*sinc

def run():
    lower_delta=delta[0]
    assert 4*lower_delta>F(9,16)
    assert beta[0]>F(8,5)
    candidates=[k for k in catalogue() if 1 in order(k)[1]]
    mask=candidates[0]
    v=I[order(mask)[1].index(1)]
    assert row(1)==(0,-8,16,-9)
    # On the stratum with only w_v=1/2, choose s=-2*Delta+9/16.
    # At delta_offset=1/16 this gives p(0)=0 and H=beta/4>2/5.
    # A shifted phase has Fourier modulus independent of momentum when H != 0.
    widths={}
    for m in (F(1,4),F(4)):
        l,h=m*F(99,100),m*F(101,100)
        # H>2/5, so the phase excursion from the midpoint of the phase range
        # is strictly less than this bound. Integral modulus divided by band width
        # is >= cos(excursion) >= 1 - excursion^2/2.
        exc=(h*h-l*l)/(4*F(2,5))
        lower=1-exc*exc/2
        assert lower>=F(23,25)
        for tau in [0.,.5,2.]:
            # Direct Simpson quadrature of inverse Fourier transform.
            n=128;step=float((h-l)/n)
            vals=[exp(-1j*(float(l)+j*step)*tau) for j in range(n+1)]
            num=(vals[0]+vals[-1]+sum((4 if j%2 else 2)*vals[j] for j in range(1,n)))*step/3
            num/=sqrt(2*pi*float(h-l))
            assert abs(num-packet_value(tau,float(m),float(h-l)))<1e-12
        widths[str(m)]={"momentum_window":[str(l),str(h)],"fourier_packet_norm_squared":"1",
                        "relative_overlap_lower_bound_for_zero_initial_charge":str(lower)}
    return {"test_order":mask,"active_vertex":v,"single_active_density":"1/2","offset":"1/16",
            "inner_clock":"-2 Delta + 9/16","p_original":"0","source_curvature":"beta/4",
            "two_packets":widths,"overlap_between_distinct_prepared_momentum_modes":"0",
            "representation":"Additional collective translation tau on the full real line, standard L2(d tau). Test of the one-amplitude Fourier proposal, not the published compact packet.",
            "relative_overlap_normalization":"Magnitude of the complex integral averaged over each momentum band, divided by the constant Fourier modulus of a single chirp. Not a probability."}

def scale_audit(summary):
    # In units c=1 M_P3=G*M_rest/L_P3. Under unrenormalised matching kappa=1,
    # L_tau=ell and ell=L_P3 one would have g=1/(2*pi*sqrt(6)).
    # Use broad rigorous pi and sqrt bounds; the separation is ample.
    glo=F(1)/(2*F(22,7)*F(5,2))
    ghi=F(1)/(2*F(3)*F(12,5))
    max_raw=F(summary["maximum_of_type_suprema"][1])
    assert ghi*max_raw<F(99,25)
    return {"units":"c=1; dimensionless p=-d(S/hbar)/d tau. If equal to physical rest momentum, g=G*hbar/(L_tau*L_P3).",
            "hypotheses_for_equal_length_control":["unrenormalised identification of the finite F4 coefficient with kappa=1",
                  "L_tau=ell","ell=L_P3","same physical mass observable and orientation"],
            "hypothetical_gain":"1/(2*pi*sqrt(6))","enclosure":[str(glo),str(ghi)],
            "max_mass_all_raw_types_upper_under_these_hypotheses":str(ghi*max_raw),
            "number_of_types_with_heavy_band_in_equal_length_control":0,
            "physical_gain":None}
