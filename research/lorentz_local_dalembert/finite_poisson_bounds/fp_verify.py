"""Post-freeze reproducibility and exact witness-to-confidence bridge.
SPDX-License-Identifier: Apache-2.0
"""
import argparse,hashlib
from fp_common import *
from fp_run import compute
from fp_controls import controls

def bridge():
    witness=read(OLD/'witness.json');c=read(HERE/'contract.json')
    packet,obs,mask=input_record(witness['index'])
    assert [obs['counts'][i] for i in mask]==witness['counts']
    means=[count_box(n,c['chernoff_c']) for n in witness['counts']]
    z=[[[F(v) for v in row] for row in geometry] for geometry in witness['coordinates']]
    scale=F(witness['scale']);pi0,pi1=pi_bounds();slacks=[]
    for geometry in z:
        s=[]
        for (i,j),(lo,hi) in zip(witness['pairs'],means):
            q=interval(geometry,i,j);a,b=sqrt_bounds(q)
            factor=F(witness['rho'],12)*scale**3*q
            lower=factor*pi0*a;upper=factor*pi1*b
            assert lo<lower<upper<hi
            s.append(min(lower-lo,hi-upper))
        slacks.append(outward(min(s))[0])
    old=read(OLD/'certificate.json')
    return dict(status='BOTH_WITNESSES_INSIDE',index=witness['index'],intervals=len(means),
                minimum_mean_box_slack_lower=slacks,
                inherited_relative_weight_separation=old['relative_weight_separation'],
                inherited_uniform_recovery_lower_bound=old['normalized_minimax_lower_bound'],
                scope='Both exact PR88 geometries lie strictly inside this simultaneous confidence set. This bounds its target diameter, not testing distance, error probability or statistical minimax risk.')

def audit():
    frozen();c=read(HERE/'contract.json');summary=read(HERE/'summary.json')
    total=0;full=0;local=[];gated=[]
    for i in c['indices']:
        old=read(HERE/f'results/cloud-{i:02d}.json.gz')
        pivots=old.get('constants',{}).get('pivots')
        new=compute(i,pivots=pivots)
        assert new==old,i
        total+=old['intervals']
        if old['status']=='COMPLETE':
            assert old['constants']['center_in_confidence_box']
            assert old['constants']['exact_center_order']
            full+=old['full_box_ten_percent'];local.append(old['first_local_ten_percent'])
            gated.append(F(old['constants']['restricted_condition_domain_weight_norm_upper']))
            previous=None
            for row in old['bounds']:
                value=F(row['contraction_upper'])
                if previous is not None:assert value<=previous
                previous=value
    assert total==c['family_interval_total']==summary['interval_total']
    failure=confidence_bound(total,c['chernoff_c'])
    assert summary['family_failure_upper']==outward(failure)[1]
    assert summary['full_box_ten_percent']==full
    synthetic=controls();b=bridge()
    return dict(status='PASS',source_packets=len(c['indices']),intervals=total,
                exact_replays=len(c['indices']),synthetic_controls=len(synthetic['checks']),
                full_box_ten_percent=full,local_ten_percent_cases=sum(v is not None for v in local),
                local_first_k_range=[min(local),max(local)],
                restricted_weight_norm_envelope_range=[str(min(gated)),str(max(gated))],
                bridge=b,
                decision='COVERAGE_PROVED; FINITE_BOUND_THEOREM_PROVED; FULL_RADIUS_ACCURACY_NOT_CERTIFIED. No instability or impossibility conclusion; scientific HOLDs remain.')

def main():
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');args=p.parse_args()
    if (HERE/'SHA256SUMS').exists():
        for line in (HERE/'SHA256SUMS').read_text().splitlines():
            h,name=line.split('  ',1);assert hashlib.sha256((HERE/name).read_bytes()).hexdigest()==h,name
    result=audit()
    if args.write:save(HERE/'audit.json',result)
    else:assert result==read(HERE/'audit.json')
    print(result)

if __name__=='__main__':main()
