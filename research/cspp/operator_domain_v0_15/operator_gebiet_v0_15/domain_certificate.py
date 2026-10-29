"""Cover every H >= 4 at frozen rho=3/pi, epsilon=1/16; no grid-only inference."""
import json, time
from pathlib import Path
from flint import arb,ctx
from run import model, pack, dump, require, HERE

def compute(bits):
    ctx.prec=bits; start=time.monotonic()
    q=arb(3)/(16*arb.pi());ell=q**(-arb(1)/4);a=4*(q/6).sqrt()
    # For u>=0, u^j exp(-u) <= j^j exp(-j).
    C=1+9*(-arb(1)).exp()+32*(-arb(2)).exp()+36*(-arb(3)).exp()
    # d mu_H/dH in null coordinates: integrate 0<=s<=H.
    # integral (H-s)^2 ds = H^3/3; max H^3 exp(-H^2/16) at sqrt(24).
    M=a*q*arb.pi()/6*C*arb(24)**arb('3/2')*(-arb('3/2')).exp()
    nodes=[]; margin=arb('1/16');distance=margin/2
    for i in range(129):
        H=arb(4)+i*margin
        value=model.finite_mean_direct(ell,H)
        lower=(value+arb('1/2')).abs_lower()-M.abs_upper()*distance
        require(lower>arb('0.05'),'10-percent necessary RMS excluded throughout covered H cell')
        nodes.append({'H':pack(H),'mean':pack(value),'covered_bias_lower':pack(lower)})
    mu,_=model.previous_mean.mean_witness(ell)
    tail=model.previous_mean.gaussian_tail(ell,12,2)
    far=(mu+arb('1/2')).abs_lower()-tail.abs_upper()
    require(far>arb('0.05'),'all H>=12 excluded by monotone tail')
    lower=min([far]+[arb(z['covered_bias_lower'][0]) for z in nodes])
    out={'precision_bits':bits,'range':'every real H >= 4','rho':'3/pi','epsilon':'1/16',
         'step':'1/16','nearest_node_distance_bound':'1/32','global_kernel_bound':pack(C),
         'global_H_derivative_bound':pack(M),'covering_nodes':nodes,'all_H_ge_12_bias_lower':pack(far),
         'all_H_ge_4_relative_bias_lower':pack(2*lower),'decision':'ALL_PAST_DOMAIN_ENLARGEMENTS_REJECTED_FOR_FIXED_CELL',
         'interpretation':'Gaussian necessary witness; fixed density and kernel; no claim for modified boundary kernels or original detector error fractions',
         'elapsed_seconds':time.monotonic()-start}
    dump(HERE/f'results/DOMAIN_CERTIFICATE_{bits}.json',out)
    print('Domain cover',bits,'relative lower',2*lower,'seconds',out['elapsed_seconds'],flush=True)
if __name__=='__main__':
    import argparse
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True)
    compute(ap.parse_args().bits)
