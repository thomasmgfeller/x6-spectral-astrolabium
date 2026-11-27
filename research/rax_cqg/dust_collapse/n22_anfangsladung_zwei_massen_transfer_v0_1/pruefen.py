"""Offline runner for the fixed-collar charge and mass comparison."""
import argparse
import csv
from fractions import Fraction as F
from hashlib import sha256
from io import StringIO
import json
from zipfile import ZipFile
from anfangsbasis import ROOT,experiment,PAST,LATE,QSTAR
from ladungsschranke import verify_linear,density_at_13


def run():
    for doc in ('Pruefplan','Ergaenzung','Dichte_an_13','Transferkontrolle'):
        assert sha256((ROOT/(doc+'.md')).read_bytes()).hexdigest()==(ROOT/(doc+'.sha256')).read_text().split()[0]
    with ZipFile(ROOT/'basis/Radiuspilot.zip') as zipfile:
        previous=json.loads(zipfile.read('Ergebnisse.json'))
        records=previous['checkpoints']
        assert len(records)==8 and all(r['R_phys'] is None for r in records) and previous['all_not_run']==60
    with experiment() as (y,w,order,edges,free):
        from feldroehre import POS
        from stationaer import solve
        from transferprobe import test_transfer
        assert set(free)==set(range(22))-set(PAST+LATE)
        b_star=round(sum(w[j] for j in POS)/(y[7]-y[3]),15)
        specs=json.loads((ROOT/'Startwerte.json').read_text())
        specs.extend(dict(name=f'Y{i}_{s}',mode='einzeln',index=i,shift=str(F(s,1024)))
                     for i in range(3) for s in (-1,1))
        rows=[solve(y,w,free,order,edges,spec,b_star) for spec in specs]
        dual=verify_linear(y,w,order,edges,json.loads((ROOT/'Lineare_Zeugen.json').read_text()))
        global_bound=density_at_13(y,order,edges,dual)
        constant=F(dual['constant'])
        coeff=list(map(F,dual['clock_coefficients']))
        for row in rows:
            predlo=predhi=constant
            for a,(lo,hi) in zip(coeff,row['y']):
                u,v=sorted((a*F(lo),a*F(hi)))
                predlo+=u;predhi+=v
            qlo,qhi=map(F,row['Q'])
            assert max(predlo,qlo)<=min(predhi,qhi)
            assert qlo>F(global_bound['Q_strict_lower'])
            assert F(row['normalized'][13][1])<F(global_bound['x13_upper'])
        # Verify the four crossed states at the exact targets and their resulting window occupancies.
        assert {(F(r['target_Q'])/QSTAR,F(r['target_B'])/b_star) for r in rows[:4]}=={
            (q,b) for q in (F(1),F(19,20)) for b in (F(1),F(4,5))}
        byname={r['name']:r for r in rows}
        degenerate=byname['Gleiche_Ladung_065']
        assert F(degenerate['target_Q'])==QSTAR and F(degenerate['target_B'])==F(13,20)*b_star
        ambiguity=(b_star-F(degenerate['target_B']))/(b_star+F(degenerate['target_B']))
        assert ambiguity==F(7,33)
        trials=[test_transfer(r,F(1,16),y,b_star,edges,free,order) for r in rows if r['mode']=='einzeln']
        from pilotfelder import paths,read_box
        from transport import packing
        transport_proposals=json.loads((ROOT/'Transportzeugen.json').read_text())
        crossings={}
        for row in rows:
            if row['mode']!='einzeln' and row['name']!='Referenz':continue
            x,wbox,occupied,nodes=read_box(row)
            chains=paths(nodes,order)
            result=packing(chains,nodes,x,wbox,transport_proposals[row['name']])
            # Every weight entering the objective and constraints is scaled by
            # the same positive factor. The normalized optimum is unchanged.
            crossings[row['name']]=dict(fraction=result['fraction'],crossing=result['crossing'],
                    inner_0_21=sorted(j for j in range(22) if (0,j) in order and (j,21) in order),
                    clock_span_0_21=[str(x[21][0]-x[0][1]),str(x[21][1]-x[0][0])])
        exact=test_transfer(byname['Gemeinsame_Aenderung_09'],F(5,72),y,b_star,edges,free,order)
        assert all(F(v[0])<=F(1,4)<=F(v[1]) for v in (exact['mass_Q'],exact['mass_B']))
        eligible=[r for r in trials if r['Q_within_two_percent'] and r['B_within_two_percent'] and r['positive_zero_pairs']]
        selected=min(eligible,key=lambda r:max(abs(F(v)) for k in ('relative_error_Q','relative_error_B') for v in r[k]))
        assert len(eligible)==2
        light=byname[selected['case']]
        dark=byname['Referenz']
        def export(row,scale):
            return dict(case=row['name'],clock_box=row['y'],
                        weight_box=[list(map(str,[F(v)*(1 if j in PAST else scale) for v in ends])) for j,ends in enumerate(row['w'])],
                        normalized_clocks=row['normalized'],contacts=row['contacts'],positive_in_window=row['positive'],
                        zero_in_window=row['empty'])
        pair=dict(study='CST-DUST N22',order_id='216141/229383/0/+',relation=sorted(order),reference_Q=str(QSTAR),
                  reference_B=str(b_star),nominal_heavy='4',nominal_light='1/4',normalized_window=['15/32','17/32'],
                  heavy=export(dark,F(1)),light=export(light,F(1,16)),light_mass_diagnostics=selected,
                  physical_radius_heavy=None,physical_radius_light=None,external_mass_standard=None)
        return dict(selected_pair=pair,reference_charge=str(QSTAR),reference_density_mass=str(b_star),cases=rows,
                    charge_ambiguity_for_B=str(ambiguity),fixed_field_bound=global_bound,
                    affine_proof=dual,transport_comparison=crossings,tests=trials,fitted_control=exact,physical_targets=records,
                    P3_NOT_RUN=previous['all_not_run'])


