"""Rebuild rational evidence, apply the fixed window and compare saved outputs."""
from fractions import Fraction as F
import argparse,csv,json
from io import StringIO
from hashlib import sha256
from modell import ROOT,WINDOW,POS,ZERO,inputs,make,active
from intervall import I
from schranke import bounds as twin_bound
from zeuge import certify
from relaxation import basebox,inequalities,plus

def check_dual(tree,past,rel,edges,bounds):
    if 'empty' in tree:
        assert min(hi-lo for lo,hi in bounds.values())<0
        return 1
    if 'split' in tree:
        i=tree['split'];lo,hi=bounds[i];mid=(lo+hi)/2
        assert lo<mid<hi and len(tree['children'])==2
        leaves=0
        for side,child in zip([(lo,mid),(mid,hi)],tree['children']):
            other=bounds.copy();other[i]=side
            leaves+=check_dual(child,past,rel,edges,other)
        return leaves
    box,rows=inequalities(past,rel,edges,bounds)
    combined={};right=0
    for i,value in tree['dual']:
        lam=F(value);assert lam>0
        coeff,limit=rows[i]
        combined=plus(combined,coeff,lam);right+=lam*limit
    lower=sum(min(c*l,c*h) for key,c in combined.items() for l,h in [box[key]])
    assert lower>right
    return 1

def build():
    pair,sets=inputs()
    for title in ['Pruefplan','Zweite_Zukunft']:
        assert sha256((ROOT/(title+'.md')).read_bytes()).hexdigest()==(ROOT/(title+'.sha256')).read_text().split()[0]
    starts=json.loads((ROOT/'Startwerte.json').read_text());proofs=json.loads((ROOT/'Lineare_Zertifikate.json').read_text())
    guards={s:twin_bound(pair,s) for s in ['heavy','light']}
    cases=[];solutions={}
    for future,pasts in sets.items():
        k=14 if 14 in future else 18
        assert set(future)=={7,8,9,10,k,21}
        _,reference=make(pair,(),future)
        for side in ('heavy','light'):
            tag=f'{k}_{side}';rel,_=make(pair,(),future)
            solutions[tag]=certify(pair,side,rel,reference,starts[tag])
        for index,past in enumerate(pasts):
            rel,edges=make(pair,past,future)
            row=dict(future=list(future),past=list(past),relations=len(rel))
            if active(edges)==active(reference):
                row['status']='EXISTS_IN_WINDOW'
                for side in ['heavy','light']:
                    # Past--future boundary terms could change the input charge:
                    # check all cross-boundary nonzero receiver terms separately.
                    def cut(E):return {e:c for e,c in E.items() if e[0]<4<=e[1] and e[1] not in ZERO}
                    assert cut(edges)==cut(reference)
                    sol=solutions[f'{k}_{side}']
                    y=[I(*v) for v in sol['y']]
                    assert all(y[i].h<y[j].l for i,j in rel)
                    row[side]=f'{k}_{side}'
            elif k==14:
                assert tuple(past)==(0,1,2)
                inc={i:c for (i,j),c in edges.items() if j==21}
                assert inc=={15:16,16:-9,17:1,19:1,20:1,22:1}
                assert (15,16) in rel and (16,21) in rel and 21 in POS
                row.update(status='EXCLUDED',proof='D21_strictly_above_19')
            elif str(index) in proofs:
                # Check every topological premise for the uniform clock bounds.
                assert all((j,7) in rel for j in (15,16,17,18,19,20))
                assert all((0,j) in rel for j in (17,20)) and all((2,j) in rel for j in (15,16,19))
                assert (22,18) in rel and (22,21) in rel
                expect={7:-9,8:16,9:-8,18:1,21:1}
                def outgoing(i):return {j:c for (u,j),c in edges.items() if u==i and j not in ZERO}
                assert outgoing(22)==expect
                for a in (17,20):
                    trial={7:16,8:-8,18:-9,21:-9} if a in past else expect.copy()
                    if a==17:trial[18]-=F(1,10**11)
                    assert outgoing(a)==trial
                assert outgoing(18)=={7:1-F(1,10**11),8:-9,9:16,10:-8}
                assert not outgoing(21)
                row.update(status='EXCLUDED',proof='rational_linear_inequalities',
                           proof_id=index,leaves=check_dual(proofs[str(index)],past,rel,edges,basebox(pair,past,edges)))
            else:raise ValueError(f'Nachweis für Fall {index} fehlt')
            cases.append(row)
    result=dict(order_id=pair['order_id'],window=list(map(str,WINDOW)),solutions=solutions,cases=cases,
                earlier_twin_necessary_bounds=guards,physical_pilot_radii=[None]*8,physical_P3='NOT_RUN',P3_count=60)
    s=StringIO();tsv=csv.writer(s,delimiter='\t',lineterminator='\n')
    tsv.writerow(['Nachfolger','Vorgaenger','Praeparation','Status','x22_unten','x22_oben','Positive_im_Fenster','M_Q_unten','M_Q_oben','M_B_unten','M_B_oben','Nachweis'])
    for row in cases:
        for side in ['heavy','light']:
            key=row.get(side)
            sol=solutions.get(key)
            outputs=([*sol['x'][22],','.join(map(str,sol['positive_in_window'])) or 'keine',*sol['mass_q'],*sol['mass_b']] if sol else ['']*7)
            tsv.writerow([','.join(map(str,row['future'])),','.join(map(str,row['past'])) or '∅',side,row['status'],*outputs,row.get('proof',key or '')])
    dumps=lambda j:json.dumps(j,sort_keys=True,indent=2)+'\n'
    return {'Ergebnisse.json':dumps(result),'Stationaere_Feldboxen.json':dumps(solutions),'Fallregister.tsv':s.getvalue()}

if __name__=='__main__':
    if not __debug__:raise RuntimeError('Ohne -O ausführen')
    ap=argparse.ArgumentParser();ap.add_argument('--ausgabe',action='store_true');args=ap.parse_args()
    for n,body in build().items():
        if args.ausgabe:(ROOT/n).write_text(body,encoding='utf-8')
        else:assert (ROOT/n).read_bytes()==body.encode('utf-8'),n
    from collections import Counter
    print('N23-Ordnungen:',dict(Counter(row['status'] for row in json.loads((ROOT/'Ergebnisse.json').read_text())['cases'])))
    print('Beide Präparationen geprüft. Physische P3-Prüfpunkte: 60 NOT_RUN.')
