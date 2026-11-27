"""Aggregate the certified infimum bounds without assuming that the infimum is attained."""
import csv
import io
import json
from fractions import Fraction
from pathlib import Path

ROOT=Path(__file__).resolve().parent
WIDTHS=tuple(map(Fraction,('1/64','3/128','13/512','27/1024','55/2048')))


def folder(h):
    return ROOT if h==WIDTHS[0] else ROOT/'Fenstervergleich'/str(h).replace('/','_')


# Tick enclosures for Y3 and Y7, recomputed from the full collar before each run.
NORMALIZERS = ([-1833333334,-1833333333], [2000000000,2000000000])


def first_possible_y19(data):
    live = [(k,s,t) for k,sectors in data['trees'].items() for s,t in sectors.items() if t['open']]
    assert len(live)==1
    k,s,tree=live[0]
    assert k==data['witness']['case_id'] and s=='0'
    slabs=tree['slabs']
    lo,hi=data['window_ticks']
    assert slabs[0]['ticks'][0]==lo and slabs[-1]['ticks'][1]==hi
    assert all(a['ticks'][1]==b['ticks'][0] for a,b in zip(slabs,slabs[1:]))
    return min(z['ticks'][0] for z in slabs if z['open'])


def derive():
    lower=Fraction(0)
    upper=None
    ended=False
    last_full=None
    first_tick=None
    summary=[]
    columns=('Halbbreite','Gewichtsfaelle','Ausgeschlossen','Offen','Intervallbaeume',
             'Geschlossene_Blaetter','Offene_Blaetter')
    out=io.StringIO()
    writer=csv.writer(out,delimiter='\t',lineterminator='\n')
    writer.writerow(columns)
    for h in WIDTHS:
        f=folder(h)/'Ergebnisse.json'
        if not f.exists():
            assert ended
            continue
        assert not ended
        data=json.loads(f.read_text())
        assert Fraction(data['halfwidth'])==h
        proof=data['witness']
        assert Fraction(proof['upper_sum'])<1
        clocks=[[Fraction(x) for x in interval] for interval in proof['normalized_clocks'][:2]]
        hi=max(abs(x-Fraction(1,2)) for interval in clocks for x in interval)
        assert upper is None or upper==hi
        upper=hi
        tree=[tree for sectors in data['trees'].values() for tree in sectors.values()]
        closed=data['counts'].get('AUSGESCHLOSSEN',0)
        opened=data['counts'].get('OFFEN',0)
        assert closed+opened==data['case_count']==1342
        if opened==0:
            lower=h
            last_full=h
            assert all(t['open']==0 for t in tree) and lower<upper
        else:
            ended=True
            first_tick=first_possible_y19(data)
            y3,y7=NORMALIZERS[0][1],NORMALIZERS[1][1]
            assert y3<first_tick<y7
            # (Y19-Y3)/(Y7-Y3) decreases in each collar variable when Y3<Y19<Y7.
            slab_floor=Fraction(first_tick-y3,y7-y3)-Fraction(1,2)
            lower=max(lower,min(h,slab_floor))
        summary.append(str(h))
        writer.writerow((str(h),data['case_count'],closed,opened,sum(len(t.get('slabs', [None])) for t in tree),
                         sum(t['closed'] for t in tree),sum(t['open'] for t in tree)))
    assert upper is not None and 0<lower<upper
    return dict(last_complete_halfwidth=str(last_full),earliest_remaining_y19_tick=first_tick,witness=proof['case_id'],halfwidths=summary,infimum_lower=str(lower),
                infimum_upper=str(upper),bracket_width=str(upper-lower)),out.getvalue()
