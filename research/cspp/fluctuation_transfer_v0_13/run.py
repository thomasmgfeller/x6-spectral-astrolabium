"""Produce declared predictive certificates at a fixed arithmetic precision."""
import argparse,hashlib,json,time
from pathlib import Path
from flint import arb,acb,ctx
from kernel import require
import transfer,oscillator,geometry
HERE=Path(__file__).resolve().parent


def encode(x):
    if isinstance(x,(arb,acb)):
        z=acb(x);return {'re':str(z.real),'im':str(z.imag)}
    if isinstance(x,dict):return {k:encode(v) for k,v in x.items()}
    if isinstance(x,(list,tuple)):return [encode(v) for v in x]
    return x

def unpack(x):return acb(arb(x['re']),arb(x['im']))

def freeze_check():
    for n,h in json.loads((HERE/'FREEZE.json').read_text())['sha256'].items():
        require(hashlib.sha256((HERE/n).read_bytes()).hexdigest()==h,'frozen input '+n)

def compute(bits,out):
    freeze_check();ctx.prec=bits;p=json.loads((HERE/'PROTOCOL.json').read_text());start=time.monotonic()
    from fractions import Fraction as F
    box,info=geometry.overlap([((-2,0,0,0),(0,0,0,0)),((-2,0,0,F(1,2)),(1,0,0,F(1,2)))],p['generic_overlap_box_depth'])
    require(box.contains(15*arb.pi()/32),'general overlap enclosure includes exact lens')
    d={'schema':p['schema'],'precision_bits':bits,'skeleton':transfer.predict_skeleton(),
       'oscillator':oscillator.predict(),'original_source':transfer.original_source_predictions(),
       'original_truncation':transfer.original_local_history_envelopes(p['source_path_order'],p['source_Poisson_count_cutoff']),
       'general_overlap_control':{'volume_enclosure':box,'box_inventory':info,'depth':p['generic_overlap_box_depth'],'analytic_volume':15*arb.pi()/32},
       'new_random_clouds':0,'fitted_parameters':0,'original_ensemble_moments':'NOT_EVALUATED','nonlocal_ensemble':'MODEL_HOLD',
       'overall_status':'METHOD_HOLD','G1':'HOLD','elapsed_seconds':time.monotonic()-start}
    out.write_text(json.dumps(encode(d),indent=2)+'\n');return d

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--bits',type=int,choices=[128,192],required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    r=compute(a.bits,a.out);print(json.dumps({'bits':a.bits,'seconds':r['elapsed_seconds'],'status':r['overall_status']}))
