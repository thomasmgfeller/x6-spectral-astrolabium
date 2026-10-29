"""Finite original-detector gain for arbitrary normalized active equation defects."""
import argparse,json,time
from flint import arb,acb,ctx
import numpy as np
from run import ROOT,HERE,geometry,require,pack,unpack,loadgz,dump,digest,weights

def compute(bits):
    ctx.prec=bits;start=time.monotonic();rho=3/arb.pi();e=arb('1/16');a=4*(e*rho/6).sqrt();beta=a*e/(a+1)
    archive=np.load(ROOT/'scalar_pilot_v0_1/results/clouds.npz')
    v10=loadgz(ROOT/f'detector_methods_v0_10/results/BENCHMARK_{bits}.json.gz')
    out=[]
    for row in v10['rows']:
        key=row['key'];x=archive[key]
        cc,_,_,_,_=geometry.inventory(x,np.empty((0,4)))
        require(digest(cc)==row['counts_sha256'],'original interval counts')
        n=row['active_nodes'];nh=row['history_nodes'];w=[beta*z for z in weights(n,e)]
        windows=[]
        for window in row['levels'][-1]['windows']:
            q=list(map(unpack,window['query_coefficients']));require(len(q)==n,'original Q length')
            z=q.copy()
            # z_A=Q_A (I-K_AA)^(-1); distribute backwards in exact causal order.
            for i in range(n-1,nh-1,-1):
                for j in range(i):
                    c=int(cc[i,j])
                    if c>=0:z[j]+=z[i]*w[c]
            reference=list(map(unpack,window['history_transfer']))
            require(all(z[j].overlaps(reference[j]) for j in range(nh)),'independent adjoint matches saved T')
            windows.append({'residual_gain_lower':pack(sum(t.abs_lower() for t in z[nh:])),
                            'residual_gain_upper':pack(sum(t.abs_upper() for t in z[nh:])),
                            'history_gain_upper':pack(sum(t.abs_upper() for t in z[:nh])),
                            'active_equations':n-nh})
        out.append({'key':key,'windows':windows})
    result={'precision_bits':bits,'rows':out,'formula':'E_O = -mean(r_detector) - Q_A (I-K_AA)^(-1) r_A',
            'bound':'abs(E_O) <= abs(mean(r_detector)) + residual_gain_upper * sup(abs(r_A))',
            'scope':'arbitrary defects on these eight fixed geometries; no ensemble-wide or density-uniform stability assertion',
            'elapsed_seconds':time.monotonic()-start}
    dump(HERE/f'results/RESIDUAL_GAIN_{bits}.json',result)
    print('Residual gain',bits,'complete',result['elapsed_seconds'],flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True);compute(ap.parse_args().bits)
