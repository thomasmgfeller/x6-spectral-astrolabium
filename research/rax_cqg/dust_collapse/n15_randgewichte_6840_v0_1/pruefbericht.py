"""Recompute exact certificates, compare archived decisions and run independent checks."""
import argparse
import json
from hashlib import sha256

import auswerten as a
from kontrollen import full_box_check, four_histories


def compute():
    digest,name=(a.ROOT/'randkontrolle.sha256').read_text().split()
    assert sha256((a.ROOT/name).read_bytes()).hexdigest()==digest
    exact=a.run()
    data=json.loads((a.ROOT/'quellen/zeugen.json').read_text())['rows']
    approx,lobe=full_box_check()
    for rho in a.RHO:
        row=exact[str(rho)]
        four,controls=four_histories(rho,data[f'6840;{rho}']['coordinates'])
        row['same_boundary_four_histories']=four
        for r,test in row['two_histories']['ratios'].items():
            l,h=map(float,test['relative_abs_error'])
            assert l-1e-13<=controls[r]<=h+1e-13
        output=row['raw_full_box']
        error,modulus=approx[rho]
        assert error < float(output['relative_abs_error_upper']) and modulus >= float(output['amplitude_modulus_lower'])
        assert abs(lobe-float(output['left_reference_weight'][0]))<0.001
        assert [four[k]['gate'] for k in ('A','B')]==['FAIL','PASS']
    return exact,approx,lobe


if __name__=='__main__':
    if not __debug__:
        raise SystemExit('Please run without -O.')
    parser=argparse.ArgumentParser()
    parser.add_argument('--emit',action='store_true')
    args=parser.parse_args()
    exact,numeric,lobe=compute()
    content=json.dumps(exact,default=str,sort_keys=True,indent=2)+'\n'
    if args.emit:
        print(content,end='')
    else:
        for line in (a.ROOT/'SHA256SUMS').read_text().splitlines():
            digest,name=line.split(maxsplit=1)
            assert sha256((a.ROOT/name).read_bytes()).hexdigest()==digest,name
        assert content==(a.ROOT/'ergebnis.json').read_text()
        print('PASS: both pairs, ratio thresholds, four common-boundary controls and two full-box bounds.')
        print('Halton numerical cross-check (not a certificate):',numeric,'left weight',lobe)
        print('Physical P3: 60 x NOT_RUN')
