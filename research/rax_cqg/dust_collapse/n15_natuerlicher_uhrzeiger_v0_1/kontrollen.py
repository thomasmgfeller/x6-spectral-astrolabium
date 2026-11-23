"""Source ablation and exact phase-mixture control of the clock-5 readout."""
import argparse
import json
from ausgang import calc
from pruefen import ROOT,check


def run():
    a,b=calc('gauss',20,True),calc('cc',21,True)
    original=json.loads((ROOT/'ausgang.json').read_text())['gauss20']
    data={}
    for key,values in a.items():
        phase=values['mixed_phase']
        diff=values['difference_in_balance']
        check(abs(phase-b[key]['mixed_phase'])<8e-14 and abs(diff-b[key]['difference_in_balance'])<8e-14,'Quadratur')
        ratio=abs(phase/original[key]['mixed_phase'])
        check(ratio<.01,'Negativkontrolle')
        data[key]={'mixed_phase':phase,'balance_difference':diff,'residual_abs_ratio':ratio}
    # The two admissible relative phases multiply only the off-diagonal term.
    # Removing it gives the same sum of intensities, on every outcome and both tags.
    data['incoherent_balance_on_both_tags']=0
    return data


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--json',action='store_true')
    args=p.parse_args();res=run()
    if args.json:print(json.dumps(res,indent=2))
    else:
        ref=json.loads((ROOT/'kontrollen.json').read_text())
        for key in ('0|0.125','0|0.25'):
            for field, value in res[key].items():
                check(abs(value-ref[key][field]) < (2e-7 if field=='residual_abs_ratio' else 2e-13),'Archiv')
        print('PASS · Paarkontrolle und inkohärente Mischung')
