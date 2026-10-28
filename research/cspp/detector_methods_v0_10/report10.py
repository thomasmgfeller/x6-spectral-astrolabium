"""Post-run descriptive report only; never changes inputs or decisions."""
import argparse
import json
import statistics
from pathlib import Path
from common10 import HERE, PREVIOUS, ctx, arb, pack, gzread, unpack, write
from run10 import summarize


def describe():
    ctx.prec=256
    new=gzread(HERE/'results/BENCHMARK_128.json.gz')
    old=gzread(PREVIOUS/'results/BENCHMARK_128.json.gz')
    complete=[r for r in new['rows'] if r['status']=='COMPLETE']
    levels=[]
    for j in range(3):
        wave=[];compact=[];h3=[];ratios=[];passed=0;h3passed=0;bounds=[[],[]]
        for r in complete:
            prior=next(v for v in old['rows'] if v['key']==r['key'])
            for wi,w in enumerate(r['levels'][j]['windows']):
                radii=w['normalized_radii_upper'];wave+=radii[:4]
                if r['source_support_hits']:
                    compact.append(radii[4]);h3.append(radii[5])
                passed+=sum(w['field_pass'][:5]);h3passed+=w['field_pass'][5]
                for f in range(5):
                    prev=prior['windows'][wi]['normalized_component_radii_upper'][f]
                    if prev>0 and radii[f]>0:ratios.append(prev/radii[f])
                for i,b in enumerate(w['adapter_normalized_error_upper']):bounds[i].append(float(unpack(b).real.upper()))
        def extent(values):return [min(values),max(values)] if values else None
        levels.append({'grid':complete[0]['levels'][j]['n'] if complete else None,
            'original_H1_pass':passed,'additional_H3_pass':h3passed,'wave_radii_range':extent(wave),
            'nonzero_compact_H1_radii_range':extent(compact),'nonzero_compact_H3_radii_range':extent(h3),
            'old_v09_radius_over_new_radius_range':extent(ratios),
            'old_v09_radius_over_new_radius_median':statistics.median(ratios) if ratios else None,
            'H1_initial_error_upper_range':extent(bounds[0]),'H3_initial_error_upper_range':extent(bounds[1])})
    maximum={key:max(float(unpack(e[key]).real.upper()) for r in complete for e in r['numeric_controls']) for key in ['input_rounding','float_nodal_solve','node_radius']} if complete else {}
    return {'scope':'post-run description of known development clouds; bounds are not measured physical errors or noise',
            'decision':summarize(new['rows']),'levels':levels,'numeric_maxima':maximum,
            'support_hits':{r['key']:r['source_support_hits'] for r in complete},
            'ideal_Poisson_adapter_coverage':{'scope':'analytic geometry, not inference from eight binary64 archive clouds',
                'history_source_volume':'7*pi/16','volume_fraction':'21/8192','lambda_at_nu512':'21/16',
                'empty_probability':pack((-arb('21/16')).exp()),
                'nu_for_empty_probability_at_most_one_percent':pack(arb(8192)/21*arb(100).log()),
                'qualification':'source availability only; not sufficient operator, adapter or G1 budget'}}


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',type=Path);a=p.parse_args();result=describe()
    if a.out:write(a.out,result)
    print(json.dumps(result,indent=2))
