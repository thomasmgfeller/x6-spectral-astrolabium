"""Algebraic attribution diagnostics; no new integrals or fitted controls."""
import json
from flint import arb,acb,ctx
from core import *
from run_certified import summarize

def analyze(data):
    ctx.prec=128
    z=acb(0);scalar_sum=acb(0)
    for r in data['orbit_results']:
        weight=arb(r['multiplicity'])/33*acb(0,r['F4']).exp()
        z+=weight;scalar_sum+=weight*unpack(r['scalar_factor'])
    if not z.abs_lower()>0:raise ArithmeticError('gravity sum not separated from zero')
    average=scalar_sum/z
    ref=unpack(data['reference_scalar_factor'])
    totals={k:acb(0) for k in ('connected_remainder','scalar_mean_shift')}
    errors={k:arb(0) for k in totals}
    for r in data['orbit_results']:
        mult=arb(r['multiplicity'])/33;phase=acb(0,r['F4']).exp()
        d=unpack(r['dust_quadrature_ball']);err=arb(r['dust_error_bound'])
        factors={'connected_remainder':unpack(r['scalar_factor'])-average,'scalar_mean_shift':average-ref}
        for name,factor in factors.items():
            totals[name]+=mult*phase*d*factor;errors[name]+=mult*err*abs(factor)
    summary={k:summarize(totals[k],errors[k]) for k in totals}
    total=unpack(summary['connected_remainder']['certified_ball'])+unpack(summary['scalar_mean_shift']['certified_ball'])
    delta=unpack(data['amplitudes']['difference']['certified_ball'])
    if not total.overlaps(delta):raise ArithmeticError('decomposition disagrees with paired difference')
    return {'definition':'p_C=exp(i F4(C))/33; Z=sum p_C; Atilde=sum p_C A_C/Z',
            'not_a_probability_average':True,'primary_amplitudes_not_divided_by_Z':True,
            'gravity_sum_Z':pack(z),'scalar_average_Atilde':pack(average),
            'diagnostics':summary,'difference_decomposition_overlap':True,
            'interpretation':'Delta = connected finite amplitude remainder + change in scalar mean. Neither term is a proof of physical entanglement or causal dust creation.'}

if __name__=='__main__':
    data=json.loads((ROOT/'results/certified_mixing.json').read_text())
    out=analyze(data)
    (ROOT/'results/causation_diagnostics.json').write_text(json.dumps(out,indent=2,sort_keys=True)+'\n')
    print(json.dumps(out,indent=2))