def files(result):
    def tsv(header,rows):
        s=StringIO();w=csv.writer(s,delimiter='\t',lineterminator='\n')
        w.writerow(header);w.writerows(rows);return s.getvalue()
    fields=tsv(['Fall','Gleichungen','Q_unten','Q_oben','B_unten','B_oben','x19_unten','x19_oben','Positiv_im_Fenster','Leer_im_Fenster'],
        [[r['name'],r['dimension'],*r['Q'],*r['B'],*r['normalized'][19],','.join(map(str,r['positive'])),','.join(map(str,r['empty']))] for r in result['cases']])
    transfer=tsv(['Fall','Gewichtsskala','M_Q_unten','M_Q_oben','M_B_unten','M_B_oben','Q_in_2Prozent','B_in_2Prozent','Gemischter_Kontakt'],
        [[r['case'],r['weight_scale'],*r['mass_Q'],*r['mass_B'],r['Q_within_two_percent'],r['B_within_two_percent'],bool(r['positive_zero_pairs'])] for r in result['tests']+[result['fitted_control']]])
    return {'Ergebnisse.json':json.dumps(result,indent=2,sort_keys=True)+'\n','Fallregister.tsv':fields,'Transferregister.tsv':transfer,
            'Vergleichspaar.json':json.dumps(result['selected_pair'],indent=2,sort_keys=True)+'\n'}


if __name__=='__main__':
    if not __debug__:raise RuntimeError('Python ohne -O erforderlich')
    parser=argparse.ArgumentParser()
    parser.add_argument('--ausgabe',action='store_true')
    args=parser.parse_args()
    result=run()
    for name,body in files(result).items():
        path=ROOT/name
        if args.ausgabe:path.write_text(body,encoding='utf-8')
        else:assert path.read_text(encoding='utf-8')==body,name
    print('Stationäre Fälle:',len(result['cases']))
    print('Beide Modellablesungen in der 2-%-Toleranz:',sum(r['Q_within_two_percent'] and r['B_within_two_percent'] for r in result['tests']),'von 6')
    print('Physische Radiuswerte offen:',len(result['physical_targets']))
