"""Reproduce all certificates. Run from the extracted archive with Python 3.10+."""
import argparse
from fractions import Fraction as Q
from hashlib import sha256
import json

import schnitt
import traeger as t
import modell as m
from gegenprobe import estimate


def main():
    d=t.evaluate(); field=m.blind_sources(); rep=field['example']
    assert d['selected']==59262 and rep==2097151 and field['below_98']==len(field['rows'])==41
    geometry={};num={}
    for code in sorted({6840,d['selected'],rep}):
        geom={'scalar':m.scalar(code),'dust':{}}
        numerical=estimate(code)
        for rho,values in numerical.items():
            if code==rep:
                row=m.chain_pointer(code,field,rho)
                assert row['status']=='FAIL'
                l,h=row['relative_underread']
                assert float(l)<-values['gleichphasig']<float(h)
            else:
                row=m.dust(code,rho)
                assert all(row[key]['status']=='PASS' for key in ('raw','all_relative_lobe_phases'))
                assert abs(values['gleichphasig'])<float(row['raw']['relative_upper'])
                assert max(map(abs,values.values()))<float(row['all_relative_lobe_phases']['relative_upper'])
            geom['dust'][str(rho)]=row
        geometry[code]=geom;num[str(code)]={str(q):v for q,v in numerical.items()}
    ports=schnitt.evaluate(rep)
    assert ports['triangular_basis_checks']==15
    repair={}
    repaired_numeric=estimate(rep,reconstructed=True)
    for rho,numbers in repaired_numeric.items():
        item=m.dust(rep,rho,full_density_identity=True)
        assert item['all_relative_lobe_phases']['status']=='PASS'
        assert abs(numbers['gleichphasig'])<float(item['raw']['relative_upper'])
        assert max(map(abs,numbers.values()))<float(item['all_relative_lobe_phases']['relative_upper'])
        repair[str(rho)]=item
    num['2097151 mit rekonstruiertem Marker']={str(q):v for q,v in repaired_numeric.items()}
    tilts={}
    for amplitude in (Q(1,2),Q(4,5)):
        # Weighted median of 1/(1±a). Complex phases cannot lower the cost.
        c=1/(1+amplitude)
        minimum=(abs(c*(1+amplitude)-1)+abs(c*(1-amplitude)-1))/2
        assert minimum==amplitude/(1+amplitude)
        tilts[str(amplitude)]={'normalized_distance':amplitude,'common_scale_minimizer':c,'minimum':minimum}
    assert tilts['4/5']['minimum']>Q(39,100)
    assert not t.read('p3.json')['physical_pass']
    checkpoints=t.read('p3_pruefpunkte.json')
    assert len(checkpoints)==60 and all(row['checkpoint_id']=='P3' and row['execution']=='NOT_RUN' for row in checkpoints)
    return dict(support=d,by_type=geometry,source=field,clock_ports=ports,repaired_chain=repair,continuous_controls=tilts,physical_P3='60 x NOT_RUN'),num


if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O.')
    cli=argparse.ArgumentParser();cli.add_argument('--emit',action='store_true');args=cli.parse_args()
    for path,v in json.loads((t.ROOT/'herkunft.json').read_text())['files'].items():
        assert sha256((t.ROOT/path).read_bytes()).hexdigest()==v['sha256'],path
    for file in ('pruefplan','ergaenzung','quelltestplan','kettenplan','schnittplan','reparaturtest'):
        expected,name=(t.ROOT/(file+'.sha256')).read_text().split()
        assert sha256((t.ROOT/name).read_bytes()).hexdigest()==expected,name
    exact,numeric=main()
    result=json.dumps(exact,sort_keys=True,indent=2,default=str)+'\n'
    if args.emit:
        print(result,end='')
    else:
        for line in (t.ROOT/'SHA256SUMS').read_text().splitlines():
            digest,name=line.split(maxsplit=1)
            assert sha256((t.ROOT/name).read_bytes()).hexdigest()==digest,name
        assert result==(t.ROOT/'ergebnis.json').read_text()
        print('PASS: 6 growth laws, deletion witnesses, 3 Gaussian blocks, 41 field bounds, chain error, 128 clock subsets, repaired pointer.')
        for c,byrho in numeric.items():
            print(c,{rho:round(100*r['gleichphasig'],7) for rho,r in byrho.items()},'numerical signed relative errors in %')
        print('Physical P3: 60 x NOT_RUN')
